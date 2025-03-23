from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pytest-reporter-html",
    version="0.1.0",
    author="Claude Assistant",
    author_email="info@example.com",
    description="A pytest plugin that generates comprehensive HTML and JSON test reports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/armandocodedev/pytest-reporter-html",
    packages=find_packages(),
    classifiers=[
        "Framework :: Pytest",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pytest>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pytest-reporter=pytest_reporter_html.cli:main",
        ],
        "pytest11": [
            "reporter-html = pytest_reporter_html.plugin",
        ],
    },
)