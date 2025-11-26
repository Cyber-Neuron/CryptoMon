'use client';

import { useState, useEffect } from 'react';
import { format } from 'date-fns';

export default function TransactionsPage() {
  const [wallets, setWallets] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [selectedFromWallet, setSelectedFromWallet] = useState('');
  const [selectedToWallet, setSelectedToWallet] = useState('');
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const limit = 50;

  // 获取钱包列表
  useEffect(() => {
    const fetchWallets = async () => {
      try {
        const response = await fetch('/api/wallets');
        const result = await response.json();
        
        if (result.success) {
          setWallets(result.data);
        }
      } catch (error) {
        console.error('Error fetching wallets:', error);
      }
    };

    fetchWallets();
  }, []);

  // 获取交易数据
  const fetchTransactions = async (resetPage = false) => {
    setLoading(true);
    try {
      const currentPage = resetPage ? 1 : page;
      const offset = (currentPage - 1) * limit;
      
      const params = new URLSearchParams({
        limit: limit.toString(),
        offset: offset.toString()
      });

      if (selectedFromWallet) {
        params.append('fromWalletId', selectedFromWallet);
      }
      if (selectedToWallet) {
        params.append('toWalletId', selectedToWallet);
      }

      const response = await fetch(`/api/transactions?${params}`);
      const result = await response.json();

      if (result.success) {
        if (resetPage) {
          setTransactions(result.data);
          setPage(1);
        } else {
          setTransactions(prev => [...prev, ...result.data]);
        }
        setHasMore(result.data.length === limit);
      }
    } catch (error) {
      console.error('Error fetching transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  // 当筛选条件改变时重新获取数据
  useEffect(() => {
    fetchTransactions(true);
  }, [selectedFromWallet, selectedToWallet]);

  // 加载更多数据
  const loadMore = () => {
    if (!loading && hasMore) {
      setPage(prev => prev + 1);
      fetchTransactions(false);
    }
  };

  // 格式化金额
  const formatAmount = (amount, decimals = 18) => {
    if (!amount) return '0';
    const num = parseFloat(amount) / Math.pow(10, decimals);
    return num.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 6
    });
  };

  // 格式化USD价值
  const formatUSD = (value) => {
    if (!value) return '-';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  // 格式化时间戳
  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '-';
    const date = new Date(timestamp * 1000);
    return format(date, 'yyyy-MM-dd HH:mm:ss');
  };

  // 截断地址显示
  const truncateAddress = (address) => {
    if (!address) return '-';
    return `${address.slice(0, 6)}...${address.slice(-4)}`;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">交易记录</h1>
          <p className="text-gray-600">查看和分析钱包之间的交易数据</p>
        </div>

        {/* 筛选器 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="fromWallet" className="block text-sm font-medium text-gray-700 mb-2">
                发送方钱包
              </label>
              <select
                id="fromWallet"
                value={selectedFromWallet}
                onChange={(e) => setSelectedFromWallet(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">所有发送方</option>
                {wallets.map((wallet) => (
                  <option key={wallet.id} value={wallet.id}>
                    {wallet.friendly_name || wallet.address} 
                    {wallet.grp_name && ` (${wallet.grp_name})`}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="toWallet" className="block text-sm font-medium text-gray-700 mb-2">
                接收方钱包
              </label>
              <select
                id="toWallet"
                value={selectedToWallet}
                onChange={(e) => setSelectedToWallet(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">所有接收方</option>
                {wallets.map((wallet) => (
                  <option key={wallet.id} value={wallet.id}>
                    {wallet.friendly_name || wallet.address}
                    {wallet.grp_name && ` (${wallet.grp_name})`}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* 交易列表 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    交易哈希
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    发送方
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    接收方
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    代币
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    数量
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    USD价值
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    时间
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    区块
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {transactions.map((tx) => (
                  <tr key={tx.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-blue-600">
                      <a 
                        href={`https://etherscan.io/tx/${tx.hash}`} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="hover:text-blue-800"
                      >
                        {truncateAddress(tx.hash)}
                      </a>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {tx.from_friendly_name || truncateAddress(tx.from_address)}
                      </div>
                      {tx.from_grp_name && (
                        <div className="text-xs text-gray-500">{tx.from_grp_name}</div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {tx.to_friendly_name || truncateAddress(tx.to_address)}
                      </div>
                      {tx.to_grp_name && (
                        <div className="text-xs text-gray-500">{tx.to_grp_name}</div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {tx.token_symbol}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatAmount(tx.amount)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatUSD(tx.usd_value)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatTimestamp(tx.timestamp)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {tx.block_number?.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* 加载更多按钮 */}
          {hasMore && (
            <div className="px-6 py-4 border-t border-gray-200">
              <button
                onClick={loadMore}
                disabled={loading}
                className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '加载中...' : '加载更多'}
              </button>
            </div>
          )}

          {/* 无数据状态 */}
          {!loading && transactions.length === 0 && (
            <div className="px-6 py-12 text-center">
              <div className="text-gray-500 text-sm">
                暂无交易数据
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 