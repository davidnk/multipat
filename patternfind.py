import bisect


def rad_sort_suffix_array(page, sa=None, i=0):
    if sa is None:
        sa = range(len(page))
    if len(sa) <= 1:
        return sa
    b = [[] for _ in range(255)]
    r = []
    for e in sa:
        if e + i >= len(page):
            r.append(e)
        else:
            b[ord(page[e+i])].append(e)
    for e in b:
        r += rad_sort_suffix_array(page, e, i+1)
    return r


def suffix_array(page):
    return sorted(range(len(page)+1), key=lambda x: page[x:])


def lcp_array(page, _suffix_array):
    def num_same(s1, s2):
        for i in range(min(len(s1), len(s2))):
            if s1[i] != s2[i]:
                return i
        return min(len(s1), len(s2))
    lcp = [0] * len(_suffix_array)
    for i in range(1, len(_suffix_array)):
        lcp[i] = num_same(page[_suffix_array[i-1]:], page[_suffix_array[i]:])
    return lcp


def pattern_to_remove(page, sa, lcp, occ=(0, float('inf')), leng=(0, float('inf'))):
    def get_max_rep_chars():
        m = (-1, -1, -1, -1, -1)
        fr = []
        for i in range(1, len(lcp) + 1):
            at = bisect.bisect_left(fr, (lcp[i], 0)) if i != len(lcp) else 0
            for v, vi in fr[at:]:
                if (occ[0] <= i - vi <= occ[1] and leng[0] <= v <= leng[1]):
                    m = max(m, (v * (i - vi), i - vi, v, vi, i))
            if i != len(lcp):
                fr[at:] = [(lcp[i], fr[at][1] if len(fr) > at else i - 1)]
        return (m[2], m[3])
    v, vi = get_max_rep_chars()
    pat = page[sa[vi]:sa[vi]+v] if v >= 0 else ''
    return pat


if __name__ == "__main__":
    if True:
        st = '\n'
        st += '<bb>a</bb><cat>\n'
        st += '<bb>j</bb><dog>\n'
        st += '<bb>bob</bb><man>\n'
        st += '<bb>to</bb><go>\n'
   # with open("/home/david/.cache/ff_searcher/1299603596466798048/1", "r") as f:
   #     st = f.read()[40330:55000].replace('<b>', '').replace('</b>', '')
    pats = []
    for i in range(15):
        sa = suffix_array(st)
        lcp = lcp_array(st, suffix_array(st))
        pat = pattern_to_remove(st, sa, lcp, (3, 6), (2, float('inf')))
        #pat = pattern_to_remove(st, sa, lcp, (12, float('inf')), (15, float('inf')))
        if '\n' in pat:
            pat = max(pat.split('\n'), key=lambda kk: len(kk))
        #print st#.replace('\n', '\\n').replace('\t', '\\t')
        if not pat.strip():
            break
        pats.append(pat)
        #print pat.replace('\n', '\\n').replace('\t', '\\t')
        st = st.replace(pat, '\t')
        #print
    for pat in pats:
        print pat.replace('\n', '\\n')
    print '--------------------------------------'
    print '\n'.join([e.strip() for e in st.split('\n')]).strip()
