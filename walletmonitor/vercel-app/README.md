# Flow Monitor

A Web application for monitoring cryptocurrency capital flows.

## Features

### Dual Selectors

* **Source Group (From)**: Select the group from which funds flow out
* **Target Group (To)**: Select the group into which funds flow
* Supports precise flow filtering, allowing you to view capital movements between specific groups

### Main Features

* Real-time capital flow charts
* Multi-token support (ETH, USDC, USDT, etc.)
* Time range selection (1 hour to 30 days)
* ETH price overlay
* Net inflow/outflow analysis
* Display in Eastern Time (ET)

## How to Use

1. **Select Time Range**: Choose the desired range from the dropdown menu
2. **Select Tokens**: Pick the tokens you want to monitor from the multi-select list
3. **Set Flow Filters**:

   * Select the group funds are flowing **from** under “Source Group”
   * Select the group funds are flowing **to** under “Target Group”
   * If no groups are selected, all flows will be displayed
4. **View Results**: The chart will show all flows that match the selected criteria

## Flow Filtering Logic

* **Both From and To selected**: Only shows flows from the selected source to the selected target; all flows are treated as inflows (positive values)
* **Only From selected**: Shows all funds flowing out from the selected source (negative values)
* **Only To selected**: Shows all funds flowing into the selected target (positive values)
* **Neither selected**: Shows all flows (compatible with default behavior; positive = inflow, negative = outflow)

### Precise Flow Mode

When a source group (From) or target group (To) is specified, the system enters **Precise Flow Mode**:

* **All matched flows are shown as positive values**: Because the focus is the flow from A to B, not net inflow/outflow
* **Chart color is unified to green**: Represents directional flows instead of in/out differences
* **Net inflow/outflow sub-charts are hidden**: As the concept of outflow does not apply—only direction
* **Tooltip displays “Capital Flow”**: Instead of “Inflow” or “Outflow”

## Chart Description

* **Main Chart**: Displays flow bar charts and ETH price line
* **Net Outflow Chart**: Shows only outflows (negative values)
* **Net Inflow Chart**: Shows only inflows (positive values)
* **Tooltip**: Hover to view detailed flow information

## Tech Stack

* Next.js 15
* React
* Lightweight Charts
* PostgreSQL
* Tailwind CSS

## Development

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

## Local Development

1. Install dependencies:

```bash
npm install
```

2. Set environment variables:

```bash
# Create .env.local file
DATABASE_URL=your_postgresql_connection_string
```

3. Start development server:

```bash
npm run dev
```

4. Visit [http://localhost:3000](http://localhost:3000)

## Deploying to Vercel

1. Push the code to a GitHub repository
2. Import the project in Vercel
3. Set environment variables:

   * `DATABASE_URL`: PostgreSQL connection string
4. Deploy the project

## Database Schema

The app uses the following database table:

* `ex_flows`: Capital flow data

  * `timestamp`: Timestamp
  * `from_grp_name`: Source group name
  * `to_grp_name`: Target group name
  * `token`: Token symbol
  * `amount`: Amount
  * `usd_value`: USD value

## API Endpoints

* `GET /api/tokens` — Retrieve available token list
* `GET /api/groups` — Retrieve available group list
* `GET /api/flows` — Retrieve flow data (supports query parameters)
* `POST /api/flows` — Retrieve flow data (supports request body)

## Usage Instructions

1. Select time range
2. Select tokens to view (multi-select supported)
3. Select groups to view (multi-select supported)
4. The system will automatically load and display the corresponding flow charts
5. Green bars represent inflows; red bars represent outflows

## Notes

* Ensure the database connection is functioning
* SSL should be configured in production
* Using a connection pool is recommended to improve database performance



# Flow Monitor

一个用于监控加密货币资金流向的Web应用程序。

## 功能特性

### 双组选择器
- **来源组别 (From)**: 选择资金流出的来源组别
- **目标组别 (To)**: 选择资金流入的目标组别
- 支持精确的流向过滤，可以查看特定组别之间的资金流动

### 主要功能
- 实时资金流向图表
- 多代币支持 (ETH, USDC, USDT等)
- 时间范围选择 (1小时到30天)
- ETH价格叠加显示
- 净流入/流出分析
- 美东时间显示

## 使用方法

1. **选择时间范围**: 从下拉菜单中选择要查看的时间范围
2. **选择代币**: 从多选列表中选择要监控的代币
3. **设置流向过滤**:
   - 在"来源组别"中选择资金流出的组别
   - 在"目标组别"中选择资金流入的组别
   - 如果不选择任何组别，将显示所有流向
4. **查看结果**: 图表将显示符合条件的所有资金流向

## 流向过滤逻辑

- **同时选择From和To**: 只显示从指定来源到指定目标的流向，所有资金流动都视为流入（正值）
- **只选择From**: 显示从指定来源流出的所有资金（负值）
- **只选择To**: 显示流入指定目标的所有资金（正值）
- **都不选择**: 显示所有流向（兼容原有功能，正值表示流入，负值表示流出）

### 精确流向模式

当指定了来源组别（From）或目标组别（To）时，系统会进入"精确流向模式"：

- **所有匹配的资金流动都显示为正值**：因为此时关注的是从A到B的资金流向，而不是净流入/流出
- **图表颜色统一为绿色**：表示资金流向，而不是区分流入/流出
- **隐藏净流入/流出子图表**：因为此时没有流出概念，只有流向
- **工具提示显示"资金流向"**：而不是"流入"或"流出"

## 图表说明

- **主图表**: 显示资金流向的柱状图和ETH价格线
- **净流出图表**: 只显示资金流出（负值）
- **净流入图表**: 只显示资金流入（正值）
- **工具提示**: 鼠标悬停时显示详细的流向信息

## 技术栈

- Next.js 15
- React
- Lightweight Charts
- PostgreSQL
- Tailwind CSS

## 开发

```bash
npm install
npm run dev
```

## 构建

```bash
npm run build
```

## 本地开发

1. 安装依赖：
```bash
npm install
```

2. 设置环境变量：
```bash
# 创建 .env.local 文件
DATABASE_URL=your_postgresql_connection_string
```

3. 启动开发服务器：
```bash
npm run dev
```

4. 访问 http://localhost:3000

## 部署到Vercel

1. 将代码推送到GitHub仓库

2. 在Vercel中导入项目

3. 设置环境变量：
   - `DATABASE_URL`: PostgreSQL数据库连接字符串

4. 部署项目

## 数据库结构

应用使用以下数据库表：

- `ex_flows`: 资金流数据表
  - `timestamp`: 时间戳
  - `from_grp_name`: 来源组名
  - `to_grp_name`: 目标组名
  - `token`: 代币符号
  - `amount`: 数量
  - `usd_value`: USD价值

## API端点

- `GET /api/tokens` - 获取可用代币列表
- `GET /api/groups` - 获取可用组别列表
- `GET /api/flows` - 获取资金流数据（支持查询参数）
- `POST /api/flows` - 获取资金流数据（支持请求体）

## 使用说明

1. 选择时间范围
2. 选择要查看的代币（可多选）
3. 选择要查看的组别（可多选）
4. 系统会自动加载并显示相应的资金流向图表
5. 绿色柱表示流入资金，红色柱表示流出资金

## 注意事项

- 确保数据库连接正常
- 生产环境需要配置SSL连接
- 建议使用连接池来优化数据库性能 
