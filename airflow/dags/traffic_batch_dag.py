# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime

# def generate_report():
#     print("Generating daily peak traffic hour report...")

# with DAG(
#     dag_id="smart_city_traffic_report",
#     start_date=datetime(2025, 1, 1),
#     schedule_interval="@daily",
#     catchup=False
# ) as dag:

#     task = PythonOperator(
#         task_id="generate_report",
#         python_callable=generate_report
#     )

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    'host': 'postgres',
    'database': 'traffic_db',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

REPORTS_DIR = '/opt/airflow/reports'
TEMP_DIR = '/tmp'

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def extract_daily_traffic(**context):
    logger.info("=" * 70)
    logger.info("TASK 1: Extracting daily traffic data...")
    logger.info("=" * 70)
    
    try:
        conn = get_db_connection()
        execution_date = context['execution_date']
        target_date = execution_date - timedelta(days=1)
        
        logger.info(f"Target Date: {target_date.strftime('%Y-%m-%d')}")
        
        query_alerts = """
            SELECT 
                sensor_id,
                window_start,
                window_end,
                avg_speed,
                avg_vehicle_count,
                congestion_index,
                alert_generated_at
            FROM critical_traffic_alerts
            WHERE DATE(window_start) = %s
            ORDER BY window_start
        """
        
        df_alerts = pd.read_sql(query_alerts, conn, params=(target_date.date(),))
        logger.info(f"Extracted {len(df_alerts)} critical alert records")
        
        query_history = """
            SELECT 
                sensor_id,
                window_start,
                window_end,
                avg_speed,
                avg_vehicle_count,
                reading_count,
                congestion_index
            FROM traffic_history
            WHERE DATE(window_start) = %s
            ORDER BY window_start
        """
        
        df_history = pd.read_sql(query_history, conn, params=(target_date.date(),))
        logger.info(f"Extracted {len(df_history)} total traffic records")
        
        conn.close()
        
        alerts_file = f'{TEMP_DIR}/daily_traffic_alerts_{target_date.strftime("%Y%m%d")}.csv'
        history_file = f'{TEMP_DIR}/daily_traffic_history_{target_date.strftime("%Y%m%d")}.csv'
        
        df_alerts.to_csv(alerts_file, index=False)
        df_history.to_csv(history_file, index=False)
        
        logger.info(f"Saved alerts to: {alerts_file}")
        logger.info(f"Saved history to: {history_file}")
        
        context['ti'].xcom_push(key='alerts_file', value=alerts_file)
        context['ti'].xcom_push(key='history_file', value=history_file)
        context['ti'].xcom_push(key='target_date', value=target_date.strftime('%Y-%m-%d'))
        context['ti'].xcom_push(key='alerts_count', value=len(df_alerts))
        context['ti'].xcom_push(key='history_count', value=len(df_history))
        
        logger.info("=" * 70)
        logger.info("TASK 1 COMPLETED: Data extraction successful")
        logger.info("=" * 70)
        
        return len(df_history)
        
    except Exception as e:
        logger.error(f"Error in extract_daily_traffic: {str(e)}")
        raise

def analyze_peak_hours(**context):
    logger.info("=" * 70)
    logger.info("TASK 2: Analyzing peak traffic hours...")
    logger.info("=" * 70)
    
    try:
        history_file = context['ti'].xcom_pull(key='history_file', task_ids='extract_daily_traffic')
        target_date = context['ti'].xcom_pull(key='target_date', task_ids='extract_daily_traffic')
        
        df = pd.read_csv(history_file)
        logger.info(f"Loaded {len(df)} records from {history_file}")
        
        if df.empty:
            logger.warning("No data to analyze")
            context['ti'].xcom_push(key='peak_hours', value=[])
            return
        
        df['window_start'] = pd.to_datetime(df['window_start'])
        df['hour'] = df['window_start'].dt.hour
        df['day_period'] = df['hour'].apply(lambda x: 
            'Morning Peak (7-9)' if 7 <= x < 9
            else 'Evening Peak (17-19)' if 17 <= x < 19
            else 'Lunch (12-14)' if 12 <= x < 14
            else 'Night (22-5)' if x >= 22 or x < 5
            else 'Off-Peak'
        )
        
        hourly_analysis = df.groupby(['sensor_id', 'hour']).agg({
            'congestion_index': 'mean',
            'avg_vehicle_count': 'mean',
            'avg_speed': 'mean',
            'reading_count': 'sum'
        }).reset_index()
        
        hourly_analysis.columns = ['sensor_id', 'hour', 'avg_congestion_index', 
                                     'avg_vehicle_count', 'avg_speed', 'total_readings']
        
        logger.info(f"Hourly aggregation completed: {len(hourly_analysis)} records")
        
        peak_hours = hourly_analysis.loc[
            hourly_analysis.groupby('sensor_id')['avg_congestion_index'].idxmax()
        ]
        
        logger.info("=" * 70)
        logger.info("PEAK TRAFFIC HOURS BY JUNCTION:")
        logger.info("=" * 70)
        
        for _, row in peak_hours.iterrows():
            logger.info(f"{row['sensor_id']}:")
            logger.info(f"   Peak Hour: {int(row['hour'])}:00")
            logger.info(f"   Avg Vehicles: {row['avg_vehicle_count']:.1f}")
            logger.info(f"   Avg Speed: {row['avg_speed']:.1f} km/h")
            logger.info(f"   Congestion Index: {row['avg_congestion_index']:.2f}")
        
        analysis_file = f'{TEMP_DIR}/peak_hours_analysis_{target_date.replace("-", "")}.csv'
        peak_hours.to_csv(analysis_file, index=False)
        hourly_analysis.to_csv(
            f'{TEMP_DIR}/hourly_analysis_{target_date.replace("-", "")}.csv',
            index=False
        )
        
        logger.info(f"Saved analysis to: {analysis_file}")
        
        context['ti'].xcom_push(key='peak_hours', value=peak_hours.to_dict('records'))
        context['ti'].xcom_push(key='analysis_file', value=analysis_file)
        context['ti'].xcom_push(key='hourly_analysis', value=hourly_analysis.to_dict('records'))
        
        logger.info("=" * 70)
        logger.info("TASK 2 COMPLETED: Peak hour analysis successful")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"Error in analyze_peak_hours: {str(e)}")
        raise

def generate_report(**context):
    logger.info("=" * 70)
    logger.info("TASK 3: Generating traffic report...")
    logger.info("=" * 70)
    
    try:
        target_date = context['ti'].xcom_pull(key='target_date', task_ids='extract_daily_traffic')
        history_file = context['ti'].xcom_pull(key='history_file', task_ids='extract_daily_traffic')
        alerts_file = context['ti'].xcom_pull(key='alerts_file', task_ids='extract_daily_traffic')
        peak_hours = pd.DataFrame(context['ti'].xcom_pull(key='peak_hours', task_ids='analyze_peak_hours'))
        hourly_analysis = pd.DataFrame(context['ti'].xcom_pull(key='hourly_analysis', task_ids='analyze_peak_hours'))
        
        df_history = pd.read_csv(history_file)
        df_alerts = pd.read_csv(alerts_file)
        
        if df_history.empty:
            logger.warning("No data available for report generation")
            return
        
        df_history['window_start'] = pd.to_datetime(df_history['window_start'])
        df_history['hour'] = df_history['window_start'].dt.hour
        
        sns.set_style("whitegrid")
        plt.rcParams['figure.facecolor'] = 'white'
        
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        fig.suptitle(f'Smart City Traffic Analysis Report - {target_date}', 
                     fontsize=20, fontweight='bold', y=0.98)
        
        ax1 = fig.add_subplot(gs[0, :2])
        hourly_volume = df_history.groupby('hour')['avg_vehicle_count'].mean()
        ax1.bar(hourly_volume.index, hourly_volume.values, color='steelblue', alpha=0.7, edgecolor='black')
        ax1.set_title('Average Traffic Volume by Hour of Day', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Hour of Day', fontsize=12)
        ax1.set_ylabel('Average Vehicle Count', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(range(24))
        
        ax2 = fig.add_subplot(gs[0, 2])
        congestion_by_hour = df_history.groupby('hour')['congestion_index'].mean()
        ax2.plot(congestion_by_hour.index, congestion_by_hour.values, 
                 marker='o', linewidth=2, color='red', markersize=6)
        ax2.set_title('Average Congestion Index', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Hour', fontsize=12)
        ax2.set_ylabel('Congestion Index', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.fill_between(congestion_by_hour.index, congestion_by_hour.values, alpha=0.3, color='red')
        
        junctions = df_history['sensor_id'].unique()
        for idx, junction in enumerate(junctions[:4]):
            ax = fig.add_subplot(gs[1 + idx//2, idx%2])
            junction_data = df_history[df_history['sensor_id'] == junction]
            
            hourly_avg = junction_data.groupby('hour')['avg_vehicle_count'].mean()
            
            bars = ax.bar(hourly_avg.index, hourly_avg.values, color='teal', alpha=0.6, edgecolor='black')
            
            if not peak_hours.empty:
                peak_hour_row = peak_hours[peak_hours['sensor_id'] == junction]
                if not peak_hour_row.empty:
                    peak_hour = int(peak_hour_row.iloc[0]['hour'])
                    if peak_hour in hourly_avg.index:
                        bars[list(hourly_avg.index).index(peak_hour)].set_color('red')
                        bars[list(hourly_avg.index).index(peak_hour)].set_alpha(0.8)
            
            ax.set_title(f'{junction} - Traffic Volume', fontsize=12, fontweight='bold')
            ax.set_xlabel('Hour of Day', fontsize=10)
            ax.set_ylabel('Avg Vehicle Count', fontsize=10)
            ax.grid(True, alpha=0.3, axis='y')
        
        ax7 = fig.add_subplot(gs[2, :])
        if not df_alerts.empty:
            alerts_by_junction = df_alerts.groupby('sensor_id').size()
            ax7.barh(alerts_by_junction.index, alerts_by_junction.values, color='orangered', alpha=0.7)
            ax7.set_title('Critical Traffic Alerts by Junction', fontsize=14, fontweight='bold')
            ax7.set_xlabel('Number of Critical Alerts', fontsize=12)
            ax7.set_ylabel('Junction', fontsize=12)
            ax7.grid(True, alpha=0.3, axis='x')
            
            for i, v in enumerate(alerts_by_junction.values):
                ax7.text(v + 0.5, i, str(v), va='center', fontweight='bold')
        else:
            ax7.text(0.5, 0.5, 'No Critical Alerts', 
                    ha='center', va='center', fontsize=16, transform=ax7.transAxes)
            ax7.axis('off')
        
        viz_filename = f'traffic_visualization_{target_date.replace("-", "")}.png'
        viz_path = os.path.join(REPORTS_DIR, viz_filename)
        plt.savefig(viz_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualization saved: {viz_path}")
        
        report_filename = f'intervention_report_{target_date.replace("-", "")}.txt'
        report_path = os.path.join(REPORTS_DIR, report_filename)
        
        with open(report_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("SMART CITY TRAFFIC MANAGEMENT SYSTEM\n")
            f.write("DAILY INTERVENTION REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Report Date: {target_date}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("EXECUTIVE SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Total Traffic Records Analyzed: {len(df_history)}\n")
            f.write(f"Critical Alerts Triggered: {len(df_alerts)}\n")
            f.write(f"Junctions Monitored: {len(junctions)}\n")
            f.write(f"Average Daily Congestion Index: {df_history['congestion_index'].mean():.2f}\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("JUNCTIONS REQUIRING POLICE INTERVENTION\n")
            f.write("=" * 80 + "\n\n")
            
            if not peak_hours.empty:
                for _, row in peak_hours.iterrows():
                    f.write(f"Junction: {row['sensor_id']}\n")
                    f.write(f"  Peak Traffic Hour: {int(row['hour'])}:00 - {int(row['hour'])+1}:00\n")
                    f.write(f"  Average Vehicle Count: {row['avg_vehicle_count']:.1f}\n")
                    f.write(f"  Average Speed: {row['avg_speed']:.1f} km/h\n")
                    f.write(f"  Congestion Index: {row['avg_congestion_index']:.2f}\n")
                    
                    if row['avg_congestion_index'] > 50:
                        intervention = "URGENT - Deploy 3+ traffic officers"
                    elif row['avg_congestion_index'] > 30:
                        intervention = "HIGH PRIORITY - Deploy 2 traffic officers"
                    elif row['avg_congestion_index'] > 15:
                        intervention = "MODERATE - Deploy 1 traffic officer"
                    else:
                        intervention = "LOW - Monitor remotely"
                    
                    f.write(f"  Recommendation: {intervention}\n\n")
            
            if not df_alerts.empty:
                f.write("=" * 80 + "\n")
                f.write("CRITICAL ALERTS SUMMARY\n")
                f.write("=" * 80 + "\n\n")
                
                for junction in junctions:
                    junction_alerts = df_alerts[df_alerts['sensor_id'] == junction]
                    if not junction_alerts.empty:
                        f.write(f"\n{junction}:\n")
                        f.write(f"  Total Critical Alerts: {len(junction_alerts)}\n")
                        f.write(f"  Lowest Speed Recorded: {junction_alerts['avg_speed'].min():.1f} km/h\n")
                        f.write(f"  Highest Congestion Index: {junction_alerts['congestion_index'].max():.2f}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
        
        logger.info(f"Text report saved: {report_path}")
        
        csv_filename = f'daily_summary_{target_date.replace("-", "")}.csv'
        csv_path = os.path.join(REPORTS_DIR, csv_filename)
        peak_hours.to_csv(csv_path, index=False)
        
        logger.info(f"CSV summary saved: {csv_path}")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            worst_junction = peak_hours.loc[peak_hours['avg_congestion_index'].idxmax(), 'sensor_id'] if not peak_hours.empty else None
            peak_time = df_history.loc[df_history['congestion_index'].idxmax(), 'window_start'] if not df_history.empty else None
            
            cursor.execute("""
                INSERT INTO daily_reports (report_date, total_alerts, peak_congestion_time, worst_junction, report_path)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (report_date) DO UPDATE
                SET total_alerts = EXCLUDED.total_alerts,
                    peak_congestion_time = EXCLUDED.peak_congestion_time,
                    worst_junction = EXCLUDED.worst_junction,
                    report_path = EXCLUDED.report_path
            """, (target_date, len(df_alerts), peak_time, worst_junction, report_path))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info("Updated daily_reports table")
            
        except Exception as e:
            logger.warning(f"Could not update daily_reports table: {str(e)}")
        
        logger.info("=" * 70)
        logger.info("TASK 3 COMPLETED: Report generation successful")
        logger.info("=" * 70)
        logger.info(f"Reports saved in: {REPORTS_DIR}")
        logger.info(f"   - Visualization: {viz_filename}")
        logger.info(f"   - Text Report: {report_filename}")
        logger.info(f"   - CSV Summary: {csv_filename}")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"Error in generate_report: {str(e)}")
        raise

default_args = {
    'owner': 'traffic_system',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='smart_city_traffic_report',
    default_args=default_args,
    description='Daily traffic analysis and intervention report generation',
    schedule_interval='0 1 * * *',
    start_date=days_ago(1),
    catchup=False,
    tags=['traffic', 'smart-city', 'batch-processing'],
) as dag:
    
    extract_task = PythonOperator(
        task_id='extract_daily_traffic',
        python_callable=extract_daily_traffic,
        provide_context=True,
    )
    
    analyze_task = PythonOperator(
        task_id='analyze_peak_hours',
        python_callable=analyze_peak_hours,
        provide_context=True,
    )
    
    report_task = PythonOperator(
        task_id='generate_report',
        python_callable=generate_report,
        provide_context=True,
    )
    
    extract_task >> analyze_task >> report_task
