annotationName = 'disambiguated-phrase'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    """ Receives a texterra-annotated annotated_text and returns its terms' list."""
    result = []
    if 'disambiguated-phrase' in document['annotations']:
        attributes = set()
        terms, ids, kbnames = [], [], []
        for term in document['annotations']['disambiguated-phrase']:
            term_id = term['value']['id']
            kb_name = term['value']['kb-name']
            ids.append(term_id)
            kbnames.append(kb_name)
            attributes.add('url({0})'.format(kb_name[:2]))
            terms.append((term['start'], term['end'], document['text'][term['start']: term['end']], term_id))

        if len(ids) > 1:
            atrs = api.getAttributes(ids, kbnames, list(attributes))['elements']['object']
            urls = {}
            for at in atrs:
                urls[int(at['concept']['id'])] = at['attributes']['I-attribute']['url']['#text']

            for term in terms:
                result.append((term[0], term[1], term[2], urls[term[3]]))

        elif len(ids) == 1:
            atrs = api.getAttributes(ids, kbnames, list(attributes))
            url = atrs['elements']['object']['attributes']['I-attribute']['url']['#text']
            result = [(terms[0][0], terms[0][1], terms[0][2], url)]

    return result

