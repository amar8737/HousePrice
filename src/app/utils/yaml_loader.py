from yaml import safe_load
from src.app.utils.constants import CONFIG_FILE_PATH
from pathlib import Path

class YamlLoader:
    @staticmethod
    def load_yaml(file_path):
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        
        with open(file_path, 'r') as file:
            try:
                data = safe_load(file)
                return data
            except Exception as e:
                print(f"Error loading YAML file: {e}")
                return None
if __name__ == "__main__":
    config = YamlLoader.load_yaml(CONFIG_FILE_PATH)
    print(config)