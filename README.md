multipat
========

Remove or transform repeated substrings.


Notes
------
See tryit.py for some examples.
For large strings, I'd advise using pypy to run: it may run for 5 seconds instead of 5 minutes.
Note: suffix arrays and lcp arrays can be constructed in O(n) time.
      As this is only a prototype I implemented them trivially using an O(nlogn) algorithm.
      This may be improved later.
