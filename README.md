# Smart City Traffic Congestion System

A real-time traffic monitoring and analysis pipeline built for the city of Colombo. The system simulates IoT sensors at 4 major junctions, processes traffic data as it streams in, detects congestion events, and generates nightly reports recommending where to deploy traffic police.

---

## How It Works

Fake sensors send traffic data every second → Kafka holds the messages → Spark processes them in 2-minute windows and saves results to PostgreSQL → A Streamlit dashboard shows live stats → Airflow runs every night and generates a police deployment report.

---

## Project Structure

```
The-Smart-City-Traffic-Congestion-System/
├── producer/
│   ├── traffic_producer.py       # Fake sensor — sends traffic data to Kafka
│   ├── Dockerfile
│   └── requirements.txt
├── spark/
│   ├── traffic_streaming.py      # Reads Kafka, calculates congestion, writes to DB
│   └── Dockerfile
├── airflow/
│   ├── dags/
│   │   └── traffic_batch_dag.py  # Nightly report generation DAG
│   └── requirements.txt
├── dashboard/
│   ├── app.py                    # Streamlit live dashboard
│   ├── Dockerfile
│   └── requirements.txt
├── init.sql                      # Creates PostgreSQL tables on first run
├── docker-compose.yml            # Starts all services together
└── requirements.txt
```

---

## Tech Stack

| Component         | Technology                        | Purpose                                       |
| ----------------- | --------------------------------- | --------------------------------------------- |
| Data ingestion    | Apache Kafka                      | Message queue between producer and Spark      |
| Stream processing | Apache Spark Structured Streaming | Real-time windowed aggregation                |
| Orchestration     | Apache Airflow                    | Nightly batch report scheduling               |
| Database          | PostgreSQL                        | Stores all traffic data and alerts            |
| File storage      | Parquet                           | Backup of processed data for offline analysis |
| Dashboard         | Streamlit + Plotly                | Live monitoring UI                            |
| Infrastructure    | Docker + Docker Compose           | Runs all services in containers               |

---

## Tools and Technologies

### Apache Kafka 7.5.0

Kafka acts as the message broker between the producer and Spark. The producer sends one message per second to a Kafka topic called `traffic-data`. Spark reads from that topic as a continuous stream. Kafka ensures no messages are lost even if Spark is momentarily busy. Zookeeper runs alongside Kafka to manage broker coordination.

- **Topic:** `traffic-data`
- **Broker:** `kafka:9092`
- **Zookeeper:** `zookeeper:2181`

### Apache Spark 3.4.1 (Structured Streaming)

Spark is the core processing engine. It reads the Kafka stream, groups data into 2-minute tumbling windows per junction, and calculates the congestion index. It uses a 30-second watermark to handle any late-arriving data. Results are written to PostgreSQL every 15 seconds via JDBC. A separate stream filters critical alerts (speed < 10 km/h) and writes them to a different table immediately.

- **Mode:** Structured Streaming with `foreachBatch`
- **Window size:** 2 minutes
- **Watermark:** 30 seconds
- **Processing trigger:** every 15 seconds
- **Output modes:** Parquet files + PostgreSQL via JDBC

### Apache Airflow 2.7.0

Airflow handles the batch/reporting side of the pipeline. It runs a DAG called `smart_city_traffic_report` on a daily schedule (1 AM). The DAG has 3 sequential Python tasks connected using XCom to pass data between them. Airflow uses its own separate PostgreSQL database for storing DAG metadata, task states, and logs.

- **Executor:** LocalExecutor
- **Schedule:** `0 1 * * *` (1 AM daily)
- **DAG:** `smart_city_traffic_report`
- **Tasks:** `extract_daily_traffic` → `analyze_peak_hours` → `generate_report`

### PostgreSQL 14

Two separate PostgreSQL instances are used. One stores all traffic data (traffic_history, critical_traffic_alerts, daily_reports). The other is exclusively for Airflow's internal metadata. Both run as Docker containers with persistent volumes so data survives restarts.

- **Traffic DB:** `postgres:5432` — database `traffic_db`
- **Airflow DB:** `postgres-airflow:5433` — database `airflow_db`

### Streamlit

Streamlit powers the live dashboard at `localhost:8501`. It re-queries the PostgreSQL database every 10 seconds using `@st.cache_data(ttl=10)`. Plotly is used for interactive charts (area charts, line charts, grouped bar charts). The dashboard shows live metrics, hourly trends, per-junction analysis, intervention recommendations, and recent alerts.

- **Version:** Latest stable
- **Charts:** Plotly Express + Plotly Graph Objects
- **Refresh rate:** 10 seconds (auto-cache expiry)

### Docker and Docker Compose

All 9 services run as Docker containers defined in a single `docker-compose.yml` file. Services use health checks to wait for their dependencies before starting (e.g. Spark waits for both Kafka and PostgreSQL to be healthy). A shared `traffic-network` bridge network allows all containers to communicate using their service names as hostnames.

- **Services:** zookeeper, kafka, postgres, postgres-airflow, producer, spark, airflow-init, airflow-webserver, airflow-scheduler, dashboard
- **Network:** `traffic-network` (bridge)
- **Persistent volumes:** `postgres_data`, `postgres_airflow_data`

### Python Libraries

| Library                  | Used In            | Purpose                                     |
| ------------------------ | ------------------ | ------------------------------------------- |
| `kafka-python`           | Producer           | Sending messages to Kafka                   |
| `pyspark`                | Spark              | Stream processing and windowed aggregations |
| `psycopg2-binary`        | Dashboard, Airflow | Connecting to PostgreSQL                    |
| `pandas`                 | Airflow            | Data manipulation in batch tasks            |
| `matplotlib` + `seaborn` | Airflow            | Generating report charts                    |
| `streamlit`              | Dashboard          | Web UI framework                            |
| `plotly`                 | Dashboard          | Interactive charts                          |
| `numpy`                  | Airflow            | Numerical operations                        |

---

## Prerequisites

- Docker Desktop (minimum 6 GB RAM allocated)
- Docker Compose (included with Docker Desktop)

---

## Getting Started

**1. Clone the repository**

```bash
git clone <your-repo-url>
cd The-Smart-City-Traffic-Congestion-System
```

**2. Create required directories**

```bash
mkdir -p reports data checkpoints ivy-cache
```

**3. Start all services**

```bash
docker-compose up --build
```

First run takes 10–20 minutes as Docker downloads images and Spark downloads its JAR packages. Subsequent runs are much faster.

**4. Wait for data**

Spark processes data in 2-minute windows. Wait about 2–3 minutes after startup before the dashboard shows any data.

---

## Accessing the System

| Interface      | URL                   | Login           |
| -------------- | --------------------- | --------------- |
| Live Dashboard | http://localhost:8501 | No login needed |
| Airflow UI     | http://localhost:8081 | admin / admin   |

---

## The Data

Each fake sensor sends one message per second in this format:

```json
{
  "sensor_id": "Junction_A",
  "timestamp": "2026-05-04T08:30:00",
  "vehicle_count": 124,
  "avg_speed": 12
}
```

This represents the total number of vehicles passing through a junction at that moment and their average speed — not individual vehicle tracking.

**Junctions monitored:** Junction_A, Junction_B, Junction_C, Junction_D

**Traffic patterns simulated:**

| Time                  | Vehicle Count | Speed                    |
| --------------------- | ------------- | ------------------------ |
| Morning peak (7–9 AM) | 100–150       | 5–35 km/h (weighted low) |
| Evening peak (5–7 PM) | 110–160       | Even slower              |
| Lunch (12–2 PM)       | 70–110        | 12–40 km/h               |
| Night (10 PM–5 AM)    | 10–40         | 30–45 km/h               |
| Off-peak              | 40–90         | 20–40 km/h               |

Critical congestion events (speed 3–9 km/h) are injected randomly to simulate real jams.

---

## Congestion Index

Spark calculates a congestion index for every 2-minute window:

```
congestion_index = (avg_vehicle_count / (avg_speed + 1)) × 10
```

The higher the vehicles and the lower the speed, the worse the congestion.

---

## Alert Trigger

If the average speed across a 2-minute window drops below **10 km/h**, that window is written to the `critical_traffic_alerts` table immediately.

---

## Nightly Report (Airflow)

The Airflow DAG `smart_city_traffic_report` runs at 1 AM every night. It has 3 tasks:

1. **extract_daily_traffic** — pulls yesterday's data from PostgreSQL
2. **analyze_peak_hours** — finds the busiest hour for each junction
3. **generate_report** — creates 3 files in the `reports/` folder:
   - `traffic_visualization_YYYYMMDD.png` — charts of traffic volume and congestion
   - `intervention_report_YYYYMMDD.txt` — police deployment recommendations
   - `daily_summary_YYYYMMDD.csv` — peak hour data per junction

To trigger the report manually: go to http://localhost:8081, find the `smart_city_traffic_report` DAG, unpause it, and click the Run button.

---

## Police Intervention Thresholds

| Congestion Index | Recommendation                    |
| ---------------- | --------------------------------- |
| > 50             | URGENT — Deploy 3+ officers       |
| 30–50            | HIGH PRIORITY — Deploy 2 officers |
| 15–30            | MODERATE — Deploy 1 officer       |
| < 15             | LOW — Monitor remotely            |

---

## Database Tables

**traffic_history** — all processed 2-minute window aggregations

**critical_traffic_alerts** — only windows where avg speed dropped below 10 km/h

**daily_reports** — metadata about each nightly report (worst junction, peak time, alert count)

---

## Stopping the System

```bash
# Stop all services but keep data
docker-compose down

# Stop and delete all saved data (full reset)
docker-compose down -v
```
