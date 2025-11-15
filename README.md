# 1NCE IoT Management Dashboard

A comprehensive IoT management platform for monitoring and managing 1NCE SIM cards with real-time analytics, usage tracking, and automated alerting.

## 🌟 Features

- **Real-time SIM Monitoring**: Track status, connectivity, and usage of all your 1NCE SIM cards
- **Usage Analytics**: Comprehensive analytics with interactive charts and historical data
- **Quota Management**: Monitor data and SMS quotas with automatic alerts
- **Alert System**: Get notified when SIMs approach quota limits or experience connectivity issues
- **Bulk Operations**: Manage multiple SIMs efficiently
- **Data Export**: Export reports in CSV format for further analysis
- **Background Data Collection**: Automated hourly data synchronization
- **TimescaleDB Integration**: Optimized time-series data storage for efficient analytics

## 🏗️ Architecture

### Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.11
- **Database**: PostgreSQL with TimescaleDB extension
- **Caching**: Redis
- **API Integration**: 1NCE Management API
- **Containerization**: Docker & Docker Compose
- **Visualization**: Plotly, Altair
- **Scheduling**: APScheduler

### Project Structure

```
IOT-mercury-1/
├── src/
│   ├── app.py                    # Main Streamlit application
│   ├── config.py                 # Configuration management
│   ├── database/
│   │   ├── models.py             # SQLAlchemy database models
│   │   └── connection.py         # Database connection and initialization
│   ├── api/
│   │   ├── auth_manager.py       # 1NCE API authentication
│   │   └── client.py             # 1NCE API client
│   ├── services/
│   │   ├── data_collector.py     # Data collection service
│   │   └── alert_service.py      # Alert management service
│   ├── utils/
│   │   └── logger.py             # Logging configuration
│   └── pages/
│       ├── 1_📊_Overview.py      # Overview dashboard
│       ├── 2_📱_SIM_Management.py # SIM management interface
│       ├── 3_📈_Usage_Analytics.py # Usage analytics
│       └── 4_🔔_Alerts.py        # Alert management
├── scripts/
│   ├── worker.py                 # Background worker for data collection
│   ├── init_db.py               # Database initialization script
│   └── init_db.sql              # SQL initialization script
├── docker-compose.yml           # Docker services configuration
├── Dockerfile                   # Docker image definition
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- 1NCE API credentials (username and password)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd IOT-mercury-1
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your 1NCE credentials:
   ```
   ONENCE_USERNAME=your_username
   ONENCE_PASSWORD=your_password
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**
   ```bash
   docker-compose exec dashboard python scripts/init_db.py
   ```

5. **Access the dashboard**
   - Dashboard: http://localhost:8501
   - pgAdmin (optional): http://localhost:5050
   - Grafana (optional): http://localhost:3000

### First-Time Setup

1. Open the dashboard at http://localhost:8501
2. Click "🔄 Sync All SIMs" to import your SIM cards from 1NCE
3. Click "📊 Collect Usage Data" to fetch historical usage data
4. Explore the different pages in the sidebar

## 📊 Dashboard Pages

### 1. Home Dashboard
- Quick overview of your IoT fleet
- Key metrics (total SIMs, active SIMs, data usage)
- Recent activity
- Quick action buttons

### 2. 📊 Overview
- Comprehensive fleet statistics
- SIM status distribution
- Usage trends over time
- Top data consumers

### 3. 📱 SIM Management
- Search and filter SIM cards
- View detailed SIM information
- Update SIM labels
- Enable/disable SIMs
- Refresh individual SIM data

### 4. 📈 Usage Analytics
- Customizable date range analysis
- Data and SMS usage trends
- SIM-level breakdown
- Export reports to CSV
- Usage distribution charts

### 5. 🔔 Alerts
- Active alert monitoring
- Quota warnings (data and SMS)
- Alert resolution
- Historical alert tracking

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

```bash
# 1NCE API Credentials
ONENCE_USERNAME=your_username
ONENCE_PASSWORD=your_password

# Database
DATABASE_URL=postgresql://onence_user:onence_password@db:5432/onence_db

# Redis
REDIS_URL=redis://redis:6379/0

# Application
ENVIRONMENT=development
LOG_LEVEL=INFO

# Data Collection
DATA_COLLECTION_INTERVAL_MINUTES=60
USAGE_RETENTION_DAYS=180
```

### Data Collection Schedule

The background worker automatically:
- Syncs SIM data daily at 2:00 AM
- Collects usage data every hour (configurable)

## 🐳 Docker Services

The application includes the following Docker services:

- **dashboard**: Streamlit web application (port 8501)
- **db**: PostgreSQL with TimescaleDB (port 5432)
- **redis**: Redis cache (port 6379)
- **worker**: Background data collection worker
- **grafana** (optional): Advanced visualization (port 3000)
- **pgadmin** (optional): Database management (port 5050)

### Managing Services

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f dashboard

# Restart a service
docker-compose restart dashboard

# Rebuild after code changes
docker-compose up -d --build
```

## 📝 Database Schema

### Main Tables

- **sim_cards**: SIM card master data
- **usage_records**: Daily usage data (TimescaleDB hypertable)
- **sim_events**: SIM card events
- **connectivity_logs**: Connectivity and location data
- **alerts**: System alerts
- **data_collection_logs**: Data collection audit trail

## 🔒 Security

- Environment variables for sensitive data
- No hardcoded credentials
- SQL injection prevention via SQLAlchemy ORM
- Connection pooling for database efficiency
- Token-based authentication with 1NCE API

## 🧪 Development

### Running Locally (without Docker)

1. **Create virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL and Redis locally**

4. **Configure .env file**

5. **Initialize database**
   ```bash
   python scripts/init_db.py
   ```

6. **Run Streamlit**
   ```bash
   streamlit run src/app.py
   ```

7. **Run background worker** (in separate terminal)
   ```bash
   python scripts/worker.py
   ```

### Code Quality

```bash
# Format code
black src/

# Sort imports
isort src/

# Lint
flake8 src/

# Type checking
mypy src/
```

### Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## 📈 Performance

- Supports monitoring of 1000+ SIM cards
- TimescaleDB hypertables for efficient time-series queries
- Redis caching for improved response times
- Connection pooling for database efficiency
- Asynchronous data collection

## 🔍 Troubleshooting

### Common Issues

**Issue**: Docker containers won't start
```bash
docker-compose logs -f
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
- Review logs: `docker-compose logs -f dashboard`

## 📚 API Documentation

The platform integrates with the following 1NCE API endpoints:

- `/v1/sims` - List all SIMs
- `/v1/sims/{iccid}` - Get SIM details
- `/v1/sims/{iccid}/usage` - Get usage data
- `/v1/sims/{iccid}/quota/data` - Get data quota
- `/v1/sims/{iccid}/quota/sms` - Get SMS quota
- `/v1/sims/{iccid}/connectivity_info` - Get connectivity info
- `/v1/sims/{iccid}/events` - Get SIM events

## 🛣️ Roadmap

- [ ] Email notifications for alerts
- [ ] Advanced analytics with ML predictions
- [ ] Custom report builder
- [ ] Multi-user support with authentication
- [ ] Mobile app companion
- [ ] Webhook integrations
- [ ] Cost optimization recommendations

## 📄 License

This project is proprietary software.

## 👥 Support

For issues and questions, please contact the development team or create an issue in the repository.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [1NCE](https://1nce.com/) IoT connectivity
- Time-series optimization by [TimescaleDB](https://www.timescale.com/)

---

**Version**: 1.0
**Last Updated**: 2025-11-15
**Author**: Nicolas / Claude AI
