import boto3
import json
import os

from pymongo import MongoClient

client = boto3.client('secretsmanager')
secret_id = os.environ["SECRET_ID"]
response = client.get_secret_value(SecretId=secret_id)
secret_str = response["SecretString"]
decoded = json.loads(secret_str)
username = decoded["username"]
password = decoded["password"]
host = decoded["host"]
port = decoded["port"]
connect_str = "mongodb://{username}:{password}@{host}:{port}/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false".format(username=username,password=password, host=host, port=port)
# connect_str = "mongodb://master:_c6hbS6zJzKUbP69ECrg6vW7Qwnpbo3ecOwQQ_kRz@cluster611f8aff-ia7spb4dsp2z.cluster-cxbtl4xaiuqh.ap-northeast-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
print(connect_str)
client = MongoClient(connect_str)
print(client.server_info())

db_name = os.environ["MONGO_DB"]
collection_name = os.environ["MONGO_COLLECTION"]
collection = client[db_name][collection_name]
print(collection)

for x in collection.find():
    print(x)
    

