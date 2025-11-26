# 交易图表页面功能说明

## 概述
新增了交易图表页面 (`/transactions-chart`)，使用TradingView Lightweight Charts的柱状图来可视化展示交易数据。

## 功能特性

### 1. TradingView柱状图
- **柱状图展示**: 使用TradingView的HistogramSeries展示交易量
- **线图展示**: 使用LineSeries展示USD价值变化
- **多代币支持**: 不同代币使用不同颜色区分
- **时间轴**: 支持时间范围选择和时间轴缩放
- **交互式图表**: 支持鼠标悬停、缩放、平移等操作

### 2. 数据筛选器
- **发送方钱包选择器**: 可以选择特定的发送方钱包进行筛选
- **接收方钱包选择器**: 可以选择特定的接收方钱包进行筛选
- **时间范围选择**: 支持1小时、6小时、24小时、7天、30天等时间范围
- **实时更新**: 筛选条件改变时图表自动更新

### 3. 图表特性
- **按小时聚合**: 交易数据按小时进行聚合，每个柱代表一小时的交易量
- **双Y轴**: 左侧显示USD价值，右侧显示交易量
- **图例显示**: 自动生成图例，显示不同代币的颜色标识
- **响应式设计**: 图表会根据窗口大小自动调整

### 4. 数据统计面板
- **总交易数**: 显示筛选条件下的总交易数量
- **总USD价值**: 显示所有交易的总美元价值
- **涉及代币数**: 显示涉及的代币种类数量
- **涉及钱包数**: 显示涉及的唯一钱包地址数量

## 技术实现

### 图表库
- **TradingView Lightweight Charts**: 使用专业的金融图表库
- **柱状图**: HistogramSeries用于展示交易量
- **线图**: LineSeries用于展示USD价值趋势

### 数据处理
```javascript
// 按代币分组数据
const tokenGroups = {};
data.forEach(tx => {
  const token = tx.token_symbol || 'Unknown';
  if (!tokenGroups[token]) {
    tokenGroups[token] = [];
  }
  tokenGroups[token].push(tx);
});

// 按时间分组（每小时一个柱）
const hourlyData = {};
txs.forEach(tx => {
  const hour = Math.floor(tx.timestamp / 3600) * 3600;
  if (!hourlyData[hour]) {
    hourlyData[hour] = {
      volume: 0,
      count: 0,
      totalValue: 0
    };
  }
  hourlyData[hour].volume += parseFloat(tx.amount) || 0;
  hourlyData[hour].count += 1;
  hourlyData[hour].totalValue += parseFloat(tx.usd_value) || 0;
});
```

### API调用
```javascript
const params = new URLSearchParams({
  limit: '10000',
  offset: '0',
  startTime: startTime.toString(),
  endTime: now.toString()
});

if (selectedFromWallet) {
  params.append('fromWalletId', selectedFromWallet);
}
if (selectedToWallet) {
  params.append('toWalletId', selectedToWallet);
}
```

## 图表配置

### 基础配置
```javascript
const chart = createChart(container, {
  width: container.clientWidth,
  height: 500,
  layout: {
    background: { color: '#ffffff' },
    textColor: '#333',
  },
  grid: {
    vertLines: { color: '#f0f0f0' },
    horzLines: { color: '#f0f0f0' },
  },
  timeScale: {
    timeVisible: true,
    secondsVisible: false,
  },
  rightPriceScale: {
    borderColor: '#cccccc',
  },
  leftPriceScale: {
    borderColor: '#cccccc',
  },
});
```

### 柱状图系列
```javascript
const volumeSeries = chart.addHistogramSeries({
  name: `${token} Volume`,
  color: index % 2 === 0 ? '#3B82F6' : '#10B981',
  priceFormat: {
    type: 'volume',
  },
  priceScaleId: index === 0 ? 'right' : `right-${index}`,
});
```

### 线图系列
```javascript
const valueSeries = chart.addLineSeries({
  name: `${token} USD Value`,
  color: index % 2 === 0 ? '#EF4444' : '#F59E0B',
  priceFormat: {
    type: 'price',
    precision: 2,
  },
  priceScaleId: `left-${index}`,
});
```

## 使用方法
1. 访问 `/transactions-chart` 页面
2. 使用筛选器选择特定的发送方和/或接收方钱包
3. 选择时间范围（1小时到30天）
4. 查看柱状图展示的交易量数据
5. 查看线图展示的USD价值趋势
6. 使用鼠标进行图表交互（缩放、平移、悬停查看详情）

## 页面导航
- 新增了"交易图表"导航项
- 与"资金流向图"和"交易记录"页面并列
- 支持页面间的快速切换

## 优势
- **专业图表**: 使用TradingView的专业金融图表库
- **数据可视化**: 直观展示交易量和价值变化趋势
- **交互性强**: 支持多种图表交互操作
- **性能优化**: 按时间聚合数据，提高图表渲染性能
- **响应式**: 适配不同屏幕尺寸 