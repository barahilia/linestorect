from pathlib import Path
from setuptools import setup


setup(
    name='linestorect',
    version='0.1.0',
    license='MIT License',

    description='Discover rectangular in many lines',
    long_description=Path('README.md').read_text(),
    long_description_content_type="text/markdown",

    py_modules=['rect'],

    author='Ilia Barahovsky',
    author_email='barahilia@gmail.com',
    url='https://github.com/barahilia/linestorect',

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
