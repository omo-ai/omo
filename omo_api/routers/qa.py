import os
import re
import pinecone
import random
import logging
from operator import itemgetter
from langchain import hub
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough, RunnableParallel
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), 
    environment=os.getenv("PINECONE_ENV"), 
)

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


from omo_api.conf.prompt import PROMPT_TEMPLATE

def answer_question(question: str):
    embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    docsearch = Pinecone.from_existing_index(PINECONE_INDEX, embedding_function)
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

    logger.debug(f"Question: {question} = Answer: {answer['answer']}")

    return answer['answer']