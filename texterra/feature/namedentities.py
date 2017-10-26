# -*- coding: utf-8 -*-
annotationName = 'named-entity'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    """ Extracts named entities in specified format from given texterra-annotated text."""
    entities = []
    if annotationName in document['annotations']:

        if rtype == 'entity':
            for token in document['annotations'][annotationName]:
                entities.append((document['text'][token['start']: token['end']], token['value']['tag']))

        else:  # rtype == 'full':
            for token in document['annotations'][annotationName]:
                entities.append((token['start'], token['end'], document['text'][token['start']: token['end']],
                                 token['value']['tag']))
    return entities
