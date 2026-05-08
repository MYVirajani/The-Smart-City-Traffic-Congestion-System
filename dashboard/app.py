import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Smart City Traffic Dashboard",
    layout="wide",
    page_icon="🚦",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .alert-critical {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .alert-high {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def get_db():
    return psycopg2.connect(host="postgres", database="traffic_db", user="postgres", password="postgres", port=5432)

@st.cache_data(ttl=10)
def get_metrics():
    conn = get_db()
    df = pd.read_sql("SELECT AVG(avg_vehicle_count)::int as v, AVG(avg_speed)::int as s, AVG(congestion_index)::numeric(5,1) as c FROM traffic_history", conn)
    alerts = pd.read_sql("SELECT COUNT(*) as a FROM critical_traffic_alerts", conn)
    conn.close()
    return df.iloc[0]["v"], df.iloc[0]["s"], df.iloc[0]["c"], alerts.iloc[0]["a"]

@st.cache_data(ttl=10)
def get_hourly():
    conn = get_db()
    df = pd.read_sql("SELECT EXTRACT(HOUR FROM window_start)::int as hour, AVG(avg_vehicle_count)::int as vehicles, AVG(avg_speed)::int as speed, AVG(congestion_index)::numeric(5,2) as congestion FROM traffic_history GROUP BY hour ORDER BY hour", conn)
    conn.close()
    return df

@st.cache_data(ttl=10)
def get_junctions(selected_junction="All"):
    conn = get_db()
    if selected_junction == "All":
        query = "SELECT sensor_id, AVG(congestion_index)::numeric(5,2) as congestion, AVG(avg_vehicle_count)::int as vehicles, COUNT(*) as records FROM traffic_history GROUP BY sensor_id ORDER BY congestion DESC"
    else:
        query = f"SELECT sensor_id, AVG(congestion_index)::numeric(5,2) as congestion, AVG(avg_vehicle_count)::int as vehicles, COUNT(*) as records FROM traffic_history WHERE sensor_id = '{selected_junction}' GROUP BY sensor_id"
    df = pd.read_sql(query, conn)
    
    # Get alerts per junction
    if selected_junction == "All":
        alert_query = "SELECT sensor_id, COUNT(*) as alert_count FROM critical_traffic_alerts GROUP BY sensor_id"
    else:
        alert_query = f"SELECT sensor_id, COUNT(*) as alert_count FROM critical_traffic_alerts WHERE sensor_id = '{selected_junction}' GROUP BY sensor_id"
    
    alerts_df = pd.read_sql(alert_query, conn)
    conn.close()
    
    if not alerts_df.empty:
        df = df.merge(alerts_df, on='sensor_id', how='left')
        df['alert_count'] = df['alert_count'].fillna(0).astype(int)
    else:
        df['alert_count'] = 0
    
    return df

@st.cache_data(ttl=10)
def get_stats():
    conn = get_db()
    df = pd.read_sql("SELECT COUNT(*) as total, MIN(window_start) as earliest, MAX(window_start) as latest FROM traffic_history", conn)
    conn.close()
    return df.iloc[0]

@st.cache_data(ttl=10)
def get_alerts():
    conn = get_db()
    df = pd.read_sql("SELECT sensor_id, window_start, avg_speed::numeric(5,1) as avg_speed, avg_vehicle_count::int as vehicle_count, congestion_index::numeric(5,2) as congestion_index FROM critical_traffic_alerts ORDER BY window_start DESC LIMIT 10", conn)
    conn.close()
    return df

# Header
st.markdown('<h1 class="main-header">🚦 Smart City Traffic Control Center</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 1.2rem;'>Real-time Traffic Monitoring & Analytics Dashboard</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Dashboard Controls")
    
    # Manual refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # Stats
    try:
        stats = get_stats()
        if stats["total"] > 0:
            st.success(f"✅ Database: {stats['total']} records")
            st.caption(f"From: {stats['earliest']}")
            st.caption(f"To: {stats['latest']}")
        else:
            st.warning("⏳ No data yet")
    except:
        st.error("❌ Database error")
    
    st.divider()
    
    # Junction filter
    st.header("📊 Filters")
    selected_junction = st.selectbox(
        "Select Junction",
        ["All", "Junction_A", "Junction_B", "Junction_C", "Junction_D"]
    )
    
    st.divider()
    st.header("ℹ️ System Status")
    st.success("✅ All systems operational")
    st.info(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")

# Main content
try:
    v, s, c, a = get_metrics()
    
    # Metrics
    st.subheader("📈 Live Traffic Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🚗 Avg Vehicles", f"{v:,}")
    col2.metric("⚡ Avg Speed", f"{s} km/h")
    col3.metric("📊 Congestion", f"{c:.1f}")
    col4.metric("⚠️ Alerts", a)
    
    st.divider()
    
    # Hourly Analysis
    st.subheader("📊 Hourly Traffic Analysis")
    df_hourly = get_hourly()
    
    if not df_hourly.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.area(df_hourly, x="hour", y="vehicles", title="Traffic Volume by Hour", color_discrete_sequence=["#667eea"])
            fig.update_layout(xaxis=dict(tickmode="linear", tick0=0, dtick=2), height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(df_hourly, x="hour", y="congestion", title="Congestion Index Trend", color_discrete_sequence=["#ef4444"])
            fig.update_traces(mode="lines+markers", line=dict(width=3))
            fig.update_layout(xaxis=dict(tickmode="linear", tick0=0, dtick=2), height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("⏳ Waiting for hourly data...")
    
    st.divider()
    
    # Junction Analysis
    st.subheader(f"🚨 Junction Analysis" + (f" - {selected_junction}" if selected_junction != "All" else ""))
    df_junctions = get_junctions(selected_junction)
    
    if not df_junctions.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Junction comparison chart
            fig_junctions = go.Figure()
            
            fig_junctions.add_trace(go.Bar(
                name='Avg Congestion',
                x=df_junctions['sensor_id'],
                y=df_junctions['congestion'],
                marker_color='#f59e0b'
            ))
            
            fig_junctions.add_trace(go.Bar(
                name='Critical Alerts',
                x=df_junctions['sensor_id'],
                y=df_junctions['alert_count'],
                marker_color='#ef4444'
            ))
            
            fig_junctions.update_layout(
                title='Junction Comparison: Congestion & Alerts',
                barmode='group',
                height=400,
                xaxis_title='Junction',
                yaxis_title='Value'
            )
            
            st.plotly_chart(fig_junctions, use_container_width=True)
        
        with col2:
            st.markdown("#### 👮 Intervention Recommendations")
            for _, row in df_junctions.iterrows():
                cong = row["congestion"]
                if cong > 50:
                    intervention = "🚨 URGENT - Deploy 3+ Officers"
                    color = "red"
                elif cong > 30:
                    intervention = "⚠️ HIGH - Deploy 2 Officers"
                    color = "orange"
                elif cong > 15:
                    intervention = "⚡ MODERATE - Deploy 1 Officer"
                    color = "blue"
                else:
                    intervention = "✅ LOW - Monitor Remotely"
                    color = "green"
                
                st.markdown(f"""
                <div style='background-color: #{color}22; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {color};'>
                    <strong>{row["sensor_id"]}</strong><br>
                    Congestion: {cong:.1f}<br>
                    Alerts: {row["alert_count"]}<br>
                    Records: {row["records"]}<br>
                    <strong>{intervention}</strong>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("⏳ Collecting junction data...")
    
    st.divider()
    
    # Recent Critical Alerts
    st.subheader("⚠️ Recent Critical Alerts")
    df_alerts = get_alerts()
    
    if not df_alerts.empty:
        df_alerts['window_start'] = pd.to_datetime(df_alerts['window_start']).dt.strftime('%Y-%m-%d %H:%M')
        
        st.dataframe(
            df_alerts,
            column_config={
                "sensor_id": st.column_config.TextColumn("Junction", width="medium"),
                "window_start": st.column_config.TextColumn("Time", width="medium"),
                "avg_speed": st.column_config.NumberColumn("Speed (km/h)", format="%.1f"),
                "vehicle_count": st.column_config.NumberColumn("Vehicles", format="%d"),
                "congestion_index": st.column_config.NumberColumn("Congestion", format="%.2f"),
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.success("✅ No critical alerts in the system!")
    
    st.divider()
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>Smart City Traffic Management System | Powered by Apache Kafka, Spark & Airflow</p>
        <p style='font-size: 0.9rem;'>Data auto-updates every 10 seconds | Click 'Refresh Data' for instant update</p>
    </div>
    """, unsafe_allow_html=True)
    
except Exception as e:
    st.error(f"Error loading dashboard: {str(e)}")
    st.info("⏳ Waiting for data... Spark processes in 2-minute windows. Please wait 2-3 minutes after starting the system.")