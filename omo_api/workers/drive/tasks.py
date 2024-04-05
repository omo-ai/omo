import logging
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from omo_api.loaders.gdrive.google_drive import GoogleDriveReaderOAuthAccessToken
from omo_api.workers.background import celery
from omo_api.utils.pipeline import get_pipeline

logger = logging.getLogger(__name__) 

@celery.task
def sync_google_drive(files: dict,
                      access_token: str):

    loader = GoogleDriveReaderOAuthAccessToken(access_token=access_token)

    folders = filter(lambda f: f['type'] == 'folder', files['files'])
    files = filter(lambda f: f['type'] != 'folder', files['files'])

    folder_ids = [f['id'] for f in folders]
    file_ids = [f['id'] for f in files]

    all_docs = []
    for folder_id in folder_ids:
        folder_docs = loader.load_data(folder_id=folder_id)
        all_docs.append(folder_docs)

    docs = loader.load_data(file_ids=file_ids)
    all_docs.append(docs)


    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")
    Settings.llm = OpenAI(temperature=0.0, model="gpt-4-0125-preview")

    pipeline = get_pipeline()
    nodes = pipeline.run(num_workers=1) # anything > 1 results in AttributeError: Can't pickle local object 'split_by_sentence_tokenizer.<locals>.split'
    logger.debug(nodes)

