import json
import time

from config import CONFIG

## Beginning of VCF block

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.network import NetworkManagementClient

LAB_STEP_VAR = 'Num_vpn_gateway_connections'
DEFAULT_VALUE = '2'

def handler(event, context):
    step_variables = event.get('step_variables',{})
    lab_step_variable = step_variables.get(LAB_STEP_VAR) or DEFAULT_VALUE
    num_vpn_gateway_connections = int(lab_step_variable)

    credentials, subscription_id = get_credentials(event)
    resource_group = event['environment_params']['resource_group']
    
    client = NetworkManagementClient(credentials, subscription_id)
    result = client.virtual_network_gateway_connections.list(resource_group)
    vpn_gateway_connections = [connection for connection in result if connection.connection_type == 'Vnet2Vnet']
    return len(vpn_gateway_connections) >= num_vpn_gateway_connections


def get_credentials(event):
    subscription_id = event['environment_params']['subscription_id']
    credentials = ServicePrincipalCredentials(
        client_id=event['credentials']['credential_id'],
        secret=event['credentials']['credential_key'],
        tenant=event['environment_params']['tenant']
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
    result = timed_handler(CONFIG, None)
    print(result)