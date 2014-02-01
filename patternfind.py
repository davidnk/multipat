import bisect


def internal_cmp(page, x, y, step=100):
    """ Buffer so it works nicely. """
    lenx, leny = len(page) - x, len(page) - y
    i = 0
    for i in range(0, max(lenx, leny), step):
        if page[x+i:x+i+step] != page[y+i:y+i+step]:
            return -1 if page[x+i:x+i+step] < page[y+i:y+i+step] else 1
    return 0


def internal_num_same(page, x, y):
    lenx, leny = len(page) - x, len(page) - y
    for i in range(min(lenx, leny)):
        if page[x+i] != page[y+i]:
            return i
    return min(lenx, leny)


def suffix_array(page):
    return sorted(range(len(page)), cmp=lambda x, y: internal_cmp(page, x, y))


def lcp_array(page, _suffix_array):
    lcp = [0] * len(_suffix_array)
    for i in range(1, len(_suffix_array)):
        lcp[i] = internal_num_same(page, _suffix_array[i-1], _suffix_array[i])
    return lcp


def suffix_array_and_lcp(page):
    sa = suffix_array(page)
    lcp = lcp_array(page, sa)
    return sa, lcp


def get_repeated_pats(lcp):
    """ Returns a list of repeated patterns of the form (leng, suf1, suf2) such that
    all suffixes associated with suffix_array[prev:cur] have a common prefix of length leng.
    No sub-patterns are included:
        (_l, _s1, _s2) is a sub-pattern of (l, s1, s2) if
         ((_l, _s1, _s2) != (l, s1, s2)) and (_l<=l and s1<=_s1<=s2 and s1<=_s1<=s2))"""
    def add_pats(pats, fr_after, cur):
        for leng, prev in fr_after:
            pats.append((leng, prev, cur))
    fr = []  # (min(lcp[index:i]), index)
    pats = []
    for i in range(1, len(lcp)):
        at = bisect.bisect_left(fr, (lcp[i], 0))
        if at < len(fr):
            add_pats(pats, fr[at + (fr[at][0] == lcp[i]):], i)
        fr[at:] = [(lcp[i], fr[at][1] if len(fr) > at else i - 1)]
    add_pats(pats, fr, len(lcp))
    return pats


def pattern_to_remove(page, sa, lcp, evalfn=(lambda reps, leng: (reps-2)*(leng-2))):
    pat_val = lambda p: evalfn(p[2]-p[1], p[0])
    pat = max(get_repeated_pats(lcp), key=pat_val)
    leng, prev = pat[0], pat[1]
    pat = page[sa[prev]:sa[prev]+leng] if pat_val(pat) >= 0 else ''
    return pat


def pattern_shading(page, sa, lcp, evalfn, init_shade=0):
    """ evalfn = lambda prev_shade, reps, leng: new_shade """
    pats = get_repeated_pats(lcp)
    shades = [init_shade] * len(sa)
    for leng, s1, s2 in pats:
        for s in range(s1, s2):
            for i in range(sa[s], sa[s] + leng):
                shades[i] = evalfn(shades[i], s2-s1, leng)
    return shades
