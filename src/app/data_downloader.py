from boto3 import Session
import os
from dotenv import load_dotenv

class DataDownloader:
    def __init__(self):
        load_dotenv()
        self.session = Session(
            aws_access_key_id=os.getenv('RUSTFS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('RUSTFS_SECRET_KEY'),
            region_name=os.getenv('RUSTFS_REGION')
        )
        self.s3 = self.session.resource('s3', endpoint_url=f"http://{os.getenv('RUSTFS_ENDPOINT')}", use_ssl=os.getenv('RUSTFS_USE_HTTPS').lower() == 'true')

    def download_file(self, bucket_name, object_key, local_path):
        try:
            bucket = self.s3.Bucket(bucket_name)
            bucket.download_file(object_key, local_path)
            print(f"File downloaded successfully to {local_path}")
        except Exception as e:
            print(f"Error downloading file: {e}")