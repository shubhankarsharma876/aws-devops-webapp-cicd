from flask import Flask, jsonify, abort,request

app = Flask(__name__)

tasks =[]
next_id=1

@app.route("/health",methods=["GET"])
def health():
    return jsonify({"status":"OK"}),200

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks),200

@app.route("/tasks",methods=["POST"])
def create_task():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        abort(400, description="'title' is required")

    task = {
        "id": next_id,
        "title": data["title"],
        "done": data.get("done",False)
    }

    tasks.append(task)
    next_id+=1
    return jsonify(task),201

@app.route("/tasks/<int:task_id>",methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"]==task_id),None)
    if task is None:
        abort(404, description="Task not found")
    return jsonify(task), 200


@app.route("/tasks/<int:task_id>",methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"]==task_id),None)
    if task is None:
        abort(404, description="Task not found")
    data = request.get_json()
    task["title"] = data.get("title", task["title"])
    task["done"] = data.get("done", task["done"])
    return jsonify(task), 200

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        abort(404, description="Task not found")

    tasks = [t for t in tasks if t["id"] != task_id]
    return "", 204

if __name__ =="__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)
