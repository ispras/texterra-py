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

        tree (dict): a dictionary containing the sentence's parse tree, with root elements as key and their child
            elements as value. Child elements that have their own children are also stored as dictionaries, where
            they serve as key and their children as value.

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

        span_to_index = {}  # maps token spans to indexes
        root_indexes = []  # to store indexes of root elements

        # get token spans and values from the Texterra-annotated document
        for i, an in enumerate(annotated_text['annotations']['syntax-relation']):
            span = (an['start'], an['end'])
            self.spans.append(span)
            span_to_index[span] = i + 1
            self.tokens.append(annotated_text['text'][an['start']: an['end']])

        # iterate over the document again to set heads and labels
        for i, an in enumerate(annotated_text['annotations']['syntax-relation']):
            if 'parent' in an['value']:
                self.heads.append(span_to_index[(an['value']['parent']['start'], an['value']['parent']['end'])])
                self.labels.append(an['value']['type'])
            else:
                self.heads.append(0)
                self.labels.append('ROOT')
                root_indexes.append(i + 1)

        # stores dependency structure of the sentence in dict, with
        # root elements as key and their child elements as value.
        # child elements that have their own children are stored as dicts
        # where they serve as key and their children as value.
        self.tree = {}
        self._visited = []  # stores elements visited during tree's building process
        self.to_string = ''

        # iterate over root elements and build their subtrees
        for root_index in root_indexes:
            # get the root's span
            root_span = self.spans[root_index]

            # indicate the root as visited
            self._visited.append(root_index)

            # build the roots subtree
            sub_tree, sub_tree_string = self._build_tree(root_index)
            sub_tree_key = (root_span[0], root_span[1], self.tokens[root_index], 'ROOT')
            self.tree[sub_tree_key] = sub_tree

            # attach the subtrees string to the sentence's parse string
            if len(root_indexes) > 0 and not sub_tree_string.startswith('('):
                format_string = '({0}) '
            else:
                format_string = '{0} '
            self.to_string += format_string.format(sub_tree_string)

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

            if i not in self._visited and self.heads[i] == index:
                self._visited.append(i)
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
