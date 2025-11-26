import { getLatestData, aggregateByMinutes, generateCSV, formatDataForJSON, generateSummary, formatSummary } from '../utils/latest-data.js';

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    
    // 默认参数：minutes=30, aggregate=true, format=json
    const format = searchParams.get('format') || 'json'; // 默认JSON格式
    const minutes = parseInt(searchParams.get('minutes')) || 30; // 默认30分钟汇总
    const aggregate = searchParams.get('aggregate') !== 'false'; // 默认启用汇总
    
    // 获取数据 - 使用固定的查询时间范围（比如6小时）
    const queryMinutes = 360; // 固定查询6小时的数据
    const result = await getLatestData('in', queryMinutes);
    
    if (!result.success) {
      return Response.json(result, { status: 500 });
    }
    
    // 如果需要汇总
    if (aggregate) {
      // 使用传入的minutes参数作为汇总窗口大小
      const aggregatedData = aggregateByMinutes(result.data, minutes);
      
      if (format === 'csv') {
        const csvContent = generateCSV(aggregatedData, true);
        return new Response(csvContent, {
          headers: {
            'Content-Type': 'text/plain; charset=utf-8'
          }
        });
      } else {
        // JSON格式 - 使用格式化函数
        const formattedResult = formatDataForJSON(aggregatedData, true);
        // 使用原始数据计算汇总统计
        const summary = generateSummary(result.data);
        const formattedSummary = formatSummary(summary);
        
        return Response.json({
          success: true,
          data: formattedResult.data,
          summary: {
            raw: summary,
            formatted: formattedSummary
          },
          total: formattedResult.data.length,
          query: {
            ...result.query,
            aggregate: true,
            aggregateWindow: `${minutes} minutes`,
            queryTimeRange: `${queryMinutes} minutes`
          }
        });
      }
    } else {
      // 原始数据
      if (format === 'csv') {
        const csvContent = generateCSV(result.data, false);
        return new Response(csvContent, {
          headers: {
            'Content-Type': 'text/plain; charset=utf-8'
          }
        });
      } else {
        // JSON格式 - 使用格式化函数
        const formattedResult = formatDataForJSON(result.data, false);
        return Response.json({
          success: true,
          data: formattedResult.data,
          summary: formattedResult.summary,
          total: formattedResult.data.length,
          query: result.query
        });
      }
    }
    
  } catch (error) {
    console.error('Error in latest_in API:', error);
    return Response.json({
      success: false,
      error: error.message,
      data: [],
      total: 0
    }, { status: 500 });
  }
} 