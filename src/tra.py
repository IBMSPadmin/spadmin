# Precomputed values (for str_join_set and translate)

letter_set = frozenset(string.ascii_lowercase + string.ascii_uppercase)
tab = string.maketrans(string.ascii_lowercase + string.ascii_uppercase,
                       string.ascii_lowercase * 2)
deletions = ''.join(ch for ch in map(chr,range(256)) if ch not in letter_set)

s="A235th@#$&( er Ra{}|?>ndom"

# From unwind's filter approach
def test_filter(s):
    return filter(lambda x: x in string.ascii_lowercase, s.lower())

# using set instead (and contains)
def test_filter_set(s):
    return filter(letter_set.__contains__, s).lower()

# Tomalak's solution
def test_regex(s):
    return re.sub('[^a-z]', '', s.lower())

# Dana's
def test_str_join(s):
    return ''.join(c for c in s.lower() if c in string.ascii_lowercase)

# Modified to use a set.
def test_str_join_set(s):
    return ''.join(c for c in s.lower() if c in letter_set)

# Translate approach.
def test_translate(s):
    return string.translate(s, tab, deletions)


for test in sorted(globals()):
    if test.startswith("test_"):
        assert globals()[test](s)=='atherrandom'
        print "%30s : %s" % (test, timeit.Timer("f(s)", 
              "from __main__ import %s as f, s" % test).timeit(200000))
