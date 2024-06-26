import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.documentdb import DocumentDBVectorSearch, DocumentDBSimilarityType
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient

mongo_connect_str = os.environ["MONGO_CONNECT_STRING"]
mongo_db = os.environ["MONGO_DB"]
mongo_collection = os.environ["MONGO_COLLECTION"]
mongo_index = os.environ["MONGO_INDEX"]

loader = PyPDFLoader("./sample/vaccine.pdf")
docs = loader.load_and_split()

embedding = OpenAIEmbeddings()
client = MongoClient(mongo_connect_str)
collection = client[mongo_db][mongo_collection]
db = DocumentDBVectorSearch.from_documents(
    docs, embedding, collection=collection, index_name=mongo_index
)

dimensions = 1536
similarity_algorithm = DocumentDBSimilarityType.COS
db.create_index(dimensions, similarity_algorithm)
