#!/usr/bin/python

from datetime import datetime
import argparse
import configparser
import os
import os.path
import re
import requests
import subprocess

configname = os.path.expanduser("~/.dyfi.cfg")

config = configparser.ConfigParser()
config.read(configname)

def update(user, password, hostname):
    baseurl = "https://www.dy.fi/nic/update?hostname=" 
    req = request.get(baseurl + hostname, auth=(user, passwd))

def get_ip():
    "Gets current ip using checkip service provided by dy.fy"
    req = requests.get("http://checkip.dy.fi/")
    regex = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    match = re.search(regex, req.text)
    return match.group(1)

def since_update(time):
    now = datetime.today().timestamp()
    old = datetime.fromtimestamp(time)
    return (old - now).days

def save_config():
    with open(configname, "w") as configfile:
        config.write(configfile)

def add_host():
    print("Username: ", end="")
    user = input()
    print("Password: ", end="")
    password = input()
    print("Host: ", end="")
    hostname = input()
    config[hostname] = {}
    config[hostname]["user"] = user
    config[hostname]["password"] = password
    config[hostname]["updated"] = 0
    save_config()

if not os.path.exists(configname):
    print("Config file not found. Run \n\n" +
          "  $ dyfi.py --add\n\nto add one of more configs")
    exit(1)


parser = argparse.ArgumentParser(description='dyfi updater')
parser.add_argument('--add', action='store_true', help='Add new dy.fi host.')
parser.add_argument('--edit', action='store_true', help='Edit config file.')
parser.add_argument('-u', '--update', action='store_true', 
        help='Update all hosts that need updating')

args = parser.parse_args()
if args.add:
    add_host()
elif args.edit:
    editor = os.environ['EDITOR']
    ret = subprocess.call([editor, configname])
elif args.update:
    for host in config:
        if since_update(config[host]["updated"]) > 5:
            update(config[host]["user"], config[host]["password"], host)
            config[host]["updated"] = datetime.today().timestamp()
