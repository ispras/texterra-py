# -*- coding: utf-8 -*-
annotationName = 'subjectivity'


def params():
    return {'targetType': annotationName, 'tweet': 1}


def process(document, rtype=None, api=None):
    """ Detects subjectivity in given batch of texts. """
    """ Extracts subjectivity value from given texterra-annotated text. """
    return bool(document['annotations'])
