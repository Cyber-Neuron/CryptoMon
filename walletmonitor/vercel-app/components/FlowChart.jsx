'use client';

import { useEffect, useRef, useState } from 'react';
import { createChart } from 'lightweight-charts';

// 获取ETH价格的函数，仿照Python代码
const getEthUsdtPriceAtUnix = async (unixTs) => {
  const ms = unixTs * 1000; // Binance 使用毫秒单位
  const url = "https://api.binance.com/api/v3/klines";
  const params = new URLSearchParams({
    symbol: "ETHUSDT",
    interval: "1m",
    startTime: (ms - 60000).toString(),
    endTime: ms.toString(),
  });

  try {
    const resp = await fetch(`${url}?${params}`, { timeout: 5000 });
    const data = await resp.json();

    if (Array.isArray(data) && data.length > 0) {
      const openPrice = parseFloat(data[0][1]); // [1] 是 open
      return openPrice;
    } else {
      //console.log("No data returned for that timestamp.");
      return null;
    }
  } catch (error) {
    console.error("Error fetching ETH price:", error);
    return null;
  }
};

// 创建单个图表的函数
const createSingleChart = (container, data, title, color, height = 200) => {
  if (!container) return null;

  // 创建工具提示元素
  const tooltip = document.createElement('div');
  tooltip.style.position = 'absolute';
  tooltip.style.display = 'none';
  tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
  tooltip.style.color = 'white';
  tooltip.style.padding = '8px 12px';
  tooltip.style.borderRadius = '4px';
  tooltip.style.fontSize = '12px';
  tooltip.style.fontFamily = 'Arial, sans-serif';
  tooltip.style.pointerEvents = 'none';
  tooltip.style.zIndex = '1000';
  tooltip.style.whiteSpace = 'nowrap';
  tooltip.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.3)';
  container.appendChild(tooltip);

  // 创建图表
  const chart = createChart(container, {
    height,
    layout: {
      background: { color: '#ffffff' },
      textColor: '#333',
    },
    grid: {
      vertLines: { color: '#f0f0f0' },
      horzLines: { color: '#f0f0f0' },
    },
    rightPriceScale: {
      borderColor: '#ddd',
      scaleMargins: {
        top: 0.1,
        bottom: 0.1,
      },
    },
    timeScale: {
      borderColor: '#ddd',
      timeVisible: true,
      secondsVisible: false,
      timeUnit: 'day',
      rightOffset: 0,
      leftOffset: 12,
      barSpacing: 6,
      fixLeftEdge: false,
      lockVisibleTimeRangeOnResize: true,
      rightBarStaysOnScroll: true,
      borderVisible: false,
      visible: true,
      timezone: 'America/New_York',
      tickMarkFormatter: (time) => {
        const date = new Date(time * 1000);
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
    localization: {
      timeFormatter: (time) => {
        const date = new Date(time * 1000);
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

  // 创建柱状图系列
  const histogramSeries = chart.addHistogramSeries({
    color: color,
    priceFormat: {
      type: 'price',
      precision: 2,
      minMove: 0.01,
    },
  });

  // 设置数据
  histogramSeries.setData(data);

  // 设置时间范围
  if (data.length > 0) {
    const lastTime = data[data.length - 1].time;
    const N = 150;
    const from = data.length > N
      ? data[data.length - N].time
      : data[0].time;
    chart.timeScale().setVisibleRange({
      from,
      to: lastTime
    });
    chart.timeScale().scrollToRealTime();
  }

  // 添加鼠标事件监听器
  chart.subscribeCrosshairMove((param) => {
    if (param.time && param.seriesData) {
      const histogramData = param.seriesData.get(histogramSeries);
      const rect = container.getBoundingClientRect();
      
      if (histogramData) {
        const value = Math.abs(histogramData.value);
        const formattedValue = value.toLocaleString('en-US', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 6
        });
        
        tooltip.innerHTML = `
          <div style="font-weight: bold; margin-bottom: 4px;">${title}</div>
          <div style="font-size: 11px;">${formattedValue}</div>
        `;
        
        tooltip.style.display = 'block';
        
        const tooltipWidth = 120;
        const tooltipHeight = 50;
        
        let left = param.point.x + 10;
        let top = param.point.y - tooltipHeight - 10;
        
        if (left + tooltipWidth > rect.width) {
          left = param.point.x - tooltipWidth - 10;
        }
        
        if (top < 0) {
          top = param.point.y + 10;
        }
        
        tooltip.style.left = `${left}px`;
        tooltip.style.top = `${top}px`;
      }
    } else {
      tooltip.style.display = 'none';
    }
  });

  // 鼠标离开图表时隐藏工具提示
  container.addEventListener('mouseleave', () => {
    tooltip.style.display = 'none';
  });

  return { chart, histogramSeries, tooltip };
};

export default function FlowChart({ data, token, height = 400, ethPriceData = [], fromGroups = [], toGroups = [] }) {
  const chartContainerRef = useRef(null);
  const netOutflowContainerRef = useRef(null);
  const netInflowContainerRef = useRef(null);
  const chartRef = useRef(null);
  const netOutflowChartRef = useRef(null);
  const netInflowChartRef = useRef(null);
  const histogramSeriesRef = useRef(null);
  const lineSeriesRef = useRef(null);
  const tooltipRef = useRef(null);
  const [isLoadingPrices, setIsLoadingPrices] = useState(false);

  // 检查是否指定了精确流向过滤
  const hasExactFlowFilter = (fromGroups && fromGroups.length > 0) || (toGroups && toGroups.length > 0);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    // 创建工具提示元素
    const tooltip = document.createElement('div');
    tooltip.style.position = 'absolute';
    tooltip.style.display = 'none';
    tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    tooltip.style.color = 'white';
    tooltip.style.padding = '8px 12px';
    tooltip.style.borderRadius = '4px';
    tooltip.style.fontSize = '12px';
    tooltip.style.fontFamily = 'Arial, sans-serif';
    tooltip.style.pointerEvents = 'none';
    tooltip.style.zIndex = '1000';
    tooltip.style.whiteSpace = 'nowrap';
    tooltip.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.3)';
    chartContainerRef.current.appendChild(tooltip);
    tooltipRef.current = tooltip;

    // 创建主图表
    const chart = createChart(chartContainerRef.current, {
      height,
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#f0f0f0' },
        horzLines: { color: '#f0f0f0' },
      },
      rightPriceScale: {
        borderColor: '#ddd',
        scaleMargins: {
          top: 0.1,
          bottom: 0.1,
        },
      },
      leftPriceScale: {
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
        timeUnit: 'day',
        rightOffset: 0,
        leftOffset: 12,
        barSpacing: 6,
        fixLeftEdge: false,
        lockVisibleTimeRangeOnResize: true,
        rightBarStaysOnScroll: true,
        borderVisible: false,
        visible: true,
        timezone: 'America/New_York',
        tickMarkFormatter: (time) => {
          // 将时间戳转换为美东时间
          const date = new Date(time * 1000);
          const options = {
            timeZone: 'America/New_York',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
          };
          
          // 强制使用美东时区格式化
          const easternTime = new Intl.DateTimeFormat('en-US', options).format(date);
          //console.log(`时间戳 ${time} -> 美东时间: ${easternTime}`);
          
          return easternTime;
        },
      },
      localization: {
        timeFormatter: (time) => {
          const date = new Date(time * 1000);
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

    // 创建柱状图系列（资金流向）
    const histogramSeries = chart.addHistogramSeries({
      color: hasExactFlowFilter ? '#26a69a' : '#26a69a', // 精确流向时统一使用绿色
      priceFormat: {
        type: 'price',
        precision: 2,
        minMove: 0.01,
      },
      priceScaleId: 'right',
    });

    // 创建折线图系列（ETH价格）
    const lineSeries = chart.addLineSeries({
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

    // 处理数据
    const processedData = data.map(item => ({
      time: Number(item.time),
      value: item.value,
      color: hasExactFlowFilter ? '#26a69a' : (item.value >= 0 ? '#26a69a' : '#ef5350'), // 精确流向时统一使用绿色
    }));

    // 设置数据
    histogramSeries.setData(processedData);
    // 设置价格数据（ETH价格线）
    if (ethPriceData && ethPriceData.length > 0) {
      lineSeries.setData(ethPriceData);
    }

    // 设置时间范围，让数据紧贴右侧显示
    if (processedData.length > 0) {
      const lastTime = processedData[processedData.length - 1].time;
      const N = 150;
      const from = processedData.length > N
        ? processedData[processedData.length - N].time
        : processedData[0].time;
      chart.timeScale().setVisibleRange({
        from,
        to: lastTime
      });
      // 关键：滚动到最右侧
      chart.timeScale().scrollToRealTime();
    }

    // 添加图例
    const legend = document.createElement('div');
    legend.style.position = 'absolute';
    legend.style.left = '12px';
    legend.style.top = '12px';
    legend.style.zIndex = '1';
    legend.style.fontSize = '12px';
    legend.style.fontFamily = 'Arial, sans-serif';
    
    if (hasExactFlowFilter) {
      legend.innerHTML = `
        <div style="display: flex; gap: 16px;">
          <div style="display: flex; align-items: center; gap: 4px;">
            <div style="width: 12px; height: 12px; background: #26a69a;"></div>
            <span>资金流向</span>
          </div>
          <div style="display: flex; align-items: center; gap: 4px;">
            <div style="width: 12px; height: 2px; background: #1976d2;"></div>
            <span>ETH价格</span>
          </div>
        </div>
      `;
    } else {
      legend.innerHTML = `
        <div style="display: flex; gap: 16px;">
          <div style="display: flex; align-items: center; gap: 4px;">
            <div style="width: 12px; height: 12px; background: #26a69a;"></div>
            <span>流入</span>
          </div>
          <div style="display: flex; align-items: center; gap: 4px;">
            <div style="width: 12px; height: 12px; background: #ef5350;"></div>
            <span>流出</span>
          </div>
          <div style="display: flex; align-items: center; gap: 4px;">
            <div style="width: 12px; height: 2px; background: #1976d2;"></div>
            <span>ETH价格</span>
          </div>
        </div>
      `;
    }
    
    chartContainerRef.current.appendChild(legend);

    // 添加鼠标事件监听器
    chart.subscribeCrosshairMove((param) => {
      if (param.time && param.seriesData) {
        const histogramData = param.seriesData.get(histogramSeries);
        const lineData = param.seriesData.get(lineSeries);
        const rect = chartContainerRef.current.getBoundingClientRect();
        
        // 从原始数据中获取 amount 信息
        const originalData = data.find(item => Number(item.time) === param.time);
        
        if (histogramData) {
          const amount = originalData?.amount || Math.abs(histogramData.value);
          const usdValue = originalData?.usd_value || Math.abs(histogramData.value);
          
          // 格式化数量
          const formattedAmount = Math.abs(amount).toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 6
          });
          
          // 格式化 USD 值
          const formattedUSD = Math.abs(usdValue).toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          });
          
          const tokenSymbol = originalData?.token || 'ETH';
          
          // 获取流向信息 - 优先使用详细的钱包信息
          const getFromDisplayName = () => {
            if (originalData?.from_friendly_name) {
              return originalData.from_friendly_name;
            } else if (originalData?.from_grp_name_detail) {
              return originalData.from_grp_name_detail;
            } else if (originalData?.from_grp_name) {
              return originalData.from_grp_name;
            }
            return '未知';
          };
          
          const getToDisplayName = () => {
            if (originalData?.to_friendly_name) {
              return originalData.to_friendly_name;
            } else if (originalData?.to_grp_name_detail) {
              return originalData.to_grp_name_detail;
            } else if (originalData?.to_grp_name) {
              return originalData.to_grp_name;
            }
            return '未知';
          };
          
          const fromGroup = getFromDisplayName();
          const toGroup = getToDisplayName();
          
          let tooltipContent = '';
          
          if (hasExactFlowFilter) {
            // 精确流向模式：显示流向信息
            tooltipContent = `
              <div style="font-weight: bold; margin-bottom: 4px;">资金流向</div>
              <div style="margin-bottom: 2px;">+${formattedAmount} ${tokenSymbol}</div>
              <div style="font-size: 11px; color: #ccc;">$${formattedUSD} USD</div>
              <div style="margin-top: 4px; font-size: 11px; color: #666;">
                <div>从: ${fromGroup}</div>
                <div>到: ${toGroup}</div>
              </div>
            `;
          } else {
            // 原有模式：显示流入/流出
            const direction = histogramData.value >= 0 ? '流入' : '流出';
            const sign = histogramData.value >= 0 ? '+' : '-';
            
            tooltipContent = `
              <div style="font-weight: bold; margin-bottom: 4px;">${direction}</div>
              <div style="margin-bottom: 2px;">${sign}${formattedAmount} ${tokenSymbol}</div>
              <div style="font-size: 11px; color: #ccc;">$${formattedUSD} USD</div>
            `;
            
            // 显示流向信息
            if (fromGroup !== '未知' || toGroup !== '未知') {
              tooltipContent += `
                <div style="margin-top: 4px; font-size: 11px; color: #666;">
                  <div>从: ${fromGroup}</div>
                  <div>到: ${toGroup}</div>
                </div>
              `;
            }
          }
          
          // 如果有价格数据，也显示价格
          if (lineData) {
            const formattedPrice = lineData.value.toLocaleString('en-US', {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            });
            tooltipContent += `<div style="margin-top: 4px; font-size: 11px; color: #1976d2;">价格: $${formattedPrice}</div>`;
          }
          
          tooltip.innerHTML = tooltipContent;
          
          tooltip.style.display = 'block';
          
          // 计算工具提示位置 - 显示在鼠标指针附近
          const tooltipWidth = 160; // 增加宽度以适应更多内容
          const tooltipHeight = lineData ? 100 : 80; // 如果有价格数据，增加高度
          
          let left = param.point.x + 10; // 鼠标右侧10px
          let top = param.point.y - tooltipHeight - 10; // 鼠标上方10px
          
          // 确保工具提示不超出容器边界
          if (left + tooltipWidth > rect.width) {
            left = param.point.x - tooltipWidth - 10; // 显示在鼠标左侧
          }
          
          if (top < 0) {
            top = param.point.y + 10; // 显示在鼠标下方
          }
          
          tooltip.style.left = `${left}px`;
          tooltip.style.top = `${top}px`;
        } else if (lineData) {
          // 只有价格数据时
          const formattedPrice = lineData.value.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          });
          
          tooltip.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 4px;">ETH价格</div>
            <div style="font-size: 11px; color: #1976d2;">$${formattedPrice}</div>
          `;
          
          tooltip.style.display = 'block';
          
          const tooltipWidth = 100;
          const tooltipHeight = 40;
          
          let left = param.point.x + 10;
          let top = param.point.y - tooltipHeight - 10;
          
          if (left + tooltipWidth > rect.width) {
            left = param.point.x - tooltipWidth - 10;
          }
          
          if (top < 0) {
            top = param.point.y + 10;
          }
          
          tooltip.style.left = `${left}px`;
          tooltip.style.top = `${top}px`;
        }
      } else {
        tooltip.style.display = 'none';
      }
    });

    // 鼠标离开图表时隐藏工具提示
    chartContainerRef.current.addEventListener('mouseleave', () => {
      tooltip.style.display = 'none';
    });

    chartRef.current = chart;
    histogramSeriesRef.current = histogramSeries;
    lineSeriesRef.current = lineSeries;

    // 清理函数
    return () => {
      if (chartRef.current) {
        chartRef.current.remove();
      }
      if (tooltipRef.current) {
        tooltipRef.current.remove();
      }
    };
  }, [data, height, ethPriceData, fromGroups, toGroups]);

  // 创建净流出图表 - 只在非精确流向模式下显示
  useEffect(() => {
    if (!netOutflowContainerRef.current || !data.length || hasExactFlowFilter) return;

    // 处理净流出数据（只显示负值）
    const outflowData = data
      .filter(item => item.value < 0)
      .map(item => ({
        time: Number(item.time),
        value: Math.abs(item.value), // 取绝对值显示
        color: '#ef5350', // 红色
      }));

    const { chart, histogramSeries, tooltip } = createSingleChart(
      netOutflowContainerRef.current,
      outflowData,
      '净流出',
      '#ef5350',
      200
    );

    netOutflowChartRef.current = { chart, histogramSeries, tooltip };

    return () => {
      if (netOutflowChartRef.current?.chart) {
        netOutflowChartRef.current.chart.remove();
      }
      if (netOutflowChartRef.current?.tooltip) {
        netOutflowChartRef.current.tooltip.remove();
      }
    };
  }, [data, hasExactFlowFilter]);

  // 创建净流入图表 - 只在非精确流向模式下显示
  useEffect(() => {
    if (!netInflowContainerRef.current || !data.length || hasExactFlowFilter) return;

    // 处理净流入数据（只显示正值）
    const inflowData = data
      .filter(item => item.value > 0)
      .map(item => ({
        time: Number(item.time),
        value: item.value,
        color: '#26a69a', // 绿色
      }));

    const { chart, histogramSeries, tooltip } = createSingleChart(
      netInflowContainerRef.current,
      inflowData,
      '净流入',
      '#26a69a',
      200
    );

    netInflowChartRef.current = { chart, histogramSeries, tooltip };

    return () => {
      if (netInflowChartRef.current?.chart) {
        netInflowChartRef.current.chart.remove();
      }
      if (netInflowChartRef.current?.tooltip) {
        netInflowChartRef.current.tooltip.remove();
      }
    };
  }, [data, hasExactFlowFilter]);

  // 当数据更新时重新设置数据
  useEffect(() => {
    if (histogramSeriesRef.current && lineSeriesRef.current && data.length > 0) {
      const processedData = data.map(item => ({
        time: Number(item.time),
        value: item.value,
        color: hasExactFlowFilter ? '#26a69a' : (item.value >= 0 ? '#26a69a' : '#ef5350'),
      }));
      histogramSeriesRef.current.setData(processedData);
      if (ethPriceData && ethPriceData.length > 0) {
        lineSeriesRef.current.setData(ethPriceData);
      }
    }
  }, [data, ethPriceData, hasExactFlowFilter]);

  return (
    <div className="flow-chart">
      <h3 className="text-lg font-semibold mb-4">资金流向图 - {token}</h3>
      
      {/* 主图表 */}
      <div ref={chartContainerRef} style={{ position: 'relative', marginBottom: '20px' }} />
      
      {/* 净流出和净流入图表 - 只在非精确流向模式下显示 */}
      {!hasExactFlowFilter && (
        <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
          <div style={{ flex: 1 }}>
            <h4 className="text-md font-medium mb-2">净流出</h4>
            <div ref={netOutflowContainerRef} style={{ position: 'relative' }} />
          </div>
          <div style={{ flex: 1 }}>
            <h4 className="text-md font-medium mb-2">净流入</h4>
            <div ref={netInflowContainerRef} style={{ position: 'relative' }} />
          </div>
        </div>
      )}
    </div>
  );
} 