from nose.tools import assert_false
from dictfilter import DictFilter as Filter


def test_check():
    true_f, false_f = Filter(True), Filter(False)
    assert_false(true_f.check({}, False) or not false_f.check({}, False),
                        "FAILED dictfilter: check({}, False)")
    assert_false(not true_f.check({}, True) or false_f.check({}, True),
                        "FAILED dictfilter: check({}, True)")

def test_init_bool():
    true_f, false_f = Filter(True), Filter(False)
    assert_false(not true_f.check({}) or false_f.check({}),
                        "FAILED dictfilter: DictFilter(bool)")

def test_init_lambda():
    true_f, false_f = Filter(lambda x: True), Filter(lambda x: False)
    assert_false(not true_f.check({}) or false_f.check({}),
                        "FAILED dictfilter: DictFilter(lambda x: bool)")

def test_init_filter():
    true_f, false_f = Filter(True), Filter(False)
    assert_false((Filter(true_f).check({}) != true_f.check({}) or
                        Filter(false_f).check({}) != false_f.check({}) or
                        Filter(true_f) is true_f),
                        "FAILED dictfilter: DictFilter(DictFilter(bool))")

def test_return_():
    true_f, false_f = Filter(True), Filter(False)
    f = Filter()
    assert_false(not (f.or_filter(Filter()) is f and
                            f.and_filter(Filter()) is f and
                            f.not_filter() is f),
                        "FAILED dictfilter: or/and/not did not return ")

def test_or_filter():
    true_f, false_f = Filter(True), Filter(False)
    f_or = lambda f1, f2: Filter(f1).or_filter(Filter(f2))
    assert_false(not (f_or(true_f, false_f).check({}) and
                            f_or(true_f, true_f).check({}) and
                            f_or(false_f, true_f).check({}) and
                            not f_or(false_f, false_f).check({})),
                        "FAILED dictfilter: or_filter")

def test_and_filter():
    true_f, false_f = Filter(True), Filter(False)
    f_and = lambda f1, f2: Filter(f1).and_filter(Filter(f2))
    assert_false(not (not f_and(true_f, false_f).check({}) and
                            f_and(true_f, true_f).check({}) and
                            not f_and(false_f, true_f).check({}) and
                            not f_and(false_f, false_f).check({})),
                        "FAILED dictfilter: and_filter")

def test_not_filter():
    true_f, false_f = Filter(True), Filter(False)
    f_not = lambda f1: Filter(f1).not_filter()
    assert_false(not (not f_not(true_f).check({}) and f_not(false_f).check({})),
                        "FAILED dictfilter: not_filter")

def test_range_key_filter():
    true_f, false_f = Filter(True), Filter(False)
    range_f = Filter().range_key_filter('key', 0, 10)
    assert_false(not (not range_f.check({'key': -1}) and
                            not range_f.check({'key': 11}) and
                            range_f.check({'key': 0}) and
                            range_f.check({'key': 10}) and
                            range_f.check({'key': 5})),
                        "FAILED dictfilter: range_key_filter")

def test_text_key_filter():
    true_f, false_f = Filter(True), Filter(False)
    text_f = Filter().text_key_filter('key', ['a', 'b'], ['c', 'd'], ['e', 'f'])
    assert_false(not (text_f.check({'key': 'cd'}, False) and
                            text_f.check({'key': 'cda'}) and
                            text_f.check({'key': 'cdb'}) and
                            text_f.check({'key': 'cdab'}) and
                            text_f.check({'key': 'abc'}, False) and
                            text_f.check({'key': 'abd'}, False) and
                            text_f.check({'key': 'abcde'}, False) and
                            text_f.check({'key': 'abcdf'}, False) and
                            text_f.check({'key': 'abcdef'}, False) and
                            text_f.check({'key': 'xxaybzzcxdz'})),
                        "FAILED dictfilter: text_key_filter")


if __name__ == "__main__":
    for f in dir():
        if f.startswith('test_'):
            locals()[f]()
