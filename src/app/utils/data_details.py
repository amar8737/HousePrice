from dataclasses import dataclass
from src.app.utils.yaml_loader import YamlLoader
from src.app.utils.constants import CONFIG_FILE_PATH, PROJECT_ROOT
from pathlib import Path


config = YamlLoader.load_yaml(CONFIG_FILE_PATH)

@dataclass
class DataDetails:
    bucket: str
    source: str
    destination: str
    file_name: str
    parameters: dict

def get_data_details():
    data_config = config.get('DATA_INGESTION', [])[0]  # Assuming the first entry is for data ingestion
    return DataDetails(
        bucket=data_config['bucket'],
        source=data_config['source'],
        destination=PROJECT_ROOT / data_config['destination'],
        file_name=data_config['file_name'],
        parameters=data_config['parameters']
    )
