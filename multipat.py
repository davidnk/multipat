def internal_cmp(s, x, y, step=100):
    """ Buffer so it works nicely. """
    lenx, leny = len(s) - x, len(s) - y
    i = 0
    for i in xrange(0, max(lenx, leny), step):
        if s[x+i:x+i+step] != s[y+i:y+i+step]:
            return -1 if s[x+i:x+i+step] < s[y+i:y+i+step] else 1
    return 0


def suffix_array(s):
    """ constant memory and nlogn most of the time. """
    return sorted(range(len(s)), cmp=lambda x, y: internal_cmp(s, x, y))


def suffix_array1(s):
    def counting_sort(arr, n=None, key=None):
        key = key or (lambda e: e)
        n = n or (max(arr, key=key) + 1)
        slots = [[] for i in xrange(n)]
        for e in arr:
            slots[key(e)].append(e)
        return sum((sorted(slots[i]) for i in xrange(n) if slots[i]), [])
    l = 1
    sa_l = counting_sort(range(len(s)), 256, lambda i: ord(s[i]))
    #sa_l.sort(key=lambda i:s[i:i+l])
    inv_l = range(len(s))
    prev, v = s[sa_l[0]], 0
    for i in sa_l:
        if s[i] != prev:
            v += 1
            prev = s[i]
        inv_l[i] = v
    while l < 2 * len(s):
        for i in xrange(len(s)):
            sa_l[i] = (inv_l[i], (i + l < len(inv_l)) and inv_l[i+l], i)
        #sa_l.sort()
        sa_l = counting_sort(sa_l, key=lambda e: e[0])
        l *= 2
        prev, v = sa_l[0][:2], 0
        for i in sa_l:
            if i[:2] != prev:
                v += 1
                prev = i[:2]
            inv_l[i[2]] = v
    sa = [0] * len(inv_l)
    for i in xrange(len(inv_l)):
        sa[inv_l[i]] = i
    return sa


def lcp_array(s, sa):
    lcp = [0] * len(sa)
    sa_inv = [0] * len(sa)
    for i in xrange(len(sa)):
        sa_inv[sa[i]] = i
    l = 0
    for s_i in xrange(len(sa)):
        sa_i = sa_inv[s_i]
        s_i2 = sa[sa_i-1] if sa_i != 0 else len(sa)
        while l + max(s_i, s_i2) < len(s) and s[s_i+l] == s[s_i2+l]:
            l += 1
        lcp[sa_i] = l
        l = max(0, l - 1)
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
    # first_end_pos -> [(pattern len, first sa index prefixed by pattern, last sa index _ 1), ...]
    patmap = {}
    for i in xrange(1, len(lcp)):
        fr_prev = (lcp[i], i - 1)
        while fr and fr[-1][0] > lcp[i]:
            fr_prev = fr.pop()
            add_pat(patmap, fr_prev, i)
        if lcp[i] and (not fr or fr[-1][0] < lcp[i]):
            fr.append((lcp[i], fr_prev[1]))
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
        for s in xrange(s1, s2):
            for i in xrange(sa[s], sa[s] + leng):
                shades[i] = shadefn(shades[i], s2-s1, leng)
    return shades


def map_with_shading(s, shading, symfn):
    """ if shading is given as a shading array, it is used as shading_array
        if shading is given as a shading function (lambda prev_shade, reps, leng: new_shade):
            shading_array is computed first as done in pattern_shading
        returns a string formed by symfn(s, shading_array, char_index) at each index of s."""
    if hasattr(shading, '__call__'):
        sa, pats = suffix_array_and_pats(st)
        shading = pattern_shading(sa, pats, shading)
    return ''.join([symfn(s, shading, i) for i in xrange(len(s))])


def split_to_repeated_sections(st, ):
    """ Return a set of ranges inside st, that all have similar structure. """
    pass


class Pats(object):
    def __init__(self, string):
        self.string = string
        self._suffix_array, self._patterns = suffix_array_and_pats(string)

    def suffix_array(self):
        return list(self._suffix_array)

    def patterns(self):
        return list(self._patterns)

    def shading(self, shadefn, init_shade=0):
        return pattern_shading(self._suffix_array, self._patterns, shadefn, init_shade)

    def maxpat(self, evalfn):
        return max_pattern(self.string, self._suffix_array, self._patterns, evalfn)

    def map_with_shading(self, shading, symfn):
        if hasattr(shading, '__call__'):
            shading = self.shading(shading)
        return ''.join([symfn(self.string, shading, i) for i in xrange(len(self.string))])
