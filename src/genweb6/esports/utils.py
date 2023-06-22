# -*- coding: utf-8 -*-
from plone import api


def make_curl_request(url):
    import re
    import subprocess

    curl_command = f'curl {url}'
    process = subprocess.Popen(curl_command, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    # Read output and remove XML declaration line
    stdout = stdout.decode('ISO-8859-1')
    stdout = re.sub(r'^<\?xml.*\?>', '', stdout)

    stderr = stderr.decode('ISO-8859-1')
    print(f'Error: {stderr}')

    return stdout

def publish_object(obj):
    workflow_tool = api.portal.get_tool('portal_workflow')
    try:
        workflow_tool.doActionFor(obj, 'publish')
    except Exception:
        print(f'Unable to publish object with id: {obj.id}')

def query_catalog(portal_type):
    catalog = api.portal.get_tool('portal_catalog')
    params = {'portal_type': portal_type, 'review_state': 'published'}

    brains = catalog.searchResults(**params)
    return [brain.getObject() for brain in brains]

def get_list_from_string(string):
    try:
        return eval(string)
    except:
        return []
