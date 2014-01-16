#!/usr/bin/python

from datetime import datetime
import argparse
import configparser
import logging
import os
import os.path
import re
import requests
import subprocess

configname = os.path.expanduser("~/.dyfi.cfg")

config = configparser.ConfigParser()
with open(configname) as configfile:
    config.read_file(configfile)

logging.basicConfig(format='%(levelname)s:%(message)s')

def update(user, password, hostname):
    baseurl = "https://www.dy.fi/nic/update?hostname=" 
    req = requests.get(baseurl + hostname, auth=(user, password))
    if re.match("good [0-9.]+", req.text):
        logging.info("Päivitys onnistui: " + hostname + ", " + req.text)
    elif re.match("nochg", req.text):
        logging.warning("IP osoite ei ollut muuttunut viime päivityksestä.")
    elif re.match("badauth", req.text):
        logging.error("Tunnistautuminen epäonnistui.")
    elif re.match("nohost", req.text):
        logging.error("Domain nimeä ei annettu tai käyttäjä ei omista " +
                      "domainia")
    elif re.match("notfqdn", req.text):
        logging.error("Domain nimi ei ole oikea .dy.fi domain")
    elif re.match("badip [0-9.]+", req.text):
        logging.error("IP osoite on virheellinen tai ei suomalaisomisteinen.")
    elif re.match("dnserr", req.text):
        logging.error("Tekninen virhe dy.fi palvelimissa.")
    elif re.match("abuse", req.text):
        logging.error("Päivitys estetty väärinkäytön vuoksi.")

def get_ip():
    "Gets current ip using checkip service provided by dy.fy"
    req = requests.get("http://checkip.dy.fi/")
    regex = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    match = re.search(regex, req.text)
    return match.group(1)

def since_update(time):
    now = datetime.today()
    old = datetime.fromtimestamp(int(time))
    return (now - old).days

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
    config[hostname]["last_ip"] = "0.0.0.0"
    config[hostname]["updated"] = "0"
    save_config()

parser = argparse.ArgumentParser(description='dyfi updater')
parser.add_argument('--add', action='store_true', help='Add new dy.fi host.')
parser.add_argument('--edit', action='store_true', help='Edit config file.')
parser.add_argument('--info', action='store_true', help='Print info on hosts.')
parser.add_argument('-u', '--update', action='store_true', 
        help='Update all hosts that need updating')

args = parser.parse_args()
if args.add:
    add_host()
elif args.edit:
    editor = os.environ['EDITOR']
    ret = subprocess.call([editor, configname])
elif args.info:
    for host in config:
        if not host == "DEFAULT":
            print("[" + host + "]")
            print("Username:    ", config[host]["user"])
            print("Latest ip:   ", config[host]["last_ip"])
            print("Last updated:", since_update(config[host]["updated"]),
                  "days ago")
elif args.update:
    ip = get_ip()
    if len(config.sections()) > 0:
        for host in config:
            if host != 'DEFAULT':
                time_up = (config[host]["updated"] == "0" or 
                           since_update(config[host]["updated"]) > 5)
                ip_changed = config[host]["last_ip"] != ip
                if time_up or ip_changed:
                    update(config[host]["user"], config[host]["password"], host)
                    config[host]["updated"] = str(datetime.today().timestamp())
                    config[host]["last_ip"] = ip
                    save_config()
    else:
        logging.warning("No hosts found. Run \n\n" +
                        "  $ dyfi.py --add\n\nto add one of more configs")
        exit(1)
elif not os.path.exists(configname):
    print("Config file not found. Run \n\n" +
          "  $ dyfi.py --add\n\nto add one of more configs")
