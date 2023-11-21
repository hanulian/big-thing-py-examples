from big_thing_py.utils import *


class Timer:
    def __init__(self, timeout: float = None) -> None:
        self.timeout = timeout
        self.is_set = False
        self._timer_thread = None

    def timer_start(self) -> bool:
        if not self._timer_thread or not self._timer_thread.is_alive():
            self._timer_thread = MXThread(target=self.timeout_thread_func)
            MXLOG_DEBUG(f'{self.timeout} sec timer started', 'yellow')
            self._timer_thread.start()

            # wait until thread is started
            while not self._timer_thread.is_alive():
                time.sleep(THREAD_TIME_OUT)
        else:
            MXLOG_DEBUG('timer is already started', 'yellow')

        return True

    def set_timer(self, timeout: float) -> float:
        self.timeout = timeout
        self.is_set = False
        return self.timeout

    def timeout_thread_func(self) -> None:
        while True:
            time.sleep(THREAD_TIME_OUT * 100)
            self.timeout -= THREAD_TIME_OUT * 100
            if self.timeout <= 0:
                break

        self.is_set = True
        MXLOG_DEBUG(f'timer ended', 'yellow')
