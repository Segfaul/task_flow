from time import sleep

from config.celery import app
from .models import Task

@app.task
def process_task(task_id):

    task = Task.objects.get(id=task_id)
    task.status = 'processing'
    task.save()

    sleep(5)

    task.status = 'completed'
    task.save()

    return {'task_id': task_id, 'status': task.status, 'execution_time': 5}
