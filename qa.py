import os
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pymongo import MongoClient
from langchain_community.vectorstores.documentdb import DocumentDBVectorSearch
from langchain_openai import OpenAIEmbeddings

embedding = OpenAIEmbeddings()

mongo_connect_str = os.environ["MONGO_CONNECT_STRING"]
mongo_db = os.environ["MONGO_DB"]
mongo_collection = os.environ["MONGO_COLLECTION"]
mongo_index = os.environ["MONGO_INDEX"]

client = MongoClient(mongo_connect_str)
collection = client[mongo_db][mongo_collection]
db = DocumentDBVectorSearch(
    collection=collection, embedding=embedding, index_name=mongo_index
)

retriever = db.as_retriever()
llm = ChatOpenAI()

system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Use three sentence maximum and keep the answer concise. "
    "Context: {context}"
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, question_answer_chain)

while True:
    question = input("You> ")
    answer = chain.invoke(question)
    print("AI> ", answer)
