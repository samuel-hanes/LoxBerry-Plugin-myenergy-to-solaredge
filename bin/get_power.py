#!/usr/bin/python3

import os
import socket
import logging
from configparser import ConfigParser
import json
import influxdb_client 
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.domain.write_precision import WritePrecision
from datetime import datetime

# additional imports for myenergi async api
import asyncio
from influxdb_client.domain import write_precision

def send_udp(MINISERVER_IP, UDP_PORT, MESSAGE):
    """Send data to miniserver udp port"""
    try:
        # start the server listening on UDP socket
        sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        sock.sendto( MESSAGE.encode('ascii'), (MINISERVER_IP, UDP_PORT) )
        logging.debug("<DEBUG> Message: ", MESSAGE)
    except:
        logging.error("<ERROR> Failed to send message to miniserver socket!")
        logging.debug("<DEBUG> Message: ", MESSAGE)
        
## we will push these data to influxdb
#"con": consumption in watt
#"grd": grid in watt
#"gen": generation in watt
#"chg": charge in watt
#"bat": battery in watt,
#"vol": volt * 10,
#"frq": hertz ,
#"eimp": energy imported kwh ,
#"eexp": energy exported kwh ,
#"egen": energy generated kwh ,
#"egrn": energy green kwh 

def send_influxdb(dictionary,in_database,in_measurement, in_server, in_port, in_user, in_pwd):
    """Send data to influxdb"""
    if in_database != "" and in_server != "" and in_measurement != "" and in_port != "":
        try:
            in_url = "http://"+in_user+":"+in_pwd+"@"+in_server+":"+in_port;
            client = InfluxDBClient(in_url, org=None)
            write_api = client.write_api(write_options=SYNCHRONOUS)
            p = Point(in_measurement)\
            .field("con", dictionary["con"]*1000).field("grd", dictionary["grd"]*1000).field("gen", dictionary["gen"]*1000)\
            .field("chg", dictionary["chg"]*1000).field("bat", dictionary["bat"]*1000)\
            .field("vol", float(dictionary["vol"])).field("frq", float(dictionary["frq"]))\
            .field("eimp", dictionary["eimp"]).field("eexp", dictionary["eexp"]).field("egen", dictionary["egen"]).field("egrn", dictionary["egrn"])\
            .time(datetime.now(), write_precision=WritePrecision.S)
            
            write_api.write(bucket=in_database, record=p, org=in_database, auth_basic=True)
        except Exception as ex:
            logging.error("<ERROR> Failed to send message to influxdb!")
            logging.error("<DEBUG> Exception: ", ex)

async def main():
    """loxberry plugin for myenergi API sends every 1 minutes the actual
    power production and power consumtion values to the miniserver"""
    # create file strings from os environment variables
    lbplog = os.environ['LBPLOG'] + "/myenergi/myenergi.log"
    lbpconfig = os.environ['LBPCONFIG'] + "/myenergi/plugin.cfg"
    lbsconfig = os.environ['LBSCONFIG'] + "/general.cfg"

    # creating log file and set log format
    logging.basicConfig(filename=lbplog,level=logging.INFO,format='%(asctime)s: %(message)s ')
    #logging.info("<INFO> initialise logging...")
    # open config file and read options
    try:
        from pymyenergi.connection import Connection
        from pymyenergi.client import MyenergiClient
    except:
        logging.error("<ERROR> Error loading pymyenergi python api module... exit script")
        return
    try:
        cfg = ConfigParser()
        global_cfg = ConfigParser()
        cfg.read(lbpconfig)
        global_cfg.read(lbsconfig)
    except:
        logging.error("<ERROR> Error parsing config files...")

    #define variables with values from config files
    apiKey = cfg.get("MYENERGI", "API_KEY")
    serial = cfg.get("MYENERGI", "SERIAL")
    # comment for local debugging
    miniserver = global_cfg.get("MINISERVER1", "IPADDRESS")
    udp_port = int(cfg.get("MINISERVER", "PORT"))
    # uncomment for local debugging
    #miniserver = "127.0.0.1" 
    #udp_port = 15555
    
    in_database = cfg.get('INFLUXDB','DATABASE')
    in_measurement = cfg.get('INFLUXDB','MEASUREMENT')
    in_server = cfg.get('INFLUXDB','SERVER')
    in_port = cfg.get('INFLUXDB','PORT')
    in_user = cfg.get('INFLUXDB','USERNAME')
    in_pwd = cfg.get('INFLUXDB','PASSWORD')    

    # get the data as dictionary and as json
    try:
        dictionary = await get_data(serial, apiKey)
        msg = json.dumps(dictionary, indent = 2 , separators = (" , ", ": "))
        logging.info("<INFO> Value: %s" % msg)
    except:
        logging.error("<ERROR> Failed to execute API call...")
        msg = None

    # send the data to influxdb
    if dictionary != None:
        send_influxdb(dictionary,in_database,in_measurement, in_server, in_port, in_user, in_pwd)
        logging.info("<INFO> Data sent to Influxdb IP: %s" % in_server)
    else:
        logging.error("<ERROR> Nothing sent to Influxdb IP: %s" % in_server)
        
    # send the data to miniserver
    if msg != None:
        send_udp(miniserver, udp_port, msg)
        logging.info("<INFO> Message sent to Miniserver IP: %s" % miniserver)
    else:
        logging.error("<ERROR> Nothing sent to Miniserver IP: %s" % miniserver)


async def get_data(user, password) -> None:
    from datetime import datetime
    from pymyenergi.connection import Connection
    from pymyenergi.client import MyenergiClient
    conn = Connection(user, password)
    client = MyenergiClient(conn)
    
    # this would only refresh the current power values
    await client.refresh()
    # this also refreshes the daily sums
    await client.refresh_history_today()
    # this would also refresh the devices
    #await client.get_devices()
    # this would call the refresh methods again
    #out = await client.show()
    
    # construct dictionary
    now = datetime.now()
    currentdate = now.strftime("%d-%m-%Y")
    currenttime = now.strftime("%H:%M:%S")
    
    consumption = client.consumption_home/1000.0
    grid = client.power_grid/1000.0
    generation = max(client.power_generation,0)/1000.0
    charging = client.power_charging/1000.0
    battery = client.power_battery/1000.0
    
    consumption = consumption.__round__(2)
    grid = grid.__round__(2)
    generation = generation.__round__(2)
    charging = charging.__round__(2)
    battery = battery.__round__(2)
    
    response = {
        'dat':currentdate,
        'tim':currenttime,
        'con':consumption,
        'grd':grid,
        'gen':generation,
        'chg':charging,
        'bat':battery,
        'vol':round(client.voltage_grid * 10),
        'frq':round(client.frequency_grid),
        'eimp':client.energy_imported,
        'eexp':client.energy_exported,
        'egen':client.energy_generated,
        'egrn':client.energy_green
        }
    return response


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    
