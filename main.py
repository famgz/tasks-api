from flask import Flask, abort, request, jsonify
from pathlib import Path
from config import source_dir, data_dir, tasks_path
from utils import json_
from tools import validate_task, convert_to_plain_task
import uuid

HOST = '0.0.0.0'
DEBUG = True

tasks = json_(tasks_path)

app = Flask(__file__)
app.json.sort_keys = False


docs_msg = '''
<div style="max-width: 500px; margin: 1rem auto">
    <h1 style="text-align: center">Tasks api documentation</h1>
    <h2>Usage:</h2>
    <p><strong>GET</strong> all tasks: /tasks</p>
    <p><strong>GET</strong> one task: /tasks/<task_id></p>
    <p><strong>POST</strong> new task: /tasks with JSON body</p>
</div>
'''


def save_tasks():
    json_(tasks_path, tasks, backup=True,
          ensure_ascii=False, sort_keys=False, indent=2)


@app.get('/')
def home():
    return docs_msg


@app.get('/tasks')
def get_tasks():
    return [convert_to_plain_task(task_id, task_info) for task_id, task_info in tasks.items()]


@app.get('/tasks/<string:task_id>')
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'message': f'Task not found: {task_id}'}), 422
    return convert_to_plain_task(task_id, task[task_id])


@app.post('/tasks')
def add_task():
    data = request.json

    if not data:
        abort(400)

    try:
        validate_task(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 422

    task_id = str(uuid.uuid4())

    task = {
        task_id: {
            'title':  data.get('title'),
            'category': data.get('category'),
            'completed': data.get('completed', False),
            'dueHour':  data.get('dueHour'), }
    }
    tasks.update(task)
    save_tasks()
    return convert_to_plain_task(task), 200


if __name__ == '__main__':
    app.run(HOST, debug=DEBUG)
