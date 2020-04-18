#!/usr/bin/env python

"""
restconf_api.py
Author: Jeff Andiorio
Topic: Hands-on RESTConf Demo for ENAUTO
"""

import requests
import sys
import yaml
from yaml import safe_load
from os import path
from sys import argv
import json
import urllib3

# disable all python requests warnings in our lab environment
urllib3.disable_warnings()


def create_session(host):
    """ create session for requests calls """

    # Create headers for our requests
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    auth = (host["username"], host["password"])

    print("Creating Session Object...")

    session = requests.session()
    session.auth = auth
    session.verify = False
    session.headers = headers

    return session


def build_url(host, endpoint):
    """ build the restconf url """

    if host.get("host"):
        base_url = f"https://{host.get('host')}/"
    else:
        raise ValueError("Host Key Not Defined in Inventory")

    _url = f"{base_url}{endpoint}"

    return _url


def load_inventory(inventory_path):
    """ loads inventory from a yml file"""

    global inventory

    if path.exists(inventory_path):
        print("loading inventory...")
        with open(inventory_path, "r") as file:
            inventory = safe_load(file.read())
            print("Inventory successfully loaded...")
    else:
        raise FileExistsError("Inventory file doesn't exist.")

    return inventory
