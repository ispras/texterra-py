# -*- coding: utf-8 -*-
annotationName = 'pos-token'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    """ Extracts tokens in specified format from given texterra-annotated text. """
    tokens = []
    if annotationName in document['annotations']:
        if rtype == 'token':
            for token in document['annotations'][annotationName]:
                tokens.append(document['text'][token['start']: token['end']])

        elif rtype == 'annotation':
            for token in document['annotations'][annotationName]:
                tokens.append((token['start'], token['end']))

        else:  # if rtype == 'full':
            for token in document['annotations'][annotationName]:
                tokens.append((token['start'], token['end'], document['text'][token['start']: token['end']]))

    return tokens
