import { getFlowData, processFlowDataForChart } from '../../lib/database.js';

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    
    const startTime = searchParams.get('startTime') ? parseInt(searchParams.get('startTime')) : undefined;
    const endTime = searchParams.get('endTime') ? parseInt(searchParams.get('endTime')) : undefined;
    const tokens = searchParams.get('tokens') ? searchParams.get('tokens').split(',') : undefined;
    const groups = searchParams.get('groups') ? searchParams.get('groups').split(',') : undefined;
    
    const flowData = await getFlowData(startTime, endTime, tokens, groups);
    const chartData = processFlowDataForChart(flowData);
    
    return Response.json({
      success: true,
      data: chartData,
      total: chartData.length
    });
  } catch (error) {
    console.error('Error fetching flow data:', error);
    return Response.json(
      { success: false, error: 'Failed to fetch flow data' },
      { status: 500 }
    );
  }
}

export async function POST(request) {
  try {
    const body = await request.json();
    const { startTime, endTime, tokens, groups, fromGroups, toGroups } = body;
    
    const flowData = await getFlowData(startTime, endTime, tokens, groups, fromGroups, toGroups);
    const chartData = processFlowDataForChart(flowData, groups, fromGroups, toGroups);
    
    return Response.json({
      success: true,
      data: chartData,
      rawFlowData: flowData,
      total: chartData.length
    });
  } catch (error) {
    console.error('Error fetching flow data:', error);
    return Response.json(
      { success: false, error: 'Failed to fetch flow data' },
      { status: 500 }
    );
  }
} 