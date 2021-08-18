#!/usr/bin/env python

import http.client
import json
import argparse

def login(args):
    connection = http.client.HTTPConnection('localhost',port=5000)
    headers = {'Content-type': 'application/json'}
    body = {"LOGIN": {"address": args.ip}}
    json_body = json.dumps(body)
    connection.request("POST", "/login", json_body, headers)
    response = connection.getresponse()
    return response.read().decode('utf-8')

def discovery(args):
    connection = http.client.HTTPConnection('localhost',port=5000)
    headers = {'Content-type': 'application/json'}
    body = {"DISCOVERY": {"address": args.ip}}
    json_body = json.dumps(body)
    connection.request("GET", "/discovery",json_body, headers)
    response = connection.getresponse()
    return response.read().decode('utf-8')

def bidir(args):
    connection = http.client.HTTPConnection('localhost',port=5000)
    headers = {'Content-type': 'application/json'}
    body = {"BIDIR": {"address": args.ip, "SRC": args.src, "DST": args.dst}}
    json_body = json.dumps(body)
    connection.request("POST", "/bidir", json_body, headers)
    response = connection.getresponse()
    return response.read().decode('utf-8')

def unidir(args):
    connection = http.client.HTTPConnection('localhost',port=5000)
    headers = {'Content-type': 'application/json'}
    body = {"UNIDIR": {"address": args.ip, "SRC": args.src, "DST": args.dst}}
    json_body = json.dumps(body)
    connection.request("POST", "/unidir", json_body, headers)
    response = connection.getresponse()
    return response.read().decode('utf-8')

def delmap(args):
    connection = http.client.HTTPConnection('localhost',port=5000)
    headers = {'Content-type': 'application/json'}
    body = {"DELMAP": {"address": args.ip, "LIST": args.list}}
    json_body = json.dumps(body)
    connection.request("DELETE", "/delmap", json_body, headers)
    response = connection.getresponse()
    return response.read().decode('utf-8')

def logout(args):
    connection = http.client.HTTPConnection('localhost',port=5000)
    headers = {'Content-type': 'application/json'}
    body = {"LOGOUT": {"address": args.ip}}
    json_body = json.dumps(body)
    connection.request("POST", "/logout", json_body, headers)
    response = connection.getresponse()
    return response.read().decode('utf-8')

#Create argument parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='subcommands',
                                    description='valid subcommands',
                                    help='description')
#Login subparser
login_parser = subparsers.add_parser('login', help='login to device')
login_parser.add_argument('-a', dest='ip', required=True,
                                    help='IP of destinaton device')
login_parser.set_defaults(func=login)
#Discovery subparser
discovery_parser = subparsers.add_parser('discovery', help='show device structure and mappings')
discovery_parser.add_argument('-a', dest='ip', required=True,
                                    help='IP of destinaton device')
discovery_parser.set_defaults(func=discovery)
#Bidir subparser
bidir_parser = subparsers.add_parser('bidir', help='create bidirectional mapping')
bidir_parser.add_argument('-a', dest='ip', required=True,
                                    help='IP of destinaton device')
bidir_parser.add_argument('-s', dest='src', required=True,
                                    help='source port')
bidir_parser.add_argument('-d', dest='dst', required=True,
                                    help='destination port')
bidir_parser.set_defaults(func=bidir)
#Unidir subparser
unidir_parser = subparsers.add_parser('unidir', help='create unidirectional mapping')
unidir_parser.add_argument('-a', dest='ip', required=True,
                                    help='IP of destinaton device')
unidir_parser.add_argument('-s', dest='src', required=True,
                                    help='source port')
unidir_parser.add_argument('-d', dest='dst', required=True,
                                    help='destination port')
unidir_parser.set_defaults(func=unidir)
#Delmap subparser
delmap_parser = subparsers.add_parser('delmap', help='delete port mappings')
delmap_parser.add_argument('-a', dest='ip', required=True,
                                    help='IP of destinaton device')
delmap_parser.add_argument('-l', dest='list', nargs='+', required=True,
                                    help='list of device ports')
delmap_parser.set_defaults(func=delmap)
#Login subparser
logout_parser = subparsers.add_parser('logout', help='logout from device')
logout_parser.add_argument('-a', dest='ip', required=True,
                                    help='IP of destinaton device')
logout_parser.set_defaults(func=logout)


if __name__ == '__main__':
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        print(args.func(args))
