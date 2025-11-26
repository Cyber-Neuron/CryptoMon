'use client';

import { useEffect, useState } from 'react';
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

export default function FlowsPage() {
  const [flows, setFlows] = useState<TokenFlow[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [pageSize] = useState(50);
  const [filterChainId, setFilterChainId] = useState<string>('');
  const [filterTokenId, setFilterTokenId] = useState<string>('');

  useEffect(() => {
    fetchFlows();
  }, [currentPage, filterChainId, filterTokenId]);

  const fetchFlows = async () => {
    setLoading(true);
    try {
      let query = supabase
        .from('token_flows')
        .select('*', { count: 'exact' });

      if (filterChainId) {
        query = query.eq('chain_id', parseInt(filterChainId));
      }
      if (filterTokenId) {
        query = query.eq('token_id', parseInt(filterTokenId));
      }

      const { data, count, error } = await query
        .order('timestamp', { ascending: false })
        .range((currentPage - 1) * pageSize, currentPage * pageSize - 1);

      if (error) {
        console.error('Error fetching flows:', error);
        return;
      }

      setFlows(data || []);
      setTotalPages(Math.ceil((count || 0) / pageSize));
    } catch (error) {
      console.error('Error fetching flows:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp: number) => {
    return formatInTimeZone(timestamp * 1000, 'America/New_York', 'yyyy-MM-dd HH:mm:ss');
  };

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 6,
    }).format(num);
  };

  const formatUSD = (num: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(num);
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Token Flows</h1>
          <div className="flex gap-4">
            <Link 
              href="/flows-chart" 
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            >
              View Chart
            </Link>
            <Link 
              href="/flows-chart-chartjs" 
              className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 transition-colors"
            >
              Chart.js Chart
            </Link>
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
              href="/" 
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            >
              Back to Dashboard
            </Link>
          </div>
        </div>

        {/* Filters */}
        <div className="mb-6 flex gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Chain ID:</label>
            <input
              type="number"
              value={filterChainId}
              onChange={(e) => setFilterChainId(e.target.value)}
              placeholder="Filter by chain ID"
              className="p-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Token ID:</label>
            <input
              type="number"
              value={filterTokenId}
              onChange={(e) => setFilterTokenId(e.target.value)}
              placeholder="Filter by token ID"
              className="p-2 border rounded"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={() => {
                setFilterChainId('');
                setFilterTokenId('');
                setCurrentPage(1);
              }}
              className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
            >
              Clear Filters
            </button>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            <p className="mt-2">Loading flows...</p>
          </div>
        ) : (
          <>
            {/* Flows Table */}
            <div className="overflow-x-auto">
              <table className="min-w-full bg-white border border-gray-300">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="px-4 py-2 border-b text-left">ID</th>
                    <th className="px-4 py-2 border-b text-left">Token ID</th>
                    <th className="px-4 py-2 border-b text-left">Chain ID</th>
                    <th className="px-4 py-2 border-b text-left">Timestamp</th>
                    <th className="px-4 py-2 border-b text-right">Inflow</th>
                    <th className="px-4 py-2 border-b text-right">Outflow</th>
                    <th className="px-4 py-2 border-b text-right">Net Flow</th>
                    <th className="px-4 py-2 border-b text-right">Inflow Count</th>
                    <th className="px-4 py-2 border-b text-right">Outflow Count</th>
                    <th className="px-4 py-2 border-b text-right">Inflow USD</th>
                    <th className="px-4 py-2 border-b text-right">Outflow USD</th>
                    <th className="px-4 py-2 border-b text-right">Net Flow USD</th>
                  </tr>
                </thead>
                <tbody>
                  {flows.map((flow) => (
                    <tr key={flow.id} className="hover:bg-gray-50">
                      <td className="px-4 py-2 border-b">{flow.id}</td>
                      <td className="px-4 py-2 border-b">{flow.token_id}</td>
                      <td className="px-4 py-2 border-b">{flow.chain_id}</td>
                      <td className="px-4 py-2 border-b">{formatTimestamp(flow.timestamp)}</td>
                      <td className="px-4 py-2 border-b text-right text-green-600">
                        {formatNumber(flow.inflow)}
                      </td>
                      <td className="px-4 py-2 border-b text-right text-red-600">
                        {formatNumber(flow.outflow)}
                      </td>
                      <td className={`px-4 py-2 border-b text-right font-semibold ${
                        flow.net_flow >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {formatNumber(flow.net_flow)}
                      </td>
                      <td className="px-4 py-2 border-b text-right">{flow.inflow_count}</td>
                      <td className="px-4 py-2 border-b text-right">{flow.outflow_count}</td>
                      <td className="px-4 py-2 border-b text-right text-green-600">
                        {formatUSD(flow.inflow_usd)}
                      </td>
                      <td className="px-4 py-2 border-b text-right text-red-600">
                        {formatUSD(flow.outflow_usd)}
                      </td>
                      <td className={`px-4 py-2 border-b text-right font-semibold ${
                        flow.net_flow_usd >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {formatUSD(flow.net_flow_usd)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-6 flex justify-center items-center gap-2">
                <button
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-1 border rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                >
                  Previous
                </button>
                
                <span className="px-3 py-1">
                  Page {currentPage} of {totalPages}
                </span>
                
                <button
                  onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-1 border rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                >
                  Next
                </button>
              </div>
            )}

            {flows.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No flows found matching the current filters.
              </div>
            )}
          </>
        )}
      </div>
    </main>
  );
} 