// 共享工具函数：获取最新数据并支持按分钟汇总
export async function getLatestData(direction, minutes = 360) { // 默认6小时 = 360分钟
  try {
    // 计算时间范围
    const now = Math.floor(Date.now() / 1000);
    const startTime = now - (minutes * 60); // 转换为秒
    
    // 构建URL参数
    const params = new URLSearchParams({
      limit: '1000000',
      offset: '0',
      startTime: startTime.toString(),
      endTime: now.toString()
    });
    
    // 根据方向设置参数
    const allGroups = [
      'aave', 'auros', 'kraken', 'base', 'bitfinex', 'bitget', 'bitkub', 
      'bitpanda', 'bybit', 'cex.io', 'coinbase', 'crypto.com', 'cumberland', 
      'dwf', 'gate.io', 'htx', 'jump', 'kucoin', 'mexc', 'okx', 'opensea', 
      'wintermute', 'other'
    ];
    
    if (direction === 'out') {
      // 从binance流出到所有交易所
      params.append('fromGroup', 'binance');
      allGroups.forEach(group => {
        params.append('toGroup', group);
      });
    } else if (direction === 'in') {
      // 从所有交易所流入到binance
      params.append('toGroup', 'binance');
      allGroups.forEach(group => {
        params.append('fromGroup', group);
      });
    }
    
    // 调用transactions API
    const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'}/api/transactions?${params}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    
    if (!result.success) {
      throw new Error(result.error || 'Failed to fetch data');
    }
    
    return {
      success: true,
      data: result.data || [],
      total: result.total || 0,
      query: {
        direction,
        startTime: new Date(startTime * 1000).toISOString(),
        endTime: new Date(now * 1000).toISOString(),
        minutes,
        limit: 1000000
      }
    };
    
  } catch (error) {
    console.error(`Error in getLatestData (${direction}):`, error);
    return {
      success: false,
      error: error.message,
      data: [],
      total: 0
    };
  }
}

// 按分钟汇总数据
export function aggregateByMinutes(data, minutes = 5) {
  if (!data || data.length === 0) {
    return [];
  }
  
  // 创建时间窗口映射
  const timeWindows = {};
  
  data.forEach(tx => {
    // 确保时间戳是数字格式
    let timestamp;
    if (typeof tx.timestamp === 'string') {
      timestamp = parseInt(tx.timestamp, 10);
    } else {
      timestamp = tx.timestamp;
    }
    
    if (isNaN(timestamp)) {
      console.warn('Invalid timestamp:', tx.timestamp);
      return; // 跳过无效的时间戳
    }
    
    // 按指定的分钟数创建时间窗口
    // 例如：minutes=5，则每5分钟为一个窗口
    const windowStart = Math.floor(timestamp / (minutes * 60)) * (minutes * 60);
    
    if (!timeWindows[windowStart]) {
      timeWindows[windowStart] = {
        timestamp: windowStart,
        count: 0,
        totalAmount: 0,
        totalUsdValue: 0,
        tokens: {},
        fromGroups: {},
        toGroups: {}
      };
    }
    
    const window = timeWindows[windowStart];
    window.count++;
    window.totalAmount += Math.abs(parseFloat(tx.amount) || 0);
    window.totalUsdValue += Math.abs(parseFloat(tx.usd_value) || 0);
    
    // 统计代币
    const token = tx.token_symbol || 'Unknown';
    window.tokens[token] = (window.tokens[token] || 0) + Math.abs(parseFloat(tx.amount) || 0);
    
    // 统计发送方组
    const fromGroup = tx.from_grp_name || 'Unknown';
    window.fromGroups[fromGroup] = (window.fromGroups[fromGroup] || 0) + Math.abs(parseFloat(tx.amount) || 0);
    
    // 统计接收方组
    const toGroup = tx.to_grp_name || 'Unknown';
    window.toGroups[toGroup] = (window.toGroups[toGroup] || 0) + Math.abs(parseFloat(tx.amount) || 0);
  });
  
  // 转换为数组并排序
  return Object.values(timeWindows)
    .sort((a, b) => a.timestamp - b.timestamp)
    .map(window => ({
      ...window,
      tokens: Object.entries(window.tokens).map(([token, amount]) => ({ token, amount })),
      fromGroups: Object.entries(window.fromGroups).map(([group, amount]) => ({ group, amount })),
      toGroups: Object.entries(window.toGroups).map(([group, amount]) => ({ group, amount }))
    }));
}

// 格式化函数
export function formatTime(timestamp) {
  if (!timestamp) return 'Unknown';
  
  let date;
  if (typeof timestamp === 'string') {
    // 如果是字符串格式的时间戳，先转换为数字
    const numTimestamp = parseInt(timestamp, 10);
    if (isNaN(numTimestamp)) {
      return 'Invalid Date';
    }
    // 如果是Unix时间戳（秒），转换为毫秒
    date = new Date(numTimestamp * 1000);
  } else if (typeof timestamp === 'number') {
    // 如果是Unix时间戳（秒），转换为毫秒
    date = new Date(timestamp * 1000);
  } else if (timestamp instanceof Date) {
    // 如果已经是Date对象
    date = timestamp;
  } else {
    // 其他情况，尝试直接转换
    date = new Date(timestamp);
  }
  
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  });
}

export function formatAmount(amount, token) {
  const safeAmount = Math.abs(parseFloat(amount || 0) || 0);
  const safeToken = token || 'Unknown';
  return safeAmount.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 6
  }) + ' ' + safeToken;
}

export function formatUSDValue(usdValue) {
  const safeValue = Math.abs(parseFloat(usdValue || 0) || 0);
  return safeValue.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}

// 格式化时间窗口（用于汇总数据）
export function formatTimeWindow(timestamp) {
  if (!timestamp) return 'Unknown';
  
  let date;
  if (typeof timestamp === 'string') {
    // 如果是字符串格式的时间戳，先转换为数字
    const numTimestamp = parseInt(timestamp, 10);
    if (isNaN(numTimestamp)) {
      return 'Invalid Date';
    }
    // 如果是Unix时间戳（秒），转换为毫秒
    date = new Date(numTimestamp * 1000);
  } else if (typeof timestamp === 'number') {
    // 如果是Unix时间戳（秒），转换为毫秒
    date = new Date(timestamp * 1000);
  } else if (timestamp instanceof Date) {
    // 如果已经是Date对象
    date = timestamp;
  } else {
    // 其他情况，尝试直接转换
    date = new Date(timestamp);
  }
  
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
}

// 生成汇总统计
export function generateSummary(data) {
  if (!data || data.length === 0) {
    return {
      ethAmount: 0,
      ethUsdValue: 0,
      usdcAmount: 0,
      usdtAmount: 0,
      totalUsdAmount: 0
    };
  }
  
  let ethAmount = 0;
  let ethUsdValue = 0;
  let usdcAmount = 0;
  let usdtAmount = 0;
  let totalUsdAmount = 0;
  
  data.forEach(tx => {
    const amount = Math.abs(parseFloat(tx.amount) || 0);
    const usdValue = Math.abs(parseFloat(tx.usd_value) || 0);
    const token = (tx.token_symbol || '').toUpperCase();
    
    totalUsdAmount += usdValue;
    
    if (token === 'ETH') {
      ethAmount += amount;
      ethUsdValue += usdValue;
    } else if (token === 'USDC') {
      usdcAmount += usdValue; // USDC的USD价值
    } else if (token === 'USDT') {
      usdtAmount += usdValue; // USDT的USD价值
    }
  });
  
  return {
    ethAmount,
    ethUsdValue,
    usdcAmount,
    usdtAmount,
    totalUsdAmount
  };
}

// 格式化汇总数据
export function formatSummary(summary) {
  return {
    ethAmount: summary.ethAmount.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 6
    }),
    ethUsdValue: '$' + summary.ethUsdValue.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }),
    usdcAmount: '$' + summary.usdcAmount.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }),
    usdtAmount: '$' + summary.usdtAmount.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }),
    totalUsdAmount: '$' + summary.totalUsdAmount.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    })
  };
}

// 生成CSV内容
export function generateCSV(data, aggregated = false) {
  if (aggregated) {
    // 汇总数据的CSV格式
    const headers = ['时间窗口', '交易数量', '总数量', '总USD价值', '主要代币', '主要发送方组', '主要接收方组'];
    
    const csvContent = [
      headers.join(','),
      ...data.map(window => {
        const mainToken = window.tokens.length > 0 ? window.tokens[0].token : 'Unknown';
        const mainFromGroup = window.fromGroups.length > 0 ? window.fromGroups[0].group : 'Unknown';
        const mainToGroup = window.toGroups.length > 0 ? window.toGroups[0].group : 'Unknown';
        
        const row = [
          `"${formatTimeWindow(window.timestamp)}"`,
          `"${window.count}"`,
          `"${formatAmount(window.totalAmount, 'ETH')}"`,
          `"${formatUSDValue(window.totalUsdValue)}"`,
          `"${mainToken}"`,
          `"${mainFromGroup}"`,
          `"${mainToGroup}"`
        ];
        return row.join(',');
      })
    ].join('\n');
    
    return csvContent;
  } else {
    // 原始交易数据的CSV格式
    const headers = ['时间', '发送方', '发送方组', '接收方', '接收方组', '数量', '金额'];
    
    const csvContent = [
      headers.join(','),
      ...data.map(tx => {
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
    
    // 添加汇总信息
    const summary = generateSummary(data);
    const formattedSummary = formatSummary(summary);
    
    const summarySection = [
      '',
      '汇总统计',
      `"ETH amount","${formattedSummary.ethAmount}"`,
      `"ETH amount in USD","${formattedSummary.ethUsdValue}"`,
      `"USDC amount","${formattedSummary.usdcAmount}"`,
      `"USDT amount","${formattedSummary.usdtAmount}"`,
      `"Total USD amount","${formattedSummary.totalUsdAmount}"`
    ].join('\n');
    
    return csvContent + summarySection;
  }
}

// 格式化数据用于JSON响应（将时间戳转换为可读格式）
export function formatDataForJSON(data, aggregated = false) {
  const formattedData = aggregated ? 
    data.map(window => ({
      ...window,
      formattedTime: formatTimeWindow(window.timestamp),
      tokens: window.tokens.map(t => ({
        ...t,
        formattedAmount: formatAmount(t.amount, t.token)
      })),
      fromGroups: window.fromGroups.map(g => ({
        ...g,
        formattedAmount: formatAmount(g.amount, 'ETH')
      })),
      toGroups: window.toGroups.map(g => ({
        ...g,
        formattedAmount: formatAmount(g.amount, 'ETH')
      })),
      formattedTotalAmount: formatAmount(window.totalAmount, 'ETH'),
      formattedTotalUsdValue: formatUSDValue(window.totalUsdValue)
    })) :
    data.map(tx => ({
      ...tx,
      formattedTime: formatTime(tx.timestamp),
      formattedAmount: formatAmount(tx.amount, tx.token_symbol),
      formattedUsdValue: formatUSDValue(tx.usd_value)
    }));
  
  // 添加汇总信息
  const summary = generateSummary(data);
  const formattedSummary = formatSummary(summary);
  
  return {
    data: formattedData,
    summary: {
      raw: summary,
      formatted: formattedSummary
    }
  };
} 