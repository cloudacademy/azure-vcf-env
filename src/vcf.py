import json
import time

from config import EVENT_CONFIG

## Beginning of VCF block

from azure.identity import ClientSecretCredential
from azure.mgmt.network import NetworkManagementClient

LAB_STEP_VAR = 'Num_private_endpoints'
DEFAULT_VALUE = '1'

def handler(event, context):
    step_variables = event.get('step_variables',{})
    lab_step_variable = step_variables.get(LAB_STEP_VAR) or DEFAULT_VALUE
    num_private_endpoints = int(lab_step_variable)

    credentials, subscription_id = get_credentials(event)
    resource_group = event['environment_params']['resource_group']
    
    client = NetworkManagementClient(credentials, subscription_id)
    private_endpoints = list(client.private_endpoints.list(resource_group))
    return len(private_endpoints) >= num_private_endpoints


def get_credentials(event):
    subscription_id = event['environment_params']['subscription_id']
    credentials = ClientSecretCredential(
        client_id=event['credentials']['credential_id'],
        client_secret=event['credentials']['credential_key'],
        tenant_id=event['environment_params']['tenant']
    )
    return credentials, subscription_id

## End of VCF block

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