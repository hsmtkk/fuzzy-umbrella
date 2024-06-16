import os
from langchain_openai import ChatOpenAI
from pymongo import MongoClient
from langchain_community.vectorstores.documentdb import DocumentDBVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA


embedding = OpenAIEmbeddings()

mongo_connect_str = os.environ["MONGO_CONNECT_STRING"]
mongo_db = os.environ["MONGO_DB"]
mongo_collection = os.environ["MONGO_COLLECTION"]
mongo_namespace = mongo_db + "." + mongo_collection
mongo_index = os.environ["MONGO_INDEX"]

client = MongoClient(mongo_connect_str)
collection = client[mongo_db][mongo_collection]
db = DocumentDBVectorSearch.from_connection_string(
    connection_string=mongo_connect_str,
    namespace=mongo_namespace,
    embedding=embedding,
    index_name=mongo_index,
)

test_resp = db.similarity_search("ワクチンのメリット、デメリットは何か")
print(test_resp)

qa_retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 25},
)

llm = ChatOpenAI()

prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=qa_retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
)

while True:
    query = input("You> ")
    answer = qa.invoke({"query": query})
    print("AI> ", answer)
