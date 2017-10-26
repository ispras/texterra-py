# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import texterra
import types
import six
from os import getenv
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


# Texterra Tests

class CustomTexterraAPITest(unittest.TestCase):

    def setUp(self):
        TEXTERRA_CUSTOM_HOST = getenv("TEXTERRA_CUSTOM_HOST")
        TEXTERRA_CUSTOM_KEY = getenv("TEXTERRA_CUSTOM_KEY")
        self.custom_texterra = texterra.API(host=TEXTERRA_CUSTOM_HOST, key=TEXTERRA_CUSTOM_KEY)

    def test_custom_get_attributes(self):
        self.assertIsInstance(self.custom_texterra._get_attributes(12, 'enwiki'), dict)


class TexterraAPITest(unittest.TestCase):

    def setUp(self):
        TEXTERRA_KEY = getenv("TEXTERRA_KEY")
        self.texterra = texterra.API(key=TEXTERRA_KEY)

        self.en_text = 'Apple today updated iMac to bring numerous high-performance enhancements to the leading all-in-one desktop. iMac now features fourth-generation Intel Core processors, new graphics, and next-generation Wi-Fi. In addition, it now supports PCIe-based flash storage, making its Fusion Drive and all-flash storage options up to 50 percent faster than the previous generation'
        self.ru_text = 'Первые в этом году переговоры министра иностранных дел России Сергея Лаврова и госсекретаря США Джона Керри, длившиеся 1,5 часа, завершились в Мюнхене.'
        self.en_tweet = 'mentioning veterens care which Mccain has voted AGAINST - SUPER GOOOOD point Obama+1 #tweetdebate'
        self.ru_tweet = 'В мастерской готовят пушку и автомобили 1940-х годов, для участия в Параде Победы в Ново-Переделкино.'

    def test_bad_key(self):
        with self.assertRaises(ValueError):
            texterra.API('too short')

    def test_key_concepts(self):
        # test return type
        self.assertIsInstance(self.texterra.key_concepts([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.key_concepts([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.key_concepts([self.en_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.key_concepts([self.ru_tweet]), types.GeneratorType)

        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]
        concepts = []

        # test for a single text
        for text in texts:
            for entry in self.texterra.key_concepts(text):
                self.assertIsInstance(entry, list)
                entry_concepts = []
                for concept in entry:
                    self.assertIsInstance(concept, six.string_types)
                    entry_concepts.append(concept)
                concepts.append(entry_concepts)

        # test for text iterator
        result = self.texterra.key_concepts(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, list)
            for concept in entry:
                self.assertIsInstance(concept, six.string_types)

        # test memory limit on large text
        try:
            self.texterra.key_concepts(5000 * self.en_text)
        except Exception as e:
            self.assertIsInstance(e, ValueError)
            self.assertEqual(str(e), "Given text is over 1000000 bytes, exceeds limit.")

        self.assertEqual(concepts[0], ["http://en.m.wikipedia.org/wiki/Flash_memory"])
        self.assertEqual(concepts[1][0],
                         "http://ru.m.wikipedia.org/wiki/%D0%9C%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80_%D0%B8%D0%BD%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%BD%D1%8B%D1%85_%D0%B4%D0%B5%D0%BB")

    def test_disambiguation(self):
        # test return type
        self.assertIsInstance(self.texterra.disambiguation([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.disambiguation([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.disambiguation([self.ru_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.disambiguation([self.en_tweet]), types.GeneratorType)

        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]

        # test for a single text
        for text in texts:
            for entry in self.texterra.disambiguation(text):
                self.assertIsInstance(entry, list)

        # test text iterator
        result = self.texterra.disambiguation(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, list)
            for term in entry:
                self.assertIsInstance(term, tuple)
                self.assertEqual(len(term), 4)
                self.assertIsInstance(term[0], int)
                self.assertIsInstance(term[1], int)
                self.assertIsInstance(term[2], six.string_types)
                self.assertIsInstance(term[3], six.string_types)

        # test english
        en_test_text = "iMac now supports PCIe-based flash storage, making its Fusion Drive and all-flash storage options up to 50 percent faster than the previous generation."
        en_result = next(self.texterra.disambiguation([en_test_text]))
        en_result_expected = [(29, 42, "flash storage", "http://en.m.wikipedia.org/wiki/Flash_memory")]
        self.assertEqual(en_result, en_result_expected)

        # test russian
        ru_test_text = "Согласно официальному прогнозу Минэкономразвития, ВВП России упадет на 3%."
        ru_result = next(self.texterra.disambiguation([ru_test_text]))
        ru_result_expected = [
            (22, 30, "прогнозу", "http://ru.m.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D0%B3%D0%BD%D0%BE%D0%B7"),
            (31, 48, "Минэкономразвития",
             "http://ru.m.wikipedia.org/wiki/%D0%9C%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D0%B5%D1%80%D1%81%D1%82%D0%B2%D0%BE_%D1%8D%D0%BA%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D1%80%D0%B0%D0%B7%D0%B2%D0%B8%D1%82%D0%B8%D1%8F_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9_%D0%A4%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8"),
            (50, 60, "ВВП России",
             "http://ru.m.wikipedia.org/wiki/%D0%92%D0%92%D0%9F_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8")]
        self.assertEqual(len(ru_result), 3)
        for term in ru_result_expected:
            self.assertEqual(term in ru_result, True)

    def test_syntax_detection(self):
        # test return type
        self.assertIsInstance(self.texterra.syntax_detection([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.syntax_detection([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.syntax_detection([self.ru_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.syntax_detection([self.en_tweet]), types.GeneratorType)

        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]

        # test for a single text
        for text in texts:
            for entry in self.texterra.syntax_detection(text):
                self.assertIsInstance(entry, texterra.SyntaxTree)

        # test for text iterator
        result = self.texterra.syntax_detection(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, texterra.SyntaxTree)
            self.assertIsInstance(entry.to_string, six.string_types)
            self.assertEqual(len(entry.heads), len(entry.labels))
            self.assertEqual(0 in entry.heads, True)
            self.assertEqual('ROOT' in entry.labels, True)

        # test english
        en_test_sent = "Our kids should grow up in an America where opportunity is real."
        en_result = next(self.texterra.syntax_detection([en_test_sent]))
        self.assertIsInstance(en_result, texterra.SyntaxTree)
        self.assertEqual(en_result.get_labels(),
                         ["advmod", "nsubj", "dep", "ROOT", "advmod", "prep", "det", "pobj", "punct", "nsubj",
                          "cop", "rcmod", "dep"])
        self.assertEqual(en_result.to_string,
                         "(grow/ROOT Our/advmod kids/nsubj should/dep up/advmod (in/prep (America/pobj an/det (real/rcmod where/punct opportunity/nsubj is/cop ./dep)))) ")

        # test russian
        ru_test_sent = "Согласно официальному прогнозу Минэкономразвития, ВВП России упадет на 3%."
        ru_result = next(self.texterra.syntax_detection([ru_test_sent]))
        self.assertIsInstance(ru_result, texterra.SyntaxTree)
        self.assertEqual(ru_result.get_labels(),
                         ["обст", "опред", "предл", "квазиагент", "PUNCT", "предик", "квазиагент", "ROOT", "2-компл",
                          "предл", "PUNCT"])
        self.assertEqual(ru_result.to_string,
                         "(упадет/ROOT (Согласно/обст (прогнозу/предл официальному/опред (Минэкономразвития/квазиагент ,/PUNCT))) (ВВП/предик России/квазиагент) (на/2-компл (3%/предл ./PUNCT))) ")

    def test_language_detection(self):
        # test return type
        self.assertIsInstance(self.texterra.language_detection([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.language_detection([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.language_detection([self.en_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.language_detection([self.ru_tweet]), types.GeneratorType)

        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]

        # test for a single text
        for text in texts:
            for entry in self.texterra.language_detection(text):
                self.assertIsInstance(entry, six.string_types)

        # test for text iterator
        result = self.texterra.language_detection(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, six.string_types)

        # test english
        lang_list = list(self.texterra.language_detection(texts))
        self.assertEqual(lang_list[0], 'en')
        self.assertEqual(lang_list[2], 'en')

        # test russian
        self.assertEqual(lang_list[1], 'ru')
        self.assertEqual(lang_list[3], 'ru')

    def test_sentence_detection(self):
        # test return type
        self.assertIsInstance(self.texterra.sentence_detection([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.sentence_detection([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.sentence_detection([self.en_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.sentence_detection([self.ru_tweet]), types.GeneratorType)

        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]

        # test for a single text
        for text in texts:
            for entry in self.texterra.sentence_detection(text):
                self.assertIsInstance(entry, list)

        # test for text iterator
        result = self.texterra.sentence_detection(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, list)
            for sentence in entry:
                self.assertIsInstance(sentence, tuple)
                self.assertIsInstance(sentence[0], int)
                self.assertIsInstance(sentence[1], int)
                self.assertIsInstance(sentence[2], six.string_types)

        # test english
        en_test_text = "If you've never tried it, I think it's an interesting exercise to do without the Python semantics. It does make you appreciate what the language is providing."
        en_result = next(self.texterra.sentence_detection([en_test_text]))
        en_result_expected = [(0, 98,
                               "If you've never tried it, I think it's an interesting exercise to do without the Python semantics."),
                              (99, 158, "It does make you appreciate what the language is providing.")]
        self.assertEqual(en_result, en_result_expected)

        # test russian
        ru_test_text = "Выражение является полноправным оператором в Python. Состав, синтаксис, ассоциативность и приоритет операций достаточно привычны для языков программирования и призваны минимизировать употребление скобок."
        ru_result = next(self.texterra.sentence_detection([ru_test_text]))
        ru_result_expected = [(0, 52, "Выражение является полноправным оператором в Python."),
                              (53, 203,
                               "Состав, синтаксис, ассоциативность и приоритет операций достаточно привычны для языков программирования и призваны минимизировать употребление скобок.")]
        self.assertEqual(ru_result, ru_result_expected)

    def test_tokenization(self):
        # test return type
        self.assertIsInstance(self.texterra.tokenization([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.tokenization([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.tokenization([self.en_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.tokenization([self.ru_tweet]), types.GeneratorType)

        # test entry types
        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]
        for text in texts:
            for entry in self.texterra.tokenization([text]):
                self.assertIsInstance(entry, list)

        # test batch
        result = self.texterra.tokenization(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, list)

    def test_lemmatization(self):
        # test return type
        self.assertIsInstance(self.texterra.lemmatization([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.lemmatization([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.lemmatization([self.en_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.lemmatization([self.ru_tweet]), types.GeneratorType)

        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]

        # test for a single text
        for text in texts:
            for entry in self.texterra.lemmatization(text):
                self.assertIsInstance(entry, list)

        # test for text iterator
        result = self.texterra.lemmatization(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, list)
            for lemma in entry:
                self.assertIsInstance(lemma, tuple)
                self.assertIsInstance(lemma[0], int)
                self.assertIsInstance(lemma[1], int)
                self.assertIsInstance(lemma[2], six.string_types)
                self.assertIsInstance(lemma[3], six.string_types)

        en_test_sent = "Our kids should grow up in an America where opportunity is real."
        ru_test_sent = "Согласно официальному прогнозу Минэкономразвития, ВВП России упадет на 3%."
        result = self.texterra.lemmatization([en_test_sent, ru_test_sent])

        # test english
        en_result = next(result)
        en_result_expected = [(0, 3, "Our", "our"), (4, 8, "kids", "kid"), (9, 15, "should", "should"),
                              (16, 20, "grow", "grow"), (21, 23, "up", "up"), (24, 26, "in", "in"),
                              (27, 29, "an", "an"),
                              (30, 37, "America", "america"), (38, 43, "where", "where"),
                              (44, 55, "opportunity", "opportunity"),
                              (56, 58, "is", "be"), (59, 63, "real", "real"), (63, 64, ".", "")]
        self.assertEqual(en_result, en_result_expected)

        # test russian
        ru_result = next(result)
        ru_result_expected = [(0, 8, "Согласно", "согласно"), (9, 21, "официальному", "официальный"),
                              (22, 30, "прогнозу", "прогноз"), (31, 48, "Минэкономразвития", "минэкономразвития"),
                              (48, 49, ",", ""), (50, 53, "ВВП", "ввп"), (54, 60, "России", "россия"),
                              (61, 67, "упадет", "падать"), (68, 70, "на", "на"), (71, 73, "3%", "3"),
                              (73, 74, ".", "")]
        self.assertEqual(ru_result, ru_result_expected)

    def test_pos_tagging(self):
        # test return type
        self.assertIsInstance(self.texterra.pos_tagging([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.pos_tagging([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.pos_tagging([self.en_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.pos_tagging([self.ru_tweet]), types.GeneratorType)

        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]

        # test for a single text
        for text in texts:
            for entry in self.texterra.pos_tagging(text):
                self.assertIsInstance(entry, list)

        # test for text iterator
        result = self.texterra.pos_tagging(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, list)
            for pos_token in entry:
                self.assertIsInstance(pos_token, tuple)
                self.assertIsInstance(pos_token[0], int)
                self.assertIsInstance(pos_token[1], int)
                self.assertIsInstance(pos_token[2], six.string_types)
                self.assertIsInstance(pos_token[3], six.string_types)

        en_test_sent = "Our kids should grow up in an America where opportunity is real."
        ru_test_sent = "Согласно официальному прогнозу Минэкономразвития, ВВП России упадет на 3%."
        result = self.texterra.pos_tagging([en_test_sent, ru_test_sent])

        # test english
        en_result = next(result)
        en_result_expected = [(0, 3, "Our", "OTHER"), (4, 8, "kids", "NNS"), (9, 15, "should", "OTHER"),
                              (16, 20, "grow", "VB"), (21, 23, "up", "OTHER"), (24, 26, "in", "IN"),
                              (27, 29, "an", "DT"), (30, 37, "America", "NNP"), (38, 43, "where", "OTHER"),
                              (44, 55, "opportunity", "NN"), (56, 58, "is", "VBZ"), (59, 63, "real", "JJ"),
                              (63, 64, ".", "DOT")]
        self.assertEqual(en_result, en_result_expected)

        # test russian
        ru_result = next(result)
        ru_result_expected = [(0, 8, "Согласно", "PR"), (9, 21, "официальному", "A"), (22, 30, "прогнозу", "S"),
                              (31, 48, "Минэкономразвития", "S"), (48, 49, ",", "PUNCT"), (50, 53, "ВВП", "S"),
                              (54, 60, "России", "S"), (61, 67, "упадет", "V"), (68, 70, "на", "PR"),
                              (71, 73, "3%", "S"), (73, 74, ".", "PUNCT")]
        self.assertEqual(ru_result, ru_result_expected)

    def test_named_entities(self):
        # test return type
        self.assertIsInstance(self.texterra.named_entities([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.named_entities([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.named_entities([self.en_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.named_entities([self.ru_tweet]), types.GeneratorType)

        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]

        # test for a single text
        for text in texts:
            for entry in self.texterra.named_entities(text):
                self.assertIsInstance(entry, list)

        # test for text iterator
        result = self.texterra.named_entities(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, list)

        en_test_sent = "Our kids should grow up in an America where opportunity is real."
        ru_test_sent = "Согласно официальному прогнозу Минэкономразвития, ВВП России упадет на 3%."
        result = self.texterra.named_entities([en_test_sent, ru_test_sent])

        # test english
        en_result = next(result)
        en_result_expected = [(30, 37, "America", "LOCATION")]
        self.assertEqual(en_result, en_result_expected)

        # test russian
        ru_result = next(result)
        ru_result_expected = [(31, 48, "Минэкономразвития", "ORGANIZATION_POLITICAL"),
                              (54, 60, "России", "GPE_COUNTRY")]
        self.assertEqual(ru_result, ru_result_expected)

    def test_subjectivity_detection(self):
        # test return type
        self.assertIsInstance(self.texterra.subjectivity_detection([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.subjectivity_detection([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.subjectivity_detection([self.en_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.subjectivity_detection([self.ru_tweet]), types.GeneratorType)

        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]

        # test for a single text
        for text in texts:
            for entry in self.texterra.subjectivity_detection(text):
                self.assertIsInstance(entry, bool)

        # test for text iterator
        result = self.texterra.subjectivity_detection(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, bool)

        en_result = next(self.texterra.subjectivity_detection([self.en_tweet]))
        en_result_expected = True
        self.assertEqual(en_result, en_result_expected)

    def test_polarity_detection(self):
        # test return type
        self.assertIsInstance(self.texterra.polarity_detection([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.polarity_detection([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.polarity_detection([self.en_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.polarity_detection([self.ru_tweet]), types.GeneratorType)

        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]

        # test for a single text
        for text in texts:
            for entry in self.texterra.polarity_detection(text):
                self.assertIsInstance(entry, tuple)

        # test for text iterator
        result = self.texterra.polarity_detection(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, tuple)

        en_result = next(self.texterra.polarity_detection([self.en_tweet]))
        en_result_expected = "POSITIVE"
        self.assertEqual(en_result[0], en_result_expected)

    def test_spelling_correction(self):
        # test return type
        self.assertIsInstance(self.texterra.spelling_correction([self.en_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.spelling_correction([self.ru_text]), types.GeneratorType)
        self.assertIsInstance(self.texterra.spelling_correction([self.en_tweet]), types.GeneratorType)
        self.assertIsInstance(self.texterra.spelling_correction([self.ru_tweet]), types.GeneratorType)

        texts = [self.en_text, self.ru_text, self.en_tweet, self.ru_tweet]

        # test for a single text
        for text in texts:
            for entry in self.texterra.spelling_correction(text):
                self.assertIsInstance(entry, list)

        # test for text iterator
        result = self.texterra.spelling_correction(texts)
        self.assertIsInstance(result, types.GeneratorType)
        for entry in result:
            self.assertIsInstance(entry, list)
            for spelling_token in entry:
                self.assertIsInstance(spelling_token, tuple)
                self.assertIsInstance(spelling_token[0], int)
                self.assertIsInstance(spelling_token[1], int)
                self.assertIsInstance(spelling_token[2], six.string_types)
                self.assertIsInstance(spelling_token[3], six.string_types)

    def test_get_attributes(self):
        self.assertIsInstance(self.texterra._get_attributes(12, 'enwiki'), dict)
        self.assertIsInstance(self.texterra._get_attributes([12, 13137], 'enwiki'), dict)
        self.assertIsInstance(self.texterra._get_attributes(12, 'enwiki', ['url(en)', 'type']), dict)
        self.assertIsInstance(self.texterra._get_attributes([12, 13137], 'enwiki', ['url(en)', 'title']), dict)
