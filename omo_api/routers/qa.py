import os
import re
import pinecone
import random
import logging
from operator import itemgetter
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter
from langchain import hub
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from omo_api.conf.prompt import PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')



router = APIRouter()

def preprocess_message(message: str) -> str:
    """
    Strip out strings that make Omo give a weird response
    - hello <@USER_ID2>
    - <@USER_ID2> hello
    """
    try:
        username_pattern = '<@USER_ID2>' # strip out the `OmoAI` username from the message before querying
        message = re.sub(username_pattern, '', message).strip()
    except:
        pass

    return message

def postprocess_message(message: str) -> str:
    pass

def show_prompt() -> str:
    prompt_responses = [
        "Getting the answer for you!",
        "I'm on it!",
         "Looking into it!"
    ]
    prompt_response = random.choice(prompt_responses)
    return f"{prompt_response} Please wait a few moments..."


def answer_question(question: str, context: dict):

    pinecone.init(
        api_key=context['omo_pinecone_api_key'], 
        environment=context['omo_pinecone_env'], 
    )

    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_existing_index(context['omo_pinecone_index'], embedding_function)
    retriever = docsearch.as_retriever()

    llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0, openai_api_key=OPENAI_API_KEY)

    rag_prompt_custom = PromptTemplate.from_template(PROMPT_TEMPLATE)

    rag_chain_from_docs = (
        {
            "context": lambda input: input["documents"],
            "question": itemgetter("question"),
        }
        | rag_prompt_custom
        | llm
        | StrOutputParser() # converts any input into a string
    )

    rag_chain_with_source = RunnableParallel(
        {"documents": retriever, "question": RunnablePassthrough()}
    ) | {
        "documents": lambda input: [doc.metadata for doc in input["documents"]],
        "answer": rag_chain_from_docs,
    }

    # rag_prompt = hub.pull("rlm/rag-prompt")
    # rag_chain = {"context": retriever, "question": RunnablePassthrough()} | rag_prompt | llm

    answer = rag_chain_with_source.invoke(question)

    return answer['answer']