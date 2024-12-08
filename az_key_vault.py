# Import necessary libraries
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# # Replace with your Key Vault URL
# key_vault_url = "https://kv-alarm-codes.vault.azure.net//"

# # Create a credential object
# credential = DefaultAzureCredential()

# # Create a SecretClient object
# secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

# # Replace with your secret name
# secret_name = "adl-alarm-secret"

# # Retrieve the secret
# retrieved_secret = secret_client.get_secret(secret_name)

# # Print the secret value
# print(f"Secret Value: {retrieved_secret.value}")

def get_kv_secret(kv_name):
    key_vault_url = "https://kv-alarm-codes.vault.azure.net/"
    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
    secret_name = kv_name
    retrieved_secret = secret_client.get_secret(secret_name)

    return retrieved_secret.value


if __name__ == '__main__':
    print(get_kv_secret('adl-alarm-secret'))