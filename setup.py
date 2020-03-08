from pathlib import Path
from setuptools import setup

setup(
    name='linestorect',
    version='0.1',

    py_modules=['rect'],

    license='MIT License',
    long_description=Path('README.md').read_text(),

    url='https://github.com/barahilia/linestorect',
    author='Ilia Barahovsky',
    author_email='barahilia@gmail.com'
)
