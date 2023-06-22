import subprocess
from datetime import datetime
import psycopg2
from constants import *

def wifiTest():

    iwlist_scan = subprocess.check_output("sudo iwlist wlan0 scan", shell=True, stderr=subprocess.STDOUT)

    return iwlist_scan.decode('utf-8')
    

def outputParser(test_output):

    splitted = str(test_output).split('Cell')
    rssids = []
    filtered = []

    for x in splitted:
        rssids.append((x.split('IE'))[0])
        print((x.split('IE'))[0])

    for x in rssids:
        filtered.append(x.split('\n'))

    filtered = filtered[1:] #ignore first position which is the title

    ssids = {}
    space = ' ' * 20

    for x in filtered:
        tmp_lst = []
        for i in range(1, 6):
            tmp = x[i].replace(space, '')
            tmp_lst.append(tmp)
        ssids[x[0]] = tmp_lst

    res = {}

    for x in ssids.keys():
        ap = (x.split(' '))[-1]
        res[ap] = ssids[x]

    return res


def registResult(output):

    #format: {ap mac: [channel, frequency, quality, signal level, encryption, essid]}

    for x in output.keys():

        ap_mac = x

        channel = int((output[x][0].split(':'))[-1])
        frequency = float(((output[x][1].split(':'))[1].split(' '))[0])
        quality = (((output[x][2].split('='))[1].split(' '))[0])
        signal_level = ((output[x][2].split('level='))[-1].strip())
        encryption = ((output[x][3].split(':'))[-1])
        essid = ((output[x][4].split(':'))[-1])

        try:
            connection = psycopg2.connect(LOCAL_DB_CONNECTION_STRING)
            cursor = connection.cursor()          
            query = f"INSERT INTO wifiTest (creation_date, ap, channel, frequency, quality, signal_level, encryption_mode, essid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"    
            data = (datetime.now(), 
                        ap_mac,
                        channel, 
                        frequency, 
                        quality, 
                        signal_level, 
                        encryption, 
                        essid
                    )            
            cursor.execute(query, data)
            connection.commit()
            cursor.close()
        except Exception as e:
            print(f"\x1b[6;30;41m [LOG WifiTest - DB] An error ocurred: {str(e)}\x1b[0m", flush=True)
        finally:
            if connection is not None:
                connection.close()

def monitorWiFi():

    try:

        res = wifiTest()
        output = outputParser(res)
        registResult(output)

    except Exception as e:

        print(f"\x1b[6;30;41m [LOG Ping] An error ocurred: Monitor WiFi: {str(e)}\x1b[0m", flush=True)


