MAX_PING = 'rtt_max'
MIN_PING = 'rtt_min'
AVG_PING = 'rtt_avg'
SENT = 'packet_transmit'
RECEIVED = 'packet_receive'
PACKET_LOSS = 'packet_loss_rate'
CONNECTED = 'connected'
DISCONNECTED = 'disconnected'
NO_CONNECTION = 'no_connection'
LOCAL_DB_NAME = 'local_db'
MAIN_DB_NAME = 'main_db'
LOCAL_DB_USER = 'pi'
LOCAL_DB_PWD = 'raspberry'
LOCAL_DB_IP = '172.30.0.10'
ETH0_INTERFACE = 'enp0s3' # CHANGE 4 RPI ones
WLAN0_INTERFACE = 'enp0s3' # CHANGE 4 RPI ones - IRRELEVANT

LOCAL_DB_CONNECTION_STRING = "dbname=%s user=%s password=%s host=%s" % (LOCAL_DB_NAME, LOCAL_DB_USER, LOCAL_DB_PWD, LOCAL_DB_IP)