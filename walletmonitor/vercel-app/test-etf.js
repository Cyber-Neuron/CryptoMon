// ETF功能测试脚本
import fetch from 'node-fetch';

async function testETFAPI() {
  console.log('🧪 测试ETF API功能...\n');

  try {
    // 测试ETH数据
    console.log('1. 测试ETH ETF数据获取...');
    const ethResponse = await fetch('http://localhost:3000/api/etf-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        asset: 'ETH',
        timeRange: '1y'
      })
    });

    const ethData = await ethResponse.json();
    
    if (ethData.success) {
      console.log('✅ ETH数据获取成功');
      console.log(`   - 数据点数量: ${ethData.data.dataPoints}`);
      console.log(`   - K线数据: ${ethData.data.klineData.length} 条`);
      console.log(`   - ETF数据: ${ethData.data.etfData.length} 条`);
      console.log(`   - 宏观事件: ${ethData.data.events.length} 个`);
      console.log(`   - 数据源: ${ethData.data.dataSource}`);
      
      // 输出前10个K线数据点
      console.log('\n📊 前10个K线数据点:');
      ethData.data.klineData.slice(0, 10).forEach((kline, index) => {
        const date = new Date(kline.time * 1000);
        console.log(`   ${index + 1}. ${date.toLocaleDateString()} - 开盘:${kline.open} 最高:${kline.high} 最低:${kline.low} 收盘:${kline.close} 成交量:${kline.volume.toLocaleString()}`);
      });
      
      // 输出前10个ETF数据点
      if (ethData.data.etfData.length > 0) {
        console.log('\n💰 前10个ETF数据点:');
        ethData.data.etfData.slice(0, 10).forEach((etf, index) => {
          const date = new Date(etf.time * 1000);
          const flowType = etf.netFlow >= 0 ? '流入' : '流出';
          const color = etf.netFlow >= 0 ? '🟢' : '🔴';
          console.log(`   ${index + 1}. ${date.toLocaleDateString()} - ${color} ${Math.abs(etf.netFlow).toLocaleString()} ETH (${flowType})`);
        });
      }
      
      // 输出宏观事件
      if (ethData.data.events.length > 0) {
        console.log('\n📅 宏观事件列表:');
        ethData.data.events.forEach((event, index) => {
          const date = new Date(event.time * 1000);
          console.log(`   ${index + 1}. ${date.toLocaleDateString()} - ${event.type} (${event.description})`);
        });
      }
      
      // 输出统计信息
      console.log('\n📈 统计信息:');
      console.log(`   - 总ETF净流入: ${ethData.data.totalNetFlow.toLocaleString()} ETH`);
      console.log(`   - 时间范围: ${new Date(ethData.data.startDate).toLocaleDateString()} 到 ${new Date(ethData.data.endDate).toLocaleDateString()}`);
      
    } else {
      console.log('❌ ETH数据获取失败:', ethData.error);
    }

    // 测试BTC数据
    console.log('\n2. 测试BTC ETF数据获取...');
    const btcResponse = await fetch('http://localhost:3000/api/etf-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        asset: 'BTC',
        timeRange: '6m'
      })
    });

    const btcData = await btcResponse.json();
    
    if (btcData.success) {
      console.log('✅ BTC数据获取成功');
      console.log(`   - 数据点数量: ${btcData.data.dataPoints}`);
      console.log(`   - K线数据: ${btcData.data.klineData.length} 条`);
      console.log(`   - ETF数据: ${btcData.data.etfData.length} 条`);
      console.log(`   - 宏观事件: ${btcData.data.events.length} 个`);
      console.log(`   - 数据源: ${btcData.data.dataSource}`);
      
      // 输出前10个K线数据点
      console.log('\n📊 前10个K线数据点:');
      btcData.data.klineData.slice(0, 10).forEach((kline, index) => {
        const date = new Date(kline.time * 1000);
        console.log(`   ${index + 1}. ${date.toLocaleDateString()} - 开盘:${kline.open} 最高:${kline.high} 最低:${kline.low} 收盘:${kline.close} 成交量:${kline.volume.toLocaleString()}`);
      });
      
      // 输出前10个ETF数据点
      if (btcData.data.etfData.length > 0) {
        console.log('\n💰 前10个ETF数据点:');
        btcData.data.etfData.slice(0, 10).forEach((etf, index) => {
          const date = new Date(etf.time * 1000);
          const flowType = etf.netFlow >= 0 ? '流入' : '流出';
          const color = etf.netFlow >= 0 ? '🟢' : '🔴';
          console.log(`   ${index + 1}. ${date.toLocaleDateString()} - ${color} ${Math.abs(etf.netFlow).toLocaleString()} BTC (${flowType})`);
        });
      }
      
      // 输出宏观事件
      if (btcData.data.events.length > 0) {
        console.log('\n📅 宏观事件列表:');
        btcData.data.events.forEach((event, index) => {
          const date = new Date(event.time * 1000);
          console.log(`   ${index + 1}. ${date.toLocaleDateString()} - ${event.type} (${event.description})`);
        });
      }
      
      // 输出统计信息
      console.log('\n📈 统计信息:');
      console.log(`   - 总ETF净流入: ${btcData.data.totalNetFlow.toLocaleString()} BTC`);
      console.log(`   - 时间范围: ${new Date(btcData.data.startDate).toLocaleDateString()} 到 ${new Date(btcData.data.endDate).toLocaleDateString()}`);
      
    } else {
      console.log('❌ BTC数据获取失败:', btcData.error);
    }

    // 测试错误参数
    console.log('\n3. 测试错误参数处理...');
    const errorResponse = await fetch('http://localhost:3000/api/etf-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        asset: 'INVALID',
        timeRange: '1y'
      })
    });

    const errorData = await errorResponse.json();
    
    if (!errorData.success) {
      console.log('✅ 错误参数处理正确:', errorData.error);
    } else {
      console.log('❌ 错误参数处理失败');
    }

    console.log('\n🎉 ETF功能测试完成！');
    console.log('\n📊 访问以下地址查看可视化效果:');
    console.log('   - ETF分析页面: http://localhost:3000/etf');
    console.log('   - 主页面: http://localhost:3000');

  } catch (error) {
    console.error('❌ 测试过程中发生错误:', error.message);
  }
}

// 运行测试
testETFAPI(); 