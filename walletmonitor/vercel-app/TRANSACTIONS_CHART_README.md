# Transaction Chart Page Feature Description

## Overview
Added a new transaction chart page (`/transactions-chart`) that uses TradingView Lightweight Charts bar charts to visualize transaction data.

## Features

### 1. TradingView Bar Charts
- **Bar Chart Display**: Uses TradingView's HistogramSeries to display transaction volume
- **Line Chart Display**: Uses LineSeries to display USD value changes
- **Multi-Token Support**: Different tokens are distinguished by different colors
- **Time Axis**: Supports time range selection and time axis zooming
- **Interactive Charts**: Supports mouse hover, zoom, pan, and other operations

### 2. Data Filters
- **Sender Wallet Selector**: Can select specific sender wallets for filtering
- **Receiver Wallet Selector**: Can select specific receiver wallets for filtering
- **Time Range Selection**: Supports time ranges such as 1 hour, 6 hours, 24 hours, 7 days, 30 days
- **Real-time Updates**: Charts automatically update when filter conditions change

### 3. Chart Features
- **Hourly Aggregation**: Transaction data is aggregated by hour, each bar represents one hour of transaction volume
- **Dual Y-Axis**: Left side displays USD value, right side displays transaction volume
- **Legend Display**: Automatically generates legend showing color identifiers for different tokens
- **Responsive Design**: Charts automatically adjust based on window size

### 4. Data Statistics Panel
- **Total Transactions**: Displays total number of transactions under filter conditions
- **Total USD Value**: Displays total USD value of all transactions
- **Number of Tokens**: Displays number of token types involved
- **Number of Wallets**: Displays number of unique wallet addresses involved

## Technical Implementation

### Chart Library
- **TradingView Lightweight Charts**: Uses professional financial chart library
- **Bar Chart**: HistogramSeries for displaying transaction volume
- **Line Chart**: LineSeries for displaying USD value trends

### Data Processing
```javascript
// Group data by token
const tokenGroups = {};
data.forEach(tx => {
  const token = tx.token_symbol || 'Unknown';
  if (!tokenGroups[token]) {
    tokenGroups[token] = [];
  }
  tokenGroups[token].push(tx);
});

// Group by time (one bar per hour)
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

### API Calls
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

## Chart Configuration

### Basic Configuration
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

### Bar Chart Series
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

### Line Chart Series
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

## Usage

1. Visit the `/transactions-chart` page
2. Use filters to select specific sender and/or receiver wallets
3. Select time range (1 hour to 30 days)
4. View bar charts displaying transaction volume data
5. View line charts displaying USD value trends
6. Use mouse for chart interactions (zoom, pan, hover to view details)

## Page Navigation
- Added "Transaction Chart" navigation item
- Listed alongside "Fund Flow Chart" and "Transaction Records" pages
- Supports quick switching between pages

## Advantages
- **Professional Charts**: Uses TradingView's professional financial chart library
- **Data Visualization**: Intuitively displays transaction volume and value change trends
- **Strong Interactivity**: Supports multiple chart interaction operations
- **Performance Optimization**: Aggregates data by time to improve chart rendering performance
- **Responsive**: Adapts to different screen sizes
