from google.cloud import datastore

datastore_client = datastore.Client()

task_key = datastore_client.key("names-of-competitors", "2")

task = datastore.Entity(key = task_key)
task["name"] = "niall"
task["score"] = "60"
datastore_client.put(task)