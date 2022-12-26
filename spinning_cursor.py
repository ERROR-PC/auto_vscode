"""Spinning cursor class defined here"""

import threading
from time import sleep

class SpinningCursor:
    """A spinning cursor"""
    def __init__(self) -> None:
        self.delay = 0.3
        self.busy = True
        self.thread = None

    @staticmethod
    def cursor_frames():
        """Generator of frames"""
        while True:
            for frame in '-/|\\':
                yield frame

    def print_cycle(self):
        """Prints the next frame from cursor frames"""
        for frame in self.cursor_frames():
            print(frame, end='', flush=True)
            sleep(self.delay)
            print('\b', end='', flush=True)
            if not self.busy:
                return

    def __enter__(self):
        self.busy = True
        self.thread = threading.Thread(target=self.print_cycle, daemon=True)
        self.thread.start()

    def __exit__(self, exception, _value, _tb):
        self.busy = False
        if self.thread is not None:
            self.thread.join()
            # Newline after spinning cursor
            print()
        if exception is not None:
            return False
