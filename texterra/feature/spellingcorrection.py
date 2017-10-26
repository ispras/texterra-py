# -*- coding: utf-8 -*-
annotationName = 'spelling-correction-token'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    """ Extracts spelling-corrected tokens in specified format from given texterra-annotated text. """
    corrected_tokens = []
    if annotationName in document['annotations']:
        if rtype == 'annotation':
            for token in document['annotations'][annotationName]:
                corrected_tokens.append((token['start'], token['end'], token['value']))

        elif rtype == 'token':
            for token in document['annotations'][annotationName]:
                corrected_tokens.append((document['text'][token['start']: token['end']], token['value']))

        else:  # rtype == 'full'
            for token in document['annotations'][annotationName]:
                corrected_tokens.append((token['start'], token['end'], document['text'][token['start']: token['end']],
                                         token['value']))
    return corrected_tokens
