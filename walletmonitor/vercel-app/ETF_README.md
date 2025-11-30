# ETF Flow Analysis Feature

## Feature Overview

The ETF flow analysis page provides correlation analysis between cryptocurrency ETF net inflows and price trends, helping users understand the impact of macro events on the cryptocurrency market.

## Main Features

### 1. Macro Event Markers
- **FOMC Meetings**: Federal Reserve interest rate meetings, affecting market rate expectations
- **Non-Farm Payroll Data**: US non-farm employment changes, reflecting economic conditions
- **CPI Data**: Consumer Price Index, measuring inflation levels
- **PPI Data**: Producer Price Index
- **GDP Data**: Gross Domestic Product

### 2. ETF Net Inflow Data
- Supports ETH and BTC ETF data
- Displays daily net inflow/outflow
- Positive values indicate net inflow, negative values indicate net outflow
- Data source: Farside.co.uk

### 3. Price Candlestick Charts
- Uses Binance API to fetch real-time price data
- Displays open, high, low, and close prices
- Supports 6 months, 1 year, and 2 year time ranges

### 4. Visualization Analysis
- Combined chart display: Candlestick chart + ETF net inflow bar chart
- Macro event vertical marker lines
- Statistics information panel
- Responsive design

## Technical Implementation

### Frontend Components
- `ETFChart.jsx`: Main chart component, using lightweight-charts library
- `page.jsx`: ETF analysis page, containing control panel and data display

### Backend API
- `/api/etf-data`: Fetches ETF data, price data, and macro events
- Supports real data fetching and simulated data fallback

### Data Sources
1. **ETF Data**: Farside.co.uk API
2. **Price Data**: Binance public API
3. **Macro Events**: Predefined key event time points

## Usage

1. Visit the `/etf` page
2. Select asset type (ETH or BTC)
3. Select time range (6 months, 1 year, 2 years)
4. View charts and statistics
5. Analyze the impact of macro events on prices and ETF flows

## Chart Description

### Chart Elements
- **Candlestick Chart**: Displays price trends (green for up, red for down)
- **Bar Chart**: Displays ETF net inflow (green for inflow, red for outflow)
- **Vertical Lines**: Mark macro event occurrence times

### Statistics
- Total ETF net inflow
- Maximum single-day inflow
- Maximum single-day outflow
- Number of macro events

## Data Updates

- ETF Data: Updated daily
- Price Data: Updated in real-time
- Macro Events: Manually maintained

## Notes

1. Real data fetching may be subject to API limitations, will automatically fallback to simulated data
2. Macro event time points need to be updated regularly
3. Chart performance optimization supports displaying large amounts of data points

## Future Improvements

1. Add more macro event types
2. Support more time periods (weekly, monthly)
3. Add technical indicator overlays
4. Support data export functionality
5. Add event impact analysis reports
