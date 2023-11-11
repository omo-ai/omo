import os
import logging
import chromadb
from fastapi import FastAPI
from logging.config import dictConfig
from langchain import hub
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from conf.log import log_config

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHROMADB_PERSIST_DIR = os.getenv('CHROMADB_PERSIST_DIR')

dictConfig(log_config)
logger = logging.getLogger(__name__)

app = FastAPI()

SLACK_WEBHOOKS = {
    'omoai': {
        'hook_url': 'https://hooks.slack.com/services/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',
        'description': 'Posts to OmoAI app channel'
    }
}

@app.get("/")
async def root():
    return {"message": "Hello, Omo!"}


@app.get('/api/v1/answer_question/{question}')
async def answer_question(question: str):
    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = Chroma(persist_directory='/chroma_index_data', embedding_function=embedding_function)
    retriever = db.as_retriever()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

    rag_prompt = hub.pull("rlm/rag-prompt")
    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | rag_prompt | llm

    answer = rag_chain.invoke(question)

    logger.debug(f"Question: {question} = Answer: {answer.content}")

    return answer.content
