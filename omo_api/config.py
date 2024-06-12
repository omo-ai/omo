import yaml
from enum import Enum

# To add a new Connector:
# 1. Add a new name to the Connectors class
# 2. Add it to config.yaml. Ensure the name in config.yaml matches the value 
# in the Connectors class

class Connector(Enum):
    GOOGLE_DRIVE = 'googledrive'
    ATLASSIAN = 'atlassian'
    NOTION = 'notion'

def load_config(path: str) -> dict:
    """
    Load configuration from a YAML file.

    Args:
        path (str): The path to the YAML file.

    Returns:
        dict: The loaded configuration as a dictionary.
    """
    with open(path, 'r') as file:
        conf = yaml.safe_load(file)
    
    return conf

config = load_config('config.yaml')