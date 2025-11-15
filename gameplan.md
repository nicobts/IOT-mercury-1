# 1NCE API Visualization Platform - Development Game Plan

## 📋 Project Overview

**Project Name:** 1NCE IoT Management Dashboard  
**Tech Stack:** Streamlit + PostgreSQL/TimescaleDB + Docker  
**Target:** Full-featured SIM card management and analytics platform  
**Development Timeline:** 8-12 weeks (based on 20-30 hours/week)

---

## 🎯 Project Goals

1. **Comprehensive API Integration:** Leverage all 1NCE API endpoints
2. **Real-time Monitoring:** Live SIM status, usage, and connectivity tracking
3. **Historical Analytics:** 6-month usage trends and patterns
4. **Bulk Management:** CSV/XLSX import for managing multiple SIMs
5. **Alerting System:** Quota warnings and connectivity issues
6. **Production-Ready:** Dockerized, secure, and scalable

---

## 🗂️ Table of Contents

1. [Phase 0: Planning & Setup (Week 1)](#phase-0-planning--setup-week-1)
2. [Phase 1: Foundation (Weeks 2-3)](#phase-1-foundation-weeks-2-3)
3. [Phase 2: Core Features (Weeks 4-6)](#phase-2-core-features-weeks-4-6)
4. [Phase 3: Advanced Features (Weeks 7-8)](#phase-3-advanced-features-weeks-7-8)
5. [Phase 4: Testing & Optimization (Week 9)](#phase-4-testing--optimization-week-9)
6. [Phase 5: Deployment (Weeks 10-11)](#phase-5-deployment-weeks-10-11)
7. [Phase 6: Documentation & Handover (Week 12)](#phase-6-documentation--handover-week-12)

---

## Phase 0: Planning & Setup (Week 1)

### 📝 Day 1-2: Requirements & Architecture

#### Tasks:
- [ ] **Define detailed requirements**
  - List all features needed
  - Prioritize must-have vs nice-to-have
  - Define success criteria
  
- [ ] **Create architecture diagram**
  - System components
  - Data flow
  - Integration points
  
- [ ] **Set up project management**
  - Create GitHub repository
  - Set up project board (GitHub Projects or Trello)
  - Define sprint/milestone structure

#### Deliverables:
- `requirements.md` - Detailed requirements document
- `architecture.png` - System architecture diagram
- GitHub repository with initial README

---

### 🛠️ Day 3-4: Development Environment Setup

#### Tasks:
- [ ] **Install required software**
  ```bash
  # macOS/Linux
  brew install python3.11
  brew install postgresql
  brew install docker
  brew install docker-compose
  
  # Or use Docker for everything
  docker --version
  docker-compose --version
  ```

- [ ] **Set up Python virtual environment**
  ```bash
  python3.11 -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install --upgrade pip
  ```

- [ ] **Create project structure**
  ```
  onence-dashboard/
  ├── .env.example
  ├── .env
  ├── .gitignore
  ├── docker-compose.yml
  ├── Dockerfile
  ├── requirements.txt
  ├── README.md
  ├── gameplan.md
  ├── src/
  │   ├── __init__.py
  │   ├── app.py                    # Main Streamlit app
  │   ├── config.py                 # Configuration management
  │   ├── database/
  │   │   ├── __init__.py
  │   │   ├── models.py             # SQLAlchemy models
  │   │   ├── connection.py         # Database connection
  │   │   └── migrations/           # Alembic migrations
  │   ├── api/
  │   │   ├── __init__.py
  │   │   ├── auth_manager.py       # 1NCE authentication
  │   │   ├── client.py             # API client
  │   │   └── endpoints/
  │   │       ├── sims.py
  │   │       ├── usage.py
  │   │       ├── connectivity.py
  │   │       └── events.py
  │   ├── services/
  │   │   ├── __init__.py
  │   │   ├── data_collector.py     # Background data collection
  │   │   ├── alert_service.py      # Alert logic
  │   │   └── file_processor.py     # CSV/XLSX processing
  │   ├── utils/
  │   │   ├── __init__.py
  │   │   ├── logger.py             # Logging configuration
  │   │   ├── validators.py         # Input validation
  │   │   └── formatters.py         # Data formatting
  │   ├── pages/
  │   │   ├── 1_📊_Overview.py
  │   │   ├── 2_📈_Usage_Analytics.py
  │   │   ├── 3_📱_SIM_Management.py
  │   │   ├── 4_🔌_Connectivity.py
  │   │   ├── 5_📤_Import_Export.py
  │   │   ├── 6_⚙️_Settings.py
  │   │   └── 7_📊_Reports.py
  │   └── components/
  │       ├── __init__.py
  │       ├── charts.py             # Reusable chart components
  │       ├── tables.py             # Data table components
  │       └── alerts.py             # Alert components
  ├── tests/
  │   ├── __init__.py
  │   ├── test_api_client.py
  │   ├── test_auth.py
  │   ├── test_database.py
  │   └── test_services.py
  ├── scripts/
  │   ├── init_db.py                # Database initialization
  │   ├── seed_data.py              # Sample data for testing
  │   └── worker.py                 # Background worker
  └── docs/
      ├── api_documentation.md
      ├── deployment.md
      └── user_guide.md
  ```

- [ ] **Initialize Git repository**
  ```bash
  git init
  git add .
  git commit -m "Initial project structure"
  git remote add origin <your-repo-url>
  git push -u origin main
  ```

#### Deliverables:
- Complete project structure
- Git repository initialized
- Development environment ready

---

### 📚 Day 5-7: Initial Dependencies & Docker Setup

#### Tasks:
- [ ] **Create `requirements.txt`**
  ```txt
  # Core Framework
  streamlit==1.31.0
  
  # API & HTTP
  requests==2.31.0
  httpx==0.26.0
  
  # Database
  sqlalchemy==2.0.25
  psycopg2-binary==2.9.9
  alembic==1.13.1
  
  # Time-series extension
  # (TimescaleDB is PostgreSQL extension, no Python package needed)
  
  # Data Processing
  pandas==2.2.0
  openpyxl==3.1.2
  xlsxwriter==3.1.9
  
  # Visualization
  plotly==5.18.0
  altair==5.2.0
  
  # Scheduling
  apscheduler==3.10.4
  
  # Utilities
  python-dotenv==1.0.1
  pydantic==2.5.3
  pydantic-settings==2.1.0
  
  # Caching
  redis==5.0.1
  
  # Logging
  loguru==0.7.2
  
  # Testing
  pytest==8.0.0
  pytest-cov==4.1.0
  pytest-asyncio==0.23.3
  
  # Type checking
  mypy==1.8.0
  
  # Code quality
  black==24.1.1
  flake8==7.0.0
  isort==5.13.2
  ```

- [ ] **Create `docker-compose.yml`**
  ```yaml
  version: '3.8'
  
  services:
    # Streamlit Dashboard Application
    dashboard:
      build:
        context: .
        dockerfile: Dockerfile
      container_name: onence-dashboard
      ports:
        - "8501:8501"
      environment:
        - DATABASE_URL=postgresql://onence_user:onence_password@db:5432/onence_db
        - REDIS_URL=redis://redis:6379/0
        - ONENCE_USERNAME=${ONENCE_USERNAME}
        - ONENCE_PASSWORD=${ONENCE_PASSWORD}
        - ENVIRONMENT=development
        - LOG_LEVEL=INFO
      volumes:
        - ./src:/app/src
        - ./uploads:/app/uploads
        - ./logs:/app/logs
      depends_on:
        db:
          condition: service_healthy
        redis:
          condition: service_healthy
      restart: unless-stopped
      networks:
        - onence-network
  
    # PostgreSQL with TimescaleDB
    db:
      image: timescale/timescaledb:latest-pg15
      container_name: onence-postgres
      environment:
        - POSTGRES_USER=onence_user
        - POSTGRES_PASSWORD=onence_password
        - POSTGRES_DB=onence_db
      ports:
        - "5432:5432"
      volumes:
        - postgres_data:/var/lib/postgresql/data
        - ./scripts/init_db.sql:/docker-entrypoint-initdb.d/init_db.sql
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U onence_user -d onence_db"]
        interval: 10s
        timeout: 5s
        retries: 5
      restart: unless-stopped
      networks:
        - onence-network
  
    # Redis for caching and task queue
    redis:
      image: redis:7-alpine
      container_name: onence-redis
      ports:
        - "6379:6379"
      volumes:
        - redis_data:/data
      healthcheck:
        test: ["CMD", "redis-cli", "ping"]
        interval: 10s
        timeout: 3s
        retries: 5
      restart: unless-stopped
      networks:
        - onence-network
  
    # Background Worker for data collection
    worker:
      build:
        context: .
        dockerfile: Dockerfile
      container_name: onence-worker
      command: python scripts/worker.py
      environment:
        - DATABASE_URL=postgresql://onence_user:onence_password@db:5432/onence_db
        - REDIS_URL=redis://redis:6379/0
        - ONENCE_USERNAME=${ONENCE_USERNAME}
        - ONENCE_PASSWORD=${ONENCE_PASSWORD}
        - ENVIRONMENT=development
        - LOG_LEVEL=INFO
      volumes:
        - ./src:/app/src
        - ./logs:/app/logs
      depends_on:
        db:
          condition: service_healthy
        redis:
          condition: service_healthy
      restart: unless-stopped
      networks:
        - onence-network
  
    # Optional: Grafana for advanced visualization
    grafana:
      image: grafana/grafana:latest
      container_name: onence-grafana
      ports:
        - "3000:3000"
      environment:
        - GF_SECURITY_ADMIN_USER=admin
        - GF_SECURITY_ADMIN_PASSWORD=admin
        - GF_INSTALL_PLUGINS=
      volumes:
        - grafana_data:/var/lib/grafana
        - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
        - ./grafana/datasources:/etc/grafana/provisioning/datasources
      depends_on:
        - db
      restart: unless-stopped
      networks:
        - onence-network
  
    # Optional: pgAdmin for database management
    pgadmin:
      image: dpage/pgadmin4:latest
      container_name: onence-pgadmin
      ports:
        - "5050:80"
      environment:
        - PGADMIN_DEFAULT_EMAIL=admin@onence.local
        - PGADMIN_DEFAULT_PASSWORD=admin
      volumes:
        - pgadmin_data:/var/lib/pgadmin
      depends_on:
        - db
      restart: unless-stopped
      networks:
        - onence-network
  
  networks:
    onence-network:
      driver: bridge
  
  volumes:
    postgres_data:
    redis_data:
    grafana_data:
    pgadmin_data:
  ```

- [ ] **Create `Dockerfile`**
  ```dockerfile
  FROM python:3.11-slim
  
  # Set working directory
  WORKDIR /app
  
  # Install system dependencies
  RUN apt-get update && apt-get install -y \
      gcc \
      postgresql-client \
      && rm -rf /var/lib/apt/lists/*
  
  # Copy requirements and install Python dependencies
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  
  # Copy application code
  COPY src/ ./src/
  COPY scripts/ ./scripts/
  
  # Create necessary directories
  RUN mkdir -p /app/uploads /app/logs
  
  # Expose Streamlit port
  EXPOSE 8501
  
  # Health check
  HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1
  
  # Run Streamlit
  CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
  ```

- [ ] **Create `.env.example`**
  ```bash
  # 1NCE API Credentials
  ONENCE_USERNAME=your_username_here
  ONENCE_PASSWORD=your_password_here
  
  # Database Configuration
  DATABASE_URL=postgresql://onence_user:onence_password@localhost:5432/onence_db
  
  # Redis Configuration
  REDIS_URL=redis://localhost:6379/0
  
  # Application Settings
  ENVIRONMENT=development
  LOG_LEVEL=INFO
  SECRET_KEY=your-secret-key-here-change-in-production
  
  # Data Collection Settings
  DATA_COLLECTION_INTERVAL_MINUTES=60
  USAGE_RETENTION_DAYS=180
  
  # Alert Settings
  ENABLE_EMAIL_ALERTS=false
  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USERNAME=your_email@gmail.com
  SMTP_PASSWORD=your_app_password
  ALERT_EMAIL_TO=alerts@yourcompany.com
  
  # Optional: Grafana
  GRAFANA_ADMIN_PASSWORD=admin
  
  # Optional: pgAdmin
  PGADMIN_DEFAULT_EMAIL=admin@onence.local
  PGADMIN_DEFAULT_PASSWORD=admin
  ```

- [ ] **Create `.gitignore`**
  ```
  # Python
  __pycache__/
  *.py[cod]
  *$py.class
  *.so
  .Python
  venv/
  env/
  ENV/
  
  # Environment variables
  .env
  
  # IDE
  .vscode/
  .idea/
  *.swp
  *.swo
  
  # Database
  *.db
  *.sqlite3
  
  # Logs
  logs/
  *.log
  
  # Uploads
  uploads/
  
  # OS
  .DS_Store
  Thumbs.db
  
  # Docker
  docker-compose.override.yml
  
  # Testing
  .pytest_cache/
  .coverage
  htmlcov/
  
  # Build
  dist/
  build/
  *.egg-info/
  ```

- [ ] **Test Docker setup**
  ```bash
  # Build images
  docker-compose build
  
  # Start services
  docker-compose up -d
  
  # Check logs
  docker-compose logs -f dashboard
  
  # Verify services are running
  docker-compose ps
  ```

#### Deliverables:
- Working Docker environment
- All services running and healthy
- Streamlit accessible at http://localhost:8501

---

## Phase 1: Foundation (Weeks 2-3)

### 🗄️ Week 2, Day 1-3: Database Setup

#### Tasks:
- [ ] **Create database models** (`src/database/models.py`)
  ```python
  from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
  from sqlalchemy.ext.declarative import declarative_base
  from sqlalchemy.orm import relationship
  from datetime import datetime
  
  Base = declarative_base()
  
  class SIMCard(Base):
      """SIM Card master data"""
      __tablename__ = 'sim_cards'
      
      id = Column(Integer, primary_key=True)
      iccid = Column(String(20), unique=True, nullable=False, index=True)
      iccid_with_luhn = Column(String(21))
      imsi = Column(String(15))
      imsi_2 = Column(String(15))
      current_imsi = Column(String(15))
      msisdn = Column(String(15))
      imei = Column(String(15))
      imei_lock = Column(Boolean, default=False)
      status = Column(String(20))  # Enabled/Disabled
      activation_date = Column(DateTime)
      ip_address = Column(String(15))
      label = Column(String(255))
      
      # Quota information
      current_quota_mb = Column(Float)
      quota_status_id = Column(Integer)
      quota_threshold_date = Column(DateTime)
      quota_exceeded_date = Column(DateTime)
      
      current_quota_sms = Column(Integer)
      quota_sms_status_id = Column(Integer)
      quota_sms_threshold_date = Column(DateTime)
      quota_sms_exceeded_date = Column(DateTime)
      
      # Metadata
      created_at = Column(DateTime, default=datetime.utcnow)
      updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
      last_synced_at = Column(DateTime)
      
      # Relationships
      usage_records = relationship("UsageRecord", back_populates="sim_card", cascade="all, delete-orphan")
      events = relationship("SIMEvent", back_populates="sim_card", cascade="all, delete-orphan")
      connectivity_logs = relationship("ConnectivityLog", back_populates="sim_card", cascade="all, delete-orphan")
  
  
  class UsageRecord(Base):
      """Daily usage records (time-series data)"""
      __tablename__ = 'usage_records'
      
      id = Column(Integer, primary_key=True)
      sim_card_id = Column(Integer, ForeignKey('sim_cards.id'), nullable=False)
      date = Column(DateTime, nullable=False, index=True)
      
      # Data usage
      data_volume_mb = Column(Float, default=0)
      data_volume_rx_mb = Column(Float, default=0)
      data_volume_tx_mb = Column(Float, default=0)
      
      # SMS usage
      sms_volume = Column(Integer, default=0)
      sms_volume_mo = Column(Integer, default=0)  # Mobile Originated
      sms_volume_mt = Column(Integer, default=0)  # Mobile Terminated
      
      # Metadata
      created_at = Column(DateTime, default=datetime.utcnow)
      
      # Relationships
      sim_card = relationship("SIMCard", back_populates="usage_records")
      
      # Create hypertable for TimescaleDB (done in migration)
      __table_args__ = (
          # Composite index for efficient queries
          {'timescaledb_hypertable': {'time_column_name': 'date'}},
      )
  
  
  class SIMEvent(Base):
      """SIM card events"""
      __tablename__ = 'sim_events'
      
      id = Column(Integer, primary_key=True)
      sim_card_id = Column(Integer, ForeignKey('sim_cards.id'), nullable=False)
      event_type = Column(String(50), nullable=False)
      event_description = Column(String(500))
      event_data = Column(JSON)
      occurred_at = Column(DateTime, nullable=False, index=True)
      created_at = Column(DateTime, default=datetime.utcnow)
      
      # Relationships
      sim_card = relationship("SIMCard", back_populates="events")
  
  
  class ConnectivityLog(Base):
      """Connectivity and location logs"""
      __tablename__ = 'connectivity_logs'
      
      id = Column(Integer, primary_key=True)
      sim_card_id = Column(Integer, ForeignKey('sim_cards.id'), nullable=False)
      
      # Location data
      current_location_retrieved = Column(Boolean)
      age_of_location_minutes = Column(Integer)
      cid = Column(Integer)  # Cell ID
      lac = Column(Integer)  # Location Area Code
      mcc = Column(String(3))  # Mobile Country Code
      mnc = Column(String(3))  # Mobile Network Code
      
      # Timestamps
      request_timestamp = Column(DateTime)
      reply_timestamp = Column(DateTime)
      created_at = Column(DateTime, default=datetime.utcnow)
      
      # Relationships
      sim_card = relationship("SIMCard", back_populates="connectivity_logs")
  
  
  class Alert(Base):
      """System alerts"""
      __tablename__ = 'alerts'
      
      id = Column(Integer, primary_key=True)
      sim_card_id = Column(Integer, ForeignKey('sim_cards.id'), nullable=True)
      alert_type = Column(String(50), nullable=False)  # quota_warning, connectivity_issue, etc.
      severity = Column(String(20))  # info, warning, critical
      message = Column(String(500))
      is_resolved = Column(Boolean, default=False)
      created_at = Column(DateTime, default=datetime.utcnow, index=True)
      resolved_at = Column(DateTime)
  
  
  class DataCollectionLog(Base):
      """Log of data collection runs"""
      __tablename__ = 'data_collection_logs'
      
      id = Column(Integer, primary_key=True)
      collection_type = Column(String(50))  # full_sync, usage_update, etc.
      started_at = Column(DateTime, default=datetime.utcnow)
      completed_at = Column(DateTime)
      status = Column(String(20))  # success, failed, partial
      sims_processed = Column(Integer, default=0)
      errors_count = Column(Integer, default=0)
      error_details = Column(JSON)
  ```

- [ ] **Create database connection** (`src/database/connection.py`)
  ```python
  from sqlalchemy import create_engine, event
  from sqlalchemy.orm import sessionmaker, Session
  from sqlalchemy.pool import NullPool
  from contextlib import contextmanager
  from typing import Generator
  import logging
  
  from src.config import config
  from src.database.models import Base
  
  logger = logging.getLogger(__name__)
  
  # Create engine with connection pooling
  engine = create_engine(
      config.DATABASE_URL,
      pool_pre_ping=True,  # Verify connections before using
      pool_size=10,
      max_overflow=20,
      echo=config.ENVIRONMENT == "development",  # Log SQL in development
  )
  
  # Create session factory
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  
  
  def init_db():
      """Initialize database tables"""
      try:
          Base.metadata.create_all(bind=engine)
          
          # Enable TimescaleDB extension and create hypertable
          with engine.connect() as conn:
              # Enable TimescaleDB
              conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
              
              # Create hypertable for usage_records
              conn.execute("""
                  SELECT create_hypertable(
                      'usage_records',
                      'date',
                      if_not_exists => TRUE
                  );
              """)
              
              conn.commit()
              
          logger.info("Database initialized successfully")
      except Exception as e:
          logger.error(f"Failed to initialize database: {e}")
          raise
  
  
  @contextmanager
  def get_db() -> Generator[Session, None, None]:
      """
      Context manager for database sessions
      
      Usage:
          with get_db() as db:
              sim = db.query(SIMCard).first()
      """
      db = SessionLocal()
      try:
          yield db
          db.commit()
      except Exception:
          db.rollback()
          raise
      finally:
          db.close()
  
  
  def get_db_session() -> Session:
      """Get database session (for dependency injection)"""
      return SessionLocal()
  ```

- [ ] **Create initial migration script** (`scripts/init_db.sql`)
  ```sql
  -- Enable TimescaleDB extension
  CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
  
  -- Create custom types
  CREATE TYPE sim_status AS ENUM ('Enabled', 'Disabled');
  CREATE TYPE alert_severity AS ENUM ('info', 'warning', 'critical');
  
  -- Indexes for performance
  CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_usage_records_date 
      ON usage_records (date DESC);
  
  CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_usage_records_sim_date 
      ON usage_records (sim_card_id, date DESC);
  
  CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sim_events_occurred 
      ON sim_events (occurred_at DESC);
  
  CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_alerts_created 
      ON alerts (created_at DESC) WHERE is_resolved = false;
  
  -- Continuous aggregates for performance (TimescaleDB feature)
  CREATE MATERIALIZED VIEW IF NOT EXISTS weekly_usage_summary
  WITH (timescaledb.continuous) AS
  SELECT 
      sim_card_id,
      time_bucket('7 days', date) AS week,
      SUM(data_volume_mb) as total_data_mb,
      SUM(sms_volume) as total_sms,
      AVG(data_volume_mb) as avg_daily_data_mb
  FROM usage_records
  GROUP BY sim_card_id, week;
  
  -- Refresh policy for continuous aggregate
  SELECT add_continuous_aggregate_policy('weekly_usage_summary',
      start_offset => INTERVAL '1 month',
      end_offset => INTERVAL '1 day',
      schedule_interval => INTERVAL '1 day');
  
  -- Retention policy (keep 6 months of raw data)
  SELECT add_retention_policy('usage_records', INTERVAL '180 days');
  ```

- [ ] **Test database connection**
  ```bash
  # From container
  docker-compose exec dashboard python -c "from src.database.connection import init_db; init_db()"
  
  # Check tables created
  docker-compose exec db psql -U onence_user -d onence_db -c "\dt"
  ```

#### Deliverables:
- Complete database schema
- TimescaleDB hypertables configured
- Database connection working

---

### 🔐 Week 2, Day 4-7: API Integration

#### Tasks:
- [ ] **Create configuration management** (`src/config.py`)
  ```python
  from pydantic_settings import BaseSettings, SettingsConfigDict
  from typing import Optional
  
  
  class Settings(BaseSettings):
      """Application settings from environment variables"""
      
      model_config = SettingsConfigDict(
          env_file='.env',
          env_file_encoding='utf-8',
          case_sensitive=False
      )
      
      # 1NCE API
      ONENCE_USERNAME: str
      ONENCE_PASSWORD: str
      ONENCE_API_BASE_URL: str = "https://api.1nce.com/management-api"
      
      # Database
      DATABASE_URL: str
      
      # Redis
      REDIS_URL: str = "redis://localhost:6379/0"
      
      # Application
      ENVIRONMENT: str = "development"
      LOG_LEVEL: str = "INFO"
      SECRET_KEY: str = "change-me-in-production"
      
      # Data Collection
      DATA_COLLECTION_INTERVAL_MINUTES: int = 60
      USAGE_RETENTION_DAYS: int = 180
      
      # Alerts
      ENABLE_EMAIL_ALERTS: bool = False
      SMTP_SERVER: Optional[str] = None
      SMTP_PORT: int = 587
      SMTP_USERNAME: Optional[str] = None
      SMTP_PASSWORD: Optional[str] = None
      ALERT_EMAIL_TO: Optional[str] = None
      
      def validate(self):
          """Validate required settings"""
          if not self.ONENCE_USERNAME or not self.ONENCE_PASSWORD:
              raise ValueError("1NCE credentials not configured")
          return self
  
  
  # Global config instance
  config = Settings().validate()
  ```

- [ ] **Implement authentication manager** (`src/api/auth_manager.py`)
  ```python
  import requests
  import base64
  from datetime import datetime, timedelta
  from typing import Optional
  from threading import Lock
  import logging
  
  logger = logging.getLogger(__name__)
  
  
  class OnceAuthManager:
      """Manages authentication for 1NCE API with automatic token refresh"""
      
      def __init__(self, username: str, password: str, base_url: str):
          self.username = username
          self.password = password
          self.base_url = base_url
          
          # Token management
          self._access_token: Optional[str] = None
          self._token_expires_at: Optional[datetime] = None
          self._lock = Lock()
          
          # Buffer time before expiry to refresh token (5 minutes)
          self.refresh_buffer = timedelta(minutes=5)
      
      def _get_basic_auth_header(self) -> str:
          """Create Basic Authentication header"""
          credentials = f"{self.username}:{self.password}"
          encoded = base64.b64encode(credentials.encode()).decode()
          return f"Basic {encoded}"
      
      def _obtain_token(self) -> dict:
          """Obtain a new access token from 1NCE API"""
          url = f"{self.base_url}/oauth/token"
          
          headers = {
              "Authorization": self._get_basic_auth_header(),
              "Content-Type": "application/json",
              "Accept": "application/json"
          }
          
          payload = {"grant_type": "client_credentials"}
          
          try:
              response = requests.post(url, json=payload, headers=headers, timeout=10)
              response.raise_for_status()
              
              token_data = response.json()
              logger.info("Successfully obtained new access token")
              return token_data
              
          except requests.exceptions.HTTPError as e:
              if e.response.status_code == 400:
                  error_data = e.response.json()
                  error_msg = error_data.get('message', 'Unknown error')
                  logger.error(f"Authentication failed: {error_msg}")
                  raise Exception(f"1NCE Authentication Error: {error_msg}")
              raise
          except requests.exceptions.RequestException as e:
              logger.error(f"Failed to obtain token: {e}")
              raise
      
      def _is_token_valid(self) -> bool:
          """Check if current token is valid and not about to expire"""
          if not self._access_token or not self._token_expires_at:
              return False
          
          return datetime.now() < (self._token_expires_at - self.refresh_buffer)
      
      def get_token(self) -> str:
          """Get valid access token, refreshing if necessary"""
          with self._lock:
              if self._is_token_valid():
                  return self._access_token
              
              logger.info("Token expired or missing, obtaining new token...")
              token_data = self._obtain_token()
              
              self._access_token = token_data['access_token']
              expires_in = token_data.get('expires_in', 3600)
              self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)
              
              logger.info(f"New token obtained, expires at {self._token_expires_at}")
              return self._access_token
      
      def get_auth_headers(self) -> dict:
          """Get headers with valid Bearer token"""
          token = self.get_token()
          return {
              "Authorization": f"Bearer {token}",
              "Content-Type": "application/json",
              "Accept": "application/json"
          }
      
      def invalidate_token(self):
          """Force token refresh on next request"""
          with self._lock:
              self._access_token = None
              self._token_expires_at = None
              logger.info("Token invalidated")
  ```

- [ ] **Create API client** (`src/api/client.py`)
  ```python
  import requests
  from typing import Optional, Dict, Any
  import logging
  from datetime import datetime, timedelta
  
  from src.api.auth_manager import OnceAuthManager
  from src.config import config
  
  logger = logging.getLogger(__name__)
  
  
  class OnceAPIClient:
      """Complete 1NCE API client with automatic authentication"""
      
      def __init__(self):
          self.auth_manager = OnceAuthManager(
              username=config.ONENCE_USERNAME,
              password=config.ONENCE_PASSWORD,
              base_url=config.ONENCE_API_BASE_URL
          )
          self.base_url = config.ONENCE_API_BASE_URL
          self.session = requests.Session()
      
      def _make_request(
          self, 
          method: str, 
          endpoint: str, 
          **kwargs
      ) -> Dict[str, Any]:
          """Make authenticated request with automatic retry on auth failure"""
          url = f"{self.base_url}{endpoint}"
          headers = self.auth_manager.get_auth_headers()
          
          if 'headers' in kwargs:
              headers.update(kwargs.pop('headers'))
          
          try:
              response = self.session.request(
                  method, url, headers=headers, timeout=30, **kwargs
              )
              
              # Handle 401 Unauthorized
              if response.status_code == 401:
                  logger.warning("Received 401, invalidating token and retrying...")
                  self.auth_manager.invalidate_token()
                  headers = self.auth_manager.get_auth_headers()
                  response = self.session.request(
                      method, url, headers=headers, timeout=30, **kwargs
                  )
              
              response.raise_for_status()
              return response.json() if response.text else {}
              
          except requests.exceptions.HTTPError as e:
              logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
              raise
          except requests.exceptions.RequestException as e:
              logger.error(f"Request failed: {e}")
              raise
      
      # ===== SIM Management Methods =====
      
      def get_all_sims(self) -> Dict[str, Any]:
          """Get all SIMs"""
          return self._make_request('GET', '/v1/sims')
      
      def get_sim(self, iccid: str) -> Dict[str, Any]:
          """Get single SIM details"""
          return self._make_request('GET', f'/v1/sims/{iccid}')
      
      def get_sim_status(self, iccid: str) -> Dict[str, Any]:
          """Get SIM status"""
          return self._make_request('GET', f'/v1/sims/{iccid}/status')
      
      def get_sim_usage(
          self, 
          iccid: str, 
          start_date: str, 
          end_date: str
      ) -> Dict[str, Any]:
          """Get SIM usage for date range (YYYY-MM-DD)"""
          params = {'start_dt': start_date, 'end_dt': end_date}
          return self._make_request('GET', f'/v1/sims/{iccid}/usage', params=params)
      
      def get_sim_connectivity(
          self, 
          iccid: str, 
          subscriber: bool = True,
          ussd: bool = False
      ) -> Dict[str, Any]:
          """Get SIM connectivity information"""
          params = {'subscriber': subscriber, 'ussd': ussd}
          return self._make_request(
              'GET', 
              f'/v1/sims/{iccid}/connectivity_info',
              params=params
          )
      
      def get_sim_data_quota(self, iccid: str) -> Dict[str, Any]:
          """Get SIM data quota"""
          return self._make_request('GET', f'/v1/sims/{iccid}/quota/data')
      
      def get_sim_sms_quota(self, iccid: str) -> Dict[str, Any]:
          """Get SIM SMS quota"""
          return self._make_request('GET', f'/v1/sims/{iccid}/quota/sms')
      
      def get_sim_events(self, iccid: str) -> Dict[str, Any]:
          """Get SIM events"""
          return self._make_request('GET', f'/v1/sims/{iccid}/events')
      
      # Bulk operations
      def get_usage_for_multiple_sims(
          self,
          iccids: list,
          start_date: str,
          end_date: str
      ) -> Dict[str, Dict[str, Any]]:
          """Get usage for multiple SIMs"""
          results = {}
          for iccid in iccids:
              try:
                  results[iccid] = self.get_sim_usage(iccid, start_date, end_date)
              except Exception as e:
                  logger.error(f"Failed to get usage for {iccid}: {e}")
                  results[iccid] = {"error": str(e)}
          return results
  ```

- [ ] **Create endpoint-specific modules** (`src/api/endpoints/sims.py`, etc.)

- [ ] **Test API integration**
  ```python
  # scripts/test_api.py
  from src.api.client import OnceAPIClient
  from datetime import datetime, timedelta
  
  def test_api():
      client = OnceAPIClient()
      
      # Test authentication
      print("Testing authentication...")
      token = client.auth_manager.get_token()
      print(f"✓ Token obtained: {token[:20]}...")
      
      # Test get all SIMs
      print("\nTesting get all SIMs...")
      sims = client.get_all_sims()
      print(f"✓ Found {len(sims)} SIMs")
      
      if sims:
          iccid = sims[0]['iccid']
          
          # Test get single SIM
          print(f"\nTesting get SIM {iccid}...")
          sim_detail = client.get_sim(iccid)
          print(f"✓ SIM details: {sim_detail.get('label', 'No label')}")
          
          # Test get usage
          print(f"\nTesting get usage...")
          end_date = datetime.now().strftime('%Y-%m-%d')
          start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
          usage = client.get_sim_usage(iccid, start_date, end_date)
          print(f"✓ Usage data retrieved: {len(usage.get('stats', []))} days")
      
      print("\n✅ All API tests passed!")
  
  if __name__ == "__main__":
      test_api()
  ```

#### Deliverables:
- Complete API client with all endpoints
- Authentication working with auto-refresh
- API tests passing

---

### 📊 Week 3: Data Collection Service

#### Tasks:
- [ ] **Create data collector service** (`src/services/data_collector.py`)
  ```python
  from datetime import datetime, timedelta
  from typing import List, Dict, Any
  import logging
  
  from src.api.client import OnceAPIClient
  from src.database.connection import get_db
  from src.database.models import (
      SIMCard, UsageRecord, ConnectivityLog, 
      SIMEvent, DataCollectionLog
  )
  
  logger = logging.getLogger(__name__)
  
  
  class DataCollector:
      """Service for collecting data from 1NCE API"""
      
      def __init__(self):
          self.api_client = OnceAPIClient()
      
      def sync_all_sims(self) -> Dict[str, Any]:
          """Sync all SIM cards from API to database"""
          log_entry = DataCollectionLog(
              collection_type='full_sync',
              started_at=datetime.utcnow(),
              status='running'
          )
          
          try:
              with get_db() as db:
                  db.add(log_entry)
                  db.commit()
                  
                  # Fetch all SIMs from API
                  api_sims = self.api_client.get_all_sims()
                  
                  processed = 0
                  errors = []
                  
                  for api_sim in api_sims:
                      try:
                          self._sync_single_sim(db, api_sim)
                          processed += 1
                      except Exception as e:
                          errors.append({
                              'iccid': api_sim.get('iccid'),
                              'error': str(e)
                          })
                          logger.error(f"Failed to sync SIM {api_sim.get('iccid')}: {e}")
                  
                  # Update log
                  log_entry.completed_at = datetime.utcnow()
                  log_entry.status = 'success' if not errors else 'partial'
                  log_entry.sims_processed = processed
                  log_entry.errors_count = len(errors)
                  log_entry.error_details = errors if errors else None
                  db.commit()
                  
                  return {
                      'success': True,
                      'processed': processed,
                      'errors': len(errors)
                  }
                  
          except Exception as e:
              logger.error(f"Full sync failed: {e}")
              log_entry.status = 'failed'
              log_entry.completed_at = datetime.utcnow()
              with get_db() as db:
                  db.add(log_entry)
                  db.commit()
              raise
      
      def _sync_single_sim(self, db, api_sim: Dict[str, Any]):
          """Sync single SIM card data"""
          iccid = api_sim['iccid']
          
          # Find or create SIM record
          sim = db.query(SIMCard).filter(SIMCard.iccid == iccid).first()
          
          if not sim:
              sim = SIMCard(iccid=iccid)
              db.add(sim)
          
          # Update fields
          sim.iccid_with_luhn = api_sim.get('iccid_with_luhn')
          sim.imsi = api_sim.get('imsi')
          sim.imsi_2 = api_sim.get('imsi_2')
          sim.current_imsi = api_sim.get('current_imsi')
          sim.msisdn = api_sim.get('msisdn')
          sim.imei = api_sim.get('imei')
          sim.imei_lock = api_sim.get('imei_lock', False)
          sim.status = api_sim.get('status')
          sim.ip_address = api_sim.get('ip_address')
          sim.label = api_sim.get('label')
          
          # Activation date
          if api_sim.get('activation_date'):
              sim.activation_date = datetime.fromisoformat(
                  api_sim['activation_date'].replace('Z', '+00:00')
              )
          
          # Quota data
          sim.current_quota_mb = api_sim.get('current_quota')
          if api_sim.get('quota_status'):
              sim.quota_status_id = api_sim['quota_status'].get('id')
          
          sim.current_quota_sms = api_sim.get('current_quota_SMS')
          if api_sim.get('quota_status_SMS'):
              sim.quota_sms_status_id = api_sim['quota_status_SMS'].get('id')
          
          sim.last_synced_at = datetime.utcnow()
          sim.updated_at = datetime.utcnow()
          
          db.commit()
      
      def collect_usage_data(
          self, 
          iccid: str, 
          start_date: str, 
          end_date: str
      ):
          """Collect and store usage data for a SIM"""
          with get_db() as db:
              sim = db.query(SIMCard).filter(SIMCard.iccid == iccid).first()
              if not sim:
                  raise ValueError(f"SIM {iccid} not found in database")
              
              # Fetch usage from API
              usage_data = self.api_client.get_sim_usage(iccid, start_date, end_date)
              
              for daily_stat in usage_data.get('stats', []):
                  date = datetime.fromisoformat(daily_stat['date'].replace('Z', '+00:00'))
                  
                  # Check if record exists
                  existing = db.query(UsageRecord).filter(
                      UsageRecord.sim_card_id == sim.id,
                      UsageRecord.date == date
                  ).first()
                  
                  if existing:
                      # Update existing record
                      usage_record = existing
                  else:
                      # Create new record
                      usage_record = UsageRecord(
                          sim_card_id=sim.id,
                          date=date
                      )
                      db.add(usage_record)
                  
                  # Update data usage
                  data = daily_stat.get('data', {})
                  usage_record.data_volume_mb = float(data.get('volume', 0))
                  usage_record.data_volume_rx_mb = float(data.get('volume_rx', 0))
                  usage_record.data_volume_tx_mb = float(data.get('volume_tx', 0))
                  
                  # Update SMS usage
                  sms = daily_stat.get('sms', {})
                  usage_record.sms_volume = int(sms.get('volume', 0))
                  usage_record.sms_volume_mo = int(sms.get('volume_rx', 0))
                  usage_record.sms_volume_mt = int(sms.get('volume_tx', 0))
              
              db.commit()
      
      def collect_all_usage_data(self, days_back: int = 7):
          """Collect usage data for all SIMs"""
          end_date = datetime.now().strftime('%Y-%m-%d')
          start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
          
          with get_db() as db:
              sims = db.query(SIMCard).all()
              
              for sim in sims:
                  try:
                      self.collect_usage_data(sim.iccid, start_date, end_date)
                      logger.info(f"Collected usage for {sim.iccid}")
                  except Exception as e:
                      logger.error(f"Failed to collect usage for {sim.iccid}: {e}")
  ```

- [ ] **Create background worker** (`scripts/worker.py`)
  ```python
  from apscheduler.schedulers.blocking import BlockingScheduler
  from apscheduler.triggers.interval import IntervalTrigger
  import logging
  from datetime import datetime
  
  from src.services.data_collector import DataCollector
  from src.config import config
  from src.utils.logger import setup_logging
  
  # Setup logging
  setup_logging()
  logger = logging.getLogger(__name__)
  
  
  def collect_usage_job():
      """Scheduled job to collect usage data"""
      logger.info("Starting usage data collection...")
      try:
          collector = DataCollector()
          collector.collect_all_usage_data(days_back=1)
          logger.info("Usage data collection completed")
      except Exception as e:
          logger.error(f"Usage data collection failed: {e}")
  
  
  def full_sync_job():
      """Scheduled job for full SIM sync"""
      logger.info("Starting full SIM sync...")
      try:
          collector = DataCollector()
          result = collector.sync_all_sims()
          logger.info(f"Full sync completed: {result}")
      except Exception as e:
          logger.error(f"Full sync failed: {e}")
  
  
  def main():
      scheduler = BlockingScheduler()
      
      # Collect usage data every hour
      scheduler.add_job(
          collect_usage_job,
          trigger=IntervalTrigger(
              minutes=config.DATA_COLLECTION_INTERVAL_MINUTES
          ),
          id='collect_usage',
          name='Collect usage data',
          replace_existing=True
      )
      
      # Full sync once per day at 2 AM
      scheduler.add_job(
          full_sync_job,
          trigger='cron',
          hour=2,
          minute=0,
          id='full_sync',
          name='Full SIM sync',
          replace_existing=True
      )
      
      logger.info("Starting scheduler...")
      logger.info(f"Usage collection interval: {config.DATA_COLLECTION_INTERVAL_MINUTES} minutes")
      
      try:
          scheduler.start()
      except (KeyboardInterrupt, SystemExit):
          logger.info("Scheduler stopped")
  
  
  if __name__ == "__main__":
      main()
  ```

- [ ] **Create logging utility** (`src/utils/logger.py`)
  ```python
  import logging
  import sys
  from pathlib import Path
  from loguru import logger as loguru_logger
  
  from src.config import config
  
  
  def setup_logging():
      """Configure logging for the application"""
      
      # Remove default handlers
      loguru_logger.remove()
      
      # Console handler
      loguru_logger.add(
          sys.stdout,
          format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
          level=config.LOG_LEVEL,
          colorize=True
      )
      
      # File handler
      log_dir = Path("logs")
      log_dir.mkdir(exist_ok=True)
      
      loguru_logger.add(
          log_dir / "app_{time:YYYY-MM-DD}.log",
          rotation="1 day",
          retention="30 days",
          level=config.LOG_LEVEL,
          format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}"
      )
      
      # Intercept standard logging
      class InterceptHandler(logging.Handler):
          def emit(self, record):
              try:
                  level = loguru_logger.level(record.levelname).name
              except ValueError:
                  level = record.levelno
              
              frame, depth = logging.currentframe(), 2
              while frame.f_code.co_filename == logging.__file__:
                  frame = frame.f_back
                  depth += 1
              
              loguru_logger.opt(depth=depth, exception=record.exc_info).log(
                  level, record.getMessage()
              )
      
      logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
  ```

#### Deliverables:
- Data collector service working
- Background worker running
- Usage data being collected and stored

---

## Phase 2: Core Features (Weeks 4-6)

### 🎨 Week 4: Streamlit Dashboard Foundation

#### Tasks:
- [ ] **Create main Streamlit app** (`src/app.py`)
  ```python
  import streamlit as st
  from datetime import datetime, timedelta
  import pandas as pd
  
  from src.config import config
  from src.database.connection import get_db
  from src.database.models import SIMCard, UsageRecord
  from src.utils.logger import setup_logging
  
  # Setup
  setup_logging()
  
  # Page config
  st.set_page_config(
      page_title="1NCE IoT Management",
      page_icon="📡",
      layout="wide",
      initial_sidebar_state="expanded"
  )
  
  # Custom CSS
  st.markdown("""
      <style>
      .main > div {
          padding-top: 2rem;
      }
      .stMetric {
          background-color: #f0f2f6;
          padding: 1rem;
          border-radius: 0.5rem;
      }
      </style>
  """, unsafe_allow_html=True)
  
  
  def main():
      # Header
      st.title("📡 1NCE IoT Management Dashboard")
      st.markdown("---")
      
      # Sidebar
      with st.sidebar:
          st.image("https://via.placeholder.com/150x50?text=1NCE", width=150)
          st.markdown("### Navigation")
          st.markdown("Use the pages in the sidebar to navigate")
          
          st.markdown("---")
          st.markdown("### Quick Stats")
          
          with get_db() as db:
              total_sims = db.query(SIMCard).count()
              active_sims = db.query(SIMCard).filter(
                  SIMCard.status == 'Enabled'
              ).count()
              
              st.metric("Total SIMs", total_sims)
              st.metric("Active SIMs", active_sims)
      
      # Main content
      col1, col2, col3, col4 = st.columns(4)
      
      with get_db() as db:
          # Total SIMs
          with col1:
              total = db.query(SIMCard).count()
              st.metric("Total SIMs", f"{total:,}")
          
          # Active SIMs
          with col2:
              active = db.query(SIMCard).filter(
                  SIMCard.status == 'Enabled'
              ).count()
              delta = f"+{active - (total - active)}" if active > (total - active) else ""
              st.metric("Active SIMs", f"{active:,}", delta)
          
          # Today's data usage
          with col3:
              today = datetime.now().date()
              usage_today = db.query(
                  db.func.sum(UsageRecord.data_volume_mb)
              ).filter(
                  UsageRecord.date >= today
              ).scalar() or 0
              st.metric("Today's Data Usage", f"{usage_today:.1f} MB")
          
          # Quota alerts
          with col4:
              alerts = db.query(SIMCard).filter(
                  SIMCard.quota_status_id.in_([1, 2])
              ).count()
              st.metric("Quota Alerts", alerts, delta=f"{alerts} SIMs" if alerts > 0 else "")
      
      st.markdown("---")
      
      # Recent activity
      st.subheader("Recent Activity")
      
      with get_db() as db:
          recent_sims = db.query(SIMCard).order_by(
              SIMCard.updated_at.desc()
          ).limit(10).all()
          
          if recent_sims:
              df = pd.DataFrame([
                  {
                      'ICCID': sim.iccid,
                      'Label': sim.label or 'N/A',
                      'Status': sim.status,
                      'Last Updated': sim.updated_at.strftime('%Y-%m-%d %H:%M')
                  }
                  for sim in recent_sims
              ])
              st.dataframe(df, use_container_width=True)
          else:
              st.info("No SIM cards found. Import SIM data to get started.")
      
      # Quick actions
      st.markdown("---")
      st.subheader("Quick Actions")
      
      col1, col2, col3 = st.columns(3)
      
      with col1:
          if st.button("🔄 Sync All SIMs", use_container_width=True):
              with st.spinner("Syncing SIM data..."):
                  from src.services.data_collector import DataCollector
                  collector = DataCollector()
                  result = collector.sync_all_sims()
                  st.success(f"Synced {result['processed']} SIMs")
      
      with col2:
          if st.button("📊 Collect Usage Data", use_container_width=True):
              with st.spinner("Collecting usage data..."):
                  from src.services.data_collector import DataCollector
                  collector = DataCollector()
                  collector.collect_all_usage_data(days_back=7)
                  st.success("Usage data collected")
      
      with col3:
          if st.button("📈 Generate Report", use_container_width=True):
              st.info("Navigate to Reports page")
  
  
  if __name__ == "__main__":
      main()
  ```

- [ ] **Create page: Overview** (`src/pages/1_📊_Overview.py`)

- [ ] **Create page: Usage Analytics** (`src/pages/2_📈_Usage_Analytics.py`)

- [ ] **Create page: SIM Management** (`src/pages/3_📱_SIM_Management.py`)

- [ ] **Create reusable components** (`src/components/`)

#### Deliverables:
- Working Streamlit dashboard
- Multiple pages functional
- Basic navigation working

---

### 📈 Week 5: Visualization & Analytics

#### Tasks:
- [ ] **Implement usage trend charts**
  - Time-series line charts
  - Bar charts for comparisons
  - Heatmaps for usage patterns

- [ ] **Create analytics functions**
  - Top consumers identification
  - Usage forecasting
  - Anomaly detection

- [ ] **Add export functionality**
  - Export to CSV
  - Export to Excel with charts
  - PDF report generation

#### Deliverables:
- Interactive charts working
- Analytics insights displayed
- Export functions implemented

---

### 📤 Week 6: Import/Export & Bulk Operations

#### Tasks:
- [ ] **Create file upload interface**
  - CSV upload
  - XLSX upload
  - File validation

- [ ] **Implement bulk operations**
  - Bulk SIM import
  - Bulk data refresh
  - Bulk export

- [ ] **Create file processor** (`src/services/file_processor.py`)

#### Deliverables:
- File upload working
- Bulk operations functional
- Data validation implemented

---

## Phase 3: Advanced Features (Weeks 7-8)

### 🔔 Week 7: Alerting System

#### Tasks:
- [ ] **Implement alert service** (`src/services/alert_service.py`)
  ```python
  from src.database.models import Alert, SIMCard
  from src.database.connection import get_db
  
  def check_quota_alerts():
      """Check and create quota alerts"""
      with get_db() as db:
          # Find SIMs with low quota
          low_quota_sims = db.query(SIMCard).filter(
              SIMCard.quota_status_id == 1  # Less than 20%
          ).all()
          
          for sim in low_quota_sims:
              # Create alert if not exists
              existing = db.query(Alert).filter(
                  Alert.sim_card_id == sim.id,
                  Alert.alert_type == 'quota_warning',
                  Alert.is_resolved == False
              ).first()
              
              if not existing:
                  alert = Alert(
                      sim_card_id=sim.id,
                      alert_type='quota_warning',
                      severity='warning',
                      message=f"SIM {sim.iccid} has less than 20% quota remaining"
                  )
                  db.add(alert)
          
          db.commit()
  ```

- [ ] **Create email notification system**
- [ ] **Add in-app notifications**
- [ ] **Create alert management page**

#### Deliverables:
- Alert system functional
- Email notifications working (optional)
- Alert dashboard created

---

### 🔌 Week 8: Connectivity Monitoring

#### Tasks:
- [ ] **Implement connectivity tracking**
- [ ] **Create connectivity dashboard**
- [ ] **Add cell tower visualization**
- [ ] **Implement location tracking**

#### Deliverables:
- Connectivity monitoring active
- Location data displayed
- Cell tower info shown

---

## Phase 4: Testing & Optimization (Week 9)

### 🧪 Week 9: Comprehensive Testing

#### Tasks:
- [ ] **Unit tests**
  ```bash
  pytest tests/ -v --cov=src
  ```

- [ ] **Integration tests**
- [ ] **Performance testing**
  - Load testing with multiple SIMs
  - Database query optimization
  - Caching implementation

- [ ] **Security audit**
  - Environment variable security
  - SQL injection prevention
  - XSS prevention in Streamlit

- [ ] **Code quality**
  ```bash
  black src/
  isort src/
  flake8 src/
  mypy src/
  ```

#### Deliverables:
- Test coverage > 80%
- Performance benchmarks met
- Security issues resolved

---

## Phase 5: Deployment (Weeks 10-11)

### 🚀 Week 10: Production Preparation

#### Tasks:
- [ ] **Create production Docker Compose**
  ```yaml
  # docker-compose.prod.yml
  version: '3.8'
  
  services:
    dashboard:
      build:
        context: .
        dockerfile: Dockerfile.prod
      restart: always
      environment:
        - ENVIRONMENT=production
      # ... production configs
  ```

- [ ] **Set up SSL/TLS**
  - Configure NGINX reverse proxy
  - Install SSL certificates (Let's Encrypt)

- [ ] **Configure backup strategy**
  ```bash
  # Automated PostgreSQL backups
  pg_dump -U onence_user onence_db > backup_$(date +%Y%m%d).sql
  ```

- [ ] **Set up monitoring**
  - Prometheus + Grafana
  - Application metrics
  - Error tracking (Sentry)

#### Deliverables:
- Production-ready Docker setup
- SSL configured
- Monitoring active

---

### 🌐 Week 11: Deployment & Launch

#### Tasks:
- [ ] **Choose deployment platform**
  - **Option A**: AWS (ECS/EC2)
  - **Option B**: Azure (Container Instances)
  - **Option C**: DigitalOcean (Droplet)
  - **Option D**: Self-hosted server

- [ ] **Deploy to production**
  ```bash
  # Example: Deploy to server
  ssh user@server
  git clone <repo>
  cd onence-dashboard
  cp .env.example .env
  # Edit .env with production credentials
  docker-compose -f docker-compose.prod.yml up -d
  ```

- [ ] **Configure domain & DNS**
- [ ] **Set up CI/CD pipeline** (GitHub Actions)
  ```yaml
  # .github/workflows/deploy.yml
  name: Deploy to Production
  on:
    push:
      branches: [main]
  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v2
        - name: Deploy
          run: |
            # Deployment script
  ```

- [ ] **User acceptance testing**

#### Deliverables:
- Application deployed
- Domain configured
- UAT completed

---

## Phase 6: Documentation & Handover (Week 12)

### 📚 Week 12: Documentation

#### Tasks:
- [ ] **Complete user documentation**
  - User guide with screenshots
  - Video tutorials
  - FAQ section

- [ ] **Complete technical documentation**
  - API documentation
  - Database schema
  - Architecture diagrams
  - Deployment guide

- [ ] **Create admin documentation**
  - Maintenance procedures
  - Backup/restore procedures
  - Troubleshooting guide

- [ ] **Knowledge transfer sessions**
  - Live demo
  - Q&A sessions
  - Training materials

#### Deliverables:
- Complete documentation suite
- Training completed
- Handover successful

---

## 📊 Success Criteria

### Functional Requirements ✅
- [ ] All 1NCE API endpoints integrated
- [ ] Real-time SIM monitoring
- [ ] Historical usage analytics (6 months)
- [ ] CSV/XLSX import functionality
- [ ] Alert system operational
- [ ] Report generation working

### Non-Functional Requirements ✅
- [ ] Page load time < 3 seconds
- [ ] Support for 1000+ SIMs
- [ ] 99% uptime
- [ ] Data refreshed hourly
- [ ] Mobile responsive
- [ ] Secure (HTTPS, authentication)

### Performance Targets ✅
- [ ] Dashboard loads in < 2 seconds
- [ ] API calls complete in < 5 seconds
- [ ] Database queries optimized (< 1 second)
- [ ] File uploads process in < 30 seconds

---

## 🛠️ Development Best Practices

### Daily Workflow
1. **Morning**: Review GitHub issues/project board
2. **Development**: Work on assigned tasks
3. **Testing**: Write tests for new features
4. **Documentation**: Update docs as you go
5. **Git**: Commit frequently with clear messages
6. **Evening**: Update project board, plan next day

### Git Workflow
```bash
# Feature branch workflow
git checkout -b feature/usage-analytics
# ... make changes ...
git add .
git commit -m "feat: add usage analytics charts"
git push origin feature/usage-analytics
# Create pull request
```

### Code Review Checklist
- [ ] Code follows style guide
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No sensitive data committed
- [ ] Performance considerations addressed

---

## 🆘 Troubleshooting Guide

### Common Issues

**Issue**: Docker containers won't start
```bash
# Check logs
docker-compose logs -f

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Issue**: Database connection fails
```bash
# Check PostgreSQL is running
docker-compose ps db

# Test connection
docker-compose exec db psql -U onence_user -d onence_db
```

**Issue**: API authentication fails
- Verify credentials in `.env`
- Check 1NCE account has API access
- Test credentials manually

---

## 📈 Future Enhancements (Post-Launch)

### Phase 7: Advanced Features (Optional)
- [ ] **Machine Learning**
  - Usage prediction models
  - Anomaly detection
  - Cost optimization recommendations

- [ ] **Mobile App**
  - React Native mobile companion
  - Push notifications
  - Offline mode

- [ ] **Advanced Reporting**
  - Custom report builder
  - Scheduled reports
  - Multi-tenant support

- [ ] **Integration Ecosystem**
  - Webhook support
  - REST API for third-party integration
  - Zapier integration

---

## 📞 Support & Resources

### Documentation
- [Streamlit Docs](https://docs.streamlit.io)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org)
- [TimescaleDB Docs](https://docs.timescale.com)
- [1NCE API Docs](https://help.1nce.com/dev-hub)

### Community
- Streamlit Community Forum
- Stack Overflow
- GitHub Issues

---

## ✅ Project Checklist

### Phase 0: Planning ☐
- [ ] Requirements defined
- [ ] Architecture designed
- [ ] Development environment setup
- [ ] Project structure created

### Phase 1: Foundation ☐
- [ ] Database setup complete
- [ ] API integration working
- [ ] Data collection service running

### Phase 2: Core Features ☐
- [ ] Dashboard functional
- [ ] Visualizations implemented
- [ ] Import/export working

### Phase 3: Advanced Features ☐
- [ ] Alerting system active
- [ ] Connectivity monitoring live

### Phase 4: Testing ☐
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Performance optimized

### Phase 5: Deployment ☐
- [ ] Production environment ready
- [ ] Application deployed
- [ ] Monitoring configured

### Phase 6: Documentation ☐
- [ ] User docs complete
- [ ] Technical docs complete
- [ ] Training delivered

---

## 🎯 Key Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Project Kickoff | Week 1 | ☐ |
| MVP (Basic Dashboard) | Week 4 | ☐ |
| Feature Complete | Week 8 | ☐ |
| Testing Complete | Week 9 | ☐ |
| Production Deployment | Week 11 | ☐ |
| Project Handover | Week 12 | ☐ |

---

## 📝 Notes

- Adjust timeline based on team size and availability
- Prioritize must-have features for MVP
- Regular stakeholder demos (bi-weekly recommended)
- Keep security and performance in mind from day 1
- Document decisions and changes as you go

---

**Last Updated**: 2025-11-15  
**Version**: 1.0  
**Author**: Nicolas / Claude  
**Status**: Ready for Development 🚀
