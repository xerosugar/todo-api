# API was tested with the 'REST Client'-extension in VS Code during development
import uuid
from flask import Flask, json, request

api = Flask(__name__)

# todoDb[ uuid ] => { done=True/False, message="..." }
todoDb = {}

# List all registered to-dos, or add a new to-do
@api.route('/todos', methods=['GET', "POST"])
def list_or_post_todos():
    if request.method == "GET":
        # sorting = request.args.get("sort")
        # TODO: Add support for sorting to-dos
        return json.dumps(todoDb)
    elif request.method == "POST":
        body = request.get_json()
        todoId = str(uuid.uuid4())
        todoDb[todoId] = dict(done=body["done"], message=body["message"])
        return todoId

# Get/update/delete a specific to-do
@api.route('/todos/<id>', methods=['GET', "PUT", "DELETE"])
def get_update_or_delete_todos(id):
    if request.method == "GET":
        return json.dumps(todoDb[id])
    elif request.method == "DELETE":
        removedSuccessfully = False
        if todoDb.get(id) != None:
            todoDb.pop(id)
            removedSuccessfully = True
        return json.dumps(removedSuccessfully)
    elif request.method == "PUT":
        todo = todoDb[id]
        body = request.get_json()
        todo["done"] = body["done"]
        todo["message"] = body["message"]
        return json.dumps(True)

# If the debug flag is set the server will automatically reload for 
# code changes and show a debugger in case an exception happened
debugMode = True
port = 3000
address = "127.0.0.1"

if __name__ == '__main__':
    api.run(address, port, debugMode)