# -*- coding: utf-8 -*-
annotationName = 'keyconcepts'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    """ Receives a texterra-annotated text and returns the list of kb-article links for that text's concepts. """
    result = []
    if 'keyconcepts' in document['annotations']:
        ids, kbnames = [], []
        weights = {}
        for entry in document['annotations'][annotationName]:
            for concept in entry['value']:
                concept_id = concept['concept']['id']
                kb_name = concept['concept']['kb-name']
                ids.append(concept_id)
                kbnames.append(kb_name)
                weights['{0}:{1}'.format(concept_id, kb_name)] = concept['weight']

        if len(ids) > 0:
            concepts = []
            atrs = api._get_attributes(ids, kbnames, ['url'])
            for at in atrs:
                concepts.append((weights[at], atrs[at]['url']))
            concepts.sort(key=lambda x: -x[0])
            result = [c[1] for c in concepts]

    return result
