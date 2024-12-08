from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from az_key_vault import get_kv_secret

# Replace with your storage account name
storage_account_name = get_kv_secret('adl-alarm-name')

# Create a credential object
credential = DefaultAzureCredential()

# Create a DataLakeServiceClient object
service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net", credential=credential)

# Replace with your file system (container) name
file_system_name = "captures"

# Replace with your file path
local_file_path = "test_file.jpg"
remote_file_path = "incident_1_.jpg"

# Create a FileSystemClient
file_system_client = service_client.get_file_system_client(file_system=file_system_name)

# Upload the file
with open(local_file_path, "rb") as data:
    file_client = file_system_client.get_file_client(remote_file_path)
    file_client.upload_data(data, overwrite=True)

print(f"File {local_file_path} uploaded to {file_system_name} as {remote_file_path}")
