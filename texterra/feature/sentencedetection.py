# -*- coding: utf-8 -*-
annotationName = 'sentence'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    """ Extracts sentences in specified format from given texterra-annotated text. """
    sents = []
    if annotationName in document['annotations']:
        if rtype == 'sentence':
            for sent in document['annotations'][annotationName]:
                sents.append(document['text'][sent['start']: sent['end']])

        elif rtype == 'annotation':
            for sent in document['annotations'][annotationName]:
                sents.append((sent['start'], sent['end']))

        else:  # if rtype == 'full':
            for sent in document['annotations'][annotationName]:
                sents.append((sent['start'], sent['end'], document['text'][sent['start']: sent['end']]))
    return sents
