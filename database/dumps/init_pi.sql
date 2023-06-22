DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS externalPerformance CASCADE;
DROP TABLE IF EXISTS internalPerformance CASCADE;

SET TIME ZONE '+0:00';

CREATE TABLE events (
    creation_date TIMESTAMP,
    destination_ip VARCHAR(100) NOT NULL,
    max BIGINT,
    min BIGINT,
    avg BIGINT,
    packets_sent INTEGER,
    packets_received INTEGER,
    packet_loss DECIMAL(5,2),
    jitter DECIMAL(8,3),
    interface VARCHAR(20),
    PRIMARY KEY (creation_date)
);

CREATE TABLE externalPerformance (
    creation_date TIMESTAMP,
    upload_speed BIGINT,
    download_speed BIGINT,
    latency BIGINT,
    bytes_sent BIGINT,
    bytes_received BIGINT,
    destination_host VARCHAR(200), 
    PRIMARY KEY (creation_date)
);

CREATE TABLE internalPerformance (
    creation_date TIMESTAMP,
    protocol VARCHAR(10),
    bytes_sent BIGINT,
    bytes_received BIGINT,
    jitter BIGINT,
    packet_loss BIGINT,    
    sent_Mbps BIGINT,
    received_Mbps BIGINT,
    destination_host VARCHAR(200),
    PRIMARY KEY (creation_date)
);

CREATE TABLE wifiTest (
    creation_date TIMESTAMP,
    ap VARCHAR(100) NOT NULL,
    channel BIGINT,
    frequency BIGINT,
    quality VARCHAR(20),
    signal_level VARCHAR(20),
    encryption_mode VARCHAR(20),
    essid VARCHAR(100),
    PRIMARY KEY (creation_date)
);
