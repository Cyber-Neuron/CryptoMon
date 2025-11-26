# Fund Flow Monitoring Dashboard Deployment Guide

## Overview

This is a fund inflow/outflow visualization tool based on TradingView Lightweight Charts that can be deployed to the Vercel platform.

## Features

- 📊 Use TradingView Lightweight Charts to draw fund flow bar charts
- 🕒 Support multiple time ranges: 1 hour, 6 hours, 24 hours, 7 days, 30 days
- 🪙 Display charts separately by different tokens
- 👥 Group display by from_grp_name and to_grp_name
- 📈 Positive values represent fund inflow, negative values represent fund outflow
- 🎨 Modern responsive UI design

## Deployment Steps

### 1. Prepare Database

Ensure your PostgreSQL database is running and contains the following table structure:

```sql
-- Fund flow data table
CREATE TABLE IF NOT EXISTS ex_flows (
    id BIGSERIAL PRIMARY KEY,
    timestamp BIGINT NOT NULL,
    token VARCHAR(20) NOT NULL,
    chain_id BIGINT REFERENCES chains(id),
    from_grp_name VARCHAR(100),
    to_grp_name VARCHAR(100),
    amount NUMERIC(30, 18),
    usd_value NUMERIC(30, 2),
    tx_hash VARCHAR(66),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tx_hash, token)
);
```

### 2. Local Testing

1. Enter application directory:
```bash
cd walletmonitor/vercel-app
```

2. Install dependencies:
```bash
npm install
```

3. Set environment variables (create `.env.local` file):
```bash
DATABASE_URL=postgresql://username:password@host:port/database
```

4. Test database connection:
```bash
node test-local.js
```

5. Start development server:
```bash
npm run dev
```

6. Visit http://localhost:3000 to view the application

### 3. Deploy to Vercel

#### Method 1: Use Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Run deployment script:
```bash
cd walletmonitor
./deploy-to-vercel.sh
```

#### Method 2: Deploy via GitHub

1. Push code to GitHub repository

2. Visit [Vercel Dashboard](https://vercel.com/dashboard)

3. Click "New Project"

4. Import your GitHub repository

5. Configure environment variables:
   - `DATABASE_URL`: Your PostgreSQL connection string

6. Click "Deploy"

### 4. Configure Environment Variables

Configure the following environment variables in Vercel project settings:

- `DATABASE_URL`: PostgreSQL database connection string
  - Format: `postgresql://username:password@host:port/database`
  - Production environment recommended to use SSL connection

### 5. Verify Deployment

1. Visit your Vercel application URL
2. Check if page loads normally
3. Test data query functionality
4. Verify chart display

## Database Connection Configuration

### Local Development
```bash
DATABASE_URL=postgresql://localhost:5432/walletmonitor
```

### Production Environment (Vercel)
```bash
DATABASE_URL=postgresql://username:password@host:port/database?sslmode=require
```

## Common Issues

### 1. Database Connection Failed
- Check if `DATABASE_URL` is correct
- Confirm database server is accessible
- Verify username and password are correct

### 2. Charts Not Displaying Data
- Check if `ex_flows` table exists in database
- Confirm if table has data
- Check time range settings

### 3. Deployment Failed
- Check if dependencies in `package.json` are correct
- Confirm all files are committed to Git repository
- View Vercel build logs

### 4. Performance Issues
- Consider adding database indexes
- Optimize query statements
- Use connection pool

## Custom Configuration

### Modify Time Range
Modify time range options in `app/page.jsx`:

```javascript
const timeRanges = [
  { value: '1h', label: 'Last 1 Hour' },
  { value: '6h', label: 'Last 6 Hours' },
  { value: '24h', label: 'Last 24 Hours' },
  { value: '7d', label: 'Last 7 Days' },
  { value: '30d', label: 'Last 30 Days' }
];
```

### Modify Chart Style
Modify chart configuration in `components/FlowChart.jsx`:

```javascript
const chart = createChart(chartContainerRef.current, {
  height,
  layout: {
    background: { color: '#ffffff' },
    textColor: '#333',
  },
  // Other configuration...
});
```

### Add New Token
Add new token record in database:

```sql
INSERT INTO tokens (symbol, chain_id, decimals) 
VALUES ('NEW_TOKEN', (SELECT id FROM chains WHERE name = 'ethereum'), 18);
```

## Monitoring and Maintenance

### Log Monitoring
- View Vercel function logs
- Monitor database connection status
- Check API response time

### Data Backup
- Regularly backup database
- Monitor data growth
- Clean expired data

### Performance Optimization
- Add database indexes
- Optimize query statements
- Use caching mechanism

## Technical Support

If you encounter problems, please check:

1. Database connection status
2. Environment variable configuration
3. Vercel deployment logs
4. Browser console errors

## Changelog

- v0.1.0: Initial version, supports basic fund flow chart functionality
