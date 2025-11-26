'use client';

import { useEffect, useRef, useState } from 'react';
import { createChart, ColorType, Time } from 'lightweight-charts';
import { createClient } from '@supabase/supabase-js';
import { format } from 'date-fns';
import { formatInTimeZone } from 'date-fns-tz';
import Link from 'next/link';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// MA periods
const MA_PERIODS = [7, 14, 30]; // 7天, 14天, 30天

export default function Home() {
  const [timeframe, setTimeframe] = useState('1H');
  const [maData, setMaData] = useState<{[key: string]: {value: number, change: number}}>({});
  const ethChartRef = useRef<HTMLDivElement>(null);
  const usdtChartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ethChartRef.current || !usdtChartRef.current) return;

    const ethChart = createChart(ethChartRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: 'white' },
        textColor: 'black',
      },
      width: ethChartRef.current.clientWidth,
      height: 400,
      timeScale: {
        timeVisible: true,
        secondsVisible: true,
        tickMarkFormatter: (time: number) => {
          const date = new Date(time * 1000);
          return formatInTimeZone(date, 'America/New_York', 'MM-dd HH:mm:ss');
        },
      },
      localization: {
        locale: 'en-US',
        timeFormatter: (time: number) => {
          const date = new Date(time * 1000);
          return formatInTimeZone(date, 'America/New_York', 'MM-dd HH:mm:ss');
        },
      },
    });

    const usdtChart = createChart(usdtChartRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: 'white' },
        textColor: 'black',
      },
      width: usdtChartRef.current.clientWidth,
      height: 400,
      timeScale: {
        timeVisible: true,
        secondsVisible: true,
        tickMarkFormatter: (time: number) => {
          const date = new Date(time * 1000);
          return formatInTimeZone(date, 'America/New_York', 'MM-dd HH:mm:ss');
        },
      },
      localization: {
        locale: 'en-US',
        timeFormatter: (time: number) => {
          const date = new Date(time * 1000);
          return formatInTimeZone(date, 'America/New_York', 'MM-dd HH:mm:ss');
        },
      },
    });

    const ethLineSeries = ethChart.addLineSeries({
      color: '#2962FF',
      lineWidth: 2,
      title: 'ETH Balance',
    });

    const usdtLineSeries = usdtChart.addLineSeries({
      color: '#2962FF',
      lineWidth: 2,
      title: 'USDT Balance',
    });

    // Add MA series for ETH
    const ethMaSeries = MA_PERIODS.map((period, index) => {
      const series = ethChart.addLineSeries({
        color: getMaColor(index),
        lineWidth: 2,
        title: `MA${period}`,
      });
      return { period, series };
    });

    // Add MA series for USDT
    const usdtMaSeries = MA_PERIODS.map((period, index) => {
      const series = usdtChart.addLineSeries({
        color: getMaColor(index),
        lineWidth: 2,
        title: `MA${period}`,
      });
      return { period, series };
    });

    const fetchData = async () => {
      const { data: ethData } = await supabase
        .from('wallet_balances')
        .select('*')
        .eq('wallet_id', 348)
        .gt('amount', 0)
        .order('ts', { ascending: false });

      const { data: usdtData } = await supabase
        .from('wallet_balances')
        .select('*')
        .eq('wallet_id', 355)
        .gt('amount', 0)
        .order('ts', { ascending: false });

      if (ethData) {
        const processedEthData = processData(ethData);
        ethLineSeries.setData(processedEthData);
        
        // Calculate and set MA data for ETH
        const ethMaData = calculateMA(processedEthData);
        ethMaSeries.forEach(({ period, series }) => {
          series.setData(ethMaData[period]);
        });
        updateMaChangeRates(ethMaData, 'ETH');
      }

      if (usdtData) {
        const processedUsdtData = processData(usdtData);
        usdtLineSeries.setData(processedUsdtData);
        
        // Calculate and set MA data for USDT
        const usdtMaData = calculateMA(processedUsdtData);
        usdtMaSeries.forEach(({ period, series }) => {
          series.setData(usdtMaData[period]);
        });
        updateMaChangeRates(usdtMaData, 'USDT');
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 60000); // Update every minute

    return () => {
      clearInterval(interval);
      ethChart.remove();
      usdtChart.remove();
    };
  }, [timeframe]);

  const processData = (data: any[]) => {
    // Create a map to store the latest value for each timestamp
    const timeMap = new Map<number, number>();
    
    // Process data and keep only the latest value for each timestamp
    data.forEach(item => {
      const utcDate = new Date(item.ts);
      // 转换为美国东部时间
      const etDate = new Date(utcDate.toLocaleString('en-US', { timeZone: 'America/New_York' }));
      const timestamp = Math.floor(etDate.getTime() / 1000);
      const value = Number(item.amount) / 1e18; // Convert from wei to ETH
      
      // Only keep the latest value for each timestamp
      timeMap.set(timestamp, value);
    });
    
    // Convert map to array and sort by timestamp
    return Array.from(timeMap.entries())
      .map(([time, value]) => ({
        time: time as Time,
        value: value,
      }))
      .sort((a, b) => Number(a.time) - Number(b.time));
  };

  const calculateMA = (data: any[]) => {
    const result: {[key: number]: any[]} = {};
    
    MA_PERIODS.forEach(period => {
      const maData = [];
      for (let i = period - 1; i < data.length; i++) {
        const slice = data.slice(i - period + 1, i + 1);
        const sum = slice.reduce((acc, curr) => acc + curr.value, 0);
        const ma = sum / period;
        
        maData.push({
          time: data[i].time,
          value: ma,
        });
      }
      result[period] = maData;
    });

    return result;
  };

  const updateMaChangeRates = (maData: {[key: number]: any[]}, asset: string) => {
    const rates: {[key: string]: {value: number, change: number}} = {};
    
    MA_PERIODS.forEach(period => {
      const data = maData[period];
      if (data.length > 0) {
        const currentValue = data[data.length - 1].value;
        const previousValue = data[data.length - 2]?.value;
        const change = previousValue ? ((currentValue - previousValue) / previousValue) * 100 : 0;
        
        rates[`${asset}_MA${period}`] = {
          value: currentValue,
          change: change,
        };
      }
    });
    
    setMaData(prev => ({...prev, ...rates}));
  };

  const getMaColor = (index: number) => {
    const colors = ['#FF9500', '#FF6B6B', '#2ECC71'];
    return colors[index % colors.length];
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Exchange Monitor</h1>
          <div className="flex gap-4">
            <Link 
              href="/flows" 
              className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
            >
              View Token Flows
            </Link>
            <Link 
              href="/flows-chart" 
              className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition-colors"
            >
              View Flows Chart
            </Link>
            <Link 
              href="/ex-flows-chart" 
              className="px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 transition-colors"
            >
              Exchange Flows Chart
            </Link>
          </div>
        </div>
        
        <div className="mb-4">
          <select
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
            className="p-2 border rounded"
          >
            <option value="1H">1 Hour</option>
            <option value="4H">4 Hours</option>
            <option value="1D">1 Day</option>
          </select>
        </div>

        <div className="space-y-8">
          <div>
            <h2 className="text-xl font-semibold mb-4">ETH Balance</h2>
            <div ref={ethChartRef} />
            <div className="mt-4 grid grid-cols-3 gap-4">
              {MA_PERIODS.map(period => (
                <div key={`ETH_MA${period}`} className="p-4 border rounded">
                  <h3 className="font-semibold">MA{period}</h3>
                  <p>Value: {maData[`ETH_MA${period}`]?.value.toFixed(2) || 'N/A'}</p>
                  <p className={maData[`ETH_MA${period}`]?.change >= 0 ? 'text-green-600' : 'text-red-600'}>
                    Change: {maData[`ETH_MA${period}`]?.change.toFixed(2)}%
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">USDT Balance</h2>
            <div ref={usdtChartRef} />
            <div className="mt-4 grid grid-cols-3 gap-4">
              {MA_PERIODS.map(period => (
                <div key={`USDT_MA${period}`} className="p-4 border rounded">
                  <h3 className="font-semibold">MA{period}</h3>
                  <p>Value: {maData[`USDT_MA${period}`]?.value.toFixed(2) || 'N/A'}</p>
                  <p className={maData[`USDT_MA${period}`]?.change >= 0 ? 'text-green-600' : 'text-red-600'}>
                    Change: {maData[`USDT_MA${period}`]?.change.toFixed(2)}%
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
} 