from distutils.core import setup


f = open("multitools/__init__.py")
contents = f.read()
f.close()

info = {}
exec(contents, info)
info.pop('__builtins__')


setup(
    name='multitools',
    packages=['multitools'],
    author=info['__author__'],
    description='A python library that offers various different tools. ',
    version=info['__version__'],
)
