#!/usr/bin/env python

from flask import Flask, json, request
import yaml
import time
import threading

#Initialization of server
with open('INIT.yaml') as fd:
    devices_dict = yaml.safe_load(fd)

#Dictionary for devices connection tracking
DEV_LOGIN = {}

#Empty function for threading
def empty():
    pass

def idle_timeout(IP):
    global DEV_LOGIN
    DEV_LOGIN[IP] = threading.Timer(30,empty)  
    DEV_LOGIN[IP].start()


# Create an API server
srv = Flask(__name__)

@srv.route('/login', methods=['POST'])
def login():
    try:
        BODY = request.json
        IP = BODY['LOGIN']['address']
    except:
        return json.dumps({"STATUS": False})
    idle_timeout(IP)
    return json.dumps({"STATUS": True})

@srv.route('/discovery', methods=['GET'])
def discovery():
    try:
        BODY = request.json
        IP = BODY['DISCOVERY']['address']
    except:
        return json.dumps({"STATUS": False, "MSG": "Wrong request format!"})
    if isinstance(DEV_LOGIN.get(IP), threading.Timer) and DEV_LOGIN.get(IP).is_alive():
        idle_timeout(IP)
        return json.dumps({"STATUS": True, "MSG": devices_dict})
    else:
        return json.dumps({"STATUS": False, "MSG": "Connection to {} is closed!".format(IP)})

@srv.route('/bidir', methods=['POST'])
def bidir():
    try:
        BODY = request.json
        IP = BODY['BIDIR']['address']
        SRC = BODY['BIDIR']['SRC']
        DST = BODY['BIDIR']['DST']
    except:
        return json.dumps({"STATUS": False, "MSG": "Wrong request format!"})
    if isinstance(DEV_LOGIN.get(IP), threading.Timer) and DEV_LOGIN.get(IP).is_alive():
        idle_timeout(IP)
#Check if device exists
        if not devices_dict.get(IP):
            return json.dumps({"STATUS": False, "MSG": "There is no such a device as {}!".format(IP)})
        else:
#Check if modules/ports are valid
            if not devices_dict[IP]["STRUCTURE"].get(int(SRC.split('/')[0])):
                return json.dumps({"STATUS": False, "MSG": "Device {} has not such a module {}".format(IP,SRC.split('/')[0])})
            elif int(SRC.split('/')[1]) not in devices_dict[IP]["STRUCTURE"][int(SRC.split('/')[0])]:
                return json.dumps({"STATUS": False, "MSG": "Device {} doesn't have a port {} on a module {}".format(IP,SRC.split('/')[1],SRC.split('/')[0])})
            if not devices_dict[IP]["STRUCTURE"].get(int(DST.split('/')[0])):
                return json.dumps({"STATUS": False, "MSG": "Device {} has not such a module {}".format(IP,DST.split('/')[0])})
            elif int(DST.split('/')[1]) not in devices_dict[IP]["STRUCTURE"][int(DST.split('/')[0])]:
                return json.dumps({"STATUS": False, "MSG": "Device {} doesn't have a port {} on a module {}".format(IP,DST.split('/')[1],DST.split('/')[0])})
#Check if SRC or DST ports are on the same module
            if SRC.split('/')[0] == DST.split('/')[0]:
                return json.dumps({"STATUS": False, "MSG": "Mapping between ports on the same module is prohibited"})
#Check if BIDIR is already existed
            if devices_dict[IP]["MAPPINGS"].get(SRC):
                if DST in devices_dict[IP]["MAPPINGS"][SRC]:
                    if devices_dict[IP]["MAPPINGS"].get(DST):
                        if SRC in devices_dict[IP]["MAPPINGS"][DST]:
                            return json.dumps({"STATUS": True, "MSG": "Mapping already exists"})
#Check if SRC or DST is already participating in other BIDIR connection
            if devices_dict[IP]["MAPPINGS"].get(SRC):
                for _dst in devices_dict[IP]["MAPPINGS"][SRC]:
                    if devices_dict[IP]["MAPPINGS"].get(_dst):
                        if SRC in devices_dict[IP]["MAPPINGS"][_dst]:
                            return json.dumps({"STATUS": False, "MSG": "Port {} in use".format(SRC)})
            if devices_dict[IP]["MAPPINGS"].get(DST):
                for _dst in devices_dict[IP]["MAPPINGS"][DST]:
                    if devices_dict[IP]["MAPPINGS"].get(_dst):
                        if DST in devices_dict[IP]["MAPPINGS"][_dst]:
                            return json.dumps({"STATUS": False, "MSG": "Port {} in use".format(DST)})
#Make a BIDIR from UNIDIR connection
            if devices_dict[IP]["MAPPINGS"].get(SRC):
                if DST in devices_dict[IP]["MAPPINGS"][SRC]:
                    if devices_dict[IP]["MAPPINGS"].get(DST):
                        devices_dict[IP]["MAPPINGS"][DST].append(SRC)
                        return json.dumps({"STATUS": True, "MSG": "Mapping created"})
                    else:
                        devices_dict[IP]["MAPPINGS"][DST] = [SRC]
                        return json.dumps({"STATUS": True, "MSG": "Mapping created"})
            if devices_dict[IP]["MAPPINGS"].get(DST):
                if SRC in devices_dict[IP]["MAPPINGS"][DST]:
                    if devices_dict[IP]["MAPPINGS"].get(SRC):
                        devices_dict[IP]["MAPPINGS"][SRC].append(DST)
                        return json.dumps({"STATUS": True, "MSG": "Mapping created"})
                    else:
                        devices_dict[IP]["MAPPINGS"][SRC] = [DST]
                        return json.dumps({"STATUS": True, "MSG": "Mapping created"})
#Create a new BIDIR connection
            if devices_dict[IP]["MAPPINGS"].get(SRC):
                devices_dict[IP]["MAPPINGS"][SRC].append(DST)
            else:
                devices_dict[IP]["MAPPINGS"][SRC] = [DST]
            if devices_dict[IP]["MAPPINGS"].get(DST):
                devices_dict[IP]["MAPPINGS"][DST].append(SRC)
            else:
                devices_dict[IP]["MAPPINGS"][DST] = [SRC]
            return json.dumps({"STATUS": True, "MSG": "Mapping created"})
    else:
        return json.dumps({"STATUS": False, "MSG": "Connection to {} is closed!".format(IP)})

@srv.route('/unidir', methods=['POST'])
def unidir():
    try:
        BODY = request.json
        IP = BODY['UNIDIR']['address']
        SRC = BODY['UNIDIR']['SRC']
        DST = BODY['UNIDIR']['DST']
    except:
        return json.dumps({"STATUS": False, "MSG": "Wrong request format!"})
    if isinstance(DEV_LOGIN.get(IP), threading.Timer) and DEV_LOGIN.get(IP).is_alive():
        idle_timeout(IP)
#Check if device exists
        if not devices_dict.get(IP):
            return json.dumps({"STATUS": False, "MSG": "There is no such a device as {}!".format(IP)})
        else:
#Check if modules/ports are valid
            if not devices_dict[IP]["STRUCTURE"].get(int(SRC.split('/')[0])):
                return json.dumps({"STATUS": False, "MSG": "Device {} has not such a module {}".format(IP,SRC.split('/')[0])})
            elif int(SRC.split('/')[1]) not in devices_dict[IP]["STRUCTURE"][int(SRC.split('/')[0])]:
                return json.dumps({"STATUS": False, "MSG": "Device {} doesn't have a port {} on a module {}".format(IP,SRC.split('/')[1],SRC.split('/')[0])})
            if not devices_dict[IP]["STRUCTURE"].get(int(DST.split('/')[0])):
                return json.dumps({"STATUS": False, "MSG": "Device {} has not such a module {}".format(IP,DST.split('/')[0])})
            elif int(DST.split('/')[1]) not in devices_dict[IP]["STRUCTURE"][int(DST.split('/')[0])]:
                return json.dumps({"STATUS": False, "MSG": "Device {} doesn't have a port {} on a module {}".format(IP,DST.split('/')[1],DST.split('/')[0])})
#Check if SRC or DST ports are on the same module
            if SRC.split('/')[0] == DST.split('/')[0]:
                return json.dumps({"STATUS": False, "MSG": "Mapping between ports on the same module is prohibited"})
#Check if UNIDIR is already existed
            if devices_dict[IP]["MAPPINGS"].get(SRC):
                if DST in devices_dict[IP]["MAPPINGS"][SRC]:
                    return json.dumps({"STATUS": True, "MSG": "Mapping already exists"})
#Check if DST port is in use as a destination port
            for _src in devices_dict[IP]["MAPPINGS"]:
                if DST in devices_dict[IP]["MAPPINGS"][_src]:
                    return json.dumps({"STATUS": False, "MSG": "Port {} in use".format(DST)})
#Create an additional connection for SRC port
            if devices_dict[IP]["MAPPINGS"].get(SRC):
                devices_dict[IP]["MAPPINGS"][SRC].append(DST)
                return json.dumps({"STATUS": True, "MSG": "Additional mapping created"})
#Create a new UNIDIR mappings
            else:
                devices_dict[IP]["MAPPINGS"][SRC] = [DST]
                return json.dumps({"STATUS": True, "MSG": "Mapping created"})
    else:
        return json.dumps({"STATUS": False, "MSG": "Connection to {} is closed!".format(IP)})

@srv.route('/delmap', methods=['DELETE'])
def delmap():
    try:
        BODY = request.json
        IP = BODY['DELMAP']['address']
        DEL_LIST = BODY['DELMAP']['LIST']
    except:
        return json.dumps({"STATUS": False, "MSG": "Wrong request format!"})
    if isinstance(DEV_LOGIN.get(IP), threading.Timer) and DEV_LOGIN.get(IP).is_alive():
        idle_timeout(IP)
#Ckeck if DEL_LIST is a list
        if not isinstance(DEL_LIST,list):
            return json.dumps({"STATUS": False, "MSG": "Wrong request format!"})
#Check if device exists
        if not devices_dict.get(IP):
            return json.dumps({"STATUS": False, "MSG": "There is no such a device as {}!".format(IP)})
        else:
#Remove all existing mappings
            for _src in DEL_LIST:
                if devices_dict[IP]["MAPPINGS"].get(_src):
                    del devices_dict[IP]["MAPPINGS"][_src]
            return json.dumps({"STATUS": True, "MSG": "Mapping removed successfully"})
    else:
        return json.dumps({"STATUS": False, "MSG": "Connection to {} is closed!".format(IP)})

@srv.route('/logout', methods=['POST'])
def logout():
    try:
        BODY = request.json
        IP = BODY['LOGOUT']['address']
    except:
        return json.dumps({"STATUS": False})
    if DEV_LOGIN.get(IP):
        del DEV_LOGIN[IP]
    return json.dumps({"STATUS": True})

if __name__ == '__main__':
    srv.run() 
