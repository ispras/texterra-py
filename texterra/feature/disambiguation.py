annotationName = 'disambiguated-phrase'


def params():
    return {'targetType': annotationName}


def process(document, rtype=None, api=None):
    """ Receives a texterra-annotated annotated_text and returns its terms' list."""
    result = []
    if 'disambiguated-phrase' in document['annotations']:
        terms, ids, kbnames = [], [], []
        for term in document['annotations']['disambiguated-phrase']:
            term_id = term['value']['id']
            kb_name = term['value']['kb-name']
            ids.append(term_id)
            kbnames.append(kb_name)
            terms.append((term['start'], term['end'], document['text'][term['start']: term['end']],
                          '{0}:{1}'.format(term_id, kb_name)))

        if len(ids) > 0:
            atrs = api._get_attributes(ids, kbnames, ['url'])
            for term in terms:
                result.append((term[0], term[1], term[2], atrs[term[3]]['url']))

    return result

