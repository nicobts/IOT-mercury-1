# Deployment Guide - 1NCE IoT Management Dashboard

## 📦 Deployment Options

### 1. Local Testing (Your Machine)

**Best for:** Development, testing, personal use

#### With Docker (Recommended)

1. **Prerequisites**
   - Install Docker Desktop: https://www.docker.com/products/docker-desktop
   - Ensure Docker Desktop is running

2. **Deploy**
   ```bash
   # Configure credentials
   cp .env.example .env
   nano .env  # or use your preferred editor

   # Start services
   docker-compose up -d

   # Initialize database
   docker-compose exec dashboard python scripts/init_db.py

   # View logs
   docker-compose logs -f dashboard
   ```

3. **Access**
   - Dashboard: http://localhost:8501
   - pgAdmin: http://localhost:5050
   - Grafana: http://localhost:3000

#### Without Docker (Manual Setup)

1. **Install Services**
   - PostgreSQL 15+ with TimescaleDB
   - Python 3.11+
   - Redis (optional)

2. **Setup**
   ```bash
   # Create virtual environment
   python3.11 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Configure
   cp .env.example .env
   # Edit .env with your database connection string

   # Initialize database
   python scripts/init_db.py

   # Run dashboard
   streamlit run src/app.py

   # Run worker (separate terminal)
   python scripts/worker.py
   ```

---

### 2. Cloud Deployment (AWS)

**Best for:** Production use, teams, high availability

#### Option A: AWS ECS (Fargate)

1. **Build and Push Docker Image**
   ```bash
   # Build image
   docker build -t 1nce-dashboard:latest .

   # Tag for ECR
   docker tag 1nce-dashboard:latest <account-id>.dkr.ecr.<region>.amazonaws.com/1nce-dashboard:latest

   # Push to ECR
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/1nce-dashboard:latest
   ```

2. **Set Up Services**
   - RDS PostgreSQL with TimescaleDB
   - ElastiCache Redis
   - ECS Cluster with Fargate
   - Application Load Balancer

3. **Deploy**
   - Create task definitions for dashboard and worker
   - Configure environment variables via AWS Secrets Manager
   - Set up auto-scaling policies

#### Option B: AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.medium or larger
   - Security group: Allow ports 22, 80, 443, 8501

2. **Install Docker**
   ```bash
   ssh ubuntu@<instance-ip>

   # Install Docker
   sudo apt update
   sudo apt install docker.io docker-compose -y
   sudo usermod -aG docker ubuntu
   ```

3. **Deploy Application**
   ```bash
   git clone <your-repo>
   cd IOT-mercury-1
   cp .env.example .env
   nano .env  # Add credentials

   docker-compose -f docker-compose.yml up -d
   ```

4. **Set Up Nginx Reverse Proxy**
   ```bash
   sudo apt install nginx certbot python3-certbot-nginx -y

   # Create Nginx config
   sudo nano /etc/nginx/sites-available/1nce-dashboard

   # Paste:
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }

   # Enable site
   sudo ln -s /etc/nginx/sites-available/1nce-dashboard /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx

   # Get SSL certificate
   sudo certbot --nginx -d your-domain.com
   ```

---

### 3. Cloud Deployment (Azure)

**Best for:** Microsoft-centric organizations

#### Azure Container Instances

1. **Create Resource Group**
   ```bash
   az group create --name 1nce-dashboard-rg --location eastus
   ```

2. **Create PostgreSQL**
   ```bash
   az postgres flexible-server create \
     --name 1nce-db-server \
     --resource-group 1nce-dashboard-rg \
     --location eastus \
     --admin-user onence_user \
     --admin-password <password> \
     --sku-name Standard_B2s \
     --version 15
   ```

3. **Deploy Container**
   ```bash
   az container create \
     --resource-group 1nce-dashboard-rg \
     --name 1nce-dashboard \
     --image <your-registry>/1nce-dashboard:latest \
     --dns-name-label 1nce-dashboard \
     --ports 8501 \
     --environment-variables \
       ONENCE_USERNAME=<username> \
       ONENCE_PASSWORD=<password> \
       DATABASE_URL=<connection-string>
   ```

---

### 4. Cloud Deployment (DigitalOcean)

**Best for:** Simple, cost-effective deployment

#### Using DigitalOcean Droplet

1. **Create Droplet**
   - Choose Ubuntu 22.04
   - Select $12/month plan (2GB RAM)
   - Add SSH key

2. **Setup**
   ```bash
   ssh root@<droplet-ip>

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   apt install docker-compose -y

   # Clone and deploy
   git clone <your-repo>
   cd IOT-mercury-1
   cp .env.example .env
   nano .env  # Configure

   docker-compose up -d
   ```

3. **Configure Domain**
   - Point your domain to droplet IP
   - Set up SSL with Let's Encrypt (see Nginx config above)

---

### 5. Heroku Deployment

**Best for:** Quick deployment, hobby projects

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Create App**
   ```bash
   heroku login
   heroku create 1nce-dashboard

   # Add PostgreSQL
   heroku addons:create heroku-postgresql:hobby-dev

   # Add Redis
   heroku addons:create heroku-redis:hobby-dev
   ```

3. **Configure**
   ```bash
   heroku config:set ONENCE_USERNAME=your_username
   heroku config:set ONENCE_PASSWORD=your_password
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

   Note: Create `Procfile`:
   ```
   web: streamlit run src/app.py --server.port=$PORT
   worker: python scripts/worker.py
   ```

---

## 🔒 Production Security Checklist

### Before Deployment

- [ ] Change default passwords in `.env`
- [ ] Use strong, unique SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Configure database backups
- [ ] Set up monitoring and alerts
- [ ] Use secrets management (AWS Secrets Manager, Azure Key Vault, etc.)
- [ ] Restrict database access to application IPs only
- [ ] Enable database encryption at rest
- [ ] Set up log aggregation
- [ ] Configure auto-updates for security patches

### Environment Variables for Production

```bash
# Required
ONENCE_USERNAME=<your-username>
ONENCE_PASSWORD=<your-password>
DATABASE_URL=postgresql://user:password@host:5432/database
SECRET_KEY=<generate-strong-random-key>

# Recommended
ENVIRONMENT=production
LOG_LEVEL=WARNING
ENABLE_EMAIL_ALERTS=true
SMTP_SERVER=smtp.gmail.com
SMTP_USERNAME=<email>
SMTP_PASSWORD=<app-password>
ALERT_EMAIL_TO=<recipient>

# Optional
REDIS_URL=redis://host:6379/0
DATA_COLLECTION_INTERVAL_MINUTES=60
USAGE_RETENTION_DAYS=180
```

---

## 📊 Monitoring Setup

### Using Grafana (Included)

1. **Access Grafana**
   - URL: http://localhost:3000
   - Default login: admin/admin

2. **Add PostgreSQL Data Source**
   - Configuration > Data Sources > Add PostgreSQL
   - Host: db:5432
   - Database: onence_db
   - User: onence_user

3. **Import Dashboards**
   - Create dashboards for:
     - SIM status overview
     - Usage trends
     - Alert history
     - System health

### Using CloudWatch (AWS)

1. **Install CloudWatch Agent**
   ```bash
   wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
   sudo dpkg -i amazon-cloudwatch-agent.deb
   ```

2. **Configure Metrics**
   - Application logs → CloudWatch Logs
   - Custom metrics for SIM counts, usage totals
   - Set up alarms for critical metrics

---

## 🔄 Backup Strategy

### Database Backups

#### Automated Backup Script

Create `scripts/backup_db.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/onence_db_$DATE.sql"

mkdir -p $BACKUP_DIR

docker-compose exec -T db pg_dump -U onence_user onence_db > $BACKUP_FILE

# Compress
gzip $BACKUP_FILE

# Delete backups older than 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

#### Schedule with Cron

```bash
# Run daily at 3 AM
0 3 * * * /path/to/scripts/backup_db.sh
```

#### Restore from Backup

```bash
gunzip backup.sql.gz
docker-compose exec -T db psql -U onence_user onence_db < backup.sql
```

---

## 📈 Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**
   - Use Nginx or cloud load balancer
   - Distribute traffic across multiple dashboard instances

2. **Database Connection Pooling**
   - Configure `pool_size` and `max_overflow` in `connection.py`
   - Use PgBouncer for connection pooling

3. **Redis Cluster**
   - For caching across multiple instances
   - Configure Redis Sentinel for high availability

### Vertical Scaling

**Small (< 100 SIMs):**
- 2GB RAM, 2 vCPU
- PostgreSQL: 2GB RAM
- Redis: 512MB RAM

**Medium (100-500 SIMs):**
- 4GB RAM, 2 vCPU
- PostgreSQL: 4GB RAM
- Redis: 1GB RAM

**Large (500-1000+ SIMs):**
- 8GB RAM, 4 vCPU
- PostgreSQL: 8GB RAM
- Redis: 2GB RAM

---

## 🔧 Maintenance

### Regular Tasks

**Weekly:**
- Review application logs
- Check disk space
- Monitor database size

**Monthly:**
- Update dependencies: `docker-compose pull`
- Review and resolve old alerts
- Clean up old logs

**Quarterly:**
- Security audit
- Performance review
- Backup restore test

### Updates

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Run migrations if needed
docker-compose exec dashboard python scripts/init_db.py
```

---

## 📞 Support & Troubleshooting

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f dashboard

# Last 100 lines
docker-compose logs --tail=100 dashboard
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart dashboard
```

### Health Checks

```bash
# Check container health
docker-compose ps

# Test database connection
docker-compose exec db psql -U onence_user -d onence_db -c "SELECT version();"

# Test API
docker-compose exec dashboard python scripts/test_api.py
```

---

**Deployment Status:** ✅ Production Ready
**Last Updated:** 2025-11-15
