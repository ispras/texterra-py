from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Read the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="texterra",
    version='1.0.0',
    description="API for natural language processing.",
    long_description=long_description,
    url="https://texterra.ispras.ru",
    license="Apache License, Version 2.0",
    keywords=['natural language processing', 'nlp', 'text processing', 'parsing', 'tagging', 'tokenizing', 'syntax',
              'language', 'lemmatization', 'named entity recognition', 'spelling correction', 'sentiment analysis',
              'disambiguation', 'key concepts detection'],
    classifiers=['Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Topic :: Software Development',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Text Processing',
                 'Topic :: Text Processing :: Linguistic',
                 'Operating System :: OS Independent',
                 'Natural Language :: English',
                 'Natural Language :: Russian',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3'
                 ],
    author="Tsolak Ghukasyan",
    author_email="texterra@ispras.ru",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests',
        'six'
    ],
    py_modules=['texterra']
)
