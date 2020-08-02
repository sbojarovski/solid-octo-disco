from typing import List
from threading import RLock


class ResourceDispatcher:
    """
    Provides resources that can be accessed by multiple threads.

    Uses a reentrable lock for thread-safety.
    """

    def __init__(self,
                 dead_letter_queue: List = None,
                 ):
        self._dead_letter_queue = dead_letter_queue
        self._lock = RLock()

    @property
    def dead_letter_queue(self) -> List:
        return self._dead_letter_queue

    @dead_letter_queue.setter
    def dead_letter_queue(self, value: List) -> None:
        self._dead_letter_queue = value

    @property
    def lock(self):
        return self._lock
