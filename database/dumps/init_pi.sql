DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS externalPerformance CASCADE;
DROP TABLE IF EXISTS internalPerformance CASCADE;

SET TIME ZONE '+0:00';

CREATE TABLE events (
    creation_date TIMESTAMP,
    destination_ip VARCHAR(100) NOT NULL,
    max NUMERIC,
    min NUMERIC,
    avg NUMERIC,
    packets_sent INTEGER,
    packets_received INTEGER,
    packet_loss DECIMAL(4,1),
    jitter DECIMAL(4,1),
    interface VARCHAR(20),
    PRIMARY KEY (creation_date)
);

CREATE TABLE externalPerformance (
    creation_date TIMESTAMP,
    upload_speed NUMERIC,
    download_speed NUMERIC,
    latency NUMERIC,
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
    jitter NUMERIC,
    packet_loss NUMERIC,    
    sent_Mbps NUMERIC,
    received_Mbps NUMERIC,
    destination_host VARCHAR(200),
    PRIMARY KEY (creation_date)
);
