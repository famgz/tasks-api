from flask import Flask
from pathlib import Path
from config import source_dir, data_dir, tasks_path
from utils import json_

HOST = '0.0.0.0'

tasks = json_(tasks_path)

app = Flask(__file__)


docs_msg = '''
<div style="max-width: 1024px; margin: 1rem auto">
    <h1>Tasks api documentation</h1>
    <p>Usage:</p>
    <span>GET all taks: /tasks</span>
</div>
'''


@app.get('/')
def home():
    return docs_msg


@app.get('/tasks')
def get_tasks():
    return tasks


if __name__ == '__main__':
    app.run(HOST, debug=True)
