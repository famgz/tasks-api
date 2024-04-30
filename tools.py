import re

MAX_CHARS = 50

TASK_KEYS = [
    'title',
    'category',
    'completed',
    'dueHour'
]


def is_valid_time_format(time_str):
    pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    return bool(pattern.match(time_str))


def check_keys(task_info):
    valid_keys = [key for key in task_info if key in TASK_KEYS]

    if not valid_keys:
        raise ValueError(
            'No valid fields to update')

    return valid_keys


def validate_task(task_info, method):
    valid_keys = check_keys(task_info)

    if method == 'POST':
        missing_keys = [key for key in TASK_KEYS if key not in valid_keys]
        if missing_keys:
            raise ValueError(
                f'All fields must be given. Missing: {" ".join(missing_keys)}')

    title = task_info.get('title')
    category = task_info.get('category')
    completed = task_info.get('completed')
    dueHour = task_info.get('dueHour')

    if method == 'POST' and not (title and category and dueHour):
        raise ValueError(
            'These fields cannot be missing or empty: title, category, dueHour')

    for value in [title, category, dueHour]:
        if value is not None and not isinstance(value, str):
            raise TypeError(f'Invalid data type {type(value)}: {value}')

    if completed is not None and not isinstance(completed, bool):
        raise TypeError(f'Invalid data type {type(completed)}: {completed}')

    if dueHour is not None and not is_valid_time_format(dueHour):
        raise ValueError('dueHour must be in the following format: <HH:MM>')


def parse_task(task_info):
    valid_keys = check_keys(task_info)

    parsed_info = {}
    for key in valid_keys:
        value = task_info.get(key)
        if key in ['title', 'category']:
            value = value[:MAX_CHARS]
        parsed_info[key] = value

    return parsed_info


def convert_to_plain_task(task_id: str, task_info: dict):
    plain_task = {'_id': task_id}
    plain_task.update(task_info)
    return plain_task
