'use client';

import { useState, useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';

// 获取ETH价格的函数，获取全局价格数据
const getEthUsdtPrices = async (startTime, endTime, interval = '1h') => {
  const url = "https://api.binance.com/api/v3/klines";
  const params = new URLSearchParams({
    symbol: "ETHUSDT",
    interval: interval,
    startTime: (startTime * 1000).toString(), // 转换为毫秒
    endTime: (endTime * 1000).toString(), // 转换为毫秒
  });

  try {
    //console.log(`🔍 请求ETH价格数据: ${url}?${params}`);
    const resp = await fetch(`${url}?${params}`, { 
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (!resp.ok) {
      console.error(`❌ ETH价格请求失败: ${resp.status} ${resp.statusText}`);
      return [];
    }
    
    const data = await resp.json();
    //console.log(`🔍 ETH价格响应数据条数:`, data.length);

    if (Array.isArray(data) && data.length > 0) {
      const priceData = data.map(item => ({
        time: Number(item[0]), // 时间戳（毫秒）
        value: parseFloat(item[4]) // 收盘价
      }));
      //console.log(`✅ 解析到ETH价格数据:`, priceData.length, '条');
      return priceData;
    } else {
      //console.log("❌ No ETH price data returned.");
      return [];
    }
  } catch (error) {
    console.error("❌ Error fetching ETH prices:", error);
    return [];
  }
};

// 交易详情表格组件
const TransactionDetailsTable = ({ transactions, onClose }) => {
  const [selectedRows, setSelectedRows] = useState(new Set());
  const [selectAll, setSelectAll] = useState(false);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: null }); // 排序状态

  if (!transactions || transactions.length === 0) {
    return null;
  }

  // 排序函数
  const getSortedTransactions = () => {
    if (!sortConfig.key || !sortConfig.direction) return transactions;
    const sorted = [...transactions];
    sorted.sort((a, b) => {
      let aValue, bValue;
      switch (sortConfig.key) {
        case 'timestamp':
          aValue = a.timestamp || 0;
          bValue = b.timestamp || 0;
          break;
        case 'from':
          aValue = a.from_friendly_name || '';
          bValue = b.from_friendly_name || '';
          break;
        case 'to':
          aValue = a.to_friendly_name || '';
          bValue = b.to_friendly_name || '';
          break;
        case 'amount':
          aValue = parseFloat(a.amount || 0);
          bValue = parseFloat(b.amount || 0);
          break;
        case 'usd_value':
          aValue = parseFloat(a.usd_value || 0);
          bValue = parseFloat(b.usd_value || 0);
          break;
        case 'hash':
          aValue = a.hash || '';
          bValue = b.hash || '';
          break;
        default:
          aValue = '';
          bValue = '';
      }
      if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
      return 0;
    });
    return sorted;
  };

  // 切换排序状态
  const handleSort = (key) => {
    setSortConfig(prev => {
      if (prev.key !== key) {
        return { key, direction: 'asc' };
      } else if (prev.direction === 'asc') {
        return { key, direction: 'desc' };
      } else if (prev.direction === 'desc') {
        return { key: null, direction: null };
      } else {
        return { key, direction: 'asc' };
      }
    });
  };

  const sortedTransactions = getSortedTransactions();

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
    return '$' + safeValue.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  };

  // 复制到剪贴板的函数
  const copyToClipboard = async (text, type) => {
    try {
      await navigator.clipboard.writeText(text);
      // 可以添加一个简单的提示，比如改变按钮颜色或显示临时文本
      //console.log(`✅ 已复制${type}: ${text}`);
    } catch (err) {
      console.error('❌ 复制失败:', err);
      // 降级方案：使用传统的复制方法
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand('copy');
        //console.log(`✅ 已复制${type}: ${text}`);
      } catch (fallbackErr) {
        console.error('❌ 降级复制也失败:', fallbackErr);
      }
      document.body.removeChild(textArea);
    }
  };

  // 处理单个checkbox选择
  const handleTransactionSelect = (index) => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(index)) {
      newSelected.delete(index);
    } else {
      newSelected.add(index);
    }
    setSelectedRows(newSelected);
    setSelectAll(newSelected.size === transactions.length);
  };

  // 处理全选/取消全选
  const handleSelectAll = () => {
    if (selectAll) {
      setSelectedRows(new Set());
      setSelectAll(false);
    } else {
      const allIndices = new Set(transactions.map((_, index) => index));
      setSelectedRows(allIndices);
      setSelectAll(true);
    }
  };

  // 下载CSV文件
  const downloadCSV = () => {
    if (selectedRows.size === 0) {
      alert('请先选择要下载的交易');
      return;
    }

    // CSV头部
    const headers = ['时间', '发送方', '发送方组', '接收方', '接收方组', '数量', 'USD价值', 'ETH价格', '交易哈希'];
    
    // 构建CSV内容
    const csvContent = [
      headers.join(','),
      ...Array.from(selectedRows).map(index => {
        const tx = transactions[index];
        
        // 安全检查：确保tx存在且包含必要属性
        if (!tx) {
          console.warn('⚠️ 发现空的交易数据，跳过:', index);
          return '';
        }
        
        // 计算ETH价格：USD价值 / 数量
        const amount = Math.abs(parseFloat(tx.amount || 0) || 0);
        const usdValue = Math.abs(parseFloat(tx.usd_value || 0) || 0);
        const ethPrice = amount > 0 ? (usdValue / amount).toFixed(2) : '0.00';
        
        const row = [
          `"${formatTime(tx.timestamp || 0)}"`,
          `"${tx.from_friendly_name || 'Unknown'}"`,
          `"${tx.from_grp_name || 'Unknown Group'}"`,
          `"${tx.to_friendly_name || 'Unknown'}"`,
          `"${tx.to_grp_name || 'Unknown Group'}"`,
          `"${formatAmount(tx.amount || 0, tx.token_symbol || 'Unknown')}"`,
          `"${formatUSDValue(tx.usd_value || 0)}"`,
          `"$${ethPrice}"`,
          `"${tx.hash || 'Unknown'}"`
        ];
        return row.join(',');
      }).filter(row => row !== '') // 过滤掉空行
    ].join('\n');

    // 创建并下载文件
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `transactions_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // 复制CSV到剪贴板
  const copyCSV = async () => {
    if (selectedRows.size === 0) {
      alert('请先选择要复制的交易');
      return;
    }
    const headers = ['时间', '发送方', '发送方组', '接收方', '接收方组', '数量'];
    const csvContent = [
      headers.join(','),
      ...Array.from(selectedRows).map(index => {
        const tx = transactions[index];
        if (!tx) return '';
        const row = [
          `"${formatTime(tx.timestamp || 0)}"`,
          `"${tx.from_friendly_name || 'Unknown'}"`,
          `"${tx.from_grp_name || 'Unknown Group'}"`,
          `"${tx.to_friendly_name || 'Unknown'}"`,
          `"${tx.to_grp_name || 'Unknown Group'}"`,
          `"${formatAmount(tx.amount || 0, tx.token_symbol || 'Unknown')}"`
        ];
        return row.join(',');
      }).filter(row => row !== '')
    ].join('\n');
    try {
      await navigator.clipboard.writeText(csvContent);
      alert('已复制到剪贴板！');
    } catch (err) {
      // 降级方案
      const textArea = document.createElement('textarea');
      textArea.value = csvContent;
      document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand('copy');
        alert('已复制到剪贴板！');
      } catch (fallbackErr) {
        alert('复制失败，请手动复制');
      }
      document.body.removeChild(textArea);
    }
  };

  // 汇总层计算
  const summary = sortedTransactions.reduce(
    (acc, tx) => {
      const symbol = (tx.token_symbol || '').toUpperCase();
      const amount = parseFloat(tx.amount || 0) || 0;
      const usdValue = parseFloat(tx.usd_value || 0) || 0;
      if (symbol === 'ETH') {
        acc.ethAmount += amount;
        acc.ethUsd += usdValue;
      } else if (symbol === 'USDC') {
        acc.usdcAmount += amount;
      } else if (symbol === 'USDT') {
        acc.usdtAmount += amount;
      }
      acc.totalUsd += usdValue;
      return acc;
    },
    { ethAmount: 0, ethUsd: 0, usdcAmount: 0, usdtAmount: 0, totalUsd: 0 }
  );

  // 格式化简写
  const formatAbbreviated = (value) => {
    if (value >= 1000000) {
      return `${(value / 1000000).toFixed(1)}M`;
    } else if (value >= 1000) {
      return `${(value / 1000).toFixed(1)}K`;
    }
    return value.toFixed(0);
  };

  return (
    <div style={{
      marginTop: '20px',
      border: '1px solid #e0e0e0',
      borderRadius: '8px',
      backgroundColor: '#fafafa',
      maxHeight: '400px',
      overflow: 'auto'
    }}>
      <div style={{
        padding: '12px 16px',
        borderBottom: '1px solid #e0e0e0',
        backgroundColor: '#f5f5f5',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div style={{ fontWeight: 'bold', fontSize: '14px' }}>
          交易详情 ({transactions.length} 笔交易)
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button
            onClick={downloadCSV}
            disabled={selectedRows.size === 0}
            style={{
              background: selectedRows.size === 0 ? '#ccc' : '#1976d2',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              padding: '6px 12px',
              fontSize: '12px',
              cursor: selectedRows.size === 0 ? 'not-allowed' : 'pointer',
              fontFamily: 'Arial, sans-serif'
            }}
            title={selectedRows.size === 0 ? '请先选择交易' : '下载选中交易为CSV'}
          >
            下载CSV ({selectedRows.size})
          </button>
          <button
            onClick={copyCSV}
            disabled={selectedRows.size === 0}
            style={{
              background: selectedRows.size === 0 ? '#ccc' : '#10B981',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              padding: '6px 12px',
              fontSize: '12px',
              cursor: selectedRows.size === 0 ? 'not-allowed' : 'pointer',
              fontFamily: 'Arial, sans-serif'
            }}
            title={selectedRows.size === 0 ? '请先选择交易' : '复制选中交易为CSV'}
          >
            复制CSV
          </button>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '18px',
              cursor: 'pointer',
              color: '#666',
              padding: '0',
              width: '24px',
              height: '24px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            ×
          </button>
        </div>
      </div>
      
      <div style={{ overflow: 'auto' }}>
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          fontSize: '12px'
        }}>
          <thead>
            <tr style={{
              backgroundColor: '#f8f9fa',
              borderBottom: '1px solid #e0e0e0'
            }}>
              <th style={{ padding: '8px 12px', textAlign: 'center', borderRight: '1px solid #e0e0e0', width: '40px' }}>
                <input
                  type="checkbox"
                  checked={selectAll}
                  onChange={handleSelectAll}
                  style={{ cursor: 'pointer' }}
                />
              </th>
              <th style={{ padding: '8px 12px', textAlign: 'left', borderRight: '1px solid #e0e0e0', whiteSpace: 'nowrap' }}>
                时间
                <SortButton active={sortConfig.key === 'timestamp'} direction={sortConfig.direction} onClick={() => handleSort('timestamp')} />
              </th>
              <th style={{ padding: '8px 12px', textAlign: 'left', borderRight: '1px solid #e0e0e0', whiteSpace: 'nowrap' }}>
                发送方
                <SortButton active={sortConfig.key === 'from'} direction={sortConfig.direction} onClick={() => handleSort('from')} />
              </th>
              <th style={{ padding: '8px 12px', textAlign: 'left', borderRight: '1px solid #e0e0e0', whiteSpace: 'nowrap' }}>
                接收方
                <SortButton active={sortConfig.key === 'to'} direction={sortConfig.direction} onClick={() => handleSort('to')} />
              </th>
              <th style={{ padding: '8px 12px', textAlign: 'right', borderRight: '1px solid #e0e0e0', whiteSpace: 'nowrap' }}>
                数量
                <SortButton active={sortConfig.key === 'amount'} direction={sortConfig.direction} onClick={() => handleSort('amount')} />
              </th>
              <th style={{ padding: '8px 12px', textAlign: 'right', borderRight: '1px solid #e0e0e0', whiteSpace: 'nowrap' }}>
                USD价值
                <SortButton active={sortConfig.key === 'usd_value'} direction={sortConfig.direction} onClick={() => handleSort('usd_value')} />
              </th>
              <th style={{ padding: '8px 12px', textAlign: 'center', whiteSpace: 'nowrap' }}>
                操作
                <SortButton active={sortConfig.key === 'hash'} direction={sortConfig.direction} onClick={() => handleSort('hash')} />
              </th>
            </tr>
          </thead>
          <tbody>
            {sortedTransactions.map((tx, index) => (
              <tr key={index} style={{
                borderBottom: '1px solid #f0f0f0',
                backgroundColor: index % 2 === 0 ? '#ffffff' : '#fafafa'
              }}>
                <td style={{ padding: '8px 12px', textAlign: 'center', borderRight: '1px solid #e0e0e0' }}>
                  <input
                    type="checkbox"
                    checked={selectedRows.has(index)}
                    onChange={() => handleTransactionSelect(index)}
                    style={{ cursor: 'pointer' }}
                  />
                </td>
                <td style={{ padding: '8px 12px', borderRight: '1px solid #e0e0e0', fontSize: '11px' }}>
                  {formatTime(tx.timestamp)}
                </td>
                <td style={{ padding: '8px 12px', borderRight: '1px solid #e0e0e0' }}>
                  <div 
                    style={{ 
                      fontWeight: '500', 
                      cursor: 'pointer',
                      color: '#1976d2',
                      textDecoration: 'underline',
                      fontSize: '11px'
                    }}
                    onClick={() => copyToClipboard(tx.from_address, '发送方地址')}
                    title="点击复制发送方地址"
                  >
                    {tx.from_friendly_name || 'Unknown'}
                  </div>
                  <div style={{ fontSize: '10px', color: '#666' }}>{tx.from_grp_name || 'Unknown Group'}</div>
                </td>
                <td style={{ padding: '8px 12px', borderRight: '1px solid #e0e0e0' }}>
                  <div 
                    style={{ 
                      fontWeight: '500', 
                      cursor: 'pointer',
                      color: '#1976d2',
                      textDecoration: 'underline',
                      fontSize: '11px'
                    }}
                    onClick={() => copyToClipboard(tx.to_address, '接收方地址')}
                    title="点击复制接收方地址"
                  >
                    {tx.to_friendly_name || 'Unknown'}
                  </div>
                  <div style={{ fontSize: '10px', color: '#666' }}>{tx.to_grp_name || 'Unknown Group'}</div>
                </td>
                <td style={{ padding: '8px 12px', textAlign: 'right', borderRight: '1px solid #e0e0e0', fontFamily: 'monospace' }}>
                  {formatAmount(tx.amount, tx.token_symbol)}
                </td>
                <td style={{ padding: '8px 12px', textAlign: 'right', borderRight: '1px solid #e0e0e0', fontFamily: 'monospace' }}>
                  {formatUSDValue(tx.usd_value)}
                </td>
                <td style={{ padding: '8px 12px', textAlign: 'center' }}>
                  <button
                    onClick={() => copyToClipboard(tx.hash, '交易哈希')}
                    style={{
                      background: '#1976d2',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '4px 8px',
                      fontSize: '10px',
                      cursor: 'pointer',
                      fontFamily: 'monospace'
                    }}
                    title="复制交易哈希"
                  >
                    复制哈希
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr style={{ background: '#f5f5f5', fontWeight: 'bold', color: '#1976d2' }}>
              <td colSpan={3} style={{ textAlign: 'right', borderRight: '1px solid #e0e0e0' }}>ETH总量：</td>
              <td style={{ textAlign: 'right', fontFamily: 'monospace' }}>{summary.ethAmount.toLocaleString('en-US', { maximumFractionDigits: 6 })}</td>
              <td colSpan={3}></td>
            </tr>
            <tr style={{ background: '#f5f5f5', fontWeight: 'bold', color: '#1976d2' }}>
              <td colSpan={3} style={{ textAlign: 'right', borderRight: '1px solid #e0e0e0' }}>ETH总USD价值：</td>
              <td style={{ textAlign: 'right', fontFamily: 'monospace' }}> ${summary.ethUsd.toLocaleString('en-US', { maximumFractionDigits: 2 })}</td>
              <td colSpan={3}></td>
            </tr>
            <tr style={{ background: '#f5f5f5', fontWeight: 'bold', color: '#1976d2' }}>
              <td colSpan={3} style={{ textAlign: 'right', borderRight: '1px solid #e0e0e0' }}>USDC总量：</td>
              <td style={{ textAlign: 'right', fontFamily: 'monospace' }}>${summary.usdcAmount.toLocaleString('en-US', { maximumFractionDigits: 2 })}</td>
              <td colSpan={3}></td>
            </tr>
            <tr style={{ background: '#f5f5f5', fontWeight: 'bold', color: '#1976d2' }}>
              <td colSpan={3} style={{ textAlign: 'right', borderRight: '1px solid #e0e0e0' }}>USDT总量：</td>
              <td style={{ textAlign: 'right', fontFamily: 'monospace' }}>${summary.usdtAmount.toLocaleString('en-US', { maximumFractionDigits: 2 })}</td>
              <td colSpan={3}></td>
            </tr>
            <tr style={{ background: '#f5f5f5', fontWeight: 'bold', color: '#1976d2' }}>
              <td colSpan={3} style={{ textAlign: 'right', borderRight: '1px solid #e0e0e0' }}>总USD价值：</td>
              <td style={{ textAlign: 'right', fontFamily: 'monospace' }}>${summary.totalUsd.toLocaleString('en-US', { maximumFractionDigits: 2 })}</td>
              <td style={{ textAlign: 'left', fontFamily: 'monospace' }}>(${formatAbbreviated(summary.totalUsd)})</td>
              <td></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
};

// 排序按钮组件
const SortButton = ({ active, direction, onClick }) => {
  let symbol = '↕️';
  if (active && direction === 'asc') symbol = '▲';
  if (active && direction === 'desc') symbol = '▼';
  return (
    <button
      onClick={onClick}
      style={{
        marginLeft: 4,
        border: 'none',
        background: 'none',
        cursor: 'pointer',
        fontSize: '12px',
        color: active ? '#1976d2' : '#888',
        padding: 0
      }}
      title={active ? (direction === 'asc' ? '升序' : '降序') : '排序'}
    >
      {symbol}
    </button>
  );
};

export default function TransactionsChart({ data, height = 500, fromGroup = '', toGroup = '', selectedTokens = [], timeAggregation = '1h', deselectedFromGroups = [], deselectedToGroups = [] }) {
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);
  const seriesRefs = useRef([]);
  const legendRef = useRef(null);
  const [ethPriceData, setEthPriceData] = useState([]);
  const [isLoadingPrices, setIsLoadingPrices] = useState(false);
  const [selectedTransactions, setSelectedTransactions] = useState([]);
  const [selectedTimeRange, setSelectedTimeRange] = useState(null);
  const [isClickMode, setIsClickMode] = useState(false);
  const [isLoadingDetails, setIsLoadingDetails] = useState(false);

  // 获取指定时间范围内的详细交易数据
  const fetchTransactionDetails = async (startTime, endTime, token) => {
    // //console.log('🔍 开始获取交易详情，时间范围:', {
    //   startTime: new Date(startTime).toLocaleString(),
    //   endTime: new Date(endTime).toLocaleString(),
    //   token
    // });
    
    setIsLoadingDetails(true);
    
    try {
      // 构建查询参数
      const params = new URLSearchParams({
        startTime: Math.floor(startTime / 1000).toString(), // 转换为秒
        endTime: Math.floor(endTime / 1000).toString(), // 转换为秒
        limit: '2000' // 获取更多数据
      });
      
      // 添加代币过滤 - 始终使用选中的代币列表，而不是点击的代币
      if (selectedTokens.length > 0) {
        // 使用选中的代币列表，用逗号分隔
        params.append('token', selectedTokens.join(','));
        //console.log('🔍 传递选中的代币:', selectedTokens);
      } else if (token && token !== 'Unknown') {
        // 如果没有选中任何代币，才使用点击的代币
        params.append('token', token);
        //console.log('🔍 传递点击的代币:', token);
      }
      
      // 添加钱包组过滤 - 用逗号分隔
      if (fromGroup) {
        // 将逗号分隔的fromGroup拆分为多个参数
        const fromGroups = fromGroup.split(',').map(g => g.trim()).filter(g => g);
        fromGroups.forEach(group => {
          params.append('fromGroup', group);
        });
      }
      if (toGroup) {
        // 将逗号分隔的toGroup拆分为多个参数
        const toGroups = toGroup.split(',').map(g => g.trim()).filter(g => g);
        toGroups.forEach(group => {
          params.append('toGroup', group);
        });
      }
      
      // 添加deselected参数
      if (deselectedFromGroups.length > 0) {
        params.append('deselectedFromGroup', deselectedFromGroups.join(','));
      }
      if (deselectedToGroups.length > 0) {
        params.append('deselectedToGroup', deselectedToGroups.join(','));
      }
      
      const url = `/api/transactions?${params}`;
      //console.log('🔍 请求URL:', url);
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      //console.log('🔍 获取到交易详情:', result.data?.length || 0, '条记录');
      
      if (result.success && result.data) {
        return result.data;
      } else {
        console.error('❌ 获取交易详情失败:', result.error);
        return [];
      }
    } catch (error) {
      console.error('❌ 获取交易详情时出错:', error);
      return [];
    } finally {
      setIsLoadingDetails(false);
    }
  };

  // 处理点击事件的函数
  const handleChartClick = async (param) => {
    //console.log('🔍 图表点击事件触发:', param);
    
    // 安全检查：确保组件仍然挂载
    if (!chartContainerRef.current) {
      //console.log('⚠️ chartContainerRef.current 为空，跳过点击处理');
      return;
    }
    
    if (param.seriesData && param.seriesData.size > 0) {
      //console.log('🔍 点击事件包含系列数据，系列数量:', param.seriesData.size);
      
      // 遍历所有系列数据
      for (const [series, seriesData] of param.seriesData) {
        //console.log('🔍 检查系列:', series.options().name, '数据:', seriesData);
        
        if (seriesData && seriesData.time) {
          //console.log('🔍 找到时间数据:', seriesData.time);
          
          // 计算时间范围
          const clickedTime = seriesData.time;
          let startTime, endTime;
          
          // 根据时间聚合级别计算时间范围
          switch (timeAggregation) {
            case '1m':
              startTime = clickedTime;
              endTime = clickedTime + 60 * 1000; // 1分钟
              break;
            case '5m':
              startTime = clickedTime;
              endTime = clickedTime + 5 * 60 * 1000; // 5分钟
              break;
            case '10m':
              startTime = clickedTime;
              endTime = clickedTime + 10 * 60 * 1000; // 10分钟
              break;
            case '30m':
              startTime = clickedTime;
              endTime = clickedTime + 30 * 60 * 1000; // 30分钟
              break;
            case '1h':
              startTime = clickedTime;
              endTime = clickedTime + 60 * 60 * 1000; // 1小时
              break;
            case '4h':
              startTime = clickedTime;
              endTime = clickedTime + 4 * 60 * 60 * 1000; // 4小时
              break;
            default:
              startTime = clickedTime;
              endTime = clickedTime + 60 * 60 * 1000; // 默认1小时
          }
          
          //console.log('🔍 计算的时间范围:', {
            // startTime: new Date(startTime).toLocaleString(),
          //   endTime: new Date(endTime).toLocaleString()
          // });
          
          // 获取代币信息
          const token = series.options().name.split(' ')[0] || 'Unknown';
          
          // 获取该时间范围内的详细交易数据
          const transactionDetails = await fetchTransactionDetails(startTime, endTime, token);
          
          if (transactionDetails.length > 0) {
            //console.log('🔍 获取到交易详情，交易数量:', transactionDetails.length);
            //console.log('🔍 交易详情:', transactionDetails);
            
            setSelectedTransactions(transactionDetails);
            setSelectedTimeRange({
              time: seriesData.time,
              volume: seriesData.value,
              token: token,
              startTime: startTime,
              endTime: endTime
            });
            setIsClickMode(true);
            
            //console.log('✅ 已设置选中的交易数据');
          } else {
            //console.log('⚠️ 该时间范围内没有找到交易数据');
          }
          
          // 只处理第一个包含数据的系列
          break;
        }
      }
    } else {
      //console.log('🔍 点击事件没有包含系列数据');
    }
  };

  // 获取ETH价格数据
  const fetchEthPrices = async () => {
    if (data.length === 0) {
      //console.log('⚠️ 没有交易数据，跳过ETH价格获取');
      return;
    }
    
    //console.log('🔍 开始获取ETH价格数据，交易数量:', data.length);
    setIsLoadingPrices(true);
    
    try {
      // 获取交易数据的时间范围
      const timestamps = data.map(tx => Number(tx.timestamp));
      const minTime = Math.min(...timestamps);
      const maxTime = Math.max(...timestamps);
      
      //console.log('🔍 交易数据时间范围:', {
        // minTime: new Date(minTime * 1000).toLocaleString(),
        // maxTime: new Date(maxTime * 1000).toLocaleString(),
        // duration: Math.floor((maxTime - minTime) / 3600) + '小时'
      // });
      
      // 根据时间范围选择interval
      const duration = maxTime - minTime;
      let interval = '1h';
      if (duration <= 3600) { // 1小时内
        interval = '1m';
      } else if (duration <= 6 * 3600) { // 6小时内
        interval = '5m';
      } else if (duration <= 24 * 3600) { // 24小时内
        interval = '15m';
      } else if (duration <= 7 * 24 * 3600) { // 7天内
        interval = '1h';
      } else { // 超过7天
        interval = '4h';
      }
      
      //console.log('🔍 选择的interval:', interval);
      
      // 获取ETH价格数据
      const priceData = await getEthUsdtPrices(minTime, maxTime, interval);
      
      //console.log('🔍 ETH价格数据获取完成:', priceData.length, '条');
      setEthPriceData(priceData);
    } catch (error) {
      console.error('Error fetching ETH prices:', error);
    } finally {
      setIsLoadingPrices(false);
    }
  };

  // 当数据更新时获取ETH价格
  useEffect(() => {
    fetchEthPrices();
  }, [data]);

  // 创建图表，只创建一次
  useEffect(() => {
    if (!chartContainerRef.current) {
      //console.log('⚠️ chartContainerRef.current 为空，跳过图表创建');
      return;
    }
    if (chartRef.current) {
      //console.log('⚠️ 图表已存在，跳过重复创建');
      return;
    }
    
    //console.log('🔍 开始创建图表，容器宽度:', chartContainerRef.current.clientWidth);
    
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height,
      layout: { 
        background: { color: '#ffffff' }, 
        textColor: '#333' 
      },
      grid: { 
        vertLines: { color: '#f0f0f0' }, 
        horzLines: { color: '#f0f0f0' } 
      },
      crosshair: {
        mode: 1, // 启用十字线模式
        vertLine: {
          color: '#999',
          width: 1,
          style: 0,
          labelBackgroundColor: '#f0f0f0',
        },
        horzLine: {
          color: '#999',
          width: 1,
          style: 0,
          labelBackgroundColor: '#f0f0f0',
        },
      },
      rightPriceScale: { 
        borderColor: '#ddd',
        scaleMargins: {
          top: 0.1,
          bottom: 0.1,
        },
      },
      leftPriceScale: { 
        borderColor: '#ddd',
        scaleMargins: {
          top: 0.1,
          bottom: 0.1,
        },
        visible: true,
      },
      timeScale: { 
        borderColor: '#ddd',
        timeVisible: true, 
        secondsVisible: false,
        timeUnit: timeAggregation.includes('m') ? 'minute' : 'hour',
        rightOffset: 0,
        leftOffset: 12,
        barSpacing: 6,
        fixLeftEdge: false,
        lockVisibleTimeRangeOnResize: true,
        rightBarStaysOnScroll: true,
        borderVisible: false,
        visible: true,
        tickMarkFormatter: (time) => {
          // 将时间戳转换为本地时间
          const date = new Date(time);
          const options = {
            timeZone: 'America/New_York',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
          };
          const easternTime = new Intl.DateTimeFormat('en-US', options).format(date);
          return easternTime;
        },
      },
      localization: {
        timeFormatter: (time) => {
          const date = new Date(time);
          return date.toLocaleString('en-US', {
            timeZone: 'America/New_York',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
          });
        }
      }
    });
    
    //console.log('✅ 图表创建成功');
    
    chartRef.current = chart;
    //console.log('🔍 chartRef.current 已设置:', !!chartRef.current);
    seriesRefs.current = [];
    
    // 创建工具提示元素
    const tooltip = document.createElement('div');
    tooltip.style.position = 'absolute';
    tooltip.style.display = 'none';
    tooltip.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
    tooltip.style.color = '#333';
    tooltip.style.padding = '12px 16px';
    tooltip.style.borderRadius = '8px';
    tooltip.style.fontSize = '12px';
    tooltip.style.fontFamily = 'Arial, sans-serif';
    tooltip.style.pointerEvents = 'none';
    tooltip.style.zIndex = '1000';
    tooltip.style.whiteSpace = 'nowrap';
    tooltip.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    tooltip.style.border = '1px solid rgba(0, 0, 0, 0.1)';
    tooltip.style.minWidth = '160px';
    tooltip.style.maxWidth = '220px';
    chartContainerRef.current.appendChild(tooltip);
    
    // //console.log('🔍 工具提示元素已创建');
    
    // 响应式调整
    const handleResize = () => {
      if (chartRef.current && chartContainerRef.current) {
        chartRef.current.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };
    window.addEventListener('resize', handleResize);
    
    // 添加点击事件监听器 - 在图表创建时添加，只添加一次
    //console.log('🔍 添加图表点击事件监听器');
    chart.subscribeClick(handleChartClick);
    
    // 添加鼠标事件监听器
    //console.log('🔍 开始设置鼠标事件监听器');
    chart.subscribeCrosshairMove((param) => {
      // 如果当前有选中的交易，不显示工具提示，避免干扰点击事件
      if (selectedTransactions.length > 0) {
        return;
      }
      
      // 安全检查：确保 chartContainerRef.current 存在
      if (!chartContainerRef.current) {
        return;
      }
      
      // //console.log('🔍 鼠标移动事件触发:', param);
      if (param.time && param.seriesData) {
        const rect = chartContainerRef.current.getBoundingClientRect();
        let tooltipContent = '';
        let hasData = false;
        
        // //console.log('🔍 系列数据:', param.seriesData);
        
        // 遍历所有系列，获取数据
        seriesRefs.current.forEach(series => {
          const seriesData = param.seriesData.get(series);
          // //console.log('🔍 系列数据:', series, seriesData);
          
          if (seriesData && seriesData.value !== undefined) {
            hasData = true;
            const seriesName = series.options().name || 'Unknown';
            
            if (seriesName.includes('Volume')) {
              // 显示交易量
              const formattedVolume = Math.abs(seriesData.value).toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 6
              });
              const tokenSymbol = seriesName.split(' ')[0]; // 提取代币符号
              tooltipContent += `
                <div style="margin-bottom: 4px;">
                  <div style="font-weight: bold; color: #333;">${tokenSymbol} 交易量</div>
                  <div style="font-size: 12px; color: #666;">${formattedVolume} ${tokenSymbol}</div>
                </div>
              `;
            } else if (seriesName.includes('ETH Price')) {
              // 显示ETH价格
              const formattedPrice = seriesData.value.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
              });
              tooltipContent += `
                <div style="margin-bottom: 4px;">
                  <div style="font-weight: bold; color: #1976d2;">ETH价格</div>
                  <div style="font-size: 12px; color: #1976d2;">$${formattedPrice}</div>
                </div>
              `;
            }
          }
        });
        
        // 显示时间信息
        if (hasData) {
          const date = new Date(param.time);
          const timeString = date.toLocaleString('en-US', {
            timeZone: 'America/New_York',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
          });
          
          tooltipContent = `
            <div style="margin-bottom: 6px; font-size: 11px; color: #999; border-bottom: 1px solid #eee; padding-bottom: 4px;">
              ${timeString}
            </div>
            ${tooltipContent}
          `;
        }
        
        // //console.log('🔍 工具提示内容:', tooltipContent);
        
        if (tooltipContent) {
          tooltip.innerHTML = tooltipContent;
          tooltip.style.display = 'block';
          
          // 计算工具提示位置 - 显示在鼠标指针附近
          const tooltipWidth = 180; // 增加宽度以适应更多内容
          const tooltipHeight = tooltipContent.split('<div').length * 25 + 20; // 根据内容动态计算高度
          
          let left = param.point.x + 10; // 鼠标右侧10px
          let top = param.point.y - tooltipHeight - 10; // 鼠标上方10px
          
          // 确保工具提示不超出容器边界
          if (left + tooltipWidth > rect.width) {
            left = param.point.x - tooltipWidth - 10; // 显示在鼠标左侧
          }
          
          if (top < 0) {
            top = param.point.y + 10; // 显示在鼠标下方
          }
          
          tooltip.style.left = `${left}px`;
          tooltip.style.top = `${top}px`;
          
          // //console.log('🔍 工具提示已显示，位置:', { left, top });
        }
      } else {
        tooltip.style.display = 'none';
        // //console.log('🔍 隐藏工具提示');
      }
    });

    // 鼠标离开图表时隐藏工具提示
    chartContainerRef.current.addEventListener('mouseleave', () => {
      if (tooltip) {
        tooltip.style.display = 'none';
      }
      // //console.log('🔍 鼠标离开，隐藏工具提示');
    });
    
    return () => {
      // //console.log('🔍 清理图表资源');
      window.removeEventListener('resize', handleResize);
      
      // 清理图表实例
      if (chartRef.current) {
        try {
          chartRef.current.remove();
        } catch (error) {
          console.error('Error removing chart:', error);
        }
        chartRef.current = null;
      }
      
      // 清理图例
      if (legendRef.current) {
        try {
          legendRef.current.remove();
        } catch (error) {
          console.error('Error removing legend:', error);
        }
        legendRef.current = null;
      }
      
      // 清理工具提示
      if (tooltip) {
        try {
          tooltip.remove();
        } catch (error) {
          console.error('Error removing tooltip:', error);
        }
      }
      
      // 清理系列引用
      seriesRefs.current = [];
    };
  }, [height, timeAggregation]); // 移除 selectedTransactions 依赖

  // 更新图表数据 - 独立于表格数据
  useEffect(() => {
    if (!chartRef.current) {
      //console.log('⚠️ chartRef.current 为空，跳过图表数据更新');
      return;
    }
    
    //console.log('🔍 开始更新图表，交易数据:', data);
    
    // 清除旧的 series
    try {
      seriesRefs.current.forEach(s => {
        if (s && chartRef.current && typeof chartRef.current.removeSeries === 'function') {
          chartRef.current.removeSeries(s);
        }
      });
    } catch (error) {
      console.error('Error removing series:', error);
    }
    seriesRefs.current = [];
    
    // 清除旧 legend
    if (legendRef.current) {
      try {
        legendRef.current.remove();
      } catch (error) {
        console.error('Error removing legend:', error);
      }
      legendRef.current = null;
    }
    
    if (data.length === 0) {
      //console.log('⚠️ 没有交易数据，跳过图表更新');
      return;
    }
    
    // 按代币分组数据
    const tokenGroups = {};
    data.forEach(tx => {
      const token = tx.token_symbol || 'Unknown';
      if (!tokenGroups[token]) tokenGroups[token] = [];
      tokenGroups[token].push(tx);
    });
    
    //console.log('🔍 按代币分组后的数据:', tokenGroups);
    
    // 为每个代币创建柱状图和线图系列
    Object.entries(tokenGroups).forEach(([token, txs], index) => {
      //console.log(`🔍 处理代币 ${token}，交易数量: ${txs.length}`);
      
      // 按时间分组（根据选择的时间聚合级别）
      const aggregatedData = {};
      
      txs.forEach(tx => {
        // 使用 Number() 而不是 parseInt()，参考 FlowChart.jsx
        const timestamp = Number(tx.timestamp) * 1000; // Unix时间戳转毫秒
        const date = new Date(timestamp);
        
        // 根据时间聚合级别计算时间桶
        let timeBucket;
        switch (timeAggregation) {
          case '1m':
            // 1分钟聚合
            timeBucket = new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), date.getMinutes()).getTime();
            break;
          case '5m':
            // 5分钟聚合
            const minutes5 = Math.floor(date.getMinutes() / 5) * 5;
            timeBucket = new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), minutes5).getTime();
            break;
          case '10m':
            // 10分钟聚合
            const minutes10 = Math.floor(date.getMinutes() / 10) * 10;
            timeBucket = new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), minutes10).getTime();
            break;
          case '30m':
            // 30分钟聚合
            const minutes30 = Math.floor(date.getMinutes() / 30) * 30;
            timeBucket = new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours(), minutes30).getTime();
            break;
          case '1h':
            // 1小时聚合
            timeBucket = new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours()).getTime();
            break;
          case '4h':
            // 4小时聚合
            const hours4 = Math.floor(date.getHours() / 4) * 4;
            timeBucket = new Date(date.getFullYear(), date.getMonth(), date.getDate(), hours4).getTime();
            break;
          default:
            // 默认1小时聚合
            timeBucket = new Date(date.getFullYear(), date.getMonth(), date.getDate(), date.getHours()).getTime();
        }
        
        // 调试时间信息
        if (txs.indexOf(tx) < 3) { // 只显示前3条记录的时间信息
          //console.log(`🔍 原始时间戳: ${tx.timestamp}, 转换后: ${timestamp}, 日期: ${date.toLocaleString('zh-CN')}, ${timeAggregation}聚合: ${new Date(timeBucket).toLocaleString('zh-CN')}`);
        }
        
        if (!aggregatedData[timeBucket]) {
          aggregatedData[timeBucket] = { volume: 0, count: 0, totalValue: 0 };
        }
        aggregatedData[timeBucket].volume += parseFloat(tx.amount) || 0;
        aggregatedData[timeBucket].count += 1;
        aggregatedData[timeBucket].totalValue += parseFloat(tx.usd_value) || 0;
      });
      
      //console.log(`🔍 ${token} 按${timeAggregation}聚合后的数据:`, aggregatedData);
      
      // 获取代币固定颜色
      const getTokenColor = (tokenSymbol) => {
        switch (tokenSymbol.toUpperCase()) {
          case 'ETH':
            return '#3B82F6'; // 蓝色
          case 'USDT':
            return '#10B981'; // 绿色
          case 'USDC':
            return '#F59E0B'; // 黄色
          default:
            return '#6B7280'; // 默认灰色
        }
      };
      
      const tokenColor = getTokenColor(token);
      
      // 柱状图数据 - 参考 FlowChart.jsx 的数据格式
      const chartData = Object.entries(aggregatedData).map(([time, data]) => ({
        time: Number(time), // 使用 Number() 而不是 parseInt()
        value: data.volume,
        color: tokenColor
      })).sort((a, b) => a.time - b.time); // 按时间升序排列
      
      //console.log(`🔍 ${token} 柱状图数据:`, chartData);
      
      if (chartRef.current && typeof chartRef.current.addHistogramSeries === 'function') {
        try {
          const volumeSeries = chartRef.current.addHistogramSeries({
            name: `${token} Volume`,
            color: tokenColor,
            priceFormat: { type: 'volume' },
            priceScaleId: index === 0 ? 'right' : `right-${index}`,
          });
          
          // 设置数据
          volumeSeries.setData(chartData);
          //console.log(`✅ ${token} 柱状图系列创建成功，数据点数量:`, chartData.length);
          
          seriesRefs.current.push(volumeSeries);
        } catch (error) {
          console.error('Error adding volume series:', error);
        }
      }
    });

    // 添加ETH价格线
    //console.log('🔍 检查ETH价格数据:', ethPriceData);
    if (ethPriceData && ethPriceData.length > 0 && chartRef.current && typeof chartRef.current.addLineSeries === 'function') {
      //console.log('🔍 开始添加ETH价格线');
      try {
        const ethPriceSeries = chartRef.current.addLineSeries({
          name: 'ETH Price',
          color: '#1976d2',
          lineWidth: 2,
          priceFormat: {
            type: 'price',
            precision: 2,
            minMove: 0.01,
          },
          priceScaleId: 'left-eth',
          crosshairMarkerVisible: true,
          lastValueVisible: true,
        });
        //console.log('🔍 ETH价格线创建成功，设置数据:', ethPriceData);
        ethPriceSeries.setData(ethPriceData);
        seriesRefs.current.push(ethPriceSeries);
        //console.log('✅ ETH价格线添加成功');
      } catch (error) {
        console.error('❌ Error adding ETH price series:', error);
      }
    } 
    // else {
      //console.log('⚠️ 跳过ETH价格线添加:', {
        // hasEthPriceData: !!ethPriceData,
        // ethPriceDataLength: ethPriceData?.length,
        // hasChartRef: !!chartRef.current,
        // hasAddLineSeries: !!(chartRef.current && typeof chartRef.current.addLineSeries === 'function')
      //});

    // }

    // 设置时间范围，让数据紧贴右侧显示
    if (Object.keys(tokenGroups).length > 0 && chartRef.current && chartRef.current.timeScale) {
      try {
        const allData = Object.values(tokenGroups).flat();
        if (allData.length > 0) {
          const processedData = allData.map(tx => ({
            time: Number(tx.timestamp) * 1000,
            value: parseFloat(tx.amount) || 0
          })).sort((a, b) => a.time - b.time);

          if (processedData.length > 0) {
            const lastTime = processedData[processedData.length - 1].time;
            const N = 150;
            const from = processedData.length > N
              ? processedData[processedData.length - N].time
              : processedData[0].time;
            chartRef.current.timeScale().setVisibleRange({
              from,
              to: lastTime
            });
            // 关键：滚动到最右侧
            chartRef.current.timeScale().scrollToRealTime();
          }
        }
      } catch (error) {
        console.error('Error setting time range:', error);
      }
    }

    // 添加图例
    if (Object.keys(tokenGroups).length > 0 && chartContainerRef.current) {
      const legend = document.createElement('div');
      legend.style.position = 'absolute';
      legend.style.left = '12px';
      legend.style.top = '12px';
      legend.style.zIndex = '1';
      legend.style.fontSize = '12px';
      legend.style.fontFamily = 'Arial, sans-serif';
      
      const fromGroupDisplay = fromGroup || '所有发送方组';
      const toGroupDisplay = toGroup || '所有接收方组';
      const tokenDisplay = selectedTokens.length > 0 ? selectedTokens.join(', ') : '所有代币';
      const timeDisplay = timeAggregation === '1m' ? '1分钟' : 
                         timeAggregation === '5m' ? '5分钟' : 
                         timeAggregation === '10m' ? '10分钟' : 
                         timeAggregation === '30m' ? '30分钟' : 
                         timeAggregation === '1h' ? '1小时' : 
                         timeAggregation === '4h' ? '4小时' : '1小时';
      
      let legendHtml = `<div style="font-weight: bold; margin-bottom: 8px;">${fromGroupDisplay} → ${toGroupDisplay} (${tokenDisplay}) - ${timeDisplay}聚合</div>`;
      
      // 添加代币数据系列
      Object.entries(tokenGroups).forEach(([token, txs], index) => {
        const getTokenColor = (tokenSymbol) => {
          switch (tokenSymbol.toUpperCase()) {
            case 'ETH':
              return '#3B82F6'; // 蓝色
            case 'USDT':
              return '#10B981'; // 绿色
            case 'USDC':
              return '#F59E0B'; // 黄色
            default:
              return '#6B7280'; // 默认灰色
          }
        };
        
        const color = getTokenColor(token);
        legendHtml += `<div style="margin: 2px 0;"><span style="color: ${color};">■</span> ${token} Volume</div>`;
      });
      
      // 添加ETH价格线
      if (ethPriceData && ethPriceData.length > 0) {
        //console.log('🔍 在图例中添加ETH价格线');
        // 根据数据量估算interval
        const duration = ethPriceData.length > 0 ? 
          (ethPriceData[ethPriceData.length - 1].time - ethPriceData[0].time) / (1000 * 60) : 0;
        const estimatedInterval = duration <= 60 ? '1m' : 
                                 duration <= 360 ? '5m' : 
                                 duration <= 1440 ? '15m' : 
                                 duration <= 10080 ? '1h' : '4h';
        legendHtml += `<div style="margin: 2px 0;"><span style="color: #1976d2;">─</span> ETH Price (${estimatedInterval})</div>`;
      } else {
        //console.log('⚠️ 图例中跳过ETH价格线，ethPriceData:', ethPriceData);
      }
      
      legend.innerHTML = legendHtml;
      chartContainerRef.current.appendChild(legend);
      legendRef.current = legend;
    }
    
    //console.log('✅ 图表更新完成');
  }, [data, fromGroup, toGroup, selectedTokens, timeAggregation, ethPriceData]); // 移除 selectedTransactions 依赖

  // 关闭交易详情表格
  const closeTransactionDetails = () => {
    //console.log('🔍 关闭交易详情表格');
    setSelectedTransactions([]);
    setSelectedTimeRange(null);
    setIsClickMode(false);
  };

  return (
    <div style={{ position: 'relative' }}>
      <div ref={chartContainerRef} style={{ position: 'relative' }} />
      {isLoadingPrices && (
        <div style={{
          position: 'absolute',
          top: '10px',
          right: '10px',
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          padding: '4px 8px',
          borderRadius: '4px',
          fontSize: '11px',
          color: '#666',
          zIndex: '1001'
        }}>
          获取ETH价格中...
        </div>
      )}
      
      {/* 交易详情表格 */}
      <TransactionDetailsTable 
        transactions={selectedTransactions} 
        onClose={closeTransactionDetails}
      />
      
      {/* 加载详情指示器 */}
      {isLoadingDetails && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          padding: '12px 20px',
          borderRadius: '8px',
          fontSize: '14px',
          color: '#333',
          zIndex: '1002',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          border: '1px solid rgba(0, 0, 0, 0.1)'
        }}>
          正在获取交易详情...
        </div>
      )}
    </div>
  );
}