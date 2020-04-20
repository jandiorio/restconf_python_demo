#!/usr/bin/env python

"""
ospf.py
Author: Jeff Andiorio
Topic: Hands-on RESTConf Demo for ENAUTO
"""

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

    # 2. Map target rotuer
    router_1 = inventory["r1"]

    # 3. Create Session
    session = create_session(router_1["username"], router_1["password"])

    # 4. Variable for ospf data
    ospf = router_1["ospf"]

    # 5. Render payload
    payload = render_payload(ospf, "ospf.j2")
    print("configuring ospf with the following data...")
    print(payload)

    # 6. Make request
    endpoint = "restconf/data/Cisco-IOS-XE-native:native/router/router-ospf"
    result = put_request(router_1["host"], session, endpoint, payload)
    print(result)

    # 7. Save config
    saved = save_config(router_1["host"], session)
    print(saved)

    # 8. Get State
    from pprint import pprint
    import yaml
    endpoint = "restconf/data/Cisco-IOS-XE-ospf-oper:ospf-oper-data/ospf-state"
    ospf_state = get_request(router_1["host"], session, endpoint)
    # print(ospf_state['Cisco-IOS-XE-ospf-oper:ospf-state'])
    with open('state_output.yml', 'w') as file:
        file.write(yaml.safe_dump(ospf_state))

    # 9. Check the Routing Protocol
    endpoint = "restconf/data/ietf-routing:routing-state"
    routing_state = get_request(router_1["host"], session, endpoint)
    # pprint(routing_state)
    for route in routing_state['ietf-routing:routing-state']['routing-instance'][0]['ribs']['rib'][0]['routes']['route']:
        print(f"{route['destination-prefix']:40}{route['source-protocol']:40}")

    #     # breakpoint()

if __name__ == "__main__":
    main()
