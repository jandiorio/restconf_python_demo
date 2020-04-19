#!/usr/bin/env python

"""
interface.py
Author: Jeff Andiorio
Topic: Hands-on RESTConf Demo for ENAUTO
"""


import sys
import json
from jinja2 import Environment, FileSystemLoader
from os import path
from sys import argv
from yaml import safe_load
import urllib3
from restconf_api import create_session, build_url, load_inventory, render_payload, get_request, put_request, save_config


# disable all python requests warnings in our lab environment
urllib3.disable_warnings()

def main():
    """main entrypoint for program"""

    # endpdoint =  "restconf/data/ietf-interfaces:interfaces"
    # endpoint = f"restconf/data/ietf-interfaces:interfaces/interface={name}"

    if len(argv) > 1:
        try:
            inventory = load_inventory(argv[1])
        except FileExistsError as err:
            print("FileExistsError: ", err)
    else:
        print("You must provide a path to your inventory file.")
        sys.exit()

    r1 = inventory['dev-r1']
    loop = [interface for interface in r1["interface"] if interface["name"] == "Loopback0"][0]

    payload = render_payload(
            loop,
            "interface.j2"
            )

    session = create_session(r1["username"], r1["password"])
    endpoint = f"restconf/data/ietf-interfaces:interfaces/interface=Loopback0"
    results = put_request(r1["host"],session, endpoint, payload)
    print(results)

    save_endpoint = "restconf/operations/cisco-ia:save-config/"
    saved = save_config(r1["host"], session, save_endpoint)

    # target_routers = ["dev-r1"]

    # for host_key, attribs in inventory.items():

    #     if host_key in target_routers:
    #         print(f"configuring interfaces on {host_key}")

    #         # create a session imported from restconf_api
    #         session = create_session(attribs)

    #         # get all interfaces
    #         results = get_interface(attribs, session, "Loopback0")

    #         interface = results["ietf-interfaces:interface"]

    #         print(json.dumps(interface))
    #         # convert to yaml
    #         # yaml_output = yaml.safe_dump(results)
    #         # with open("vars/interfaces.yml", "w") as file:
    #         #     file.write(yaml_output)

    #         # results = update_interfaces(attribs, session)
    #         # print(results.text, results.status_code)

    #         # print(get_interfaces(attribs, session))


if __name__ == "__main__":
    main()
