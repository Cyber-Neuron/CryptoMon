import pkg from 'pg';
const { Pool } = pkg;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || process.env.POSTGRES_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    
    console.log('🔍 钱包余额API - 所有接收到的参数:');
    for (const [key, value] of searchParams.entries()) {
      console.log(`🔍 ${key}: ${value}`);
    }
    
    const walletIdsParam = searchParams.get('walletIds');
    
    if (!walletIdsParam) {
      return Response.json({
        success: false,
        error: 'walletIds parameter is required'
      }, { status: 400 });
    }

    // 解析钱包ID列表
    const walletIds = walletIdsParam.split(',').map(id => parseInt(id.trim())).filter(id => !isNaN(id));
    
    if (walletIds.length === 0) {
      return Response.json({
        success: false,
        error: 'No valid wallet IDs provided'
      }, { status: 400 });
    }

    console.log('🔍 处理的钱包ID:', walletIds);

    // 简化后的SQL：只查from_wallet_id在候选id中的交易，且from_balance不为空
    let query = `
      SELECT
        t.id as transaction_id,
        t.from_wallet_id,
        t.from_balance,
        t.timestamp
      FROM transactions t
      WHERE t.from_wallet_id = ANY($1)
        AND t.from_balance IS NOT NULL
        AND t.from_balance > 0
      ORDER BY t.timestamp ASC
    `;

    const client = await pool.connect();
    try {
      const result = await client.query(query, [walletIds]);
      const transactions = result.rows;

      console.log('🔍 查询到的from交易数据:', transactions.length, '条记录');

      // 构建原始图表数据（不聚合）
      const chartData = transactions
        .filter(tx => tx.from_balance !== null && tx.from_balance !== undefined)
        .filter(tx => parseFloat(tx.from_balance) > 0)
        .map(tx => ({
          time: tx.timestamp * 1000, // 转为毫秒
          value: parseFloat(tx.from_balance || 0),
          walletId: tx.from_wallet_id,
          transactionId: tx.transaction_id,
          fromBalance: parseFloat(tx.from_balance || 0)
        }));

      console.log('🔍 过滤后的有效余额数据:', chartData.length, '条记录');
      console.log('🔍 过滤掉的空余额记录:', transactions.length - chartData.length, '条');

      // 汇总统计
      const summary = {
        totalBalance: chartData.reduce((sum, d) => sum + d.value, 0),
        walletCount: walletIds.length,
        transactionCount: chartData.length // 使用过滤后的数据长度
      };

      return Response.json({
        success: true,
        data: chartData,
        summary: summary,
        total: chartData.length
      });
    } finally {
      client.release();
    }
  } catch (error) {
    console.error('❌ Error fetching wallet balances:', error);
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
} 