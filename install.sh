#!/bin/bash

# ANH Smart Reporter - Installation Script
# Version: 3.0.0

set -e

echo "=========================================="
echo "  ANH Smart Reporter - Installation"
echo "  Version 3.0.0"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}Warning: Running as root. It's recommended to run as a regular user.${NC}"
fi

# Check Docker
echo "🔍 Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✓ Docker is installed${NC}"

# Check Docker Compose
echo "🔍 Checking Docker Compose..."
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose is installed${NC}"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env file with your configuration before starting the system${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Create required directories
echo ""
echo "📁 Creating required directories..."
mkdir -p data/exports
mkdir -p data/sample
mkdir -p docker/nginx/ssl
echo -e "${GREEN}✓ Directories created${NC}"

# Pull Docker images
echo ""
echo "📦 Pulling Docker images (this may take a few minutes)..."
docker-compose pull

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Installation completed successfully!${NC}"
echo "=========================================="
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Review and edit configuration:"
echo "   nano .env"
echo ""
echo "2. Start the system:"
echo "   ./start.sh"
echo ""
echo "3. Access the application:"
echo "   Frontend:  http://localhost:8080"
echo "   API Docs:  http://localhost:9110/docs"
echo "   Backend:   http://localhost:9110"
echo ""
echo "4. Seed demo data (optional):"
echo "   docker-compose exec backend python -m app.services.seed_data"
echo ""
echo "5. Demo credentials:"
echo "   Username: admin / Password: admin123"
echo "   Username: engineer / Password: engineer123"
echo "   Username: operator / Password: operator123"
echo ""
echo "=========================================="
echo ""
