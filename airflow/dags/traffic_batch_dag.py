from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def generate_report():
    print("Generating daily peak traffic hour report...")

with DAG(
    dag_id="smart_city_traffic_report",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    task = PythonOperator(
        task_id="generate_report",
        python_callable=generate_report
    )
