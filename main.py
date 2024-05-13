from flask import Flask, abort, request, jsonify, render_template
from flask_cors import CORS
from config import tasks_path
from utils import json_
from tools import get_all_plain_tasks, validate_task, convert_to_plain_task, parse_task
import uuid

HOST = '0.0.0.0'
DEBUG = False
WRITE_TO_JSON = False

_tasks = json_(tasks_path)

app = Flask(__file__)
app.json.sort_keys = False
CORS(app, origins=['https://famgz-todo-list-angular.vercel.app', 'http://localhost:4200'],
     methods=["GET", "POST", "PUT", "DELETE"])


def save_tasks():
    if not WRITE_TO_JSON:
        return
    json_(tasks_path, _tasks,
          ensure_ascii=False, sort_keys=False, indent=2)


@app.get('/')
def home():
    return render_template('docs.html')


@app.get('/tasks')
def get_tasks():
    return jsonify(get_all_plain_tasks(_tasks)), 200


@app.get('/tasks/<string:task_id>')
def get_task(task_id):
    task = _tasks.get(task_id)
    if not task:
        return jsonify({'message': f'Task not found with _id: {task_id}'}), 404
    return convert_to_plain_task(task_id, _tasks[task_id])


@app.post('/tasks')
def add_task():
    data = request.json

    if not data:
        abort(400)

    try:
        validate_task(data, method=request.method)
        task_info = parse_task(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 422

    task_id = str(uuid.uuid4())
    task = {task_id: task_info}
    _tasks.update(task)
    save_tasks()
    return convert_to_plain_task(task_id, task_info), 200


@app.put('/tasks/<string:task_id>')
def update_task(task_id):
    if task_id not in _tasks:
        return jsonify({'message': f'Task not found with _id: {task_id}'}), 404

    data = request.json

    if not data:
        abort(400)

    try:
        validate_task(data, method=request.method)
        task_info = parse_task(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 422

    _tasks[task_id].update(task_info)
    save_tasks()
    return convert_to_plain_task(task_id, _tasks[task_id]), 200


@app.delete('/tasks/<string:task_id>')
def delete_task(task_id):
    if task_id not in _tasks:
        return jsonify({'message': f'Task not found with _id: {task_id}'}), 404
    del _tasks[task_id]
    return jsonify({'message': 'Item deleted successfully'}), 200


if __name__ == '__main__':
    app.run(HOST, debug=DEBUG)
