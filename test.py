import time

import draft5
import _thread


def th_code():
    a = 10
    for i in range(10):
        a += 1
    print(a)


def th_code_empty():
    raise TypeError


tid = _thread.start_new_thread(th_code, ())

time.sleep(3)

