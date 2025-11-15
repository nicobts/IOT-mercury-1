# Quick Start Guide - 1NCE IoT Management Dashboard

## 🚀 Getting Started (Multiple Options)

### Option 1: Docker Setup (Recommended for Production)

This is the easiest way to get everything running with one command.

#### Prerequisites
- Docker Desktop installed and running
- 1NCE API credentials

#### Steps

1. **Install Docker Desktop**
   - Windows: Download from https://www.docker.com/products/docker-desktop
   - Mac: Download from https://www.docker.com/products/docker-desktop
   - Linux: Install docker and docker-compose via package manager

2. **Start Docker Desktop**
   - Make sure Docker Desktop is running (check system tray/menu bar)
   - Wait until it shows "Docker Desktop is running"

3. **Clone and Configure**
   ```bash
   git clone <your-repo-url>
   cd IOT-mercury-1

   # Copy environment template
   cp .env.example .env

   # Edit .env and add your credentials:
   # ONENCE_USERNAME=your_username
   # ONENCE_PASSWORD=your_password
   ```

4. **Start All Services**
   ```bash
   docker-compose up -d
   ```

5. **Initialize Database**
   ```bash
   docker-compose exec dashboard python scripts/init_db.py
   ```

6. **Access Dashboard**
   - Open http://localhost:8501 in your browser
   - Click "Sync All SIMs" to import your data

---

### Option 2: Local Development (No Docker Required)

Run the application directly on your machine without Docker.

#### Prerequisites
- Python 3.11 or higher
- PostgreSQL 14+ with TimescaleDB extension
- Redis (optional, for caching)
- 1NCE API credentials

#### Steps

1. **Install Python Dependencies**
   ```bash
   # Create virtual environment
   python3.11 -m venv venv

   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate

   # Install packages
   pip install -r requirements.txt
   ```

2. **Install PostgreSQL**

   **Windows:**
   - Download and install PostgreSQL from https://www.postgresql.org/download/windows/
   - Install TimescaleDB extension: https://docs.timescale.com/install/latest/self-hosted/installation-windows/

   **Mac:**
   ```bash
   brew install postgresql@15
   brew install timescaledb
   brew services start postgresql@15
   ```

   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get install postgresql-15
   sudo sh -c "echo 'deb https://packagecloud.io/timescale/timescaledb/ubuntu/ $(lsb_release -c -s) main' > /etc/apt/sources.list.d/timescaledb.list"
   wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | sudo apt-key add -
   sudo apt-get update
   sudo apt-get install timescaledb-2-postgresql-15
   sudo systemctl restart postgresql
   ```

3. **Create Database**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres

   # Create database and user
   CREATE DATABASE onence_db;
   CREATE USER onence_user WITH PASSWORD 'onence_password';
   GRANT ALL PRIVILEGES ON DATABASE onence_db TO onence_user;
   \q
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env

   # Edit .env with your settings:
   # ONENCE_USERNAME=your_username
   # ONENCE_PASSWORD=your_password
   # DATABASE_URL=postgresql://onence_user:onence_password@localhost:5432/onence_db
   # REDIS_URL=redis://localhost:6379/0  # Optional
   ```

5. **Initialize Database**
   ```bash
   python scripts/init_db.py
   ```

6. **Run the Application**

   Terminal 1 - Streamlit Dashboard:
   ```bash
   streamlit run src/app.py
   ```

   Terminal 2 - Background Worker (optional):
   ```bash
   python scripts/worker.py
   ```

7. **Access Dashboard**
   - Open http://localhost:8501 in your browser

---

### Option 3: Quick Test (API Only)

Test the 1NCE API integration without database or full setup.

1. **Install Minimal Dependencies**
   ```bash
   pip install requests python-dotenv pydantic pydantic-settings loguru
   ```

2. **Create .env File**
   ```bash
   # .env
   ONENCE_USERNAME=your_username
   ONENCE_PASSWORD=your_password
   ONENCE_API_BASE_URL=https://api.1nce.com/management-api
   LOG_LEVEL=INFO
   ```

3. **Run API Test**
   ```bash
   python scripts/test_api.py
   ```

This will verify your 1NCE credentials work without needing database or Docker.

---

## 🔧 Troubleshooting

### Docker Desktop Not Running (Windows)

**Error:** `The system cannot find the file specified`

**Solution:**
1. Open Docker Desktop from Start Menu
2. Wait for "Docker Desktop is running" message
3. Try `docker ps` in terminal to verify
4. If still not working, restart Docker Desktop

### PostgreSQL Connection Issues

**Error:** `could not connect to server`

**Solution:**
1. Check PostgreSQL is running:
   ```bash
   # Windows (PowerShell):
   Get-Service postgresql*

   # Mac:
   brew services list

   # Linux:
   sudo systemctl status postgresql
   ```

2. Verify connection details in .env match your setup

### Import Errors

**Error:** `ModuleNotFoundError`

**Solution:**
```bash
# Make sure you're in virtual environment
pip install -r requirements.txt

# For development without venv:
pip install --user -r requirements.txt
```

### TimescaleDB Not Available

**Error:** `extension "timescaledb" is not available`

**Solution:**
- Follow TimescaleDB installation for your platform
- Restart PostgreSQL after installation
- Re-run `scripts/init_db.py`

---

## 📋 Next Steps

### After Initial Setup

1. **Sync SIM Data**
   - Open dashboard at http://localhost:8501
   - Click "🔄 Sync All SIMs" button
   - Wait for sync to complete

2. **Collect Usage Data**
   - Click "📊 Collect Usage Data" button
   - This fetches last 7 days of usage

3. **Explore Dashboard**
   - Navigate to different pages via sidebar
   - View analytics and trends
   - Manage individual SIMs

### Production Deployment

For production use:
1. Use Docker Compose setup
2. Configure proper secrets management
3. Set up SSL/TLS with reverse proxy
4. Configure automated backups
5. Set up monitoring (Grafana included)

---

## 🆘 Still Having Issues?

### Common Questions

**Q: Do I need Redis?**
A: No, Redis is optional. The app works without it, just with slightly slower caching.

**Q: Can I use SQLite instead of PostgreSQL?**
A: No, TimescaleDB (PostgreSQL extension) is required for time-series data optimization.

**Q: How much data can it handle?**
A: Tested with 1000+ SIMs and 6 months of daily usage data.

**Q: Can I run this in the cloud?**
A: Yes! Works on AWS, Azure, DigitalOcean, etc. Use Docker Compose for easy deployment.

### Getting Help

1. Check logs:
   ```bash
   # Docker:
   docker-compose logs -f dashboard

   # Local:
   Check logs/ directory
   ```

2. Verify credentials:
   ```bash
   python scripts/test_api.py
   ```

3. Check database connection:
   ```bash
   python scripts/init_db.py
   ```

---

## 📚 Additional Resources

- [1NCE API Documentation](https://help.1nce.com/dev-hub)
- [Streamlit Documentation](https://docs.streamlit.io)
- [TimescaleDB Documentation](https://docs.timescale.com)
- [Docker Documentation](https://docs.docker.com)
