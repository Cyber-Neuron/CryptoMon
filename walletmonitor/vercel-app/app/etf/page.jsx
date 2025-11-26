'use client';

import { useState, useEffect } from 'react';
import ETFChart from '../../components/ETFChart';

export default function ETFAnalysis() {
  const [etfData, setEtfData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedAsset, setSelectedAsset] = useState('ETH');
  const [timeRange, setTimeRange] = useState('1y');

  useEffect(() => {
    fetchETFData();
  }, [selectedAsset, timeRange]);

  const fetchETFData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/etf-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          asset: selectedAsset,
          timeRange: timeRange
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setEtfData(data.data);
      } else {
        setError(data.error || '获取数据失败');
      }
    } catch (err) {
      setError('网络错误，请稍后重试');
      console.error('Error fetching ETF data:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            ETF 流向分析
          </h1>
          <p className="text-gray-600">
            分析加密货币ETF净流入与价格走势的关系，标记关键宏观事件
          </p>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex flex-wrap gap-4 items-center">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                资产选择
              </label>
              <select
                value={selectedAsset}
                onChange={(e) => setSelectedAsset(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="ETH">以太坊 (ETH)</option>
                <option value="BTC">比特币 (BTC)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                时间范围
              </label>
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="6m">6个月</option>
                <option value="1y">1年</option>
                <option value="2y">2年</option>
              </select>
            </div>

            <button
              onClick={fetchETFData}
              disabled={loading}
              className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
            >
              {loading ? '加载中...' : '刷新数据'}
            </button>
          </div>
        </div>

        {/* Chart */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          {loading && (
            <div className="flex items-center justify-center h-96">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          )}

          {error && (
            <div className="flex items-center justify-center h-96">
              <div className="text-center">
                <div className="text-red-600 text-lg mb-2">加载失败</div>
                <div className="text-gray-600 mb-4">{error}</div>
                <button
                  onClick={fetchETFData}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  重试
                </button>
              </div>
            </div>
          )}

          {!loading && !error && etfData && (
            <ETFChart data={etfData} asset={selectedAsset} />
          )}
        </div>

        {/* Legend */}
        {!loading && !error && etfData && (
          <div className="mt-6 bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">图例说明</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-medium text-gray-700 mb-2">图表元素</h4>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li className="flex items-center">
                    <div className="w-4 h-4 bg-blue-500 mr-2"></div>
                    <span>价格K线图</span>
                  </li>
                  <li className="flex items-center">
                    <div className="w-4 h-4 bg-green-500 mr-2"></div>
                    <span>ETF净流入（正值）</span>
                  </li>
                  <li className="flex items-center">
                    <div className="w-4 h-4 bg-red-500 mr-2"></div>
                    <span>ETF净流出（负值）</span>
                  </li>
                  <li className="flex items-center">
                    <div className="w-4 h-4 bg-gray-400 mr-2"></div>
                    <span>成交量柱状图</span>
                  </li>
                  <li className="flex items-center">
                    <div className="w-4 h-0.5 bg-red-400 border-dashed mr-2"></div>
                    <span>宏观事件标记线</span>
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="font-medium text-gray-700 mb-2">宏观事件类型</h4>
                <ul className="space-y-1 text-sm text-gray-600">
                  <li>• FOMC: 美联储议息会议</li>
                  <li>• NonFarm: 非农就业数据</li>
                  <li>• CPI: 消费者物价指数</li>
                  <li>• PPI: 生产者物价指数</li>
                  <li>• GDP: 国内生产总值</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 