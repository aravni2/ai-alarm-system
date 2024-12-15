# Import necessary libraries
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Ghosananda Wijaya and Anthony Ravnic 
# CS437
# 2024.10.12
#
# Description:
    # OPTIONAL IF CLOUD STORAGE IS SET UP
    # 
    # This is a simple function to retrieve keyvault secrets from azure key vault. One must first authenticate with azure via MFA, then they can use this module
    # to retrieve both the storage account name, and secret (this obscures both name and key, allowing for an additional layer of safety)


def get_kv_secret(kv_name):
    key_vault_url = "https://kv-alarm-codes.vault.azure.net/"
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
    secret_name = kv_name
    retrieved_secret = secret_client.get_secret(secret_name)

    return retrieved_secret.value


if __name__ == '__main__':
    print(get_kv_secret('adl-alarm-secret'))