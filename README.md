---

# File 7: setup_kafka.sh
**Path: `scripts/setup_kafka.sh`**
```bash
#!/bin/bash

echo "=================================================="
echo "Setting up Kafka Topics for Smart City Traffic System"
echo "=================================================="

echo "Waiting for Kafka to be ready..."
sleep 10

docker exec -it kafka kafka-topics --create \
    --topic traffic-data \
    --bootstrap-server localhost:9092 \
    --partitions 4 \
    --replication-factor 1 \
    --if-not-exists

echo "Kafka topic 'traffic-data' created successfully"

echo ""
echo "Current Kafka topics:"
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092

echo ""
echo "=================================================="
echo "Kafka setup completed!"
echo "=================================================="
```

---

# File 8: run_all.sh

**Path: `scripts/run_all.sh`**

```bash
#!/bin/bash

echo "=================================================="
echo "Smart City Traffic System - Complete Setup"
echo "=================================================="

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Checking prerequisites..."

if ! command_exists docker; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command_exists python3; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "Prerequisites satisfied"
echo ""

echo "Step 1: Starting Docker containers..."
docker-compose up -d

echo "Waiting for services to be ready..."
sleep 30

echo ""
echo "Step 2: Setting up Kafka topics..."
bash scripts/setup_kafka.sh

echo ""
echo "Step 3: Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "=================================================="
echo "Setup completed successfully!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Start the traffic producer:"
echo "   python3 producer/traffic_producer.py"
echo ""
echo "2. Start Spark streaming (in a new terminal):"
echo "   python3 spark/traffic_streaming.py"
echo ""
echo "3. Access Airflow UI at http://localhost:8080"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "4. Check PostgreSQL:"
echo "   docker exec -it postgres psql -U postgres -d traffic_db"
echo ""
echo "=================================================="
```

---

# File 9: run_all.bat

**Path: `scripts/run_all.bat`**

```batch
@echo off
echo ==================================================
echo Smart City Traffic System - Complete Setup
echo ==================================================

echo Checking prerequisites...

where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed. Please install Docker first.
    exit /b 1
)

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed. Please install Python first.
    exit /b 1
)

echo Prerequisites satisfied
echo.

echo Step 1: Starting Docker containers...
docker-compose up -d

echo Waiting for services to be ready...
timeout /t 30 /nobreak

echo.
echo Step 2: Setting up Kafka topics...
docker exec -it kafka kafka-topics --create --topic traffic-data --bootstrap-server localhost:9092 --partitions 4 --replication-factor 1 --if-not-exists

echo.
echo Step 3: Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ==================================================
echo Setup completed successfully!
echo ==================================================
echo.
echo Next steps:
echo 1. Start the traffic producer:
echo    python producer/traffic_producer.py
echo.
echo 2. Start Spark streaming (in a new terminal):
echo    python spark/traffic_streaming.py
echo.
echo 3. Access Airflow UI at http://localhost:8080
echo    Username: admin
echo    Password: admin
echo.
echo ==================================================
pause
```

---

# EXECUTION INSTRUCTIONS

## Step 1: Create Project Structure

```bash
mkdir Smart-City-Traffic-System
cd Smart-City-Traffic-System
mkdir -p producer spark airflow/dags scripts data checkpoints reports
```

## Step 2: Copy All Files

Copy each file above to its respective path.

## Step 3: Start Infrastructure

```bash
# Linux/Mac
bash scripts/run_all.sh

# Windows
scripts\run_all.bat
```

## Step 4: Run Producer (Terminal 1)

```bash
python3 producer/traffic_producer.py
```

## Step 5: Run Spark Streaming (Terminal 2)

```bash
python3 spark/traffic_streaming.py
```

## Step 6: Access Airflow (Browser)

URL: http://localhost:8080
Username: admin
Password: admin

Enable and trigger the DAG: `smart_city_traffic_report`
