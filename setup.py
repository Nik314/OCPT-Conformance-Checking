from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name="fast_hash",
    ext_modules=cythonize("fast_hash.pyx", language_level="3"),
    include_dirs=[numpy.get_include()],
)