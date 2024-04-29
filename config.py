from pathlib import Path

source_dir = Path(__file__).parent.resolve()

data_dir = Path(source_dir, 'path')

tasks_path = Path(data_dir, 'tasks.json')
