import pkg from 'pg';
const { Pool } = pkg;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || process.env.POSTGRES_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    
    //console.log('🔍 所有接收到的参数:');
    for (const [key, value] of searchParams.entries()) {
      //console.log(`🔍 ${key}: ${value}`);
    }
    
    const fromWalletId = searchParams.get('fromWalletId');
    const toWalletId = searchParams.get('toWalletId');
    const startTime = searchParams.get('startTime');
    const endTime = searchParams.get('endTime');
    const limit = parseInt(searchParams.get('limit')) || 100;
    const offset = parseInt(searchParams.get('offset')) || 0;
    const tokenParam = searchParams.get('token');
    const tokens = tokenParam ? decodeURIComponent(tokenParam).split(',').map(t => t.trim()).filter(t => t) : [];
    const fromGroupParams = searchParams.getAll('fromGroup');
    const fromGroups = fromGroupParams.length > 0 ? fromGroupParams.map(g => decodeURIComponent(g).trim()).filter(g => g) : [];
    const toGroupParams = searchParams.getAll('toGroup');
    const toGroups = toGroupParams.length > 0 ? toGroupParams.map(g => decodeURIComponent(g).trim()).filter(g => g) : [];
    const deselectedFromGroupParam = searchParams.get('deselectedFromGroup');
    const deselectedFromGroups = deselectedFromGroupParam ? decodeURIComponent(deselectedFromGroupParam).split(',').map(g => g.trim()).filter(g => g) : [];
    const deselectedToGroupParam = searchParams.get('deselectedToGroup');
    const deselectedToGroups = deselectedToGroupParam ? decodeURIComponent(deselectedToGroupParam).split(',').map(g => g.trim()).filter(g => g) : [];
    const format = searchParams.get('format');

    //console.log('🔍 原始参数值:');
    //console.log('🔍 deselectedFromGroupParam:', deselectedFromGroupParam);
    //console.log('🔍 deselectedToGroupParam:', deselectedToGroupParam);
    //console.log('🔍 解析后的deselectedFromGroups:', deselectedFromGroups);
    //console.log('🔍 解析后的deselectedToGroups:', deselectedToGroups);

    let query = `
      SELECT 
        t.id,
        t.hash,
        t.block_number,
        t.amount,
        t.timestamp,
        t.usd_value,
        t.created_at,
        fw.address as from_address,
        fw.friendly_name as from_friendly_name,
        fw.grp_name as from_grp_name,
        tw.address as to_address,
        tw.friendly_name as to_friendly_name,
        tw.grp_name as to_grp_name,
        tok.symbol as token_symbol,
        c.name as chain_name,
        c.native_sym as chain_native_sym
      FROM transactions t
      LEFT JOIN wallets fw ON t.from_wallet_id = fw.id
      LEFT JOIN wallets tw ON t.to_wallet_id = tw.id
      LEFT JOIN tokens tok ON t.token_id = tok.id
      LEFT JOIN chains c ON t.chain_id = c.id
      WHERE 1=1
      -- 排除交易所内部转账：发送方和接收方属于同一个grp_name且wallet_type_id都是2
      AND NOT (
        fw.grp_name = tw.grp_name 
        AND fw.grp_name IS NOT NULL 
        AND tw.grp_name IS NOT NULL
        AND fw.wallet_type_id = 2 
        AND tw.wallet_type_id = 2
      )
    `;

    const params = [];
    let paramIndex = 1;

    if (fromWalletId) {
      query += ` AND t.from_wallet_id = $${paramIndex}`;
      params.push(fromWalletId);
      paramIndex++;
    }

    if (toWalletId) {
      query += ` AND t.to_wallet_id = $${paramIndex}`;
      params.push(toWalletId);
      paramIndex++;
    }

    if (startTime) {
      query += ` AND t.timestamp >= $${paramIndex}`;
      params.push(parseInt(startTime));
      paramIndex++;
    }

    if (endTime) {
      query += ` AND t.timestamp <= $${paramIndex}`;
      params.push(parseInt(endTime));
      paramIndex++;
    }

    if (tokens.length > 0) {
      const placeholders = tokens.map((_, i) => `$${paramIndex + i}`).join(',');
      query += ` AND tok.symbol IN (${placeholders})`;
      params.push(...tokens);
      paramIndex += tokens.length;
    }

    if (fromGroups.length > 0) {
      const hasOthers = fromGroups.includes('other');
      if (hasOthers) {
        // 如果包含"other"，则显示选中的组 + 所有不在下拉菜单中的组
        const selectedGroups = fromGroups.filter(g => g !== 'other');
        if (selectedGroups.length > 0) {
          const placeholders = selectedGroups.map((_, i) => `$${paramIndex + i}`).join(',');
          query += ` AND (fw.grp_name IN (${placeholders}) OR (fw.grp_name NOT IN (${placeholders}) AND fw.grp_name IS NOT NULL))`;
          params.push(...selectedGroups);
          paramIndex += selectedGroups.length;
        }
      } else {
        // 正常过滤
        const placeholders = fromGroups.map((_, i) => `$${paramIndex + i}`).join(',');
        query += ` AND fw.grp_name IN (${placeholders})`;
        params.push(...fromGroups);
        paramIndex += fromGroups.length;
      }
    }

    if (toGroups.length > 0) {
      const hasOthers = toGroups.includes('other');
      if (hasOthers) {
        // 如果包含"other"，则显示选中的组 + 所有不在下拉菜单中的组
        const selectedGroups = toGroups.filter(g => g !== 'other');
        if (selectedGroups.length > 0) {
          const placeholders = selectedGroups.map((_, i) => `$${paramIndex + i}`).join(',');
          query += ` AND (tw.grp_name IN (${placeholders}) OR (tw.grp_name NOT IN (${placeholders}) AND tw.grp_name IS NOT NULL))`;
          params.push(...selectedGroups);
          paramIndex += selectedGroups.length;
        }
      } else {
        // 正常过滤
        const placeholders = toGroups.map((_, i) => `$${paramIndex + i}`).join(',');
        query += ` AND tw.grp_name IN (${placeholders})`;
        params.push(...toGroups);
        paramIndex += toGroups.length;
      }
    }

    query += ` ORDER BY t.timestamp DESC LIMIT $${paramIndex} OFFSET $${paramIndex + 1}`;
    params.push(limit, offset);

    const client = await pool.connect();
    try {
      const result = await client.query(query, params);
      let filteredData = result.rows;

      //console.log('🔍 原始查询结果数量:', filteredData.length);
      //console.log('🔍 fromGroups:', fromGroups);
      //console.log('🔍 toGroups:', toGroups);
      //console.log('🔍 deselectedFromGroups:', deselectedFromGroups);
      //console.log('🔍 deselectedToGroups:', deselectedToGroups);

      // 后端过滤：处理"other"分组的deselected逻辑
      if (fromGroups.includes('other') && deselectedFromGroups.length > 0) {
        //console.log('🔍 开始过滤发送方deselected组:', deselectedFromGroups);
        const beforeFilterCount = filteredData.length;
        filteredData = filteredData.filter(tx => {
          const fromGroup = tx.from_grp_name;
          const shouldKeep = !deselectedFromGroups.includes(fromGroup);
          if (!shouldKeep) {
            //console.log('🔍 过滤掉发送方组:', fromGroup);
          }
          return shouldKeep;
        });
        //console.log('🔍 发送方过滤后数量:', filteredData.length, '过滤掉:', beforeFilterCount - filteredData.length);
      }

      if (toGroups.includes('other') && deselectedToGroups.length > 0) {
        //console.log('🔍 开始过滤接收方deselected组:', deselectedToGroups);
        const beforeFilterCount = filteredData.length;
        filteredData = filteredData.filter(tx => {
          const toGroup = tx.to_grp_name;
          const shouldKeep = !deselectedToGroups.includes(toGroup);
          if (!shouldKeep) {
            //console.log('🔍 过滤掉接收方组:', toGroup);
          }
          return shouldKeep;
        });
        //console.log('🔍 接收方过滤后数量:', filteredData.length, '过滤掉:', beforeFilterCount - filteredData.length);
      }

      // 格式化函数
      const formatTime = (timestamp) => {
        if (!timestamp) return 'Unknown';
        const date = new Date(timestamp * 1000);
        return date.toLocaleString('en-US', {
          timeZone: 'America/New_York',
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: false
        });
      };

      const formatAmount = (amount, token) => {
        const safeAmount = Math.abs(parseFloat(amount || 0) || 0);
        const safeToken = token || 'Unknown';
        return safeAmount.toLocaleString('en-US', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 6
        }) + ' ' + safeToken;
      };

      const formatUSDValue = (usdValue) => {
        const safeValue = Math.abs(parseFloat(usdValue || 0) || 0);
        return safeValue.toLocaleString('en-US', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        });
      };

      // 如果请求CSV格式
      if (format === 'csv') {
        const headers = ['时间', '发送方', '发送方组', '接收方', '接收方组', '数量', '金额'];
        
        const csvContent = [
          headers.join(','),
          ...filteredData.map(tx => {
            const row = [
              `"${formatTime(tx.timestamp)}"`,
              `"${tx.from_friendly_name || 'Unknown'}"`,
              `"${tx.from_grp_name || 'Unknown Group'}"`,
              `"${tx.to_friendly_name || 'Unknown'}"`,
              `"${tx.to_grp_name || 'Unknown Group'}"`,
              `"${formatAmount(tx.amount, tx.token_symbol)}"`,
              `"${formatUSDValue(tx.usd_value)}"`
            ];
            return row.join(',');
          })
        ].join('\n');

        return new Response(csvContent, {
          headers: {
            'Content-Type': 'text/csv; charset=utf-8',
            'Content-Disposition': `attachment; filename="transactions_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.csv"`
          }
        });
      }

      // 默认返回JSON格式
      return Response.json({
        success: true,
        data: filteredData,
        total: filteredData.length
      });
    } finally {
      client.release();
    }
  } catch (error) {
    console.error('Error fetching transactions:', error);
    return Response.json({
      success: false,
      error: error.message
    }, { status: 500 });
  }
} 