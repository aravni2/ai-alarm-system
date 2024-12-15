from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from az_key_vault import get_kv_secret
from datetime import datetime
from azure.storage.blob import BlobServiceClient
import os
# Ghosananda Wijaya and Anthony Ravnic 
# CS437
# 2024.10.12
#
# Description:
    # This Class deals with using authetication through azure to upload and download known faces, a pull/push process to make sure local known faces are synced
    # with the cloud. it also has some functions that allow it to send captured images (when alarm goes off) to the cloud

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
                
                print('download blob floder:',blob_folder)
                # print(f"Name: {blob.name}", blob_path, blob_folder,blob_name)

                # create local folder if it doesn't exist
                if not os.path.exists( 'known_faces/' + blob_folder):
                    os.makedirs('known_faces/'+blob_folder)
                
                # download and stream blob to local file
                with open(f'known_faces/{blob_folder}/{blob_name}', mode="wb") as sample_blob:
                    download_stream = blob_client.download_blob()
                    sample_blob.write(download_stream.readall())
                    print('downloaded to:', f'known_faces/{blob_folder}/{blob_name}')
        
        # print(f"File {self.local_file_path} uploaded to {self.adl_container_name} as {file_name}")
    
    def upload_known_faces(self):
        for dirpath, dirnames, filenames in os.walk('known_faces'):
            
            # print(f"Directory: {dirpath}")
            # for dirname in dirnames:
            #     print(f"Subfolder: {os.path.join(dirpath, dirname)}")
            for filename in filenames:
                print(f"first - {os.path.join(dirpath, filename)}")
                # folder = dirpath.split('\\')[-1]   #windows version  MUST CHANGE WHEN USING DEMO
                folder = dirpath.split('/')[-1]  #linux version
                print(folder,filename)
                with open(f'known_faces/{folder}/{filename}', mode="rb") as fh:
                    blob_client = self.container_client.upload_blob(name=f'knownFaces/{folder}/{filename}', data=fh, overwrite=True)
    def pull_push_known_faces(self):
        self.download_known_faces()
        self.upload_known_faces()
    



if __name__ =='__main__':
    adl_account = get_kv_secret('adl-alarm-name')
    dl = data_lake(adl_account=adl_account,lcl_file_path = 'captures')
    dl.pull_push_known_faces()
    dl.send_files('test_file.jpg')