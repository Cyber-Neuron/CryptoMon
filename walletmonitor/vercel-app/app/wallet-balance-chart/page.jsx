'use client';

import { useState, useEffect } from 'react';
import WalletBalanceChart from '../../components/WalletBalanceChart';

export default function WalletBalanceChartPage() {
  const [selectedWalletIds, setSelectedWalletIds] = useState([]);
  const [customWalletIds, setCustomWalletIds] = useState('');
  const [showCustomInput, setShowCustomInput] = useState(false);
  const [walletGroups, setWalletGroups] = useState([]);
  const [isLoadingGroups, setIsLoadingGroups] = useState(true);
  const [groupError, setGroupError] = useState(null);
  const [selectedGroup, setSelectedGroup] = useState(null);

  // 获取钱包组数据
  const fetchWalletGroups = async () => {
    setIsLoadingGroups(true);
    setGroupError(null);
    
    try {
      // 获取所有热钱包组
      const allGroupsResponse = await fetch('/api/wallet-groups?grpType=Hot&allGroups=true');
      const allGroupsResult = await allGroupsResponse.json();
      
      if (!allGroupsResult.success) {
        throw new Error(allGroupsResult.error || '获取钱包组失败');
      }

      // 构建钱包组列表
      const groups = allGroupsResult.data.map(group => ({
        name: `${group.grpName.charAt(0).toUpperCase() + group.grpName.slice(1)}`,
        ids: group.walletIds,
        description: `${group.grpName} (${group.walletCount}个钱包)`,
        filters: { grpType: 'Hot', grpName: group.grpName },
        walletCount: group.walletCount
      }));

      // 按钱包数量排序，数量多的排在前面
      groups.sort((a, b) => b.walletCount - a.walletCount);

      setWalletGroups(groups);
      
      // 默认选择第一个组（通常是binance，因为钱包数量最多）
      if (groups.length > 0 && groups[0].ids.length > 0) {
        setSelectedWalletIds(groups[0].ids);
        setSelectedGroup(groups[0]);
      }
      
      console.log('✅ 钱包组数据获取成功:', groups.length, '个组');
      console.log('🔍 各组详情:', groups.map(g => `${g.name}: ${g.walletCount}个钱包`));
    } catch (error) {
      console.error('❌ 获取钱包组失败:', error);
      setGroupError(error.message);
      
      // 如果获取失败，使用默认的硬编码ID作为后备
      const fallbackIds = [1,2,4,143,144,145,141,142,146,147,148,149,151,152,153,154,155,156,137,138,139,140];
      setSelectedWalletIds(fallbackIds);
      setSelectedGroup({
        name: '默认钱包组 (后备)',
        ids: fallbackIds,
        description: `默认钱包组 (${fallbackIds.length}个) - 服务器连接失败时使用`
      });
    } finally {
      setIsLoadingGroups(false);
    }
  };

  // 组件加载时获取钱包组
  useEffect(() => {
    fetchWalletGroups();
  }, []);

  // 处理预设钱包组选择
  const handlePresetSelect = (group) => {
    setSelectedWalletIds(group.ids);
    setSelectedGroup(group);
    setShowCustomInput(false);
  };

  // 处理自定义钱包ID输入
  const handleCustomSubmit = () => {
    const ids = customWalletIds
      .split(',')
      .map(id => parseInt(id.trim()))
      .filter(id => !isNaN(id) && id > 0);
    
    if (ids.length > 0) {
      setSelectedWalletIds(ids);
      setSelectedGroup({
        name: '自定义钱包组',
        ids: ids,
        description: `自定义钱包组 (${ids.length}个)`
      });
      setShowCustomInput(false);
    } else {
      alert('请输入有效的钱包ID，用逗号分隔');
    }
  };

  // 格式化钱包ID显示
  const formatWalletIds = (ids) => {
    if (ids.length <= 5) {
      return ids.join(', ');
    }
    return `${ids.slice(0, 5).join(', ')}... (共${ids.length}个)`;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* 页面标题 */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <h1 className="text-3xl font-bold text-gray-900">钱包余额统计</h1>
            <div className="text-sm text-gray-600">
              当前显示: {selectedWalletIds.length} 个钱包
            </div>
          </div>
          <p className="text-gray-600">查看指定钱包的余额分布和统计信息</p>
        </div>

        {/* 钱包选择器 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">选择钱包</h2>
          
          {isLoadingGroups && (
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                <span className="text-sm text-blue-700">正在从服务器获取钱包组数据...</span>
              </div>
            </div>
          )}
          
          {groupError && (
            <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div className="flex items-center">
                <span className="text-sm text-yellow-700">
                  ⚠️ 服务器连接失败，使用默认钱包组: {groupError}
                </span>
              </div>
            </div>
          )}
          
          {/* 预设钱包组 */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-gray-700 mb-3">
              预设钱包组 ({walletGroups.length} 个组)
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 max-h-96 overflow-y-auto">
              {walletGroups.map((group, index) => (
                <button
                  key={index}
                  onClick={() => handlePresetSelect(group)}
                  className={`p-3 text-left rounded-lg border transition-colors ${
                    selectedGroup && selectedGroup.name === group.name
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="font-medium text-sm">{group.name}</div>
                  <div className="text-xs text-gray-500 mt-1">
                    {group.walletCount} 个钱包
                  </div>
                  {group.filters && (
                    <div className="text-xs text-gray-400 mt-1">
                      {group.filters.grpType}/{group.filters.grpName}
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* 自定义钱包ID */}
          <div className="border-t pt-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-medium text-gray-700">自定义钱包ID</h3>
              <button
                onClick={() => setShowCustomInput(!showCustomInput)}
                className="text-sm text-blue-600 hover:text-blue-700"
              >
                {showCustomInput ? '取消' : '添加自定义'}
              </button>
            </div>
            
            {showCustomInput && (
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    钱包ID (用逗号分隔)
                  </label>
                  <input
                    type="text"
                    value={customWalletIds}
                    onChange={(e) => setCustomWalletIds(e.target.value)}
                    placeholder="例如: 1,2,3,4,5"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div className="flex space-x-3">
                  <button
                    onClick={handleCustomSubmit}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  >
                    应用
                  </button>
                  <button
                    onClick={() => setShowCustomInput(false)}
                    className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                  >
                    取消
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* 当前选择的钱包ID */}
          <div className="mt-4 p-3 bg-gray-50 rounded-lg">
            <div className="text-sm font-medium text-gray-700 mb-1">
              当前选择: {selectedGroup ? selectedGroup.name : '未选择'}
            </div>
            <div className="text-sm text-gray-600 font-mono">
              {formatWalletIds(selectedWalletIds)}
            </div>
            {selectedGroup && selectedGroup.filters && (
              <div className="text-xs text-gray-500 mt-1">
                筛选条件: {selectedGroup.filters.grpType} / {selectedGroup.filters.grpName}
              </div>
            )}
          </div>
        </div>

        {/* 钱包余额图表 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">钱包余额分布</h2>
          {selectedWalletIds.length > 0 ? (
            <WalletBalanceChart walletIds={selectedWalletIds} />
          ) : (
            <div className="text-center py-8 text-gray-500">
              请先选择钱包组
            </div>
          )}
        </div>

        {/* 说明信息 */}
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="text-sm font-medium text-blue-800 mb-2">使用说明</h3>
          <ul className="text-sm text-blue-700 space-y-1">
            <li>• 钱包组数据从服务器动态获取，基于 wallets 表的 grp_type 和 grp_name 字段</li>
            <li>• 余额数据基于交易记录中的 from_balance 字段</li>
            <li>• 鼠标悬停在柱状图上可查看详细的钱包信息</li>
            <li>• 支持选择预设钱包组或输入自定义钱包ID</li>
            <li>• 当前显示所有 grp_type='Hot' 的钱包，按 grp_name 分组</li>
            <li>• 钱包组按钱包数量排序，数量多的排在前面</li>
          </ul>
        </div>
      </div>
    </div>
  );
} 