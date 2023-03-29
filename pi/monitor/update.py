import psycopg2
from constants import *
from getmac import get_mac_address as getMacAddress
from monitor.configurations import Configurations

def retrieveDataFromEvents():

    result = None
    id = getMacAddress()
    configs = Configurations()  
    last_updated = configs.last_updated_monitor

    print(f"[LOG Update] Last updated at {last_updated}")

    try:
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        query = "SELECT * FROM events WHERE (creation_date > (%s)::timestamp)"  
        data = (last_updated,)  
        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()
        connection.close() 
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection is not None:
            connection.close()

    print(f"[LOG Update - Ping] {result}")
    
    return id, result

def retrieveDataFromPerformance():

    result = None
    id = getMacAddress()
    configs = Configurations()  
    last_updated = configs.last_updated_performance

    print(f"[LOG Update] Last updated at {last_updated}")

    try:
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        query = "SELECT * FROM performance WHERE (creation_date > (%s)::timestamp)"  
        data = (last_updated,)  
        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()
        connection.close() 
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection is not None:
            connection.close()

    print("Query result:" + str(result))
    
    return id, result
