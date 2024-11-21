from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='kam12filereader',
    version='3.1',
    long_description=Path('README.md').read_text(),
    author='Dara TOUCH',
    author_email='touchdara2015@live.com',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'numpy>=1.26.1',
        'pandas>= 2.2.1',
        'openpyxl>=3.1.2',
        ],
    package_data={
        '': ['data/*.csv'],  # Include all CSV files in data directory
        },
    include_package_data=True,  # This line is needed to include non-python files
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.11',
    ],
)