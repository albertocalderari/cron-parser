from distutils.core import setup

from setuptools import find_packages

with open("./requirements.txt") as f:
    requirements = [l for l in f.readlines() if not l.startswith("#")]

setup(
    name='cronparser',
    version='0.1.0',
    packages=find_packages(include=["cronparser", "cronparser.*"], exclude=["tests"]),
    install_requires=[requirements],
    entry_points={
        'console_scripts': ['cronparser=cronparser.main:main']
    }
)
