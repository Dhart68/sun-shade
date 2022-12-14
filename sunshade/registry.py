from google.cloud import storage
import pandas as pd

def save_local(name:str,data:pd.DataFrame):
    '''Save a Dataframe to a csv file'''
    data.to_csv(f'data/{name}.csv')
    print(f"The data {name} has been saved to csv")



def save_cloud(source_file_name, destination_blob_name,bucket_name="sunshade_data_bucket"):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"


    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
