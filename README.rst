Texterra Python Interface
=========================

This package provides a Python interface for Texterra API.
Texterra is a toolkit for natural language processing and knowledge base utilization,
developed by the Ivannikov Institute for System Programming.

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

To install this SDK run::

    python setup.py install

or you can install using pip::

    pip install texterra


Documentation
-------------

You can use pydoc to list available services::

    pydoc texterra

and check documentation of methods for each service::

    pydoc texterra.texterra


Usage
-----

To use Texterra API in your project, simply import it like this:: 

    import texterra

Now you can create an access object using your API key::

    t = texterra.API('YOURKEY')

To access different tools just call the corresponding method::

    tags = t.pos_tagging('Hello World') 
    # You can also invoke Texterra with custom request: 
    result = t.custom_query(path, params) # for GET request 
    result = t.custom_query(path, params, headers, json) # for POST request

