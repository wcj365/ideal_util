#/usr/bin/env python3

import re
from setuptools import setup, find_packages


def get_version():
    with open('gao_st/__init__.py', 'r') as f:
        content = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string in __init__.py.")


def get_requirements():
    with open('requirements.txt', 'r') as f:
        return f.read().splitlines()


setup(
    name='gao-st',  # use "-" instead of "_" only to satisfy Python Package Index
    version=get_version(),
    packages=find_packages(),
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    install_requires=get_requirements(),
    author='Dr. Chaojie (jay) Wang',
    author_email='wangc1@gao.gov',
    description='Common utilities for Streamlit apps.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://git.gao.gov/WangC1/gao_st',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
