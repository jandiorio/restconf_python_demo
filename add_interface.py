#!/usr/bin/env python

"""
add_interface.py
Author: Jeff Andiorio
Topic: Hands-on RESTConf Demo for ENAUTO
"""


import yaml
from restconf_api import (
    create_session,
    load_inventory,
    render_payload,
    put_request,
    save_config,
    get_request,
)


def main():
    """main entrypoint for program"""

    # endpdoint =  "restconf/data/ietf-interfaces:interfaces"
    # endpoint = f"restconf/data/ietf-interfaces:interfaces/interface={name}"

    # 1. load our inventory
    inventory = load_inventory("inventory/hosts.yml")

    # Loop through the devices in our inventory (simple example)
    for device in inventory.keys():

        # 2. map our target router
        router = inventory[device]
        print(router)

        # 3.  create a session
        session = create_session(router["username"], router["password"])

        # 4. create variable for loopback0 data
        loop0 = [
            interface
            for interface in router["interface"]
            if interface["name"] == "Loopback0"
        ][0]
        print(loop0)

        # 5.  Build the Payload
        #     You can either model your data to match the YANG model or use a
        #     template.
        # payload = render_payload(loop0, "interface.j2")
        payload = dict({"ietf-interfaces:interface:": loop0})
        print(payload)

        # 6. create variable for the rest endpoint
        #    note: the payload was a single interface in the data not a list.
        #    you can use a list to update more than one interface but must use
        #    the `patch` method
        endpoint = f"restconf/data/ietf-interfaces:interfaces/interface=Loopback0"

        # 7. make the put request using helper function
        results = put_request(router["host"], session, endpoint, payload)
        print(results)

        # 8. Save our config - issues with save hanging...
        saved = save_config(router["host"], session)

        if saved:
            print("Successfully saved configuration...")
        else:
            print("Failed to save configuration...")

        # 9. Get Interface
        endpoint = "restconf/data/ietf-interfaces:interfaces/interface=Loopback0"
        interface_results = get_request(router["host"], session, endpoint)

        # Save to file for reference
        with open(f"files/{router['host']}_loopback0.yml", "w") as file:

            file.write(yaml.safe_dump(interface_results))


if __name__ == "__main__":
    main()
