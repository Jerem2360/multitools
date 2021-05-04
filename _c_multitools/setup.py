from distutils.core import setup, Extension

_c_maths_ext = Extension(
    name="_c_maths",
    sources=["_c_maths.c"]
)

setup(
    name='_c_multitools',
    ext_modules=[_c_maths_ext],
    author='Jerem2360',
    description='The c extensions that are absolutely necessary for multitools to work correctly. '
)
