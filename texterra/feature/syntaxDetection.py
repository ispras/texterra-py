from .. import syntaxTree

annotationName = 'syntax-relation'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    if annotationName in document['annotations']:
        return syntaxTree.SyntaxTree(document)
    else:
        return None
