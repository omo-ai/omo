import os
from omo_api.utils.exceptions import MissingEnvironmentVariable

def flatten_list(list_of_lists: list) -> list:
    """Accepts a list of lists and returns a single list"""
    if not list_of_lists:
        return list_of_lists
    
    element = list_of_lists[0]

    # check if the inner objects are lists
    if not type(element) == list:
        return list_of_lists

    return [item for row in list_of_lists for item in row]

def clean_url(url: str) -> str:
    if url.endswith('/'):
        url = url[:-1]
    return url

def get_env_var(var_name: str) -> str:
    try:
        return os.environ[var_name]
    except KeyError:
        raise MissingEnvironmentVariable(f"{var_name} does not exist")