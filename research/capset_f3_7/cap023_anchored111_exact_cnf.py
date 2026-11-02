#!/usr/bin/env python3
"""CAP-023: exact anchored-111 n=7 cap CNF + 3x3-grid negative controls.

No solver is invoked. CNF satisfiability/unsatisfiability is UNKNOWN.
Universal scope of the anchored-111 reduction is CONDITIONAL on a theorem
that every 111-cap in F_3^6 extends to a unique 112-cap (Potechin +
Thackeray's 110-completion + independent secant argument).
All arithmetic here is exact integers over F_3; no GPU/randomness.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import unittest

B0 = ((0,1,2),(0,1,3),(0,2,4),(0,3,5),(0,4,5),
      (1,2,5),(1,3,4),(1,4,5),(2,3,4),(2,3,5))
B1 = ((0,1,4),(0,1,5),(0,2,3),(0,2,5),(0,3,4),
      (1,2,3),(1,2,4),(1,3,5),(2,4,5),(3,4,5))
GRID_COUNTERMODELS = (
    ((39,36,36),(34,34,20),(20,39,29)),
    ((40,36,35),(34,33,21),(20,40,28)),
    ((45,44,22),(38,30,20),(26,35,27)),
    ((45,45,21),(36,32,20),(28,32,28)),
)
F111 = Counter({(39,36,36):110,(40,36,35):198,
                (45,44,22):45,(45,45,21):11})


def pack(v):
    out=0
    for d in v:
        assert d in (0,1,2)
        out=3*out+d
    return out


def digits(k,n=6):
    out=[0]*n
    for i in range(n-1,-1,-1):
        out[i]=k%3
        k//=3
    assert k==0
    return tuple(out)


def third(x,y):
    return tuple((-a-b)%3 for a,b in zip(x,y))


def make112(blocks):
    shell={v for v in product((1,2),repeat=6) if v.count(2)%2==0}
    pts=set(shell)
    for b in blocks:
        for signs in product((1,2),repeat=3):
            x=[0]*6
            for i,s in zip(b,signs): x[i]=s
            pts.add(tuple(x))
    assert len(pts)==112 and len(shell)==32
    return frozenset(pts)


def known236():
    h0,h1=make112(B0),make112(B1)
    e=set()
    for i in range(6):
        for v in (1,2):
            x=[0]*6;x[i]=v;e.add(tuple(x))
    cap={(0,)+x for x in h0}|{(1,)+x for x in h1}|{(2,)+x for x in e}
    assert len(cap)==236 and len(e)==12
    return frozenset(cap)


def verify_cap(points,n):
    pts=set(points)
    assert len(pts)==len(points) and all(len(p)==n for p in pts)
    assert all(all(x in (0,1,2) for x in p) for p in pts)
    for x,y in combinations(sorted(pts),2):
        if third(x,y) in pts:return False
    return True


def anchored111():
    h=make112(B0)
    missing=min(h)
    return h-frozenset((missing,)),missing


def lines6():
    vectors=[digits(i) for i in range(729)]
    for i in range(729):
        for j in range(i+1,729):
            k=pack(third(vectors[i],vectors[j]))
            if j<k: yield i,j,k


def forbidden_edges(anchor):
    """Pairs of external point IDs (1..729 and 730..1458)."""
    for p in sorted(anchor):
        for i in range(729):
            yield i+1,pack(third(p,digits(i)))+730


def aux_id(i,j,N,k):
    assert 1<=j<=min(i,k)
    t=i-1
    before=t*(t+1)//2 if t<=k else k*(k+1)//2+(t-k)*k
    return N+before+j


def stats(target=287):
    k=target-111
    assert 1<=k<=1458
    N=1458
    aux=sum(min(i,k) for i in range(1,N+1))
    nlines=2*(729*728//6)
    edges=111*729
    counter_clauses=2*aux-N+1
    return dict(anchor=111,target=target,external_target=k,external_variables=N,
                fixed_anchor_absent=618,within_layer_line_clauses=nlines,
                cross_layer_binary_clauses=edges,auxiliary_variables=aux,
                counter_clauses=counter_clauses,total_variables=N+aux,
                total_clauses=nlines+edges+counter_clauses,
                sat_status='UNKNOWN',scope='anchored 111 section only')


def clauses(target=287):
    anchor,_=anchored111()
    k=target-111;N=1458
    assert 1<=k<=N
    for i,j,l in lines6():
        yield (-i-1,-j-1,-l-1)
        yield (-i-730,-j-730,-l-730)
    for a,b in forbidden_edges(anchor):yield (-a,-b)
    for i in range(1,N+1):
        for j in range(1,min(i,k)+1):
            s=aux_id(i,j,N,k)
            prev=aux_id(i-1,j,N,k) if j<=min(i-1,k) else None
            prev_low=aux_id(i-1,j-1,N,k) if j>1 else 0
            yield (-s,prev,i) if prev is not None else (-s,i)
            if j>1:
                yield (-s,prev,prev_low) if prev is not None else (-s,prev_low)
    yield (aux_id(N,k,N,k),)


def write_cnf(path,target=287):
    s=stats(target);path=Path(path)
    with path.open('w',encoding='ascii',newline='\n') as f:
        f.write('c CAP-023 anchored-111 exact CNF; SAT status UNKNOWN\n')
        f.write(f'p cnf {s["total_variables"]} {s["total_clauses"]}\n')
        count=0
        for clause in clauses(target):
            f.write(' '.join(map(str,clause))+' 0\n')
            count+=1
    assert count==s['total_clauses'],(count,s)
    s['cnf_bytes']=path.stat().st_size
    s['cnf_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    return s


def check_witness(points,target=235):
    """Evaluate EVERY emitted clause under an exact, explicit counter assignment."""
    anchor,_=anchored111()
    assert {p[1:] for p in points if p[0]==0}==anchor
    S={pack(p[1:])+1 if p[0]==1 else pack(p[1:])+730
       for p in points if p[0] in (1,2)}
    N=1458;k=target-111
    truth=bytearray(N+sum(min(i,k) for i in range(1,N+1))+1)
    for i in S:truth[i]=1
    count=0
    for i in range(1,N+1):
        count+=truth[i]
        for j in range(1,min(i,k)+1):
            truth[aux_id(i,j,N,k)]=int(count>=j)
    for cl in clauses(target):
        if not any(bool(truth[abs(v)])==(v>0) for v in cl):
            return False
    return True


def projective_normals():
    return (u for u in product(range(3),repeat=6)
            if any(u) and next(z for z in u if z)!=2)


def fingerprint_111():
    anchor,_=anchored111()
    hist=Counter()
    for u in projective_normals():
        counts=[0,0,0]
        for p in anchor:counts[sum(a*b for a,b in zip(u,p))%3]+=1
        hist[tuple(sorted(counts,reverse=True))]+=1
    return hist


def grid_lines(grid):
    lines=[]
    for a in range(3):
        lines.append(tuple(grid[a][b] for b in range(3)))
        lines.append(tuple(grid[b][a] for b in range(3)))
        lines.append(tuple(grid[b][(b+a)%3] for b in range(3)))
        lines.append(tuple(grid[b][(a-b)%3] for b in range(3)))
    return lines


def grid_negative_controls():
    out=[]
    for grid in GRID_COUNTERMODELS:
        assert tuple(sorted(grid[0],reverse=True)) in F111
        assert sum(map(sum,grid))==287
        assert sum(grid[1])==sum(grid[2])==88
        assert all(20<=x<=45 for row in grid for x in row)
        lines=grid_lines(grid)
        assert len(lines)==12
        assert sum(lines[0])==111
        assert all(63<=sum(l)<=109 for l in lines[1:])
        out.append({'anchor_profile':list(grid[0]),'grid':[list(row) for row in grid],
                    'other_line_sums':sorted(sum(l) for l in lines[1:])})
    return out


class CAP023(unittest.TestCase):
    def test_known_236_and_anchor_235(self):
        cap=known236()
        self.assertTrue(verify_cap(cap,7))
        anchor,missing=anchored111()
        self.assertEqual({p[1:] for p in cap if p[0]==0},anchor|{missing})
        reduced=cap-{(0,)+missing}
        self.assertEqual(len(reduced),235)
        self.assertTrue(verify_cap(reduced,7))
        self.assertTrue(check_witness(reduced,235))
    def test_perfect_matching_between_anchor_graphs(self):
        h=make112(B0);a,p=anchored111()
        edges112=set(forbidden_edges(h));edges111=set(forbidden_edges(a))
        self.assertEqual((len(edges112),len(edges111)),(81648,80919))
        diff=edges112-edges111
        self.assertEqual(len(diff),729)
        self.assertEqual(len({x for x,_ in diff}),729)
        self.assertEqual(len({y for _,y in diff}),729)
        self.assertEqual(diff,{(i+1,pack(third(p,digits(i)))+730) for i in range(729)})
    def test_exact_clause_count(self):
        s=stats(287)
        self.assertEqual(s['external_target'],176)
        self.assertEqual(s['total_variables'],242666)
        self.assertEqual(s['total_clauses'],738782)
        self.assertEqual(sum(1 for _ in lines6()),88452)
    def test_fingerprint_independently(self):
        self.assertEqual(fingerprint_111(),F111)
    def test_all_four_grid_countermodels(self):
        self.assertEqual(len(grid_negative_controls()),4)
    def test_omitted_anchor_edge_is_really_a_matching(self):
        anchor,missing=anchored111()
        y=(0,)*6
        z=third(missing,y)
        self.assertNotIn((pack(y)+1,pack(z)+730),set(forbidden_edges(anchor)))
        self.assertIn((pack(y)+1,pack(z)+730),set(forbidden_edges(anchor|{missing})))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--target',type=int,default=287)
    parser.add_argument('--out',type=str)
    parser.add_argument('--test',action='store_true')
    args=parser.parse_args()
    if args.test:
        unittest.main(argv=['cap023','-v'])
    elif args.out:
        print(json.dumps(write_cnf(args.out,args.target),sort_keys=True,indent=2))
    else:
        print(json.dumps({'stats':stats(args.target),
                          'grid_negative_controls':grid_negative_controls()},sort_keys=True,indent=2))
