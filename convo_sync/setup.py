#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# Read the long description from README
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='convo_sync',
    version='1.0.0',
    description='AI Conversation Data Processing Toolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Cagedbird',
    author_email='',
    url='https://github.com/cagedbird/convo_sync',
    license='MIT',
    
    packages=find_packages(),
    
    python_requires='>=3.7',
    
    entry_points={
        'console_scripts': [
            'convo_sync=convo_sync:main',
        ],
    },
    
    keywords=[
        'conversation',
        'json',
        'markdown',
        'data-processing',
        'ai',
    ],
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ],
    
    project_urls={
        'Bug Reports': 'https://github.com/cagedbird/convo_sync/issues',
        'Source': 'https://github.com/cagedbird/convo_sync',
        'Documentation': 'https://github.com/cagedbird/convo_sync/blob/main/README.md',
    },
)
