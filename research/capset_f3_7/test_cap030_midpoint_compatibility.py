"""CAP-030: exact cross-fiber midpoint compatibility, stdlib-only."""
import itertools, json, pathlib, unittest
F=range(3)
def midpoint(a,b): return tuple((-x-y)%3 for x,y in zip(a,b))
def split(points): return [[p[1:] for p in points if p[0]==i] for i in F]
def forbidden(a,b): return {midpoint(x,y) for x in a for y in b}
def check(points):
    assert len(points)==len(set(map(tuple,points)))
    a=split(points)
    for i in F:
        for x,y in itertools.combinations(a[i],2):
            assert midpoint(x,y) not in a[i]
    for i in F:
        j,k=(i+1)%3,(i+2)%3
        assert not (forbidden(a[i],a[j]) & set(map(tuple,a[k])))
    return [len(forbidden(a[i],a[(i+1)%3])) for i in F]
class Tests(unittest.TestCase):
    def test_witnesses(self):
        cert=json.loads((pathlib.Path(__file__).parent/'CAP028_4d_quotient_line_certificate.json').read_text())
        self.assertEqual(check([tuple(x) for x in cert['witness_774']]),[23,19,19])
        self.assertEqual(check([tuple(x) for x in cert['witness_766']]),[20,19,20])
    def test_negative(self):
        cert=json.loads((pathlib.Path(__file__).parent/'CAP028_4d_quotient_line_certificate.json').read_text())
        pts=[tuple(x) for x in cert['witness_774']]
        a=split(pts)
        bad=next(iter(forbidden(a[0],a[1])))
        with self.assertRaises(AssertionError):check(pts+[(2,)+bad])
    def test_all_4d_lines(self):
        for i in F:
            for j in F:
                self.assertEqual(midpoint((i,j),(i,j)),(i,j))
if __name__=='__main__': unittest.main()
