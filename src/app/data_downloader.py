from boto3 import Session
import os
from dotenv import load_dotenv
from pathlib import Path
from .utils.data_details import get_data_details


class DataDownloader:
    def __init__(self):
        load_dotenv()
        self.session = Session(
            aws_access_key_id=os.getenv('RUSTFS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('RUSTFS_SECRET_KEY'),
            region_name=os.getenv('RUSTFS_REGION'),
        )

        self.s3 = self.session.resource(
            's3',
            endpoint_url=f"http://{os.getenv('RUSTFS_ENDPOINT')}",
            use_ssl=os.getenv('RUSTFS_USE_HTTPS', 'true').lower() == 'true',
        )

    def download_file(self):
        data_details = get_data_details()
        bucket_name = data_details.bucket
        object_key = data_details.source
        local_path = data_details.destination / data_details.file_name

        try:
            s3 = self.s3
            # ensure directory exists
            Path(local_path).parent.mkdir(parents=True, exist_ok=True)
            bucket = s3.Bucket(bucket_name)
            print("Bucket:", bucket_name)
            print("Object key:", object_key)
            print("Local path:", local_path)
            bucket.download_file(object_key, str(local_path))
            print(f"✅ File downloaded successfully to {local_path}")

        except Exception as e:
            print(f"❌ Error downloading file: {e}")


if __name__ == "__main__":
    downloader = DataDownloader()
    downloader.download_file()