#!/usr/bin/env python

"""
ospf.py
Author: Jeff Andiorio
Topic: Hands-on RESTConf Demo for ENAUTO
"""


import sys
import json
import urllib3
from jinja2 import Environment, FileSystemLoader
from os import path
from sys import argv
from yaml import safe_load, safe_dump
from restconf_api import create_session, build_url, load_inventory


def get_ospf_config(host, session, save_to_file=True):
    """ retreive the ospf config from the host"""

    endpoint = "restconf/data/Cisco-IOS-XE-native:native/router/router-ospf"
    _url = build_url(host, endpoint)
    results = session.get(_url)

    if save_to_file:
        ospf_config = safe_dump(results.json())
        with open(f"vars/{host['host']}_ospf.yml", "w") as file:
            file.write(ospf_config)

    return results


def create_ospf(host, session):
    """ configure ospf using RESTCONF """

    endpoint = "restconf/data/Cisco-IOS-XE-native:native/router/router-ospf"
    _url = build_url(host, endpoint)

    ospf = host['ospf']

    env = Environment(loader=FileSystemLoader("templates"),
                      lstrip_blocks=True,
                      trim_blocks=True,
                      autoescape=True)
    tmp = env.get_template("ospf.j2")
    payload = safe_load(tmp.render(ospf=ospf))

    results = session.put(_url, json=payload)
    # breakpoint()

    return results

def main():
    """ main entry point of program """
    if len(argv) > 1 and path.exists(argv[1]):
        inventory = load_inventory(argv[1])
    else:
        print("You must provide a valid path to your inventory...")
        sys.exit(1)

    for host_key, attribs in inventory.items():
        print(f"configuring ospf for {host_key}")
        # for host in inventory.items():
        # r1 = inventory.get("dev-r1")
        session = create_session(attribs)

        # ospf_config = get_ospf_config(r1,session)
        results = create_ospf(attribs, session)
        print(results)


if __name__=="__main__":
    main()