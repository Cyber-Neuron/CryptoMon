import { getFlowData, getAvailableTokens, getAvailableGroups, processFlowDataForChart } from './app/lib/database.js';

async function testDatabaseConnection() {
  //console.log('🧪 测试数据库连接...');
  
  try {
    // 测试获取代币列表
    //console.log('📊 获取可用代币...');
    const tokens = await getAvailableTokens();
    //console.log('✅ 可用代币:', tokens);
    
    // 测试获取组别列表
    //console.log('👥 获取可用组别...');
    const groups = await getAvailableGroups();
    //console.log('✅ 可用组别:', groups);
    
    // 测试获取资金流数据
    if (tokens.length > 0) {
      //console.log('💰 获取资金流数据...');
      const now = Math.floor(Date.now() / 1000);
      const startTime = now - 86400; // 24小时前
      
      const flowData = await getFlowData(
        startTime, 
        now, 
        tokens.slice(0, 1), // 只测试第一个代币
        groups.slice(0, 3)  // 只测试前3个组别
      );
      
      //console.log(`✅ 获取到 ${flowData.length} 条资金流数据`);
      
      if (flowData.length > 0) {
        const chartData = processFlowDataForChart(flowData);
        //console.log(`✅ 处理后的图表数据: ${chartData.length} 条`);
        //console.log('📈 示例数据:', chartData.slice(0, 3));
      }
    }
    
    //console.log('🎉 所有测试通过！');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    console.error('请检查 DATABASE_URL 环境变量是否正确设置');
  }
}

// 运行测试
testDatabaseConnection(); 