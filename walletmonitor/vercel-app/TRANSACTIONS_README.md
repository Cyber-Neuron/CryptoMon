# Transaction Records Page Feature Description

## Overview
Added a transaction records page (`/transactions`) for displaying and analyzing transaction data between wallets.

## Features

### 1. Wallet Filters
- **Sender Wallet Selector**: Can select specific sender wallets for filtering
- **Receiver Wallet Selector**: Can select specific receiver wallets for filtering
- Supports filtering by wallet ID
- Displays wallet friendly names and group affiliations

### 2. Transaction Data Display
- **Transaction Hash**: Displays transaction hash, clickable to jump to Etherscan for details
- **Sender Information**: Displays sender wallet address and friendly name
- **Receiver Information**: Displays receiver wallet address and friendly name
- **Token Information**: Displays transaction token symbol
- **Transaction Amount**: Formatted display of transaction amount
- **USD Value**: Displays transaction USD value
- **Timestamp**: Formatted display of transaction time
- **Block Number**: Displays block containing the transaction

### 3. Data Pagination
- Supports paginated loading, 50 records per page
- "Load More" button implements infinite scroll
- Automatically handles data reset when filter conditions change

### 4. Responsive Design
- Adapts to desktop and mobile devices
- Table supports horizontal scrolling
- Modern UI design

## API Endpoints

### GET /api/transactions
Get transaction data, supports the following query parameters:
- `fromWalletId`: Sender wallet ID
- `toWalletId`: Receiver wallet ID
- `limit`: Records per page (default: 100)
- `offset`: Offset (default: 0)

### GET /api/wallets
Get wallet list, supports the following query parameters:
- `groupType`: Filter by group type
- `groupName`: Filter by group name

## Database Query
Transaction data is fetched through the following SQL query:
```sql
SELECT 
  t.id, t.hash, t.block_number, t.amount, t.timestamp, t.usd_value, t.created_at,
  fw.address as from_address, fw.friendly_name as from_friendly_name, fw.grp_name as from_grp_name,
  tw.address as to_address, tw.friendly_name as to_friendly_name, tw.grp_name as to_grp_name,
  tok.symbol as token_symbol, c.name as chain_name, c.native_sym as chain_native_sym
FROM transactions t
LEFT JOIN wallets fw ON t.from_wallet_id = fw.id
LEFT JOIN wallets tw ON t.to_wallet_id = tw.id
LEFT JOIN tokens tok ON t.token_id = tok.id
LEFT JOIN chains c ON t.chain_id = c.id
```

## Navigation
- Added top navigation bar with "Fund Flow Chart" and "Transaction Records" pages
- Supports quick switching between pages
- Current page is highlighted

## Tech Stack
- **Frontend**: Next.js 15, React 18, Tailwind CSS
- **Database**: PostgreSQL (via @vercel/postgres)
- **Utility Libraries**: date-fns (time formatting)

## Usage
1. Visit the `/transactions` page
2. Use filters to select specific sender and/or receiver wallets
3. View transaction list data
4. Click "Load More" to view more historical records
5. Click transaction hash to jump to Etherscan for detailed information
