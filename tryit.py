from __future__ import print_function, division
from multipat import suffix_array_and_pats, pattern_shading, map_with_shading
import random
import requests


def change_by_shade(st, shadefn, symfn):
    """ returns a string formed by symfn(st, shades, char_index) at each index of st. """
    sa, pats = suffix_array_and_pats(st)
    shading = pattern_shading(sa, pats, shadefn)
    return map_with_shading(st, shading, symfn)


def gentest():
    n = 100
    st = ''.join([chr(random.randint(ord('A'), ord('Z'))) for i in range(20)])
    st *= n
    data = 'attic dog is not orange good cat or is it apple and jumping pie cab cat'.split()
    insertat = sorted(random.sample(xrange(len(st)), len(data)), reverse=True)
    for (d, i) in zip(data, insertat):
        st = st[:i] + d + st[i:]
    symfn = lambda s, sh, i: s[i] if sh[i] == 0 else ''
    shadefn = lambda sh, reps, leng: max(sh, int(reps >= n))
    ret = change_by_shade(st, shadefn, symfn)
    print(len([i for i in ret if i.islower()])/len([i for i in ret if i.isalpha()]))


def parse_small():
    st = '\n'
    st += '<bb>a</bb><cat>\n'
    st += '<bb>j</bb><dog>\n'
    st += '<bb>bob</bb><man>\n'
    st += '<bb>to</bb><go>\n'
    symfn = lambda s, sh, i: s[i] if s[i] == '\n' or sh[i] <= 0 else ' '
    shadefn = lambda sh, reps, leng: max(sh, int(leng >= 2 and reps >= 3))
    st = change_by_shade(st, shadefn, symfn)
    pl = [p.split() for p in st.strip().split('\n')]
    print('\n'.join([str(p) for p in pl]))


def view_detected_redundency(filename, nreps):
    def symfn(stri, shades, i):
        if stri[i] == '\n':
            return '\n'
        if shades[i] <= 0:
            return stri[i]
        else:
            if stri[i].isdigit():
                return '_' + stri[i]
            if stri[i].isalpha():
                return stri[i].upper()
            return '#'
    shadefn = lambda sh, reps, leng: max(sh, int(leng > 10 and reps >= nreps))
    st = requests.get('http://www.w3schools.com/xml/{}'.format(filename)).content
    st = st.lower()
    st = change_by_shade(st, shadefn, symfn)
    print(st)


def parse_xkcd_multipage():
    pages = []
    for p in range(1300, 1326):
        with open('files/xkcd{}.html'.format(p), 'r') as f:
            pages.append("#" + str(p % 10) + ("*"*5 + str(p)) + "#" + f.read())
    nreps = len(pages)
    st = ''.join(pages)
    st = st.replace("&#39;", "'")
    symfn = lambda s, sh, i: s[i] if s[i] == '\n' or sh[i] <= 0 else '#' if sh[i-1] <= 0 else ''
    symfn = lambda s, sh, i: s[i] if sh[i] <= 0 else '#' if sh[i-1] <= 0 else ''
    shadefn = lambda sh, reps, leng: sh + (leng > 15 and nreps * 2 >= reps >= nreps * .9)
    st = change_by_shade(st, shadefn, symfn)
    st = st.replace('#', '\n')
    print(st)


def parse_umd_search():
    nreps = 8
    st = requests.get("http://www.searchum.umd.edu/search?site=UMCP&client=UMCP&" +
                      "proxystylesheet=UMCP&output=xml_no_dtd&q=research").content
    st = st.replace('<b>', '').replace('</b>', '').replace('<br>', '').replace('\n', '')
    symfn = lambda s, sh, i: s[i] if sh[i] <= 0 else '#' if sh[i-1] <= 0 else ''
    shadefn = lambda sh, reps, leng: sh + (leng * reps**2 > 1500 and leng > 15 and reps > nreps)
    st = change_by_shade(st, shadefn, symfn)
    st = st.replace('#', '\n')
    lines = st.strip().split('\n')
    nline = 1
    for i in xrange(len(lines)):
        if lines[i] == str(nline):
            nline += 1
            print(lines[i] + '\n' + '\n'.join(lines[i+2:i+5]) + '\n')


def parse_xml(filename, nreps):
    st = requests.get('http://www.w3schools.com/xml/{}'.format(filename)).content
    symfn = lambda s, sh, i: s[i] if s[i] == '\n' or sh[i] <= 0 or s[i].isdigit() else ''
    shadefn = lambda sh, reps, leng: max(sh, int(leng > 10 and reps > nreps))
    st = change_by_shade(st, shadefn, symfn)
    pl = [p.strip().split('\n') for p in st.split('\n\n')]
    print('\n'.join([str(p) for p in pl]))


if __name__ == "__main__":
    parse_small()
    exit()
    parse_xkcd_multipage()
    gentest()
    view_detected_redundency('plant_catalog.xml', 36)
    parse_xml('simple.xml', 4)
    parse_xml('cd_catalog.xml', 20)
    parse_xml('plant_catalog.xml', 30)
    parse_umd_search()
