'use client';

import { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';

export default function ETFChart({ data, asset }) {
  const chartContainerRef = useRef();
  const chartRef = useRef();
  const isCreatingChart = useRef(false); // 防止重复创建图表的标志

  useEffect(() => {
    if (!data || !chartContainerRef.current || isCreatingChart.current) {
      return;
    }

    // 检查DOM中是否已经有图表
    const existingCharts = chartContainerRef.current.querySelectorAll('canvas');
    
    if (existingCharts.length > 0) {
      chartContainerRef.current.innerHTML = '';
    }

    isCreatingChart.current = true; // 设置标志，防止重复创建

    // 清理之前的图表
    if (chartRef.current) {
      chartRef.current = null;
    }

    // 强制清理容器
    chartContainerRef.current.innerHTML = '';
    
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 600,
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#f0f0f0' },
        horzLines: { color: '#f0f0f0' },
      },
      crosshair: {
        mode: 1,
      },
      rightPriceScale: {
        borderColor: '#ddd',
        visible: true,
      },
      leftPriceScale: {
        borderColor: '#ddd',
        visible: true,
      },
      timeScale: {
        borderColor: '#ddd',
        timeVisible: true,
        secondsVisible: false,
      },
      tooltip: {
        enabled: true,
        mode: 1,
      },
    });

    // 创建K线图系列 (主图区域 - 顶部60%)
    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#26a69a',
      downColor: '#ef5350',
      borderVisible: false,
      wickUpColor: '#26a69a',
      wickDownColor: '#ef5350',
      priceScaleId: 'right',  // 主图
      scaleMargins: {
        top: 0.05,
        bottom: 0.25, // 为ETF留出空间
      },
    });

    // 创建ETF净流入柱状图系列 (底部区域 - 30%)
    const etfSeries = chart.addHistogramSeries({
      color: '#26a69a',
      priceFormat: {
        type: 'price',
        precision: 1,
        minMove: 0.1,
      },
      priceScaleId: 'left',   // 使用左侧价格轴
      scaleMargins: {
        top: 0.75,
        bottom: 0,
      },
    });

    // 配置左侧价格轴（ETF净流入）
    const leftPriceScale = chart.priceScale('left');
    if (leftPriceScale) {
      leftPriceScale.applyOptions({
        borderColor: '#ddd',
        visible: true,
        scaleMargins: {
          top: 0.75,
          bottom: 0,
        },
        // 添加轴标签
        title: 'ETF净流入 (百万美元)',
        titleColor: '#666',
        textColor: '#666',
      });
    }

    // 配置右侧价格轴（K线价格）
    const rightPriceScale = chart.priceScale('right');
    if (rightPriceScale) {
      rightPriceScale.applyOptions({
        borderColor: '#ddd',
        visible: true,
        scaleMargins: {
          top: 0.05,
          bottom: 0.25,
        },
        // 添加轴标签
        title: `${asset}价格 (USD)`,
        titleColor: '#666',
        textColor: '#666',
      });
    }

    // 设置数据
    const klineData = data.klineData.map(item => ({
      time: item.time,
      open: item.open,
      high: item.high,
      low: item.low,
      close: item.close,
    }));

    const etfData = data.etfData.map(item => ({
      time: item.time,
      value: item.netFlow, // 使用实际值而不是绝对值，这样可以显示正负
      color: item.netFlow >= 0 ? '#26a69a' : '#ef5350',
      // 添加额外的元数据用于工具提示
      netFlow: item.netFlow,
      date: item.date,
    }));

    candlestickSeries.setData(klineData);
    etfSeries.setData(etfData);

    // 添加宏观事件标记 - 使用正确的API
    
    const eventMarkers = data.events.map(event => ({
      time: event.time,
      position: 'aboveBar',
      color: '#ff6b6b',
      shape: 'arrowDown',
      text: event.type,
      size: 2, // 增加标记大小
    }));

    // 使用 setMarkers 添加事件标记到K线图系列
    candlestickSeries.setMarkers(eventMarkers);

    // 同时也在ETF系列上添加事件标记，让事件更明显
    const etfEventMarkers = data.events.map(event => ({
      time: event.time,
      position: 'aboveBar',
      color: '#ff6b6b',
      shape: 'circle',
      text: event.type,
      size: 1,
    }));

    etfSeries.setMarkers(etfEventMarkers);

    // 响应式调整
    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);
    chartRef.current = chart;
    isCreatingChart.current = false; // 重置标志

    return () => {
      window.removeEventListener('resize', handleResize);
      if (chartRef.current) {
        chartRef.current = null;
      }
      if (chartContainerRef.current) {
        chartContainerRef.current.innerHTML = ''; // 清空容器中的 old chart
      }
      isCreatingChart.current = false; // 重置标志
    };
  }, [data, asset]);

  if (!data) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-gray-500">暂无数据</div>
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          {asset} ETF流向与价格走势分析
        </h3>
        <p className="text-sm text-gray-600">
          时间范围: {new Date(data.klineData[0]?.time * 1000).toLocaleDateString()} - {new Date(data.klineData[data.klineData.length - 1]?.time * 1000).toLocaleDateString()}
        </p>
        {data.events.length > 0 && (
          <p className="text-sm text-red-600 mt-1">
            📍 图表上标记了 {data.events.length} 个宏观事件 (红色标记)
          </p>
        )}
      </div>
      
      <div ref={chartContainerRef} className="w-full" />
      
      {/* 统计信息 */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600">总ETF净流入</div>
          <div className={`text-lg font-semibold ${data.totalNetFlow >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {data.totalNetFlow.toLocaleString()} {asset}
          </div>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600">最大单日流入</div>
          <div className="text-lg font-semibold text-green-600">
            {Math.max(...data.etfData.map(d => d.netFlow)).toLocaleString()} {asset}
          </div>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600">最大单日流出</div>
          <div className="text-lg font-semibold text-red-600">
            {Math.min(...data.etfData.map(d => d.netFlow)).toLocaleString()} {asset}
          </div>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="text-sm text-gray-600">宏观事件数量</div>
          <div className="text-lg font-semibold text-blue-600">
            {data.events.length}
          </div>
        </div>
      </div>

      {/* 宏观事件列表 */}
      {data.events.length > 0 && (
        <div className="mt-6 bg-gray-50 p-4 rounded-lg">
          <h4 className="font-medium text-gray-700 mb-3">宏观事件列表</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
            {data.events.map((event, index) => (
              <div key={index} className="text-sm">
                <span className="font-medium text-blue-600">{event.type}</span>
                <span className="text-gray-600 ml-2">
                  {new Date(event.time * 1000).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
} 