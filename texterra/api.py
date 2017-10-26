# -*- coding: utf-8 -*-
"""
Tools for Natural Language Processing.
"""
import sys
import six
from os import getenv
from . import feature
from . import utils


class API(utils.HttpBase):
    """
    This class provides methods for natural language processing with Texterra REST via OpenAPI.
    """

    # default texterra path
    texterra_version = 'v1'
    texterra_url = 'https://api.ispras.ru/texterra/{0}/'.format(texterra_version)

    max_batch_size = 1000000

    def __init__(self, key=getenv('TEXTERRA_KEY', False), host=getenv('TEXTERRA_HOST', None)):
        """
        Provide an API key to use the default Texterra version (v1).
        For a different version of Texterra, specify a custom host.

        :type key: str
        :type host: str
        """
        if host is None:
            host = self.texterra_url

            if key is None or len(key) != 40:
                raise ValueError('Invalid API key. Please provide a proper API key.')

        super(API, self).__init__(key, host)

    # NLP methods

    def language_detection(self, texts):
        """
        Detects given texts' language.

        :param texts: the texts to be language detected
        :type texts: list(str) or str
        :return: yields given texts' ISO 639-1 language codes
        :rtype: str generator
        """
        return self._process_texts(texts, feature.languagedetection)

    def sentence_detection(self, texts, rtype='full', domain='', language=''):
        """
        Detects boundaries of sentences in given texts.

        :param texts: the texts to be sentence tokenized
        :type texts: list(str) or str
        :param rtype: sets return type (the default is 'full'):
                     - 'sentence': list(str), i.e. list of detected sentences
                     - 'annotation': list(tuple(int, int)), i.e. list of detected sentences' start, end indexes
                     - 'full': list(tuple(int, int, str))
        :type rtype: str
        :param domain: specifies texts' domain (auto-detect if not provided)
        :type domain: str
        :param language: texts' language ISO 639-1 code
        :type language: str
        :return: yields lists of tuples, where tuple contains a sentence's start, end indexes and its value
        :rtype: generator of list(tuple(int, int, str))
        """
        return self._process_texts(texts, feature.sentencedetection, rtype=rtype, domain=domain, language=language)

    def tokenization(self, texts, rtype='full', domain='', language=''):
        """
        Detects all tokens (minimal significant text parts) in given texts.

        :param texts: the texts to be tokenized.
        :type texts: list(str) or str
        :param rtype: sets return type (the default is 'full'):
                    - 'token': list(str), i.e. list of detected tokens
                    - 'annotation': list(tuple(int, int)), i.e. list of detected tokens' start, end indexes
                    - 'full': list(tuple(int, int, str))
        :type rtype: str
        :param domain: specifies texts' domain (auto-detect if not provided)
        :type domain: str
        :param language: texts' language ISO 639-1 code
        :type language: str
        :return: yields lists of tuples, where each tuple contains a token's start, end indexes and its value.
        :rtype: generator of list(tuple(int, int, str))
        """
        return self._process_texts(texts, feature.tokenization, rtype=rtype, domain=domain, language=language)

    def lemmatization(self, texts, rtype='full', domain='', language=''):
        """
        Detects each word's lemma in given texts.

        :param texts: the texts to lemmatize
        :type texts: list(str) or str
        :param rtype: sets return type (the default is 'full'):
                     - 'lemma': list(str), i.e. list of lemmas
                     - 'annotation': list(tuple(int, int, str)), i.e. list of lemmas’ start, end indexes and value
                     - 'full': list(tuple(int, int, str, str))
        :type rtype: str
        :param domain: specifies texts' domain (auto-detect if not provided)
        :type domain: str
        :param language: texts' language ISO 639-1 code
        :type language: str
        :return: yields lists of tuples, where each tuple contains a token’s start, end indexes, its value and lemma
        :rtype: generator of list(tuple(int, int, str, str))
        """
        return self._process_texts(texts, feature.lemmatization, rtype=rtype, domain=domain, language=language)

    def pos_tagging(self, texts, rtype='full', domain='', language=''):
        """
        Detects each token's part of speech tag in given texts.

        :param texts: the text to be pos-tagged
        :type texts: list(str) or str
        :param rtype: sets return type (the default is 'full'):
                     - 'token': list(tuple(str, str)), i.e. list of detected tokens and their tags
                     - 'annotation': list(tuple(int, int, str)), i.e. list of tokens’ start, end indexes and tag
                     - 'full': list(tuple(int, int, str, str))
        :type rtype: str
        :param domain: specifies texts' domain (auto-detect if not provided)
        :type domain: str
        :param language: texts' language ISO 639-1 code
        :type language: str
        :return: yields lists of tuples, where each tuple contains a token’s start, end indexes, value, and tag
        :rtype: generator of list(tuple(int, int, str, str))
        """
        return self._process_texts(texts, feature.postagging, rtype=rtype, domain=domain, language=language)

    def spelling_correction(self, texts, rtype='full', domain='', language=''):
        """
        Tries to correct spelling errors in given texts.

        :param texts: the text to be corrected
        :type texts: list(str) or str
        :param rtype: sets return type (the default is 'full'):
                     - 'token': list(tuple(str, str)), i.e. list of tokens and their corrections
                     - 'annotation': list(tuple(int, int, str)), i.e. list of tokens’ start, end indexes and correction
                     - 'full': list(tuple(int, int, str, str))
        :type rtype: str
        :param domain: specifies texts' domain (auto-detect if not provided)
        :type domain: str
        :param language: texts' language ISO 639-1 code
        :type language: str
        :return: yields lists of tuples, where each tuple contains a token’s start, end indexes,
                its value and correction
        :rtype: generator of list(tuple(int, int, str, str))
        """
        return self._process_texts(texts, feature.spellingcorrection, rtype=rtype, domain=domain, language=language)

    def named_entities(self, texts, rtype='full', domain='', language=''):
        """
        Finds all named entities occurrences in given texts.

        :param texts: the text to be analyzed
        :type texts: list(str) or str
        :param rtype: sets return type (the default is 'full'):
                     - 'entity': list(tuple(str, str)), i.e. list of named entities and their BBN categories
                     - 'full': list(tuple(int, int, str, str))
        :type rtype: str
        :param domain: specifies texts' domain (auto-detect if not provided)
        :type domain: str
        :param language: texts' language ISO 639-1 code
        :type language: str
        :return: yields lists of tuples, where each tuple contains a named entity’s start, end indexes, value, and
                 BBN category
        :rtype: generator of list(tuple(int, int, str, str))
        """
        return self._process_texts(texts, feature.namedentities, rtype=rtype, domain=domain, language=language)

    def disambiguation(self, texts, domain='', language=''):
        """
        Detects the most appropriate meanings (concepts) for terms occurred in a given text.

        :param texts: the text to be disambiguated
        :type texts: list(str) or str
        :param domain: specifies texts' domain (auto-detect if not provided)
        :type domain: str
        :param language: texts' language ISO 639-1 code
        :type language: str
        :return: yields lists of tuples. Each tuple contains a term’s start, end indexes, value, and the link to
                 the corresponding article in KB.
        :rtype: generator of list(tuple(int, int, str, str))
        """
        return self._process_texts(texts, feature.disambiguation, domain=domain, language=language)

    def key_concepts(self, texts, domain='', language=''):
        """
        Key concepts are the concepts providing short (conceptual) and informative text description.
        This service extracts the key concepts for given texts.

        :param texts: the text to be analyzed
        :type texts: list(str) or str
        :param domain: specifies texts' domain (auto-detect if not provided)
        :type domain: str
        :param language: texts' language ISO 639-1 code
        :type language: str
        :return: yields lists of links to concepts' corresponding KB articles
                sorted by concept weight in descending order
        :rtype: generator of list(str)
        """
        return self._process_texts(texts, feature.keyconcepts, domain=domain, language=language)

    def subjectivity_detection(self, texts, domain='', language=''):
        """
        Detects for each of the given texts if it is subjective or not.

        :param texts: the texts to be analyzed
        :type texts: list(str) or str
        :param domain: specifies texts' domain (auto-detect if not provided)
        :type domain: str
        :param language: texts' language ISO 639-1 code
        :type language: str
        :return: yields True for subjective texts, otherwise False.
        :rtype: bool generator
        """
        return self._process_texts(texts, feature.subjectivitydetection, domain=domain, language=language)

    def polarity_detection(self, texts, domain='', language=''):
        """
        Detects whether given texts have positive, negative, or no sentiment, with respect to domain.
        If domain isn't provided, domain detection is applied, this way method tries to achieve best results.
        If no domain is detected general domain algorithm is applied.
        This method only accepts texts that are not empty and contain at least one non-whitespace character.

        :param texts: the texts to be analyzed
        :type texts: list(str) or str
        :param domain: domain
        :type domain: str
        :param language: texts' language ISO 639-1 code
        :type language: str
        :return: yields tuples containing a text's polarity and domain.
        :rtype: generator of tuple(str, str)
        """
        return self._process_texts(texts, feature.polaritydetection, domain=domain, language=language)

    def syntax_detection(self, sentences, domain='', language=''):
        """
        Detects syntax relations in given sentences.
        For sentences that are empty or contain only whitespace characters, returns None.

        :param sentences: the sentences to be parsed
        :type sentences: list(str) or str
        :param domain: domain
        :type domain: str
        :param language: texts' language ISO 639-1 code
        :type language: str
        :return: yields a SyntaxTree instance for each sentence
        :rtype: generator of SyntaxTree
        """
        return self._process_texts(sentences, feature.syntaxdetection, domain=domain, language=language)

    # KBM methods

    def _wrap_concepts(self, concepts, kbnames):
        """ Utility wrapper for matrix parameters """
        if isinstance(concepts, list):
            if isinstance(kbnames, list):
                return ''.join(['id={0}:{1};'.format(concept, kb) for concept, kb in zip(concepts, kbnames)])
            else:
                return ''.join(['id={0}:{1};'.format(concept, kbnames) for concept in concepts])
        else:
            return 'id={0}:{1};'.format(concepts, kbnames)

    def _get_attributes(self, concepts, kbnames, atr_list=None):
        """
        Get attributes for concepts(list or single concept, each concept is {id}, {kbname} is separate parameter).
        Supported attributes:
            'coordinates' - GPS coordinates
            'definition' - brief concept definition
            'url' or 'url(<language>)' - URL to page with description of the given concept on the specified language
            '<language>' - language code, like: en, de, fr, ko, ru, ...
            'synonym' - different textual representations of the concept
            'title' - concept title
            'translation(<language>)' textual representation of the concept on the specified language
            '<language>' - language code (e.g. en, de, fr, ko, ru, ...)
            'type' - concept type
        """
        params = {'attribute': atr_list or []}
        return self.get('walker/{}'.format(self._wrap_concepts(concepts, kbnames)), params)

    # Helper methods

    def _batch_query(self, texts, params):
        """ Invokes custom batch request to Texterra. Returns json. """
        result = self.post('nlp', params, json=texts)
        return result

    def _process_texts(self, texts, module, rtype=None, domain='', language=''):
        for batch in self._get_batches(texts):
            if len(batch) != 0:
                params = module.params()

                if language != '':
                    params['language'] = language

                if domain != '':
                    params['domain'] = domain

                for document in self._batch_query(batch, params):
                    yield module.process(document, rtype, api=self)

    def _get_batches(self, texts):
        """ Reads texts from iterator and yields in 1MB-size batches."""
        if isinstance(texts, six.string_types):
            self._check_size([texts])
            yield [{'text': texts}]
        else:
            batch = []
            for text in texts:
                if self._check_size(batch + [text]):
                    batch.append({'text': text})
                else:
                    yield batch
                    batch = [{'text': text}]
                    self._check_size(batch)
            yield batch

    def _check_size(self, texts):
        """ Checks that texts don't exceed memory limit. """
        if sys.getsizeof(texts) >= self.max_batch_size:
            if len(texts) == 1:
                raise ValueError("Given text is over {0} bytes, exceeds limit.".format(self.max_batch_size))
            raise ValueError("Given texts are over {0} bytes, exceed limit.".format(self.max_batch_size))
        return True
