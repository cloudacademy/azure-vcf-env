from distutils.command.config import config
from importlib.resources import Resource
import resource
import time

from pkg_resources import resource_stream

from config import EVENT_CONFIG

# Beginning of VCF block

from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient

def with_hint(result, hint=None):
    return {'result': result, 'hint_message': hint} if hint else result

def handler(event, context):
    credentials, subscription_id = get_credentials(event)
    resource_group = event['environment_params']['resource_group']    
    resource_client = ResourceManagementClient(credentials, subscription_id)

    try:
        bot_resource = list(resource_client.resources.list_by_resource_group(resource_group, filter="resourceType eq 'Microsoft.BotService/botServices'"))
        if bot_resource:
            return with_hint(True, 'Found bot resource.')
        else:
            return with_hint(False, 'Could not find any bot resource.')
    except:
        return with_hint(False, 'Could not find relevant resource.')

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
