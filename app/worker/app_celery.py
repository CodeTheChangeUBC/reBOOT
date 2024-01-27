import traceback
from http import HTTPStatus

from celery.states import FAILURE, STARTED, SUCCESS

from reboot.celery import app

ATTEMPT_LIMIT = 5


def update_state(state, percent, http_status):
    print('{0!r} state: {1!r}, progress: {2!r}'.format(
        app.current_task.request.id, state, percent))
    app.current_task.update_state(state=state, meta={
        'state': state,
        'process_percent': percent,
        'status': http_status,
    })


def update_percent(percent):
    update_state(STARTED, percent, HTTPStatus.ACCEPTED)


def set_success():
    update_state(SUCCESS, 100, HTTPStatus.OK)


def set_failure(e):
    app.current_task.update_state(
        state=FAILURE,
        meta={
            'exc_type': type(e).__name__,
            'exc_message': traceback.format_exc().split('\n'),
            'state': FAILURE,
            'process_percent': 0,
            'status': HTTPStatus.BAD_REQUEST,
        })


class AppTask(app.Task):
    max_retries = 0
    # default_retry_delay = 10

    def on_success(self, retval, task_id, args, kwargs):
        set_success()
        print('{0!r} success: {1!r}'.format(task_id, retval))
        super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        set_failure(exc)
        print('{0!r} failed: {1!r}'.format(task_id, exc))
        super().on_failure(exc, task_id, args, kwargs, einfo)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} retry: {1!r}'.format(task_id, exc))
        return super().on_retry(exc, task_id, args, kwargs, einfo)
