'use client';

import { useEffect, useRef, useState } from 'react';
import { createChart, ColorType, Time, IChartApi, ISeriesApi, HistogramData, CandlestickData } from 'lightweight-charts';
import { createClient } from '@supabase/supabase-js';
import { format } from 'date-fns';
import { formatInTimeZone } from 'date-fns-tz';
import Link from 'next/link';

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

// Token mapping - 根据常见的token_id映射到名称
const TOKEN_NAMES: { [key: number]: string } = {
  141670: 'Ethereum',    // 假设token_id 1是Ethereum
  141678: 'USD Coin',    // 假设token_id 2是USDC
  141685: 'Tether',      // 假设token_id 3是USDT
};

const TOKEN_COLORS = {
  'Ethereum': '#627EEA',
  'USD Coin': '#2775CA',
  'Tether': '#26A17B',
};

export default function FlowsChartPage() {
  const chartRef = useRef<HTMLDivElement>(null);
  const [chart, setChart] = useState<IChartApi | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeframe, setTimeframe] = useState('1D');
  const [flows, setFlows] = useState<TokenFlow[]>([]);
  const [tooltipData, setTooltipData] = useState<{
    visible: boolean;
    x: number;
    y: number;
    time: number;
    data: any;
  } | null>(null);

  useEffect(() => {
    if (!chartRef.current) {
      console.log('Chart ref not ready, waiting...');
      return;
    }

    console.log('Initializing chart, container dimensions:', {
      width: chartRef.current.clientWidth,
      height: chartRef.current.clientHeight,
      offsetWidth: chartRef.current.offsetWidth,
      offsetHeight: chartRef.current.offsetHeight
    });

    // 确保容器有尺寸
    if (chartRef.current.clientWidth === 0) {
      console.log('Container has no width, waiting for layout...');
      // 等待下一帧再尝试
      const timer = setTimeout(() => {
        if (chartRef.current && chartRef.current.clientWidth > 0) {
          console.log('Container now has width, creating chart');
          createInitialChart();
        }
      }, 100);
      return () => clearTimeout(timer);
    }

    createInitialChart();

    return () => {
      console.log('Cleaning up chart instance');
      if (chart) {
        chart.remove();
      }
    };
  }, []);

  const createInitialChart = () => {
    if (!chartRef.current) return;

    try {
      const chartInstance = createChart(chartRef.current, {
        layout: {
          background: { type: ColorType.Solid, color: 'white' },
          textColor: 'black',
        },
        width: chartRef.current.clientWidth || 800, // 提供默认宽度
        height: 600,
        timeScale: {
          timeVisible: true,
          secondsVisible: false,
          tickMarkFormatter: (time: number) => {
            const date = new Date(time * 1000);
            return formatInTimeZone(date, 'America/New_York', 'MM-dd HH:mm');
          },
        },
        localization: {
          locale: 'en-US',
          timeFormatter: (time: number) => {
            const date = new Date(time * 1000);
            return formatInTimeZone(date, 'America/New_York', 'MM-dd HH:mm:ss');
          },
        },
        rightPriceScale: {
          scaleMargins: {
            top: 0.1,
            bottom: 0.1,
          },
          visible: true,
          borderVisible: true,
        },
        leftPriceScale: {
          scaleMargins: {
            top: 0.1,
            bottom: 0.1,
          },
          visible: true,
          borderVisible: true,
          autoScale: true,
        },
        grid: {
          vertLines: {
            color: '#f0f0f0',
          },
          horzLines: {
            color: '#f0f0f0',
          },
        },
        crosshair: {
          mode: 1,
        },
      });

      // 添加鼠标移动事件监听
      chartInstance.subscribeCrosshairMove((param) => {
        if (param.time && param.point) {
          const time = param.time as number;
          const x = param.point.x;
          const y = param.point.y;
          
          // 获取该时间点的所有数据
          const timeData = getDataAtTime(time);
          
          // 计算悬浮层位置，确保不超出容器边界
          const containerRect = chartRef.current?.getBoundingClientRect();
          const tooltipWidth = 320; // 预估悬浮层宽度
          const tooltipHeight = 200; // 预估悬浮层高度
          
          let tooltipX = x + 10;
          let tooltipY = y - 10;
          
          // 如果悬浮层会超出右边界，则显示在鼠标左侧
          if (containerRect && tooltipX + tooltipWidth > containerRect.width) {
            tooltipX = x - tooltipWidth - 10;
          }
          
          // 如果悬浮层会超出上边界，则显示在鼠标下方
          if (tooltipY - tooltipHeight < 0) {
            tooltipY = y + 10;
          }
          
          setTooltipData({
            visible: true,
            x: tooltipX,
            y: tooltipY,
            time: time,
            data: timeData,
          });
        } else {
          setTooltipData(null);
        }
      });

      console.log('Chart instance created:', chartInstance);
      setChart(chartInstance);
    } catch (error) {
      console.error('Error creating initial chart:', error);
    }
  };

  // 获取指定时间点的所有数据
  const getDataAtTime = (timestamp: number) => {
    const timeData: any = {
      timestamp: timestamp,
      timeString: formatInTimeZone(timestamp * 1000, 'America/New_York', 'yyyy-MM-dd HH:mm:ss'),
      tokens: {},
    };

    // 按token_id分组该时间点的数据
    const tokenGroups: { [key: number]: TokenFlow[] } = {};
    flows.forEach(flow => {
      if (flow.timestamp === timestamp) {
        if (!tokenGroups[flow.token_id]) {
          tokenGroups[flow.token_id] = [];
        }
        tokenGroups[flow.token_id].push(flow);
      }
    });

    // 处理每个token的数据
    Object.entries(tokenGroups).forEach(([tokenIdStr, flows]) => {
      const tokenId = parseInt(tokenIdStr);
      const tokenName = TOKEN_NAMES[tokenId] || `Token ${tokenId}`;
      
      // 合并该token在该时间点的所有数据
      const merged = flows.reduce((acc, flow) => ({
        inflow: acc.inflow + flow.inflow_usd,
        outflow: acc.outflow + flow.outflow_usd,
        net: acc.net + flow.net_flow_usd,
        inflow_count: acc.inflow_count + flow.inflow_count,
        outflow_count: acc.outflow_count + flow.outflow_count,
      }), {
        inflow: 0,
        outflow: 0,
        net: 0,
        inflow_count: 0,
        outflow_count: 0,
      });

      timeData.tokens[tokenName] = {
        ...merged,
        color: TOKEN_COLORS[tokenName as keyof typeof TOKEN_COLORS] || '#666666',
      };
    });

    return timeData;
  };

  useEffect(() => {
    console.log('Timeframe changed to:', timeframe);
    fetchFlows();
  }, [timeframe]);

  // 添加窗口大小变化监听器
  useEffect(() => {
    const handleResize = () => {
      if (chart && chartRef.current) {
        console.log('Resizing chart to:', chartRef.current.clientWidth);
        chart.applyOptions({
          width: chartRef.current.clientWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [chart]);

  const fetchFlows = async () => {
    setLoading(true);
    try {
      // 获取最近的数据，根据timeframe调整
      let hours = 24; // 默认1天
      if (timeframe === '4H') hours = 4;
      if (timeframe === '1H') hours = 1;

      // 使用UTC时间计算截止时间，保持与数据库时间戳一致
      const cutoffTime = Math.floor(Date.now() / 1000) - (hours * 3600);
      
      console.log('Fetching flows with cutoff time (UTC):', new Date(cutoffTime * 1000).toISOString());

      const { data, error } = await supabase
        .from('token_flows')
        .select('*')
        .gte('timestamp', cutoffTime)
        .order('timestamp', { ascending: true });

      if (error) {
        console.error('Error fetching flows:', error);
        return;
      }

      console.log('Fetched flows data:', data);
      console.log('Number of flows:', data?.length || 0);
      
      if (data && data.length > 0) {
        console.log('First flow:', data[0]);
        console.log('Last flow:', data[data.length - 1]);
        console.log('Available token_ids:', Array.from(new Set(data.map(f => f.token_id))));
      }

      setFlows(data || []);
      
      // 检查组件是否仍然挂载
      if (chartRef.current) {
        updateChart(data || []);
      } else {
        console.log('Component unmounted, skipping chart update');
      }
    } catch (error) {
      console.error('Error fetching flows:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateChart = (flowsData: TokenFlow[]) => {
    console.log('updateChart called with data:', flowsData);
    console.log('Chart ref current:', chartRef.current);
    console.log('Chart instance:', chart);
    
    if (!chartRef.current) {
      console.error('Chart ref is not available');
      return;
    }

    if (!chart) {
      console.error('Chart instance is not available');
      return;
    }

    if (flowsData.length === 0) {
      console.log('No flows data to display');
      return;
    }

    try {
      // 清除现有系列
      console.log('Removing existing chart');
      chart.remove();

      console.log('Creating new chart');
      // 重新创建图表
      const newChart = createChart(chartRef.current, {
        layout: {
          background: { type: ColorType.Solid, color: 'white' },
          textColor: 'black',
        },
        width: chartRef.current.clientWidth || 800, // 提供默认宽度
        height: 600,
        timeScale: {
          timeVisible: true,
          secondsVisible: false,
          tickMarkFormatter: (time: number) => {
            const date = new Date(time * 1000);
            return formatInTimeZone(date, 'America/New_York', 'MM-dd HH:mm');
          },
        },
        localization: {
          locale: 'en-US',
          timeFormatter: (time: number) => {
            const date = new Date(time * 1000);
            return formatInTimeZone(date, 'America/New_York', 'MM-dd HH:mm:ss');
          },
        },
        rightPriceScale: {
          scaleMargins: {
            top: 0.1,
            bottom: 0.1,
          },
          visible: true,
          borderVisible: true,
        },
        leftPriceScale: {
          scaleMargins: {
            top: 0.1,
            bottom: 0.1,
          },
          visible: true,
          borderVisible: true,
          autoScale: true,
        },
        grid: {
          vertLines: {
            color: '#f0f0f0',
          },
          horzLines: {
            color: '#f0f0f0',
          },
        },
        crosshair: {
          mode: 1,
        },
      });

      setChart(newChart);
      console.log('New chart created');

      // 按token_id分组数据，用于柱状图
      const tokenGroups: { [key: number]: TokenFlow[] } = {};
      flowsData.forEach(flow => {
        if (!tokenGroups[flow.token_id]) {
          tokenGroups[flow.token_id] = [];
        }
        tokenGroups[flow.token_id].push(flow);
      });

      console.log('Token groups:', tokenGroups);
      console.log('Available token IDs:', Object.keys(tokenGroups));

      // 为每个token创建柱状图系列 - 使用数据偏移来实现并列显示
      const tokenIds = Object.keys(tokenGroups).map(id => parseInt(id)).sort();
      console.log('Sorted token IDs:', tokenIds);

      // 计算时间偏移，让柱状图并列显示
      const timeOffset = 300; // 5分钟偏移，可以根据需要调整

      tokenIds.forEach((tokenId, index) => {
        const tokenName = TOKEN_NAMES[tokenId] || `Token ${tokenId}`;
        const tokenColor = TOKEN_COLORS[tokenName as keyof typeof TOKEN_COLORS] || '#666666';

        console.log(`Processing token ${tokenId} (${tokenName}) with ${tokenGroups[tokenId].length} records`);

        // 合并同一timestamp下的记录
        const timeGroupedData: { [key: number]: { inflow: number; outflow: number; count: number } } = {};
        
        tokenGroups[tokenId].forEach(flow => {
          if (!timeGroupedData[flow.timestamp]) {
            timeGroupedData[flow.timestamp] = { inflow: 0, outflow: 0, count: 0 };
          }
          timeGroupedData[flow.timestamp].inflow += flow.inflow_usd;
          timeGroupedData[flow.timestamp].outflow += flow.outflow_usd;
          timeGroupedData[flow.timestamp].count += 1;
        });

        // 创建合并后的柱状图数据 - 添加时间偏移来实现并列显示
        const barData: HistogramData[] = Object.entries(timeGroupedData)
          .map(([timestamp, data]) => ({
            time: (parseInt(timestamp) + index * timeOffset) as Time,
            value: data.inflow, // 正值显示在正半轴
          }))
          .sort((a, b) => Number(a.time) - Number(b.time));

        // 创建合并后的流出柱状图数据（负值）
        const outflowBarData: HistogramData[] = Object.entries(timeGroupedData)
          .map(([timestamp, data]) => ({
            time: (parseInt(timestamp) + index * timeOffset) as Time,
            value: -data.outflow, // 负值显示在负半轴
          }))
          .sort((a, b) => Number(a.time) - Number(b.time));

        console.log(`Token ${tokenId} merged inflow data:`, barData.slice(0, 3)); // 显示前3条数据
        console.log(`Token ${tokenId} merged outflow data:`, outflowBarData.slice(0, 3)); // 显示前3条数据
        console.log(`Token ${tokenId} time groups:`, Object.keys(timeGroupedData).length);

        // 添加流入柱状图
        const inflowSeries = newChart.addHistogramSeries({
          color: tokenColor,
          priceFormat: {
            type: 'price',
            precision: 2,
            minMove: 0.01,
          },
          priceScaleId: 'right',
          title: `${tokenName} Inflow`,
        });
        inflowSeries.setData(barData);
        console.log(`Added inflow series for ${tokenName}`);

        // 添加流出柱状图
        const outflowSeries = newChart.addHistogramSeries({
          color: '#FF6B6B',
          priceFormat: {
            type: 'price',
            precision: 2,
            minMove: 0.01,
          },
          priceScaleId: 'right',
          title: `${tokenName} Outflow`,
        });
        outflowSeries.setData(outflowBarData);
        console.log(`Added outflow series for ${tokenName}`);
      });

      // 分别创建USDC和USDT的线图数据 - 也需要合并处理
      const usdcData: { time: Time; value: number }[] = [];
      const usdtData: { time: Time; value: number }[] = [];
      
      // 合并USDC数据
      const usdcTimeGroups: { [key: number]: { net: number; count: number } } = {};
      flowsData.forEach(flow => {
        if (flow.token_id === 141678) { // USDC
          if (!usdcTimeGroups[flow.timestamp]) {
            usdcTimeGroups[flow.timestamp] = { net: 0, count: 0 };
          }
          usdcTimeGroups[flow.timestamp].net += flow.net_flow_usd;
          usdcTimeGroups[flow.timestamp].count += 1;
        }
      });

      // 合并USDT数据
      const usdtTimeGroups: { [key: number]: { net: number; count: number } } = {};
      flowsData.forEach(flow => {
        if (flow.token_id === 141685) { // USDT
          if (!usdtTimeGroups[flow.timestamp]) {
            usdtTimeGroups[flow.timestamp] = { net: 0, count: 0 };
          }
          usdtTimeGroups[flow.timestamp].net += flow.net_flow_usd;
          usdtTimeGroups[flow.timestamp].count += 1;
        }
      });

      // 创建合并后的USDC线图数据
      Object.entries(usdcTimeGroups).forEach(([timestamp, data]) => {
        usdcData.push({
          time: parseInt(timestamp) as Time,
          value: data.net,
        });
      });

      // 创建合并后的USDT线图数据
      Object.entries(usdtTimeGroups).forEach(([timestamp, data]) => {
        usdtData.push({
          time: parseInt(timestamp) as Time,
          value: data.net,
        });
      });

      // 按时间排序
      usdcData.sort((a, b) => Number(a.time) - Number(b.time));
      usdtData.sort((a, b) => Number(a.time) - Number(b.time));

      console.log('USDC merged line data:', usdcData.slice(0, 3));
      console.log('USDT merged line data:', usdtData.slice(0, 3));
      console.log('USDC merged data points:', usdcData.length);
      console.log('USDT merged data points:', usdtData.length);

      // 添加USDC线图
      if (usdcData.length > 0) {
        const usdcLineSeries = newChart.addLineSeries({
          color: '#2775CA', // USDC蓝色
          lineWidth: 3, // 增加线条粗细
          priceScaleId: 'left',
          title: 'USDC Net Flow USD',
          lastValueVisible: true,
          priceLineVisible: false,
        });
        usdcLineSeries.setData(usdcData);
        console.log('Added USDC line series');
      }

      // 添加USDT线图
      if (usdtData.length > 0) {
        const usdtLineSeries = newChart.addLineSeries({
          color: '#26A17B', // USDT绿色
          lineWidth: 3, // 增加线条粗细
          priceScaleId: 'left',
          title: 'USDT Net Flow USD',
          lastValueVisible: true,
          priceLineVisible: false,
        });
        usdtLineSeries.setData(usdtData);
        console.log('Added USDT line series');
      }

      // 添加零线 - 使用左侧Y轴
      if (usdcData.length > 0 || usdtData.length > 0) {
        const allData = [...usdcData, ...usdtData];
        const sortedData = allData.sort((a, b) => Number(a.time) - Number(b.time));
        
        const zeroLineSeries = newChart.addLineSeries({
          color: '#999999',
          lineWidth: 2, // 增加零线粗细
          lineStyle: 2, // 虚线
          priceScaleId: 'left',
          title: 'Zero Line',
        });
        zeroLineSeries.setData([
          { time: sortedData[0].time, value: 0 },
          { time: sortedData[sortedData.length - 1].time, value: 0 },
        ]);
        console.log('Added zero line with left price scale');
      }

      console.log('Chart update completed');
    } catch (error) {
      console.error('Error updating chart:', error);
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Token Flows Chart (Line View)</h1>
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
              href="/flows-chart-recharts" 
              className="px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 transition-colors"
            >
              Recharts Chart
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
        ) : (
          <div className="bg-white border rounded-lg p-4 relative">
            <div className="mb-4">
              <h2 className="text-lg font-semibold mb-2">Chart Legend</h2>
              <div className="flex flex-wrap gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-green-500 rounded"></div>
                  <span>Inflow (Positive) - Right Y-axis (Grouped)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-red-500 rounded"></div>
                  <span>Outflow (Negative) - Right Y-axis (Grouped)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-blue-500 rounded"></div>
                  <span>USDC Net Flow - Left Y-axis</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-green-600 rounded"></div>
                  <span>USDT Net Flow - Left Y-axis</span>
                </div>
              </div>
              <p className="text-xs text-gray-600 mt-2">
                Note: Bar charts are grouped by token (ETH, USDC, USDT) with time offsets for better visibility.
              </p>
            </div>
            <div ref={chartRef} />
            
            {/* 悬浮层 */}
            {tooltipData && (
              <div 
                className="absolute bg-white border border-gray-300 rounded-lg shadow-lg p-4 z-10 max-w-md"
                style={{
                  left: `${tooltipData.x}px`,
                  top: `${tooltipData.y}px`,
                }}
              >
                <div className="text-sm">
                  <div className="font-semibold text-gray-800 mb-2">
                    {tooltipData.data.timeString}
                  </div>
                  
                  {Object.entries(tooltipData.data.tokens).map(([tokenName, tokenData]: [string, any]) => (
                    <div key={tokenName} className="mb-3 p-2 border-l-4 rounded" style={{ borderLeftColor: tokenData.color }}>
                      <div className="font-medium text-gray-700 mb-1">{tokenName}</div>
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Inflow:</span>
                          <span className="text-green-600 font-medium">
                            ${tokenData.inflow.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Outflow:</span>
                          <span className="text-red-600 font-medium">
                            ${tokenData.outflow.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Net Flow:</span>
                          <span className={`font-medium ${tokenData.net >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                            ${tokenData.net.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Transactions:</span>
                          <span className="text-gray-800 font-medium">
                            {tokenData.inflow_count + tokenData.outflow_count}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {Object.keys(tooltipData.data.tokens).length === 0 && (
                    <div className="text-gray-500 text-xs">
                      No data available for this time point
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}