# ANH Smart Reporter - Installation Guide

Complete installation and deployment guide for ANH Smart Reporter v3.0.0.

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Quick Start (5 Minutes)](#quick-start-5-minutes)
- [Detailed Installation](#detailed-installation)
- [Configuration](#configuration)
- [Starting the System](#starting-the-system)
- [Seeding Demo Data](#seeding-demo-data)
- [Accessing the System](#accessing-the-system)
- [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2
- **RAM**: 8 GB
- **Storage**: 50 GB available
- **CPU**: 4 cores
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### Recommended for Production
- **RAM**: 16 GB+
- **Storage**: 500 GB SSD
- **CPU**: 8+ cores
- **Network**: 100 Mbps+

---

## 🚀 Quick Start (5 Minutes)

For a quick demo installation, run:

```bash
# 1. Clone the repository
git clone https://github.com/WilBtc/anh-reporter-showcase-es.git
cd anh-reporter-showcase-es

# 2. Make scripts executable
chmod +x install.sh start.sh

# 3. Run installation
./install.sh

# 4. Start the system
./start.sh

# 5. Seed demo data (optional)
docker-compose exec backend python -m app.services.seed_data

# 6. Access the application
# Open http://localhost:8080 in your browser
```

**Demo Credentials:**
- Admin: `admin` / `admin123`
- Engineer: `engineer` / `engineer123`
- Operator: `operator` / `operator123`

---

## 📦 Detailed Installation

### Step 1: Install Prerequisites

#### Ubuntu/Debian
```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin -y

# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### macOS
```bash
# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop

# Or use Homebrew
brew install --cask docker
```

#### Windows
1. Install [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/install/)
2. Enable WSL2 integration
3. Use WSL2 terminal for commands

### Step 2: Clone Repository

```bash
git clone https://github.com/WilBtc/anh-reporter-showcase-es.git
cd anh-reporter-showcase-es
```

### Step 3: Configuration

```bash
# Create .env file from template
cp .env.example .env

# Edit configuration
nano .env
```

**Important settings to configure:**

```bash
# Security (REQUIRED)
SECRET_KEY=your-secure-random-key-here  # Generate with: openssl rand -base64 32

# Database (Optional - defaults provided)
DATABASE_URL=postgresql+asyncpg://anh_user:anh_password@postgres:5432/anh_reporter

# ANH FTP (Required for production)
ANH_FTP_HOST=ftp.anh.gov.co
ANH_FTP_USER=your_username
ANH_FTP_PASSWORD=your_password

# Email Alerts (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Step 4: Build and Start Services

```bash
# Build all containers
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | JWT secret key | auto-generated | Yes |
| `DATABASE_URL` | PostgreSQL connection | localhost | No |
| `REDIS_URL` | Redis connection | localhost | No |
| `ANH_FTP_HOST` | ANH FTP server | ftp.anh.gov.co | Yes (prod) |
| `ANH_FTP_USER` | FTP username | - | Yes (prod) |
| `ANH_FTP_PASSWORD` | FTP password | - | Yes (prod) |
| `SMTP_HOST` | Email server | smtp.gmail.com | No |
| `OPCUA_ENABLED` | Enable OPC UA | true | No |
| `MODBUS_ENABLED` | Enable Modbus | true | No |
| `MQTT_ENABLED` | Enable MQTT | true | No |

### Industrial Protocol Configuration

#### OPC UA
```bash
OPCUA_ENABLED=true
OPCUA_ENDPOINT=opc.tcp://your-scada:4840
OPCUA_NAMESPACE=2
```

#### Modbus TCP
```bash
MODBUS_ENABLED=true
MODBUS_HOST=192.168.1.100
MODBUS_PORT=502
```

#### MQTT
```bash
MQTT_ENABLED=true
MQTT_BROKER=mqtt.your-server.com
MQTT_PORT=1883
MQTT_TOPIC_PREFIX=anh/telemetry
```

---

## 🎬 Starting the System

### Using Scripts (Recommended)

```bash
# Start all services
./start.sh

# Stop all services
docker-compose down

# Restart a specific service
docker-compose restart backend
```

### Manual Start

```bash
# Start in detached mode
docker-compose up -d

# Start with logs
docker-compose up

# Start specific services
docker-compose up -d postgres redis backend
```

### Verify Services

```bash
# Check all services are running
docker-compose ps

# Check backend health
curl http://localhost:9110/health

# Check Rust engine health
curl http://localhost:8080/health

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## 🌱 Seeding Demo Data

To populate the database with demo data:

```bash
# Seed the database
docker-compose exec backend python -m app.services.seed_data
```

This will create:
- ✅ 3 demo users (admin, engineer, operator)
- ✅ 3 oil fields with 9 wells
- ✅ 7 days of telemetry data (144 samples/day per well)
- ✅ Sample alerts and anomalies
- ✅ Sample ANH reports

**Expected output:**
```
🌱 ANH Reporter - Seeding Database
📝 Creating users...
✓ Created user: admin
✓ Created user: engineer
✓ Created user: operator
🏭 Creating fields and wells...
✓ Created field: Campo Rubiales
  ✓ Created well: RUB-001-W01
  ...
✅ Database seeding completed successfully!
```

---

## 🌐 Accessing the System

### Web Interfaces

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend Dashboard** | http://localhost:8080 | Main user interface |
| **API Documentation** | http://localhost:9110/docs | Interactive API docs (Swagger) |
| **API Alternative Docs** | http://localhost:9110/redoc | ReDoc API documentation |
| **Backend API** | http://localhost:9110 | REST API endpoints |
| **Rust Engine** | http://localhost:8080 | High-performance processor |
| **Prometheus Metrics** | http://localhost:9110/metrics | System metrics |

### Default Credentials

| User | Username | Password | Role |
|------|----------|----------|------|
| Administrator | `admin` | `admin123` | Full access |
| Engineer | `engineer` | `engineer123` | Technical access |
| Operator | `operator` | `operator123` | Operational access |

⚠️ **IMPORTANT**: Change these passwords in production!

### API Access

```bash
# Get authentication token
curl -X POST http://localhost:9110/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Use token in requests
TOKEN="your_token_here"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:9110/api/v1/dashboard/overview
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Check what's using the port
sudo lsof -i :9110
sudo lsof -i :8080

# Stop the process or change port in docker-compose.yml
```

#### 2. Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

#### 3. Frontend Not Loading

```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

#### 4. Rust Engine Build Fails

```bash
# Check Rust engine logs
docker-compose logs rust-engine

# Rebuild with no cache
docker-compose build --no-cache rust-engine
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Resetting the System

```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Remove all data (WARNING: This deletes everything!)
rm -rf data/exports/*

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d

# Reseed database
docker-compose exec backend python -m app.services.seed_data
```

### Performance Issues

```bash
# Check resource usage
docker stats

# Check disk space
df -h

# Clean up Docker
docker system prune -a
```

---

## 📊 Production Deployment

For production deployment, see [DEPLOYMENT_INSTRUCTIONS.md](DEPLOYMENT_INSTRUCTIONS.md)

Key considerations:
- Use strong passwords and secrets
- Enable HTTPS/TLS
- Configure firewall rules
- Set up backup procedures
- Enable monitoring and alerts
- Use production-grade database configuration
- Implement rate limiting
- Configure log rotation

---

## 🆘 Getting Help

- **Documentation**: https://docs.anh-reporter.com
- **Issues**: https://github.com/WilBtc/anh-reporter-showcase-es/issues
- **Email**: anh-reporter@insaingenieria.com
- **Support**: support.anh-reporter.com

---

## 📝 License

Copyright © 2025 INSA Ingeniería y Automatización
All rights reserved.

---

*Last updated: November 2025 | Version 3.0.0*
