import os
import logging
import tempfile
import json
from typing import Optional, List, Any
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from llama_index.core.readers.base import BasePydanticReader
from llama_index.core.bridge.pydantic import PrivateAttr
from llama_index.core.schema import Document
from llama_index.core import SimpleDirectoryReader

logger = logging.getLogger(__name__)

# class GoogleDriveLoaderDomainWideDelegation(GoogleDriveLoader):
#     """
#     This loader can be used in the case there is domain wide delegation
#     configured with delegated user email. (i.e. impersonate a user)
#     """
#     def _load_credentials(self, scopes):
#         try:
#             creds = service_account.Credentials.from_service_account_file(
#                 os.getenv('GOOGLE_ACCOUNT_FILE'),
#                 scopes=scopes
#             )
#             if 'GOOGLE_DELEGATE_EMAIL' in os.environ:
#                 delegated_creds = creds.with_subject(os.getenv('GOOGLE_DELEGATE_EMAIL'))
#                 return delegated_creds

#             return creds
#         except ValueError as e:
#             return super()._load_credentials(scopes)





# Scope for reading and downloading google drive files
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Custom implementation of 
# https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/readers/llama-index-readers-google/llama_index/readers/google/drive/base.py
class GoogleDriveReaderOAuthAccessToken(BasePydanticReader):

    client_config: Optional[dict] = None
    authorized_user_info: Optional[dict] = None
    service_account_key: Optional[dict] = None
    token_path: Optional[str] = None
    access_token: Optional[str] = None

    _is_cloud: bool = PrivateAttr(default=False)
    _creds: Credentials = PrivateAttr()
    _mimetypes: dict = PrivateAttr()

    def __init__(
        self,
        is_cloud: Optional[bool] = False,
        credentials_path: str = "credentials.json",
        token_path: str = "token.json",
        service_account_key_path: str = "service_account_key.json",
        client_config: Optional[dict] = None,
        authorized_user_info: Optional[dict] = None,
        service_account_key: Optional[dict] = None,
        access_token: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize with parameters."""
        self._creds = None
        self._is_cloud = (is_cloud,)
        # Download Google Docs/Slides/Sheets as actual files
        # See https://developers.google.com/drive/v3/web/mime-types
        self._mimetypes = {
            # Google filetypes will be downloaded as OpenXML formats
            "google": {
                "application/vnd.google-apps.document": {
                    "mimetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "extension": ".docx",
                },
                "application/vnd.google-apps.spreadsheet": {
                    "mimetype": (
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    ),
                    "extension": ".xlsx",
                },
                "application/vnd.google-apps.presentation": {
                    "mimetype": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    "extension": ".pptx",
                },
            },
            "other": {
                # Microsoft Word
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
                    "mimetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "extension": ".docx"
                },
                # Excel
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
                    "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "extension": ".xlsx",
                },
                # Powerpoint
                "application/vnd.openxmlformats-officedocument.presentationml.presentation": {
                    "mimetype": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    "extension": ".pptx",
                },
                # PDF
                "application/pdf": {
                    "mimetype": "application/pdf",
                    "extension": ".pdf",
                }

            }
        }

        super().__init__(
            client_config=client_config,
            authorized_user_info=authorized_user_info,
            service_account_key=service_account_key,
            token_path=token_path,
            access_token=access_token,
            **kwargs,
        )

    @classmethod
    def class_name(cls) -> str:
        return "GoogleDriveReaderOAuthAccessToken"

    def _get_credentials(self):
        creds = None

        if self.access_token:
            creds = Credentials(self.access_token)

        return creds

    def _get_fileids_meta(
        self,
        drive_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        file_id: Optional[str] = None,
        mime_types: Optional[List[str]] = None,
        query_string: Optional[str] = None,
    ) -> List[List[str]]:
        """Get file ids present in folder/ file id
        Args:
            drive_id: Drive id of the shared drive in google drive.
            folder_id: folder id of the folder in google drive.
            file_id: file id of the file in google drive
            mime_types: The mimeTypes you want to allow e.g.: "application/vnd.google-apps.document"
            query_string: A more generic query string to filter the documents, e.g. "name contains 'test'".

        Returns:
            metadata: List of metadata of filde ids.
        """
        from googleapiclient.discovery import build

        try:
            service = build("drive", "v3", credentials=self._creds)
            fileids_meta = []
            if folder_id:
                folder_mime_type = "application/vnd.google-apps.folder"
                query = "('" + folder_id + "' in parents)"

                # Add mimeType filter to query
                if mime_types:
                    if folder_mime_type not in mime_types:
                        mime_types.append(folder_mime_type)  # keep the recursiveness
                    mime_query = " or ".join(
                        [f"mimeType='{mime_type}'" for mime_type in mime_types]
                    )
                    query += f" and ({mime_query})"

                # Add query string filter
                if query_string:
                    # to keep the recursiveness, we need to add folder_mime_type to the mime_types
                    query += (
                        f" and ((mimeType='{folder_mime_type}') or ({query_string}))"
                    )

                items = []
                # get files taking into account that the results are paginated
                while True:
                    if drive_id:
                        results = (
                            service.files()
                            .list(
                                q=query,
                                driveId=drive_id,
                                corpora="drive",
                                includeItemsFromAllDrives=True,
                                supportsAllDrives=True,
                                fields="*",
                            )
                            .execute()
                        )
                    else:
                        results = (
                            service.files()
                            .list(
                                q=query,
                                includeItemsFromAllDrives=True,
                                supportsAllDrives=True,
                                fields="*",
                            )
                            .execute()
                        )
                    items.extend(results.get("files", []))
                    page_token = results.get("nextPageToken", None)
                    if page_token is None:
                        break

                for item in items:
                    if item["mimeType"] == folder_mime_type:
                        if drive_id:
                            fileids_meta.extend(
                                self._get_fileids_meta(
                                    drive_id=drive_id,
                                    folder_id=item["id"],
                                    mime_types=mime_types,
                                    query_string=query_string,
                                )
                            )
                        else:
                            fileids_meta.extend(
                                self._get_fileids_meta(
                                    folder_id=item["id"],
                                    mime_types=mime_types,
                                    query_string=query_string,
                                )
                            )
                    else:
                        # Check if file doesn't belong to a Shared Drive. "owners" doesn't exist in a Shared Drive
                        is_shared_drive = "driveId" in item
                        author = (
                            item["owners"][0]["displayName"]
                            if not is_shared_drive
                            else "Shared Drive"
                        )

                        fileids_meta.append(
                            (
                                item["id"],
                                author,
                                item["name"],
                                item["mimeType"],
                                item["createdTime"],
                                item["modifiedTime"],
                                item["webViewLink"],
                            )
                        )
            else:
                # Get the file details
                file = (
                    service.files()
                    .get(fileId=file_id, supportsAllDrives=True, fields="*")
                    .execute()
                )
                # Get metadata of the file
                # Check if file doesn't belong to a Shared Drive. "owners" doesn't exist in a Shared Drive
                is_shared_drive = "driveId" in file
                author = (
                    file["owners"][0]["displayName"]
                    if not is_shared_drive
                    else "Shared Drive"
                )

                fileids_meta.append(
                    (
                        file["id"],
                        author,
                        file["name"],
                        file["mimeType"],
                        file["createdTime"],
                        file["modifiedTime"],
                        file["webViewLink"],
                    )
                )
            return fileids_meta

        except Exception as e:
            logger.error(
                f"An error occurred while getting fileids metadata: {e}", exc_info=True
            )

    def _download_file(self, fileid: str, filename: str) -> str:
        """Download the file with fileid and filename
        Args:
            fileid: file id of the file in google drive
            filename: filename with which it will be downloaded
        Returns:
            The downloaded filename, which which may have a new extension.
        """
        from io import BytesIO

        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseDownload

        try:
            # Get file details
            service = build("drive", "v3", credentials=self._creds)
            file = service.files().get(fileId=fileid, supportsAllDrives=True).execute()

            logger.debug(f"file mimetype: {file['mimeType']}")

            # Depending on the mimetype, we have to make a different API call
            if file["mimeType"] in self._mimetypes['google']:
                logger.debug("...downloading google mimetype")
                download_mimetype = self._mimetypes['google'][file["mimeType"]]["mimetype"]
                download_extension = self._mimetypes['google'][file["mimeType"]]["extension"]
                new_file_name = filename + download_extension

                # Download and convert file
                request = service.files().export_media(
                    fileId=fileid, mimeType=download_mimetype
                )
            else:
                try:
                    logger.debug("...trying other mimetype")
                    download_extension = self._mimetypes['other'][file['mimeType']]['extension']
                    new_file_name = filename + download_extension
                except KeyError as e:
                    new_file_name = filename

                # Download file without conversion
                logger.debug('...request get_media()')
                request = service.files().get_media(fileId=fileid)

            # Download file data
            # creates a temp file e.g.
            # /tmp/tmpf_u0031c/1A6kqGjaSJo4X7Asa2RJsqK6JBZ1nBjgM.pptx
            logger.debug('...creating tmp file...')
            file_data = BytesIO()
            downloader = MediaIoBaseDownload(file_data, request)
            done = False

            while not done:
                logger.debug('...downloading chunk...')
                status, done = downloader.next_chunk()
            
            logger.debug(f"...tmp file name {new_file_name}")

            # Save the downloaded file
            with open(new_file_name, "wb") as f:
                f.write(file_data.getvalue())

            return new_file_name

        except Exception as e:
            logger.error(
                f"An error occurred while downloading file: {e}", exc_info=True
            )

    def _load_data_fileids_meta(self, fileids_meta: List[List[str]]) -> List[Document]:
        """Load data from fileids metadata
        Args:
            fileids_meta: metadata of fileids in google drive.

        Returns:
            List[Document]: List of Document of data present in fileids.
        """
        try:
            with tempfile.TemporaryDirectory() as temp_dir:

                def get_metadata(filename):
                    return metadata[filename]

                temp_dir = Path(temp_dir)
                metadata = {}

                for fileid_meta in fileids_meta:
                    # Download files and name them with their fileid
                    fileid = fileid_meta[0]
                    filepath = os.path.join(temp_dir, fileid)
                    final_filepath = self._download_file(fileid, filepath)

                    # Add metadata of the file to metadata dictionary
                    metadata[final_filepath] = {
                        "file_id": fileid_meta[0],
                        "author": fileid_meta[1],
                        "file_name": fileid_meta[2],
                        "mimetype": fileid_meta[3],
                        "creation_date": fileid_meta[4],
                        "last_modified_date": fileid_meta[5],
                        "source": fileid_meta[6],
                    }
                loader = SimpleDirectoryReader(
                    temp_dir, 
                    file_metadata=get_metadata,
                )
                logger.debug('...loading data from Google Drive')
                documents = loader.load_data()
                logger.debug(
                    f"...loaded {len(documents)} Document chunks from Google Drive."
                )
                for doc in documents:
                    doc.id_ = doc.metadata.get("file_id", doc.id_)

            return documents
        except Exception as e:
            logger.error(
                f"An error occurred while loading data from fileids meta: {e}",
                exc_info=True,
            )

    def _load_from_file_ids(
        self,
        drive_id: Optional[str],
        file_ids: List[str],
        mime_types: Optional[List[str]],
        query_string: Optional[str],
    ) -> List[Document]:
        """Load data from file ids
        Args:
            file_ids: File ids of the files in google drive.
            mime_types: The mimeTypes you want to allow e.g.: "application/vnd.google-apps.document"
            query_string: List of query strings to filter the documents, e.g. "name contains 'test'".

        Returns:
            Document: List of Documents of text.
        """
        try:
            fileids_meta = []
            for file_id in file_ids:
                fileids_meta.extend(
                    self._get_fileids_meta(
                        drive_id=drive_id,
                        file_id=file_id,
                        mime_types=mime_types,
                        query_string=query_string,
                    )
                )
            return self._load_data_fileids_meta(fileids_meta)
        except Exception as e:
            logger.error(
                f"An error occurred while loading with fileid: {e}", exc_info=True
            )

    def _load_from_folder(
        self,
        drive_id: Optional[str],
        folder_id: str,
        mime_types: Optional[List[str]],
        query_string: Optional[str],
    ) -> List[Document]:
        """Load data from folder_id.

        Args:
            drive_id: Drive id of the shared drive in google drive.
            folder_id: folder id of the folder in google drive.
            mime_types: The mimeTypes you want to allow e.g.: "application/vnd.google-apps.document"
            query_string: A more generic query string to filter the documents, e.g. "name contains 'test'".

        Returns:
            Document: List of Documents of text.
        """
        try:
            fileids_meta = self._get_fileids_meta(
                drive_id=drive_id,
                folder_id=folder_id,
                mime_types=mime_types,
                query_string=query_string,
            )
            return self._load_data_fileids_meta(fileids_meta)
        except Exception as e:
            logger.error(
                f"An error occurred while loading from folder: {e}", exc_info=True
            )

    def load_data(
        self,
        drive_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        file_ids: Optional[List[str]] = None,
        mime_types: Optional[List[str]] = None,  # Deprecated
        query_string: Optional[str] = None,
    ) -> List[Document]:
        """Load data from the folder id or file ids.

        Args:
            drive_id: Drive id of the shared drive in google drive.
            folder_id: Folder id of the folder in google drive.
            file_ids: File ids of the files in google drive.
            mime_types: The mimeTypes you want to allow e.g.: "application/vnd.google-apps.document"
            query_string: A more generic query string to filter the documents, e.g. "name contains 'test'".
                It gives more flexibility to filter the documents. More info: https://developers.google.com/drive/api/v3/search-files

        Returns:
            List[Document]: A list of documents.
        """
        self._creds = self._get_credentials()

        if folder_id:
            return self._load_from_folder(drive_id, folder_id, mime_types, query_string)
        elif file_ids:
            return self._load_from_file_ids(
                drive_id, file_ids, mime_types, query_string
            )
        else:
            logger.warning("Either 'folder_id' or 'file_ids' must be provided.")
            return []