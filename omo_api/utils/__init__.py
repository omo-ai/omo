import os
from omo_api.utils.exceptions import MissingEnvironmentVariable

def flatten_list(list_of_lists):
    """Accepts a list of lists and returns a single list"""
    return [item for row in list_of_lists for item in row]

def clean_url(url: str):
    if url.endswith('/'):
        url = url[:-1]
    return url

def get_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise MissingEnvironmentVariable(f"{var_name} does not exist")