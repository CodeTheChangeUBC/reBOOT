from celery import current_task
from celery.states import SUCCESS


def update_state(state, percent):
    current_task.update_state(state=state, meta={
        'state': state,
        'process_percent': percent
    })


def update_percent(percent):
    update_state('PROGRESS', percent)


def set_complete():
    update_state(SUCCESS, 100)
