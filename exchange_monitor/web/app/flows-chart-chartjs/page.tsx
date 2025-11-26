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

interface TokenFlow {
  id: number;
  token_id: number;
  chain_id: number;
  timestamp: number;
  inflow: number;
  outflow: number;
  inflow_count: number;
  outflow_count: number;
  net_flow: number;
  created_at: number;
  inflow_usd: number;
  outflow_usd: number;
  net_flow_usd: number;
}

// Token mapping
const TOKEN_NAMES: { [key: number]: string } = {
  141670: 'Ethereum',
  141678: 'USD Coin',
  141685: 'Tether',
};

const TOKEN_COLORS = {
  'Ethereum': '#627EEA',
  'USD Coin': '#2775CA',
  'Tether': '#26A17B',
};

interface ChartDataPoint {
  timestamp: number;
  timeString: string;
  eth_inflow: number;
  eth_outflow: number;
  usdc_inflow: number;
  usdc_outflow: number;
  usdt_inflow: number;
  usdt_outflow: number;
  usdc_net: number;
  usdt_net: number;
  total_inflow: number;
  total_outflow: number;
  total_net: number;
}

export default function FlowsChartChartJSPage() {
  const [loading, setLoading] = useState(true);
  const [timeframe, setTimeframe] = useState('1D');
  const [flows, setFlows] = useState<TokenFlow[]>([]);
  const [chartData, setChartData] = useState<ChartDataPoint[]>([]);

  useEffect(() => {
    fetchFlows();
  }, [timeframe]);

  const fetchFlows = async () => {
    setLoading(true);
    try {
      let hours = 24;
      if (timeframe === '4H') hours = 4;
      if (timeframe === '1H') hours = 1;

      const cutoffTime = Math.floor(Date.now() / 1000) - (hours * 3600);
      
      console.log('Fetching flows with cutoff time (UTC):', new Date(cutoffTime * 1000).toISOString());

      const { data, error } = await supabase
        .from('token_flows')
        .select('*')
        .gte('timestamp', cutoffTime)
        .order('timestamp', { ascending: false });

      if (error) {
        console.error('Error fetching flows:', error);
        return;
      }

      console.log('Fetched flows data:', data);
      console.log('Number of flows:', data?.length || 0);
      
      setFlows(data || []);
      processDataForChart(data || []);
    } catch (error) {
      console.error('Error fetching flows:', error);
    } finally {
      setLoading(false);
    }
  };

  const processDataForChart = (flowsData: TokenFlow[]) => {
    console.log('Processing data for chart, input flows:', flowsData.length);
    
    // 按时间戳分组数据
    const timeGroups: { [key: number]: TokenFlow[] } = {};
    
    flowsData.forEach(flow => {
      if (!timeGroups[flow.timestamp]) {
        timeGroups[flow.timestamp] = [];
      }
      timeGroups[flow.timestamp].push(flow);
    });

    console.log('Time groups created:', Object.keys(timeGroups).length);

    // 创建图表数据点
    const chartDataPoints: ChartDataPoint[] = Object.entries(timeGroups).map(([timestamp, flows]) => {
      const time = parseInt(timestamp);
      const timeString = formatInTimeZone(time * 1000, 'America/New_York', 'MM-dd HH:mm');
      
      // 初始化数据
      let eth_inflow = 0, eth_outflow = 0;
      let usdc_inflow = 0, usdc_outflow = 0, usdc_net = 0;
      let usdt_inflow = 0, usdt_outflow = 0, usdt_net = 0;

      // 处理每个token的数据
      flows.forEach(flow => {
        if (flow.token_id === 141670) { // Ethereum
          eth_inflow += flow.inflow_usd;
          eth_outflow += flow.outflow_usd;
        } else if (flow.token_id === 141678) { // USDC
          usdc_inflow += flow.inflow_usd;
          usdc_outflow += flow.outflow_usd;
          usdc_net += flow.net_flow_usd;
        } else if (flow.token_id === 141685) { // USDT
          usdt_inflow += flow.inflow_usd;
          usdt_outflow += flow.outflow_usd;
          usdt_net += flow.net_flow_usd;
        }
      });

      const total_inflow = eth_inflow + usdc_inflow + usdt_inflow;
      const total_outflow = eth_outflow + usdc_outflow + usdt_outflow;
      const total_net = total_inflow - total_outflow;

      return {
        timestamp: time,
        timeString,
        eth_inflow: Math.round(eth_inflow * 100) / 100,
        eth_outflow: Math.round(eth_outflow * 100) / 100,
        usdc_inflow: Math.round(usdc_inflow * 100) / 100,
        usdc_outflow: Math.round(usdc_outflow * 100) / 100,
        usdt_inflow: Math.round(usdt_inflow * 100) / 100,
        usdt_outflow: Math.round(usdt_outflow * 100) / 100,
        usdc_net: Math.round(usdc_net * 100) / 100,
        usdt_net: Math.round(usdt_net * 100) / 100,
        total_inflow: Math.round(total_inflow * 100) / 100,
        total_outflow: Math.round(total_outflow * 100) / 100,
        total_net: Math.round(total_net * 100) / 100,
      };
    });

    // 按时间排序
    chartDataPoints.sort((a, b) => a.timestamp - b.timestamp);
    
    // 只取最近的数据点进行测试
    const limitedDataPoints = chartDataPoints.slice(-30);
    
    console.log('Chart data points created:', chartDataPoints.length);
    console.log('Limited data points for testing:', limitedDataPoints.length);
    console.log('Sample chart data:', limitedDataPoints.slice(0, 3));
    
    setChartData(limitedDataPoints);
  };

  // Chart.js 配置
  const barChartData = {
    labels: chartData.map(d => d.timeString),
    datasets: [
      {
        label: 'ETH Inflow',
        data: chartData.map(d => d.eth_inflow),
        backgroundColor: TOKEN_COLORS['Ethereum'],
        borderColor: TOKEN_COLORS['Ethereum'],
        borderWidth: 1,
        stack: 'inflow',
      },
      {
        label: 'USDC Inflow',
        data: chartData.map(d => d.usdc_inflow),
        backgroundColor: TOKEN_COLORS['USD Coin'],
        borderColor: TOKEN_COLORS['USD Coin'],
        borderWidth: 1,
        stack: 'inflow',
      },
      {
        label: 'USDT Inflow',
        data: chartData.map(d => d.usdt_inflow),
        backgroundColor: TOKEN_COLORS['Tether'],
        borderColor: TOKEN_COLORS['Tether'],
        borderWidth: 1,
        stack: 'inflow',
      },
      {
        label: 'ETH Outflow',
        data: chartData.map(d => -d.eth_outflow), // 负值显示在负半轴
        backgroundColor: '#FF6B6B',
        borderColor: '#FF6B6B',
        borderWidth: 1,
        stack: 'outflow',
      },
      {
        label: 'USDC Outflow',
        data: chartData.map(d => -d.usdc_outflow), // 负值显示在负半轴
        backgroundColor: '#FF8E8E',
        borderColor: '#FF8E8E',
        borderWidth: 1,
        stack: 'outflow',
      },
      {
        label: 'USDT Outflow',
        data: chartData.map(d => -d.usdt_outflow), // 负值显示在负半轴
        backgroundColor: '#FFB1B1',
        borderColor: '#FFB1B1',
        borderWidth: 1,
        stack: 'outflow',
      },
    ],
  };

  const lineChartData = {
    labels: chartData.map(d => d.timeString),
    datasets: [
      {
        label: 'ETH Net Flow',
        data: chartData.map(d => d.eth_inflow - d.eth_outflow),
        borderColor: TOKEN_COLORS['Ethereum'],
        backgroundColor: TOKEN_COLORS['Ethereum'],
        tension: 0.1,
        fill: false,
        borderWidth: 3,
      },
      {
        label: 'USDC Net Flow',
        data: chartData.map(d => d.usdc_net),
        borderColor: TOKEN_COLORS['USD Coin'],
        backgroundColor: TOKEN_COLORS['USD Coin'],
        tension: 0.1,
        fill: false,
        borderWidth: 3,
      },
      {
        label: 'USDT Net Flow',
        data: chartData.map(d => d.usdt_net),
        borderColor: TOKEN_COLORS['Tether'],
        backgroundColor: TOKEN_COLORS['Tether'],
        tension: 0.1,
        fill: false,
        borderWidth: 3,
      },
      {
        label: 'Total Net Flow',
        data: chartData.map(d => d.total_net),
        borderColor: '#999999',
        backgroundColor: '#999999',
        tension: 0.1,
        fill: false,
        borderWidth: 2,
        borderDash: [5, 5],
      },
    ],
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Token Flows - Inflow & Outflow',
      },
    },
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
        beginAtZero: false,
        grid: {
          color: function(context: any) {
            if (context.tick.value === 0) {
              return '#999999';
            }
            return '#f0f0f0';
          },
        },
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
        text: 'Token Net Flows',
      },
    },
    scales: {
      y: {
        beginAtZero: false,
        grid: {
          color: function(context: any) {
            if (context.tick.value === 0) {
              return '#999999';
            }
            return '#f0f0f0';
          },
        },
      },
    },
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Token Flows Chart (Chart.js)</h1>
          <div className="flex gap-4">
            <select
              value={timeframe}
              onChange={(e) => setTimeframe(e.target.value)}
              className="p-2 border rounded"
            >
              <option value="1H">1 Hour</option>
              <option value="4H">4 Hours</option>
              <option value="1D">1 Day</option>
            </select>
            <Link 
              href="/flows-chart" 
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            >
              Lightweight Chart
            </Link>
            <Link 
              href="/flows-chart-recharts" 
              className="px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 transition-colors"
            >
              Recharts Chart
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
                  <div className="w-4 h-4 bg-green-500 rounded"></div>
                  <span>Inflow (Positive)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-red-500 rounded"></div>
                  <span>Outflow (Negative)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4" style={{backgroundColor: TOKEN_COLORS['Ethereum']}}></div>
                  <span>ETH Net Flow</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4" style={{backgroundColor: TOKEN_COLORS['USD Coin']}}></div>
                  <span>USDC Net Flow</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4" style={{backgroundColor: TOKEN_COLORS['Tether']}}></div>
                  <span>USDT Net Flow</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-gray-500 rounded"></div>
                  <span>Total Net Flow (Dashed)</span>
                </div>
              </div>
              <div className="mt-2 text-xs text-gray-600">
                Debug: {flows.length} flows loaded, {chartData.length} chart points
                {chartData.length > 0 && (
                  <div className="mt-1">
                    Sample data: ETH Inflow={chartData[0]?.eth_inflow}, ETH Outflow={chartData[0]?.eth_outflow}, ETH Net={chartData[0]?.eth_inflow - chartData[0]?.eth_outflow}, USDC Net={chartData[0]?.usdc_net}
                  </div>
                )}
              </div>
            </div>
            
            <div className="space-y-8">
              {/* Bar Chart */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Token Flows - Inflow & Outflow (Bar Chart)</h3>
                <div className="h-[400px] border-2 border-gray-200">
                  <Bar data={barChartData} options={barOptions} />
                </div>
              </div>

              {/* Line Chart */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Token Net Flows (Line Chart)</h3>
                <div className="h-[400px] border-2 border-gray-200">
                  <Line data={lineChartData} options={lineOptions} />
                </div>
              </div>

              {/* Data Summary Table */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Data Summary</h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full bg-white border border-gray-300">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="px-4 py-2 border-b text-left">Token</th>
                        <th className="px-4 py-2 border-b text-right">Total Inflow (USD)</th>
                        <th className="px-4 py-2 border-b text-right">Total Outflow (USD)</th>
                        <th className="px-4 py-2 border-b text-right">Net Flow (USD)</th>
                        <th className="px-4 py-2 border-b text-right">Net Flow %</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr className="hover:bg-gray-50">
                        <td className="px-4 py-2 border-b font-medium">Ethereum</td>
                        <td className="px-4 py-2 border-b text-right text-green-600">
                          ${chartData.reduce((sum, d) => sum + d.eth_inflow, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right text-red-600">
                          ${chartData.reduce((sum, d) => sum + d.eth_outflow, 0).toLocaleString()}
                        </td>
                        <td className={`px-4 py-2 border-b text-right font-semibold ${
                          chartData.reduce((sum, d) => sum + d.eth_inflow - d.eth_outflow, 0) >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          ${chartData.reduce((sum, d) => sum + d.eth_inflow - d.eth_outflow, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right">
                          {((chartData.reduce((sum, d) => sum + d.eth_inflow - d.eth_outflow, 0) / 
                             chartData.reduce((sum, d) => sum + d.eth_inflow + d.eth_outflow, 0)) * 100).toFixed(2)}%
                        </td>
                      </tr>
                      <tr className="hover:bg-gray-50">
                        <td className="px-4 py-2 border-b font-medium">USDC</td>
                        <td className="px-4 py-2 border-b text-right text-green-600">
                          ${chartData.reduce((sum, d) => sum + d.usdc_inflow, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right text-red-600">
                          ${chartData.reduce((sum, d) => sum + d.usdc_outflow, 0).toLocaleString()}
                        </td>
                        <td className={`px-4 py-2 border-b text-right font-semibold ${
                          chartData.reduce((sum, d) => sum + d.usdc_net, 0) >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          ${chartData.reduce((sum, d) => sum + d.usdc_net, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right">
                          {((chartData.reduce((sum, d) => sum + d.usdc_net, 0) / 
                             chartData.reduce((sum, d) => sum + d.usdc_inflow + d.usdc_outflow, 0)) * 100).toFixed(2)}%
                        </td>
                      </tr>
                      <tr className="hover:bg-gray-50">
                        <td className="px-4 py-2 border-b font-medium">USDT</td>
                        <td className="px-4 py-2 border-b text-right text-green-600">
                          ${chartData.reduce((sum, d) => sum + d.usdt_inflow, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right text-red-600">
                          ${chartData.reduce((sum, d) => sum + d.usdt_outflow, 0).toLocaleString()}
                        </td>
                        <td className={`px-4 py-2 border-b text-right font-semibold ${
                          chartData.reduce((sum, d) => sum + d.usdt_net, 0) >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          ${chartData.reduce((sum, d) => sum + d.usdt_net, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right">
                          {((chartData.reduce((sum, d) => sum + d.usdt_net, 0) / 
                             chartData.reduce((sum, d) => sum + d.usdt_inflow + d.usdt_outflow, 0)) * 100).toFixed(2)}%
                        </td>
                      </tr>
                      <tr className="hover:bg-gray-50 bg-gray-100">
                        <td className="px-4 py-2 border-b font-bold">Total</td>
                        <td className="px-4 py-2 border-b text-right text-green-600 font-bold">
                          ${chartData.reduce((sum, d) => sum + d.total_inflow, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right text-red-600 font-bold">
                          ${chartData.reduce((sum, d) => sum + d.total_outflow, 0).toLocaleString()}
                        </td>
                        <td className={`px-4 py-2 border-b text-right font-bold ${
                          chartData.reduce((sum, d) => sum + d.total_net, 0) >= 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          ${chartData.reduce((sum, d) => sum + d.total_net, 0).toLocaleString()}
                        </td>
                        <td className="px-4 py-2 border-b text-right font-bold">
                          {((chartData.reduce((sum, d) => sum + d.total_net, 0) / 
                             chartData.reduce((sum, d) => sum + d.total_inflow + d.total_outflow, 0)) * 100).toFixed(2)}%
                        </td>
                      </tr>
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