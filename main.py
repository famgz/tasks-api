from flask import Flask, abort, request, jsonify, render_template
from config import tasks_path
from utils import json_
from tools import validate_task, convert_to_plain_task
import uuid

HOST = '0.0.0.0'
DEBUG = False
WRITE_TO_JSON = False


tasks = json_(tasks_path)

app = Flask(__file__)
app.json.sort_keys = False


def save_tasks():
    if not WRITE_TO_JSON:
        return
    json_(tasks_path, tasks,
          ensure_ascii=False, sort_keys=False, indent=2)


@app.get('/')
def home():
    return render_template('docs.html')


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
