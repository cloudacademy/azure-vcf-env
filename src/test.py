import time

from config import EVENT_CONFIG

# Beginning of VCF block
from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient 
from datetime import datetime, timedelta

def handler(event, context):
    credentials, subscription_id = get_credentials(event)
    resource_group = event['environment_params']['resource_group']
    client = LogsQueryClient(credentials)
    la_client = LogAnalyticsManagementClient(credentials, subscription_id)

    try:
        #something
        d_date = datetime.now()
        N = 1
        date_N_days_ago = d_date - timedelta(days=N)
        la_client_res = list(la_client.workspaces.list_by_resource_group(resource_group))
        query = """LAQueryLogs"""
        if any(la_client_res) and la_client_res:
            results = client.query_workspace(la_client_res[0].customer_id, query, timespan=(date_N_days_ago, d_date)).tables
            return True
    except:
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
