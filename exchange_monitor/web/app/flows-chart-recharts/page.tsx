'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';
import { formatInTimeZone } from 'date-fns-tz';
import Link from 'next/link';
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  BarChart,
  LineChart,
} from 'recharts';

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

export default function FlowsChartRechartsPage() {
  const [loading, setLoading] = useState(true);
  const [timeframe, setTimeframe] = useState('1D');
  const [flows, setFlows] = useState<TokenFlow[]>([]);
  const [chartData, setChartData] = useState<ChartDataPoint[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchFlows();
  }, [timeframe]);

  const fetchFlows = async () => {
    setLoading(true);
    setError(null);
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
        .order('timestamp', { ascending: true });

      if (error) {
        console.error('Error fetching flows:', error);
        setError('Failed to fetch data: ' + error.message);
        return;
      }

      console.log('Fetched flows data:', data);
      console.log('Number of flows:', data?.length || 0);
      
      setFlows(data || []);
      processDataForChart(data || []);
    } catch (error) {
      console.error('Error fetching flows:', error);
      setError('Failed to fetch data: ' + (error as Error).message);
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
    const limitedDataPoints = chartDataPoints.slice(-5);
    
    console.log('Chart data points created:', chartDataPoints.length);
    console.log('Limited data points for testing:', limitedDataPoints.length);
    console.log('Sample chart data:', limitedDataPoints.slice(0, 3));
    
    setChartData(limitedDataPoints);
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white border border-gray-300 rounded-lg shadow-lg p-4">
          <p className="font-semibold text-gray-800 mb-2">{data.timeString}</p>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">ETH Inflow:</span>
              <span className="text-green-600 font-medium">${data.eth_inflow.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">ETH Outflow:</span>
              <span className="text-red-600 font-medium">${data.eth_outflow.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">USDC Inflow:</span>
              <span className="text-green-600 font-medium">${data.usdc_inflow.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">USDC Outflow:</span>
              <span className="text-red-600 font-medium">${data.usdc_outflow.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">USDT Inflow:</span>
              <span className="text-green-600 font-medium">${data.usdt_inflow.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">USDT Outflow:</span>
              <span className="text-red-600 font-medium">${data.usdt_outflow.toLocaleString()}</span>
            </div>
            <hr className="my-2" />
            <div className="flex justify-between">
              <span className="text-gray-600">USDC Net:</span>
              <span className={`font-medium ${data.usdc_net >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                ${data.usdc_net.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">USDT Net:</span>
              <span className={`font-medium ${data.usdt_net >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                ${data.usdt_net.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Total Net:</span>
              <span className={`font-medium ${data.total_net >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                ${data.total_net.toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Token Flows Chart (Recharts)</h1>
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
              href="/flows-chart-tv" 
              className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition-colors"
            >
              TradingView Chart
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
        ) : error ? (
          <div className="text-center py-8">
            <div className="text-red-500 text-lg font-semibold mb-2">Error</div>
            <p className="text-red-600">{error}</p>
          </div>
        ) : (
          <div className="bg-white border rounded-lg p-4">
            {/* Test Chart with hardcoded data */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">Test Chart (Hardcoded Data)</h3>
              <div className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={[
                    { name: 'A', value: 10 },
                    { name: 'B', value: 20 },
                    { name: 'C', value: 15 },
                    { name: 'D', value: 25 }
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="value" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Test Chart with actual data */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">Test Chart (Actual Data - First 3 points)</h3>
              <div className="h-[300px] border-2 border-green-500 bg-gray-50">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData.slice(0, 3)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timeString" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="eth_inflow" fill={TOKEN_COLORS['Ethereum']} name="ETH Inflow" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
            
            <div className="mb-4">
              <h2 className="text-lg font-semibold mb-2">Chart Legend</h2>
              <div className="flex flex-wrap gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-green-500 rounded"></div>
                  <span>Inflow Bars (Positive)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-red-500 rounded"></div>
                  <span>Outflow Bars (Negative)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-blue-500 rounded"></div>
                  <span>USDC Net Flow Line</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-green-600 rounded"></div>
                  <span>USDT Net Flow Line</span>
                </div>
              </div>
              <div className="mt-2 text-xs text-gray-600">
                Debug: {flows.length} flows loaded, {chartData.length} chart points
                {chartData.length > 0 && (
                  <div className="mt-1">
                    Sample data: ETH Inflow={chartData[0]?.eth_inflow}, USDC Net={chartData[0]?.usdc_net}
                  </div>
                )}
              </div>
            </div>
            
            <div className="h-[600px]">
              {chartData.length > 0 ? (
                <div>
                  {/* Simple Bar Chart */}
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold mb-2">Simple Bar Chart</h3>
                    <div className="h-[300px] w-full border-2 border-red-500 bg-gray-50">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={chartData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="timeString" />
                          <YAxis />
                          <Tooltip />
                          <Legend />
                          <Bar dataKey="eth_inflow" fill={TOKEN_COLORS['Ethereum']} name="ETH Inflow" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Simple Line Chart */}
                  <div className="mb-6">
                    <h3 className="text-lg font-semibold mb-2">Simple Line Chart</h3>
                    <div className="h-[300px] w-full border-2 border-blue-500 bg-gray-50">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={chartData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="timeString" />
                          <YAxis />
                          <Tooltip />
                          <Legend />
                          <Line type="monotone" dataKey="usdc_net" stroke={TOKEN_COLORS['USD Coin']} name="USDC Net" />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                  
                  {/* Debug info */}
                  <div className="mt-4 p-4 bg-gray-100 rounded text-xs">
                    <h3 className="font-bold mb-2">Debug Information:</h3>
                    <p>Chart data points: {chartData.length}</p>
                    <p>First data point: {JSON.stringify(chartData[0])}</p>
                    <p>Last data point: {JSON.stringify(chartData[chartData.length - 1])}</p>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-gray-500">
                  <div className="text-center">
                    <p>No chart data available</p>
                    <p className="text-sm">Data points: {chartData.length}</p>
                    <p className="text-sm">Raw flows: {flows.length}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  );
} 