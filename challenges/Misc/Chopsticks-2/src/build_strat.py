from setuptools import setup
from Cython.Build import cythonize

from pathlib import Path

# python build_strat.py build_ext --inplace

setup(
    ext_modules = cythonize(
        str(Path(__file__).parent.resolve()/"strat.pyx"))
)