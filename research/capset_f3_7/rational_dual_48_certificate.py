#!/usr/bin/env python3
"""Exact rational dual certificate: no enlargement from 48 specified outsiders.

Original cap A of size 236, fixed outsiders B (the first 48 ordered by
(secant count, coordinates)). The hardcoded nonnegative weights w_e/7
belong to old-old secants with third point in B.
Every outsider gets total incident weight >=1; every old cap vertex
has total incident weight <=1. Therefore any deletion set R supporting
a subset T of B satisfies |R| >= |T|, so no enlargement is possible.
The proof checker below uses INTEGER arithmetic only (denominator 7).
"""
from collections import defaultdict
from generate_calderbank_fishburn import construction

CERT=[
(0,64,70,7),(1,65,71,5),(1,105,111,2),(2,88,93,7),(3,66,71,1),
(3,91,94,6),(4,40,46,7),(5,43,45,2),(5,106,111,5),(6,48,53,5),
(6,105,106,2),(7,74,79,4),(7,109,110,3),(8,80,83,7),(9,84,87,7),
(10,33,34,7),(11,52,55,7),(12,152,158,7),(13,211,213,7),
(14,192,198,7),(15,145,151,7),(16,217,218,7),(17,163,165,7),
(18,193,196,7),(19,186,191,7),(20,153,156,7),(21,205,206,7),
(22,169,170,7),(23,164,167,7),(24,26,48,2),(24,85,109,4),
(24,94,110,1),(25,92,102,7),(26,75,82,7),(27,31,67,7),
(28,125,225,7),(29,23,41,7),(30,16,32,7),(31,6,45,5),
(31,86,110,2),(32,1,44,7),(33,78,103,1),(33,95,107,6),
(34,27,66,6),(34,95,99,1),(35,8,61,7),(36,28,50,4),
(36,79,101,3),(37,11,63,7),(38,4,37,7),(39,29,51,7),
(40,5,60,6),(40,90,110,1),(41,135,224,7),(42,20,56,7),
(43,7,71,1),(43,90,103,6),(44,89,100,7),(45,72,97,7),
(46,73,96,7),(47,22,59,7)
]
DENOMINATOR=7

def prove():
    original=construction()
    lines=defaultdict(list)
    for a in range(236):
        for b in range(a+1,236):
            x,y=original[a],original[b]
            third=tuple((-u-v)%3 for u,v in zip(x,y))
            lines[third].append((a,b))
    candidates=sorted(lines,key=lambda p:(len(lines[p]),p))[:48]
    old_weight=[0]*236
    new_weight=[0]*48
    for pos,a,b,numer in CERT:
        assert 0<=pos<48 and 0<=a<b<236 and 0<=numer<=7
        assert (a,b) in lines[candidates[pos]]
        old_weight[a]+=numer
        old_weight[b]+=numer
        new_weight[pos]+=numer
    assert len(CERT)==61
    assert len(set((p,a,b) for p,a,b,n in CERT))==len(CERT)
    assert min(new_weight)>=DENOMINATOR
    assert max(old_weight)<=DENOMINATOR
    assert sum(old_weight)==2*sum(new_weight)==2*336
    return candidates,old_weight,new_weight

if __name__=="__main__":
    _,ow,nw=prove()
    print("VERIFIED EXACT DUAL: 48 outsider candidate points; 61 secant weights, denominator 7")
    print("Maximum original endpoint load",max(ow),"<= 7")
    print("Minimum outsider coverage",min(nw),">= 7")
    print("THUS for any candidate subset T from these 48 outsiders and deletion set R allowing all of T, |R|>=|T|; final cap size<=236.")
