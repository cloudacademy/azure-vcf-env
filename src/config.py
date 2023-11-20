import os

CONFIG = {
    'credentials': {
        'credential_id' : os.environ.get('AZURE_CLIENT_ID'),
        'credential_key': os.environ.get('AZURE_CLIENT_SECRET')
    },
    'environment_params': {
        'subscription_id': os.environ.get('AZURE_SUBSCRIPTION_ID'),
        'tenant'         : os.environ.get('AZURE_TENANT_ID'),
        'resource_group' : os.environ.get('AZURE_RESOURCE_GROUP')
    }
}