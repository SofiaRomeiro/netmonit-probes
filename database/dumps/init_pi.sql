DROP TABLE IF EXISTS ping CASCADE;
DROP TABLE IF EXISTS events CASCADE;

CREATE TABLE events (
    creation_date TIMESTAMP WITHOUT TIME ZONE,
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
    creation_date TIMESTAMP WITHOUT TIME ZONE,
    upload_speed INTEGER,
    download_speed INTEGER,
    latency INTEGER,
    bytes_sent INTEGER,
    bytes_received INTEGER,
    destination_host VARCHAR(200), 
    PRIMARY KEY (creation_date)
);

CREATE TABLE internalPerformance (
    creation_date TIMESTAMP WITHOUT TIME ZONE,
    protocol VARCHAR(10),
    bytes_sent INTEGER,
    bytes_received INTEGER,
    jitter INTEGER,
    packet_loss INTEGER,    
    sent_Mbps INTEGER,
    received_Mbps INTEGER,
    destination_host VARCHAR(200),
    PRIMARY KEY (creation_date)
);
