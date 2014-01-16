#!/usr/bin/python

from datetime import datetime
import configparser
import os.path
import re
import requests

config = configparser.ConfigParser()
config.read(os.path.expanduser("~/.dyfi.cfg"))

def update(user, password, hostname):
    baseurl = "https://www.dy.fi/nic/update?hostname=" 
    req = request.get(baseurl + hostname, auth=(user, passwd))

def get_ip():
    "Gets current ip using checkip service provided by dy.fy"
    req = requests.get("http://checkip.dy.fi/")
    regex = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    match = re.search(regex, req.text)
    return match.group(1)

def last_update(time):
    now = datetime.today().timestamp()
    old = datetime.fromtimestamp(time)
    return (old - now).days

def save_config():
    with open(os.path.expanduser("~/.dyfi.cfg"), "w") as configfile:
        config.write(configfile)

if not os.path.exists(os.path.expanduser("~/.dyfi.cfg")):
    print("Config file not found. Run \n\n" +
          "  $ dyfi.py --add\n\nto add one of more configs")
