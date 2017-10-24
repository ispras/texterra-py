# -*- coding: utf-8 -*-
from .. import syntaxtree

annotationName = 'syntax-relation'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    if annotationName in document['annotations']:
        return syntaxtree.SyntaxTree(document)
    else:
        return None
