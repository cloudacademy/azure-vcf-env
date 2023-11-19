from dotenv import load_dotenv
load_dotenv() 

import time
from config import CONFIG
import vcf

class credential_helper:
    @staticmethod
    def get_credentials(event):
        from azure.identity import DefaultAzureCredential
        import logging
        logger = logging.getLogger('azure.identity')
        logger.setLevel(logging.CRITICAL)
        subscription_id = CONFIG['environment_params']['subscription_id']
        credentials = DefaultAzureCredential(exclude_interactive_browser_credential=True, exclude_shared_token_cache_credential=True, exclude_visual_studio_code_credential=True, exclude_managed_identity_credential=True, exclude_shared_ms_i_credential=True, exclude_azure_arc_credential=True)
        return credentials, subscription_id

vcf.get_credentials = credential_helper.get_credentials

def timed_handler(event, context):
    start = time.time()
    result = vcf.handler(event, context)
    end = time.time()
    print(end - start)
    return result

def entry():
    if not CONFIG['environment_params']['resource_group']:
        print('Resource group not found in AZURE_RESOURCE_GROUP environment variable. Attempting to retrieve from az config get defaults.group.')
        import subprocess, sys
        res = subprocess.run(["az", "config", "get", "defaults.group", "--query", "value", "-o", "tsv"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
        if res.returncode == 0:
            resource_group = res.stdout.decode('utf-8').strip('\n')
            print(f"Using resource group {resource_group} from az config get defaults.group")
            CONFIG['environment_params']['resource_group'] = resource_group
        else:
            print('Resource group not found in AZURE_RESOURCE_GROUP environment variable and not set with az config set defaults.group. Attempting to continue...', file=sys.stderr)
    if not CONFIG['environment_params']['subscription_id']:
        print('Subscription ID not found in AZURE_SUBSCRIPTION_ID environment variable. Attempting to retrieve from az account show.')
        import subprocess, sys
        res = subprocess.run(["az", "account", "show", "--query", "id", "-o", "tsv"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
        if res.returncode == 0:
            subscription_id = res.stdout.decode('utf-8').strip('\n')
            print(f"Using Subscription ID {subscription_id} from az account show")
            CONFIG['environment_params']['subscription_id'] = subscription_id
        else:
            print('Subscription ID not found in AZURE_SUBSCRIPTION_ID environment variable and not set in az account show. Attempting to continue...', file=sys.stderr)
    result = timed_handler(CONFIG, None)
    print(result)

if __name__ == "__main__":
    entry()
