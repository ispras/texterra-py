annotationName = 'language'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    try:
        return document['annotations'][annotationName][0]['value']
    except KeyError:
        return ''
