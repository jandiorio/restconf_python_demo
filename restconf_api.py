#!/usr/bin/env python

"""
restconf_api.py
Author: Jeff Andiorio
Topic: Hands-on RESTConf Demo for ENAUTO
"""

from os import path
import requests
from yaml import safe_load
import urllib3
from jinja2 import Environment, FileSystemLoader

# disable all python requests warnings in our lab environment
urllib3.disable_warnings()


def load_inventory(inventory_path):
    """ loads inventory from a yml file"""

    if path.exists(inventory_path):
        print("loading inventory...")
        with open(inventory_path, "r") as file:
            inventory = safe_load(file.read())
            print("Inventory successfully loaded...")
    else:
        raise FileExistsError("Inventory file doesn't exist.")

    return inventory


def create_session(username, password):
    """ create session for requests calls """

    # Create headers for our requests
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    auth = (username, password)

    print("Creating Session Object...")

    session = requests.session()
    session.auth = auth
    session.verify = False
    session.headers = headers

    return session


def build_url(host, endpoint):
    """ build the restconf url """

    print("Building _url...")
    base_url = f"https://{host}/"

    _url = f"{base_url}{endpoint}"

    return _url


def get_request(host, session, endpoint):
    """ generic get function """

    _url = build_url(host, endpoint)

    results = session.get(_url)

    return results.json()


def post_request(host, session, endpoint, payload):
    """ basic post request """

    _url = build_url(host, endpoint)

    print("Making POST request...")
    results = session.post(_url, json=payload)

    return results


def put_request(host, session, endpoint, payload):
    """ generic put function """

    _url = build_url(host, endpoint)

    print("Making request...")
    results = session.put(_url, json=payload)

    return results


def delete_request(host, session, endpoint):
    """ generic delete function """

    _url = build_url(host, endpoint)

    print("Making request...")
    results = session.delete(_url)

    return results

def render_payload(data, template_name, template_path="templates/"):
    """
    render payload from a template
    Params:
      data (dict) - dictionary of values to populate the template
      template_name (str) - name of the template
      tempmlate_path (str) - path to the templates (used in jinja Environment)
    """

    print("Rendering payload...")

    env = Environment(
        loader=FileSystemLoader(template_path),
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True,
    )

    tmp = env.get_template(template_name)

    payload = safe_load(tmp.render(data=data))

    return payload


def save_config(host, session):
    """ convenience method for saving config """

    payload = {}
    endpoint = "restconf/operations/cisco-ia:save-config/"
    results = post_request(host, session, endpoint, payload)

    return bool(results.ok)
