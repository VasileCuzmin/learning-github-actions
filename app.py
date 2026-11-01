from flask import Flask, jsonify, request, abort


def create_app():
    app = Flask(__name__)

    # In-memory store (resets when the app restarts)
    app.config["TASKS"] = {}
    app.config["NEXT_ID"] = 1

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/tasks")
    def list_tasks():
        return jsonify(list(app.config["TASKS"].values()))

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        task = app.config["TASKS"].get(task_id)
        if task is None:
            abort(404, description="Task not found")
        return jsonify(task)

    @app.post("/tasks")
    def create_task():
        data = request.get_json(silent=True)
        if not data or not data.get("title"):
            abort(400, description="'title' is required")

        task_id = app.config["NEXT_ID"]
        app.config["NEXT_ID"] += 1

        task = {"id": task_id, "title": data["title"], "done": False}
        app.config["TASKS"][task_id] = task
        return jsonify(task), 201

    @app.put("/tasks/<int:task_id>")
    def update_task(task_id):
        task = app.config["TASKS"].get(task_id)
        if task is None:
            abort(404, description="Task not found")

        data = request.get_json(silent=True) or {}
        if "title" in data:
            task["title"] = data["title"]
        if "done" in data:
            task["done"] = bool(data["done"])
        return jsonify(task)

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        if app.config["TASKS"].pop(task_id, None) is None:
            abort(404, description="Task not found")
        return "", 204

    @app.errorhandler(400)
    @app.errorhandler(404)
    def handle_error(err):
        return jsonify(error=err.description), err.code

    return app


if __name__ == "__main__":
    create_app().run(debug=True)