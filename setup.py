from distutils.core import setup
import os


APPDATA = os.getenv('AppData') + '\\.pyCpp\\'

POINTER_DLL = """

"""

if not os.path.exists(APPDATA):
    os.mkdir(APPDATA)

if not os.path.exists(APPDATA + "pointer.dll"):
    dll = open(APPDATA + "pointer.dll", "x+")
    dll.write(POINTER_DLL)
    dll.close()


setup(
    name='multitools',
    packages=['multi_tools'],
    author='Jerem2360',
    description='A python library that offers various different tools. '
)
