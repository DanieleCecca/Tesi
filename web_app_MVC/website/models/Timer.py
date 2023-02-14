import time

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    def __init__(self):
        self._start_time = 0
        self.elapsed_time=0

    def start(self):
        """Start a new timer"""
        if self._start_time is not 0:
           print(f"Timer is running. Use .stop() to stop it")
        else:
            self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is 0:
            raise TimerError(f"Timer is not running. Use .start() to start it")
        self._start_time = 0
        self.elapsed_time=0

        
    def get_time(self):
        self.elapsed_time = int(time.perf_counter() - self._start_time)
        return self.elapsed_time
    
    