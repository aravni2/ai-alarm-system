from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from az_key_vault import get_kv_secret
from datetime import datetime

# # Replace with your storage account name
# storage_account_name = get_kv_secret('adl-alarm-name')

# # Create a credential object
# credential = DefaultAzureCredential()

# # Create a DataLakeServiceClient object
# service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net", credential=credential)

# # Replace with your file system (container) name
# file_system_name = "captures"

# # Replace with your file path
# local_file_path = "test_file.jpg"
# remote_file_path = "incident_1_.jpg"

# # Create a FileSystemClient
# file_system_client = service_client.get_file_system_client(file_system=file_system_name)

# # Upload the file
# with open(local_file_path, "rb") as data:
#     file_client = file_system_client.get_file_client(remote_file_path)
#     file_client.upload_data(data, overwrite=True)

# print(f"File {local_file_path} uploaded to {file_system_name} as {remote_file_path}")

class data_lake:
    def __init__(self,adl_account = 'adlalarm', lcl_file_path = 'captures'):
        self.storage_account_name = adl_account
        self.local_file_path = lcl_file_path
        self.adl_container_name = 'captures'

        # Create a credential object
        self.credential = DefaultAzureCredential()

        # Create a DataLakeServiceClient object
        self.service_client = DataLakeServiceClient(account_url=f"https://{self.storage_account_name}.dfs.core.windows.net", credential=self.credential)
        
        # create file container client
        self.file_system_client = self.service_client.get_file_system_client(file_system=self.adl_container_name)

    def send_files(self,file_name):
        print(f'{self.local_file_path}/{file_name}')
        with open(f'{self.local_file_path}/{file_name}', "rb") as data:
            file_client = self.file_system_client.get_file_client(file_name)
            file_client.upload_data(data, overwrite=True)
        
        print(f"File {self.local_file_path} uploaded to {self.adl_container_name} as {file_name}")

if __name__ =='__main__':
    adl_account = get_kv_secret('adl-alarm-name')
    dl = data_lake(adl_account=adl_account,lcl_file_path = 'captures')

    dl.send_files('test_file.jpg')