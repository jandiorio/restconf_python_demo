#!/usr/bin/env python

"""
interface.py
Author: Jeff Andiorio
Topic: Hands-on RESTConf Demo for ENAUTO
"""


import sys
from jinja2 import Environment, FileSystemLoader
from os import path
from sys import argv
from yaml import safe_load
import urllib3
from restconf_api import create_session, build_url, load_inventory


# disable all python requests warnings in our lab environment
urllib3.disable_warnings()

# define global vars
INVENTORY = None
SESSION = None


def get_interfaces(host, session):
    """use restconf to obtain the interfaces currently configured"""

    endpoint = "restconf/data/ietf-interfaces:interfaces"

    # build_url
    interfaces_url = build_url(host, endpoint)

    results = session.get(interfaces_url)

    return results.json()


def update_interfaces(host, session):
    """ create or configure a new interface """

    endpoint = "restconf/data/ietf-interfaces:interfaces/interface"

    _url = build_url(host, endpoint)

    # with open("vars/interfaces.yml", "r") as file:
    #     data = safe_load(file.read())

    env = Environment(loader=FileSystemLoader("templates/"),
                      trim_blocks=True,
                      lstrip_blocks=True,
                      autoescape=True
                      )
    tmp = env.get_template("interface.j2")

    payload = safe_load(tmp.render(interfaces=host['interface']))
    print(payload)
    results = session.patch(_url, json=payload)

    return results


def main():
    """main entrypoint for program"""

    if len(argv) > 1:
        try:
            inventory = load_inventory(argv[1])
        except FileExistsError as err:
            print("FileExistsError: ", err)
    else:
        print("You must provide a path to your inventory file.")
        sys.exit()

    for host_key, attribs in inventory.items():
        print(f"configuring interfaces on {host_key}")

        # create a session imported from restconf_api
        session = create_session(attribs)

        # get all interfaces
        results = get_interfaces(attribs, session)
        interfaces = results["ietf-interfaces:interfaces"]["interface"]

        # convert to yaml
        # yaml_output = yaml.safe_dump(results)
        # with open("vars/interfaces.yml", "w") as file:
        #     file.write(yaml_output)

        results = update_interfaces(attribs, session)
        print(results.text, results.status_code)
        
        # print(get_interfaces(attribs, session))


if __name__ == "__main__":
    main()
