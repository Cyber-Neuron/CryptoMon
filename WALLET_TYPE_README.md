# Wallet Type Feature Documentation

## Overview

This update adds the `wallet_type` feature to the wallet monitoring system, allowing classification of wallets based on their purpose.

## Database Changes

### 1. New wallet_types Table

```sql
CREATE TABLE public.wallet_types (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Predefined Wallet Types

- `cold` - Cold storage wallet
- `hot` - Hot wallet (active trading)
- `deposit` - Deposit wallet
- `internal` - Internal transfer wallet
- `regular` - Regular user wallet

### 3. Update wallets Table

Added `wallet_type_id` field to the `wallets` table, referencing the `wallet_types` table.

## Features

### Automatic Type Recognition

The system automatically recognizes wallet types based on `friendly_name`:

- Contains "cold" keyword → `cold` type
- Contains "hot" keyword → `hot` type
- Contains "deposit" keyword → `deposit` type
- Contains "internal" keyword → `internal` type
- Other cases → `regular` type

### Caching Mechanism

- `wallet_type` information is cached to improve performance
- Supports batch operations and cache management

## Usage

### 1. Run Database Migration

```bash
psql -d your_database -f wallet_type_migration.sql
```

### 2. Use in Code

```python
from walletmonitor.database import DatabaseManager
from walletmonitor.models import Wallet

# Create database manager
db_manager = DatabaseManager()

# Create wallet (automatically recognizes type)
wallet = Wallet(
    address="0x1234567890123456789012345678901234567890",
    friendly_name="Cold Storage Wallet"  # Automatically recognized as cold type
)

# Store wallet
with db_manager.get_connection() as conn:
    wallet_id = db_manager.get_or_create_wallet(conn, wallet)
    print(f"Wallet Type: {wallet.wallet_type}")  # Output: cold
```

### 3. Manually Specify Wallet Type

```python
wallet = Wallet(
    address="0x1234567890123456789012345678901234567890",
    friendly_name="My Wallet",
    wallet_type="hot"  # Manually specify type
)
```

### 4. Batch Get Wallets

```python
addresses = ["0x1234...", "0x5678..."]
wallets = db_manager.get_wallets_batch(conn, addresses)

for addr, wallet in wallets.items():
    print(f"Address: {addr}, Type: {wallet.wallet_type}")
```

## Testing

Run test script to verify functionality:

```bash
python test_wallet_type.py
```

## Backward Compatibility

- Existing wallets are automatically set to `regular` type
- Existing wallets containing "cold" keyword are automatically set to `cold` type
- All existing functionality remains unchanged

## Performance Optimization

- Added `wallet_type_id` index to improve query performance
- Implemented caching mechanism to reduce database queries
- Supports batch operations to improve efficiency

## Notes

1. Ensure database backup before running migration script
2. Migration script uses `IF NOT EXISTS` and `ON CONFLICT` to ensure safe execution
3. Newly created wallets automatically set type based on `friendly_name`
4. Can customize type recognition logic by modifying `determine_wallet_type` method
