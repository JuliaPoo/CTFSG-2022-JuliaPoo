from setuptools import setup
from Cython.Build import cythonize

# python solve.py build_ext --inplace

import sys
sys.setrecursionlimit(10**6)

setup(
    ext_modules = cythonize("chal.pyx")
)

import chal # Solve!