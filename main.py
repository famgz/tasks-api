from flask import Flask
from pathlib import Path
from config import source_dir, data_dir, tasks_path
from utils import json_

HOST = '0.0.0.0'

tasks = json_(tasks_path)

app = Flask(__file__)


@app.get('/tasks')
def get_tasks():
    return 'Tasks api is running'


if __name__ == '__main__':
    app.run(HOST, debug=True)
