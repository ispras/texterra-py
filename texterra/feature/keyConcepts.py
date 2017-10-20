annotationName = 'keyconcepts'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    """ Receives a texterra-annotated text and returns the list of kb-article links for that text's concepts. """
    result = []
    if 'keyconcepts' in document['annotations']:
        ids, kbnames = [], []
        weights = {}
        attributes = set()
        for entry in document['annotations'][annotationName]:
            for concept in entry['value']:
                attributes.add('url({0})'.format(concept['concept']['kb-name'][:2]))
                ids.append(concept['concept']['id'])
                kbnames.append(concept['concept']['kb-name'])
                weights[concept['concept']['id']] = concept['weight']

        if len(ids) > 1:
            concepts = []
            atrs = api.get_attributes(ids, kbnames, list(attributes))['elements']['object']
            for at in atrs:
                concepts.append((weights[int(at['concept']['id'])],
                                 at['attributes']['I-attribute']['url']['#text']))
            concepts.sort(key=lambda x: -x[0])
            result = [c[1] for c in concepts]

        elif len(ids) == 1:
            atrs = api.get_attributes(ids, kbnames, list(attributes))['elements']['object']
            result = [atrs['attributes']['I-attribute']['url']['#text']]

    return result

