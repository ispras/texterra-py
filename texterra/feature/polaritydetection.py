# -*- coding: utf-8 -*-
annotationName = ['domain', 'polarity']


def params():
    return {'targetType': ['domain', 'polarity'], 'tweet': 1}


def process(document, rtype=None, api=None):
    """ Extracts polarity and domain values from given texterra-annotated text. """
    try:
        return document['annotations'][annotationName[1]][0]['value'], \
               document['annotations'][annotationName[0]][0]['value']
    except KeyError:
        if 'domain' in document['annotations']:
            return 'NEUTRAL', document['annotations'][annotationName[0]][0]['value']
        else:
            return 'NEUTRAL', 'general'
