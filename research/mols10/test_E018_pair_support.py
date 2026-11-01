"""Pure-stdlib independent replay of E018 Parker pair-support counts.
No SciPy/HiGHS dependency; can run in GitHub Actions standard Python.
"""
import itertools, json, unittest
from pathlib import Path

class PairSupportReplay(unittest.TestCase):
 def test_parker_pair_support(self):
  A=json.loads((Path(__file__).resolve().parent/'parker_pair.json').read_text())['squares'][0]
  n=len(A)
  self.assertEqual(n,10)
  self.assertTrue(all(set(row)==set(range(n)) for row in A))
  T=[]
  for p in itertools.permutations(range(n)):
   if len({A[r][p[r]] for r in range(n)})==n:
    T.append(sum(1<<(r*n+p[r]) for r in range(n)))
  self.assertEqual(len(T),1104)
  refs=[0]*(n*n)
  for i,u in enumerate(T):
   for cell in range(n*n):
    if u>>cell&1:refs[cell]|=1<<i
  compat=[]
  for u in T:
   compat.append(sum(1<<j for j,v in enumerate(T) if (u&v).bit_count()==1))
  self.assertTrue(all(all(compat[i]&ref for ref in refs) for i in range(len(T))))
  pairs=blocked=0
  for i,u in enumerate(T):
   for j in range(i+1,len(T)):
    if u&T[j]:continue
    pairs+=1
    common=compat[i]&compat[j]
    if any(not (common&ref) for ref in refs):blocked+=1
  self.assertEqual((pairs,blocked),(236104,226))

if __name__=='__main__':unittest.main()
