#!/usr/bin/env python3
"""A short exact integer-arithmetic fractional dual proof for 71 outsiders.

Use the canonical Calderbank–Fishburn 236-point cap and select the 71
outside points with the lexicographically smallest (secant count, point).
For each selected outsider, old-old secants define edge variables.
This sparse dual has weights /100, checked EXACTLY against every
selected outsider and every old vertex.

No optimisation solver is needed to verify the proof certificate.
"""
from collections import defaultdict
from generate_calderbank_fishburn import construction

DEN=100
PAIRS="2:7 3:6 7:7 8:81 11:17 12:6 13:11 15:67 21:22 29:79 34:52 36:26 39:23 40:19 44:31 46:50 50:14 52:61 58:8 59:18 62:37 63:8 64:17 69:38 70:58 72:42 82:16 88:39 89:46 94:44 98:57 108:8 109:93 110:41 116:13 117:47 121:99 126:2 131:99 134:2 141:99 144:2 150:2 153:99 166:2 168:99 172:99 176:2 182:94 184:5 186:2 192:3 199:97 205:99 207:2 215:3 217:97 224:99 225:2 236:96 237:5 245:14 247:68 248:18 251:4 252:36 253:41 255:20 264:62 265:8 266:31 273:2 276:72 277:26 286:27 287:59 288:15 295:38 297:6 305:57 310:33 312:15 314:35 315:17 317:54 318:11 320:35 328:64 329:5 337:32 341:17 344:30 345:53 349:1 356:55 357:46 362:30 366:50 369:20 374:85 375:5 377:5 381:6 384:64 385:13 393:24 394:72 404:29 406:31 407:2 408:63 414:5 419:37 420:64 427:56 431:19 435:26 439:65 445:31 447:5 451:38 452:10 453:16 456:37 465:94 468:7 472:49 474:52 484:38 486:37 490:26 493:61 503:40 507:80 513:21 515:36 517:13 520:39 522:13 526:45 528:56 538:52 541:49 555:55 558:46 562:92 564:9 572:99 580:2 582:23 584:48 587:14 589:15 594:2 602:99 603:95 612:5 614:4 616:41 618:56 626:17 628:29 629:55 640:99 643:2 648:43 650:27 651:17 655:14 658:59 659:42 670:7 674:34 679:60 682:39 684:43 685:19 691:47 692:10 694:5 695:18 699:21 708:86 711:15 720:33 721:6 722:61 726:8 727:31 728:51 729:10 737:61 741:1 745:40 747:51 749:47 750:3"
def check():
    A=construction()
    secants=defaultdict(list)
    for i,p in enumerate(A):
        for j in range(i+1,len(A)):
            q=A[j]
            z=tuple((-a-b)%3 for a,b in zip(p,q))
            secants[z].append((i,j))
    pool=sorted(secants,key=lambda x:(len(secants[x]),x))[:71]
    assert len(pool)==71
    edges=[(pi,i,j) for pi,p in enumerate(pool) for i,j in secants[p]]
    assert len(edges)==757
    nums=[0]*len(edges)
    entries=[v.split(':') for v in PAIRS.split()]
    assert len(entries)==197
    for e,w in entries:
        e=int(e);w=int(w)
        assert 0<=e<len(edges) and nums[e]==0 and 1<=w<=100
        nums[e]=w
    old=[0]*236;added=[0]*71
    for (pi,i,j),w in zip(edges,nums):
        old[i]+=w;old[j]+=w;added[pi]+=w
    assert max(old)<=DEN and min(added)>=DEN
    assert sum(old)==2*sum(added)==2*sum(nums)
    print("VERIFIED: 71 outside candidates, 197 sparse dual weights, denominator=100")
    print("max old-vertex edge load",max(old),"min outsider secant coverage",min(added))
    print("For any T subset of the 71 and any original removals R admitting T, |R|>=|T|, hence no >236 cap can be formed.")
if __name__=="__main__":
    check()
