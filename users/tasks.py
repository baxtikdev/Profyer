import time
from Profyer import celery_app
from celery import shared_task
from .models import UserVote


@shared_task(name='partial_update')
def partial_update(id, data, type):
    time.sleep(10)
    instance = UserVote.objects.get(id=id)
    if type == 'number':
        instance.vote_number = data
    elif type == 'sex':
        instance.sex = data
    elif type == 'age':
        instance.age = data
    instance.save()
    return
