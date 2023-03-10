import time
from Profyer import celery_app
from celery import shared_task
from .models import Page, Category, Question, Option, UserAnswer


# @shared_task(name='up to one quantity')
@celery_app.task(name='add_answers')
def add_ans(data):
    time.sleep(10)
    state = {'error': False}
    user_answer, created = UserAnswer.objects.get_or_create(user_id=data.get('user'), question_id=data.get('question'))
    if user_answer is None:
        state['error'] = True
        return state
    for i in data.get('answer'):
        user_answer.answer.add(i)
    return state
