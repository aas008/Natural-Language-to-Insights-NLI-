# setup.py
from setuptools import setup, find_packages

setup(
    name="nli",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "argparse",
    ],
    entry_points={
        'console_scripts': [
            'nli=src.cli:main',
        ],
    },
)