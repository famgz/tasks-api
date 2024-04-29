from flask import Flask, request, jsonify
from pathlib import Path
from config import source_dir, data_dir, tasks_path
from utils import json_
import uuid

HOST = '0.0.0.0'

tasks = json_(tasks_path)

app = Flask(__file__)


docs_msg = '''
<div style="max-width: 500px; margin: 1rem auto">
    <h1 style="text-align: center">Tasks api documentation</h1>
    <h2>Usage:</h2>
    <p><strong>GET</strong> all taks: /tasks</p>
    <p><strong>POST</strong> new task: /tasks with JSON body</p>
</div>
'''


@app.get('/')
def home():
    return docs_msg


@app.get('/tasks')
def get_tasks():
    return tasks


@app.post('/tasks')
def add_task():
    data = request.json
    if not (data.get('title'), data.get('category'), data.get('dueHour')):
        return

    task = {
        'id': str(uuid.uuid4()),
        'title':  data.get('title'),
        'category': data.get('category'),
        'completed': data.get('completed', False),
        'dueHour':  data.get('dueHour'),
    }
    tasks.append(task)
    return task


if __name__ == '__main__':
    app.run(HOST, debug=True)
