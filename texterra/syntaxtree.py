# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class SyntaxTree(object):
    """
    Implements a sentence's dependency parse tree.

    Attributes:
        tokens (list(str)): the list of the sentence's tokens, including the root element 'ROOT'

        spans (list(tuple(int, int))): the list of the sentence's tokens' (start index, end index) spans,
            with a 'None' value at the start for the root element.

        heads (list(int)): the list of indexes of each token's head element, where '1' corresponds to the first
            token in the sentence, and '0' corresponds to the root element. The list starts with a 'None' value
            for the root element (the root has no head element).

        labels (list(str)): the list of each token's dependency type from its head. The list starts with a
            'None' value for the root element (the root has no head element).

        tree (dict): a dictionary containing the sentence's parse tree. In the dictionary, a head element serves
            as a key and the value stores the list of its child elements.

        to_string (str): a string representation of the sentence's dependency parse.
    """

    def __init__(self, annotated_text):
        """
        Receives a Texterra-annotated text and initializes the syntax tree.
        """
        self.tokens = ['ROOT']  # initially has only root element
        self.spans = [None]
        self.heads = [None]  # root has no head element
        self.labels = [None]  # root has no head element => no label

        span_to_index = {}
        i = 1
        for an in annotated_text['annotations']['syntax-relation']:
            span = (an['start'], an['end'])
            self.spans.append(span)
            span_to_index[span] = i
            self.tokens.append(annotated_text['text'][an['start']: an['end']])
            i += 1

        for an in annotated_text['annotations']['syntax-relation']:
            if 'parent' in an['value']:
                self.heads.append(span_to_index[(an['value']['parent']['start'], an['value']['parent']['end'])])
                self.labels.append(an['value']['type'])
            else:
                self.heads.append(0)
                self.labels.append('ROOT')

        root_index = self.heads.index(0)
        root_span = self.spans[root_index]
        self.visited = [root_index]
        self.tree = {}
        self.tree[(root_span[0], root_span[1], self.tokens[root_index], 'ROOT')], s = self._build_tree(root_index)
        self.to_string = s

    def get_labels(self):
        """ Returns the list of each token's dependency type from its head. """
        return self.labels[1:]

    def get_heads(self):
        """
        Returns the list of indexes of each token's head element.
        In the returned list, '1' corresponds to the first token in the sentence, and
        '0' corresponds to the root element.
        """
        return self.heads[1:]

    def _build_tree(self, index):
        """
        Traverses parse tree's elements and recursively adds children of element at given index to the tree.

        :param index: head element's index
        """

        children = []
        to_string = '({0}/{1}'.format(self.tokens[index], self.labels[index])

        for i in range(1, len(self.tokens)):

            if i not in self.visited and self.heads[i] == index:
                self.visited.append(i)
                child_tree = {}
                c, s = self._build_tree(i)
                child_tree[(self.spans[i][0], self.spans[i][1], self.tokens[i], self.labels[i])] = c
                children.append(child_tree)
                to_string += ' {0}'.format(s)

        if len(children) > 0:
            to_string += ')'
            return children, to_string
        else:
            return children, to_string[1:]

    def __str__(self):
        return self.to_string
