import pkg from 'pg';
const { Pool } = pkg;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

export async function getFlowData(startTime, endTime, tokens, groups, fromGroups = [], toGroups = []) {
  const client = await pool.connect();
  
  try {
    let query = `
      SELECT 
        t.timestamp,
        LOWER(fwt.name) as from_grp_name,
        LOWER(twt.name) as to_grp_name,
        fw.friendly_name as from_friendly_name,
        tw.friendly_name as to_friendly_name,
        fw.grp_name as from_grp_name_detail,
        tw.grp_name as to_grp_name_detail,
        tk.symbol as token,
        t.amount,
        t.usd_value
      FROM transactions t
      LEFT JOIN wallets fw ON t.from_wallet_id = fw.id
      LEFT JOIN wallets tw ON t.to_wallet_id = tw.id
      LEFT JOIN wallet_types fwt ON fw.wallet_type_id = fwt.id
      LEFT JOIN wallet_types twt ON tw.wallet_type_id = twt.id
      LEFT JOIN tokens tk ON t.token_id = tk.id
      WHERE 1=1
    `;
    
    const params = [];
    let paramIndex = 1;
    
    if (startTime) {
      query += ` AND t.timestamp >= $${paramIndex}`;
      params.push(startTime);
      paramIndex++;
    }
    
    if (endTime) {
      query += ` AND t.timestamp <= $${paramIndex}`;
      params.push(endTime);
      paramIndex++;
    }
    
    if (tokens && tokens.length > 0) {
      query += ` AND tk.symbol = ANY($${paramIndex})`;
      params.push(tokens);
      paramIndex++;
    }
    
    // 处理 fromGroups 和 toGroups 的精确过滤
    if (fromGroups && fromGroups.length > 0 && toGroups && toGroups.length > 0) {
      // 如果同时指定了 from 和 to 组别，则精确匹配流向
      const lowerFromGroups = fromGroups.map(g => g.toLowerCase());
      const lowerToGroups = toGroups.map(g => g.toLowerCase());
      query += ` AND LOWER(fwt.name) = ANY($${paramIndex}) AND LOWER(twt.name) = ANY($${paramIndex + 1})`;
      params.push(lowerFromGroups);
      params.push(lowerToGroups);
      paramIndex += 2;
    } else if (fromGroups && fromGroups.length > 0) {
      // 只指定了 from 组别
      const lowerFromGroups = fromGroups.map(g => g.toLowerCase());
      query += ` AND LOWER(fwt.name) = ANY($${paramIndex})`;
      params.push(lowerFromGroups);
      paramIndex++;
    } else if (toGroups && toGroups.length > 0) {
      // 只指定了 to 组别
      const lowerToGroups = toGroups.map(g => g.toLowerCase());
      query += ` AND LOWER(twt.name) = ANY($${paramIndex})`;
      params.push(lowerToGroups);
      paramIndex++;
    } else if (groups && groups.length > 0) {
      // 兼容原有的 groups 参数（模糊匹配）
      const lowerGroups = groups.map(g => g.toLowerCase());
      query += ` AND (LOWER(fwt.name) = ANY($${paramIndex}) OR LOWER(twt.name) = ANY($${paramIndex}))`;
      params.push(lowerGroups);
      paramIndex++;
    }
    
    query += ` ORDER BY t.timestamp ASC`;
    
    const result = await client.query(query, params);
    return result.rows;
  } finally {
    client.release();
  }
}

export async function getAvailableTokens() {
  const client = await pool.connect();
  
  try {
    const result = await client.query(`
      SELECT DISTINCT tk.symbol as token 
      FROM transactions t
      LEFT JOIN tokens tk ON t.token_id = tk.id
      WHERE tk.symbol IS NOT NULL 
      ORDER BY tk.symbol
    `);
    return result.rows.map(row => row.token);
  } finally {
    client.release();
  }
}

export async function getAvailableGroups() {
  const client = await pool.connect();
  
  try {
    const result = await client.query(`
      SELECT DISTINCT LOWER(wt.name) as grp_name 
      FROM (
        SELECT DISTINCT fw.wallet_type_id
        FROM transactions t
        LEFT JOIN wallets fw ON t.from_wallet_id = fw.id
        WHERE fw.wallet_type_id IS NOT NULL
        UNION
        SELECT DISTINCT tw.wallet_type_id
        FROM transactions t
        LEFT JOIN wallets tw ON t.to_wallet_id = tw.id
        WHERE tw.wallet_type_id IS NOT NULL
      ) wallet_types
      LEFT JOIN wallet_types wt ON wallet_types.wallet_type_id = wt.id
      WHERE wt.name IS NOT NULL
      ORDER BY wt.name
    `);
    return result.rows.map(row => row.grp_name);
  } finally {
    client.release();
  }
}

export function processFlowDataForChart(flowData, selectedGroups = [], fromGroups = [], toGroups = []) {
  const timeMap = new Map(); // 用 Map 来合并相同时间戳的数据
  
  // 调试：输出原始数据库记录
  //console.log('🔍 原始数据库记录:');
  // flowData.slice(0, 5).forEach((flow, index) => {
    // console.log(`记录 ${index + 1}:`, {
    //   timestamp: flow.timestamp,
    //   from_grp_name: flow.from_grp_name,
    //   to_grp_name: flow.to_grp_name,
    //   from_friendly_name: flow.from_friendly_name,
    //   to_friendly_name: flow.to_friendly_name,
    //   from_grp_name_detail: flow.from_grp_name_detail,
    //   to_grp_name_detail: flow.to_grp_name_detail,
    //   token: flow.token,
    //   amount: flow.amount,
    //   usd_value: flow.usd_value,
    //   usd_value_type: typeof flow.usd_value
    // });
  // });
  
  // 检查是否指定了精确的流向过滤
  const hasExactFlowFilter = (fromGroups && fromGroups.length > 0) || (toGroups && toGroups.length > 0);
  
  for (const flow of flowData) {
    const time = flow.timestamp;
    const usdValue = parseFloat(flow.usd_value) || 0;
    const amount = parseFloat(flow.amount) || 0;
    
    // 如果流入和流出是同一组，跳过这条记录
    if (flow.from_grp_name === flow.to_grp_name && flow.from_grp_name !== 'unk') {
      //console.log(`跳过内部转账: ${flow.from_grp_name} -> ${flow.to_grp_name}`);
      continue;
    }
    
    // 计算选中组的净流入/流出
    let netFlowUSD = 0;
    let netFlowAmount = 0;
    
    if (hasExactFlowFilter) {
      // 当指定了精确流向过滤时，所有匹配的记录都视为流入（从from到to）
      if (flow.from_grp_name && flow.from_grp_name !== 'unk' && 
          flow.to_grp_name && flow.to_grp_name !== 'unk') {
        // 检查是否匹配指定的流向
        const fromMatch = fromGroups.length === 0 || fromGroups.includes(flow.from_grp_name);
        const toMatch = toGroups.length === 0 || toGroups.includes(flow.to_grp_name);
        
        if (fromMatch && toMatch) {
          netFlowUSD = usdValue; // 全部视为正值（流入）
          netFlowAmount = amount; // 全部视为正值（流入）
          //console.log(`精确流向匹配: ${flow.from_grp_name} -> ${flow.to_grp_name} -> +${usdValue} USD, +${amount} ${flow.token}`);
        }
      }
    } else {
      // 原有的逻辑：如果from_grp_name在选中组中，说明有流出
      if (flow.from_grp_name && flow.from_grp_name !== 'unk' && 
          (selectedGroups.length === 0 || selectedGroups.includes(flow.from_grp_name))) {
        netFlowUSD -= usdValue; // 流出为负值
        netFlowAmount -= amount; // 流出为负值
        //console.log(`流出: ${flow.from_grp_name} -> -${usdValue} USD, -${amount} ${flow.token}`);
      }
      
      // 如果to_grp_name在选中组中，说明有流入
      if (flow.to_grp_name && flow.to_grp_name !== 'unk' && 
          (selectedGroups.length === 0 || selectedGroups.includes(flow.to_grp_name))) {
        netFlowUSD += usdValue; // 流入为正值
        netFlowAmount += amount; // 流入为正值
        //console.log(`流入: ${flow.to_grp_name} -> +${usdValue} USD, +${amount} ${flow.token}`);
      }
    }
    
    // 累加到时间戳
    if (timeMap.has(time)) {
      const existing = timeMap.get(time);
      existing.usd_value += netFlowUSD;
      existing.amount += netFlowAmount;
      // 保留流向信息用于显示
      if (!existing.flows) existing.flows = [];
      existing.flows.push({
        from_grp_name: flow.from_grp_name,
        to_grp_name: flow.to_grp_name,
        from_friendly_name: flow.from_friendly_name,
        to_friendly_name: flow.to_friendly_name,
        from_grp_name_detail: flow.from_grp_name_detail,
        to_grp_name_detail: flow.to_grp_name_detail,
        amount: amount,
        usd_value: usdValue,
        token: flow.token
      });
    } else {
      timeMap.set(time, {
        usd_value: netFlowUSD,
        amount: netFlowAmount,
        token: flow.token,
        flows: [{
          from_grp_name: flow.from_grp_name,
          to_grp_name: flow.to_grp_name,
          from_friendly_name: flow.from_friendly_name,
          to_friendly_name: flow.to_friendly_name,
          from_grp_name_detail: flow.from_grp_name_detail,
          to_grp_name_detail: flow.to_grp_name_detail,
          amount: amount,
          usd_value: usdValue,
          token: flow.token
        }]
      });
    }
    
    //console.log(`时间 ${time} 净流量: ${netFlowUSD} USD, ${netFlowAmount} ${flow.token}`);
  }
  
  // 转换为数组并按时间排序
  const chartData = Array.from(timeMap.entries()).map(([time, data]) => ({
    time: Number(time),
    value: data.usd_value, // 保持向后兼容，value 字段仍然使用 USD 值
    amount: data.amount,   // 新增 amount 字段
    usd_value: data.usd_value, // 新增 usd_value 字段
    group: 'combined',
    token: data.token,
    // 保留流向信息
    from_grp_name: data.flows?.[0]?.from_grp_name,
    to_grp_name: data.flows?.[0]?.to_grp_name,
    from_friendly_name: data.flows?.[0]?.from_friendly_name,
    to_friendly_name: data.flows?.[0]?.to_friendly_name,
    from_grp_name_detail: data.flows?.[0]?.from_grp_name_detail,
    to_grp_name_detail: data.flows?.[0]?.to_grp_name_detail,
    flows: data.flows || []
  }));
  
  //console.log('🔍 最终图表数据:', chartData);
  
  return chartData.sort((a, b) => a.time - b.time);
} 