import os
from datetime import datetime
from omo_api.background import celery
from llama_index.readers.google import GoogleDriveReader


@celery.task
def add(x, y):
    return x + y