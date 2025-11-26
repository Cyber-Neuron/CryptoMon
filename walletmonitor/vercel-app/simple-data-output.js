// 简化数据输出脚本
import fetch from 'node-fetch';

async function outputSimpleData() {
  console.log('📊 ETF数据点输出\n');

  try {
    // 获取ETH数据
    console.log('🔍 ETH数据 (1年):');
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
      console.log(`✅ 数据获取成功 - 共${ethData.data.klineData.length}个K线数据点`);
      
      // 显示前5个和后5个数据点
      console.log('\n📈 K线数据点 (前5个):');
      ethData.data.klineData.slice(0, 5).forEach((kline, index) => {
        const date = new Date(kline.time * 1000);
        const change = ((kline.close - kline.open) / kline.open * 100).toFixed(2);
        console.log(`   ${index + 1}. ${date.toLocaleDateString()} | 开盘:${kline.open} | 收盘:${kline.close} | 涨跌:${change}%`);
      });
      
      console.log('\n📈 K线数据点 (后5个):');
      ethData.data.klineData.slice(-5).forEach((kline, index) => {
        const date = new Date(kline.time * 1000);
        const change = ((kline.close - kline.open) / kline.open * 100).toFixed(2);
        console.log(`   ${index + 1}. ${date.toLocaleDateString()} | 开盘:${kline.open} | 收盘:${kline.close} | 涨跌:${change}%`);
      });
      
      // 显示ETF数据点
      if (ethData.data.etfData.length > 0) {
        console.log('\n💰 ETF数据点 (前5个):');
        ethData.data.etfData.slice(0, 5).forEach((etf, index) => {
          const date = new Date(etf.time * 1000);
          const flowType = etf.netFlow >= 0 ? '流入' : '流出';
          console.log(`   ${index + 1}. ${date.toLocaleDateString()} | ${Math.abs(etf.netFlow)} ETH | ${flowType}`);
        });
      } else {
        console.log('\n💰 ETF数据点: 暂无数据 (使用模拟数据)');
      }
      
      // 显示宏观事件
      console.log('\n📅 宏观事件 (前5个):');
      ethData.data.events.slice(0, 5).forEach((event, index) => {
        const date = new Date(event.time * 1000);
        console.log(`   ${index + 1}. ${date.toLocaleDateString()} | ${event.type} | ${event.description}`);
      });
      
      // 显示统计信息
      const prices = ethData.data.klineData.map(k => k.close);
      const maxPrice = Math.max(...prices);
      const minPrice = Math.min(...prices);
      const priceChange = ((prices[prices.length - 1] - prices[0]) / prices[0] * 100).toFixed(2);
      
      console.log('\n📊 统计信息:');
      console.log(`   最高价: ${maxPrice.toFixed(2)}`);
      console.log(`   最低价: ${minPrice.toFixed(2)}`);
      console.log(`   期间涨跌: ${priceChange}%`);
      console.log(`   宏观事件: ${ethData.data.events.length}个`);
      console.log(`   数据源: ${ethData.data.dataSource}`);
    }

    // 获取BTC数据
    console.log('\n\n🔍 BTC数据 (6个月):');
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
      console.log(`✅ 数据获取成功 - 共${btcData.data.klineData.length}个K线数据点`);
      
      // 显示前5个和后5个数据点
      console.log('\n📈 K线数据点 (前5个):');
      btcData.data.klineData.slice(0, 5).forEach((kline, index) => {
        const date = new Date(kline.time * 1000);
        const change = ((kline.close - kline.open) / kline.open * 100).toFixed(2);
        console.log(`   ${index + 1}. ${date.toLocaleDateString()} | 开盘:${kline.open} | 收盘:${kline.close} | 涨跌:${change}%`);
      });
      
      console.log('\n📈 K线数据点 (后5个):');
      btcData.data.klineData.slice(-5).forEach((kline, index) => {
        const date = new Date(kline.time * 1000);
        const change = ((kline.close - kline.open) / kline.open * 100).toFixed(2);
        console.log(`   ${index + 1}. ${date.toLocaleDateString()} | 开盘:${kline.open} | 收盘:${kline.close} | 涨跌:${change}%`);
      });
      
      // 显示ETF数据点
      if (btcData.data.etfData.length > 0) {
        console.log('\n💰 ETF数据点 (前5个):');
        btcData.data.etfData.slice(0, 5).forEach((etf, index) => {
          const date = new Date(etf.time * 1000);
          const flowType = etf.netFlow >= 0 ? '流入' : '流出';
          console.log(`   ${index + 1}. ${date.toLocaleDateString()} | ${Math.abs(etf.netFlow)} BTC | ${flowType}`);
        });
      } else {
        console.log('\n💰 ETF数据点: 暂无数据 (使用模拟数据)');
      }
      
      // 显示宏观事件
      if (btcData.data.events.length > 0) {
        console.log('\n📅 宏观事件 (前5个):');
        btcData.data.events.slice(0, 5).forEach((event, index) => {
          const date = new Date(event.time * 1000);
          console.log(`   ${index + 1}. ${date.toLocaleDateString()} | ${event.type} | ${event.description}`);
        });
      } else {
        console.log('\n📅 宏观事件: 6个月范围内无事件');
      }
      
      // 显示统计信息
      const prices = btcData.data.klineData.map(k => k.close);
      const maxPrice = Math.max(...prices);
      const minPrice = Math.min(...prices);
      const priceChange = ((prices[prices.length - 1] - prices[0]) / prices[0] * 100).toFixed(2);
      
      console.log('\n📊 统计信息:');
      console.log(`   最高价: ${maxPrice.toFixed(2)}`);
      console.log(`   最低价: ${minPrice.toFixed(2)}`);
      console.log(`   期间涨跌: ${priceChange}%`);
      console.log(`   宏观事件: ${btcData.data.events.length}个`);
      console.log(`   数据源: ${btcData.data.dataSource}`);
    }

    console.log('\n\n🎉 数据点输出完成！');

  } catch (error) {
    console.error('❌ 输出过程中发生错误:', error.message);
  }
}

// 运行简化数据输出
outputSimpleData(); 