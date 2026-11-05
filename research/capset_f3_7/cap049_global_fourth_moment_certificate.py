#!/usr/bin/env python3
"""CAP049 root-directed global fourth moment exact proof audit (stdlib only).
Re-proves the ALREADY-PUBLISHED numerical upper r3(7)<=291; exact problem OPEN.
Assumes known r3(6)=112. No solver or floating-point in certificate verification.
"""
from math import comb
from fractions import Fraction
import json
D=1093;L2=364;L3=121;L4=40
def falling(n,k):
    z=1
    for i in range(k):z*=n-i
    return z
def base_fourth(n):
    return D*n+7*L2*falling(n,2)+6*L3*falling(n,3)+L4*falling(n,4)
def prove_no_292():
    n=292
    profiles=[(a,b,n-a-b) for a in range(n-224,113)
              for b in range(a,113) if b<=n-a-b<=112]
    assert len(profiles)==184
    def P(p,k):return sum(x**k for x in p)
    slack=[30464609312-2254590*P(p,2)+16531*P(p,3)-45*P(p,4) for p in profiles]
    assert min(slack)==0 and all(v>=0 for v in slack)
    assert [p for p,v in zip(profiles,slack) if v==0]==[
        (68,112,112),(90,90,112),(97,97,98)]
    S2=D*n+L2*falling(n,2)
    S3=D*n+3*L2*falling(n,2)+L3*falling(n,3)
    upper45=30464609312*D-2254590*S2+16531*S3
    outsiders=3**7-n
    d,r=divmod(comb(n,2),outsiders)
    coplanar_min=(outsiders-r)*comb(d,2)+r*comb(d+1,2)
    assert (d,r,coplanar_min)==(22,796,455257)
    lower=base_fourth(n)+1944*coplanar_min
    assert 45*lower-upper45==48384
    return {'n':n,'profiles':len(profiles),'dual_contacts':3,'S2':S2,'S3':S3,
            'lower_S4':lower,'upper_S4':str(Fraction(upper45,45)),
            'coplanar_quadruples_min':coplanar_min,
            'contradiction_times_45':45*lower-upper45,
            'global_bound':'r3(7)<=291 (already known)'}
def check_291_gap():
    n=291
    p=[(a,b,n-a-b) for a in range(n-224,113)
       for b in range(a,113) if b<=n-a-b<=112]
    assert len(p)==192
    for a,b,c in p:
        S2=a*a+b*b+c*c
        S3=a**3+b**3+c**3
        S4=a**4+b**4+c**4
        assert 9957864606-743397*S2+5482*S3-15*S4>=0
    S2=D*n+L2*falling(n,2)
    S3=D*n+3*L2*falling(n,2)+L3*falling(n,3)
    max_coplanar=(Fraction(9957864606*D-743397*S2+5482*S3,15)-base_fourth(n))/1944
    assert max_coplanar==Fraction(548600572,1215)
    outsiders=3**7-n
    d,r=divmod(comb(n,2),outsiders)
    min_coplanar=(outsiders-r)*comb(d,2)+r*comb(d+1,2)
    assert min_coplanar==448602
    needed=max_coplanar.numerator//max_coplanar.denominator+1
    assert needed==451524
    return {'n':n,'profiles':len(p),'P_min':min_coplanar,
            'P_max':str(max_coplanar),'P_min_needed':needed,
            'additional_coplanar_quadruples_needed':needed-min_coplanar,
            'status':'291 NOT EXCLUDED'}
if __name__=='__main__':
    print(json.dumps({'rigorous_known_upper':prove_no_292(),
                      'open_improvement_target':check_291_gap()},sort_keys=True))
