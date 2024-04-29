from pathlib import Path
from utils import json_

source_dir = Path(__file__).parent.resolve()

data_dir = Path(source_dir, 'data')

tasks_path = Path(data_dir, 'tasks.json')

if not data_dir.exists():
    data_dir.mkdir()

if not tasks_path.exists():
    json_(tasks_path, [])
