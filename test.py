from draft5._internal import overwrite, secretattr


import sys
import _thread


print(dir(sys.settrace))
print(sys.gettrace)
print(_thread.start_new_thread)

print(secretattr.dir(sys.settrace))

