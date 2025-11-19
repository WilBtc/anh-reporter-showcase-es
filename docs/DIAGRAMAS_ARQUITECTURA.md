# 🎨 Diagramas de Arquitectura - ANH Smart Reporter

## 📊 Arquitectura General del Sistema

```mermaid
graph TB
    subgraph "Capa de Campo - Equipos Industriales"
        SENSORS[fa:fa-microchip Sensores<br/>Presión, Flujo, Temperatura]
        METERS[fa:fa-tachometer-alt Medidores<br/>Fiscales y Operacionales]
        RTU[fa:fa-server RTUs<br/>Unidades Remotas]
        PLC[fa:fa-cogs PLCs<br/>Controladores]
    end

    subgraph "Capa de Comunicación Industrial"
        OPCUA[fa:fa-plug OPC UA<br/>IEC 62541]
        MODBUS[fa:fa-network-wired Modbus<br/>TCP/RTU]
        MQTT[fa:fa-broadcast-tower MQTT<br/>IoT Protocol]
        IEC[fa:fa-bolt IEC 61850<br/>Power Systems]
    end

    subgraph "Edge Computing Layer"
        EDGE1[fa:fa-microchip Edge Node 1<br/>Campo Norte]
        EDGE2[fa:fa-microchip Edge Node 2<br/>Campo Sur]
        EDGE3[fa:fa-microchip Edge Node 3<br/>Campo Este]
    end

    subgraph "Core Processing - Rust Engine"
        RUST[fa:fa-rocket Rust Processor<br/>100K ops/sec]
        VALIDATOR[fa:fa-check-circle Validador<br/>300+ reglas]
        NORMALIZER[fa:fa-filter Normalizador<br/>Unidades y formatos]
    end

    subgraph "Inteligencia Artificial"
        ML[fa:fa-brain ML Engine<br/>Anomaly Detection]
        SPC[fa:fa-chart-line SPC Analysis<br/>Control Estadístico]
        FORECAST[fa:fa-chart-area Forecasting<br/>Predicción 7 días]
    end

    subgraph "Almacenamiento"
        TSDB[(fa:fa-database TimescaleDB<br/>5 años retención)]
        REDIS[(fa:fa-memory Redis<br/>Cache y Queue)]
        S3[(fa:fa-cloud AWS S3<br/>Backup y archivos)]
    end

    subgraph "API Backend"
        FASTAPI[fa:fa-server FastAPI<br/>44+ endpoints]
        AUTH[fa:fa-lock Auth Service<br/>JWT + RBAC]
        SCHEDULER[fa:fa-clock Scheduler<br/>APScheduler]
    end

    subgraph "Frontend"
        VUE[fa:fa-desktop Vue 3 SPA<br/>Dashboard]
        MOBILE[fa:fa-mobile PWA<br/>Mobile App]
    end

    subgraph "Entrega ANH"
        JSON[fa:fa-file-code JSON Generator<br/>ANH Format]
        FTP[fa:fa-upload FTP Upload<br/>6:50 AM daily]
        EMAIL[fa:fa-envelope Alertas<br/>Email/SMS]
    end

    subgraph "Monitoreo"
        PROM[fa:fa-chart-bar Prometheus<br/>Métricas]
        GRAF[fa:fa-tv Grafana<br/>Dashboards]
        ALERT[fa:fa-bell AlertManager<br/>Notificaciones]
    end

    SENSORS --> OPCUA
    METERS --> MODBUS
    RTU --> MQTT
    PLC --> IEC

    OPCUA --> EDGE1
    MODBUS --> EDGE2
    MQTT --> EDGE3
    IEC --> EDGE1

    EDGE1 --> RUST
    EDGE2 --> RUST
    EDGE3 --> RUST

    RUST --> VALIDATOR
    VALIDATOR --> NORMALIZER
    NORMALIZER --> ML

    ML --> SPC
    SPC --> FORECAST

    NORMALIZER --> TSDB
    ML --> TSDB
    FORECAST --> TSDB

    TSDB --> FASTAPI
    REDIS --> FASTAPI

    FASTAPI --> AUTH
    AUTH --> VUE
    FASTAPI --> MOBILE

    SCHEDULER --> JSON
    JSON --> FTP
    FASTAPI --> EMAIL

    FASTAPI --> PROM
    PROM --> GRAF
    GRAF --> ALERT

    style RUST fill:#f9f,stroke:#333,stroke-width:4px
    style ML fill:#bbf,stroke:#333,stroke-width:2px
    style TSDB fill:#f96,stroke:#333,stroke-width:2px
```

## 🔄 Flujo de Procesamiento de Datos

```mermaid
sequenceDiagram
    participant Campo as Campo Petrolero
    participant SCADA as Sistema SCADA
    participant Edge as Edge Node
    participant Rust as Rust Processor
    participant ML as ML Engine
    participant DB as TimescaleDB
    participant API as FastAPI
    participant ANH as Sistema ANH

    loop Cada 10 minutos
        Campo->>SCADA: Lectura sensores
        SCADA->>Edge: Transmit via OPC UA
        Edge->>Edge: Buffer local (offline capable)
        Edge->>Rust: Batch transfer

        par Procesamiento Paralelo
            Rust->>Rust: Validación (< 1ms)
        and
            Rust->>Rust: Normalización
        and
            Rust->>ML: Detección anomalías
        end

        ML->>ML: Análisis SPC
        ML->>DB: Store con quality flags

        alt Anomalía Detectada
            ML->>API: Trigger alerta
            API->>API: Notificar usuarios
        end
    end

    Note over DB: 144 muestras/día acumuladas

    rect rgb(200, 255, 200)
        Note right of API: Generación Diaria 6:00 AM
        API->>DB: Query datos del día
        DB->>API: 144 samples × N variables
        API->>Rust: Generar JSON
        Rust->>ANH: Upload FTP (6:50 AM)
        ANH->>ANH: Validación y aprobación
    end
```

## 🏗️ Arquitectura de Microservicios

```mermaid
graph LR
    subgraph "Client Layer"
        WEB[fa:fa-globe Web Browser]
        MOBILE[fa:fa-mobile Mobile App]
        API_EXT[fa:fa-plug External APIs]
    end

    subgraph "Gateway Layer"
        NGINX[fa:fa-shield-alt NGINX<br/>Load Balancer]
        WAF[fa:fa-firewall WAF<br/>Security]
    end

    subgraph "Service Mesh"
        AUTH_SVC[fa:fa-key Auth Service<br/>Port 9001]
        TELEMETRY_SVC[fa:fa-satellite Telemetry Service<br/>Port 9002]
        REPORT_SVC[fa:fa-file-alt Report Service<br/>Port 9003]
        ANALYTICS_SVC[fa:fa-chart-pie Analytics Service<br/>Port 9004]
        WELL_SVC[fa:fa-oil-can Well Service<br/>Port 9005]
        ALERT_SVC[fa:fa-bell Alert Service<br/>Port 9006]
    end

    subgraph "Processing Layer"
        RUST_PROC[fa:fa-cog Rust Processor<br/>Port 9100]
        ML_PROC[fa:fa-brain ML Processor<br/>Port 9101]
        SCHEDULER[fa:fa-calendar Scheduler<br/>Port 9102]
    end

    subgraph "Data Layer"
        PG[(fa:fa-database PostgreSQL<br/>Port 5432)]
        REDIS[(fa:fa-bolt Redis<br/>Port 6379)]
        S3[(fa:fa-cloud Object Store)]
    end

    subgraph "Message Bus"
        KAFKA[fa:fa-stream Kafka/Redis Pub-Sub]
    end

    WEB --> NGINX
    MOBILE --> NGINX
    API_EXT --> WAF

    NGINX --> AUTH_SVC
    NGINX --> TELEMETRY_SVC
    NGINX --> REPORT_SVC
    NGINX --> ANALYTICS_SVC
    NGINX --> WELL_SVC

    AUTH_SVC -.->|Validate| REDIS
    TELEMETRY_SVC --> RUST_PROC
    REPORT_SVC --> SCHEDULER
    ANALYTICS_SVC --> ML_PROC
    WELL_SVC --> PG

    RUST_PROC --> KAFKA
    ML_PROC --> KAFKA
    SCHEDULER --> KAFKA

    KAFKA --> PG
    KAFKA --> S3
    KAFKA --> ALERT_SVC

    style RUST_PROC fill:#f9f,stroke:#333,stroke-width:4px
    style ML_PROC fill:#bbf,stroke:#333,stroke-width:2px
```

## 🔐 Arquitectura de Seguridad

```mermaid
graph TB
    subgraph "Zona Externa - Internet"
        INTERNET[fa:fa-globe Internet]
        ATTACKER[fa:fa-user-secret Amenazas]
    end

    subgraph "DMZ - Zona Desmilitarizada"
        FW1[fa:fa-shield-alt Firewall Perimetral]
        WAF[fa:fa-filter WAF<br/>OWASP Protection]
        IDS[fa:fa-eye IDS/IPS<br/>Snort]
        PROXY[fa:fa-server Reverse Proxy<br/>NGINX]
    end

    subgraph "Zona de Aplicación"
        subgraph "Security Layer"
            JWT[fa:fa-key JWT Auth]
            RBAC[fa:fa-users RBAC<br/>4 niveles]
            RATE[fa:fa-tachometer-alt Rate Limiting]
            AUDIT[fa:fa-clipboard Audit Logging]
        end

        APP[fa:fa-code Application<br/>FastAPI + Vue]
    end

    subgraph "Zona de Datos"
        subgraph "Data Security"
            ENCRYPT[fa:fa-lock Encryption<br/>AES-256]
            BACKUP[fa:fa-copy Backup<br/>Encrypted]
            VAULT[fa:fa-vault Secrets Vault]
        end

        DB[(fa:fa-database Database<br/>Row-Level Security)]
    end

    subgraph "Zona Industrial"
        FW2[fa:fa-shield-alt Firewall Industrial]
        DMZ2[fa:fa-network-wired Industrial DMZ]
        SCADA[fa:fa-industry SCADA/DCS]
    end

    INTERNET --> FW1
    ATTACKER -.->|Blocked| FW1
    FW1 --> WAF
    WAF --> IDS
    IDS --> PROXY

    PROXY --> JWT
    JWT --> RBAC
    RBAC --> RATE
    RATE --> APP
    APP --> AUDIT

    APP --> ENCRYPT
    ENCRYPT --> DB
    DB --> BACKUP
    VAULT -.->|Credentials| APP

    APP <--> FW2
    FW2 <--> DMZ2
    DMZ2 <--> SCADA

    style FW1 fill:#f99,stroke:#333,stroke-width:4px
    style WAF fill:#f99,stroke:#333,stroke-width:2px
    style ENCRYPT fill:#9f9,stroke:#333,stroke-width:2px
    style FW2 fill:#f99,stroke:#333,stroke-width:4px
```

## 📈 Pipeline de Machine Learning

```mermaid
graph LR
    subgraph "Data Ingestion"
        RAW[fa:fa-database Raw Data<br/>100K points/sec]
        CLEAN[fa:fa-filter Data Cleaning<br/>Outlier removal]
        FEATURE[fa:fa-cogs Feature Engineering<br/>79 variables]
    end

    subgraph "Model Training"
        SPLIT[fa:fa-cut Train/Test Split<br/>80/20]
        TRAIN[fa:fa-graduation-cap Training<br/>Isolation Forest]
        VALIDATE[fa:fa-check Validation<br/>Cross-validation]
        TUNE[fa:fa-sliders-h Hyperparameter<br/>Tuning]
    end

    subgraph "Model Deployment"
        SERIALIZE[fa:fa-save Model Export<br/>Pickle/ONNX]
        DEPLOY[fa:fa-rocket Deploy<br/>Production]
        MONITOR[fa:fa-chart-line Monitor<br/>Performance]
    end

    subgraph "Inference Pipeline"
        STREAM[fa:fa-stream Real-time Stream]
        PREDICT[fa:fa-magic Prediction<br/>< 10ms latency]
        ACTION[fa:fa-bolt Action<br/>Alert/Report]
    end

    subgraph "Feedback Loop"
        FEEDBACK[fa:fa-sync Feedback<br/>From operators]
        RETRAIN[fa:fa-redo Retrain<br/>Monthly]
        VERSION[fa:fa-code-branch Versioning<br/>MLflow]
    end

    RAW --> CLEAN
    CLEAN --> FEATURE
    FEATURE --> SPLIT

    SPLIT --> TRAIN
    TRAIN --> VALIDATE
    VALIDATE --> TUNE
    TUNE --> SERIALIZE

    SERIALIZE --> DEPLOY
    DEPLOY --> MONITOR

    STREAM --> PREDICT
    PREDICT --> ACTION

    ACTION --> FEEDBACK
    FEEDBACK --> RETRAIN
    RETRAIN --> VERSION
    VERSION --> DEPLOY

    style PREDICT fill:#bbf,stroke:#333,stroke-width:4px
    style TRAIN fill:#f9f,stroke:#333,stroke-width:2px
```

## 🌐 Arquitectura de Alta Disponibilidad

```mermaid
graph TB
    subgraph "Users"
        USER1[fa:fa-user Usuario 1]
        USER2[fa:fa-user Usuario 2]
        USER3[fa:fa-user Usuario N]
    end

    subgraph "CDN Layer"
        CDN[fa:fa-globe CloudFlare CDN<br/>Global Distribution]
    end

    subgraph "Load Balancing"
        LB1[fa:fa-balance-scale LB Primary<br/>NGINX]
        LB2[fa:fa-balance-scale LB Secondary<br/>HAProxy]
    end

    subgraph "Region 1 - Primary"
        subgraph "App Cluster 1"
            APP1A[fa:fa-server App Node 1A]
            APP1B[fa:fa-server App Node 1B]
            APP1C[fa:fa-server App Node 1C]
        end

        subgraph "DB Cluster 1"
            DB1_PRIMARY[(fa:fa-database DB Primary)]
            DB1_REPLICA1[(fa:fa-database Replica 1)]
            DB1_REPLICA2[(fa:fa-database Replica 2)]
        end

        REDIS1[(fa:fa-bolt Redis Cluster 1)]
    end

    subgraph "Region 2 - DR Site"
        subgraph "App Cluster 2"
            APP2A[fa:fa-server App Node 2A]
            APP2B[fa:fa-server App Node 2B]
        end

        subgraph "DB Cluster 2"
            DB2_STANDBY[(fa:fa-database DB Standby)]
            DB2_REPLICA[(fa:fa-database Replica)]
        end

        REDIS2[(fa:fa-bolt Redis Cluster 2)]
    end

    subgraph "Backup & Recovery"
        BACKUP[fa:fa-archive Backup Storage<br/>S3 + Glacier]
        SNAPSHOT[fa:fa-camera Snapshots<br/>Every 4 hours]
    end

    USER1 --> CDN
    USER2 --> CDN
    USER3 --> CDN

    CDN --> LB1
    CDN -.->|Failover| LB2

    LB1 --> APP1A
    LB1 --> APP1B
    LB1 --> APP1C

    APP1A --> DB1_PRIMARY
    APP1B --> DB1_PRIMARY
    APP1C --> DB1_PRIMARY

    DB1_PRIMARY -->|Sync| DB1_REPLICA1
    DB1_PRIMARY -->|Sync| DB1_REPLICA2
    DB1_PRIMARY -->|Async| DB2_STANDBY

    APP1A --> REDIS1
    APP1B --> REDIS1
    APP1C --> REDIS1

    LB2 -.-> APP2A
    LB2 -.-> APP2B

    APP2A -.-> DB2_STANDBY
    APP2B -.-> DB2_STANDBY

    DB2_STANDBY -->|Sync| DB2_REPLICA

    APP2A -.-> REDIS2
    APP2B -.-> REDIS2

    DB1_PRIMARY --> BACKUP
    DB1_PRIMARY --> SNAPSHOT
    DB2_STANDBY --> BACKUP

    style DB1_PRIMARY fill:#9f9,stroke:#333,stroke-width:4px
    style LB1 fill:#99f,stroke:#333,stroke-width:2px
```

## 🔌 Integración SCADA/OPC UA

```mermaid
graph TB
    subgraph "Field Equipment Layer"
        subgraph "Oil Production"
            ESP[fa:fa-fan ESP Pumps]
            SEP[fa:fa-filter Separators]
            TANK[fa:fa-database Storage Tanks]
        end

        subgraph "Gas Processing"
            COMP[fa:fa-compress Compressors]
            DEHYD[fa:fa-tint Dehydrators]
            METER[fa:fa-tachometer-alt Gas Meters]
        end

        subgraph "Water Management"
            INJECT[fa:fa-syringe Injection Pumps]
            TREAT[fa:fa-recycle Treatment Units]
        end
    end

    subgraph "Control Systems"
        subgraph "DCS/SCADA Vendors"
            ABB[ABB System 800xA]
            SCHNEIDER[Schneider EcoStruxure]
            HONEYWELL[Honeywell Experion]
            EMERSON[Emerson DeltaV]
        end
    end

    subgraph "Communication Protocols"
        subgraph "Industrial Standards"
            OPCUA_SERVER[fa:fa-server OPC UA Server<br/>IEC 62541]
            MODBUS_GW[fa:fa-exchange-alt Modbus Gateway<br/>TCP/RTU]
            MQTT_BROKER[fa:fa-broadcast-tower MQTT Broker<br/>Sparkplug B]
        end
    end

    subgraph "ANH Reporter Integration"
        subgraph "Protocol Adapters"
            OPCUA_CLIENT[OPC UA Client<br/>Async, Subscriptions]
            MODBUS_CLIENT[Modbus Client<br/>Batch Reading]
            MQTT_CLIENT[MQTT Client<br/>QoS 2]
        end

        MAPPER[fa:fa-map Variable Mapper<br/>Tag → ANH Format]
        BUFFER[fa:fa-memory Buffer Manager<br/>Offline Capable]
    end

    subgraph "Data Processing"
        PROCESSOR[fa:fa-microchip Rust Processor<br/>Real-time]
    end

    ESP --> ABB
    SEP --> SCHNEIDER
    TANK --> HONEYWELL
    COMP --> EMERSON
    DEHYD --> ABB
    METER --> SCHNEIDER
    INJECT --> HONEYWELL
    TREAT --> EMERSON

    ABB --> OPCUA_SERVER
    SCHNEIDER --> MODBUS_GW
    HONEYWELL --> OPCUA_SERVER
    EMERSON --> MQTT_BROKER

    OPCUA_SERVER --> OPCUA_CLIENT
    MODBUS_GW --> MODBUS_CLIENT
    MQTT_BROKER --> MQTT_CLIENT

    OPCUA_CLIENT --> MAPPER
    MODBUS_CLIENT --> MAPPER
    MQTT_CLIENT --> MAPPER

    MAPPER --> BUFFER
    BUFFER --> PROCESSOR

    style OPCUA_SERVER fill:#9f9,stroke:#333,stroke-width:2px
    style PROCESSOR fill:#f9f,stroke:#333,stroke-width:4px
```

## 📊 Dashboard de Monitoreo en Tiempo Real

```mermaid
graph TB
    subgraph "Dashboard Principal"
        subgraph "KPIs Principales"
            PROD[fa:fa-oil-can Producción<br/>15,234 bbl/día]
            GAS[fa:fa-fire Gas<br/>45.6 MMSCF/día]
            WATER[fa:fa-tint Agua<br/>8,450 bbl/día]
            QUALITY[fa:fa-star Calidad<br/>99.8%]
        end

        subgraph "Gráficos en Tiempo Real"
            TREND[fa:fa-chart-line Tendencia 24h]
            GAUGE[fa:fa-tachometer-alt Gauges]
            MAP[fa:fa-map Mapa de Campos]
            HEATMAP[fa:fa-th Heatmap Variables]
        end

        subgraph "Alertas Activas"
            CRITICAL[fa:fa-exclamation-triangle Críticas: 0]
            WARNING[fa:fa-exclamation-circle Warnings: 2]
            INFO[fa:fa-info-circle Info: 5]
        end

        subgraph "Estado ANH"
            COMPLIANCE[fa:fa-check-circle Cumplimiento: 100%]
            NEXT[fa:fa-clock Próximo: 6:00 AM]
            HISTORY[fa:fa-history Historial: 30 días]
        end
    end

    subgraph "Data Sources"
        WS[fa:fa-plug WebSocket<br/>Real-time]
        API[fa:fa-server REST API<br/>Historical]
        CACHE[fa:fa-bolt Cache<br/>Redis]
    end

    WS --> TREND
    WS --> GAUGE
    API --> MAP
    API --> HEATMAP
    CACHE --> PROD
    CACHE --> GAS
    CACHE --> WATER
    CACHE --> QUALITY

    style QUALITY fill:#9f9,stroke:#333,stroke-width:2px
    style COMPLIANCE fill:#9f9,stroke:#333,stroke-width:2px
```

## 🔄 CI/CD Pipeline

```mermaid
graph LR
    subgraph "Development"
        DEV[fa:fa-code Developer<br/>Local Env]
        GIT[fa:fa-code-branch Git Push<br/>Feature Branch]
    end

    subgraph "CI Pipeline"
        subgraph "Build Stage"
            LINT[fa:fa-check Linting<br/>ESLint, Black]
            BUILD[fa:fa-hammer Build<br/>Docker Images]
            TEST[fa:fa-vial Tests<br/>Unit + Integration]
        end

        subgraph "Security Stage"
            SAST[fa:fa-shield-alt SAST<br/>Semgrep]
            DEPS[fa:fa-lock Dependency<br/>Check]
            SCAN[fa:fa-search Container<br/>Scan]
        end
    end

    subgraph "CD Pipeline"
        subgraph "Staging"
            DEPLOY_STG[fa:fa-rocket Deploy<br/>Staging]
            E2E[fa:fa-robot E2E Tests<br/>Cypress]
            PERF[fa:fa-tachometer-alt Performance<br/>Tests]
        end

        subgraph "Production"
            APPROVE[fa:fa-user-check Manual<br/>Approval]
            DEPLOY_PROD[fa:fa-rocket Deploy<br/>Production]
            MONITOR[fa:fa-chart-line Monitor<br/>Metrics]
        end
    end

    subgraph "Feedback"
        ALERT[fa:fa-bell Alerts]
        ROLLBACK[fa:fa-undo Rollback<br/>if needed]
    end

    DEV --> GIT
    GIT --> LINT
    LINT --> BUILD
    BUILD --> TEST

    TEST --> SAST
    SAST --> DEPS
    DEPS --> SCAN

    SCAN --> DEPLOY_STG
    DEPLOY_STG --> E2E
    E2E --> PERF

    PERF --> APPROVE
    APPROVE --> DEPLOY_PROD
    DEPLOY_PROD --> MONITOR

    MONITOR --> ALERT
    ALERT -.->|Issues| ROLLBACK
    ROLLBACK -.-> DEPLOY_PROD

    style TEST fill:#9f9,stroke:#333,stroke-width:2px
    style DEPLOY_PROD fill:#f9f,stroke:#333,stroke-width:4px
```

## 🌍 Arquitectura Multi-Tenant

```mermaid
graph TB
    subgraph "Tenant Layer"
        T1[fa:fa-building Ecopetrol<br/>Tenant 1]
        T2[fa:fa-building Frontera<br/>Tenant 2]
        T3[fa:fa-building GeoPark<br/>Tenant 3]
    end

    subgraph "API Gateway"
        GATEWAY[fa:fa-door-open API Gateway<br/>Tenant Routing]
        AUTH[fa:fa-key Auth & Tenant ID]
    end

    subgraph "Application Layer"
        subgraph "Shared Services"
            SHARED_APP[fa:fa-server Shared App Servers]
            SHARED_CACHE[fa:fa-bolt Shared Cache]
        end

        subgraph "Tenant Isolation"
            ISO[fa:fa-lock Tenant Isolation<br/>Middleware]
        end
    end

    subgraph "Data Layer"
        subgraph "Database Isolation"
            DB_T1[(fa:fa-database Schema T1<br/>Ecopetrol)]
            DB_T2[(fa:fa-database Schema T2<br/>Frontera)]
            DB_T3[(fa:fa-database Schema T3<br/>GeoPark)]
        end

        subgraph "Shared Infrastructure"
            SHARED_DB[fa:fa-server PostgreSQL Cluster]
        end
    end

    subgraph "Storage Layer"
        subgraph "Isolated Storage"
            S3_T1[fa:fa-folder /tenant1/*]
            S3_T2[fa:fa-folder /tenant2/*]
            S3_T3[fa:fa-folder /tenant3/*]
        end
    end

    T1 --> GATEWAY
    T2 --> GATEWAY
    T3 --> GATEWAY

    GATEWAY --> AUTH
    AUTH --> ISO

    ISO --> SHARED_APP
    SHARED_APP --> SHARED_CACHE

    ISO -->|Tenant 1| DB_T1
    ISO -->|Tenant 2| DB_T2
    ISO -->|Tenant 3| DB_T3

    DB_T1 --> SHARED_DB
    DB_T2 --> SHARED_DB
    DB_T3 --> SHARED_DB

    ISO -->|Tenant 1| S3_T1
    ISO -->|Tenant 2| S3_T2
    ISO -->|Tenant 3| S3_T3

    style ISO fill:#f99,stroke:#333,stroke-width:4px
    style AUTH fill:#99f,stroke:#333,stroke-width:2px
```

---

## 📐 Resumen de Componentes Técnicos

### Tecnologías Core

| Componente | Tecnología | Versión | Función |
|------------|------------|---------|----------|
| **Backend** | FastAPI | 0.104+ | REST API |
| **Processing** | Rust | 1.75+ | High-performance |
| **Frontend** | Vue.js | 3.3+ | SPA Dashboard |
| **Database** | PostgreSQL | 15+ | Data persistence |
| **Time Series** | TimescaleDB | 2.13+ | Telemetry storage |
| **Cache** | Redis | 7+ | In-memory cache |
| **ML Framework** | scikit-learn | 1.3+ | Anomaly detection |
| **Container** | Docker | 24+ | Containerization |
| **Orchestration** | Docker Compose | 2.23+ | Local deployment |
| **Monitoring** | Prometheus | 2.47+ | Metrics collection |
| **Visualization** | Grafana | 10.2+ | Dashboards |

### Protocolos Industriales Soportados

| Protocolo | Estándar | Uso |
|-----------|----------|-----|
| **OPC UA** | IEC 62541 | SCADA moderno |
| **Modbus** | TCP/RTU | PLCs legacy |
| **MQTT** | v5.0 | IoT devices |
| **IEC 61850** | Ed 2.0 | Power systems |
| **DNP3** | IEEE 1815 | Telemetría remota |
| **IEC 60870-5-104** | IEC 60870 | Utilities |

### Métricas de Performance

| Métrica | Valor | Condición |
|---------|-------|-----------|
| **Throughput** | 100K msgs/sec | Peak load |
| **Latency** | < 1ms | P99 |
| **Availability** | 99.95% | Annual |
| **RPO** | 15 min | Recovery Point |
| **RTO** | 1 hour | Recovery Time |
| **MTBF** | 2500 hours | Reliability |
| **MTTR** | < 30 min | Maintainability |

---

*Documentación visual actualizada: Noviembre 2025 | v3.0.0*