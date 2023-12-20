import sys
import os
from typing import Optional, List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter
from google.oauth2 import service_account

from langchain_googledrive.document_loaders import GoogleDriveLoader

class GoogleDriveLoaderDomainWideDelegation(GoogleDriveLoader):
    """
    This loader can be used in the case there is domain wide delegation
    configured with delegated user email. (i.e. impersonate a user)
    """
    def _load_credentials(self, scopes):
        try:
            creds = service_account.Credentials.from_service_account_file(
                os.getenv('GOOGLE_ACCOUNT_FILE'),
                scopes=scopes
            )
            if 'GOOGLE_DELEGATE_EMAIL' in os.environ:
                delegated_creds = creds.with_subject(os.getenv('GOOGLE_DELEGATE_EMAIL'))
                return delegated_creds

            return creds
        except ValueError as e:
            return super()._load_credentials(scopes)