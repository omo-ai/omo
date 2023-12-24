import os
import re
import sys
import logging
from datetime import datetime
import pinecone
import googleapiclient.discovery
from dotenv import load_dotenv 
from typing import Dict, List, Any
from google.oauth2 import service_account
from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter

from omo_api.db.models import GDriveObject
from omo_api.db.connection import session
from omo_api.utils.prompt import query_yes_no

file_handler = logging.FileHandler(filename='/mnt/efs/tmp.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger(__name__)

"""
The below is code extracted from langchain-googledrive. The above abtracts 
too much for our use cases. The repo above encapsulates authentication, text 
extraction, and instantiating Document objects, and loading into Pinecone.

Having separate functions for each of this would allow us to use each of 
these functions independently so we can have more control over how we 
authenticate, extract text, and track progress.
"""

def extract_text(
        node: Any,
        *,
        key: str = "content",
        path: str = "/textRun",
        markdown: bool = True,
    ) -> List[str]:
        def visitor(result: List[str], node: Any, parent: str) -> List[str]:
            return_link = False # defaults to false in original code
            if isinstance(node, dict):
                if "paragraphMarker" in node:
                    result.append("- " if "bullet" in node["paragraphMarker"] else "")
                    return result
                if "paragraph" in node:
                    prefix = ""
                    named_style_type = node["paragraph"]["paragraphStyle"][
                        "namedStyleType"
                    ]
                    level = re.match("HEADING_([1-9])", named_style_type)
                    if level:
                        prefix = f"{'#' * int(level[1])} "
                    if "bullet" in node["paragraph"]:
                        prefix += "- "
                    result.append(prefix)
                if "table" in node:
                    col_size = [0 for _ in range(node["table"]["columns"])]
                    rows: List[List[Any]] = [[] for _ in range(node["table"]["rows"])]
                    for row_idx, row in enumerate(node["table"]["tableRows"]):
                        for col_idx, cell in enumerate(row["tableCells"]):
                            body = "".join(
                                visitor([], cell, parent + "/table/tableCells/[]")
                            )
                            # remove URL to calculate the col max size
                            pure_body = re.sub(r"\[(.*)\](?:\(.*\))", r"\1", body)
                            cell_size = max(3, len(max(pure_body.split("\n"), key=len)))
                            col_size[col_idx] = max(col_size[col_idx], cell_size)
                            str_cell = re.sub(r"\n", r"<br />", "".join(body).strip())
                            rows[row_idx].append(str_cell)
                    # Reformate to markdown with extra space

                    for row in rows:
                        for col_idx, cell in enumerate(row):
                            split_cell = re.split(r"(<br />|\n)", cell)
                            # Split each portion and pad with space
                            for i, portion in enumerate(split_cell):
                                if portion != "<br />":
                                    pure_portion = re.sub(
                                        r"\[(.*)\](?:\(.*\))", r"\1", portion
                                    )
                                    split_cell[i] = portion + (
                                        " " * (col_size[col_idx] - len(pure_portion))
                                    )
                            # rebuild the body
                            row[col_idx] = "".join(split_cell)
                    # Now, build a markdown array
                    for row_idx, row in enumerate(rows):
                        row_result = ["| "]
                        for cell in row:
                            row_result.append(f"{cell} | ")
                        result.append("".join(row_result) + "\n")
                        if row_idx == 0:
                            row_result = ["|"]
                            for col_idx in range(len(row)):
                                row_result.append(("-" * (col_size[col_idx] + 2)) + "|")
                            result.append("".join(row_result) + "\n")
                    return result

                if key in node and isinstance(node.get(key), str):
                    if parent.endswith(path):
                        if node[key].strip():
                            if markdown and (
                                ("style" in node and "link" in node["style"])
                                or ("textStyle" in node and "link" in node["textStyle"])
                            ):
                                style_node = (
                                    node["style"]
                                    if "style" in node
                                    else node["textStyle"]
                                )
                                link = style_node["link"]
                                if isinstance(link, dict):
                                    link = link.get("url")
                                if return_link and link:
                                    result[-1] = f"{result[-1]}[{node[key]}]({link})"
                                else:
                                    # Empty link
                                    result[-1] = f"{result[-1]}{node[key]}"
                            else:
                                result[-1] = f"{result[-1]}{node[key]}"

                for k, v in node.items():
                    visitor(result, v, parent + "/" + k)
            elif isinstance(node, list):
                for v in node:
                    visitor(result, v, parent + "/[]")
            return result

        result: List[str] = []
        visitor(result, node, "")
        # Clean the result:
        purge_result = []
        previous_empty = False
        for line in result:
            line = re.sub("\x0b\s*", "\n", line).strip()
            if not line:
                if previous_empty:
                    continue
                previous_empty = True
            else:
                previous_empty = False

            purge_result.append(line)
        return purge_result

def extract_meta_data(file: Dict) -> Dict:
    """
    Extract metadata from file

    :param file: The file
    :return: Dict the meta data
    """
    meta = {
        "gdriveId": file["id"],
        "id": file["id"],
        "mimeType": file["mimeType"],
        "name": file["name"],
        "title": file["name"],
    }
    if file["webViewLink"]:
        meta["source"] = file["webViewLink"]
    else:
        logger.debug(f"Invalid URL {file}")
    if "createdTime" in file:
        meta["createdTime"] = file["createdTime"]
    if "modifiedTime" in file:
        meta["modifiedTime"] = file["modifiedTime"]
    if "sha256Checksum" in file:
        meta["sha256Checksum"] = file["sha256Checksum"]
    if "owners" in file:
        meta["author"] = file["owners"][0]["displayName"]
    if file.get("description", "").strip():
        meta["summary"] = file["description"]
    return meta

