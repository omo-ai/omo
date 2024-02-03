
def flatten_list(list_of_lists):
    """Accepts a list of lists and returns a single list"""
    return [item for row in list_of_lists for item in row]

def clean_url(url: str):
    if url.endswith('/'):
        url = url[:-1]
    return url