import re


def is_valid_time_format(time_str):
    pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    return bool(pattern.match(time_str))


def validate_task(task):
    title = task.get('title')
    category = task.get('category')
    completed = task.get('completed')
    dueHour = task.get('dueHour')

    if not (title and category and dueHour):
        raise ValueError(
            'These fields cannot be missing or empty: title, category, dueHour')

    if not is_valid_time_format(dueHour):
        raise ValueError('dueHour must be in a valid format: <HH:MM>')

    return True


def convert_to_plain_task(task: dict):
    task_id = next(iter(task))
    plain_task = {
        'id': task_id,
    }
    plain_task.update(task[task_id])
    return plain_task
