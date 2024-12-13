from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.storage.filedatalake import DataLakeServiceClient
import os

class az_blobs:
    def __init__(self,adl_account = 'adlalarmdata', lcl_file_path = 'captures'):
        self.storage_account_name = adl_account
        self.local_file_path = lcl_file_path
        self.adl_container_name = 'captures'

        # Create a credential object
        self.credential = DefaultAzureCredential()

        # Create a DataLakeServiceClient object
        self.service_client = DataLakeServiceClient(account_url=f"https://{self.storage_account_name}.dfs.core.windows.net", credential=self.credential)
        
        # create file container client
        self.file_system_client = self.service_client.get_file_system_client(file_system=self.adl_container_name)

        # Create the BlobServiceClient object
        # self.blob_service = BlockBlobService(account_url=f"https://{self.storage_account_name}.dfs.core.windows.net", credential=self.credential)
        self.blob_service_client = BlobServiceClient(account_url=f"https://{self.storage_account_name}.blob.core.windows.net", credential=self.credential)
        self.container_client = self.blob_service_client.get_container_client(container=self.adl_container_name)

    def send_files(self,file_name):
        print(f'{self.local_file_path}/{file_name}')
        with open(f'{self.local_file_path}/{file_name}', "rb") as data:
            file_client = self.file_system_client.get_file_client(file_name)
            file_client.upload_data(data, overwrite=True)

    def download_known_faces(self):
        # retrieve container name
        

        # list blobs in knownFaces hierarchy
        blob_list = self.container_client.list_blobs(name_starts_with='knownFaces/')

        for blob in blob_list:
            blob_path = blob.name.split('/')

            # get correct hierarchy
            if len(blob_path)==3:

                # get breakouts of blob
                blob_folder = blob_path[1]
                blob_name = blob_path[2]
                blob_client = self.container_client.get_blob_client(blob.name)
                
                print(f"Name: {blob.name}", blob_path, blob_folder,blob_name)

                # create local folder if it doesn't exist
                if not os.path.exists( 'known_faces/' + blob_folder):
                    os.makedirs('known_faces/'+blob_folder)
                
                # download and stream blob to local file
                with open(f'known_faces/{blob_folder}/{blob_name}', mode="wb") as sample_blob:
                    download_stream = blob_client.download_blob()
                    sample_blob.write(download_stream.readall())
        
        # print(f"File {self.local_file_path} uploaded to {self.adl_container_name} as {file_name}")
    
    def upload_known_faces(self):
        for dirpath, dirnames, filenames in os.walk('known_faces'):
            # print(f"Directory: {dirpath}")
            # for dirname in dirnames:
            #     print(f"Subfolder: {os.path.join(dirpath, dirname)}")
            for filename in filenames:
                print(f"{os.path.join(dirpath, filename)}")
                folder = dirpath.split('\\')[-1]
                # print(folder,filename)
                with open(f'known_faces/{folder}/{filename}', mode="rb") as fh:
                    blob_client = self.container_client.upload_blob(name=f'{folder}/{filename}', data=fh, overwrite=True)
                    
                



if __name__ == '__main__':
    blob = az_blobs()

    blob.upload_known_faces()

    blob.send_files('20241210-000623_.png')

