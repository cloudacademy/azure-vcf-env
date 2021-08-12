# azure-vcf-env

Environment for working with Azure VCFs

## Getting started

1. Ensure Python 3.8+ is installed on your system

1. Create an Azure Active Directory application (or request on be created)

1. Create a secret for the application

1. Create a resource group

1. Assign the application to the _Contributor_ or _Reader_ role on the resource group (Request permission if you are not authorized to assign roles on the resource group)

1. In `.vscode/launch.json` fill in the `AZURE_CLIENT_ID` and `AZURE_CLIENT_SECRET` for the VCF user. Be sure to escape the JSON. Avoid using online tools to do this due to the sensitive nature of what you are escaping. The resulting `env` map will resemble:
    ```json
    {
        "AZURE_SUBSCRIPTION_ID": "12345678-1234-1234-1234-123456789012",
        "AZURE_CLIENT_ID": "abcdefab-abcd-abcd-abcd-abcdefabcdef",
        "AZURE_CLIENT_SECRET": "AL8)RxYQzCf./dF!y5EN13eqdg3T!qwh",
        "AZURE_TENANT_ID": "1234abcd-1234-1234-1234-1234abcd1234",
        "AZURE_RESOURCE_GROUP": "your-resource-group"
    }
    ```

1. In `init.sh` (Mac/Linux)/`init.ps1` (Windows) replace YOUR_BITBUCKET_USER with the name of your Cloud Academy BitBucket user

1. Run `init.sh` (Mac/Linux)/`init.ps1` (Windows) to set up the environment

    - Enter your Cloud Academy BitBucket password/[app password](https://confluence.atlassian.com/bitbucket/app-passwords-828781300.html) when prompted.

1. Add the following line to `.gitignore` to avoid committing any sensitive information:

    ```
    .vscode/
    ```

1. Develop and debug functions using the `Current File (Integrated Terminal)` configuration (press F5 with the file open)

## Update Dependencies

1. Run `init.sh` (Mac/Linux)/`init.ps1` (Windows) to set up the virtual environment again. (only the `venv/` directory is impacted by this operation)

## References

- [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python/tree/master/sdk) (Unit test code in particular)
