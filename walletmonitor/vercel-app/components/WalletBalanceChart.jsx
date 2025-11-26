import { useState, useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';

// 获取ETH价格的函数，获取全局价格数据
const getEthUsdtPrices = async (startTime, endTime, interval = '1h') => {
  const url = "https://api.binance.com/api/v3/klines";
  const params = new URLSearchParams({
    symbol: "ETHUSDT",
    interval: interval,
    startTime: (startTime * 1000).toString(), // 转换为毫秒
    endTime: (endTime * 1000).toString(), // 转换为毫秒
  });

  try {
    //console.log(`🔍 请求ETH价格数据: ${url}?${params}`);
    const resp = await fetch(`${url}?${params}`, { 
      timeout: 10000,
      headers: {
        'Accept': 'application/json'
      }
    });
    
    if (!resp.ok) {
      console.error(`❌ ETH价格请求失败: ${resp.status} ${resp.statusText}`);
      return [];
    }
    
    const data = await resp.json();
    //console.log(`🔍 ETH价格响应数据条数:`, data.length);

    if (Array.isArray(data) && data.length > 0) {
      const priceData = data.map(item => ({
        time: Number(item[0]), // 时间戳（毫秒）
        value: parseFloat(item[4]) // 收盘价
      }));
      //console.log(`✅ 解析到ETH价格数据:`, priceData.length, '条');
      return priceData;
    } else {
      //console.log("❌ No ETH price data returned.");
      return [];
    }
  } catch (error) {
    console.error("❌ Error fetching ETH prices:", error);
    return [];
  }
};

export default function WalletBalanceChart({ walletIds }) {
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);
  const legendRef = useRef(null);
  const currentChartDataRef = useRef([]); // 存储当前图表数据
  const seriesRef = useRef(null); // 存储系列引用
  const ethPriceSeriesRef = useRef(null); // 存储ETH价格系列引用
  const [walletBalances, setWalletBalances] = useState([]);
  const [summary, setSummary] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [aggregationInterval, setAggregationInterval] = useState('1min'); // 默认1分钟聚合
  const [ethPriceData, setEthPriceData] = useState([]);
  const [isLoadingPrices, setIsLoadingPrices] = useState(false);

  // 聚合时间间隔选项
  const aggregationOptions = [
    { value: '1min', label: '1分钟', ms: 60 * 1000 },
    { value: '5min', label: '5分钟', ms: 5 * 60 * 1000 },
    { value: '10min', label: '10分钟', ms: 10 * 60 * 1000 },
    { value: '30min', label: '30分钟', ms: 30 * 60 * 1000 }
  ];

  // 聚合数据函数
  const aggregateData = (data, intervalMs) => {
    if (data.length === 0) return [];

    const aggregated = new Map();
    
    data.forEach(item => {
      // 将时间戳对齐到聚合间隔
      const alignedTime = Math.floor(item.time / intervalMs) * intervalMs;
      
      if (!aggregated.has(alignedTime)) {
        aggregated.set(alignedTime, {
          time: alignedTime,
          value: 0,
          count: 0,
          walletIds: new Set(),
          transactions: []
        });
      }
      
      const bucket = aggregated.get(alignedTime);
      bucket.value += item.value;
      bucket.count += 1;
      bucket.walletIds.add(item.walletId);
      bucket.transactions.push(item);
    });

    // 转换为数组并排序
    return Array.from(aggregated.values())
      .map(bucket => ({
        time: bucket.time,
        value: bucket.value,
        count: bucket.count,
        walletCount: bucket.walletIds.size,
        walletIds: Array.from(bucket.walletIds),
        transactions: bucket.transactions
      }))
      .sort((a, b) => a.time - b.time);
  };

  // Fetch wallet balances
  const fetchWalletBalances = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`/api/wallet-balances?walletIds=${walletIds.join(',')}`);
      const result = await response.json();
      if (result.success) {
        setWalletBalances(result.data);
        setSummary(result.summary);
        console.log('✅ 获取钱包余额成功:', result.data.length, '个钱包');
      } else {
        setError(result.error || '获取钱包余额失败');
        console.error('❌ 获取钱包余额失败:', result.error);
      }
    } catch (error) {
      setError('网络错误，请稍后重试');
      console.error('❌ Error fetching wallet balances:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // 获取ETH价格数据
  const fetchEthPrices = async () => {
    if (walletBalances.length === 0) {
      console.log('⚠️ 没有钱包余额数据，跳过ETH价格获取');
      return;
    }
    
    console.log('🔍 开始获取ETH价格数据，钱包余额数据数量:', walletBalances.length);
    setIsLoadingPrices(true);
    
    try {
      // 获取钱包余额数据的时间范围
      const timestamps = walletBalances.map(balance => Number(balance.time) / 1000); // 转换为秒
      const minTime = Math.min(...timestamps);
      const maxTime = Math.max(...timestamps);
      
      console.log('🔍 钱包余额数据时间范围:', {
        minTime: new Date(minTime * 1000).toLocaleString(),
        maxTime: new Date().toLocaleString(),
        duration: Math.floor((maxTime - minTime) / 3600) + '小时'
      });
      
      // 根据时间范围选择interval
      const duration = maxTime - minTime;
      let interval = '30m';
      // if (duration <= 3600) { // 1小时内
      //   interval = '1m';
      // } else if (duration <= 6 * 3600) { // 6小时内
      //   interval = '5m';
      // } else if (duration <= 24 * 3600) { // 24小时内
      //   interval = '15m';
      // } else if (duration <= 7 * 24 * 3600) { // 7天内
      //   interval = '1h';
      // } else { // 超过7天
      //   interval = '4h';
      // }
      
      console.log('🔍 选择的interval:', interval);
      
      // 获取ETH价格数据
      const priceData = await getEthUsdtPrices(minTime, maxTime, interval);
      
      console.log('🔍 ETH价格数据获取完成:', priceData.length, '条');
      setEthPriceData(priceData);
    } catch (error) {
      console.error('Error fetching ETH prices:', error);
    } finally {
      setIsLoadingPrices(false);
    }
  };

  useEffect(() => {
    fetchWalletBalances();
  }, [walletIds]);

  // 当钱包余额数据更新时获取ETH价格
  useEffect(() => {
    fetchEthPrices();
  }, [walletBalances]);

  // 监听聚合间隔变化，重新处理图表数据
  useEffect(() => {
    console.log('🔄 聚合间隔变化检查:', {
      hasChartRef: !!chartRef.current,
      hasSeriesRef: !!seriesRef.current,
      hasWalletBalances: walletBalances.length > 0
    });
    
    if (chartRef.current && seriesRef.current && walletBalances.length > 0) {
      // 清除现有图表数据
      const series = seriesRef.current;
      if (series) {
        series.setData([]);
      }
      
      // 重新处理数据
      console.log('🔄 聚合间隔变化，重新处理数据:', aggregationInterval);
      
      // 确保数据按时间升序排列，并处理重复时间戳
      let rawData = walletBalances
        .filter(balance => balance.time > 0) // 过滤掉无效的时间戳
        .filter(balance => balance.fromBalance !== null && balance.fromBalance !== undefined) // 过滤掉空的余额
        .filter(balance => parseFloat(balance.fromBalance) > 0) // 过滤掉余额为0的数据
        .map((balance, index) => {
          const fromBalance = parseFloat(balance.fromBalance);
          return {
            time: balance.time,
            value: fromBalance,
            walletId: balance.walletId,
            transactionId: balance.transactionId,
            fromBalance: fromBalance
          };
        })
        .filter(item => !isNaN(item.value) && item.value > 0) // 确保value是有效数字
        .sort((a, b) => a.time - b.time); // 按时间升序排列

      // 获取当前选择的聚合间隔
      const selectedOption = aggregationOptions.find(opt => opt.value === aggregationInterval);
      const intervalMs = selectedOption ? selectedOption.ms : 60 * 1000;

      // 聚合数据
      let chartData = aggregateData(rawData, intervalMs);
      console.log('🔍 聚合后的数据:', chartData.length, '条记录，间隔:', selectedOption?.label);

      // 处理重复时间戳
      const timeMap = new Map();
      chartData = chartData.map((item, index) => {
        let adjustedTime = item.time;
        
        if (timeMap.has(item.time)) {
          const count = timeMap.get(item.time);
          adjustedTime = item.time + (count * 1000);
          timeMap.set(item.time, count + 1);
        } else {
          timeMap.set(item.time, 1);
        }
        
        return {
          ...item,
          time: adjustedTime
        };
      });

      chartData.sort((a, b) => a.time - b.time);

      // 验证数据
      const finalValidation = chartData.every(item => 
        item.time !== undefined && 
        item.time > 0 && 
        item.value !== undefined && 
        !isNaN(item.value) && 
        item.value > 0
      );
      
      if (finalValidation && chartData.length > 0) {
        console.log('✅ 聚合数据验证通过，更新图表');
        
        // 转换为lightweight-charts期望的格式
        const chartDataFormatted = chartData.map(item => ({
          time: Number(item.time), // 确保使用Number()转换
          value: Number(item.value), // 确保使用Number()转换
          color: '#3B82F6' // 添加颜色属性
        }))
        .filter(item => !isNaN(item.time) && !isNaN(item.value) && item.time > 0 && item.value > 0); // 最终过滤
        
        console.log('🔍 格式化后的图表数据示例:', chartDataFormatted.slice(0, 3));
        console.log('🔍 数据格式验证:', chartDataFormatted.every(item => 
          typeof item.time === 'number' && 
          typeof item.value === 'number' && 
          !isNaN(item.time) && 
          !isNaN(item.value) && 
          item.time > 0 && 
          item.value > 0
        ));
        
        // 存储当前图表数据到ref中，供工具提示使用
        currentChartDataRef.current = chartData;
        
        try {
          series.setData(chartDataFormatted);
          console.log('✅ 图表数据设置成功');
          
          // 设置时间范围，让数据在图表中均匀分布
          if (chartDataFormatted.length > 0 && chartRef.current && chartRef.current.timeScale) {
            try {
              const sortedData = chartDataFormatted.sort((a, b) => a.time - b.time);
              const firstTime = sortedData[0].time;
              const lastTime = sortedData[sortedData.length - 1].time;
              
              // 计算显示范围：显示最后N个数据点，但确保数据均匀分布
              const N = 150; // 显示的数据点数量
              let from, to;
              
              if (sortedData.length > N) {
                // 如果数据点超过N个，显示最后N个
                from = sortedData[sortedData.length - N].time;
                to = lastTime;
              } else {
                // 如果数据点少于N个，显示所有数据，但添加一些边距
                const timeRange = lastTime - firstTime;
                const margin = timeRange * 0.05; // 5%的边距
                from = firstTime - margin;
                to = lastTime + margin;
              }
              
              console.log('🔍 设置时间范围:', {
                dataPoints: sortedData.length,
                from: new Date(from).toLocaleString(),
                to: new Date(to).toLocaleString(),
                range: Math.floor((to - from) / (1000 * 60)) + '分钟'
              });
              
              chartRef.current.timeScale().setVisibleRange({
                from,
                to
              });
              
              // 滚动到最右侧
              chartRef.current.timeScale().scrollToRealTime();
            } catch (error) {
              console.error('❌ 设置时间范围时出错:', error);
            }
          }
        } catch (error) {
          console.error('❌ 设置图表数据时出错:', error);
          console.error('❌ 错误数据:', chartDataFormatted);
        }
      } else {
        console.error('❌ 聚合数据验证失败');
      }
    }
  }, [aggregationInterval, walletBalances]);

  // 监听ETH价格数据变化，更新ETH价格线
  useEffect(() => {
    if (chartRef.current && ethPriceData && ethPriceData.length > 0) {
      console.log('🔍 ETH价格数据更新，重新设置ETH价格线:', ethPriceData.length, '条');
      
      // 如果ETH价格系列已存在，先移除
      if (ethPriceSeriesRef.current) {
        try {
          chartRef.current.removeSeries(ethPriceSeriesRef.current);
          console.log('✅ 移除旧的ETH价格系列');
        } catch (error) {
          console.error('❌ 移除ETH价格系列时出错:', error);
        }
      }
      
      // 创建新的ETH价格系列
      try {
        const ethPriceSeries = chartRef.current.addLineSeries({
          name: 'ETH Price',
          color: '#1976d2',
          lineWidth: 2,
          priceFormat: {
            type: 'price',
            precision: 2,
            minMove: 0.01,
          },
          priceScaleId: 'left',
          crosshairMarkerVisible: true,
          lastValueVisible: true,
        });
        
        console.log('🔍 ETH价格线创建成功，设置数据:', ethPriceData.length, '条');
        ethPriceSeries.setData(ethPriceData);
        ethPriceSeriesRef.current = ethPriceSeries;
        console.log('✅ ETH价格线更新成功');
      } catch (error) {
        console.error('❌ Error updating ETH price series:', error);
      }
    } else if (chartRef.current && (!ethPriceData || ethPriceData.length === 0)) {
      console.log('⚠️ ETH价格数据为空，移除ETH价格线');
      if (ethPriceSeriesRef.current) {
        try {
          chartRef.current.removeSeries(ethPriceSeriesRef.current);
          ethPriceSeriesRef.current = null;
          console.log('✅ ETH价格线已移除');
        } catch (error) {
          console.error('❌ 移除ETH价格系列时出错:', error);
        }
      }
    }
  }, [ethPriceData]);

  useEffect(() => {
    if (!chartContainerRef.current) return;
    if (chartRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: { 
        background: { color: '#ffffff' }, 
        textColor: '#333' 
      },
      grid: { 
        vertLines: { color: '#f0f0f0' }, 
        horzLines: { color: '#f0f0f0' } 
      },
      leftPriceScale: {
        borderColor: '#ddd',
        scaleMargins: {
          top: 0.1,
          bottom: 0.1,
        },
        visible: true,
      },
      rightPriceScale: { 
        borderColor: '#ddd',
        scaleMargins: {
          top: 0.1,
          bottom: 0.1,
        },
        visible: true,
      },
      timeScale: { 
        borderColor: '#ddd',
        timeVisible: true, 
        secondsVisible: false,
        timeUnit: 'hour',
        rightOffset: 0,
        leftOffset: 12,
        barSpacing: 6,
        fixLeftEdge: false,
        lockVisibleTimeRangeOnResize: true,
        rightBarStaysOnScroll: true,
        borderVisible: false,
        visible: true,
        tickMarkFormatter: (time) => {
          // 将时间戳转换为本地时间，参考 TransactionsChart.jsx
          const date = new Date(time);
          const options = {
            timeZone: 'America/New_York',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
          };
          const easternTime = new Intl.DateTimeFormat('en-US', options).format(date);
          return easternTime;
        },
      },
      crosshair: {
        mode: 1,
        vertLine: {
          color: '#999',
          width: 1,
          style: 0,
          labelBackgroundColor: '#f0f0f0',
        },
        horzLine: {
          color: '#999',
          width: 1,
          style: 0,
          labelBackgroundColor: '#f0f0f0',
        },
      },
      localization: {
        timeFormatter: (time) => {
          const date = new Date(time);
          return date.toLocaleString('en-US', {
            timeZone: 'America/New_York',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
          });
        }
      }
    });

    chartRef.current = chart;

    // 创建柱状图系列 - 使用addHistogramSeries而不是addBarSeries
    const series = chart.addHistogramSeries({
      name: 'Wallet Balance',
      color: '#3B82F6',
      priceFormat: { type: 'volume' },
      priceScaleId: 'right',
    });

    // 存储系列引用
    seriesRef.current = series;
    console.log('✅ 系列引用已设置:', !!seriesRef.current);

    // ETH价格线将在useEffect中动态创建，这里不再创建

    // 设置数据
    if (walletBalances.length > 0) {
      console.log('🔍 原始钱包余额数据:', walletBalances.length, '条记录');
      
      // 确保数据按时间升序排列，并处理重复时间戳
      let rawData = walletBalances
        .filter(balance => balance.time > 0) // 过滤掉无效的时间戳
        .filter(balance => balance.fromBalance !== null && balance.fromBalance !== undefined) // 过滤掉空的余额
        .filter(balance => parseFloat(balance.fromBalance) > 0) // 过滤掉余额为0的数据
        .map((balance, index) => {
          const fromBalance = parseFloat(balance.fromBalance);
          return {
            time: balance.time,
            value: fromBalance, // 使用fromBalance而不是balance.value
            walletId: balance.walletId,
            transactionId: balance.transactionId,
            fromBalance: fromBalance
          };
        })
        .filter(item => !isNaN(item.value) && item.value > 0) // 确保value是有效数字
        .sort((a, b) => a.time - b.time); // 按时间升序排列

      console.log('🔍 过滤后的有效余额数据:', rawData.length, '条记录');
      console.log('🔍 过滤掉的记录:', walletBalances.length - rawData.length, '条');

      // 获取当前选择的聚合间隔
      const selectedOption = aggregationOptions.find(opt => opt.value === aggregationInterval);
      const intervalMs = selectedOption ? selectedOption.ms : 60 * 1000;

      // 聚合数据
      let chartData = aggregateData(rawData, intervalMs);
      console.log('🔍 聚合后的数据:', chartData.length, '条记录，间隔:', selectedOption?.label);

      // 处理重复时间戳 - 改进版本
      const timeMap = new Map();
      chartData = chartData.map((item, index) => {
        let adjustedTime = item.time;
        
        // 如果时间戳已存在，添加偏移量
        if (timeMap.has(item.time)) {
          const count = timeMap.get(item.time);
          adjustedTime = item.time + (count * 1000); // 每个重复项增加count秒
          timeMap.set(item.time, count + 1);
        } else {
          timeMap.set(item.time, 1);
        }
        
        return {
          ...item,
          time: adjustedTime
        };
      });

      // 重新排序以确保时间顺序正确
      chartData.sort((a, b) => a.time - b.time);

      console.log('🔍 处理重复时间戳后的数据:', chartData.length, '条记录');

      // 最终验证数据是否按时间升序排列
      const isValidOrder = chartData.every((item, index) => {
        if (index === 0) return true;
        return item.time > chartData[index - 1].time;
      });

      if (!isValidOrder) {
        console.error('❌ 数据排序验证失败');
        console.error('❌ 问题数据:', chartData.map((d, index) => ({ 
          index,
          time: d.time, 
          value: d.value,
          walletId: d.walletId,
          originalTime: walletBalances.find(w => w.transactionId === d.transactionId)?.time,
          isOrdered: index === 0 || d.time > chartData[index - 1].time
        })));
        
        // 尝试最后一次排序修复
        console.log('🔄 尝试最后一次排序修复...');
        chartData.sort((a, b) => a.time - b.time);
        
        // 再次验证
        const finalCheck = chartData.every((item, index) => {
          if (index === 0) return true;
          return item.time > chartData[index - 1].time;
        });
        
        if (!finalCheck) {
          console.error('❌ 最终排序验证仍然失败，跳过图表渲染');
          return;
        } else {
          console.log('✅ 最终排序修复成功');
        }
      }

      console.log('✅ 数据排序验证通过');
      console.log('🔍 最终图表数据:', chartData.map(d => ({ 
        time: new Date(d.time).toLocaleString(), 
        value: d.value, 
        walletId: d.walletId 
      })));
      
      // 最终验证：确保所有数据都有有效的值
      const finalValidation = chartData.every(item => 
        item.time !== undefined && 
        item.time > 0 && 
        item.value !== undefined && 
        !isNaN(item.value) && 
        item.value > 0
      );
      
      if (!finalValidation) {
        console.error('❌ 最终数据验证失败，存在无效值');
        console.error('❌ 问题数据:', chartData.filter(item => 
          item.time === undefined || 
          item.time <= 0 || 
          item.value === undefined || 
          isNaN(item.value) || 
          item.value <= 0
        ));
        return;
      }
      
      console.log('✅ 最终数据验证通过，设置图表数据');
      
      // 转换为lightweight-charts期望的格式
      const chartDataFormatted = chartData.map(item => ({
        time: Number(item.time), // 确保使用Number()转换
        value: Number(item.value), // 确保使用Number()转换
        color: '#3B82F6' // 添加颜色属性
      }))
      .filter(item => !isNaN(item.time) && !isNaN(item.value) && item.time > 0 && item.value > 0); // 最终过滤
      
      console.log('🔍 格式化后的图表数据示例:', chartDataFormatted.slice(0, 3));
      console.log('🔍 数据格式验证:', chartDataFormatted.every(item => 
        typeof item.time === 'number' && 
        typeof item.value === 'number' && 
        !isNaN(item.time) && 
        !isNaN(item.value) && 
        item.time > 0 && 
        item.value > 0
      ));
      
      // 存储当前图表数据到ref中，供工具提示使用
      currentChartDataRef.current = chartData;
      
      try {
        series.setData(chartDataFormatted);
        console.log('✅ 图表数据设置成功');
        
        // 设置时间范围，让数据在图表中均匀分布
        if (chartDataFormatted.length > 0 && chartRef.current && chartRef.current.timeScale) {
          try {
            const sortedData = chartDataFormatted.sort((a, b) => a.time - b.time);
            const firstTime = sortedData[0].time;
            const lastTime = sortedData[sortedData.length - 1].time;
            
            // 计算显示范围：显示最后N个数据点，但确保数据均匀分布
            const N = 150; // 显示的数据点数量
            let from, to;
            
            if (sortedData.length > N) {
              // 如果数据点超过N个，显示最后N个
              from = sortedData[sortedData.length - N].time;
              to = lastTime;
            } else {
              // 如果数据点少于N个，显示所有数据，但添加一些边距
              const timeRange = lastTime - firstTime;
              const margin = timeRange * 0.05; // 5%的边距
              from = firstTime - margin;
              to = lastTime + margin;
            }
            
            console.log('🔍 初始化时设置时间范围:', {
              dataPoints: sortedData.length,
              from: new Date(from).toLocaleString(),
              to: new Date(to).toLocaleString(),
              range: Math.floor((to - from) / (1000 * 60)) + '分钟'
            });
            
            chartRef.current.timeScale().setVisibleRange({
              from,
              to
            });
            
            // 滚动到最右侧
            chartRef.current.timeScale().scrollToRealTime();
          } catch (error) {
            console.error('❌ 初始化时设置时间范围出错:', error);
          }
        }
      } catch (error) {
        console.error('❌ 设置图表数据时出错:', error);
        console.error('❌ 错误数据:', chartDataFormatted);
      }
    }

    // 添加工具提示
    const tooltip = document.createElement('div');
    tooltip.style.position = 'absolute';
    tooltip.style.display = 'none';
    tooltip.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
    tooltip.style.color = '#333';
    tooltip.style.padding = '12px 16px';
    tooltip.style.borderRadius = '8px';
    tooltip.style.fontSize = '12px';
    tooltip.style.fontFamily = 'Arial, sans-serif';
    tooltip.style.pointerEvents = 'none';
    tooltip.style.zIndex = '1000';
    tooltip.style.whiteSpace = 'nowrap';
    tooltip.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    tooltip.style.border = '1px solid rgba(0, 0, 0, 0.1)';
    tooltip.style.minWidth = '200px';
    chartContainerRef.current.appendChild(tooltip);

    // 鼠标移动事件
    chart.subscribeCrosshairMove((param) => {
      if (param.time !== undefined && param.seriesData) {
        const rect = chartContainerRef.current.getBoundingClientRect();
        
        // 查找ETH价格数据
        const ethPricePoint = ethPriceData.find(price => 
          Math.abs(price.time - param.time) < 60000 // 1分钟内的容差
        );
        
        // 检查是否有钱包余额数据
        const seriesData = param.seriesData.get(series);
        const aggregatedData = currentChartDataRef.current.find(d => {
          return Math.abs(d.time - param.time) < 2000; // 2秒内的容差
        });
        
        // 格式化时间显示
        const formatTime = (timestamp) => {
          if (!timestamp) return 'Unknown';
          const date = new Date(timestamp);
          return date.toLocaleString('en-US', {
            timeZone: 'America/New_York',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
          });
        };
        
        const selectedOption = aggregationOptions.find(opt => opt.value === aggregationInterval);
        
        let tooltipContent = '';
        let hasData = false;
        
        // 如果有钱包余额数据，显示余额信息
        if (seriesData && seriesData.value !== undefined && aggregatedData) {
          hasData = true;
          const formattedBalance = aggregatedData.value.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 6
          });
          
          tooltipContent += `
            <div style="margin-bottom: 6px; font-size: 11px; color: #999; border-bottom: 1px solid #eee; padding-bottom: 4px;">
              ${formatTime(aggregatedData.time)} (${selectedOption?.label || '1分钟'}聚合)
            </div>
            <div style="margin-bottom: 4px;">
              <div style="font-weight: bold; color: #3B82F6;">总余额</div>
              <div style="font-size: 12px; color: #3B82F6; font-family: monospace;">${formattedBalance}</div>
            </div>
            <div style="margin-bottom: 4px; font-size: 11px; color: #666;">
              交易数: ${aggregatedData.count || 0} | 钱包数: ${aggregatedData.walletCount || 0}
            </div>
          `;
        }
        
        // 如果有ETH价格数据，显示价格信息
        if (ethPricePoint) {
          hasData = true;
          const formattedPrice = ethPricePoint.value.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          });
          
          // 如果没有余额数据，显示时间标题
          if (!seriesData || seriesData.value === undefined) {
            tooltipContent += `
              <div style="margin-bottom: 6px; font-size: 11px; color: #999; border-bottom: 1px solid #eee; padding-bottom: 4px;">
                ${formatTime(ethPricePoint.time)}
              </div>
            `;
          }
          
          tooltipContent += `
            <div style="margin-bottom: 4px;">
              <div style="font-weight: bold; color: #1976d2;">ETH价格</div>
              <div style="font-size: 12px; color: #1976d2; font-family: monospace;">$${formattedPrice}</div>
            </div>
          `;
        }
        
        if (hasData) {
          tooltip.innerHTML = tooltipContent;
          tooltip.style.display = 'block';
          
          let left = param.point.x + 10;
          let top = param.point.y - tooltip.offsetHeight - 10;
          
          if (left + tooltip.offsetWidth > rect.width) {
            left = param.point.x - tooltip.offsetWidth - 10;
          }
          
          if (top < 0) {
            top = param.point.y + 10;
          }
          
          tooltip.style.left = `${left}px`;
          tooltip.style.top = `${top}px`;
        } else {
          tooltip.style.display = 'none';
        }
      } else {
        tooltip.style.display = 'none';
      }
    });

    // 鼠标离开图表时隐藏工具提示
    chartContainerRef.current.addEventListener('mouseleave', () => {
      tooltip.style.display = 'none';
    });

    // 响应式调整
    const handleResize = () => {
      if (chartRef.current && chartContainerRef.current) {
        chartRef.current.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
      if (tooltip) {
        tooltip.remove();
      }
      // 清理系列引用
      seriesRef.current = null;
      ethPriceSeriesRef.current = null;
    };
  }, [walletBalances]);

  // 添加图例
  useEffect(() => {
    if (walletBalances.length > 0 && chartContainerRef.current) {
      // 清除旧图例
      if (legendRef.current) {
        legendRef.current.remove();
      }

      const legend = document.createElement('div');
      legend.style.position = 'absolute';
      legend.style.left = '50%';
      legend.style.top = '-50px'; // 移到图表顶部上方
      legend.style.transform = 'translateX(-50%)'; // 居中显示
      legend.style.zIndex = '1';
      legend.style.fontSize = '12px';
      legend.style.fontFamily = 'Arial, sans-serif';
      legend.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
      legend.style.padding = '8px 12px';
      legend.style.borderRadius = '4px';
      legend.style.border = '1px solid #e0e0e0';
      legend.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
      legend.style.whiteSpace = 'nowrap'; // 防止换行
      
      let legendHtml = `<div style="font-weight: bold; margin-bottom: 4px;">钱包余额统计 (${walletIds.length} 个钱包)</div>`;
      
      // 添加聚合间隔信息
      const selectedOption = aggregationOptions.find(opt => opt.value === aggregationInterval);
      legendHtml += `<div style="margin: 2px 0; font-size: 11px; color: #666;">聚合间隔: ${selectedOption?.label || '1分钟'}</div>`;
      
      if (summary) {
        const formattedTotal = summary.totalBalance.toLocaleString('en-US', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 6
        });
        legendHtml += `<div style="margin: 2px 0;"><span style="color: #3B82F6;">■</span> 总余额 (右侧Y轴): ${formattedTotal}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`;
        legendHtml += `平均余额: ${(summary.totalBalance / summary.walletCount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 6 })}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`;
        legendHtml += `有效交易: ${summary.transactionCount} 条</div>`;
      }
      
      // 添加ETH价格线信息
      if (ethPriceData && ethPriceData.length > 0) {
        console.log('🔍 在图例中添加ETH价格线');
        // 根据数据量估算interval
        const duration = ethPriceData.length > 0 ? 
          (ethPriceData[ethPriceData.length - 1].time - ethPriceData[0].time) / (1000 * 60) : 0;
        const estimatedInterval = duration <= 60 ? '1m' : 
                                 duration <= 360 ? '5m' : 
                                 duration <= 1440 ? '15m' : 
                                 duration <= 10080 ? '1h' : '4h';
        legendHtml += `<div style="margin: 2px 0;"><span style="color: #1976d2;">─</span> ETH价格 (左侧Y轴, ${estimatedInterval})`;
        
        // 添加时间范围信息到同一行
        if (walletBalances.length > 0) {
          const formatTime = (timestamp) => {
            if (!timestamp) return 'Unknown';
            const date = new Date(timestamp);
            return date.toLocaleString('en-US', {
              timeZone: 'America/New_York',
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
              hour12: false
            });
          };
          
          // 创建排序后的数据副本用于时间范围计算
          const sortedData = [...walletBalances]
            .filter(balance => balance.time > 0)
            .sort((a, b) => a.time - b.time);
          
          if (sortedData.length > 0) {
            const earliestTime = sortedData[0].time;
            const latestTime = sortedData[sortedData.length - 1].time;
            
            legendHtml += `&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;时间范围: ${formatTime(earliestTime)} - ${formatTime(latestTime)}`;
          }
        }
        legendHtml += `</div>`;
      } else {
        console.log('⚠️ 图例中跳过ETH价格线，ethPriceData:', ethPriceData);
        
        // 如果没有ETH价格数据，单独显示时间范围
        if (walletBalances.length > 0) {
          const formatTime = (timestamp) => {
            if (!timestamp) return 'Unknown';
            const date = new Date(timestamp);
            return date.toLocaleString('en-US', {
              timeZone: 'America/New_York',
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
              hour12: false
            });
          };
          
          // 创建排序后的数据副本用于时间范围计算
          const sortedData = [...walletBalances]
            .filter(balance => balance.time > 0)
            .sort((a, b) => a.time - b.time);
          
          if (sortedData.length > 0) {
            const earliestTime = sortedData[0].time;
            const latestTime = sortedData[sortedData.length - 1].time;
            
            legendHtml += `<div style="margin: 2px 0; font-size: 11px; color: #666;">时间范围: ${formatTime(earliestTime)} - ${formatTime(latestTime)}</div>`;
          }
        }
      }
      
      legend.innerHTML = legendHtml;
      chartContainerRef.current.appendChild(legend);
      legendRef.current = legend;
    }

    return () => {
      if (legendRef.current) {
        legendRef.current.remove();
        legendRef.current = null;
      }
    };
  }, [walletBalances, summary, walletIds]);

  return (
    <div style={{ position: 'relative' }}>
      {/* 聚合间隔选择器 */}
      <div style={{
        position: 'absolute',
        top: '12px',
        right: '12px',
        zIndex: '1001',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        padding: '8px 12px',
        borderRadius: '6px',
        border: '1px solid #e0e0e0',
        fontSize: '12px',
        fontFamily: 'Arial, sans-serif',
        display: 'flex',
        alignItems: 'center',
        gap: '12px'
      }}>
        <label style={{ color: '#666' }}>聚合间隔:</label>
        <select
          value={aggregationInterval}
          onChange={(e) => setAggregationInterval(e.target.value)}
          style={{
            padding: '4px 8px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '12px',
            backgroundColor: '#fff'
          }}
        >
          {aggregationOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        
        <button
          onClick={() => {
            console.log('🔄 手动刷新数据');
            fetchWalletBalances();
            fetchEthPrices();
          }}
          disabled={isLoading || isLoadingPrices}
          style={{
            padding: '4px 12px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '12px',
            backgroundColor: isLoading || isLoadingPrices ? '#f5f5f5' : '#fff',
            color: isLoading || isLoadingPrices ? '#999' : '#333',
            cursor: isLoading || isLoadingPrices ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            transition: 'all 0.2s ease'
          }}
          onMouseEnter={(e) => {
            if (!isLoading && !isLoadingPrices) {
              e.target.style.backgroundColor = '#f0f0f0';
            }
          }}
          onMouseLeave={(e) => {
            if (!isLoading && !isLoadingPrices) {
              e.target.style.backgroundColor = '#fff';
            }
          }}
        >
          <span style={{ fontSize: '14px' }}>🔄</span>
          刷新
        </button>
      </div>

      <div ref={chartContainerRef} style={{ position: 'relative', height: '400px', marginTop: '60px' }} />
      
      {isLoadingPrices && (
        <div style={{
          position: 'absolute',
          top: '10px',
          right: '10px',
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          padding: '4px 8px',
          borderRadius: '4px',
          fontSize: '11px',
          color: '#666',
          zIndex: '1001'
        }}>
          获取ETH价格中...
        </div>
      )}
      
      {isLoading && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          padding: '12px 20px',
          borderRadius: '8px',
          fontSize: '14px',
          color: '#333',
          zIndex: '1002',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          border: '1px solid rgba(0, 0, 0, 0.1)'
        }}>
          正在获取钱包余额...
        </div>
      )}
      
      {error && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          padding: '12px 20px',
          borderRadius: '8px',
          fontSize: '14px',
          color: '#d32f2f',
          zIndex: '1002',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          border: '1px solid rgba(0, 0, 0, 0.1)'
        }}>
          {error}
        </div>
      )}
      
      {walletBalances.length === 0 && !isLoading && !error && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          padding: '12px 20px',
          borderRadius: '8px',
          fontSize: '14px',
          color: '#666',
          zIndex: '1002',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          border: '1px solid rgba(0, 0, 0, 0.1)'
        }}>
          暂无钱包余额数据
        </div>
      )}
    </div>
  );
} 