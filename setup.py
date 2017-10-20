import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name="texterra",
    desciption="API for natural language processing.",
    version='1.0.0',
    url="https://texterra.ispras.ru",
    long_description="""Texterra API provides tools for natural language processing and knowledge base utilization.""",
    license="Apache License, Version 2.0",
    keywords=['natural language processing', 'text processing', 'parsing', 'tagging', 'tokenizing', 'syntax',
              'language', 'lemmatization', 'named entity recognition', 'spelling correction', 'sentiment analysis',
              'disambiguation', 'key concepts detection'],
    classifiers=['Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'License :: Apache License, Version 2.0',
                 'Programming Language :: Python',
                 'Topic :: Software Development',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Text Processing',
                 'Topic :: Text Processing :: Linguistic',
                 'Operating System :: OS Independent',
                 'Natural Language :: English',
                 'Natural Language :: Russian',
                 'Programming Language :: Python :: 3'
                 ],
    author="",
    author_email="texterra@ispras.ru",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests',
        'xmltodict'
    ],
    py_modules=['texterra'],
    python_requires=">=3"
)
