import yaml

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