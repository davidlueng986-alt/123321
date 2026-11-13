"""Independent direct integer GF(3) cross-check of CAP057 ejection counts."""
from itertools import combinations
A=[s.strip() for s in open('/mnt/data/capset_v5/witness236.txt') if len(s.strip())==7]
V=[tuple(map(int,s)) for s in A]
pack=lambda t:sum(x*3**(6-j) for j,x in enumerate(t))
third=lambda a,b:tuple((-x-y)%3 for x,y in zip(a,b))
D=[tuple((i//(3**(6-j)))%3 for j in range(7)) for i in range(2187)]
S=set(V)
for qcode in (1,2,3,730,972):
 q=D[qcode]
 pairs=[(a,b) for a,b in combinations(V,2) if third(a,b)==q]
 assert len(pairs)==10
 for mask in (0,1,17,511,1023):
  removed={b if mask>>i&1 else a for i,(a,b) in enumerate(pairs)}
  fixed=(S-removed)|{q}
  assert len(fixed)==227
  forb={third(a,b) for a,b in combinations(fixed,2)}|fixed
  eligible=[p for p in D if p not in forb]
  assert not eligible,(qcode,mask,len(eligible),eligible[:3])
print('independent selected5*5 test PASS; independently recomputed all 227 choose2 pairs for each')
