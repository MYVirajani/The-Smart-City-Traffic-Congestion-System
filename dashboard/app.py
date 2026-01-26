# # # import React, { useState, useEffect } from 'react';
# # # import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart, PieChart, Pie, Cell } from 'recharts';
# # # import { AlertTriangle, Activity, TrendingUp, Clock, MapPin } from 'lucide-react';

# # # const TrafficDashboard = () => {
# # #   const [currentTime, setCurrentTime] = useState(new Date());
# # #   const [selectedJunction, setSelectedJunction] = useState('All');
# # #   const [autoRefresh, setAutoRefresh] = useState(true);

# # #   // Simulated real-time data - in production, fetch from PostgreSQL
# # #   const [dashboardData, setDashboardData] = useState({
# # #     liveMetrics: {
# # #       totalVehicles: 1245,
# # #       avgSpeed: 28,
# # #       activeAlerts: 3,
# # #       congestionIndex: 35.2
# # #     },
# # #     junctions: ['Junction_A', 'Junction_B', 'Junction_C', 'Junction_D'],
# # #     hourlyTraffic: [
# # #       { hour: '00:00', vehicles: 25, speed: 45, congestion: 5 },
# # #       { hour: '01:00', vehicles: 18, speed: 48, congestion: 3 },
# # #       { hour: '02:00', vehicles: 15, speed: 50, congestion: 2 },
# # #       { hour: '03:00', vehicles: 12, speed: 52, congestion: 2 },
# # #       { hour: '04:00', vehicles: 20, speed: 48, congestion: 4 },
# # #       { hour: '05:00', vehicles: 45, speed: 40, congestion: 10 },
# # #       { hour: '06:00', vehicles: 85, speed: 30, congestion: 22 },
# # #       { hour: '07:00', vehicles: 135, speed: 15, congestion: 65 },
# # #       { hour: '08:00', vehicles: 145, speed: 12, congestion: 75 },
# # #       { hour: '09:00', vehicles: 110, speed: 25, congestion: 45 },
# # #       { hour: '10:00', vehicles: 75, speed: 32, congestion: 28 },
# # #       { hour: '11:00', vehicles: 80, speed: 30, congestion: 30 },
# # #       { hour: '12:00', vehicles: 95, speed: 25, congestion: 38 },
# # #       { hour: '13:00', vehicles: 100, speed: 22, congestion: 42 },
# # #       { hour: '14:00', vehicles: 85, speed: 28, congestion: 32 },
# # #       { hour: '15:00', vehicles: 90, speed: 26, congestion: 35 },
# # #       { hour: '16:00', vehicles: 115, speed: 18, congestion: 55 },
# # #       { hour: '17:00', vehicles: 150, speed: 10, congestion: 80 },
# # #       { hour: '18:00', vehicles: 155, speed: 8, congestion: 85 },
# # #       { hour: '19:00', vehicles: 120, speed: 20, congestion: 50 },
# # #       { hour: '20:00', vehicles: 90, speed: 28, congestion: 32 },
# # #       { hour: '21:00', vehicles: 65, speed: 35, congestion: 22 },
# # #       { hour: '22:00', vehicles: 45, speed: 40, congestion: 15 },
# # #       { hour: '23:00', vehicles: 30, speed: 42, congestion: 8 }
# # #     ],
# # #     junctionData: [
# # #       { name: 'Junction_A', alerts: 8, peakHour: '08:00', avgCongestion: 42.5, color: '#ef4444' },
# # #       { name: 'Junction_B', alerts: 5, peakHour: '17:30', avgCongestion: 38.2, color: '#f59e0b' },
# # #       { name: 'Junction_C', alerts: 3, peakHour: '08:30', avgCongestion: 28.7, color: '#10b981' },
# # #       { name: 'Junction_D', alerts: 2, peakHour: '18:00', avgCongestion: 25.1, color: '#3b82f6' }
# # #     ],
# # #     recentAlerts: [
# # #       { id: 1, junction: 'Junction_A', time: '08:15', speed: 8, vehicles: 142, severity: 'critical' },
# # #       { id: 2, junction: 'Junction_B', time: '08:22', speed: 9, vehicles: 138, severity: 'critical' },
# # #       { id: 3, junction: 'Junction_A', time: '17:45', speed: 7, vehicles: 155, severity: 'critical' }
# # #     ],
# # #     trafficDistribution: [
# # #       { period: 'Morning Peak', value: 35, color: '#ef4444' },
# # #       { period: 'Off-Peak', value: 25, color: '#10b981' },
# # #       { period: 'Lunch', value: 15, color: '#f59e0b' },
# # #       { period: 'Evening Peak', value: 20, color: '#dc2626' },
# # #       { period: 'Night', value: 5, color: '#6366f1' }
# # #     ]
# # #   });

# # #   useEffect(() => {
# # #     const timer = setInterval(() => {
# # #       setCurrentTime(new Date());
      
# # #       if (autoRefresh) {
# # #         // Simulate data updates
# # #         setDashboardData(prev => ({
# # #           ...prev,
# # #           liveMetrics: {
# # #             ...prev.liveMetrics,
# # #             totalVehicles: Math.floor(800 + Math.random() * 600),
# # #             avgSpeed: Math.floor(15 + Math.random() * 25),
# # #             congestionIndex: parseFloat((20 + Math.random() * 40).toFixed(1))
# # #           }
# # #         }));
# # #       }
# # #     }, 3000);

# # #     return () => clearInterval(timer);
# # #   }, [autoRefresh]);

# # #   const getSeverityColor = (severity) => {
# # #     switch(severity) {
# # #       case 'critical': return 'bg-red-100 border-red-500 text-red-800';
# # #       case 'high': return 'bg-orange-100 border-orange-500 text-orange-800';
# # #       default: return 'bg-yellow-100 border-yellow-500 text-yellow-800';
# # #     }
# # #   };

# # #   const getInterventionLevel = (congestion) => {
# # #     if (congestion > 50) return { text: 'URGENT - Deploy 3+ Officers', color: 'text-red-600', bg: 'bg-red-50' };
# # #     if (congestion > 30) return { text: 'HIGH - Deploy 2 Officers', color: 'text-orange-600', bg: 'bg-orange-50' };
# # #     if (congestion > 15) return { text: 'MODERATE - Deploy 1 Officer', color: 'text-yellow-600', bg: 'bg-yellow-50' };
# # #     return { text: 'LOW - Monitor Remotely', color: 'text-green-600', bg: 'bg-green-50' };
# # #   };

# # #   return (
# # #     <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
# # #       {/* Header */}
# # #       <div className="mb-8">
# # #         <div className="flex items-center justify-between">
# # #           <div>
# # #             <h1 className="text-4xl font-bold text-white mb-2">
# # #               🚦 Smart City Traffic Control Center
# # #             </h1>
# # #             <p className="text-slate-400">Real-time Traffic Monitoring & Analytics Dashboard</p>
# # #           </div>
# # #           <div className="text-right">
# # #             <div className="text-2xl font-mono text-white">
# # #               {currentTime.toLocaleTimeString()}
# # #             </div>
# # #             <div className="text-slate-400 text-sm">
# # #               {currentTime.toLocaleDateString()}
# # #             </div>
# # #           </div>
# # #         </div>
        
# # #         <div className="flex gap-4 mt-4">
# # #           <button
# # #             onClick={() => setAutoRefresh(!autoRefresh)}
# # #             className={`px-4 py-2 rounded-lg font-medium transition-all ${
# # #               autoRefresh 
# # #                 ? 'bg-green-600 text-white' 
# # #                 : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
# # #             }`}
# # #           >
# # #             {autoRefresh ? '🔄 Auto-Refresh ON' : '⏸ Auto-Refresh OFF'}
# # #           </button>
# # #           <select
# # #             value={selectedJunction}
# # #             onChange={(e) => setSelectedJunction(e.target.value)}
# # #             className="px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600"
# # #           >
# # #             <option value="All">All Junctions</option>
# # #             {dashboardData.junctions.map(j => (
# # #               <option key={j} value={j}>{j}</option>
# # #             ))}
# # #           </select>
# # #         </div>
# # #       </div>

# # #       {/* Live Metrics */}
# # #       <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
# # #         <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-6 shadow-2xl">
# # #           <div className="flex items-center justify-between mb-2">
# # #             <Activity className="text-blue-200" size={32} />
# # #             <div className="text-blue-200 text-sm">Live</div>
# # #           </div>
# # #           <div className="text-4xl font-bold text-white mb-1">
# # #             {dashboardData.liveMetrics.totalVehicles}
# # #           </div>
# # #           <div className="text-blue-200 text-sm">Total Vehicles</div>
# # #         </div>

# # #         <div className="bg-gradient-to-br from-green-600 to-green-700 rounded-xl p-6 shadow-2xl">
# # #           <div className="flex items-center justify-between mb-2">
# # #             <TrendingUp className="text-green-200" size={32} />
# # #             <div className="text-green-200 text-sm">Avg</div>
# # #           </div>
# # #           <div className="text-4xl font-bold text-white mb-1">
# # #             {dashboardData.liveMetrics.avgSpeed} <span className="text-2xl">km/h</span>
# # #           </div>
# # #           <div className="text-green-200 text-sm">Average Speed</div>
# # #         </div>

# # #         <div className="bg-gradient-to-br from-red-600 to-red-700 rounded-xl p-6 shadow-2xl">
# # #           <div className="flex items-center justify-between mb-2">
# # #             <AlertTriangle className="text-red-200" size={32} />
# # #             <div className="text-red-200 text-sm animate-pulse">Alert</div>
# # #           </div>
# # #           <div className="text-4xl font-bold text-white mb-1">
# # #             {dashboardData.liveMetrics.activeAlerts}
# # #           </div>
# # #           <div className="text-red-200 text-sm">Active Alerts</div>
# # #         </div>

# # #         <div className="bg-gradient-to-br from-purple-600 to-purple-700 rounded-xl p-6 shadow-2xl">
# # #           <div className="flex items-center justify-between mb-2">
# # #             <Clock className="text-purple-200" size={32} />
# # #             <div className="text-purple-200 text-sm">Index</div>
# # #           </div>
# # #           <div className="text-4xl font-bold text-white mb-1">
# # #             {dashboardData.liveMetrics.congestionIndex}
# # #           </div>
# # #           <div className="text-purple-200 text-sm">Congestion Index</div>
# # #         </div>
# # #       </div>

# # #       {/* Main Charts */}
# # #       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
# # #         {/* Hourly Traffic Volume */}
# # #         <div className="bg-slate-800 rounded-xl p-6 shadow-2xl border border-slate-700">
# # #           <h3 className="text-xl font-bold text-white mb-4">📊 Traffic Volume by Hour</h3>
# # #           <ResponsiveContainer width="100%" height={300}>
# # #             <AreaChart data={dashboardData.hourlyTraffic}>
# # #               <defs>
# # #                 <linearGradient id="colorVehicles" x1="0" y1="0" x2="0" y2="1">
# # #                   <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
# # #                   <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1}/>
# # #                 </linearGradient>
# # #               </defs>
# # #               <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
# # #               <XAxis dataKey="hour" stroke="#94a3b8" tick={{fontSize: 12}} />
# # #               <YAxis stroke="#94a3b8" />
# # #               <Tooltip 
# # #                 contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '8px' }}
# # #                 labelStyle={{ color: '#f1f5f9' }}
# # #               />
# # #               <Area type="monotone" dataKey="vehicles" stroke="#3b82f6" fillOpacity={1} fill="url(#colorVehicles)" />
# # #             </AreaChart>
# # #           </ResponsiveContainer>
# # #         </div>

# # #         {/* Congestion Index Trend */}
# # #         <div className="bg-slate-800 rounded-xl p-6 shadow-2xl border border-slate-700">
# # #           <h3 className="text-xl font-bold text-white mb-4">🔥 Congestion Index Trend</h3>
# # #           <ResponsiveContainer width="100%" height={300}>
# # #             <LineChart data={dashboardData.hourlyTraffic}>
# # #               <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
# # #               <XAxis dataKey="hour" stroke="#94a3b8" tick={{fontSize: 12}} />
# # #               <YAxis stroke="#94a3b8" />
# # #               <Tooltip 
# # #                 contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '8px' }}
# # #                 labelStyle={{ color: '#f1f5f9' }}
# # #               />
# # #               <Line type="monotone" dataKey="congestion" stroke="#ef4444" strokeWidth={3} dot={{ fill: '#ef4444', r: 4 }} />
# # #             </LineChart>
# # #           </ResponsiveContainer>
# # #         </div>
# # #       </div>

# # #       {/* Junction Analysis and Traffic Distribution */}
# # #       <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
# # #         {/* Junction Comparison */}
# # #         <div className="lg:col-span-2 bg-slate-800 rounded-xl p-6 shadow-2xl border border-slate-700">
# # #           <h3 className="text-xl font-bold text-white mb-4">🚨 Critical Alerts by Junction</h3>
# # #           <ResponsiveContainer width="100%" height={300}>
# # #             <BarChart data={dashboardData.junctionData}>
# # #               <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
# # #               <XAxis dataKey="name" stroke="#94a3b8" />
# # #               <YAxis stroke="#94a3b8" />
# # #               <Tooltip 
# # #                 contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569', borderRadius: '8px' }}
# # #                 labelStyle={{ color: '#f1f5f9' }}
# # #               />
# # #               <Bar dataKey="alerts" radius={[8, 8, 0, 0]}>
# # #                 {dashboardData.junctionData.map((entry, index) => (
# # #                   <Cell key={`cell-${index}`} fill={entry.color} />
# # #                 ))}
# # #               </Bar>
# # #             </BarChart>
# # #           </ResponsiveContainer>
# # #         </div>

# # #         {/* Traffic Distribution */}
# # #         <div className="bg-slate-800 rounded-xl p-6 shadow-2xl border border-slate-700">
# # #           <h3 className="text-xl font-bold text-white mb-4">⏰ Traffic Distribution</h3>
# # #           <ResponsiveContainer width="100%" height={300}>
# # #             <PieChart>
# # #               <Pie
# # #                 data={dashboardData.trafficDistribution}
# # #                 cx="50%"
# # #                 cy="50%"
# # #                 labelLine={false}
# # #                 label={(entry) => `${entry.value}%`}
# # #                 outerRadius={100}
# # #                 fill="#8884d8"
# # #                 dataKey="value"
# # #               >
# # #                 {dashboardData.trafficDistribution.map((entry, index) => (
# # #                   <Cell key={`cell-${index}`} fill={entry.color} />
# # #                 ))}
# # #               </Pie>
# # #               <Tooltip />
# # #             </PieChart>
# # #           </ResponsiveContainer>
# # #           <div className="mt-4 space-y-2">
# # #             {dashboardData.trafficDistribution.map((item, idx) => (
# # #               <div key={idx} className="flex items-center justify-between text-sm">
# # #                 <div className="flex items-center gap-2">
# # #                   <div className="w-3 h-3 rounded" style={{backgroundColor: item.color}}></div>
# # #                   <span className="text-slate-300">{item.period}</span>
# # #                 </div>
# # #                 <span className="text-white font-medium">{item.value}%</span>
# # #               </div>
# # #             ))}
# # #           </div>
# # #         </div>
# # #       </div>

# # #       {/* Junction Details & Alerts */}
# # #       <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
# # #         {/* Junction Details */}
# # #         <div className="bg-slate-800 rounded-xl p-6 shadow-2xl border border-slate-700">
# # #           <h3 className="text-xl font-bold text-white mb-4">📍 Junction Intervention Requirements</h3>
# # #           <div className="space-y-4">
# # #             {dashboardData.junctionData.map((junction, idx) => {
# # #               const intervention = getInterventionLevel(junction.avgCongestion);
# # #               return (
# # #                 <div key={idx} className={`${intervention.bg} rounded-lg p-4 border-l-4`} style={{borderLeftColor: junction.color}}>
# # #                   <div className="flex items-center justify-between mb-2">
# # #                     <div className="flex items-center gap-2">
# # #                       <MapPin size={20} className={intervention.color} />
# # #                       <span className="font-bold text-slate-900">{junction.name}</span>
# # #                     </div>
# # #                     <span className="text-sm text-slate-700">Peak: {junction.peakHour}</span>
# # #                   </div>
# # #                   <div className="grid grid-cols-2 gap-4 mb-2">
# # #                     <div>
# # #                       <div className="text-xs text-slate-600">Alerts Today</div>
# # #                       <div className="text-lg font-bold text-slate-900">{junction.alerts}</div>
# # #                     </div>
# # #                     <div>
# # #                       <div className="text-xs text-slate-600">Avg Congestion</div>
# # #                       <div className="text-lg font-bold text-slate-900">{junction.avgCongestion}</div>
# # #                     </div>
# # #                   </div>
# # #                   <div className={`text-sm font-semibold ${intervention.color}`}>
# # #                     {intervention.text}
# # #                   </div>
# # #                 </div>
# # #               );
# # #             })}
# # #           </div>
# # #         </div>

# # #         {/* Recent Critical Alerts */}
# # #         <div className="bg-slate-800 rounded-xl p-6 shadow-2xl border border-slate-700">
# # #           <h3 className="text-xl font-bold text-white mb-4">⚠️ Recent Critical Alerts</h3>
# # #           <div className="space-y-3">
# # #             {dashboardData.recentAlerts.map((alert) => (
# # #               <div key={alert.id} className={`border-l-4 rounded-lg p-4 ${getSeverityColor(alert.severity)}`}>
# # #                 <div className="flex items-center justify-between mb-2">
# # #                   <div className="flex items-center gap-2">
# # #                     <AlertTriangle size={18} />
# # #                     <span className="font-bold">{alert.junction}</span>
# # #                   </div>
# # #                   <span className="text-sm font-mono">{alert.time}</span>
# # #                 </div>
# # #                 <div className="grid grid-cols-2 gap-2 text-sm">
# # #                   <div>
# # #                     <span className="opacity-75">Speed:</span>
# # #                     <span className="font-bold ml-2">{alert.speed} km/h</span>
# # #                   </div>
# # #                   <div>
# # #                     <span className="opacity-75">Vehicles:</span>
# # #                     <span className="font-bold ml-2">{alert.vehicles}</span>
# # #                   </div>
# # #                 </div>
# # #               </div>
# # #             ))}
# # #           </div>
          
# # #           <div className="mt-6 p-4 bg-slate-700 rounded-lg">
# # #             <div className="text-sm text-slate-300 mb-2">System Status</div>
# # #             <div className="flex items-center gap-2">
# # #               <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
# # #               <span className="text-white text-sm">All systems operational</span>
# # #             </div>
# # #             <div className="text-xs text-slate-400 mt-2">
# # #               Last updated: {currentTime.toLocaleTimeString()}
# # #             </div>
# # #           </div>
# # #         </div>
# # #       </div>
# # #     </div>
# # #   );
# # # };

# # # export default TrafficDashboard;

# # # import streamlit as st
# # # import pandas as pd
# # # import psycopg2
# # # from psycopg2.extras import RealDictCursor
# # # import plotly.express as px
# # # import plotly.graph_objects as go
# # # from datetime import datetime, timedelta
# # # import time

# # # # Page configuration
# # # st.set_page_config(
# # #     page_title="Smart City Traffic Dashboard",
# # #     layout="wide",
# # #     page_icon="🚦",
# # #     initial_sidebar_state="expanded"
# # # )

# # # # Custom CSS for styling
# # # st.markdown("""
# # # <style>
# # #     .main-header {
# # #         font-size: 3rem;
# # #         font-weight: bold;
# # #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# # #         -webkit-background-clip: text;
# # #         -webkit-text-fill-color: transparent;
# # #         text-align: center;
# # #         padding: 1rem 0;
# # #     }
# # #     .metric-container {
# # #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# # #         padding: 1.5rem;
# # #         border-radius: 10px;
# # #         color: white;
# # #         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
# # #     }
# # #     .alert-critical {
# # #         background-color: #fee2e2;
# # #         border-left: 4px solid #ef4444;
# # #         padding: 1rem;
# # #         border-radius: 5px;
# # #         margin: 0.5rem 0;
# # #     }
# # #     .alert-high {
# # #         background-color: #fef3c7;
# # #         border-left: 4px solid #f59e0b;
# # #         padding: 1rem;
# # #         border-radius: 5px;
# # #         margin: 0.5rem 0;
# # #     }
# # #     .stButton>button {
# # #         width: 100%;
# # #     }
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # Database connection with caching
# # # @st.cache_resource
# # # def get_db_connection():
# # #     """Create PostgreSQL connection"""
# # #     try:
# # #         conn = psycopg2.connect(
# # #             host='postgres',  # Use 'localhost' if running dashboard locally
# # #             database='traffic_db',
# # #             user='postgres',
# # #             password='postgres',
# # #             port=5432
# # #         )
# # #         return conn
# # #     except Exception as e:
# # #         st.error(f"Database connection failed: {str(e)}")
# # #         st.info("💡 Tip: If running locally, change host to 'localhost' in app.py")
# # #         return None

# # # # Fetch functions
# # # def fetch_live_metrics():
# # #     """Fetch latest traffic metrics"""
# # #     conn = get_db_connection()
# # #     if not conn:
# # #         return None
    
# # #     try:
# # #         query = """
# # #             SELECT 
# # #                 COUNT(*) as total_records,
# # #                 AVG(avg_vehicle_count)::int as avg_vehicles,
# # #                 AVG(avg_speed)::int as avg_speed,
# # #                 AVG(congestion_index)::numeric(5,1) as avg_congestion
# # #             FROM traffic_history
# # #             WHERE window_start >= CURRENT_DATE

# # #         """
# # #         df = pd.read_sql(query, conn)
        
# # #         # Get active alerts count
# # #         alert_query = """
# # #             SELECT COUNT(*) as alert_count
# # #             FROM critical_traffic_alerts
# # #             WHERE window_start >= CURRENT_DATE
# # #         """
# # #         alerts_df = pd.read_sql(alert_query, conn)
        
# # #         return {
# # #             'total_vehicles': df['avg_vehicles'].iloc[0] if not df.empty else 0,
# # #             'avg_speed': df['avg_speed'].iloc[0] if not df.empty else 0,
# # #             'active_alerts': alerts_df['alert_count'].iloc[0] if not alerts_df.empty else 0,
# # #             'congestion_index': df['avg_congestion'].iloc[0] if not df.empty else 0
# # #         }
# # #     except Exception as e:
# # #         st.error(f"Error fetching metrics: {str(e)}")
# # #         return None
# # #     finally:
# # #         conn.close()

# # # def fetch_hourly_traffic():
# # #     """Fetch hourly aggregated traffic data"""
# # #     conn = get_db_connection()
# # #     if not conn:
# # #         return pd.DataFrame()
    
# # #     try:
# # #         query = """
# # #             SELECT 
# # #                 EXTRACT(HOUR FROM window_start)::int as hour,
# # #                 AVG(avg_vehicle_count)::int as avg_vehicles,
# # #                 AVG(avg_speed)::int as avg_speed,
# # #                 AVG(congestion_index)::numeric(5,2) as avg_congestion
# # #             FROM traffic_history
# # #             WHERE window_start >= CURRENT_DATE
# # #             GROUP BY EXTRACT(HOUR FROM window_start)
# # #             ORDER BY hour
# # #         """
# # #         df = pd.read_sql(query, conn)
# # #         return df
# # #     except Exception as e:
# # #         st.error(f"Error fetching hourly data: {str(e)}")
# # #         return pd.DataFrame()
# # #     finally:
# # #         conn.close()

# # # def fetch_junction_data():
# # #     """Fetch junction-wise statistics"""
# # #     conn = get_db_connection()
# # #     if not conn:
# # #         return pd.DataFrame()
    
# # #     try:
# # #         query = """
# # #             SELECT 
# # #                 sensor_id,
# # #                 COUNT(*) as total_records,
# # #                 AVG(congestion_index)::numeric(5,2) as avg_congestion,
# # #                 MAX(congestion_index)::numeric(5,2) as max_congestion,
# # #                 AVG(avg_vehicle_count)::int as avg_vehicles
# # #             FROM traffic_history
# # #             WHERE window_start >= CURRENT_DATE
# # #             GROUP BY sensor_id
# # #             ORDER BY avg_congestion DESC
# # #         """
# # #         df = pd.read_sql(query, conn)
        
# # #         # Get alerts per junction
# # #         alert_query = """
# # #             SELECT 
# # #                 sensor_id,
# # #                 COUNT(*) as alert_count
# # #             FROM critical_traffic_alerts
# # #             WHERE window_start >= CURRENT_DATE
# # #             GROUP BY sensor_id
# # #         """
# # #         alerts_df = pd.read_sql(alert_query, conn)
        
# # #         # Merge dataframes
# # #         if not alerts_df.empty:
# # #             df = df.merge(alerts_df, on='sensor_id', how='left')
# # #             df['alert_count'] = df['alert_count'].fillna(0).astype(int)
# # #         else:
# # #             df['alert_count'] = 0
            
# # #         return df
# # #     except Exception as e:
# # #         st.error(f"Error fetching junction data: {str(e)}")
# # #         return pd.DataFrame()
# # #     finally:
# # #         conn.close()

# # # def fetch_recent_alerts(limit=10):
# # #     """Fetch recent critical alerts"""
# # #     conn = get_db_connection()
# # #     if not conn:
# # #         return pd.DataFrame()
    
# # #     try:
# # #         query = f"""
# # #             SELECT 
# # #                 sensor_id,
# # #                 window_start,
# # #                 avg_speed::numeric(5,1) as avg_speed,
# # #                 avg_vehicle_count::int as vehicle_count,
# # #                 congestion_index::numeric(5,2) as congestion_index
# # #             FROM critical_traffic_alerts
# # #             ORDER BY window_start DESC
# # #             LIMIT {limit}
# # #         """
# # #         df = pd.read_sql(query, conn)
# # #         return df
# # #     except Exception as e:
# # #         st.error(f"Error fetching alerts: {str(e)}")
# # #         return pd.DataFrame()
# # #     finally:
# # #         conn.close()

# # # # Main app
# # # def main():
# # #     # Header
# # #     st.markdown('<h1 class="main-header">🚦 Smart City Traffic Control Center</h1>', unsafe_allow_html=True)
# # #     st.markdown("<p style='text-align: center; color: #666; font-size: 1.2rem;'>Real-time Traffic Monitoring & Analytics Dashboard</p>", unsafe_allow_html=True)
    
# # #     # Sidebar
# # #     with st.sidebar:
# # #         st.header("⚙️ Dashboard Controls")
# # #         auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=True)
        
# # #         st.divider()
# # #         st.header("📊 Filters")
# # #         selected_junction = st.selectbox(
# # #             "Select Junction",
# # #             ["All", "Junction_A", "Junction_B", "Junction_C", "Junction_D"]
# # #         )
        
# # #         st.divider()
# # #         st.header("ℹ️ System Status")
# # #         st.success("✅ All systems operational")
# # #         st.info(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")
        
# # #         if st.button("🔄 Refresh Data"):
# # #             st.rerun()
    
# # #     # Auto-refresh logic
# # #     if auto_refresh:
# # #         time.sleep(5)
# # #         st.rerun()
    
# # #     # Fetch data
# # #     metrics = fetch_live_metrics()
    
# # #     if metrics:
# # #         # Live Metrics (Top Row)
# # #         st.subheader("📈 Live Metrics (Last Hour)")
# # #         col1, col2, col3, col4 = st.columns(4)
        
# # #         with col1:
# # #             st.metric(
# # #                 label="🚗 Total Vehicles",
# # #                 value=f"{metrics['total_vehicles']:,}",
# # #                 delta="Live"
# # #             )
        
# # #         with col2:
# # #             st.metric(
# # #                 label="⚡ Avg Speed",
# # #                 value=f"{metrics['avg_speed']} km/h",
# # #                 delta=f"{metrics['avg_speed'] - 30} km/h" if metrics['avg_speed'] else "0 km/h"
# # #             )
        
# # #         with col3:
# # #             st.metric(
# # #                 label="⚠️ Active Alerts",
# # #                 value=f"{metrics['active_alerts']}",
# # #                 delta="Critical" if metrics['active_alerts'] > 0 else "None"
# # #             )
        
# # #         with col4:
# # #             st.metric(
# # #                 label="📊 Congestion Index",
# # #                 value=f"{metrics['congestion_index']:.1f}",
# # #                 delta=f"{metrics['congestion_index'] - 25:.1f}"
# # #             )
    
# # #     st.divider()
    
# # #     # Hourly Traffic Analysis
# # #     st.subheader("📊 Hourly Traffic Analysis")
# # #     df_hourly = fetch_hourly_traffic()
    
# # #     if not df_hourly.empty:
# # #         col1, col2 = st.columns(2)
        
# # #         with col1:
# # #             # Traffic Volume Chart
# # #             fig_volume = px.area(
# # #                 df_hourly,
# # #                 x='hour',
# # #                 y='avg_vehicles',
# # #                 title='Traffic Volume by Hour',
# # #                 labels={'hour': 'Hour of Day', 'avg_vehicles': 'Average Vehicles'},
# # #                 color_discrete_sequence=['#667eea']
# # #             )
# # #             fig_volume.update_layout(
# # #                 xaxis=dict(tickmode='linear', tick0=0, dtick=2),
# # #                 height=400
# # #             )
# # #             st.plotly_chart(fig_volume, use_container_width=True)
        
# # #         with col2:
# # #             # Congestion Trend Chart
# # #             fig_congestion = px.line(
# # #                 df_hourly,
# # #                 x='hour',
# # #                 y='avg_congestion',
# # #                 title='Congestion Index Trend',
# # #                 labels={'hour': 'Hour of Day', 'avg_congestion': 'Congestion Index'},
# # #                 color_discrete_sequence=['#ef4444']
# # #             )
# # #             fig_congestion.update_traces(mode='lines+markers', line=dict(width=3))
# # #             fig_congestion.update_layout(
# # #                 xaxis=dict(tickmode='linear', tick0=0, dtick=2),
# # #                 height=400
# # #             )
# # #             st.plotly_chart(fig_congestion, use_container_width=True)
# # #     else:
# # #         st.info("⏳ Waiting for hourly data... The system needs to collect data for at least one hour.")
    
# # #     st.divider()
    
# # #     # Junction Analysis
# # #     st.subheader("🚨 Junction Analysis & Intervention Requirements")
# # #     df_junctions = fetch_junction_data()
    
# # #     if not df_junctions.empty:
# # #         col1, col2 = st.columns([2, 1])
        
# # #         with col1:
# # #             # Junction comparison chart
# # #             fig_junctions = go.Figure()
            
# # #             fig_junctions.add_trace(go.Bar(
# # #                 name='Avg Congestion',
# # #                 x=df_junctions['sensor_id'],
# # #                 y=df_junctions['avg_congestion'],
# # #                 marker_color='#f59e0b'
# # #             ))
            
# # #             fig_junctions.add_trace(go.Bar(
# # #                 name='Critical Alerts',
# # #                 x=df_junctions['sensor_id'],
# # #                 y=df_junctions['alert_count'],
# # #                 marker_color='#ef4444'
# # #             ))
            
# # #             fig_junctions.update_layout(
# # #                 title='Junction Comparison: Congestion & Alerts',
# # #                 barmode='group',
# # #                 height=400,
# # #                 xaxis_title='Junction',
# # #                 yaxis_title='Value'
# # #             )
            
# # #             st.plotly_chart(fig_junctions, use_container_width=True)
        
# # #         with col2:
# # #             st.markdown("#### 👮 Intervention Recommendations")
# # #             for _, row in df_junctions.iterrows():
# # #                 congestion = row['avg_congestion']
                
# # #                 if congestion > 50:
# # #                     intervention = "🚨 URGENT - Deploy 3+ Officers"
# # #                     color = "red"
# # #                 elif congestion > 30:
# # #                     intervention = "⚠️ HIGH - Deploy 2 Officers"
# # #                     color = "orange"
# # #                 elif congestion > 15:
# # #                     intervention = "⚡ MODERATE - Deploy 1 Officer"
# # #                     color = "blue"
# # #                 else:
# # #                     intervention = "✅ LOW - Monitor Remotely"
# # #                     color = "green"
                
# # #                 st.markdown(f"""
# # #                 <div style='background-color: #{color}22; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {color};'>
# # #                     <strong>{row['sensor_id']}</strong><br>
# # #                     Congestion: {congestion:.1f}<br>
# # #                     Alerts: {row['alert_count']}<br>
# # #                     <strong>{intervention}</strong>
# # #                 </div>
# # #                 """, unsafe_allow_html=True)
# # #     else:
# # #         st.info("⏳ Collecting junction data...")
    
# # #     st.divider()
    
# # #     # Recent Critical Alerts
# # #     st.subheader("⚠️ Recent Critical Alerts")
# # #     df_alerts = fetch_recent_alerts()
    
# # #     if not df_alerts.empty:
# # #         # Format the dataframe
# # #         df_alerts['window_start'] = pd.to_datetime(df_alerts['window_start']).dt.strftime('%Y-%m-%d %H:%M')
        
# # #         # Display as styled table
# # #         st.dataframe(
# # #             df_alerts,
# # #             column_config={
# # #                 "sensor_id": st.column_config.TextColumn("Junction", width="medium"),
# # #                 "window_start": st.column_config.TextColumn("Time", width="medium"),
# # #                 "avg_speed": st.column_config.NumberColumn("Speed (km/h)", format="%.1f"),
# # #                 "vehicle_count": st.column_config.NumberColumn("Vehicles", format="%d"),
# # #                 "congestion_index": st.column_config.NumberColumn("Congestion", format="%.2f"),
# # #             },
# # #             hide_index=True,
# # #             use_container_width=True
# # #         )
# # #     else:
# # #         st.success("✅ No critical alerts in the system!")
    
# # #     # Footer
# # #     st.divider()
# # #     st.markdown("""
# # #     <div style='text-align: center; color: #666; padding: 2rem 0;'>
# # #         <p>Smart City Traffic Management System | Powered by Apache Kafka, Spark & Airflow</p>
# # #         <p style='font-size: 0.9rem;'>Data refreshes automatically every 5 seconds</p>
# # #     </div>
# # #     """, unsafe_allow_html=True)

# # # if __name__ == "__main__":
# # #     main()

# # import streamlit as st
# # import pandas as pd
# # import psycopg2
# # from psycopg2.extras import RealDictCursor
# # import plotly.express as px
# # import plotly.graph_objects as go
# # from datetime import datetime, timedelta
# # import time

# # # Page configuration
# # st.set_page_config(
# #     page_title="Smart City Traffic Dashboard",
# #     layout="wide",
# #     page_icon="🚦",
# #     initial_sidebar_state="expanded"
# # )

# # # Custom CSS for styling
# # st.markdown("""
# # <style>
# #     .main-header {
# #         font-size: 3rem;
# #         font-weight: bold;
# #         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
# #         -webkit-background-clip: text;
# #         -webkit-text-fill-color: transparent;
# #         text-align: center;
# #         padding: 1rem 0;
# #     }
# #     .metric-container {
# #         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #         padding: 1.5rem;
# #         border-radius: 10px;
# #         color: white;
# #         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
# #     }
# #     .alert-critical {
# #         background-color: #fee2e2;
# #         border-left: 4px solid #ef4444;
# #         padding: 1rem;
# #         border-radius: 5px;
# #         margin: 0.5rem 0;
# #     }
# #     .alert-high {
# #         background-color: #fef3c7;
# #         border-left: 4px solid #f59e0b;
# #         padding: 1rem;
# #         border-radius: 5px;
# #         margin: 0.5rem 0;
# #     }
# #     .stButton>button {
# #         width: 100%;
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # # Database connection with caching
# # @st.cache_resource
# # def get_db_connection():
# #     """Create PostgreSQL connection"""
# #     try:
# #         conn = psycopg2.connect(
# #             host='postgres',
# #             database='traffic_db',
# #             user='postgres',
# #             password='postgres',
# #             port=5432
# #         )
# #         return conn
# #     except Exception as e:
# #         st.error(f"Database connection failed: {str(e)}")
# #         st.info("💡 Tip: If running locally, change host to 'localhost' in app.py")
# #         return None

# # # Fetch functions
# # def fetch_live_metrics():
# #     """Fetch latest traffic metrics - SHOWS ALL AVAILABLE DATA"""
# #     conn = get_db_connection()
# #     if not conn:
# #         return None
    
# #     try:
# #         # First check if ANY data exists
# #         count_query = "SELECT COUNT(*) as count FROM traffic_history"
# #         count_df = pd.read_sql(count_query, conn)
        
# #         if count_df['count'].iloc[0] == 0:
# #             st.warning("⏳ No data in database yet. Waiting for Spark to write first batch...")
# #             return None
        
# #         # Get metrics from ALL available data (no time filter)
# #         query = """
# #             SELECT 
# #                 COUNT(*) as total_records,
# #                 AVG(avg_vehicle_count)::int as avg_vehicles,
# #                 AVG(avg_speed)::int as avg_speed,
# #                 AVG(congestion_index)::numeric(5,1) as avg_congestion,
# #                 MAX(window_start) as latest_data
# #             FROM traffic_history
# #         """
# #         df = pd.read_sql(query, conn)
        
# #         # Get active alerts count (all data)
# #         alert_query = "SELECT COUNT(*) as alert_count FROM critical_traffic_alerts"
# #         alerts_df = pd.read_sql(alert_query, conn)
        
# #         # Show latest data timestamp
# #         latest = df['latest_data'].iloc[0] if not df.empty else None
# #         if latest:
# #             st.sidebar.info(f"📅 Latest data: {latest}")
        
# #         return {
# #             'total_vehicles': df['avg_vehicles'].iloc[0] if not df.empty else 0,
# #             'avg_speed': df['avg_speed'].iloc[0] if not df.empty else 0,
# #             'active_alerts': alerts_df['alert_count'].iloc[0] if not alerts_df.empty else 0,
# #             'congestion_index': df['avg_congestion'].iloc[0] if not df.empty else 0
# #         }
# #     except Exception as e:
# #         st.error(f"Error fetching metrics: {str(e)}")
# #         return None
# #     finally:
# #         conn.close()

# # def fetch_hourly_traffic():
# #     """Fetch hourly aggregated traffic data - ALL DATA"""
# #     conn = get_db_connection()
# #     if not conn:
# #         return pd.DataFrame()
    
# #     try:
# #         query = """
# #             SELECT 
# #                 EXTRACT(HOUR FROM window_start)::int as hour,
# #                 AVG(avg_vehicle_count)::int as avg_vehicles,
# #                 AVG(avg_speed)::int as avg_speed,
# #                 AVG(congestion_index)::numeric(5,2) as avg_congestion
# #             FROM traffic_history
# #             GROUP BY EXTRACT(HOUR FROM window_start)
# #             ORDER BY hour
# #         """
# #         df = pd.read_sql(query, conn)
# #         return df
# #     except Exception as e:
# #         st.error(f"Error fetching hourly data: {str(e)}")
# #         return pd.DataFrame()
# #     finally:
# #         conn.close()

# # def fetch_junction_data():
# #     """Fetch junction-wise statistics - ALL DATA"""
# #     conn = get_db_connection()
# #     if not conn:
# #         return pd.DataFrame()
    
# #     try:
# #         query = """
# #             SELECT 
# #                 sensor_id,
# #                 COUNT(*) as total_records,
# #                 AVG(congestion_index)::numeric(5,2) as avg_congestion,
# #                 MAX(congestion_index)::numeric(5,2) as max_congestion,
# #                 AVG(avg_vehicle_count)::int as avg_vehicles
# #             FROM traffic_history
# #             GROUP BY sensor_id
# #             ORDER BY avg_congestion DESC
# #         """
# #         df = pd.read_sql(query, conn)
        
# #         # Get alerts per junction
# #         alert_query = """
# #             SELECT 
# #                 sensor_id,
# #                 COUNT(*) as alert_count
# #             FROM critical_traffic_alerts
# #             GROUP BY sensor_id
# #         """
# #         alerts_df = pd.read_sql(alert_query, conn)
        
# #         # Merge dataframes
# #         if not alerts_df.empty:
# #             df = df.merge(alerts_df, on='sensor_id', how='left')
# #             df['alert_count'] = df['alert_count'].fillna(0).astype(int)
# #         else:
# #             df['alert_count'] = 0
            
# #         return df
# #     except Exception as e:
# #         st.error(f"Error fetching junction data: {str(e)}")
# #         return pd.DataFrame()
# #     finally:
# #         conn.close()

# # def fetch_recent_alerts(limit=10):
# #     """Fetch recent critical alerts"""
# #     conn = get_db_connection()
# #     if not conn:
# #         return pd.DataFrame()
    
# #     try:
# #         query = f"""
# #             SELECT 
# #                 sensor_id,
# #                 window_start,
# #                 avg_speed::numeric(5,1) as avg_speed,
# #                 avg_vehicle_count::int as vehicle_count,
# #                 congestion_index::numeric(5,2) as congestion_index
# #             FROM critical_traffic_alerts
# #             ORDER BY window_start DESC
# #             LIMIT {limit}
# #         """
# #         df = pd.read_sql(query, conn)
# #         return df
# #     except Exception as e:
# #         st.error(f"Error fetching alerts: {str(e)}")
# #         return pd.DataFrame()
# #     finally:
# #         conn.close()

# # def get_data_stats():
# #     """Get database statistics"""
# #     conn = get_db_connection()
# #     if not conn:
# #         return None
    
# #     try:
# #         query = """
# #             SELECT 
# #                 COUNT(*) as total_records,
# #                 MIN(window_start) as earliest,
# #                 MAX(window_start) as latest
# #             FROM traffic_history
# #         """
# #         df = pd.read_sql(query, conn)
# #         return df.iloc[0] if not df.empty else None
# #     except:
# #         return None
# #     finally:
# #         conn.close()

# # # Main app
# # def main():
# #     # Header
# #     st.markdown('<h1 class="main-header">🚦 Smart City Traffic Control Center</h1>', unsafe_allow_html=True)
# #     st.markdown("<p style='text-align: center; color: #666; font-size: 1.2rem;'>Real-time Traffic Monitoring & Analytics Dashboard</p>", unsafe_allow_html=True)
    
# #     # Sidebar
# #     with st.sidebar:
# #         st.header("⚙️ Dashboard Controls")
# #         auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=True)
        
# #         st.divider()
        
# #         # Show data statistics
# #         stats = get_data_stats()
# #         if stats is not None and stats['total_records'] > 0:
# #             st.success(f"✅ Database: {stats['total_records']} records")
# #             st.caption(f"From: {stats['earliest']}")
# #             st.caption(f"To: {stats['latest']}")
# #         else:
# #             st.warning("⏳ Waiting for data...")
        
# #         st.divider()
# #         st.header("📊 Filters")
# #         selected_junction = st.selectbox(
# #             "Select Junction",
# #             ["All", "Junction_A", "Junction_B", "Junction_C", "Junction_D"]
# #         )
        
# #         st.divider()
# #         st.header("ℹ️ System Status")
# #         st.success("✅ All systems operational")
# #         st.info(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")
        
# #         if st.button("🔄 Refresh Data"):
# #             st.cache_resource.clear()
# #             st.rerun()
    
# #     # Auto-refresh logic
# #     if auto_refresh:
# #         time.sleep(5)
# #         st.rerun()
    
# #     # Fetch data
# #     metrics = fetch_live_metrics()
    
# #     if metrics:
# #         # Live Metrics (Top Row)
# #         st.subheader("📈 Traffic Metrics (All Available Data)")
# #         col1, col2, col3, col4 = st.columns(4)
        
# #         with col1:
# #             st.metric(
# #                 label="🚗 Avg Vehicles",
# #                 value=f"{metrics['total_vehicles']:,}",
# #                 delta="Live"
# #             )
        
# #         with col2:
# #             st.metric(
# #                 label="⚡ Avg Speed",
# #                 value=f"{metrics['avg_speed']} km/h",
# #                 delta=f"{metrics['avg_speed'] - 30} km/h" if metrics['avg_speed'] else "0 km/h"
# #             )
        
# #         with col3:
# #             st.metric(
# #                 label="⚠️ Total Alerts",
# #                 value=f"{metrics['active_alerts']}",
# #                 delta="Critical" if metrics['active_alerts'] > 0 else "None"
# #             )
        
# #         with col4:
# #             st.metric(
# #                 label="📊 Congestion Index",
# #                 value=f"{metrics['congestion_index']:.1f}",
# #                 delta=f"{metrics['congestion_index'] - 25:.1f}"
# #             )
# #     else:
# #         st.info("⏳ Waiting for data... Spark processes data in 2-minute windows. Please wait 2-3 minutes after starting the system.")
    
# #     st.divider()
    
# #     # Hourly Traffic Analysis
# #     st.subheader("📊 Hourly Traffic Analysis")
# #     df_hourly = fetch_hourly_traffic()
    
# #     if not df_hourly.empty:
# #         col1, col2 = st.columns(2)
        
# #         with col1:
# #             # Traffic Volume Chart
# #             fig_volume = px.area(
# #                 df_hourly,
# #                 x='hour',
# #                 y='avg_vehicles',
# #                 title='Traffic Volume by Hour',
# #                 labels={'hour': 'Hour of Day', 'avg_vehicles': 'Average Vehicles'},
# #                 color_discrete_sequence=['#667eea']
# #             )
# #             fig_volume.update_layout(
# #                 xaxis=dict(tickmode='linear', tick0=0, dtick=2),
# #                 height=400
# #             )
# #             st.plotly_chart(fig_volume, use_container_width=True)
        
# #         with col2:
# #             # Congestion Trend Chart
# #             fig_congestion = px.line(
# #                 df_hourly,
# #                 x='hour',
# #                 y='avg_congestion',
# #                 title='Congestion Index Trend',
# #                 labels={'hour': 'Hour of Day', 'avg_congestion': 'Congestion Index'},
# #                 color_discrete_sequence=['#ef4444']
# #             )
# #             fig_congestion.update_traces(mode='lines+markers', line=dict(width=3))
# #             fig_congestion.update_layout(
# #                 xaxis=dict(tickmode='linear', tick0=0, dtick=2),
# #                 height=400
# #             )
# #             st.plotly_chart(fig_congestion, use_container_width=True)
# #     else:
# #         st.info("⏳ Waiting for hourly data... The system needs to collect data across multiple hours.")
    
# #     st.divider()
    
# #     # Junction Analysis
# #     st.subheader("🚨 Junction Analysis & Intervention Requirements")
# #     df_junctions = fetch_junction_data()
    
# #     if not df_junctions.empty:
# #         col1, col2 = st.columns([2, 1])
        
# #         with col1:
# #             # Junction comparison chart
# #             fig_junctions = go.Figure()
            
# #             fig_junctions.add_trace(go.Bar(
# #                 name='Avg Congestion',
# #                 x=df_junctions['sensor_id'],
# #                 y=df_junctions['avg_congestion'],
# #                 marker_color='#f59e0b'
# #             ))
            
# #             fig_junctions.add_trace(go.Bar(
# #                 name='Critical Alerts',
# #                 x=df_junctions['sensor_id'],
# #                 y=df_junctions['alert_count'],
# #                 marker_color='#ef4444'
# #             ))
            
# #             fig_junctions.update_layout(
# #                 title='Junction Comparison: Congestion & Alerts',
# #                 barmode='group',
# #                 height=400,
# #                 xaxis_title='Junction',
# #                 yaxis_title='Value'
# #             )
            
# #             st.plotly_chart(fig_junctions, use_container_width=True)
        
# #         with col2:
# #             st.markdown("#### 👮 Intervention Recommendations")
# #             for _, row in df_junctions.iterrows():
# #                 congestion = row['avg_congestion']
                
# #                 if congestion > 50:
# #                     intervention = "🚨 URGENT - Deploy 3+ Officers"
# #                     color = "red"
# #                 elif congestion > 30:
# #                     intervention = "⚠️ HIGH - Deploy 2 Officers"
# #                     color = "orange"
# #                 elif congestion > 15:
# #                     intervention = "⚡ MODERATE - Deploy 1 Officer"
# #                     color = "blue"
# #                 else:
# #                     intervention = "✅ LOW - Monitor Remotely"
# #                     color = "green"
                
# #                 st.markdown(f"""
# #                 <div style='background-color: #{color}22; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {color};'>
# #                     <strong>{row['sensor_id']}</strong><br>
# #                     Congestion: {congestion:.1f}<br>
# #                     Alerts: {row['alert_count']}<br>
# #                     <strong>{intervention}</strong>
# #                 </div>
# #                 """, unsafe_allow_html=True)
# #     else:
# #         st.info("⏳ Collecting junction data...")
    
# #     st.divider()
    
# #     # Recent Critical Alerts
# #     st.subheader("⚠️ Recent Critical Alerts")
# #     df_alerts = fetch_recent_alerts()
    
# #     if not df_alerts.empty:
# #         # Format the dataframe
# #         df_alerts['window_start'] = pd.to_datetime(df_alerts['window_start']).dt.strftime('%Y-%m-%d %H:%M')
        
# #         # Display as styled table
# #         st.dataframe(
# #             df_alerts,
# #             column_config={
# #                 "sensor_id": st.column_config.TextColumn("Junction", width="medium"),
# #                 "window_start": st.column_config.TextColumn("Time", width="medium"),
# #                 "avg_speed": st.column_config.NumberColumn("Speed (km/h)", format="%.1f"),
# #                 "vehicle_count": st.column_config.NumberColumn("Vehicles", format="%d"),
# #                 "congestion_index": st.column_config.NumberColumn("Congestion", format="%.2f"),
# #             },
# #             hide_index=True,
# #             use_container_width=True
# #         )
# #     else:
# #         st.success("✅ No critical alerts in the system!")
    
# #     # Footer
# #     st.divider()
# #     st.markdown("""
# #     <div style='text-align: center; color: #666; padding: 2rem 0;'>
# #         <p>Smart City Traffic Management System | Powered by Apache Kafka, Spark & Airflow</p>
# #         <p style='font-size: 0.9rem;'>Data refreshes automatically every 5 seconds</p>
# #     </div>
# #     """, unsafe_allow_html=True)

# # if __name__ == "__main__":
# #     main()

# import streamlit as st
# import pandas as pd
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# import time

# # Page configuration
# st.set_page_config(
#     page_title="Smart City Traffic Dashboard",
#     layout="wide",
#     page_icon="🚦",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         font-weight: bold;
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         text-align: center;
#         padding: 1rem 0;
#     }
#     .metric-container {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 1.5rem;
#         border-radius: 10px;
#         color: white;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }
#     .alert-critical {
#         background-color: #fee2e2;
#         border-left: 4px solid #ef4444;
#         padding: 1rem;
#         border-radius: 5px;
#         margin: 0.5rem 0;
#     }
#     .alert-high {
#         background-color: #fef3c7;
#         border-left: 4px solid #f59e0b;
#         padding: 1rem;
#         border-radius: 5px;
#         margin: 0.5rem 0;
#     }
#     .stButton>button {
#         width: 100%;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Database connection - NO CACHING to avoid "connection closed" errors
# def get_db_connection():
#     """Create PostgreSQL connection - creates fresh connection each time"""
#     try:
#         conn = psycopg2.connect(
#             host='postgres',
#             database='traffic_db',
#             user='postgres',
#             password='postgres',
#             port=5432
#         )
#         return conn
#     except Exception as e:
#         st.error(f"Database connection failed: {str(e)}")
#         st.info("💡 Tip: If running locally, change host to 'localhost' in app.py")
#         return None

# # Fetch functions
# def fetch_live_metrics():
#     """Fetch latest traffic metrics - SHOWS ALL AVAILABLE DATA"""
#     conn = get_db_connection()
#     if not conn:
#         return None
    
#     try:
#         # First check if ANY data exists
#         count_query = "SELECT COUNT(*) as count FROM traffic_history"
#         count_df = pd.read_sql(count_query, conn)
        
#         if count_df['count'].iloc[0] == 0:
#             st.warning("⏳ No data in database yet. Waiting for Spark to write first batch...")
#             return None
        
#         # Get metrics from ALL available data (no time filter)
#         query = """
#             SELECT 
#                 COUNT(*) as total_records,
#                 AVG(avg_vehicle_count)::int as avg_vehicles,
#                 AVG(avg_speed)::int as avg_speed,
#                 AVG(congestion_index)::numeric(5,1) as avg_congestion,
#                 MAX(window_start) as latest_data
#             FROM traffic_history
#         """
#         df = pd.read_sql(query, conn)
        
#         # Get active alerts count (all data)
#         alert_query = "SELECT COUNT(*) as alert_count FROM critical_traffic_alerts"
#         alerts_df = pd.read_sql(alert_query, conn)
        
#         # Show latest data timestamp
#         latest = df['latest_data'].iloc[0] if not df.empty else None
#         if latest:
#             st.sidebar.info(f"📅 Latest data: {latest}")
        
#         return {
#             'total_vehicles': df['avg_vehicles'].iloc[0] if not df.empty else 0,
#             'avg_speed': df['avg_speed'].iloc[0] if not df.empty else 0,
#             'active_alerts': alerts_df['alert_count'].iloc[0] if not alerts_df.empty else 0,
#             'congestion_index': df['avg_congestion'].iloc[0] if not df.empty else 0
#         }
#     except Exception as e:
#         st.error(f"Error fetching metrics: {str(e)}")
#         return None
#     finally:
#         conn.close()

# def fetch_hourly_traffic():
#     """Fetch hourly aggregated traffic data - ALL DATA"""
#     conn = get_db_connection()
#     if not conn:
#         return pd.DataFrame()
    
#     try:
#         query = """
#             SELECT 
#                 EXTRACT(HOUR FROM window_start)::int as hour,
#                 AVG(avg_vehicle_count)::int as avg_vehicles,
#                 AVG(avg_speed)::int as avg_speed,
#                 AVG(congestion_index)::numeric(5,2) as avg_congestion
#             FROM traffic_history
#             GROUP BY EXTRACT(HOUR FROM window_start)
#             ORDER BY hour
#         """
#         df = pd.read_sql(query, conn)
#         return df
#     except Exception as e:
#         st.error(f"Error fetching hourly data: {str(e)}")
#         return pd.DataFrame()
#     finally:
#         conn.close()

# def fetch_junction_data():
#     """Fetch junction-wise statistics - ALL DATA"""
#     conn = get_db_connection()
#     if not conn:
#         return pd.DataFrame()
    
#     try:
#         query = """
#             SELECT 
#                 sensor_id,
#                 COUNT(*) as total_records,
#                 AVG(congestion_index)::numeric(5,2) as avg_congestion,
#                 MAX(congestion_index)::numeric(5,2) as max_congestion,
#                 AVG(avg_vehicle_count)::int as avg_vehicles
#             FROM traffic_history
#             GROUP BY sensor_id
#             ORDER BY avg_congestion DESC
#         """
#         df = pd.read_sql(query, conn)
        
#         # Get alerts per junction
#         alert_query = """
#             SELECT 
#                 sensor_id,
#                 COUNT(*) as alert_count
#             FROM critical_traffic_alerts
#             GROUP BY sensor_id
#         """
#         alerts_df = pd.read_sql(alert_query, conn)
        
#         # Merge dataframes
#         if not alerts_df.empty:
#             df = df.merge(alerts_df, on='sensor_id', how='left')
#             df['alert_count'] = df['alert_count'].fillna(0).astype(int)
#         else:
#             df['alert_count'] = 0
            
#         return df
#     except Exception as e:
#         st.error(f"Error fetching junction data: {str(e)}")
#         return pd.DataFrame()
#     finally:
#         conn.close()

# def fetch_recent_alerts(limit=10):
#     """Fetch recent critical alerts"""
#     conn = get_db_connection()
#     if not conn:
#         return pd.DataFrame()
    
#     try:
#         query = f"""
#             SELECT 
#                 sensor_id,
#                 window_start,
#                 avg_speed::numeric(5,1) as avg_speed,
#                 avg_vehicle_count::int as vehicle_count,
#                 congestion_index::numeric(5,2) as congestion_index
#             FROM critical_traffic_alerts
#             ORDER BY window_start DESC
#             LIMIT {limit}
#         """
#         df = pd.read_sql(query, conn)
#         return df
#     except Exception as e:
#         st.error(f"Error fetching alerts: {str(e)}")
#         return pd.DataFrame()
#     finally:
#         conn.close()

# def get_data_stats():
#     """Get database statistics"""
#     conn = get_db_connection()
#     if not conn:
#         return None
    
#     try:
#         query = """
#             SELECT 
#                 COUNT(*) as total_records,
#                 MIN(window_start) as earliest,
#                 MAX(window_start) as latest
#             FROM traffic_history
#         """
#         df = pd.read_sql(query, conn)
#         return df.iloc[0] if not df.empty else None
#     except:
#         return None
#     finally:
#         conn.close()

# # Main app
# def main():
#     # Header
#     st.markdown('<h1 class="main-header">🚦 Smart City Traffic Control Center</h1>', unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; color: #666; font-size: 1.2rem;'>Real-time Traffic Monitoring & Analytics Dashboard</p>", unsafe_allow_html=True)
    
#     # Sidebar
#     with st.sidebar:
#         st.header("⚙️ Dashboard Controls")
#         auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=True)
        
#         st.divider()
        
#         # Show data statistics
#         stats = get_data_stats()
#         if stats is not None and stats['total_records'] > 0:
#             st.success(f"✅ Database: {stats['total_records']} records")
#             st.caption(f"From: {stats['earliest']}")
#             st.caption(f"To: {stats['latest']}")
#         else:
#             st.warning("⏳ Waiting for data...")
        
#         st.divider()
#         st.header("📊 Filters")
#         selected_junction = st.selectbox(
#             "Select Junction",
#             ["All", "Junction_A", "Junction_B", "Junction_C", "Junction_D"]
#         )
        
#         st.divider()
#         st.header("ℹ️ System Status")
#         st.success("✅ All systems operational")
#         st.info(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")
        
#         if st.button("🔄 Refresh Data"):
#             st.cache_resource.clear()
#             st.rerun()
    
#     # Auto-refresh logic
#     if auto_refresh:
#         time.sleep(5)
#         st.rerun()
    
#     # Fetch data
#     metrics = fetch_live_metrics()
    
#     if metrics:
#         # Live Metrics (Top Row)
#         st.subheader("📈 Traffic Metrics (All Available Data)")
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.metric(
#                 label="🚗 Avg Vehicles",
#                 value=f"{metrics['total_vehicles']:,}",
#                 delta="Live"
#             )
        
#         with col2:
#             st.metric(
#                 label="⚡ Avg Speed",
#                 value=f"{metrics['avg_speed']} km/h",
#                 delta=f"{metrics['avg_speed'] - 30} km/h" if metrics['avg_speed'] else "0 km/h"
#             )
        
#         with col3:
#             st.metric(
#                 label="⚠️ Total Alerts",
#                 value=f"{metrics['active_alerts']}",
#                 delta="Critical" if metrics['active_alerts'] > 0 else "None"
#             )
        
#         with col4:
#             st.metric(
#                 label="📊 Congestion Index",
#                 value=f"{metrics['congestion_index']:.1f}",
#                 delta=f"{metrics['congestion_index'] - 25:.1f}"
#             )
#     else:
#         st.info("⏳ Waiting for data... Spark processes data in 2-minute windows. Please wait 2-3 minutes after starting the system.")
    
#     st.divider()
    
#     # Hourly Traffic Analysis
#     st.subheader("📊 Hourly Traffic Analysis")
#     df_hourly = fetch_hourly_traffic()
    
#     if not df_hourly.empty:
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Traffic Volume Chart
#             fig_volume = px.area(
#                 df_hourly,
#                 x='hour',
#                 y='avg_vehicles',
#                 title='Traffic Volume by Hour',
#                 labels={'hour': 'Hour of Day', 'avg_vehicles': 'Average Vehicles'},
#                 color_discrete_sequence=['#667eea']
#             )
#             fig_volume.update_layout(
#                 xaxis=dict(tickmode='linear', tick0=0, dtick=2),
#                 height=400
#             )
#             st.plotly_chart(fig_volume, use_container_width=True)
        
#         with col2:
#             # Congestion Trend Chart
#             fig_congestion = px.line(
#                 df_hourly,
#                 x='hour',
#                 y='avg_congestion',
#                 title='Congestion Index Trend',
#                 labels={'hour': 'Hour of Day', 'avg_congestion': 'Congestion Index'},
#                 color_discrete_sequence=['#ef4444']
#             )
#             fig_congestion.update_traces(mode='lines+markers', line=dict(width=3))
#             fig_congestion.update_layout(
#                 xaxis=dict(tickmode='linear', tick0=0, dtick=2),
#                 height=400
#             )
#             st.plotly_chart(fig_congestion, use_container_width=True)
#     else:
#         st.info("⏳ Waiting for hourly data... The system needs to collect data across multiple hours.")
    
#     st.divider()
    
#     # Junction Analysis
#     st.subheader("🚨 Junction Analysis & Intervention Requirements")
#     df_junctions = fetch_junction_data()
    
#     if not df_junctions.empty:
#         col1, col2 = st.columns([2, 1])
        
#         with col1:
#             # Junction comparison chart
#             fig_junctions = go.Figure()
            
#             fig_junctions.add_trace(go.Bar(
#                 name='Avg Congestion',
#                 x=df_junctions['sensor_id'],
#                 y=df_junctions['avg_congestion'],
#                 marker_color='#f59e0b'
#             ))
            
#             fig_junctions.add_trace(go.Bar(
#                 name='Critical Alerts',
#                 x=df_junctions['sensor_id'],
#                 y=df_junctions['alert_count'],
#                 marker_color='#ef4444'
#             ))
            
#             fig_junctions.update_layout(
#                 title='Junction Comparison: Congestion & Alerts',
#                 barmode='group',
#                 height=400,
#                 xaxis_title='Junction',
#                 yaxis_title='Value'
#             )
            
#             st.plotly_chart(fig_junctions, use_container_width=True)
        
#         with col2:
#             st.markdown("#### 👮 Intervention Recommendations")
#             for _, row in df_junctions.iterrows():
#                 congestion = row['avg_congestion']
                
#                 if congestion > 50:
#                     intervention = "🚨 URGENT - Deploy 3+ Officers"
#                     color = "red"
#                 elif congestion > 30:
#                     intervention = "⚠️ HIGH - Deploy 2 Officers"
#                     color = "orange"
#                 elif congestion > 15:
#                     intervention = "⚡ MODERATE - Deploy 1 Officer"
#                     color = "blue"
#                 else:
#                     intervention = "✅ LOW - Monitor Remotely"
#                     color = "green"
                
#                 st.markdown(f"""
#                 <div style='background-color: #{color}22; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {color};'>
#                     <strong>{row['sensor_id']}</strong><br>
#                     Congestion: {congestion:.1f}<br>
#                     Alerts: {row['alert_count']}<br>
#                     <strong>{intervention}</strong>
#                 </div>
#                 """, unsafe_allow_html=True)
#     else:
#         st.info("⏳ Collecting junction data...")
    
#     st.divider()
    
#     # Recent Critical Alerts
#     st.subheader("⚠️ Recent Critical Alerts")
#     df_alerts = fetch_recent_alerts()
    
#     if not df_alerts.empty:
#         # Format the dataframe
#         df_alerts['window_start'] = pd.to_datetime(df_alerts['window_start']).dt.strftime('%Y-%m-%d %H:%M')
        
#         # Display as styled table
#         st.dataframe(
#             df_alerts,
#             column_config={
#                 "sensor_id": st.column_config.TextColumn("Junction", width="medium"),
#                 "window_start": st.column_config.TextColumn("Time", width="medium"),
#                 "avg_speed": st.column_config.NumberColumn("Speed (km/h)", format="%.1f"),
#                 "vehicle_count": st.column_config.NumberColumn("Vehicles", format="%d"),
#                 "congestion_index": st.column_config.NumberColumn("Congestion", format="%.2f"),
#             },
#             hide_index=True,
#             use_container_width=True
#         )
#     else:
#         st.success("✅ No critical alerts in the system!")
    
#     # Footer
#     st.divider()
#     st.markdown("""
#     <div style='text-align: center; color: #666; padding: 2rem 0;'>
#         <p>Smart City Traffic Management System | Powered by Apache Kafka, Spark & Airflow</p>
#         <p style='font-size: 0.9rem;'>Data refreshes automatically every 5 seconds</p>
#     </div>
#     """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

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

# Database connection - NO CACHING to avoid "connection closed" errors
def get_db_connection():
    """Create PostgreSQL connection - creates fresh connection each time"""
    try:
        conn = psycopg2.connect(
            host='postgres',
            database='traffic_db',
            user='postgres',
            password='postgres',
            port=5432
        )
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        st.info("💡 Tip: If running locally, change host to 'localhost' in app.py")
        return None

# Fetch functions
def fetch_live_metrics():
    """Fetch latest traffic metrics - SHOWS ALL AVAILABLE DATA"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        # First check if ANY data exists
        count_query = "SELECT COUNT(*) as count FROM traffic_history"
        count_df = pd.read_sql(count_query, conn)
        
        if count_df['count'].iloc[0] == 0:
            st.warning("⏳ No data in database yet. Waiting for Spark to write first batch...")
            return None
        
        # Get metrics from ALL available data (no time filter)
        query = """
            SELECT 
                COUNT(*) as total_records,
                AVG(avg_vehicle_count)::int as avg_vehicles,
                AVG(avg_speed)::int as avg_speed,
                AVG(congestion_index)::numeric(5,1) as avg_congestion,
                MAX(window_start) as latest_data
            FROM traffic_history
        """
        df = pd.read_sql(query, conn)
        
        # Get active alerts count (all data)
        alert_query = "SELECT COUNT(*) as alert_count FROM critical_traffic_alerts"
        alerts_df = pd.read_sql(alert_query, conn)
        
        # Show latest data timestamp
        latest = df['latest_data'].iloc[0] if not df.empty else None
        if latest:
            st.sidebar.info(f"📅 Latest data: {latest}")
        
        return {
            'total_vehicles': df['avg_vehicles'].iloc[0] if not df.empty else 0,
            'avg_speed': df['avg_speed'].iloc[0] if not df.empty else 0,
            'active_alerts': alerts_df['alert_count'].iloc[0] if not alerts_df.empty else 0,
            'congestion_index': df['avg_congestion'].iloc[0] if not df.empty else 0
        }
    except Exception as e:
        st.error(f"Error fetching metrics: {str(e)}")
        return None
    finally:
        conn.close()

def fetch_hourly_traffic():
    """Fetch hourly aggregated traffic data - ALL DATA"""
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                EXTRACT(HOUR FROM window_start)::int as hour,
                AVG(avg_vehicle_count)::int as avg_vehicles,
                AVG(avg_speed)::int as avg_speed,
                AVG(congestion_index)::numeric(5,2) as avg_congestion
            FROM traffic_history
            GROUP BY EXTRACT(HOUR FROM window_start)
            ORDER BY hour
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error fetching hourly data: {str(e)}")
        return pd.DataFrame()
    finally:
        conn.close()

def fetch_junction_data():
    """Fetch junction-wise statistics - ALL DATA"""
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                sensor_id,
                COUNT(*) as total_records,
                AVG(congestion_index)::numeric(5,2) as avg_congestion,
                MAX(congestion_index)::numeric(5,2) as max_congestion,
                AVG(avg_vehicle_count)::int as avg_vehicles
            FROM traffic_history
            GROUP BY sensor_id
            ORDER BY avg_congestion DESC
        """
        df = pd.read_sql(query, conn)
        
        # Get alerts per junction
        alert_query = """
            SELECT 
                sensor_id,
                COUNT(*) as alert_count
            FROM critical_traffic_alerts
            GROUP BY sensor_id
        """
        alerts_df = pd.read_sql(alert_query, conn)
        
        # Merge dataframes
        if not alerts_df.empty:
            df = df.merge(alerts_df, on='sensor_id', how='left')
            df['alert_count'] = df['alert_count'].fillna(0).astype(int)
        else:
            df['alert_count'] = 0
            
        return df
    except Exception as e:
        st.error(f"Error fetching junction data: {str(e)}")
        return pd.DataFrame()
    finally:
        conn.close()

def fetch_recent_alerts(limit=10):
    """Fetch recent critical alerts"""
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()
    
    try:
        query = f"""
            SELECT 
                sensor_id,
                window_start,
                avg_speed::numeric(5,1) as avg_speed,
                avg_vehicle_count::int as vehicle_count,
                congestion_index::numeric(5,2) as congestion_index
            FROM critical_traffic_alerts
            ORDER BY window_start DESC
            LIMIT {limit}
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error fetching alerts: {str(e)}")
        return pd.DataFrame()
    finally:
        conn.close()

def get_data_stats():
    """Get database statistics"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        query = """
            SELECT 
                COUNT(*) as total_records,
                MIN(window_start) as earliest,
                MAX(window_start) as latest
            FROM traffic_history
        """
        df = pd.read_sql(query, conn)
        return df.iloc[0] if not df.empty else None
    except:
        return None
    finally:
        conn.close()

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🚦 Smart City Traffic Control Center</h1>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 1.2rem;'>Real-time Traffic Monitoring & Analytics Dashboard</p>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Dashboard Controls")
        auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=True)
        
        st.divider()
        
        # Show data statistics
        stats = get_data_stats()
        if stats is not None and stats['total_records'] > 0:
            st.success(f"✅ Database: {stats['total_records']} records")
            st.caption(f"From: {stats['earliest']}")
            st.caption(f"To: {stats['latest']}")
        else:
            st.warning("⏳ Waiting for data...")
        
        st.divider()
        st.header("📊 Filters")
        selected_junction = st.selectbox(
            "Select Junction",
            ["All", "Junction_A", "Junction_B", "Junction_C", "Junction_D"]
        )
        
        st.divider()
        st.header("ℹ️ System Status")
        st.success("✅ All systems operational")
        st.info(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")
        
        if st.button("🔄 Refresh Data"):
            st.cache_resource.clear()
            st.rerun()
    
    # Auto-refresh logic - moved to end of page to avoid interrupting data fetch
    # This will be handled at the bottom after all data is loaded
    
    # Fetch data
    metrics = fetch_live_metrics()
    
    if metrics:
        # Live Metrics (Top Row)
        st.subheader("📈 Traffic Metrics (All Available Data)")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🚗 Avg Vehicles",
                value=f"{metrics['total_vehicles']:,}",
                delta="Live"
            )
        
        with col2:
            st.metric(
                label="⚡ Avg Speed",
                value=f"{metrics['avg_speed']} km/h",
                delta=f"{metrics['avg_speed'] - 30} km/h" if metrics['avg_speed'] else "0 km/h"
            )
        
        with col3:
            st.metric(
                label="⚠️ Total Alerts",
                value=f"{metrics['active_alerts']}",
                delta="Critical" if metrics['active_alerts'] > 0 else "None"
            )
        
        with col4:
            st.metric(
                label="📊 Congestion Index",
                value=f"{metrics['congestion_index']:.1f}",
                delta=f"{metrics['congestion_index'] - 25:.1f}"
            )
    else:
        st.info("⏳ Waiting for data... Spark processes data in 2-minute windows. Please wait 2-3 minutes after starting the system.")
    
    st.divider()
    
    # Hourly Traffic Analysis
    st.subheader("📊 Hourly Traffic Analysis")
    df_hourly = fetch_hourly_traffic()
    
    if not df_hourly.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Traffic Volume Chart
            fig_volume = px.area(
                df_hourly,
                x='hour',
                y='avg_vehicles',
                title='Traffic Volume by Hour',
                labels={'hour': 'Hour of Day', 'avg_vehicles': 'Average Vehicles'},
                color_discrete_sequence=['#667eea']
            )
            fig_volume.update_layout(
                xaxis=dict(tickmode='linear', tick0=0, dtick=2),
                height=400
            )
            st.plotly_chart(fig_volume, use_container_width=True)
        
        with col2:
            # Congestion Trend Chart
            fig_congestion = px.line(
                df_hourly,
                x='hour',
                y='avg_congestion',
                title='Congestion Index Trend',
                labels={'hour': 'Hour of Day', 'avg_congestion': 'Congestion Index'},
                color_discrete_sequence=['#ef4444']
            )
            fig_congestion.update_traces(mode='lines+markers', line=dict(width=3))
            fig_congestion.update_layout(
                xaxis=dict(tickmode='linear', tick0=0, dtick=2),
                height=400
            )
            st.plotly_chart(fig_congestion, use_container_width=True)
    else:
        st.info("⏳ Waiting for hourly data... The system needs to collect data across multiple hours.")
    
    st.divider()
    
    # Junction Analysis
    st.subheader("🚨 Junction Analysis & Intervention Requirements")
    df_junctions = fetch_junction_data()
    
    if not df_junctions.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Junction comparison chart
            fig_junctions = go.Figure()
            
            fig_junctions.add_trace(go.Bar(
                name='Avg Congestion',
                x=df_junctions['sensor_id'],
                y=df_junctions['avg_congestion'],
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
                congestion = row['avg_congestion']
                
                if congestion > 50:
                    intervention = "🚨 URGENT - Deploy 3+ Officers"
                    color = "red"
                elif congestion > 30:
                    intervention = "⚠️ HIGH - Deploy 2 Officers"
                    color = "orange"
                elif congestion > 15:
                    intervention = "⚡ MODERATE - Deploy 1 Officer"
                    color = "blue"
                else:
                    intervention = "✅ LOW - Monitor Remotely"
                    color = "green"
                
                st.markdown(f"""
                <div style='background-color: #{color}22; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {color};'>
                    <strong>{row['sensor_id']}</strong><br>
                    Congestion: {congestion:.1f}<br>
                    Alerts: {row['alert_count']}<br>
                    <strong>{intervention}</strong>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("⏳ Collecting junction data...")
    
    st.divider()
    
    # Recent Critical Alerts
    st.subheader("⚠️ Recent Critical Alerts")
    df_alerts = fetch_recent_alerts()
    
    if not df_alerts.empty:
        # Format the dataframe
        df_alerts['window_start'] = pd.to_datetime(df_alerts['window_start']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Display as styled table
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
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p>Smart City Traffic Management System | Powered by Apache Kafka, Spark & Airflow</p>
        <p style='font-size: 0.9rem;'>Data refreshes automatically every 5 seconds</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh at the very end after all content is loaded
    if auto_refresh:
        time.sleep(5)
        st.rerun()

if __name__ == "__main__":
    main()