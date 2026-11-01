"""Independent full 10! permutation replay of E019 triple blocking witnesses."""
import itertools, json, unittest
from pathlib import Path
from E019_depth_support import PARKER_A
class TestDepth3(unittest.TestCase):
 def test_independent_witnesses(self):
  n=10;A=PARKER_A
  # Independent brute-force permutation generator, no DFS enumerator.
  trans=[p for p in itertools.permutations(range(n)) if len({A[r][p[r]] for r in range(n)})==n]
  self.assertEqual(len(trans),1104)
  evidence=json.loads((Path(__file__).resolve().parent/'E019_RESULTS.json').read_text())
  self.assertEqual(evidence['input_sha256'],'1694eda37452b6709d8f8d77d8dfcddae08e18c6a94e4aabc102bec6323c1c77')
  for i,j,k,cell in evidence['blocked_triple_examples']+[evidence['root_new_witness']]:
   chosen=[trans[t] for t in (i,j,k)]
   sets=[{(r,p[r]) for r in range(n)} for p in chosen]
   self.assertTrue(all(not sets[x]&sets[y] for x in range(3) for y in range(x+1,3)))
   target=divmod(cell,n)
   self.assertFalse(any(target in {(r,p[r]) for r in range(n)} and all(sum(p[r]==t[r] for r in range(n))==1 for t in chosen) for p in trans), (i,j,k,cell))
 def test_rooted_slice_independent(self):
  A=PARKER_A;n=10
  trans=[p for p in itertools.permutations(range(n)) if len({A[r][p[r]] for r in range(n)})==n]
  masks=[sum(1<<(10*r+p[r]) for r in range(10)) for p in trans]
  cell_refs=[0]*100
  for t,mask in enumerate(masks):
   for cell in range(100):
    if mask>>cell&1:cell_refs[cell]|=1<<t
  compat=[]
  for a in masks:
   compat.append(sum(1<<j for j,b in enumerate(masks) if (a&b).bit_count()==1))
  def unsupported(x):return any(not (x&ref) for ref in cell_refs)
  total=blocked=new=0
  for j in range(1,len(masks)):
   if masks[0]&masks[j]:continue
   for k in range(j+1,len(masks)):
    if masks[0]&masks[k] or masks[j]&masks[k]:continue
    total+=1
    if unsupported(compat[0]&compat[j]&compat[k]):
     blocked+=1
     if all(not unsupported(compat[a]&compat[b]) for a,b in ((0,j),(0,k),(j,k))):new+=1
  self.assertEqual((total,blocked,new),(39528,29973,23296))
if __name__=='__main__':unittest.main()
