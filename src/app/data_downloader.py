from boto3 import Session
import os
from dotenv import load_dotenv
from pathlib import Path
from .utils.data_details import get_data_details
from src.app.utils.logger import Logger

logger = Logger.get_logger(__file__)

class DataDownloader:
    def __init__(self):
        load_dotenv()
        logger.info("Initializing DataDownloader with environment variables.")
        self.session = Session(
            aws_access_key_id=os.getenv('RUSTFS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('RUSTFS_SECRET_KEY'),
            region_name=os.getenv('RUSTFS_REGION'),
        )
        logger.info("AWS session initialized.")

        self.s3 = self.session.resource(
            's3',
            endpoint_url=f"http://{os.getenv('RUSTFS_ENDPOINT')}",
            use_ssl=os.getenv('RUSTFS_USE_HTTPS', 'true').lower() == 'true',
        )
        logger.info("S3 resource initialized with endpoint: "
                    f"{os.getenv('RUSTFS_ENDPOINT')} and SSL: "
                    f"{os.getenv('RUSTFS_USE_HTTPS', 'true').lower() == 'true'}")

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
            logger.info(f"Starting download of {object_key} from bucket {bucket_name} to {local_path}")
            bucket.download_file(object_key, str(local_path))
            logger.info(f"✅ File downloaded successfully to {local_path}")

        except Exception as e:
            logger.exception("❌ Error downloading file: %s", local_path)


if __name__ == "__main__":
    downloader = DataDownloader()
    downloader.download_file()