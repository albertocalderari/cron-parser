from distutils.core import setup

from setuptools import find_packages

setup(
    name='cronparser',
    version='0.1.0',
    packages=find_packages(include=["cronparser", "cronparser.*"], exclude=["tests"]),
    install_requires=["marshmallow-dataclass==8.5.3"],
    entry_points={
        'console_scripts': ['cronparser=cronparser.main:main']
    }
)
