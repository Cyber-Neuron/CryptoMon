'use client';

import { useState, useEffect } from 'react';
import FlowChart from '../components/FlowChart';

export default function Home() {
  const [tokens, setTokens] = useState([]);
  const [groups, setGroups] = useState([]);
  const [selectedTokens, setSelectedTokens] = useState([]);
  const [selectedGroups, setSelectedGroups] = useState([]);
  const [fromGroups, setFromGroups] = useState([]);
  const [toGroups, setToGroups] = useState([]);
  const [timeRange, setTimeRange] = useState('24h');
  const [chartData, setChartData] = useState({});
  const [loading, setLoading] = useState(false);
  const [ethPriceData, setEthPriceData] = useState([]);

  // 获取可用的代币和组别
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const [tokensRes, groupsRes] = await Promise.all([
          fetch('/api/tokens'),
          fetch('/api/groups')
        ]);
        
        const tokensData = await tokensRes.json();
        const groupsData = await groupsRes.json();
        
        if (tokensData.success) {
          setTokens(tokensData.data);
          setSelectedTokens(tokensData.data.slice(0, 3)); // 默认选择前3个代币
        }
        
        if (groupsData.success) {
          setGroups(groupsData.data);
          // setSelectedGroups(groupsData.data.slice(0, 5)); // 默认选择前5个组别

          // 新增：根据最近24小时交易数据统计出现最多的5个组别
          const now = Math.floor(Date.now() / 1000);
          const startTime = now - 86400;
          const resp = await fetch('/api/flows', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ startTime, endTime: now, tokens: tokensData.data, groups: [] })
          });
          const flowResult = await resp.json();
          //console.log('flowResult:', flowResult);
          // 用 rawFlowData 统计 top5 group
          const rawData = flowResult.rawFlowData || flowResult.data; // 兼容老数据
          if (flowResult.success && Array.isArray(rawData)) {
            const groupCount = {};
            rawData.forEach(item => {
              if (item.from_grp_name && item.from_grp_name !== 'unk') {
                groupCount[item.from_grp_name] = (groupCount[item.from_grp_name] || 0) + 1;
              }
              if (item.to_grp_name && item.to_grp_name !== 'unk') {
                groupCount[item.to_grp_name] = (groupCount[item.to_grp_name] || 0) + 1;
              }
            });
            //console.log('groupCount (from raw flowData):', groupCount);
            const groupEntries = Object.entries(groupCount);
            //console.log('groupEntries before sort:', groupEntries);
            const sortedGroups = groupEntries.sort((a, b) => b[1] - a[1]);
            //console.log('sortedGroups:', sortedGroups);
            const topGroups = sortedGroups
              .slice(0, 5)
              .map(([name]) => name);
            //console.log('Top 5 groups for selected tokens:', topGroups);
            setSelectedGroups(topGroups);
            setFromGroups(topGroups.slice(0, 3));
            setToGroups(topGroups.slice(0, 3));
          } else {
            setSelectedGroups(groupsData.data.slice(0, 5));
            setFromGroups(groupsData.data.slice(0, 3));
            setToGroups(groupsData.data.slice(0, 3));
          }
        }
      } catch (error) {
        console.error('Error fetching options:', error);
      }
    };
    
    fetchOptions();
  }, []);

  // 获取ETH价格数据的函数
  const fetchEthPrices = async (earliestTime, latestTime) => {
    // 直接在这里实现 getEthPricesForTimeRange 的逻辑
    const durationSeconds = latestTime - earliestTime;
    let interval = "5m";
    if (durationSeconds <= 6 * 3600) {
      interval = "1m";
    } else if (durationSeconds <= 24 * 3600) {
      interval = "5m";
    } else if (durationSeconds <= 7 * 24 * 3600) {
      interval = "10m";
    } else {
      interval = "1h";
    }
    const url = "https://api.binance.com/api/v3/klines";
    const params = new URLSearchParams({
      symbol: "ETHUSDT",
      interval,
      startTime: (earliestTime * 1000).toString(),
      endTime: (latestTime * 1000).toString(),
    });
    try {
      const resp = await fetch(`${url}?${params}`, { timeout: 10000 });
      const data = await resp.json();
      if (Array.isArray(data)) {
        return data.map(kline => ({
          time: Math.floor(parseInt(kline[0]) / 1000),
          value: parseFloat(kline[1])
        }));
      } else {
        return [];
      }
    } catch (error) {
      console.error("Error fetching ETH prices for time range:", error);
      return [];
    }
  };

  // 获取资金流数据
  const fetchFlowData = async () => {
    if (selectedTokens.length === 0) return;
    
    setLoading(true);
    try {
      const now = Math.floor(Date.now() / 1000);
      let startTime;
      
      switch (timeRange) {
        case '1h':
          startTime = now - 3600;
          break;
        case '6h':
          startTime = now - 21600;
          break;
        case '24h':
          startTime = now - 86400;
          break;
        case '7d':
          startTime = now - 604800;
          break;
        case '30d':
          startTime = now - 2592000;
          break;
        default:
          startTime = now - 86400;
      }
      
      const response = await fetch('/api/flows', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          startTime,
          endTime: now,
          tokens: selectedTokens,
          groups: selectedGroups,
          fromGroups: fromGroups,
          toGroups: toGroups,
        }),
      });
      
      const result = await response.json();
      
      if (result.success) {
        // 调试：输出时间戳信息
        //console.log('🔍 调试时间戳数据:');
        result.data.slice(0, 5).forEach((item, index) => {
          const date = new Date(item.time * 1000);
          //console.log(`数据 ${index + 1}:`, {
            // timestamp: item.time,
            // date: date.toString(),
            // iso: date.toISOString(),
            // local: date.toLocaleString('en-US', { timeZone: 'America/New_York' })
          // });
        });
        
        // 按代币分组数据
        const groupedData = {};
        result.data.forEach((item) => {
          if (!groupedData[item.token]) {
            groupedData[item.token] = [];
          }
          groupedData[item.token].push(item);
        });
        
        setChartData(groupedData);

        // 计算所有数据的最早和最晚时间戳
        const allTimestamps = result.data.map(item => Number(item.time));
        if (allTimestamps.length > 0) {
          const earliestTime = Math.min(...allTimestamps);
          const latestTime = now; // 使用现在的时间而不是数据中的最晚时间
          // 获取ETH价格数据
          const ethPrices = await fetchEthPrices(earliestTime, latestTime);
          setEthPriceData(ethPrices);
        } else {
          setEthPriceData([]);
        }
      }
    } catch (error) {
      console.error('Error fetching flow data:', error);
    } finally {
      setLoading(false);
    }
  };

  // 当选择项或时间范围改变时重新获取数据
  useEffect(() => {
    fetchFlowData();
  }, [selectedTokens, selectedGroups, fromGroups, toGroups, timeRange]);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Flow Monitor</h1>
        
        {/* 导航链接 */}
        <div className="mb-8">
          <nav className="flex space-x-4">
            <a
              href="/"
              className="px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-md"
            >
              资金流向监控
            </a>
            <a
              href="/etf"
              className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-md"
            >
              ETF流向分析
            </a>
            <a
              href="/transactions"
              className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-md"
            >
              交易记录
            </a>
            <a
              href="/transactions-chart"
              className="px-3 py-2 text-sm font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-md"
            >
              交易图表
            </a>
          </nav>
        </div>
        
        {/* 控制面板 */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            {/* 时间范围选择 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                时间范围
              </label>
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="1h">最近1小时</option>
                <option value="6h">最近6小时</option>
                <option value="24h">最近24小时</option>
                <option value="7d">最近7天</option>
                <option value="30d">最近30天</option>
              </select>
            </div>
            
            {/* 代币选择 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                代币
              </label>
              <select
                multiple
                value={selectedTokens}
                onChange={(e) => {
                  const values = Array.from(e.target.selectedOptions, option => option.value);
                  setSelectedTokens(values);
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                size={4}
              >
                {tokens.map(token => (
                  <option key={token} value={token}>{token}</option>
                ))}
              </select>
            </div>
            
            {/* From组别选择 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                来源组别 (From)
              </label>
              <div className="flex flex-col max-h-32 overflow-y-auto border border-gray-300 rounded-md px-3 py-2">
                {groups.map(group => (
                  <label key={group} className="inline-flex items-center mb-1">
                    <input
                      type="checkbox"
                      className="form-checkbox h-4 w-4 text-red-600"
                      checked={fromGroups.includes(group)}
                      onChange={() => {
                        setFromGroups(fromGroups =>
                          fromGroups.includes(group)
                            ? fromGroups.filter(g => g !== group)
                            : [...fromGroups, group]
                        );
                      }}
                    />
                    <span className="ml-2">{group}</span>
                  </label>
                ))}
              </div>
            </div>
            
            {/* To组别选择 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                目标组别 (To)
              </label>
              <div className="flex flex-col max-h-32 overflow-y-auto border border-gray-300 rounded-md px-3 py-2">
                {groups.map(group => (
                  <label key={group} className="inline-flex items-center mb-1">
                    <input
                      type="checkbox"
                      className="form-checkbox h-4 w-4 text-green-600"
                      checked={toGroups.includes(group)}
                      onChange={() => {
                        setToGroups(toGroups =>
                          toGroups.includes(group)
                            ? toGroups.filter(g => g !== group)
                            : [...toGroups, group]
                        );
                      }}
                    />
                    <span className="ml-2">{group}</span>
                  </label>
                ))}
              </div>
            </div>
            
            {/* 刷新按钮 */}
            <div className="flex items-end">
              <button
                onClick={fetchFlowData}
                disabled={loading}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {loading ? '加载中...' : '刷新数据'}
              </button>
            </div>
          </div>
          
          {/* 显示当前选择的流向信息 */}
          <div className="mt-4 p-3 bg-gray-50 rounded-md">
            <div className="text-sm text-gray-600">
              <div className="flex items-center gap-4">
                <span>当前查看流向：</span>
                <span className="text-red-600 font-medium">
                  {fromGroups.length > 0 ? fromGroups.join(', ') : '所有来源'}
                </span>
                <span>→</span>
                <span className="text-green-600 font-medium">
                  {toGroups.length > 0 ? toGroups.join(', ') : '所有目标'}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        {/* 图表区域 */}
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="text-lg text-gray-600">加载中...</div>
          </div>
        ) : (
          <div className="space-y-8">
            {Object.keys(chartData).map(token => (
              <div key={token} className="bg-white rounded-lg shadow-md p-6">
                <FlowChart 
                  data={chartData[token]} 
                  token={token} 
                  height={400}
                  ethPriceData={ethPriceData}
                  fromGroups={fromGroups}
                  toGroups={toGroups}
                />
              </div>
            ))}
            
            {Object.keys(chartData).length === 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="text-center text-gray-600">
                  暂无数据，请选择代币和组别查看资金流向
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
} 