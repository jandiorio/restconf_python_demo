#!/usr/bin/env python

"""
ospf.py
Author: Jeff Andiorio
Topic: Hands-on RESTConf Demo for ENAUTO
"""

import time
import yaml
from yaml import safe_dump
from restconf_api import (
    create_session,
    build_url,
    load_inventory,
    render_payload,
    put_request,
    save_config,
    get_request,
)


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


def main():
    """ main entry point of program """

    # "restconf/data/Cisco-IOS-XE-native:native/router/router-ospf"
    # "restconf/data/Cisco-IOS-XE-ospf-oper:ospf-oper-data/ospf-state"

    # 1. Load inventory
    inventory = load_inventory("inventory/hosts.yml")

    for device in inventory.keys():

        # 2. Map target rotuer
        router = inventory[device]

        # 3. Create Session
        session = create_session(router["username"], router["password"])

        # 4. Variable for ospf data
        ospf = router["ospf"]

        # 5. Render payload
        payload = render_payload(ospf, "ospf.j2")
        print(f"Configuring OSPF with the following data...\n{payload}")

        # 6. Make request
        endpoint = "restconf/data/Cisco-IOS-XE-native:native/router/router-ospf"
        result = put_request(router["host"], session, endpoint, payload)
        print(result)

    # sleep waiting for DR election and neighbor
    print("Waiting for neighbors...")
    time.sleep(60)

    # Loop through obtaining state
    for device in inventory.keys():

        # 7. Get State
        endpoint = "restconf/data/Cisco-IOS-XE-ospf-oper:ospf-oper-data/ospf-state"
        ospf_state = get_request(router["host"], session, endpoint)
        # print(ospf_state['Cisco-IOS-XE-ospf-oper:ospf-state'])
        with open("files/ospf_state_output.yml", "w") as file:
            file.write(yaml.safe_dump(ospf_state))

        # 8. Check the Routing Protocol
        endpoint = "restconf/data/ietf-routing:routing-state"
        routing_state = get_request(router["host"], session, endpoint)

        for route in routing_state['ietf-routing:routing-state']['routing-instance'][0]['ribs']['rib'][0]['routes']['route']:
            print(f"{route['destination-prefix']:40}{route['source-protocol']:40}")

        # 9. Save config
        saved = save_config(router["host"], session)
        print(saved)

if __name__ == "__main__":
    main()
