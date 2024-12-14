from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
# ////////CONNECTION STRING VERSION///////////////////


# Replace with your connection string
connection_string = "your_connection_string"

# Replace with your container name
container_name = "your_container_name"

# Replace with your file path
local_file_path = "path/to/your/local/file.txt"
blob_name = "your_blob_name_in_datalake.txt"

# Create a BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Create a ContainerClient
container_client = blob_service_client.get_container_client(container_name)

# Upload the file to the container
with open(local_file_path, "rb") as data:
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(data, overwrite=True)

print(f"File {local_file_path} uploaded to {container_name} container as {blob_name}")
