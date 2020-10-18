import logging
import datetime
import azure.functions as func
from azure.cosmos import exceptions, CosmosClient, PartitionKey

endpoint = "https://tst-azure.documents.azure.com:443/"
key = '89lhKSndZ8tsZx4X9g8xrKez2IbMH0lJliJEdNnP1PdXSAGin42M952uBkCUbyFX1HmhDUt71gKYZSaygEL3tA=='

client = CosmosClient(endpoint, key)
    
database_name = 'demodb'
database = client.create_database_if_not_exists(id=database_name)

container_name = 'items'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/name"),
    offer_throughput=400
)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

    
    db_insert = {
        "name"= name,
        "insert_time" = datetime.datetime.now()
    }
    container.create_item(body=db_insert)



