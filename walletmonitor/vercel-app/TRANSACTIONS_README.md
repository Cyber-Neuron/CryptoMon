# 交易记录页面功能说明

## 概述
新增了交易记录页面 (`/transactions`)，用于展示和分析钱包之间的交易数据。

## 功能特性

### 1. 钱包筛选器
- **发送方钱包选择器**: 可以选择特定的发送方钱包进行筛选
- **接收方钱包选择器**: 可以选择特定的接收方钱包进行筛选
- 支持按钱包ID进行精确筛选
- 显示钱包的友好名称和所属组别

### 2. 交易数据展示
- **交易哈希**: 显示交易哈希，点击可跳转到Etherscan查看详情
- **发送方信息**: 显示发送方钱包地址和友好名称
- **接收方信息**: 显示接收方钱包地址和友好名称
- **代币信息**: 显示交易的代币符号
- **交易数量**: 格式化显示交易数量
- **USD价值**: 显示交易的美元价值
- **时间戳**: 格式化显示交易时间
- **区块号**: 显示交易所在区块

### 3. 数据分页
- 支持分页加载，每页50条记录
- "加载更多"按钮实现无限滚动
- 自动处理筛选条件变化时的数据重置

### 4. 响应式设计
- 适配桌面和移动设备
- 表格支持横向滚动
- 现代化的UI设计

## API端点

### GET /api/transactions
获取交易数据，支持以下查询参数：
- `fromWalletId`: 发送方钱包ID
- `toWalletId`: 接收方钱包ID
- `limit`: 每页记录数（默认100）
- `offset`: 偏移量（默认0）

### GET /api/wallets
获取钱包列表，支持以下查询参数：
- `groupType`: 按组别类型筛选
- `groupName`: 按组别名称筛选

## 数据库查询
交易数据通过以下SQL查询获取：
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

## 导航
- 新增了顶部导航栏，包含"资金流向图"和"交易记录"两个页面
- 支持页面间的快速切换
- 当前页面高亮显示

## 技术栈
- **前端**: Next.js 15, React 18, Tailwind CSS
- **数据库**: PostgreSQL (通过@vercel/postgres)
- **工具库**: date-fns (时间格式化)

## 使用方法
1. 访问 `/transactions` 页面
2. 使用筛选器选择特定的发送方和/或接收方钱包
3. 查看交易列表数据
4. 点击"加载更多"查看更多历史记录
5. 点击交易哈希跳转到Etherscan查看详细信息 