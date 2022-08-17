#%%
from opcua import Client
from opcua import ua
import json               # Json formating library
import threading          # Allow threading
import random
from datetime import datetime #used for timestamp
from time import sleep    # pause execution
import os , uuid
from azure.storage.queue import QueueService #Connect to Azure Queue
from azure.storage.queue import QueueMessageFormat # message format of queue
from azure.cosmosdb.table.tableservice import TableService
#from azure.cosmosdb.table.models import Entity6
from azure.iot.device import (IoTHubDeviceClient, Message, common, exceptions ) #Azure SDK 
#%%172.17.0.2
#192.168.178.60
client = Client("opc.tcp://172.17.0.2:4848") # this is the IP address of the Servers Dcoker container
client.connect()
#nodes = client.get_objects_node()
#child = nodes.get_children()[1]
#test = child.get_children()
#text_t = client.get_node("ns=2;i=2").get_value()
# global variabls defintion
#%%
global data #data: To get the variable list that has to be read from the OPC_Server
global config #config: To get the keys required for the Azure Services

data = json.load(open('varlis.json','rb'))
config = json.load(open('Config.json','rb'))
CONNECTION_STRING = config['IoT_Hub_Key']
client.load_type_definitions()  # load definition of server specific structures/extension objects

#Functions Definitions
def Timestamp():      #Gives the Timestamp 
    my_date = datetime.now()
    return my_date.strftime('%Y-%m-%dT%H:%M:%S.%f%zZ') 

def get_json_varlist():   # Gets the variable list from json file values of the variables
    global data
    _json = '{}'
    _ID = {"DeviceID":"Backend", "myinteger":Timestamp()}
    _jsonobject = json.loads(_json)
    _jsonobject.update(_ID)
    global Result
    for var in data:
        try:
            var_address = data[var]
            node = client.get_node(var_address)
            value = node.get_value()
            _jsonobject.update({var : value})
            
            #alternative
            #_jsonobject.update({var : client.get_node(data[var]).get_value()})
        except:
            print("Connection failed to OPC UA Server")
    _jsonobject.update({var : value})
    return json.dumps(_jsonobject)
  # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects

def iothub_client_init(): #Intiate the connection with the cloud
    # Create an IoT Hub client
    try:
        client = IoTHubDeviceClient.create_from_connection_string( CONNECTION_STRING , websockets=True )
        client.connect()
        return client
    except:
        print("Connection to Azure failed, retry in 10 seconds")
        sleep(10)
        iothub_client_init()   

def publich_cycle(): #Function to read from OPC_server and  publish to Azure
    try:
        strtosend = get_json_varlist()
        print( "archive: {}".format(strtosend) )
        sendmqtt.send_message(strtosend)
        print ( "The Archive Message sent successfully" )
        #sleep(10)
    except:
        iothub_client_init()
    #threading.Timer(10, publich_cycle).start()

n = '{"DeviceID": "Backend_archieve", "myinteger": "2021-07-01T19:20:28.807623Z", "Operation_mode": "Automatic", "Current_operation": "Stopped", "Quit": "False", "inductive_counter": "0", "total_inductive_counter": "0", "capactive_counter": "0", "total_capactive_counter": "0", "zu_hoch": "0", "total_zu_hoch": "0", "optisch_counter": "0", "total_optisch_counter": "0", "Hoehe_messung": "True", "Alarm": "False"}'

sendmqtt = iothub_client_init() 
#Create MQTT client 
while True :
    publich_cycle()
    #sendmqtt.send_message(n)
    sleep (3)
    print("This was the way to do it ") 
client.disconnect()
