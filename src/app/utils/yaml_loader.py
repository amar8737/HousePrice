from yaml import safe_load
from pathlib import Path
from src.app.utils.constants import CONFIG_FILE_PATH 
from src.app.utils.logger import Logger

# Initialize logger explicitly for this file
logger = Logger.get_logger(__file__)

class YamlLoader:
    @staticmethod
    def load_yaml(file_path):
        file_path = Path(file_path)
        
        # Check if file exists before trying to open
        if not file_path.exists():
            logger.error(f"YAML file not found: {file_path}")
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        
        # Safely open and load the YAML
        with open(file_path, 'r') as file:
            try:
                data = safe_load(file)
                logger.info(f"Successfully loaded config from {file_path}")
                return data
                
            except Exception:
                # Log the exact file that failed AND the full stack trace
                logger.exception(f"Error parsing YAML file: {file_path}")
                
                # Fail-fast: crash the pipeline so it doesn't execute blindly
                raise 

if __name__ == "__main__":
    try:
        config = YamlLoader.load_yaml(CONFIG_FILE_PATH)
        print("\nLoaded Configuration:")
        print(config)
    except Exception:
        print("\nPipeline execution stopped due to configuration error.")