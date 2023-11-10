import numpy as np
import openai
import pinecone
import os
from dotenv import load_dotenv
from langchain import embeddings, OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from llama_index import VectorStoreIndex, StorageContext, load_index_from_storage, SimpleDirectoryReader, LLMPredictor, \
    ServiceContext
from llama_index.indices import service_context
from openai.embeddings_utils import cosine_similarity
#from sklearn.metrics.pairwise import cosine_similarity
from pinecone import index
from sentence_transformers import SentenceTransformer,util

from utils import load_docs

#from utils import docs

model1 = SentenceTransformer('all-MiniLM-L6-v2')
## LLAMA approach

def create_index_llama(dir):
    #input_dir = 'chatBot/Data'
    load_dotenv()
    openai.api_key = os.environ['OPENAI_API_KEY']
    input_dir= './Data'
    #'C:/Users/vamsh/Desktop/NLP/chatBot-AI-Final/Data'
    #file_extension = '.txt'
    #docs=[]
    reader = SimpleDirectoryReader(input_dir)
    docs = reader.load_data()
    print('DOcs -',len(docs))

    index1 = VectorStoreIndex.from_documents(docs)
    # custom_llm_index = VectorStoreIndex.from_documents(
    #     docs, service_context=service_context)

    return index1
    #return custom_llm_index
def query_engine(index1):
    query_engine = index1.as_query_engine()


def save_index1(index):
    index.storage_context.persist("coop_index1")
    storage_context = StorageContext.from_defaults(persist_dir="coop_index1")

    return storage_context

def load_reply_index1(sto_con,query):
    load_dotenv()
    openai.api_key = os.environ['OPENAI_API_KEY']
    new_index = load_index_from_storage(sto_con)
    new_query_engine = new_index.as_query_engine()
    response = new_query_engine.query(query)
    response = str(response)
    return response

def custom_load_reply(sto_con,query):
    new_index = load_index_from_storage(sto_con)
    new_query_engine = new_index.as_query_engine()

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))

    # Create a service context with the custom predictor
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    # Create an index using the service context
    # custom_llm_index = VectorStoreIndex.from_documents(
    #     documents, service_context=service_context
    #)

    #custom_llm_query_engine = custom_llm_index.as_query_engine()
    response = new_query_engine.query(query)
    #print(response)
    return response







