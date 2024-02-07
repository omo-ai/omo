from typing import List
from pyairtable import Api
from llama_index import download_loader

AirtableReader = download_loader('AirtableReader')

class CustomAirtableReader(AirtableReader):
    """Subclasses llama-index's AirtableReader and stores additional metadata

    Args:
        api_key (str): Airtable API key.
    """

    def __init__(self, api_key: str) -> None:
        self.base_airtable_url = "https://airtable.com"
        self.api = Api(api_key)
        self.base_metadata = self.get_base_metadata()
        super().__init__(api_key)
    
    def get_base_metadata(self):
        base_meta = {
            'name': '',
            'url': '',
            'tables': {}
        }
        for base in self.api.bases():
            base_meta['name'] = base.name
            base_meta['url'] = f"{self.base_airtable_url}/{base.id}"

            for tbl in base.schema().tables:
                base_meta['tables'][tbl.id] = {
                    'name': tbl.name,
                    'url': f"{base_meta['url']}/{tbl.id}"
                }
            
            base_meta[base.id] = base_meta

        return base_meta
        
