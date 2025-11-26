import { NextResponse } from 'next/server';
import axios from 'axios';
import * as cheerio from 'cheerio';
import { readFileSync } from 'fs';
import { join } from 'path';

// 宏观事件数据（过去一年的关键事件）
const MACRO_EVENTS = {
  '2024-01-31': { type: 'FOMC', description: '美联储议息会议' },
  '2024-02-02': { type: 'NonFarm', description: '非农就业数据' },
  '2024-02-13': { type: 'CPI', description: '消费者物价指数' },
  '2024-03-20': { type: 'FOMC', description: '美联储议息会议' },
  '2024-04-05': { type: 'NonFarm', description: '非农就业数据' },
  '2024-04-10': { type: 'CPI', description: '消费者物价指数' },
  '2024-05-01': { type: 'FOMC', description: '美联储议息会议' },
  '2024-05-03': { type: 'NonFarm', description: '非农就业数据' },
  '2024-05-15': { type: 'CPI', description: '消费者物价指数' },
  '2024-06-07': { type: 'NonFarm', description: '非农就业数据' },
  '2024-06-12': { type: 'FOMC', description: '美联储议息会议' },
  '2024-06-13': { type: 'CPI', description: '消费者物价指数' }, // 修复重复日期
  '2024-07-05': { type: 'NonFarm', description: '非农就业数据' },
  '2024-07-31': { type: 'FOMC', description: '美联储议息会议' },
  '2024-08-02': { type: 'NonFarm', description: '非农就业数据' },
  '2024-08-14': { type: 'CPI', description: '消费者物价指数' },
  '2024-09-06': { type: 'NonFarm', description: '非农就业数据' },
  '2024-09-18': { type: 'FOMC', description: '美联储议息会议' },
  '2024-10-04': { type: 'NonFarm', description: '非农就业数据' },
  '2024-10-10': { type: 'CPI', description: '消费者物价指数' },
  '2024-11-01': { type: 'NonFarm', description: '非农就业数据' },
  '2024-11-07': { type: 'FOMC', description: '美联储议息会议' },
  '2024-12-06': { type: 'NonFarm', description: '非农就业数据' },
  '2024-12-12': { type: 'CPI', description: '消费者物价指数' },
  '2024-12-18': { type: 'FOMC', description: '美联储议息会议' },

  // ✅ 以下为 2025 年新增
  '2025-01-03': { type: 'NonFarm', description: '非农就业数据' },
  '2025-01-15': { type: 'CPI', description: '消费者物价指数' },
  '2025-01-29': { type: 'FOMC', description: '美联储议息会议' },
  '2025-02-07': { type: 'NonFarm', description: '非农就业数据' },
  '2025-02-13': { type: 'CPI', description: '消费者物价指数' },
  '2025-03-07': { type: 'NonFarm', description: '非农就业数据' },
  '2025-03-12': { type: 'CPI', description: '消费者物价指数' },
  '2025-03-19': { type: 'FOMC', description: '美联储议息会议' },
  '2025-04-04': { type: 'NonFarm', description: '非农就业数据' },
  '2025-04-10': { type: 'CPI', description: '消费者物价指数' },
  '2025-04-30': { type: 'FOMC', description: '美联储议息会议' },
  '2025-05-02': { type: 'NonFarm', description: '非农就业数据' },
  '2025-05-14': { type: 'CPI', description: '消费者物价指数' },
  '2025-06-06': { type: 'NonFarm', description: '非农就业数据' },
  '2025-06-11': { type: 'CPI', description: '消费者物价指数' },
  '2025-06-18': { type: 'FOMC', description: '美联储议息会议' },
  '2025-07-03': { type: 'NonFarm', description: '非农就业数据' },
  '2025-07-16': { type: 'CPI', description: '消费者物价指数' },
  '2025-07-30': { type: 'FOMC', description: '美联储议息会议' },
  '2025-08-02': { type: 'NonFarm', description: '非农就业数据' },  // 暂定
  '2025-08-13': { type: 'CPI', description: '消费者物价指数' },
  '2025-09-05': { type: 'NonFarm', description: '非农就业数据' },
  '2025-09-17': { type: 'FOMC', description: '美联储议息会议' },
  '2025-09-11': { type: 'CPI', description: '消费者物价指数' },
  '2025-10-03': { type: 'NonFarm', description: '非农就业数据' },
  '2025-10-15': { type: 'CPI', description: '消费者物价指数' },
  '2025-11-07': { type: 'NonFarm', description: '非农就业数据' },
  '2025-11-05': { type: 'FOMC', description: '美联储议息会议' },
  '2025-11-13': { type: 'CPI', description: '消费者物价指数' },
  '2025-12-05': { type: 'NonFarm', description: '非农就业数据' },
  '2025-12-10': { type: 'CPI', description: '消费者物价指数' },
  '2025-12-17': { type: 'FOMC', description: '美联储议息会议' },
};


// 获取真实的ETF数据
async function getRealETFData(asset, timeRange) {
  try {
    console.log(`Reading real ETF data for ${asset} from CSV file`);
    
    // 根据资产类型选择CSV文件
    let csvFileName;
    if (asset === 'ETH') {
      csvFileName = 'eth_etf.csv';
    } else {
      // 对于BTC，我们可以使用类似的模式或者返回null
      console.log('BTC ETF data not available in CSV, using realistic pattern data');
      return null;
    }

    // 读取CSV文件
    const csvPath = join(process.cwd(), csvFileName);
    const csvContent = readFileSync(csvPath, 'utf-8');
    
    console.log(`Successfully read CSV file: ${csvFileName}`);
    
    // 解析CSV数据
    const lines = csvContent.split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    
    console.log('CSV headers:', headers);
    
    const etfData = [];
    
    // 从第二行开始解析数据（跳过标题行）
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;
      
      const values = line.split(',').map(v => v.trim());
      
      // 确保有足够的列
      if (values.length < headers.length) continue;
      
      const dateStr = values[0]; // 第一列是日期
      const totalFlowStr = values[values.length - 1]; // 最后一列是Total
      
      // 跳过标题行和无效数据
      if (dateStr === 'Date' || dateStr === 'Total' || dateStr === '-') continue;
      
      // 解析日期
      const date = new Date(dateStr);
      if (isNaN(date.getTime())) {
        console.log(`Invalid date: ${dateStr}`);
        continue;
      }
      
      // 解析总流量数据
      const totalFlow = parseFloat(totalFlowStr);
      if (isNaN(totalFlow)) {
        console.log(`Invalid total flow: ${totalFlowStr}`);
        continue;
      }
      
      etfData.push({
        time: Math.floor(date.getTime() / 1000),
        netFlow: totalFlow,
        date: date.toISOString().split('T')[0],
        realData: true
      });
    }

    console.log(`Successfully parsed ${etfData.length} ETF data points from CSV`);
    
    // 按时间排序
    etfData.sort((a, b) => a.time - b.time);
    
    if (etfData.length > 0) {
      console.log(`Sample data:`, etfData.slice(0, 3));
      console.log(`Date range: ${etfData[0].date} to ${etfData[etfData.length - 1].date}`);
    }

    return etfData;
  } catch (error) {
    console.error('Error reading ETF data from CSV:', error);
    return null;
  }
}

// 获取币安K线数据
async function getBinanceKlineData(asset, timeRange) {
  try {
    const symbol = asset === 'ETH' ? 'ETHUSDT' : 'BTCUSDT';
    const interval = '1d';
    
    // 计算开始时间
    const now = new Date();
    const startDate = new Date();
    
    switch (timeRange) {
      case '6m':
        startDate.setMonth(now.getMonth() - 6);
        break;
      case '1y':
        startDate.setFullYear(now.getFullYear() - 1);
        break;
      case '2y':
        startDate.setFullYear(now.getFullYear() - 2);
        break;
      default:
        startDate.setFullYear(now.getFullYear() - 1);
    }

    const startTime = startDate.getTime();
    const endTime = now.getTime();
    
    const url = `https://api.binance.com/api/v3/klines?symbol=${symbol}&interval=${interval}&startTime=${startTime}&endTime=${endTime}&limit=1000`;
    
    const response = await axios.get(url);
    if (response.status !== 200) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = response.data;
    
    return data.map(kline => ({
      time: Math.floor(kline[0] / 1000), // 转换为秒
      open: parseFloat(kline[1]),
      high: parseFloat(kline[2]),
      low: parseFloat(kline[3]),
      close: parseFloat(kline[4]),
      volume: parseFloat(kline[5])
    }));
  } catch (error) {
    console.error('Error fetching Binance data:', error);
    return null;
  }
}

// 模拟ETF数据获取函数（备用方案）
async function getMockETFData(asset, timeRange) {
  const now = new Date();
  const startDate = new Date();
  
  switch (timeRange) {
    case '6m':
      startDate.setMonth(now.getMonth() - 6);
      break;
    case '1y':
      startDate.setFullYear(now.getFullYear() - 1);
      break;
    case '2y':
      startDate.setFullYear(now.getFullYear() - 2);
      break;
    default:
      startDate.setFullYear(now.getFullYear() - 1);
  }

  const days = Math.ceil((now - startDate) / (1000 * 60 * 60 * 24));
  const etfData = [];
  const klineData = [];

  for (let i = 0; i < days; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);
    const timestamp = Math.floor(date.getTime() / 1000);

    // 模拟ETF净流入数据（正值表示流入，负值表示流出）
    const baseFlow = asset === 'ETH' ? 1000 : 500;
    const randomFlow = (Math.random() - 0.5) * baseFlow * 2;
    const netFlow = Math.round(randomFlow);

    // 模拟K线数据
    const basePrice = asset === 'ETH' ? 3000 : 45000;
    const priceChange = (Math.random() - 0.5) * 0.1; // ±5% 价格变化
    const open = basePrice * (1 + priceChange);
    const close = open * (1 + (Math.random() - 0.5) * 0.05);
    const high = Math.max(open, close) * (1 + Math.random() * 0.03);
    const low = Math.min(open, close) * (1 - Math.random() * 0.03);
    const volume = Math.random() * 1000000 + 500000;

    etfData.push({
      time: timestamp,
      netFlow: netFlow,
      date: date.toISOString().split('T')[0]
    });

    klineData.push({
      time: timestamp,
      open: parseFloat(open.toFixed(2)),
      high: parseFloat(high.toFixed(2)),
      low: parseFloat(low.toFixed(2)),
      close: parseFloat(close.toFixed(2)),
      volume: parseFloat(volume.toFixed(0))
    });
  }

  return { etfData, klineData };
}

// 获取宏观事件数据
function getMacroEvents(startDate, endDate) {
  const events = [];
  
  Object.entries(MACRO_EVENTS).forEach(([dateStr, event]) => {
    const eventDate = new Date(dateStr);
    if (eventDate >= startDate && eventDate <= endDate) {
      events.push({
        time: Math.floor(eventDate.getTime() / 1000),
        date: dateStr,
        type: event.type,
        description: event.description
      });
    }
  });

  return events.sort((a, b) => a.time - b.time);
}

export async function POST(request) {
  try {
    const { asset = 'ETH', timeRange = '1y' } = await request.json();

    // 验证参数
    if (!['ETH', 'BTC'].includes(asset)) {
      return NextResponse.json({
        success: false,
        error: '不支持的资产类型'
      }, { status: 400 });
    }

    if (!['6m', '1y', '2y'].includes(timeRange)) {
      return NextResponse.json({
        success: false,
        error: '不支持的时间范围'
      }, { status: 400 });
    }

    // 计算时间范围
    const now = new Date();
    const startDate = new Date();
    
    switch (timeRange) {
      case '6m':
        startDate.setMonth(now.getMonth() - 6);
        break;
      case '1y':
        startDate.setFullYear(now.getFullYear() - 1);
        break;
      case '2y':
        startDate.setFullYear(now.getFullYear() - 2);
        break;
    }

    // 尝试获取真实数据
    let etfData = await getRealETFData(asset, timeRange);
    let klineData = await getBinanceKlineData(asset, timeRange);

    console.log('Data fetch status:', {
      etfDataSuccess: !!etfData,
      etfDataLength: etfData?.length || 0,
      klineDataSuccess: !!klineData,
      klineDataLength: klineData?.length || 0
    });

    // 如果真实数据获取失败，使用模拟数据
    if (!etfData || !klineData) {
      console.log('Using realistic pattern data due to API failure');
      const mockData = await getMockETFData(asset, timeRange);
      etfData = mockData.etfData;
      klineData = mockData.klineData;
    }

    // 过滤时间范围内的数据
    const startTimestamp = Math.floor(startDate.getTime() / 1000);
    etfData = etfData.filter(item => item.time >= startTimestamp);
    klineData = klineData.filter(item => item.time >= startTimestamp);

    // 获取宏观事件
    const events = getMacroEvents(startDate, now);

    // 计算统计信息
    const totalNetFlow = etfData.reduce((sum, item) => sum + item.netFlow, 0);

    const responseData = {
      asset,
      timeRange,
      etfData,
      klineData,
      events,
      totalNetFlow,
      dataPoints: etfData.length,
      startDate: startDate.toISOString(),
      endDate: now.toISOString(),
      dataSource: etfData.length > 0 && etfData[0].hasOwnProperty('realData') ? 'farside.co.uk' : 'realistic-pattern'
    };

    return NextResponse.json({
      success: true,
      data: responseData
    });

  } catch (error) {
    console.error('ETF data API error:', error);
    return NextResponse.json({
      success: false,
      error: '服务器内部错误'
    }, { status: 500 });
  }
} 