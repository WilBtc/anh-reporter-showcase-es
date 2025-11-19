#!/bin/bash

# ANH Smart Reporter - Startup Script
# Version: 3.0.0

set -e

echo "=========================================="
echo "  ANH Smart Reporter - Starting Services"
echo "  Version 3.0.0"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Running installation first...${NC}"
    ./install.sh
    exit 0
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Start services
echo ""
echo "🚀 Starting all services..."
echo ""
docker-compose up -d

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "🔍 Checking service health..."

services=("postgres" "redis" "backend")
all_healthy=true

for service in "${services[@]}"; do
    if docker-compose ps | grep -q "$service.*Up"; then
        echo -e "  ✓ $service: ${GREEN}Running${NC}"
    else
        echo -e "  ✗ $service: ${YELLOW}Not running${NC}"
        all_healthy=false
    fi
done

echo ""

if [ "$all_healthy" = true ]; then
    echo "=========================================="
    echo -e "${GREEN}✅ All services are running!${NC}"
    echo "=========================================="
    echo ""
    echo "🌐 Access the application:"
    echo ""
    echo "   Frontend Dashboard: http://localhost:8080"
    echo "   API Documentation:  http://localhost:9110/docs"
    echo "   Backend API:        http://localhost:9110"
    echo "   Rust Engine:        http://localhost:8080"
    echo ""
    echo "📊 To seed demo data, run:"
    echo "   docker-compose exec backend python -m app.services.seed_data"
    echo ""
    echo "📝 To view logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 To stop services:"
    echo "   docker-compose down"
    echo ""
else
    echo "⚠️  Some services may not be running properly."
    echo "Run 'docker-compose logs' to see detailed logs."
fi

echo "=========================================="
