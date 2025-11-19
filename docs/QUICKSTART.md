# 🚀 Guía de Inicio Rápido - ANH Smart Reporter

## ⏱️ De 0 a Producción en 5 Minutos

### Prerequisitos

- Docker 24.0+ y Docker Compose 2.23+
- 8GB RAM mínimo
- 20GB espacio en disco
- Puerto 9110 (API) y 5173 (Frontend) disponibles

### 🎯 Instalación Express

```bash
# 1. Clonar el repositorio
git clone https://github.com/WilBtc/anh-reporter-showcase-es.git
cd anh-reporter-showcase-es

# 2. Configuración inicial
cp .env.example .env
# Editar .env con sus credenciales ANH

# 3. Lanzar el sistema completo
docker-compose up -d

# 4. Verificar estado (esperar ~30 segundos)
docker-compose ps
curl http://localhost:9110/health

# 5. Acceder al dashboard
# Abrir navegador en: http://localhost:5173
# Usuario demo: admin@demo.com / admin123
```

## 📊 Validación de Funcionamiento

### Check de Salud del Sistema

```bash
# Verificar todos los servicios
curl http://localhost:9110/api/v1/health/full

# Respuesta esperada:
{
  "status": "healthy",
  "services": {
    "api": "online",
    "database": "connected",
    "redis": "connected",
    "scheduler": "running",
    "rust_processor": "ready"
  },
  "uptime": "00:01:23"
}
```

### Primera Prueba de Telemetría

```bash
# Enviar dato de prueba
curl -X POST http://localhost:9110/api/v1/telemetry/test \
  -H "Content-Type: application/json" \
  -d '{
    "field_id": "test-field",
    "variable": "oil_flow_rate",
    "value": 1250.5,
    "timestamp": "2025-11-19T10:00:00Z"
  }'

# Ver en dashboard: Sección Telemetry → Real-time
```

## 🔧 Configuración Rápida SCADA

### Opción 1: OPC UA

```yaml
# config/scada.yml
opc_ua:
  endpoint: "opc.tcp://your-scada-server:4840"
  security: "Basic256Sha256"
  variables:
    - "ns=2;s=Field01.Oil.FlowRate"
    - "ns=2;s=Field01.Gas.FlowRate"
    - "ns=2;s=Field01.Water.FlowRate"
```

### Opción 2: Modbus TCP

```yaml
# config/modbus.yml
modbus:
  host: "192.168.1.100"
  port: 502
  mappings:
    - address: 40001
      variable: "oil_temperature"
      scale: 0.1
    - address: 40002
      variable: "oil_pressure"
      scale: 0.01
```

## 📈 Dashboard - Primeros Pasos

### Acceso y Navegación

1. **Login**: http://localhost:5173
2. **Dashboard Principal**: Vista general de producción
3. **Telemetría**: Datos en tiempo real (actualización cada 10s)
4. **Reportes**: Generación y gestión de reportes ANH
5. **Configuración**: Personalización de alertas y umbrales

### Configurar Primera Alerta

```javascript
// En Dashboard → Settings → Alerts
{
  "name": "Baja Producción Petróleo",
  "condition": "oil_flow_rate < 1000",
  "severity": "warning",
  "recipients": ["operador@empresa.com"],
  "cooldown": 300  // segundos
}
```

## 🎮 Comandos Útiles

### Gestión de Servicios

```bash
# Ver logs en tiempo real
docker-compose logs -f backend

# Reiniciar un servicio específico
docker-compose restart backend

# Escalar servicios (para alta carga)
docker-compose up -d --scale backend=3

# Backup de base de datos
docker-compose exec timescaledb pg_dump -U anh_user anh_db > backup.sql

# Restaurar backup
docker-compose exec -T timescaledb psql -U anh_user anh_db < backup.sql
```

### Monitoreo Rápido

```bash
# Estado de servicios
docker-compose exec backend python -m app.cli status

# Métricas de performance
curl http://localhost:9110/metrics | grep anh_

# Ver colas de procesamiento
docker-compose exec redis redis-cli llen telemetry_queue
```

## 🔐 Configuración de Producción

### Variables de Entorno Críticas

```bash
# .env.production
# Base de datos
DATABASE_URL=postgresql://user:pass@db:5432/anh_prod
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://redis:6379/0

# Seguridad
SECRET_KEY=<generar-con-openssl-rand-hex-32>
JWT_EXPIRY=3600
ALLOWED_ORIGINS=https://your-domain.com

# ANH
ANH_FTP_HOST=ftp.anh.gov.co
ANH_FTP_USER=your-operator-code
ANH_FTP_PASSWORD=<encrypted-password>

# Alertas
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=alerts@company.com
ALERT_RECIPIENTS=operations@company.com,supervisor@company.com

# Performance
RUST_THREADS=8
ML_WORKERS=4
CACHE_TTL=300
```

### SSL/TLS para Producción

```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name anh-reporter.company.com;

    ssl_certificate /etc/nginx/certs/cert.pem;
    ssl_certificate_key /etc/nginx/certs/key.pem;

    location / {
        proxy_pass http://frontend:5173;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://backend:9110;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Generación de Primer Reporte ANH

### Método Automático (Recomendado)

El sistema genera automáticamente reportes diarios a las 6:00 AM COT.

### Método Manual (Testing)

```bash
# Generar reporte para fecha específica
curl -X POST http://localhost:9110/api/v1/reports/generate \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-11-19",
    "field_id": "field-001",
    "force": true
  }'

# Descargar reporte generado
curl -O http://localhost:9110/api/v1/reports/<report-id>/download
```

## 🚨 Troubleshooting Común

### Problema: Servicios no inician

```bash
# Verificar logs
docker-compose logs

# Solución común: Limpiar y reiniciar
docker-compose down -v
docker-compose up -d
```

### Problema: No hay datos en dashboard

```bash
# Verificar conexión SCADA
docker-compose exec backend python -m app.cli test-scada

# Verificar base de datos
docker-compose exec timescaledb psql -U anh_user -c "SELECT COUNT(*) FROM telemetry_data;"
```

### Problema: Reportes no se generan

```bash
# Verificar scheduler
docker-compose exec backend python -m app.cli scheduler-status

# Forzar generación manual
docker-compose exec backend python -m app.cli generate-report --date 2025-11-19
```

## 📚 Recursos Adicionales

- 📖 [Documentación Completa](https://docs.anh-reporter.com)
- 🎥 [Videos Tutoriales](https://youtube.com/@anh-reporter)
- 💬 [Soporte en Línea](https://support.anh-reporter.com)
- 📧 [Email Soporte](mailto:soporte@insaingenieria.com)

## 🎯 Próximos Pasos

1. ✅ Sistema instalado y funcionando
2. ➡️ Configurar conexión con su SCADA real
3. ➡️ Personalizar variables según sus campos
4. ➡️ Configurar alertas específicas
5. ➡️ Entrenar modelos ML con datos históricos
6. ➡️ Activar envío automático FTP a ANH

---

**¿Necesita ayuda?** Nuestro equipo está disponible 24/7:
- 📞 Hotline: 01-8000-ANH-HELP
- 💬 Chat: En el dashboard (esquina inferior derecha)
- 📧 Email: quickstart@anh-reporter.com

*Tiempo promedio de configuración completa: 2-4 horas*

---

*Guía actualizada: Noviembre 2025 | v3.0.0*