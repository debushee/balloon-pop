from google.cloud import datastore

def SendToDb(name, score):

    datastore_client = datastore.Client()
    #Get list from DB
    query = datastore_client.query(kind='names-of-competitors')
    results = list(query.fetch())
    task_key = datastore_client.key("names-of-competitors", str(len(results)+1))

    task = datastore.Entity(key = task_key)
    task["name"] = name
    task["score"] = score
    datastore_client.put(task)