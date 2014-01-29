#! /usr/bin/python
class DictFilter(object):
    """
    DictFilter creates a filter to check that a dict has the properties you specify.
    """

    def __init__(self, _fil=True):
        if isinstance(_fil, DictFilter):
            self.__filter = _fil.check
        elif isinstance(_fil, bool):
            self.__filter = lambda x: _fil
        elif hasattr(_fil, '__call__'):
            self.__filter = _fil

    def check(self, x, result=True):
        return self.__filter(x) == result

    def and_filter(self, _fil):
        if isinstance(_fil, DictFilter):
            _fil = _fil.check
        _filter = self.__filter
        self.__filter = lambda x: _filter(x) and _fil(x)
        return self

    def or_filter(self, _fil):
        if isinstance(_fil, DictFilter):
            _fil = _fil.check
        _filter = self.__filter
        self.__filter = lambda x: _filter(x) or _fil(x)
        return self

    def not_filter(self):
        _filter = self.__filter
        self.__filter = lambda x: not _filter(x)
        return self

    def text_key_filter(self, key, someof=[], allof=[], noneof=[]):
        """Ignores case only when no caps"""
        if isinstance(someof, basestring):
            someof = [someof]
        if isinstance(allof, basestring):
            allof = [allof]
        if isinstance(noneof, basestring):
            noneof = [noneof]

        def _fil(x):
            x = x[key]
            ret = len(someof) == 0
            for i in someof:
                ret = ret or ((i == i.lower() and i.lower() in x.lower()) or (i in x))
            for i in allof:
                ret = ret and ((i == i.lower() and i.lower() in x.lower()) or (i in x))
            for i in noneof:
                ret = ret and not ((i == i.lower() and i.lower() in x.lower()) or (i in x))
            return ret
        return DictFilter(_fil)

    def range_key_filter(self, key, smallest=float('-inf'), largest=float('inf')):
        return DictFilter(lambda x: (smallest <= x[key] <= largest))
