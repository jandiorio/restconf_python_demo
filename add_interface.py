#!/usr/bin/env python

"""
add_interface.py
Author: Jeff Andiorio
Topic: Hands-on RESTConf Demo for ENAUTO
"""


from restconf_api import (
    create_session,
    load_inventory,
    render_payload,
    put_request,
    save_config,
)


def main():
    """main entrypoint for program"""

    # endpdoint =  "restconf/data/ietf-interfaces:interfaces"
    # endpoint = f"restconf/data/ietf-interfaces:interfaces/interface={name}"

    # 1. load our inventory
    inventory = load_inventory("inventory/hosts.yml")

    # 2. map our target router
    router_1 = inventory["dev-r1"]

    # 3.  create a session
    session = create_session(router_1["username"], router_1["password"])

    # 4. create variable for loopback0 data
    loop0 = [
        interface for interface in router_1["interface"] if interface["name"] == "Loopback0"
    ][0]

    # 5.  Render the template
    payload = render_payload(loop0, "interface.j2")

    # 6. create variable for the rest endpoint
    endpoint = f"restconf/data/ietf-interfaces:interfaces/interface=Loopback0"

    # 7. make the put request using helper function
    results = put_request(router_1["host"], session, endpoint, payload)
    print(results)

    # 8. Save our config
    saved = save_config(router_1["host"], session)

    if saved:
        print("Successfully saved configuration...")
    else:
        print("Failed to save configuration...")

if __name__ == "__main__":
    main()
