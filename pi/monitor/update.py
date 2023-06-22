import psycopg2
from constants import *
from datetime import datetime
from getmac import get_mac_address as getMacAddress
from monitor.configurations import Configurations

def retrieveDataFromEvents():

    result = None
    id = getMacAddress()
    configs = Configurations()  
    last_updated = configs.last_updated_monitor
    print(f"\x1b[6;30;46m [LOG retrieveDataFromEvents] Events: Last updated at {last_updated}\x1b[0m", flush=True)
    try:
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        query = "SELECT * FROM events WHERE (creation_date > (%s)::timestamp)"  
        data = (last_updated,)  
        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()
        connection.close() 
        print(f"\x1b[6;30;42m [LOG retrieveDataFromEvents] Data Successfully Retrieved \x1b[0m", flush=True)
    except Exception as e:
        print(f"\x1b[6;30;41m [LOG retrieveDataFromEvents] An error occurred: {e} \x1b[0m", flush=True)
    finally:
        if connection is not None:
            connection.close()    
    return id, result

def retrieveDataFromExternalPerformance():

    result = None
    id = getMacAddress()
    configs = Configurations()  
    last_updated = configs.last_updated_external_performance
    print(f"\x1b[6;30;46m [LOG retrieveDataFromExternalPerformance] External Performance: Last updated at {last_updated}\x1b[0m", flush=True)
    try:
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        query = "SELECT * FROM externalPerformance WHERE (creation_date > (%s)::timestamp)"  
        data = (last_updated,)  
        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()
        connection.close() 
        print(f"\x1b[6;30;42m [LOG retrieveDataFromExternalPerformance] Data Successfully Retrieved \x1b[0m", flush=True)
    except Exception as e:
        print(f"\x1b[6;30;41m [LOG retrieveDataFromExternalPerformance] An error occurred: {e} \x1b[0m", flush=True)
    finally:
        if connection is not None:
            connection.close()    
    return id, result

def retrieveDataFromInternalPerformance():

    result = None
    id = getMacAddress()
    configs = Configurations()  
    last_updated = configs.last_updated_internal_performance

    print(f"\x1b[6;30;46m [LOG retrieveDataFromInternalPerformance] Internal Performance: Last updated at {last_updated}\x1b[0m", flush=True)

    try:
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        query = "SELECT * FROM internalPerformance WHERE (creation_date > (%s)::timestamp)"  
        data = (last_updated,)  
        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()
        connection.close() 
        print(f"\x1b[6;30;42m [LOG retrieveDataFromInternalPerformance] Data Successfully Retrieved \x1b[0m", flush=True)
    except Exception as e:
        print(f"\x1b[6;30;41m [LOG retrieveDataFromInternalPerformance] An error occurred: {e} \x1b[0m", flush=True)
    finally:
        if connection is not None:
            connection.close()    
    return id, result

def retrieveDataFromWifiTest():
    result = None
    id = getMacAddress()
    configs = Configurations()  
    last_updated = configs.last_updated_wifi_test

    print(f"\x1b[6;30;46m [LOG retrieveDataFromWifiTest] Wifi Test: Last updated at {last_updated}\x1b[0m", flush=True)

    try:
        connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
        cursor = connection.cursor()
        query = "SELECT * FROM wifiTest WHERE (creation_date > (%s)::timestamp)"  
        data = (last_updated,)  
        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()
        connection.close() 
        print(f"\x1b[6;30;42m [LOG retrieveDataFromWifiTest] Data Successfully Retrieved \x1b[0m", flush=True)
    except Exception as e:
        print(f"\x1b[6;30;41m [LOG retrieveDataFromWifiTest] An error occurred: {e} \x1b[0m", flush=True)
    finally:
        if connection is not None:
            connection.close()    
    return id, result