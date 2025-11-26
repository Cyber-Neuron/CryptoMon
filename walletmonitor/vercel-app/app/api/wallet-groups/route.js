import pkg from 'pg';
const { Pool } = pkg;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || process.env.POSTGRES_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    const grpType = searchParams.get('grpType') || 'Hot';
    const grpName = searchParams.get('grpName');
    const getAllGroups = searchParams.get('allGroups') === 'true';

    console.log('🔍 钱包组API - 参数:', { grpType, grpName, getAllGroups });

    let query, params;

    if (getAllGroups) {
      // 获取所有热钱包并按grp_name分组
      query = `
        SELECT 
          grp_name,
          array_agg(id ORDER BY id) as wallet_ids,
          count(*) as wallet_count
        FROM wallets 
        WHERE grp_type = $1
        GROUP BY grp_name
        ORDER BY grp_name ASC
      `;
      params = [grpType];
    } else if (grpName) {
      // 获取指定组名的钱包
      query = `
        SELECT id 
        FROM wallets 
        WHERE grp_type = $1 AND grp_name = $2
        ORDER BY id ASC
      `;
      params = [grpType, grpName];
    } else {
      // 默认获取binance组
      query = `
        SELECT id 
        FROM wallets 
        WHERE grp_type = $1 AND grp_name = $2
        ORDER BY id ASC
      `;
      params = [grpType, 'binance'];
    }

    const client = await pool.connect();
    try {
      const result = await client.query(query, params);

      if (getAllGroups) {
        // 返回分组数据
        const groups = result.rows.map(row => ({
          grpName: row.grp_name,
          walletIds: row.wallet_ids,
          walletCount: parseInt(row.wallet_count)
        }));

        console.log('🔍 查询到的钱包组:', groups.length, '个组');
        console.log('🔍 各组详情:', groups.map(g => `${g.grpName}: ${g.walletCount}个钱包`));

        return Response.json({
          success: true,
          data: groups,
          totalGroups: groups.length,
          totalWallets: groups.reduce((sum, group) => sum + group.walletCount, 0),
          filters: { grpType }
        });
      } else {
        // 返回单个组的数据
        const walletIds = result.rows.map(row => row.id);

        console.log('🔍 查询到的钱包ID:', walletIds.length, '个');

        return Response.json({
          success: true,
          data: walletIds,
          count: walletIds.length,
          filters: { grpType, grpName: grpName || 'binance' }
        });
      }
    } finally {
      client.release();
    }
  } catch (error) {
    console.error('❌ Error fetching wallet groups:', error);
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
} 