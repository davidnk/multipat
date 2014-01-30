import bisect


def internal_cmp(page, x, y, step=100):
    """ Buffer so it works nicely. """
    lenx, leny = len(page) - x, len(page) - y
    i = 0
    for i in range(0, max(lenx, leny), step):
        if page[x+i:x+i+step] != page[y+i:y+i+step]:
            return cmp(page[x+i:x+i+step], page[y+i:y+i+step])
    return 0


def suffix_array(page):
    return sorted(range(len(page)+1), cmp=lambda x, y: internal_cmp(page, x, y))


def internal_num_same(page, x, y):
    lenx, leny = len(page) - x, len(page) - y
    for i in range(min(lenx, leny)):
        if page[x+i] != page[y+i]:
            return i
    return min(lenx, leny)


def lcp_array(page, _suffix_array):
    lcp = [0] * len(_suffix_array)
    for i in range(1, len(_suffix_array)):
        lcp[i] = internal_num_same(page, _suffix_array[i-1], _suffix_array[i])
    return lcp


def pattern_to_remove(page, sa, lcp, occ=(2, float('inf')), leng=(2, float('inf'))):
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


def largetest():
    print '-----------largetest------------------'
    #with open("/home/david/.cache/ff_searcher/1299603596466798048/1", "r") as f:
    #    st = f.read()[40330:75000].replace('<b>', '').replace('</b>', '')
    with open("search.html", "r") as f:
        st = f.read().replace('<b>', '').replace('</b>', '')
    pats = []
    for i in range(150):
        sa = suffix_array(st)
        lcp = lcp_array(st, suffix_array(st))
        #pat = pattern_to_remove(st, sa, lcp, (3, 6), (2, float('inf')))
        pat = pattern_to_remove(st, sa, lcp, (4, 20), (5, float('inf')))
        #pat = pattern_to_remove(st, sa, lcp, (12, float('inf')), (15, float('inf')))
        #print st#.replace('\n', '\\n').replace('\t', '\\t')
        #if '\n' in pat:
        #    pat = max(pat.split('\n'), key=lambda kk: len(kk))
        if not pat.strip():
            break
        pats.append(pat)
        #print pat.replace('\n', '\\n').replace('\t', '\\t')
        if '\n' in pat:
            st = st.replace(pat, '##\n')
        else:
            st = st.replace(pat, '##')
        #print
    for pat in pats:
        print pat.replace('\n', '\\n')
    print '--------------------------------------'
    print '\n'.join([e.strip() for e in st.split('\n')]).strip()


def codetest():
    return
    exit()

if __name__ == "__main__":
    codetest()
    largetest()
