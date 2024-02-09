import _thread
import time

def th_code():
    time.sleep(3)


_thread.start_new_thread(th_code, ())

from draft5 import _internal


time.sleep(5)

