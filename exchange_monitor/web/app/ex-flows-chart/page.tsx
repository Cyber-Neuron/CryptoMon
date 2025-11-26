'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';
import { formatInTimeZone } from 'date-fns-tz';
import Link from 'next/link';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  PointElement
);

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface ExFlow {
  id: number;
  timestamp: number;
  token_id: number;
  chain_id: number;
  from_grp_name: string;
  to_grp_name: string;
  amount: number;
  usd_value: number;
  tx_hash: string;
}

// Token mapping
const TOKEN_NAMES: { [key: number]: string } = {
  143749: 'Ethereum',
  143773: 'USD Coin',
  37: 'Tether',
};

const TOKEN_COLORS = {
  'Ethereum': '#627EEA',
  'USD Coin': '#2775CA',
  'Tether': '#26A17B',
};

interface ChartDataPoint {
  timestamp: number;
  timeString: string;
  eth_amount: number;
  usdc_amount: number;
  usdt_amount: number;
  eth_usd: number;
  usdc_usd: number;
  usdt_usd: number;
  total_amount: number;
  total_usd: number;
  flow_count: number;
}

export default function ExFlowsChartPage() {
  const [loading, setLoading] = useState(true);
  const [flows, setFlows] = useState<ExFlow[]>([]);
  const [chartData, setChartData] = useState<ChartDataPoint[]>([]);
  const [fromTime, setFromTime] = useState('');
  const [toTime, setToTime] = useState('');
  const [fromGrp, setFromGrp] = useState('');
  const [toGrp, setToGrp] = useState('');
  const [tokenId, setTokenId] = useState('');
  const [groupFilter, setGroupFilter] = useState('');
  const [filteredFlows, setFilteredFlows] = useState<ExFlow[]>([]);

  useEffect(() => {
    fetchFlows();
  }, []);

  useEffect(() => {
    if (flows.length > 0) {
      applyTimeFilter();
    }
  }, [fromTime, toTime, fromGrp, toGrp, tokenId, groupFilter, flows]);

  const fetchFlows = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from('ex_flows')
        .select('*')
        .order('timestamp', { ascending: false })
        .limit(5000); // 限制数据量

      if (error) {
        console.error('Error fetching ex_flows:', error);
        return;
      }

      console.log('Fetched ex_flows data:', data);
      console.log('Number of flows:', data?.length || 0);
      
      setFlows(data || []);
    } catch (error) {
      console.error('Error fetching ex_flows:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyTimeFilter = () => {
    let filtered = [...flows];
    console.log('Initial flows count:', filtered.length);

    if (fromTime) {
      const fromTimestamp = Math.floor(new Date(fromTime).getTime() / 1000);
      filtered = filtered.filter(flow => flow.timestamp >= fromTimestamp);
      console.log('After fromTime filter:', filtered.length);
    }

    if (toTime) {
      const toTimestamp = Math.floor(new Date(toTime).getTime() / 1000);
      filtered = filtered.filter(flow => flow.timestamp <= toTimestamp);
      console.log('After toTime filter:', filtered.length);
    }

    if (fromGrp) {
      filtered = filtered.filter(flow => (flow.from_grp_name || '').toLowerCase().includes(fromGrp.toLowerCase()));
      console.log('After fromGrp filter:', filtered.length);
    }
    if (toGrp) {
      filtered = filtered.filter(flow => (flow.to_grp_name || '').toLowerCase().includes(toGrp.toLowerCase()));
      console.log('After toGrp filter:', filtered.length);
    }
    if (tokenId) {
      filtered = filtered.filter(flow => flow.token_id.toString() === tokenId);
      console.log('After tokenId filter:', filtered.length);
    }

    console.log('Final filtered flows count:', filtered.length);
    setFilteredFlows(filtered);
    processDataForChart(filtered);
  };

  const processDataForChart = (flowsData: ExFlow[]) => {
    console.log('Processing data for chart, input flows:', flowsData.length);
    
    // 调试：显示前几条数据
    console.log('Sample flows data:', flowsData.slice(0, 3));
    
    // 按时间戳分组数据（按小时分组）
    const timeGroups: { [key: number]: ExFlow[] } = {};
    
    flowsData.forEach(flow => {
      // 将时间戳按小时分组
      const hourTimestamp = Math.floor(flow.timestamp / 3600) * 3600;
      if (!timeGroups[hourTimestamp]) {
        timeGroups[hourTimestamp] = [];
      }
      timeGroups[hourTimestamp].push(flow);
    });

    console.log('Time groups created:', Object.keys(timeGroups).length);

    // 创建图表数据点
    const chartDataPoints: ChartDataPoint[] = Object.entries(timeGroups).map(([timestamp, flows]) => {
      const time = parseInt(timestamp);
      const timeString = formatInTimeZone(time * 1000, 'America/New_York', 'MM-dd HH:mm');
      
      // 初始化数据
      let eth_amount = 0, eth_usd = 0;
      let usdc_amount = 0, usdc_usd = 0;
      let usdt_amount = 0, usdt_usd = 0;
      let other_amount = 0, other_usd = 0;

      // 处理每个token的数据
      flows.forEach(flow => {
        const amount = Number(flow.amount) || 0;
        const usd_value = Number(flow.usd_value) || 0;
        
        if (flow.token_id === 143749) { // Ethereum
          eth_amount += amount;
          eth_usd += usd_value;
        } else if (flow.token_id === 143773) { // USDC
          usdc_amount += amount;
          usdc_usd += usd_value;
        } else if (flow.token_id === 37) { // USDT
          usdt_amount += amount;
          usdt_usd += usd_value;
        } else {
          // 处理其他token_id
          other_amount += amount;
          other_usd += usd_value;
        }
      });

      const total_amount = eth_amount + usdc_amount + usdt_amount + other_amount;
      const total_usd = eth_usd + usdc_usd + usdt_usd + other_usd;

      return {
        timestamp: time,
        timeString,
        eth_amount: Math.round(eth_amount * 1000000) / 1000000, // 保留6位小数
        usdc_amount: Math.round(usdc_amount * 1000000) / 1000000,
        usdt_amount: Math.round(usdt_amount * 1000000) / 1000000,
        eth_usd: Math.round(eth_usd * 100) / 100,
        usdc_usd: Math.round(usdc_usd * 100) / 100,
        usdt_usd: Math.round(usdt_usd * 100) / 100,
        total_amount: Math.round(total_amount * 1000000) / 1000000,
        total_usd: Math.round(total_usd * 100) / 100,
        flow_count: flows.length,
      };
    });

    // 按时间排序
    chartDataPoints.sort((a, b) => a.timestamp - b.timestamp);
    
    console.log('Chart data points created:', chartDataPoints.length);
    console.log('Sample chart data:', chartDataPoints.slice(0, 3));
    console.log('Total USD across all points:', chartDataPoints.reduce((sum, d) => sum + d.total_usd, 0));
    
    setChartData(chartDataPoints);
  };

  // 处理进出资金数据
  const processInOutFlowData = () => {
    if (!groupFilter) return [];

    const timeGroups: { [key: number]: { 
      eth_inflow: number, eth_outflow: number,
      usdc_inflow: number, usdc_outflow: number,
      usdt_inflow: number, usdt_outflow: number
    } } = {};
    
    // 调试：显示token_id分布
    const tokenCounts: { [key: number]: number } = {};
    const groupMatches: { inflow: number, outflow: number } = { inflow: 0, outflow: 0 };
    const tokenMatches: { [key: number]: { inflow: number, outflow: number } } = {};
    
    // 先过滤出包含目标分组的所有数据
    const groupFilteredFlows = filteredFlows.filter(flow => 
      (flow.from_grp_name && flow.from_grp_name.toLowerCase().includes(groupFilter.toLowerCase())) ||
      (flow.to_grp_name && flow.to_grp_name.toLowerCase().includes(groupFilter.toLowerCase()))
    );
    
    console.log('Flows containing group filter:', groupFilteredFlows.length);
    
    groupFilteredFlows.forEach(flow => {
      // 统计token_id
      tokenCounts[flow.token_id] = (tokenCounts[flow.token_id] || 0) + 1;
      
      // 初始化token匹配统计
      if (!tokenMatches[flow.token_id]) {
        tokenMatches[flow.token_id] = { inflow: 0, outflow: 0 };
      }
      
      const hourTimestamp = Math.floor(flow.timestamp / 3600) * 3600;
      if (!timeGroups[hourTimestamp]) {
        timeGroups[hourTimestamp] = { 
          eth_inflow: 0, eth_outflow: 0,
          usdc_inflow: 0, usdc_outflow: 0,
          usdt_inflow: 0, usdt_outflow: 0
        };
      }
      
      const usd_value = Number(flow.usd_value) || 0;
      
      // 检查是否是流向目标分组（流入）
      if (flow.to_grp_name && flow.to_grp_name.toLowerCase().includes(groupFilter.toLowerCase())) {
        groupMatches.inflow++;
        tokenMatches[flow.token_id].inflow++;
        if (flow.token_id === 143749) { // ETH
          timeGroups[hourTimestamp].eth_inflow += usd_value;
        } else if (flow.token_id === 143773) { // USDC
          timeGroups[hourTimestamp].usdc_inflow += usd_value;
        } else if (flow.token_id === 37) { // USDT
          timeGroups[hourTimestamp].usdt_inflow += usd_value;
        }
      }
      
      // 检查是否来自目标分组（流出）
      if (flow.from_grp_name && flow.from_grp_name.toLowerCase().includes(groupFilter.toLowerCase())) {
        groupMatches.outflow++;
        tokenMatches[flow.token_id].outflow++;
        if (flow.token_id === 143749) { // ETH
          timeGroups[hourTimestamp].eth_outflow += usd_value;
        } else if (flow.token_id === 143773) { // USDC
          timeGroups[hourTimestamp].usdc_outflow += usd_value;
        } else if (flow.token_id === 37) { // USDT
          timeGroups[hourTimestamp].usdt_outflow += usd_value;
        }
      }
    });

    console.log('Token ID distribution:', tokenCounts);
    console.log('Group matches:', groupMatches);
    console.log('Token matches:', tokenMatches);
    console.log('Looking for token_ids:', [143749, 143773, 37]);

    const result = Object.entries(timeGroups)
      .map(([timestamp, data]) => ({
        time: formatInTimeZone(parseInt(timestamp) * 1000, 'America/New_York', 'MM-dd HH:mm'),
        eth_inflow: Math.round(data.eth_inflow * 100) / 100,
        eth_outflow: Math.round(data.eth_outflow * 100) / 100,
        usdc_inflow: Math.round(data.usdc_inflow * 100) / 100,
        usdc_outflow: Math.round(data.usdc_outflow * 100) / 100,
        usdt_inflow: Math.round(data.usdt_inflow * 100) / 100,
        usdt_outflow: Math.round(data.usdt_outflow * 100) / 100,
      }))
      .sort((a, b) => new Date(a.time).getTime() - new Date(b.time).getTime());

    console.log('In/Out flow data sample:', result.slice(0, 3));
    return result;
  };

  const inOutFlowData = processInOutFlowData();

  // Chart.js 配置
  const amountChartData = {
    labels: chartData.map(d => d.timeString),
    datasets: [
      {
        label: 'ETH Amount',
        data: chartData.map(d => d.eth_amount),
        backgroundColor: TOKEN_COLORS['Ethereum'],
        borderColor: TOKEN_COLORS['Ethereum'],
        borderWidth: 1,
        stack: 'amount',
      },
      {
        label: 'USDC Amount',
        data: chartData.map(d => d.usdc_amount),
        backgroundColor: TOKEN_COLORS['USD Coin'],
        borderColor: TOKEN_COLORS['USD Coin'],
        borderWidth: 1,
        stack: 'amount',
      },
      {
        label: 'USDT Amount',
        data: chartData.map(d => d.usdt_amount),
        backgroundColor: TOKEN_COLORS['Tether'],
        borderColor: TOKEN_COLORS['Tether'],
        borderWidth: 1,
        stack: 'amount',
      },
    ],
  };

  const usdChartData = {
    labels: chartData.map(d => d.timeString),
    datasets: [
      {
        label: 'ETH USD Value',
        data: chartData.map(d => d.eth_usd),
        backgroundColor: TOKEN_COLORS['Ethereum'],
        borderColor: TOKEN_COLORS['Ethereum'],
        borderWidth: 1,
        stack: 'usd',
      },
      {
        label: 'USDC USD Value',
        data: chartData.map(d => d.usdc_usd),
        backgroundColor: TOKEN_COLORS['USD Coin'],
        borderColor: TOKEN_COLORS['USD Coin'],
        borderWidth: 1,
        stack: 'usd',
      },
      {
        label: 'USDT USD Value',
        data: chartData.map(d => d.usdt_usd),
        backgroundColor: TOKEN_COLORS['Tether'],
        borderColor: TOKEN_COLORS['Tether'],
        borderWidth: 1,
        stack: 'usd',
      },
    ],
  };

  const usdValueChartData = {
    labels: chartData.map(d => d.timeString),
    datasets: [
      {
        label: 'USD Value',
        data: chartData.map(d => d.total_usd),
        borderColor: '#FF6B6B',
        backgroundColor: 'rgba(255, 107, 107, 0.1)',
        tension: 0.1,
        fill: true,
        borderWidth: 2,
      },
    ],
  };

  const flowCountChartData = {
    labels: chartData.map(d => d.timeString),
    datasets: [
      {
        label: 'Flow Count',
        data: chartData.map(d => d.flow_count),
        borderColor: '#FF6B6B',
        backgroundColor: 'rgba(255, 107, 107, 0.1)',
        tension: 0.1,
        fill: true,
        borderWidth: 2,
      },
    ],
  };

  const inOutFlowChartData = {
    labels: inOutFlowData.map(d => d.time),
    datasets: [
      {
        label: 'ETH Inflow',
        data: inOutFlowData.map(d => d.eth_inflow),
        backgroundColor: TOKEN_COLORS['Ethereum'],
        borderColor: TOKEN_COLORS['Ethereum'],
        borderWidth: 1,
        stack: 'inflow',
      },
      {
        label: 'USDC Inflow',
        data: inOutFlowData.map(d => d.usdc_inflow),
        backgroundColor: TOKEN_COLORS['USD Coin'],
        borderColor: TOKEN_COLORS['USD Coin'],
        borderWidth: 1,
        stack: 'inflow',
      },
      {
        label: 'USDT Inflow',
        data: inOutFlowData.map(d => d.usdt_inflow),
        backgroundColor: TOKEN_COLORS['Tether'],
        borderColor: TOKEN_COLORS['Tether'],
        borderWidth: 1,
        stack: 'inflow',
      },
      {
        label: 'ETH Outflow',
        data: inOutFlowData.map(d => -d.eth_outflow), // 负值显示在负半轴
        backgroundColor: '#FF6B6B',
        borderColor: '#FF6B6B',
        borderWidth: 1,
        stack: 'outflow',
      },
      {
        label: 'USDC Outflow',
        data: inOutFlowData.map(d => -d.usdc_outflow), // 负值显示在负半轴
        backgroundColor: '#FF8E8E',
        borderColor: '#FF8E8E',
        borderWidth: 1,
        stack: 'outflow',
      },
      {
        label: 'USDT Outflow',
        data: inOutFlowData.map(d => -d.usdt_outflow), // 负值显示在负半轴
        backgroundColor: '#FFB1B1',
        borderColor: '#FFB1B1',
        borderWidth: 1,
        stack: 'outflow',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Exchange Flows Data',
      },
    },
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
        beginAtZero: true,
      },
    },
  };

  const lineOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Flow Count Over Time',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Exchange Flows Chart</h1>
          <div className="flex gap-4">
            <Link 
              href="/flows-chart-chartjs" 
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            >
              Token Flows Chart
            </Link>
            <Link 
              href="/flows" 
              className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
            >
              View Table
            </Link>
            <Link 
              href="/" 
              className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
            >
              Dashboard
            </Link>
          </div>
        </div>

        {/* Time Filter Controls */}
        <div className="bg-white border rounded-lg p-4 mb-6">
          <h2 className="text-lg font-semibold mb-4">Filter</h2>
          <div className="flex gap-4 flex-wrap items-end">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                From Time
              </label>
              <input
                type="datetime-local"
                value={fromTime}
                onChange={(e) => setFromTime(e.target.value)}
                className="p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                To Time
              </label>
              <input
                type="datetime-local"
                value={toTime}
                onChange={(e) => setToTime(e.target.value)}
                className="p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                From Group Name
              </label>
              <input
                type="text"
                value={fromGrp}
                onChange={(e) => setFromGrp(e.target.value)}
                placeholder="from_grp_name"
                className="p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                To Group Name
              </label>
              <input
                type="text"
                value={toGrp}
                onChange={(e) => setToGrp(e.target.value)}
                placeholder="to_grp_name"
                className="p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Token ID
              </label>
              <input
                type="text"
                value={tokenId}
                onChange={(e) => setTokenId(e.target.value)}
                placeholder="token_id"
                className="p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Group Filter
              </label>
              <input
                type="text"
                value={groupFilter}
                onChange={(e) => setGroupFilter(e.target.value)}
                placeholder="group_filter"
                className="p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <button
              onClick={() => {
                setFromTime('');
                setToTime('');
                setFromGrp('');
                setToGrp('');
                setTokenId('');
                setGroupFilter('');
              }}
              className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
            >
              Clear Filter
            </button>
          </div>
          <div className="mt-2 text-sm text-gray-600">
            Showing {filteredFlows.length} flows out of {flows.length} total flows
            {(fromTime || toTime || fromGrp || toGrp || tokenId || groupFilter) && (
              <span> (filtered</span>
            )}
            {fromTime && <span> from {new Date(fromTime).toLocaleString()}</span>}
            {toTime && <span> to {new Date(toTime).toLocaleString()}</span>}
            {fromGrp && <span> from_grp_name: "{fromGrp}"</span>}
            {toGrp && <span> to_grp_name: "{toGrp}"</span>}
            {tokenId && <span> token_id: {tokenId}</span>}
            {groupFilter && <span> group_filter: "{groupFilter}"</span>}
            {(fromTime || toTime || fromGrp || toGrp || tokenId || groupFilter) && <span>)</span>}
          </div>
        </div>

        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            <p className="mt-2">Loading chart data...</p>
          </div>
        ) : (
          <div className="bg-white border rounded-lg p-4">
            <div className="mb-4">
              <h2 className="text-lg font-semibold mb-2">Chart Legend</h2>
              <div className="flex flex-wrap gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4" style={{backgroundColor: TOKEN_COLORS['Ethereum']}}></div>
                  <span>Ethereum</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4" style={{backgroundColor: TOKEN_COLORS['USD Coin']}}></div>
                  <span>USD Coin (USDC)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4" style={{backgroundColor: TOKEN_COLORS['Tether']}}></div>
                  <span>Tether (USDT)</span>
                </div>
              </div>
              <div className="mt-2 text-xs text-gray-600">
                Debug: {flows.length} total flows, {filteredFlows.length} filtered flows, {chartData.length} chart points
                {filteredFlows.length > 0 && (
                  <div className="mt-1">
                    Sample data: {filteredFlows[0]?.token_id}, amount: {filteredFlows[0]?.amount}, usd_value: {filteredFlows[0]?.usd_value}
                  </div>
                )}
                {chartData.length > 0 && (
                  <div className="mt-1">
                    Chart total USD: {chartData.reduce((sum, d) => sum + d.total_usd, 0).toFixed(2)}
                  </div>
                )}
              </div>
            </div>
            
            <div className="space-y-8">
              {/* Amount Chart */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Token Amounts Over Time</h3>
                <div className="h-[400px] border-2 border-gray-200">
                  <Bar data={amountChartData} options={chartOptions} />
                </div>
              </div>

              {/* USD Value Chart */}
              <div>
                <h3 className="text-lg font-semibold mb-2">USD Values Over Time</h3>
                <div className="h-[400px] border-2 border-gray-200">
                  <Bar data={usdChartData} options={chartOptions} />
                </div>
              </div>

              {/* USD Value Line Chart */}
              <div>
                <h3 className="text-lg font-semibold mb-2">USD Value Trend</h3>
                <div className="h-[400px] border-2 border-gray-200">
                  <Line data={usdValueChartData} options={lineOptions} />
                </div>
              </div>

              {/* Flow Count Chart */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Flow Count Over Time</h3>
                <div className="h-[400px] border-2 border-gray-200">
                  <Line data={flowCountChartData} options={lineOptions} />
                </div>
              </div>

              {/* In/Out Flow Chart */}
              {groupFilter && (
                <div>
                  <h3 className="text-lg font-semibold mb-2">In/Out Flow for "{groupFilter}"</h3>
                  <div className="mb-2 text-sm text-gray-600">
                    Positive values: Money flowing TO {groupFilter} | Negative values: Money flowing FROM {groupFilter}
                  </div>
                  <div className="h-[400px] border-2 border-gray-200">
                    <Bar data={inOutFlowChartData} options={chartOptions} />
                  </div>
                </div>
              )}

              {/* Data Summary Table */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Data Summary</h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full bg-white border border-gray-300">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="px-4 py-2 border-b text-left">Token</th>
                        <th className="px-4 py-2 border-b text-right">Total Amount</th>
                        <th className="px-4 py-2 border-b text-right">Total USD Value</th>
                        <th className="px-4 py-2 border-b text-right">Flow Count</th>
                        <th className="px-4 py-2 border-b text-right">Avg USD per Flow</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr className="hover:bg-gray-50">
                        <td className="px-4 py-2 border-b font-medium">Ethereum</td>
                        <td className="px-4 py-2 border-b text-right">
                          {chartData.reduce((sum, d) => sum + d.eth_amount, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right text-green-600">
                          ${chartData.reduce((sum, d) => sum + d.eth_usd, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right">
                          {filteredFlows.filter(f => f.token_id === 143749).length}
                        </td>
                        <td className="px-4 py-2 border-b text-right">
                          ${(chartData.reduce((sum, d) => sum + d.eth_usd, 0) / 
                             Math.max(filteredFlows.filter(f => f.token_id === 143749).length, 1)).toFixed(2)}
                        </td>
                      </tr>
                      <tr className="hover:bg-gray-50">
                        <td className="px-4 py-2 border-b font-medium">USDC</td>
                        <td className="px-4 py-2 border-b text-right">
                          {chartData.reduce((sum, d) => sum + d.usdc_amount, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right text-green-600">
                          ${chartData.reduce((sum, d) => sum + d.usdc_usd, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right">
                          {filteredFlows.filter(f => f.token_id === 143773).length}
                        </td>
                        <td className="px-4 py-2 border-b text-right">
                          ${(chartData.reduce((sum, d) => sum + d.usdc_usd, 0) / 
                             Math.max(filteredFlows.filter(f => f.token_id === 143773).length, 1)).toFixed(2)}
                        </td>
                      </tr>
                      <tr className="hover:bg-gray-50">
                        <td className="px-4 py-2 border-b font-medium">USDT</td>
                        <td className="px-4 py-2 border-b text-right">
                          {chartData.reduce((sum, d) => sum + d.usdt_amount, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right text-green-600">
                          ${chartData.reduce((sum, d) => sum + d.usdt_usd, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right">
                          {filteredFlows.filter(f => f.token_id === 37).length}
                        </td>
                        <td className="px-4 py-2 border-b text-right">
                          ${(chartData.reduce((sum, d) => sum + d.usdt_usd, 0) / 
                             Math.max(filteredFlows.filter(f => f.token_id === 37).length, 1)).toFixed(2)}
                        </td>
                      </tr>
                      <tr className="hover:bg-gray-50 bg-gray-100">
                        <td className="px-4 py-2 border-b font-bold">Total</td>
                        <td className="px-4 py-2 border-b text-right font-bold">
                          {chartData.reduce((sum, d) => sum + d.total_amount, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right text-green-600 font-bold">
                          ${chartData.reduce((sum, d) => sum + d.total_usd, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right font-bold">
                          {filteredFlows.length}
                        </td>
                        <td className="px-4 py-2 border-b text-right font-bold">
                          ${(chartData.reduce((sum, d) => sum + d.total_usd, 0) / 
                             Math.max(filteredFlows.length, 1)).toFixed(2)}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* In/Out Flow Summary */}
              {groupFilter && (
                <div>
                  <h3 className="text-lg font-semibold mb-2">In/Out Flow Summary for "{groupFilter}"</h3>
                  <div className="overflow-x-auto">
                    <table className="min-w-full bg-white border border-gray-300">
                      <thead>
                        <tr className="bg-gray-50">
                          <th className="px-4 py-2 border-b text-left">Token</th>
                          <th className="px-4 py-2 border-b text-right">Inflow (TO {groupFilter})</th>
                          <th className="px-4 py-2 border-b text-right">Outflow (FROM {groupFilter})</th>
                          <th className="px-4 py-2 border-b text-right">Net Flow</th>
                          <th className="px-4 py-2 border-b text-right">Total Flows</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr className="hover:bg-gray-50">
                          <td className="px-4 py-2 border-b font-medium">Ethereum</td>
                          <td className="px-4 py-2 border-b text-right text-green-600">
                            ${inOutFlowData.reduce((sum, d) => sum + d.eth_inflow, 0).toLocaleString()}
                          </td>
                          <td className="px-4 py-2 border-b text-right text-red-600">
                            ${inOutFlowData.reduce((sum, d) => sum + d.eth_outflow, 0).toLocaleString()}
                          </td>
                          <td className={`px-4 py-2 border-b text-right font-semibold ${
                            inOutFlowData.reduce((sum, d) => sum + d.eth_inflow - d.eth_outflow, 0) >= 0 ? 'text-green-600' : 'text-red-600'
                          }`}>
                            ${inOutFlowData.reduce((sum, d) => sum + d.eth_inflow - d.eth_outflow, 0).toLocaleString()}
                          </td>
                          <td className="px-4 py-2 border-b text-right">
                            {filteredFlows.filter(f => 
                              f.token_id === 143749 && (
                                (f.to_grp_name && f.to_grp_name.toLowerCase().includes(groupFilter.toLowerCase())) ||
                                (f.from_grp_name && f.from_grp_name.toLowerCase().includes(groupFilter.toLowerCase()))
                              )
                            ).length}
                          </td>
                        </tr>
                        <tr className="hover:bg-gray-50">
                          <td className="px-4 py-2 border-b font-medium">USDC</td>
                          <td className="px-4 py-2 border-b text-right text-green-600">
                            ${inOutFlowData.reduce((sum, d) => sum + d.usdc_inflow, 0).toLocaleString()}
                          </td>
                          <td className="px-4 py-2 border-b text-right text-red-600">
                            ${inOutFlowData.reduce((sum, d) => sum + d.usdc_outflow, 0).toLocaleString()}
                          </td>
                          <td className={`px-4 py-2 border-b text-right font-semibold ${
                            inOutFlowData.reduce((sum, d) => sum + d.usdc_inflow - d.usdc_outflow, 0) >= 0 ? 'text-green-600' : 'text-red-600'
                          }`}>
                            ${inOutFlowData.reduce((sum, d) => sum + d.usdc_inflow - d.usdc_outflow, 0).toLocaleString()}
                          </td>
                          <td className="px-4 py-2 border-b text-right">
                            {filteredFlows.filter(f => 
                              f.token_id === 143773 && (
                                (f.to_grp_name && f.to_grp_name.toLowerCase().includes(groupFilter.toLowerCase())) ||
                                (f.from_grp_name && f.from_grp_name.toLowerCase().includes(groupFilter.toLowerCase()))
                              )
                            ).length}
                          </td>
                        </tr>
                        <tr className="hover:bg-gray-50">
                          <td className="px-4 py-2 border-b font-medium">USDT</td>
                          <td className="px-4 py-2 border-b text-right text-green-600">
                            ${inOutFlowData.reduce((sum, d) => sum + d.usdt_inflow, 0).toLocaleString()}
                          </td>
                          <td className="px-4 py-2 border-b text-right text-red-600">
                            ${inOutFlowData.reduce((sum, d) => sum + d.usdt_outflow, 0).toLocaleString()}
                          </td>
                          <td className={`px-4 py-2 border-b text-right font-semibold ${
                            inOutFlowData.reduce((sum, d) => sum + d.usdt_inflow - d.usdt_outflow, 0) >= 0 ? 'text-green-600' : 'text-red-600'
                          }`}>
                            ${inOutFlowData.reduce((sum, d) => sum + d.usdt_inflow - d.usdt_outflow, 0).toLocaleString()}
                          </td>
                          <td className="px-4 py-2 border-b text-right">
                            {filteredFlows.filter(f => 
                              f.token_id === 37 && (
                                (f.to_grp_name && f.to_grp_name.toLowerCase().includes(groupFilter.toLowerCase())) ||
                                (f.from_grp_name && f.from_grp_name.toLowerCase().includes(groupFilter.toLowerCase()))
                              )
                            ).length}
                          </td>
                        </tr>
                        <tr className="hover:bg-gray-50 bg-gray-100">
                          <td className="px-4 py-2 border-b font-bold">Total</td>
                          <td className="px-4 py-2 border-b text-right text-green-600 font-bold">
                            ${inOutFlowData.reduce((sum, d) => sum + d.eth_inflow + d.usdc_inflow + d.usdt_inflow, 0).toLocaleString()}
                          </td>
                          <td className="px-4 py-2 border-b text-right text-red-600 font-bold">
                            ${inOutFlowData.reduce((sum, d) => sum + d.eth_outflow + d.usdc_outflow + d.usdt_outflow, 0).toLocaleString()}
                          </td>
                          <td className={`px-4 py-2 border-b text-right font-bold ${
                            inOutFlowData.reduce((sum, d) => sum + d.eth_inflow + d.usdc_inflow + d.usdt_inflow - d.eth_outflow - d.usdc_outflow - d.usdt_outflow, 0) >= 0 ? 'text-green-600' : 'text-red-600'
                          }`}>
                            ${inOutFlowData.reduce((sum, d) => sum + d.eth_inflow + d.usdc_inflow + d.usdt_inflow - d.eth_outflow - d.usdc_outflow - d.usdt_outflow, 0).toLocaleString()}
                          </td>
                          <td className="px-4 py-2 border-b text-right font-bold">
                            {filteredFlows.filter(f => 
                              (f.to_grp_name && f.to_grp_name.toLowerCase().includes(groupFilter.toLowerCase())) ||
                              (f.from_grp_name && f.from_grp_name.toLowerCase().includes(groupFilter.toLowerCase()))
                            ).length}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Recent Flows Table */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Recent Flows (Top 20)</h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full bg-white border border-gray-300">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="px-4 py-2 border-b text-left">Time</th>
                        <th className="px-4 py-2 border-b text-left">Token</th>
                        <th className="px-4 py-2 border-b text-left">From Group</th>
                        <th className="px-4 py-2 border-b text-left">To Group</th>
                        <th className="px-4 py-2 border-b text-right">Amount</th>
                        <th className="px-4 py-2 border-b text-right">USD Value</th>
                        <th className="px-4 py-2 border-b text-left">Chain ID</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredFlows.slice(0, 20).map((flow) => (
                        <tr key={flow.id} className="hover:bg-gray-50">
                          <td className="px-4 py-2 border-b text-sm">
                            {formatInTimeZone(flow.timestamp * 1000, 'America/New_York', 'MM-dd HH:mm:ss')}
                          </td>
                          <td className="px-4 py-2 border-b">
                            {TOKEN_NAMES[flow.token_id] || `Token ${flow.token_id}`}
                          </td>
                          <td className="px-4 py-2 border-b text-sm">
                            {flow.from_grp_name || 'Unknown'}
                          </td>
                          <td className="px-4 py-2 border-b text-sm">
                            {flow.to_grp_name || 'Unknown'}
                          </td>
                          <td className="px-4 py-2 border-b text-right">
                            {flow.amount?.toLocaleString() || '0'}
                          </td>
                          <td className="px-4 py-2 border-b text-right text-green-600">
                            ${flow.usd_value?.toLocaleString() || '0'}
                          </td>
                          <td className="px-4 py-2 border-b text-sm">
                            {flow.chain_id}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
} 