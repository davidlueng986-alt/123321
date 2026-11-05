#!/usr/bin/env python3
"""CAP050 candidate rigorous global r3(7)<=290 by projective-centre 3rd moments.

Pure Python integers; no scipy, GPU, paid compute, or SAT.
Conditional on peer-reviewed external theorems:
  (A) Potechin 2008: all AG(6,3) 112-caps affinely equivalent to doubled Hill cap;
      this representative is centrally symmetric with 56 antipodal pairs.
  (B) Barat-Edel-Hill-Storme 2004: projective PG(6,3) cap size <=136.

This is a global upper BOUND, not an exact solution to r3(7).
The proof and external dependencies still require independent mathematical review.
"""
from fractions import Fraction
from math import comb
import json

N=291;D=1093;L2=364;L3=121;L4=40

def fall(n,k):
 p=1
 for i in range(k):p*=n-i
 return p

def verify_hyperplane_112_forcing():
    P=[(a,b,N-a-b) for a in range(N-224,113)
       for b in range(a,113) if b<=N-a-b<=112]
    assert len(P)==192
    contact=[]
    for a,b,c in P:
        q2=a*a+b*b+c*c;q3=a**3+b**3+c**3
        ind=int(c==112)
        slack=1350*ind+5080860-277*q2+q3
        assert slack>=0,(a,b,c,slack)
        if slack==0:contact.append((a,b,c))
    assert contact==[(67,112,112),(69,111,111),(97,97,97)]
    S2=D*N+L2*fall(N,2)
    S3=D*N+3*L2*fall(N,2)+L3*fall(N,3)
    lower_times1350= -5080860*D +277*S2-S3
    assert lower_times1350==92538
    assert Fraction(lower_times1350,1350)==Fraction(5141,75)
    directions_at_least=(-(-lower_times1350//1350))
    assert directions_at_least==69
    return {'profiles_checked':len(P),'contact':contact,'S2':S2,'S3':S3,
            'exact_minimum_direction_count_from_dual':str(Fraction(5141,75)),
            'at_least_112_slice_directions':directions_at_least}

def verify_projective_center_cost():
    results=[]; min_gap=None; min_at=None
    for d in range(0,137):
        delta=(d-22)*(d-23)//2
        assert (d-22)*(d-23)%2==0 and delta>=0
        if d<56:
            continue
        k=(d-2)//3
        assert 0<=k<=44
        numerator=(40*d*(d-1)*(d-2)+(2-2*k)*121*d*(d-1)
                   +k*(k-1)*364*d)
        denominator=56*(56-k)*(55-k)
        assert numerator>=0 and denominator>0
        diff=delta*denominator-46*numerator
        assert diff>=0,(d,k,diff)
        gap=Fraction(diff,denominator)
        if min_gap is None or gap<min_gap:
            min_gap=gap;min_at=(d,k)
        results.append((d,k,diff))
    assert len(results)==81
    assert min_at==(136,44) and min_gap==Fraction(25922,231)
    outsider_count=3**7-N
    total_secants=comb(N,2)
    assert outsider_count==1896 and total_secants==42195
    base=22*total_secants-253*outsider_count
    assert base==448602
    at_least_centers=69
    coplanar4_lower=base+46*at_least_centers
    assert coplanar4_lower==451776
    return {'projective_degree_cases_checked':len(results),
            'max_d_by_published_projective_cap_theorem':136,
            'projective_moment_cubic_constant':46,
            'choice_k':'floor((d-2)/3)',
            'minimal_positive_gap_delta_minus_46_t_upper':str(min_gap),
            'minimal_gap_attained_at_degree_and_k':min_at,
            'secants_total':total_secants,'outsiders':outsider_count,
            'coplanar4_baseline':base,
            'minimum_112_slice_directions':at_least_centers,
            'coplanar4_stronger_global_lower':coplanar4_lower}

def verify_fourth_moment_upper():
    P=[(a,b,N-a-b) for a in range(N-224,113)
       for b in range(a,113) if b<=N-a-b<=112]
    assert len(P)==192
    for a,b,c in P:
        q2=a*a+b*b+c*c;q3=a**3+b**3+c**3;q4=a**4+b**4+c**4
        assert 9957864606-743397*q2+5482*q3-15*q4>=0
    S2=D*N+L2*fall(N,2)
    S3=D*N+3*L2*fall(N,2)+L3*fall(N,3)
    S4max=Fraction(9957864606*D-743397*S2+5482*S3,15)
    base=(D*N+7*L2*fall(N,2)+6*L3*fall(N,3)+L4*fall(N,4))
    coplanar4_upper=(S4max-base)/1944
    assert coplanar4_upper==Fraction(548600572,1215)
    return {'N291_all_fourth_dual_profiles':len(P),
            'P_upper':str(coplanar4_upper),
            'P_upper_floor':coplanar4_upper.numerator//coplanar4_upper.denominator}

def main():
    h=verify_hyperplane_112_forcing()
    p=verify_projective_center_cost()
    f=verify_fourth_moment_upper()
    assert p['coplanar4_stronger_global_lower']>f['P_upper_floor']
    gap=Fraction(p['coplanar4_stronger_global_lower'])-Fraction(f['P_upper'])
    assert gap==Fraction(307268,1215)
    return {'experiment':'CAP050','theorem':'No 291-point cap in AG(7,3) under cited published theorems; r3(7)<=290',
            'note':'Candidate independent global upper improvement over published 291; stronger Thackeray 2022 preprint 288 already claimed. Independent mathematical referee and source audit required; exact r3(7) remains OPEN.',
            'external_assumptions':['Potechin 2008 AG6 unique 112 max, centrally symmetric doubled Hill cap','Barat-Edel-Hill-Storme 2004 projective m2(6,3)<=136'],
            'directions':h,'center_cost':p,'fourth_dual':f,
            'exact_P_contradiction':str(gap),'root_exact_status':'OPEN',
            'new_237_witness':False}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True))
