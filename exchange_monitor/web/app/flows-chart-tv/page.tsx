'use client';

import { useEffect, useState, useRef } from 'react';
import { createClient } from '@supabase/supabase-js';
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

export default function FlowsChartTVPage() {
  const [loading, setLoading] = useState(true);
  const [timeframe, setTimeframe] = useState('1D');
  const [flows, setFlows] = useState<TokenFlow[]>([]);
  const chartContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchFlows();
  }, [timeframe]);

  useEffect(() => {
    // 动态加载TradingView脚本
    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/tv.js';
    script.async = true;
    script.onload = () => {
      if (chartContainerRef.current && typeof window !== 'undefined' && (window as any).TradingView) {
        createTradingViewWidget();
      }
    };
    document.head.appendChild(script);

    return () => {
      // 清理脚本
      const existingScript = document.querySelector('script[src="https://s3.tradingview.com/tv.js"]');
      if (existingScript) {
        existingScript.remove();
      }
    };
  }, []);

  const createTradingViewWidget = () => {
    if (!chartContainerRef.current || typeof window === 'undefined' || !(window as any).TradingView) {
      return;
    }

    const TradingView = (window as any).TradingView;
    
    new TradingView.widget({
      container_id: chartContainerRef.current.id,
      symbol: 'NASDAQ:AAPL',
      interval: 'D',
      timezone: 'America/New_York',
      theme: 'light',
      style: '1',
      locale: 'en',
      toolbar_bg: '#f1f3f6',
      enable_publishing: false,
      allow_symbol_change: true,
      hide_top_toolbar: false,
      hide_legend: false,
      save_image: false,
      backgroundColor: 'rgba(255, 255, 255, 1)',
      width: '100%',
      height: '100%',
    });
  };

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
        .order('timestamp', { ascending: true });

      if (error) {
        console.error('Error fetching flows:', error);
        return;
      }

      console.log('Fetched flows data:', data);
      console.log('Number of flows:', data?.length || 0);
      
      setFlows(data || []);
    } catch (error) {
      console.error('Error fetching flows:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Token Flows Chart (TradingView)</h1>
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
              <h2 className="text-lg font-semibold mb-2">TradingView Chart</h2>
              <p className="text-sm text-gray-600">
                This is a TradingView Advanced Real-Time Chart. Note that this component is designed for 
                displaying financial market data and may not be the best fit for our custom token flows data.
                For better visualization of our specific data, please use the Recharts or Lightweight Chart versions.
              </p>
            </div>
            
            <div className="h-[600px]">
              <div 
                id="tradingview_chart" 
                ref={chartContainerRef}
                style={{ width: '100%', height: '100%' }}
              />
            </div>
          </div>
        )}
      </div>
    </main>
  );
} 