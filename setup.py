# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PanelJamDataExtractor-FRANCESCO-CELENZA",
    author="Francesco Celenza",
    version = "1.7.2",
    author_email="francesco.celenza98@gmail.com",
    description="A set of Python script to scrape data from PanelJam.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/collab-uniba/PanelJamDataExtractor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)