# -*- coding: utf-8 -*-
annotationName = 'pos-token'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    """ Extracts part-of-speech tagged tokens from given texterra-annotated text. """
    pos_tokens = []
    if annotationName in document['annotations']:
        if rtype == 'token':
            for token in document['annotations'][annotationName]:
                pos_tokens.append((document['text'][token['start']: token['end']], token['value']['tag']))

        elif rtype == 'annotation':
            for token in document['annotations'][annotationName]:
                pos_tokens.append((token['start'], token['end'], token['value']['tag']))

        else:  # if rtype == 'full':
            for token in document['annotations'][annotationName]:
                pos_tokens.append((token['start'], token['end'], document['text'][token['start']: token['end']],
                                   token['value']['tag']))
    return pos_tokens
