import bisect


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


def suffix_array_and_lcp(s):
    sa = suffix_array(s)
    lcp = lcp_array(s, sa)
    return sa, lcp


def patterns(sa, lcp):
    """ Returns a list of repeated patterns of the form (leng, suf1, suf2) such that
    all suffixes associated with suffix_array[prev:cur] have a common prefix of length leng.
    No sub-patterns are included:
        _p = (_l, _s1, _s2) is a sub-pattern of p = (l, s1, s2) if
        p != _p and sa[s1] <= sa[_s1] and sa[_s2] <= sa[s2] and _l <= l and _s2 - _s1 <= s2 - s1
    """
    def add_pats(patmap, fr_after, cur):
        for leng, prev in fr_after:
            first_end_index = sa[prev] + leng
            if first_end_index not in patmap:
                patmap[first_end_index] = []
            patmap[first_end_index].append((leng, prev, cur))
    fr = []  # (min(lcp[index:i]), index)
    # first_end_pos -> pattern len, first sa index prefixed by pattern, last sa index _ 1
    patmap = {}
    for i in range(1, len(lcp)):
        at = bisect.bisect_left(fr, (lcp[i], 0))
        if at < len(fr):
            add_pats(patmap, fr[at + (fr[at][0] == lcp[i]):], i)
        fr[at:] = [(lcp[i], fr[at][1] if len(fr) > at else i - 1)]
    add_pats(patmap, fr, len(lcp))
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


def max_pattern(s, sa, lcp, evalfn=(lambda reps, leng: (reps-2)*(leng-2))):
    pat_val = lambda p: evalfn(p[2]-p[1], p[0])
    pat = max(patterns(sa, lcp), key=pat_val)
    leng, prev = pat[0], pat[1]
    pat = s[sa[prev]:sa[prev]+leng] if pat_val(pat) >= 0 else ''
    return pat


def pattern_shading(sa, lcp, shadefn, init_shade=0):
    """ shadefn = lambda prev_shade, reps, leng: new_shade """
    pats = patterns(sa, lcp)
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
