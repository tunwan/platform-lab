from flask import Flask, jsonify, request

app = Flask(__name__)

# Deocamdată ținem datele în memorie. Mai târziu le mutăm în DynamoDB (prin Floci).
TASKS = []


@app.get("/health")
def health():
    # Endpoint folosit de OpenShift ca să știe dacă aplicația e „vie”
    return jsonify(status="ok")


@app.get("/tasks")
def list_tasks():
    return jsonify(TASKS)

@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    for task in TASKS:
        if task["id"] == task_id:
            TASKS.remove(task)
            return "", 204
    return jsonify(error="task inexistent"), 404

@app.post("/tasks")
def add_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify(error="câmpul 'title' e obligatoriu"), 400
    task = {"id": len(TASKS) + 1, "title": title, "done": False}
    TASKS.append(task)
    return jsonify(task), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
