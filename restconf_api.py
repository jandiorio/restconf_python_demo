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
    """
    loads inventory from a YAML file

    :param tempmlate_path: A string path to the templates (used in jinja Environment)
    """

    if path.exists(inventory_path):
        print("loading inventory...")
        with open(inventory_path, "r") as file:
            inventory = safe_load(file.read())
            print("Inventory successfully loaded...")
    else:
        raise FileExistsError("Inventory file doesn't exist.")

    return inventory


def create_session(username, password):
    """
    create :class:`Session` object for requests calls

    :param username: A string username for authentication
    :param password: A string password for authentication

    """

    # Create headers for our requests
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    # auth = (username, password)

    print("Creating Session Object...")

    session = requests.session()
    session.auth = (username, password)
    session.verify = False
    session.headers = headers

    return session


def build_url(host, endpoint):
    """
    build the restconf url

    :param host: A string of the REST API endpoint
    :param endpoint: A string of either DNS name or IP address of target host

    """

    print("Building _url...")
    base_url = f"https://{host}/"

    _url = f"{base_url}{endpoint}"

    return _url


def get_request(host, session, endpoint):
    """
    generic get function

    :param host: A string of the REST API endpoint
    :param session: A :class:`Session` object
    :param endpoint: A string of either DNS name or IP address of target host

    """

    _url = build_url(host, endpoint)

    results = session.get(_url)

    if results.ok:
        return results.json()
    else:
        print(f'GET request failed...{results.text}')


def post_request(host, session, endpoint, payload):
    """
    basic post request

    :param host: A string of the REST API endpoint
    :param session: A :class:`Session` object
    :param endpoint: A string of either DNS name or IP address of target host
    :param payload: A dictionary for the request body

    """

    _url = build_url(host, endpoint)

    print(f"Making POST request to {endpoint}...")
    results = session.post(_url, json=payload)

    return results


def put_request(host, session, endpoint, payload):
    """
    generic put function

    :param host: A string of the REST API endpoint
    :param session: A :class:`Session` object
    :param endpoint: A string of either DNS name or IP address of target host
    :param payload: A dictionary for the request body
    """

    _url = build_url(host, endpoint)

    print(f"Making PUT request to {endpoint}...")
    results = session.put(_url, json=payload)

    return results


def delete_request(host, session, endpoint):
    """
    generic delete function

    :param host: A string of the REST API endpoint
    :param session: A :class:`Session` object
    :param endpoint: A string of either DNS name or IP address of target host

    """

    _url = build_url(host, endpoint)

    print(f"Making DELETE request to {endpoint}...")
    results = session.delete(_url)

    return results


def render_payload(data, template_name, template_path="templates/"):
    """
    render payload from a template

    :param data: (dict) - A dictionary of values to populate the template
    :param template_name: A string name of the template
    :param tempmlate_path: A string path to the templates (used in jinja Environment)
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
    """
    convenience method for saving config on ios-xe devices

    :param host: A string of the REST API endpoint
    :param session: A :class:`Session` object
    """

    payload = {}
    endpoint = "restconf/operations/cisco-ia:save-config/"
    results = post_request(host, session, endpoint, payload)

    return bool(results.ok)
