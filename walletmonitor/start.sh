#!/bin/bash

# Wallet Monitor Startup Script

echo "🚀 Starting Wallet Monitor System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start database services
echo "📦 Starting database services..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 15

# Check database health
echo "🔍 Checking database health..."
if docker-compose ps | grep -q "healthy"; then
    echo "✅ Database is healthy"
else
    echo "⚠️  Database may not be fully ready, but continuing..."
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running system tests..."
python test.py

# Check database data
echo "📊 Checking database data..."
python check_db.py

echo ""
echo "🎉 Wallet Monitor System is ready!"
echo ""
echo "📋 Available commands:"
echo "  python main.py          - Start the monitoring service"
echo "  python test.py          - Run tests"
echo "  python check_db.py      - Check database data"
echo "  docker-compose logs     - View service logs"
echo "  docker-compose down     - Stop all services"
echo ""
echo "🌐 Database access:"
echo "  pgAdmin: http://localhost:8080 (check environment variables for credentials)"
echo "  PostgreSQL: localhost:5432 (check environment variables for credentials)"
echo ""
echo "📝 Next steps:"
echo "  1. Edit config.py to set your Ethereum node URL"
echo "  2. Run 'python main.py' to start monitoring"
echo "" 