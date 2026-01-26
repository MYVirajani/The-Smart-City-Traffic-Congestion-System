CREATE TABLE IF NOT EXISTS critical_traffic_alerts (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,
    avg_speed FLOAT NOT NULL,
    avg_vehicle_count FLOAT NOT NULL,
    congestion_index FLOAT NOT NULL,
    alert_generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sensor_time ON critical_traffic_alerts(sensor_id, window_start);
CREATE INDEX idx_window_start ON critical_traffic_alerts(window_start);
CREATE INDEX idx_alert_time ON critical_traffic_alerts(alert_generated_at);

CREATE TABLE IF NOT EXISTS traffic_history (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,
    avg_speed FLOAT NOT NULL,
    avg_vehicle_count FLOAT NOT NULL,
    reading_count INTEGER NOT NULL,
    congestion_index FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_history_sensor_time ON traffic_history(sensor_id, window_start);

CREATE TABLE IF NOT EXISTS daily_reports (
    id SERIAL PRIMARY KEY,
    report_date DATE NOT NULL UNIQUE,
    total_alerts INTEGER,
    peak_congestion_time TIMESTAMP,
    worst_junction VARCHAR(50),
    report_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE critical_traffic_alerts IS 'Stores real-time critical traffic alerts when avg speed drops below 10 km/h';
COMMENT ON TABLE traffic_history IS 'Stores all processed traffic data for historical analysis';
COMMENT ON TABLE daily_reports IS 'Stores metadata about daily generated reports';