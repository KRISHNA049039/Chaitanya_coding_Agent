"""Microbenchmarks for common string operations."""
import sys
import os
import timeit
from collections import deque

# Ensure repository root is on sys.path so imports work when running this script
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from string_utils import StringBuilder, use_stringio_write


def bench_join():
    return timeit.timeit("''.join(parts)", setup="parts=[str(i) for i in range(1000)]", number=2000)


def bench_plus_equal():
    return timeit.timeit(
        "s='';\nfor p in parts:\n    s+=p",
        setup="parts=[str(i) for i in range(1000)]",
        number=2000,
    )


def bench_stringbuilder():
    def run():
        sb = StringBuilder()
        for i in range(1000):
            sb.append(str(i))
        sb.build()
    return timeit.timeit("run()", globals={"run": run}, number=2000)


def bench_stringio():
    def run():
        use_stringio_write([str(i) for i in range(1000)])
    return timeit.timeit("run()", globals={"run": run}, number=2000)


def bench_pop0_vs_deque():
    def pop0():
        lst = [i for i in range(1000)]
        while lst:
            lst.pop(0)
    def deq():
        d = deque(range(1000))
        while d:
            d.popleft()
    t1 = timeit.timeit("pop0()", globals={"pop0": pop0}, number=2000)
    t2 = timeit.timeit("deq()", globals={"deq": deq}, number=2000)
    return t1, t2


def bench_translate_vs_regex():
    s = 'a'*10000 + 'b'*10000 + 'c'*10000
    mapping = {"a":"1","b":"2","c":"3"}
    def tr():
        s.translate(str.maketrans(mapping))
    import re
    pat = re.compile('a|b|c')
    def rg():
        pat.sub(lambda m: mapping[m.group(0)], s)
    t1 = timeit.timeit("tr()", globals={"tr": tr}, number=2000)
    t2 = timeit.timeit("rg()", globals={"rg": rg}, number=2000)
    return t1, t2


if __name__ == '__main__':
    print('join vs +=')
    print('join:', bench_join())
    print('plus-equal:', bench_plus_equal())
    print('StringBuilder:', bench_stringbuilder())
    print('StringIO:', bench_stringio())
    print('pop0 vs deque:', bench_pop0_vs_deque())
    print('translate vs regex:', bench_translate_vs_regex())
