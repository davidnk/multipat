def internal_cmp(s, x, y, step=100):
    """ Buffer so it works nicely. """
    lenx, leny = len(s) - x, len(s) - y
    i = 0
    for i in range(0, max(lenx, leny), step):
        if s[x+i:x+i+step] != s[y+i:y+i+step]:
            return -1 if s[x+i:x+i+step] < s[y+i:y+i+step] else 1
    return 0


def internal_num_same(s, x, y):
    lenx, leny = len(s) - x, len(s) - y
    for i in range(min(lenx, leny)):
        if s[x+i] != s[y+i]:
            return i
    return min(lenx, leny)


def suffix_array(s):
    return sorted(range(len(s)), cmp=lambda x, y: internal_cmp(s, x, y))


def lcp_array(s, _suffix_array):
    lcp = [0] * len(_suffix_array)
    for i in range(1, len(_suffix_array)):
        lcp[i] = internal_num_same(s, _suffix_array[i-1], _suffix_array[i])
    return lcp


def suffix_array_and_pats(s):
    sa = suffix_array(s)
    lcp = lcp_array(s, sa)
    pats = patterns(sa, lcp)
    return sa, pats


def patterns(sa, lcp):
    """ Returns a list of repeated patterns of the form (leng, suf1, suf2) such that
    all suffixes associated with suffix_array[prev:cur] have a common prefix of length leng.
    No sub-patterns are included:
        _p = (_l, _s1, _s2) is a sub-pattern of p = (l, s1, s2) if
        p != _p and sa[s1] <= sa[_s1] and sa[_s2] <= sa[s2] and _l <= l and _s2 - _s1 <= s2 - s1
    """
    def add_pat(patmap, (leng, prev), cur):
        first_end_index = sa[prev] + leng
        if first_end_index not in patmap:
            patmap[first_end_index] = []
        patmap[first_end_index].append((leng, prev, cur))
    fr = []  # (min(lcp[index:i]), index)
    # first_end_pos -> pattern len, first sa index prefixed by pattern, last sa index _ 1
    patmap = {}
    for i in range(1, len(lcp)):
        while fr and fr[-1][0] > lcp[i]:
            add_pat(patmap, fr.pop(), i)
        if not fr or fr[-1][0] < lcp[i]:
            fr.append((lcp[i], i - 1))
        else:
            fr[-1] = (lcp[i], fr[-1][1])
    while fr:
        add_pat(patmap, fr.pop(), len(lcp))
    pats = []
    for kpats in patmap.values():
        kpats.sort(key=lambda p: p[0], reverse=True)
        prev_reps = 0
        for (leng, s1, s2) in kpats:
            reps = s2 - s1
            if reps > prev_reps:
                pats.append((leng, s1, s2))
            prev_reps = reps
    return pats


def max_pattern(s, sa, pats, evalfn=(lambda reps, leng: (reps-2)*(leng-2))):
    pat_val = lambda p: evalfn(p[2]-p[1], p[0])
    pat = max(pats, key=pat_val)
    leng, prev = pat[0], pat[1]
    pat = s[sa[prev]:sa[prev]+leng] if pat_val(pat) >= 0 else ''
    return pat


def pattern_shading(sa, pats, shadefn, init_shade=0):
    """ shadefn = lambda prev_shade, reps, leng: new_shade """
    shades = [init_shade] * len(sa)
    for leng, s1, s2 in pats:
        for s in range(s1, s2):
            for i in range(sa[s], sa[s] + leng):
                shades[i] = shadefn(shades[i], s2-s1, leng)
    return shades


def map_with_shading(s, shading, symfn):
    """ returns a string formed by symfn(s, shading, char_index) at each index of s. """
    return ''.join([symfn(s, shading, i) for i in range(len(s))])


def split_to_repeated_sections(st, ):
    """ Return a set of ranges inside st, that all have similar structure. """
    pass


class Pats(object):
    def __init__(self, string):
        self.string = string
        self.suffix_array, self._patterns = suffix_array_and_pats(string)

    def patterns(self):
        return list(self._patterns)

    def shading(self, shadefn, init_shade=0):
        return pattern_shading(self.suffix_array, self._patterns, shadefn, init_shade)

    def maxpat(self, evalfn):
        return max_pattern(self.string, self.suffix_array, self._patterns, evalfn)

    def map_with_shading(self, shading, symfn):
        if hasattr(shading, '__call__'):
            shading = self.shading(shading)
        return ''.join([symfn(self.string, shading, i) for i in range(len(self.string))])
