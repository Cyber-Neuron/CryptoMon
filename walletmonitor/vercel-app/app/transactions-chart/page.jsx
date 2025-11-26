'use client';

import { useState, useEffect } from 'react';
import TransactionsChart from '../../components/TransactionsChart';

export default function TransactionsChartPage() {
  const [transactions, setTransactions] = useState([]);
  const [availableGroups, setAvailableGroups] = useState([]);
  const [availableTokens, setAvailableTokens] = useState([]);
  const [selectedFromGroups, setSelectedFromGroups] = useState([]);
  const [selectedToGroups, setSelectedToGroups] = useState([]);
  const [selectedTokens, setSelectedTokens] = useState([]);
  const [timeAggregation, setTimeAggregation] = useState('1h');
  const [loading, setLoading] = useState(false);
  const [timeRange, setTimeRange] = useState('24h');
  const [showFromDropdown, setShowFromDropdown] = useState(false);
  const [showToDropdown, setShowToDropdown] = useState(false);
  const [showTokenDropdown, setShowTokenDropdown] = useState(false);

  // 可选的时间聚合级别
  const timeAggregationOptions = [
    { value: '1m', label: '1分钟' },
    { value: '5m', label: '5分钟' },
    { value: '10m', label: '10分钟' },
    { value: '30m', label: '30分钟' },
    { value: '1h', label: '1小时' },
    { value: '4h', label: '4小时' }
  ];

  // 获取可用的组名列表
  useEffect(() => {
    const fetchGroups = async () => {
      try {
        const response = await fetch('/api/wallets');
        const result = await response.json();
        if (result.success) {
          // 提取唯一的 grp_name
          const groups = [...new Set(result.data.map(wallet => wallet.grp_name).filter(Boolean))];
          setAvailableGroups(groups);
        }
      } catch (error) {
        console.error('Error fetching groups:', error);
      }
    };
    fetchGroups();
  }, []);

  // 获取可用的代币列表
  useEffect(() => {
    const fetchTokens = async () => {
      try {
        const response = await fetch('/api/tokens');
        const result = await response.json();
        if (result.success) {
          //console.log('🔍 获取到的代币数据:', result.data);
          setAvailableTokens(result.data);
        }
      } catch (error) {
        console.error('Error fetching tokens:', error);
      }
    };
    fetchTokens();
  }, []);

  // 处理全选/取消全选
  const handleSelectAll = (type, selectAll) => {
    if (selectAll) {
      if (type === 'from') {
        setSelectedFromGroups([...availableGroups, 'other']);
      } else if (type === 'to') {
        setSelectedToGroups([...availableGroups, 'other']);
      } else if (type === 'token') {
        setSelectedTokens([...availableTokens]);
      }
    } else {
      if (type === 'from') {
        setSelectedFromGroups([]);
      } else if (type === 'to') {
        setSelectedToGroups([]);
      } else if (type === 'token') {
        setSelectedTokens([]);
      }
    }
  };

  // 处理单个选择
  const handleGroupToggle = (type, group) => {
    if (type === 'from') {
      setSelectedFromGroups(prev => 
        prev.includes(group) 
          ? prev.filter(g => g !== group)
          : [...prev, group]
      );
    } else if (type === 'to') {
      setSelectedToGroups(prev => 
        prev.includes(group) 
          ? prev.filter(g => g !== group)
          : [...prev, group]
      );
    }
  };

  // 处理代币选择
  const handleTokenToggle = (token) => {
    setSelectedTokens(prev => 
      prev.includes(token) 
        ? prev.filter(t => t !== token)
        : [...prev, token]
    );
  };

  // 获取交易数据 - 根据选择的组名和代币过滤
  const fetchTransactions = async () => {
    setLoading(true);
    try {
      const now = Math.floor(Date.now() / 1000);
      let startTime;
      switch (timeRange) {
        case '1h': startTime = now - 3600; break;
        case '6h': startTime = now - 21600; break;
        case '24h': startTime = now - 86400; break;
        case '7d': startTime = now - 604800; break;
        case '30d': startTime = now - 2592000; break;
        default: startTime = now - 86400;
      }
      
      const params = new URLSearchParams({
        limit: '1000000',
        offset: '0',
        startTime: startTime.toString(),
        endTime: now.toString()
      });

      // 添加发送方组过滤 - 用逗号分隔
      if (selectedFromGroups.length > 0) {
        // 将逗号分隔的fromGroup拆分为多个参数
        selectedFromGroups.forEach(group => {
          params.append('fromGroup', group);
        });
      }

      // 添加接收方组过滤 - 用逗号分隔
      if (selectedToGroups.length > 0) {
        // 将逗号分隔的toGroup拆分为多个参数
        selectedToGroups.forEach(group => {
          params.append('toGroup', group);
        });
      }

      // 添加deselected列表 - 用逗号分隔
      if (selectedFromGroups.includes('other')) {
        const deselectedFromGroups = availableGroups.filter(g => !selectedFromGroups.includes(g));
        if (deselectedFromGroups.length > 0) {
          params.append('deselectedFromGroup', deselectedFromGroups.join(','));
        }
        //console.log('🔍 发送方deselected组:', deselectedFromGroups);
      }

      if (selectedToGroups.includes('other')) {
        const deselectedToGroups = availableGroups.filter(g => !selectedToGroups.includes(g));
        if (deselectedToGroups.length > 0) {
          params.append('deselectedToGroup', deselectedToGroups.join(','));
        }
        //console.log('🔍 接收方deselected组:', deselectedToGroups);
      }

      //console.log('🔍 调试信息:');
      //console.log('🔍 selectedFromGroups:', selectedFromGroups);
      //console.log('🔍 selectedToGroups:', selectedToGroups);
      //console.log('🔍 availableGroups:', availableGroups);
      //console.log('🔍 selectedToGroups.includes("other"):', selectedToGroups.includes('other'));
      //console.log('🔍 最终请求参数:', params.toString());
      const response = await fetch(`/api/transactions?${params}`);
      const result = await response.json();
      
      if (result.success) {
        // 根据选择的代币过滤交易
        let filteredTransactions = result.data;

        // 如果选择了具体的代币
        if (selectedTokens.length > 0) {
          filteredTransactions = filteredTransactions.filter(tx => 
            selectedTokens.includes(tx.token_symbol)
          );
        }

        setTransactions(filteredTransactions);
      }
    } catch (error) {
      console.error('Error fetching transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  // 手动刷新数据
  const handleRefresh = () => {
    //console.log('🔄 手动刷新数据');
    fetchTransactions();
  };

  // 当筛选条件改变时重新获取数据
  useEffect(() => { fetchTransactions(); }, [selectedFromGroups, selectedToGroups, selectedTokens, timeRange]);

  // 获取显示文本
  const getDisplayText = (selectedItems, type) => {
    if (selectedItems.length === 0) {
      if (type === 'from') return '所有发送方组';
      if (type === 'to') return '所有接收方组';
      if (type === 'token') return '所有代币';
      return '所有';
    } else if (selectedItems.length === 1) {
      return selectedItems[0] === 'other' ? '其它' : selectedItems[0];
    } else if (type === 'from' && selectedItems.length === availableGroups.length + 1 && selectedItems.includes('other')) {
      return '所有发送方组';
    } else if (type === 'to' && selectedItems.length === availableGroups.length + 1 && selectedItems.includes('other')) {
      return '所有接收方组';
    } else if (type === 'token' && selectedItems.length === availableTokens.length) {
      return '所有代币';
    } else {
      const suffix = type === 'from' ? '个发送方组' : type === 'to' ? '个接收方组' : '个代币';
      const displayItems = selectedItems.map(item => item === 'other' ? '其它' : item);
      return `${displayItems[0]} 等 ${selectedItems.length} ${suffix}`;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <h1 className="text-3xl font-bold text-gray-900">ICTA</h1>
            <button
              onClick={handleRefresh}
              disabled={loading}
              className={`flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                loading 
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                  : 'bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
              }`}
            >
              <svg 
                className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" 
                />
              </svg>
              {loading ? '刷新中...' : '刷新数据'}
            </button>
          </div>
          <p className="text-gray-600">选择特定的钱包组查看交易数据</p>
        </div>
        {/* 筛选器 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
            {/* 发送方组多选下拉 */}
            <div className="relative">
              <label className="block text-sm font-medium text-gray-700 mb-2">发送方组</label>
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setShowFromDropdown(!showFromDropdown)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white text-left focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <span className="block truncate">{getDisplayText(selectedFromGroups, 'from')}</span>
                  <span className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                    <svg className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </span>
                </button>
                
                {showFromDropdown && (
                  <div className="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
                    {/* 全选/取消全选 */}
                    <div className="px-3 py-2 border-b border-gray-200">
                      <div className="flex items-center justify-between">
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={selectedFromGroups.length === availableGroups.length + 1 && selectedFromGroups.includes('other')}
                            onChange={(e) => handleSelectAll('from', e.target.checked)}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                          />
                          <span className="ml-2 text-sm font-medium text-gray-700">
                            {selectedFromGroups.length === availableGroups.length + 1 && selectedFromGroups.includes('other') ? '取消全选' : '全选'}
                          </span>
                        </label>
                        <span className="text-xs text-gray-500">
                          {selectedFromGroups.length}/{availableGroups.length + 1}
                        </span>
                      </div>
                    </div>
                    
                    {/* 选项列表 */}
                    {availableGroups.map((group) => (
                      <label key={group} className="flex items-center px-3 py-2 hover:bg-gray-100 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={selectedFromGroups.includes(group)}
                          onChange={() => handleGroupToggle('from', group)}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">{group}</span>
                      </label>
                    ))}
                    
                    {/* 其它选项 */}
                    <label className="flex items-center px-3 py-2 hover:bg-gray-100 cursor-pointer border-t border-gray-200">
                      <input
                        type="checkbox"
                        checked={selectedFromGroups.includes('other')}
                        onChange={() => handleGroupToggle('from', 'other')}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <span className="ml-2 text-sm text-gray-700 font-medium">其它</span>
                    </label>
                  </div>
                )}
              </div>
            </div>

            {/* 接收方组多选下拉 */}
            <div className="relative">
              <label className="block text-sm font-medium text-gray-700 mb-2">接收方组</label>
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setShowToDropdown(!showToDropdown)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white text-left focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <span className="block truncate">{getDisplayText(selectedToGroups, 'to')}</span>
                  <span className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                    <svg className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </span>
                </button>
                
                {showToDropdown && (
                  <div className="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
                    {/* 全选/取消全选 */}
                    <div className="px-3 py-2 border-b border-gray-200">
                      <div className="flex items-center justify-between">
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={selectedToGroups.length === availableGroups.length + 1 && selectedToGroups.includes('other')}
                            onChange={(e) => handleSelectAll('to', e.target.checked)}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                          />
                          <span className="ml-2 text-sm font-medium text-gray-700">
                            {selectedToGroups.length === availableGroups.length + 1 && selectedToGroups.includes('other') ? '取消全选' : '全选'}
                          </span>
                        </label>
                        <span className="text-xs text-gray-500">
                          {selectedToGroups.length}/{availableGroups.length + 1}
                        </span>
                      </div>
                    </div>
                    
                    {/* 选项列表 */}
                    {availableGroups.map((group) => (
                      <label key={group} className="flex items-center px-3 py-2 hover:bg-gray-100 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={selectedToGroups.includes(group)}
                          onChange={() => handleGroupToggle('to', group)}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">{group}</span>
                      </label>
                    ))}
                    
                    {/* 其它选项 */}
                    <label className="flex items-center px-3 py-2 hover:bg-gray-100 cursor-pointer border-t border-gray-200">
                      <input
                        type="checkbox"
                        checked={selectedToGroups.includes('other')}
                        onChange={() => handleGroupToggle('to', 'other')}
                        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <span className="ml-2 text-sm text-gray-700 font-medium">其它</span>
                    </label>
                  </div>
                )}
              </div>
            </div>

            <div>
              <label htmlFor="token" className="block text-sm font-medium text-gray-700 mb-2">代币</label>
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setShowTokenDropdown(!showTokenDropdown)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-white text-left focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <span className="block truncate">{getDisplayText(selectedTokens, 'token')}</span>
                  <span className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                    <svg className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                    </svg>
                  </span>
                </button>
                
                {showTokenDropdown && (
                  <div className="absolute z-10 mt-1 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
                    {/* 全选/取消全选 */}
                    <div className="px-3 py-2 border-b border-gray-200">
                      <div className="flex items-center justify-between">
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={selectedTokens.length === availableTokens.length}
                            onChange={(e) => handleSelectAll('token', e.target.checked)}
                            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                          />
                          <span className="ml-2 text-sm font-medium text-gray-700">
                            {selectedTokens.length === availableTokens.length ? '取消全选' : '全选'}
                          </span>
                        </label>
                        <span className="text-xs text-gray-500">
                          {selectedTokens.length}/{availableTokens.length}
                        </span>
                      </div>
                    </div>
                    
                    {/* 选项列表 */}
                    {availableTokens.map((token, index) => (
                      <label key={`${token.value}-${index}`} className="flex items-center px-3 py-2 hover:bg-gray-100 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={selectedTokens.includes(token.value)}
                          onChange={() => handleTokenToggle(token.value)}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">{token.label || token.value}</span>
                      </label>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div>
              <label htmlFor="timeAggregation" className="block text-sm font-medium text-gray-700 mb-2">时间聚合</label>
              <select 
                id="timeAggregation" 
                value={timeAggregation} 
                onChange={e => setTimeAggregation(e.target.value)} 
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                {timeAggregationOptions.map(option => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="timeRange" className="block text-sm font-medium text-gray-700 mb-2">时间范围</label>
              <select 
                id="timeRange" 
                value={timeRange} 
                onChange={e => setTimeRange(e.target.value)} 
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="1h">最近1小时</option>
                <option value="6h">最近6小时</option>
                <option value="24h">最近24小时</option>
                <option value="7d">最近7天</option>
                <option value="30d">最近30天</option>
              </select>
            </div>
          </div>
        </div>
        {/* 图表区域 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6" style={{ position: 'relative' }}>
          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="text-lg text-gray-600">加载中...</div>
            </div>
          ) : (
            <div>
              <TransactionsChart 
                data={transactions}
                height={500}
                fromGroup={selectedFromGroups.join(',')}
                toGroup={selectedToGroups.join(',')}
                selectedTokens={selectedTokens}
                timeAggregation={timeAggregation}
                deselectedFromGroups={selectedFromGroups.includes('other') ? availableGroups.filter(g => !selectedFromGroups.includes(g)) : []}
                deselectedToGroups={selectedToGroups.includes('other') ? availableGroups.filter(g => !selectedToGroups.includes(g)) : []}
              />
              {transactions.length === 0 && (
                <div className="text-center text-gray-500 mt-4">
                  {selectedFromGroups.length > 0 || selectedToGroups.length > 0 || selectedTokens.length > 0 ? 
                    `暂无 ${selectedFromGroups.length > 0 ? selectedFromGroups.join(', ') : '所有发送方组'} 到 ${selectedToGroups.length > 0 ? selectedToGroups.join(', ') : '所有接收方组'} 的 ${selectedTokens.length > 0 ? selectedTokens.join(', ') : '所有代币'} 交易数据` : 
                    '暂无交易数据'
                  }
                </div>
              )}
            </div>
          )}
        </div>
        {/* 数据统计 */}
        {transactions.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {selectedFromGroups.length > 0 ? selectedFromGroups.join(', ') : '所有发送方组'} → {selectedToGroups.length > 0 ? selectedToGroups.join(', ') : '所有接收方组'} 交易统计
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{transactions.length}</div>
                <div className="text-sm text-blue-600">总交易数</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  ${transactions.reduce((sum, tx) => sum + (parseFloat(tx.usd_value) || 0), 0).toLocaleString()}
                </div>
                <div className="text-sm text-green-600">总USD价值</div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">{new Set(transactions.map(tx => tx.token_symbol)).size}</div>
                <div className="text-sm text-purple-600">涉及代币数</div>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-orange-600">{new Set(transactions.map(tx => tx.from_address).concat(transactions.map(tx => tx.to_address))).size}</div>
                <div className="text-sm text-orange-600">涉及钱包数</div>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* 点击外部关闭下拉菜单 */}
      {(showFromDropdown || showToDropdown || showTokenDropdown) && (
        <div 
          className="fixed inset-0 z-0" 
          onClick={() => {
            setShowFromDropdown(false);
            setShowToDropdown(false);
            setShowTokenDropdown(false);
          }}
        />
      )}
    </div>
  );
} 