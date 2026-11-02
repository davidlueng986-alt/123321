"""CAP-019 independent exact integer finite audit of Drive v6 proposed r3(7)<=287.
No external dependencies; mathematical assumptions: Potechin maximal112 uniqueness,
Thackeray 110-cap completion, and the common-tangent lemma proved in CAP019 report.
"""
import unittest
from itertools import product
from collections import Counter
C={291:(631,174486,3197526333),290:(617,170139,3097556132),289:(302,83061,1502493511),288:(211,57752,1036689408)}
EXPECTED={291:-3033966,290:-22713024,289:-20848032,288:4557600}
B=182304

def profiles(M):
    for a in range(min(M,112),-1,-1):
        for b in range(min(M-a,a),-1,-1):
            c=M-a-b
            if 0<=c<=b:
                d=224-a-b
                if a>=110 and b>=110 and c>165*(44+d)//(126-d):continue
                yield (a,b,c)

def delta(M,t):
    a,b,c=t;u,v,w=C[M]
    return u*(a**3+b**3+c**3)-v*(a*a+b*b+c*c)+w

def spectrum(k,rank,last):
    diag=([1]*(rank-1)+[last] if rank else [])+[0]*(k-rank)
    count=[1,0,0]
    for a in diag:
        out=[0,0,0]
        for r in range(3):out[r]+=count[r];out[(r+a)%3]+=2*count[r]
        count=out
    assert sum(count)==3**k and (count[0]-1)%2==count[1]%2==count[2]%2==0
    return ((count[0]-1)//2,count[1]//2,count[2]//2)

def certify():
    info={}
    for M in C:
        p=list(profiles(M));assert p and all(delta(M,t)>=0 for t in p)
        S2=364*M*M+729*M
        S3=121*M*(M-1)*(M-2)+1092*M*(M-1)+1093*M
        u,v,w=C[M];moment=u*S3-v*S2+1093*w
        assert moment==EXPECTED[M]
        info[M]=(len(p),moment)
    assert 364*288*288+729*288-1093*3*96*96==B
    for t in profiles(288):
        d=delta(288,t);excess=sum(x*x for x in t)-27648
        r={x%3 for x in t}
        if r=={2}:assert d>=19362
        elif r=={0}:assert d>=214*excess
        elif r=={1}:
            if d==0:assert t==(112,109,67) and excess==1266
            else:assert d>=16830
        else:assert r=={0,1,2} and excess>=2 and d>=6032+77*(excess-2)
    checks=[]
    for case,k in [(1,7),(2,6)]:
        quad=[(0,1)]+[(r,c) for r in range(1,k+1) for c in (1,2)]
        for rank,last in quad:
            n0,n1,n2=spectrum(k,rank,last)
            base=0 if case==1 else 729*6032
            if n2:lb=base+n2*19362
            elif rank==0:
                lb=214*B if case==1 else base+77*(B-2*729)
            else:
                assert rank==1 and n1>0
                remaining=B-(0 if case==1 else 2*729)
                lb=base+(n1-min(n1,remaining//1266))*16830
            assert lb>4557600,(case,rank,last,lb)
            checks.append((case,rank,last,lb))
    assert len(checks)==28 and min(x[3] for x in checks)==4704966
    # Falsifies a mistaken intermediate estimate in Drive v6:
    # variance budget 182304, not 185664; 3016 is NOT a valid slope.
    assert delta(288,(111,108,69))==235188<3016*1098
    return info,checks

class CAP019(unittest.TestCase):
    def test_exact_287_certificate(self):self.assertEqual(len(certify()[1]),28)
    def test_fourier_spectrum_classical_112(self):
        def orb(rep):return {tuple(sorted(0 if x==0 else (x-1+s)%5+1 for x in rep)) for s in range(5)}
        blocks=orb((0,1,2))|orb((1,2,4))
        shell={v for v in product((1,2),repeat=6) if v.count(2)%2==0}
        def cap(blocks):
            h=set(shell)
            for b in blocks:
                for v in product((1,2),repeat=3):
                    x=[0]*6
                    for i,t in zip(b,v):x[i]=t
                    h.add(tuple(x))
            assert len(h)==112
            for x in h:
                for y in h:
                    if x!=y:assert tuple((-x[i]-y[i])%3 for i in range(6)) not in h
            return h
        h=cap(blocks);hp=cap(set(__import__('itertools').combinations(range(6),3))-blocks)
        dirs=[u for u in product(range(3),repeat=6) if any(u) and next(x for x in u if x)==1]
        def dual(h):
            d=set()
            for u in dirs:
                a=Counter(sum(x[i]*u[i] for i in range(6))%3 for x in h)
                t=tuple(a[j] for j in range(3))
                assert t in ((22,45,45),(40,36,36))
                if t==(22,45,45):d.add(u)
            assert len(d)==56
            return d
        dh,dp=dual(h),dual(hp);common=dh&dp
        assert len(common)==16
        rep=Counter(tuple((x[i]+y[i])%3 for i in range(6)) for x in h for y in hp)
        holes=0
        for z in product(range(3),repeat=6):
            m=sum(sum(z[i]*u[i] for i in range(6))%3==0 for u in common)
            expected=16-16*(z==(0,)*6)+4*(z in h)+4*(z in hp)+3*m-len(common)
            assert rep[z]==expected
            holes+=rep[z]==0
        self.assertEqual(holes,12)

if __name__=='__main__':unittest.main(verbosity=2)
