from google.cloud import datastore


datastore_client = datastore.Client()
    #Get list from DB
query = datastore_client.query(kind='names-of-competitors')
results = list(query.fetch())
print(results)
n = len(results)
print(n)

task_key = datastore_client.key("names-of-competitors", "1")

task = datastore.Entity(key = task_key)
task["name"] = "Niall"
task["score"] = 50
datastore_client.put(task)