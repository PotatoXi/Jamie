# -*- coding: utf-8 -*-
"""
@Author : Jamie
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(

    name="jamie_test",
    version="0.1.1",
    author="Jamie",
    long_description="README.md",
    long_description_content_type="text/markdown",
    license="BSD",
    url="https://github.com/PotatoXi/Jamie",

    install_requires=[
        "numpy", "pandas", "shapely", "geopandas", "scipy", "matplotlib"
    ],

    package_dir={'Jamie': 'src/jamie_hello'},
    packages=['Jamie'],
    python_requires=">=3.6",
)