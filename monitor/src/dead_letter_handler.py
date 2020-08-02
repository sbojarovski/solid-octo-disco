import logging
import time

import src.settings as settings
from src.stoppable_thread import StoppableThread
from src.resource_dispatcher import ResourceDispatcher

log = logging.getLogger(__name__)


class DeadLetterHandler(StoppableThread):
    """
    This class is responsible for reattempting to write events to the database.
    On a regular time interval it checks if the DLQ is not empty, and retries the insert.
    """
    def __init__(self,
                 *args,
                 model_mapper,
                 dispatcher: ResourceDispatcher = None,
                 **kwargs):
        super().__init__(args=args, kwargs=kwargs)

        self.seconds = settings.DEAD_LETTER_RETRY_SECONDS
        self.dispatcher = dispatcher
        self.model_mapper = model_mapper

    def run(self) -> None:
        while True:
            time.sleep(self.seconds)

            while len(self.dispatcher.dead_letter_queue):
                self.handle_queue()

            if self.stopped():
                return

    def handle_queue(self):
        with self.dispatcher.lock:
            try:
                num_records = len(self.dispatcher.dead_letter_queue)
                self.model_mapper.bulk_create(self.dispatcher.dead_letter_queue)
                self.dispatcher.dead_letter_queue.clear()
                log.info(f'Saved {num_records} to database')
            except Exception as e:
                log.error('Could not save DLQ to database')
                log.exception(e)
