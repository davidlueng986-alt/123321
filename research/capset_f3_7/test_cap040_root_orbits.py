"""CAP040 proof-tree exact coverage and adversarial positive controls."""
import unittest, tempfile, hashlib
from itertools import combinations,permutations
from pathlib import Path
from cap040_root_orbits import (root_orbits,audit_n7,frame,third,vec,type_key,
                               pack,barycentric,write_cnf)

def rank(M):
    a=[list(r) for r in M]
    t=0
    for j in range(len(a[0]) if a else 0):
        piv=next((i for i in range(t,len(a)) if a[i][j]),None)
        if piv is None:continue
        a[t],a[piv]=a[piv],a[t]
        inv=1 if a[t][j]==1 else 2
        a[t]=[inv*x%3 for x in a[t]]
        for i in range(len(a)):
            if i==t:continue
            f=a[i][j]
            a[i]=[(x-f*y)%3 for x,y in zip(a[i],a[t])]
        t+=1
        if t==len(a):break
    return t

def inverse(A):
    n=len(A)
    a=[list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
    for k in range(n):
        p=next(i for i in range(k,n) if a[i][k])
        a[k],a[p]=a[p],a[k]
        inv=1 if a[k][k]==1 else 2
        a[k]=[(inv*x)%3 for x in a[k]]
        for i in range(n):
            if i==k:continue
            f=a[i][k]
            a[i]=[(x-f*y)%3 for x,y in zip(a[i],a[k])]
    return [z[n:] for z in a]

def normalize_cap(cap):
    n=len(cap[0]);p0=cap[0];basis=[p0]
    for p in cap[1:]:
        if p==p0:continue
        diffs=[tuple((v[k]-p0[k])%3 for k in range(n)) for v in basis[1:]]
        trial=tuple((p[k]-p0[k])%3 for k in range(n))
        if rank(diffs+[trial])>len(diffs):basis.append(p)
        if len(basis)==n+1:break
    assert len(basis)==n+1
    A=[[(basis[j+1][i]-p0[i])%3 for j in range(n)] for i in range(n)]
    inv=inverse(A)
    out=[]
    for p in cap:
        d=[(p[i]-p0[i])%3 for i in range(n)]
        out.append(tuple(sum(inv[i][j]*d[j] for j in range(n))%3 for i in range(n)))
    assert out[:n+1]==frame(n)
    return out

class CAP040Tests(unittest.TestCase):
    def test_root_exact_partition(self):
        r=audit_n7()
        self.assertEqual(r['ninth_orbit_classes'],13)
        self.assertEqual(sum(b['ninth_orbit_size'] for b in r['branches']),2151)
        self.assertEqual(r['tenth_orbit_classes_total'],1211)
        self.assertEqual(sum(b['forced_zeros']==35 for b in r['branches']),1)

    def test_n2_exhaustive_cap_positive_control(self):
        V=[vec(i,2) for i in range(9)]
        branches=root_orbits(2)
        allowed={i for b in branches for i in range(9) if type_key(V[i])==b['type']}
        self.assertEqual(len(branches),1)
        caps=0
        for C in combinations(V,4):
            S=set(C)
            if any(third(a,b) in S for a,b in combinations(C,2)):continue
            caps+=1
            normalized=normalize_cap(list(C))
            self.assertIn(pack(normalized[3]),allowed)
        self.assertGreater(caps,0)

    def test_actual_236_witness_affine_normalization(self):
        p=Path(__file__).resolve().parent/'candidates'/'calderbank_fishburn_236.txt'
        cap=[tuple(map(int,line.strip())) for line in p.read_text().splitlines()
             if len(line.strip())==7 and set(line.strip())<=set('012')]
        self.assertEqual(len(cap),236)
        S=set(cap);self.assertEqual(len(S),236)
        for a,b in combinations(cap,2):self.assertNotIn(third(a,b),S)
        norm=normalize_cap(cap)
        N=set(norm);self.assertEqual(len(N),236)
        for a,b in combinations(norm,2):self.assertNotIn(third(a,b),N)
        cases={tuple(z['type']) for z in root_orbits(7)}
        self.assertTrue(all(type_key(p) in cases for p in norm[8:]))

    def test_barycentric_group_action_full_s8(self):
        for case in root_orbits(7):
            p=tuple(map(int,case['ninth']))
            lam=barycentric(p)
            images={tuple(lam[i] for i in perm)[1:] for perm in permutations(range(8))}
            self.assertEqual(len(images),case['ninth_orbit_size'])
            self.assertTrue(all(type_key(v)==case['type'] for v in images))

    def test_branch0_full_dimacs_header_and_hash(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'branch0.cnf'
            info=write_cnf(audit_n7()['branches'][0],str(p))
            self.assertEqual((info['variables'],info['clauses'],info['new_unit_clauses']),
                             (492540,1775362,9))
            with p.open('rb') as f:
                self.assertIn(b'p cnf 492540 1775362',f.readline()+f.readline())
            # SHA for the ENTIRE DIMACS, independently generated locally.
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),
                             '8d23ac06842a0fbdafab8aef244e54dd819770578c2c8023b04e565a330e19e9')

if __name__=='__main__':unittest.main()
