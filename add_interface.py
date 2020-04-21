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
    get_request,
)


def main():
    """main entrypoint for program"""

    # endpdoint =  "restconf/data/ietf-interfaces:interfaces"
    # endpoint = f"restconf/data/ietf-interfaces:interfaces/interface={name}"

    # 1. load our inventory
    inventory = load_inventory("inventory/hosts.yml")

    # 2. map our target router
    router = inventory["r2"]
    print(router)

    # 3.  create a session
    session = create_session(router_1["username"], router_1["password"])

    # 4. create variable for loopback0 data
    loop0 = [
        interface
        for interface in router_1["interface"]
        if interface["name"] == "Loopback0"
    ][0]
    print(loop0)

    # 5.  Render the template
    payload = render_payload(loop0, "interface.j2")
    print(payload)

    # 6. create variable for the rest endpoint
    endpoint = f"restconf/data/ietf-interfaces:interfaces/interface=Loopback0"

    # 7. make the put request using helper function
    results = put_request(router_1["host"], session, endpoint, payload)
    print(results)

    # 8. Save our config - issues with save hanging...
    saved = save_config(router_1["host"], session)
    print(f"saved? {saved}")
    
    if saved:
        print("Successfully saved configuration...")
    else:
        print("Failed to save configuration...")

    # 9. Get Interface
    endpoint = "restconf/data/ietf-interfaces:interfaces/interface=Loopback0"
    interface_results = get_request(router_1["host"], session, endpoint)
    print(interface_results)
    # Save to file for reference
    with open("loopback0.yml", "w") as file:
        import yaml
        file.write(yaml.safe_dump(interface_results))


if __name__ == "__main__":
    main()
