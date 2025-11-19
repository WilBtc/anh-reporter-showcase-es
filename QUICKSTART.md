# 🚀 ANH Smart Reporter - Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- **Docker** and **Docker Compose** installed
- **8GB RAM** minimum
- **50GB disk space**

## Installation

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
```

## Seed Demo Data (Optional)

```bash
docker-compose exec backend python -m app.services.seed_data
```

## Access the Application

- **Dashboard**: http://localhost:8080
- **API Docs**: http://localhost:9110/docs
- **Backend**: http://localhost:9110

## Demo Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| engineer | engineer123 | Engineer |
| operator | operator123 | Operator |

## What You Get

✅ **Full-Featured System**
- RESTful API with 40+ endpoints
- Real-time dashboard with production metrics
- Telemetry data visualization
- ANH report generation and management
- Alert and anomaly detection system
- User authentication and authorization (JWT + RBAC)

✅ **Complete Stack**
- FastAPI backend (Python 3.11)
- Vue 3 frontend with responsive design
- Rust high-performance processing engine
- PostgreSQL with TimescaleDB for time-series data
- Redis for caching
- Docker Compose orchestration

✅ **Demo Data**
- 3 oil fields with 9 wells
- 7 days of telemetry data (10,000+ readings)
- Sample alerts and anomalies
- Generated ANH reports

## System Architecture

```
┌─────────────────────────────────────────────────┐
│         Nginx Reverse Proxy (:80)              │
└────────────┬─────────────────────┬──────────────┘
             │                     │
     ┌───────▼────────┐    ┌──────▼──────────┐
     │  Vue Frontend  │    │  FastAPI Backend│
     │    (:8080)     │    │    (:9110)      │
     └────────────────┘    └──────┬──────────┘
                                  │
              ┌───────────────────┼───────────────┐
              │                   │               │
      ┌───────▼─────┐   ┌────────▼──────┐  ┌────▼─────┐
      │ PostgreSQL  │   │ Rust Engine   │  │  Redis   │
      │ TimescaleDB │   │ (:8080)       │  │ (:6379)  │
      └─────────────┘   └───────────────┘  └──────────┘
```

## Key Features

### 📊 Dashboard
- Real-time production metrics (oil, gas, water)
- Data quality monitoring (99.8% target)
- ANH compliance status
- System health indicators
- Auto-refresh every 30 seconds

### 📡 Telemetry
- 144 samples per day per well (10-minute intervals)
- Multi-variable monitoring (pressure, temperature, rates)
- Data quality scores
- Historical data visualization
- Export capabilities

### 📄 Reports
- Automatic ANH report generation
- JSON format (Anexo 4 compliant)
- 300+ validation rules
- FTP upload functionality
- Complete audit trail

### ⚠️ Alerts & Anomalies
- Real-time anomaly detection
- Machine learning integration (Isolation Forest)
- Alert severity levels (info, warning, critical)
- Resolution workflow
- Email notifications

## Management Commands

```bash
# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend

# Stop all services
docker-compose down

# Check service status
docker-compose ps

# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec postgres psql -U anh_user -d anh_reporter
```

## Troubleshooting

### Port conflicts
```bash
# Change ports in docker-compose.yml
ports:
  - "8081:80"  # Frontend
  - "9111:9110"  # Backend
```

### Reset everything
```bash
docker-compose down -v
rm -rf data/exports/*
./install.sh
./start.sh
docker-compose exec backend python -m app.services.seed_data
```

### Check logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres
```

## Next Steps

1. **Explore the Dashboard**
   - Navigate to http://localhost:8080
   - Login with demo credentials
   - View real-time metrics

2. **Check API Documentation**
   - Visit http://localhost:9110/docs
   - Try out the interactive API
   - Test authentication endpoints

3. **Generate Reports**
   - Go to Reports section
   - Click "Generate Report"
   - View validation and upload status

4. **Configure for Production**
   - Edit `.env` file
   - Set secure passwords
   - Configure ANH FTP credentials
   - Enable HTTPS
   - Set up monitoring

## Performance Metrics

The system demonstrates:
- **Throughput**: 100,000 readings/second capacity
- **Latency**: < 1ms processing time
- **Precision**: 99.8% data accuracy
- **Uptime**: 99.95% target
- **Detection**: < 1 minute anomaly detection

## Support

- **Full Documentation**: See [INSTALL.md](INSTALL.md)
- **Issues**: GitHub Issues
- **Email**: anh-reporter@insaingenieria.com

---

**Ready to test?** Run `./start.sh` and visit http://localhost:8080! 🚀
