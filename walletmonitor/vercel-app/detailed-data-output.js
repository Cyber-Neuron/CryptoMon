// 详细数据输出脚本
import fetch from 'node-fetch';

async function outputDetailedData() {
  console.log('📊 ETF详细数据输出\n');

  try {
    // 获取ETH数据
    console.log('🔍 获取ETH详细数据...');
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
      console.log('✅ ETH数据获取成功\n');
      
      // 输出所有K线数据点
      console.log('📈 所有K线数据点 (共' + ethData.data.klineData.length + '条):');
      console.log('='.repeat(120));
      ethData.data.klineData.forEach((kline, index) => {
        const date = new Date(kline.time * 1000);
        const change = ((kline.close - kline.open) / kline.open * 100).toFixed(2);
        const changeSymbol = change >= 0 ? '📈' : '📉';
        console.log(`${(index + 1).toString().padStart(3)}. ${date.toLocaleDateString()} | 开盘:${kline.open.toString().padStart(8)} | 最高:${kline.high.toString().padStart(8)} | 最低:${kline.low.toString().padStart(8)} | 收盘:${kline.close.toString().padStart(8)} | 成交量:${kline.volume.toLocaleString().padStart(12)} | ${changeSymbol} ${change}%`);
      });
      
      // 输出所有ETF数据点
      if (ethData.data.etfData.length > 0) {
        console.log('\n💰 所有ETF数据点 (共' + ethData.data.etfData.length + '条):');
        console.log('='.repeat(80));
        ethData.data.etfData.forEach((etf, index) => {
          const date = new Date(etf.time * 1000);
          const flowType = etf.netFlow >= 0 ? '流入' : '流出';
          const color = etf.netFlow >= 0 ? '🟢' : '🔴';
          console.log(`${(index + 1).toString().padStart(3)}. ${date.toLocaleDateString()} | ${color} ${Math.abs(etf.netFlow).toString().padStart(8)} ETH | ${flowType}`);
        });
      } else {
        console.log('\n💰 ETF数据点: 暂无数据 (使用模拟数据)');
      }
      
      // 输出宏观事件
      console.log('\n📅 宏观事件列表 (共' + ethData.data.events.length + '个):');
      console.log('='.repeat(60));
      ethData.data.events.forEach((event, index) => {
        const date = new Date(event.time * 1000);
        console.log(`${(index + 1).toString().padStart(2)}. ${date.toLocaleDateString()} | ${event.type.padEnd(8)} | ${event.description}`);
      });
      
      // 输出统计信息
      console.log('\n📊 统计信息:');
      console.log('='.repeat(40));
      console.log(`总ETF净流入: ${ethData.data.totalNetFlow.toLocaleString()} ETH`);
      console.log(`数据点数量: ${ethData.data.dataPoints}`);
      console.log(`K线数据条数: ${ethData.data.klineData.length}`);
      console.log(`ETF数据条数: ${ethData.data.etfData.length}`);
      console.log(`宏观事件数量: ${ethData.data.events.length}`);
      console.log(`数据源: ${ethData.data.dataSource}`);
      console.log(`时间范围: ${new Date(ethData.data.startDate).toLocaleDateString()} 到 ${new Date(ethData.data.endDate).toLocaleDateString()}`);
      
      // 计算价格统计
      const prices = ethData.data.klineData.map(k => k.close);
      const maxPrice = Math.max(...prices);
      const minPrice = Math.min(...prices);
      const avgPrice = prices.reduce((a, b) => a + b, 0) / prices.length;
      const priceChange = ((prices[prices.length - 1] - prices[0]) / prices[0] * 100).toFixed(2);
      
      console.log(`\n价格统计:`);
      console.log(`最高价: ${maxPrice.toFixed(2)}`);
      console.log(`最低价: ${minPrice.toFixed(2)}`);
      console.log(`平均价: ${avgPrice.toFixed(2)}`);
      console.log(`期间涨跌: ${priceChange}%`);
      
    } else {
      console.log('❌ ETH数据获取失败:', ethData.error);
    }

    // 获取BTC数据
    console.log('\n\n🔍 获取BTC详细数据...');
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
      console.log('✅ BTC数据获取成功\n');
      
      // 输出所有K线数据点
      console.log('📈 所有K线数据点 (共' + btcData.data.klineData.length + '条):');
      console.log('='.repeat(120));
      btcData.data.klineData.forEach((kline, index) => {
        const date = new Date(kline.time * 1000);
        const change = ((kline.close - kline.open) / kline.open * 100).toFixed(2);
        const changeSymbol = change >= 0 ? '📈' : '📉';
        console.log(`${(index + 1).toString().padStart(3)}. ${date.toLocaleDateString()} | 开盘:${kline.open.toString().padStart(8)} | 最高:${kline.high.toString().padStart(8)} | 最低:${kline.low.toString().padStart(8)} | 收盘:${kline.close.toString().padStart(8)} | 成交量:${kline.volume.toLocaleString().padStart(12)} | ${changeSymbol} ${change}%`);
      });
      
      // 输出所有ETF数据点
      if (btcData.data.etfData.length > 0) {
        console.log('\n💰 所有ETF数据点 (共' + btcData.data.etfData.length + '条):');
        console.log('='.repeat(80));
        btcData.data.etfData.forEach((etf, index) => {
          const date = new Date(etf.time * 1000);
          const flowType = etf.netFlow >= 0 ? '流入' : '流出';
          const color = etf.netFlow >= 0 ? '🟢' : '🔴';
          console.log(`${(index + 1).toString().padStart(3)}. ${date.toLocaleDateString()} | ${color} ${Math.abs(etf.netFlow).toString().padStart(8)} BTC | ${flowType}`);
        });
      } else {
        console.log('\n💰 ETF数据点: 暂无数据 (使用模拟数据)');
      }
      
      // 输出宏观事件
      if (btcData.data.events.length > 0) {
        console.log('\n📅 宏观事件列表 (共' + btcData.data.events.length + '个):');
        console.log('='.repeat(60));
        btcData.data.events.forEach((event, index) => {
          const date = new Date(event.time * 1000);
          console.log(`${(index + 1).toString().padStart(2)}. ${date.toLocaleDateString()} | ${event.type.padEnd(8)} | ${event.description}`);
        });
      } else {
        console.log('\n📅 宏观事件: 6个月范围内无事件');
      }
      
      // 输出统计信息
      console.log('\n📊 统计信息:');
      console.log('='.repeat(40));
      console.log(`总ETF净流入: ${btcData.data.totalNetFlow.toLocaleString()} BTC`);
      console.log(`数据点数量: ${btcData.data.dataPoints}`);
      console.log(`K线数据条数: ${btcData.data.klineData.length}`);
      console.log(`ETF数据条数: ${btcData.data.etfData.length}`);
      console.log(`宏观事件数量: ${btcData.data.events.length}`);
      console.log(`数据源: ${btcData.data.dataSource}`);
      console.log(`时间范围: ${new Date(btcData.data.startDate).toLocaleDateString()} 到 ${new Date(btcData.data.endDate).toLocaleDateString()}`);
      
      // 计算价格统计
      const prices = btcData.data.klineData.map(k => k.close);
      const maxPrice = Math.max(...prices);
      const minPrice = Math.min(...prices);
      const avgPrice = prices.reduce((a, b) => a + b, 0) / prices.length;
      const priceChange = ((prices[prices.length - 1] - prices[0]) / prices[0] * 100).toFixed(2);
      
      console.log(`\n价格统计:`);
      console.log(`最高价: ${maxPrice.toFixed(2)}`);
      console.log(`最低价: ${minPrice.toFixed(2)}`);
      console.log(`平均价: ${avgPrice.toFixed(2)}`);
      console.log(`期间涨跌: ${priceChange}%`);
      
    } else {
      console.log('❌ BTC数据获取失败:', btcData.error);
    }

    console.log('\n\n🎉 详细数据输出完成！');

  } catch (error) {
    console.error('❌ 输出过程中发生错误:', error.message);
  }
}

// 运行详细数据输出
outputDetailedData(); 