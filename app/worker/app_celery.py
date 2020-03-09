import celery
from celery.states import SUCCESS, FAILURE
from http import HTTPStatus

PROGRESS = 'PROGRESS'

ATTEMPT_LIMIT = 5


def update_state(state, percent, http_status):
    print('{0!r} state: {1!r}, progress: {2!r}'.format(
        celery.current_task.request.id, state, percent))
    celery.current_task.update_state(state=state, meta={
        'state': state,
        'process_percent': percent,
        'status': http_status,
    })


def update_percent(percent):
    update_state(PROGRESS, percent, HTTPStatus.ACCEPTED)


def set_success():
    update_state(SUCCESS, 100, HTTPStatus.OK)


def set_failure():
    update_state(FAILURE, 0, HTTPStatus.BAD_REQUEST)


class AppTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print('{0!r} success: {1!r}'.format(task_id, retval))
        super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))
        super().on_failure(exc, task_id, args, kwargs, einfo)
        set_failure()
