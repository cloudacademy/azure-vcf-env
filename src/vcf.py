from distutils.command.config import config
from importlib.resources import Resource
import resource
import time

from pkg_resources import resource_stream

from config import CONFIG

# Beginning of VCF block
from azure.identity import ClientSecretCredential
from azure.mgmt.appcontainers import ContainerAppsAPIClient

def handler(event, context):
    credentials, subscription_id = get_credentials(event)
    resource_group = event['environment_params']['resource_group']
    resource_client = ContainerAppsAPIClient(credentials, subscription_id)

    try:
        resources = list(resource_client.container_apps.list_by_resource_group(resource_group))
        ingress_set = resources[0].configuration.ingress.target_port == 8000
        reg_config = resources[0].configuration.registries
        return ingress_set and len(reg_config) > 0
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
    result = timed_handler(CONFIG, None)
    print(result)
