import json
import time

import urllib3

from config import EVENT_CONFIG

# Beginning of VCF block
from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient
from urllib import request

def handler(event, context):
    credentials, subscription_id = get_credentials(event)
    resource_group = event['environment_params']['resource_group']
    client = NetworkManagementClient(credentials, subscription_id)


    try: 
        ws = list(client.public_ip_addresses.list(resource_group))[0].ip_address
        f = request.urlopen("http://"+ws, timeout=10)
        return f.getcode() == 200
    except Exception as e:
        return False

def get_credentials(event):
    subscription_id = event['environment_params']['subscription_id']
    credentials = ClientSecretCredential(
        client_id=event['credentials']['credential_id'],
        client_secret=event['credentials']['credential_key'],
        tenant_id=event['environment_params']['tenant']
    )
    return credentials, subscription_id
# End of VCF block


def print_iter(iterable):
    for item in iterable:
        print(item)


def timed_handler(event, context):
    start = time.time()

    result = handler(event, context)

    end = time.time()
    print(end - start)

    return result


if __name__ == "__main__":
    result = timed_handler(EVENT_CONFIG, None)
    print(result)
