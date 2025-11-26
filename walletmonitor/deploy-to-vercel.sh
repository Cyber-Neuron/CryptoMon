#!/bin/bash

# 资金流向监控仪表板部署脚本
echo "🚀 开始部署资金流向监控仪表板到Vercel..."

# 检查是否安装了Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI 未安装，正在安装..."
    npm install -g vercel
fi

# 进入应用目录
cd vercel-app

# 安装依赖
echo "📦 安装依赖..."
npm install

# 检查环境变量
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  警告: DATABASE_URL 环境变量未设置"
    echo "请在部署前设置 DATABASE_URL 环境变量"
    echo "例如: export DATABASE_URL='postgresql://user:password@host:port/database'"
fi

# 构建项目
echo "🔨 构建项目..."
npm run build

# 部署到Vercel
echo "🌐 部署到Vercel..."
vercel --prod

echo "✅ 部署完成！"
echo "📝 请确保在Vercel项目设置中配置了 DATABASE_URL 环境变量" 