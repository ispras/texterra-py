# -*- coding: utf-8 -*-
annotationName = 'lemma'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    """ Extracts lemmas in specified format from given texterra-annotated text. """
    lemmas = []
    if annotationName in document['annotations']:
        if rtype == 'annotation':
            for token in document['annotations'][annotationName]:
                lemmas.append((token['start'], token['end'], token['value']))

        elif rtype == 'lemma':
            for token in document['annotations'][annotationName]:
                lemmas.append(token['value'])

        else:  # if rtype == 'full':
            for token in document['annotations'][annotationName]:
                lemmas.append((token['start'], token['end'], document['text'][token['start']: token['end']],
                               token['value']))
    return lemmas
