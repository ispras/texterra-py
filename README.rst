Texterra Python Interface
=========================

.. image:: https://img.shields.io/github/license/ispras/texterra-py.svg?style=flat-square
    :target: https://img.shields.io/github/license/ispras/texterra-py.svg
    :alt: License

.. image:: https://img.shields.io/pypi/v/texterra.svg?style=flat-square
    :target: https://pypi.python.org/pypi/texterra
    :alt: pypi Version

This package provides a Python interface for Texterra API.
Texterra is a toolkit for natural language processing and knowledge base utilization,
developed by a team of researchers at the Ivannikov Institute for System Programming.

See https://texterra.ispras.ru for more information about Texterra project.


Features
--------

* Language detection
* Tokenization
* Lemmatization
* Sentence boundary detection
* Part-of-speech tagging
* Named entity recognition
* Labelled dependency parsing
* Term disambiguation
* Key concepts extraction
* Subjectivity detection
* Sentiment analysis
* Spelling correction

Currently, 2 languages are supported: English and Russian.


Installation
------------

To install this SDK run:

.. code:: bash

    python setup.py install

or you can install using pip:

.. code:: bash

    pip install texterra


Documentation
-------------

You can use pydoc to get help on the package:

.. code:: bash

    pydoc texterra

and check the documentation of methods:

.. code:: bash

    pydoc texterra.api


Usage
-----

To use Texterra API in your project, you first need to get an API key `here <https://api.ispras.ru/products>`_.
Then, ``import`` the package and use your API key to create an access object:

.. code:: python

    import texterra
    t = texterra.API('YOURKEY')

To access different tools, simply call the corresponding method:

.. code:: python

    tags = t.pos_tagging('Hello World')

Methods also accept iterables:

.. code:: python

    tagged_sents = t.pos_tagging(['Flat is better than nested.', 'Now is better than never.'])

