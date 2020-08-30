from celery.utils.log import get_task_logger


class LoggerTask:
    """ Base task class for all class based jobs
    """
    logger = None  # Task queue logger

    def __init__(self):
        if self.logger is None:
            self.logger = get_task_logger(__name__)

    def __call__(self):
        raise NotImplementedError
