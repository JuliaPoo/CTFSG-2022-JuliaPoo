from setuptools import setup
from Cython.Build import cythonize

# python gen_strat.py build_ext --inplace

setup(
    ext_modules = cythonize("gen_strat.pyx")
)

import gen_strat
gen_strat.main()