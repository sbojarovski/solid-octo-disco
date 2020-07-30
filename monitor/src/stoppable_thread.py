import threading


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(args=args, kwargs=kwargs)
        self._stop_event = threading.Event()

    # https://stackoverflow.com/a/325528/401043
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
