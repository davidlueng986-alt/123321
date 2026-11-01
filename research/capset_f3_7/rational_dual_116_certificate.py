#!/usr/bin/env python3
"""Exact rational dual certificate excluding a reproducible 116-point pool.

Candidate pool: sorted exterior points with secant count <=12, sample
116 without replacement using Python random.Random(20261103).
Fixed 345 positive secant-edge weights have denominator 50.
This script independently checks the integer inequalities, no solver.
"""
import itertools,random
from collections import defaultdict
from generate_calderbank_fishburn import construction
W="0:32 4:8 5:10 14:30 17:18 20:2 21:1 23:30 32:21 34:11 36:10 38:30 48:16 51:35 56:21 59:18 64:11 71:16 73:26 75:9 79:15 81:19 82:12 86:4 87:1 94:12 96:3 97:36 102:10 106:28 108:12 119:19 120:17 124:14 127:20 129:20 130:11 139:24 141:26 148:29 151:16 159:5 164:38 165:12 171:21 173:3 174:27 187:6 192:34 193:11 194:13 195:9 200:28 205:36 210:13 212:1 218:7 219:20 224:24 232:17 233:8 234:26 242:11 247:12 251:27 254:44 258:5 259:1 267:18 269:22 271:11 276:23 277:5 278:14 281:8 287:2 295:49 301:12 304:6 307:32 310:13 319:37 321:2 324:23 328:26 335:3 336:14 338:18 341:11 342:4 346:2 347:8 351:4 352:26 354:10 360:46 365:4 368:11 369:22 375:17 379:6 381:26 387:19 394:19 395:20 396:11 410:30 412:20 414:18 416:32 424:30 427:18 432:2 437:10 438:16 443:24 449:22 455:15 457:9 459:5 460:2 461:1 463:36 468:11 474:10 476:19 480:21 484:2 488:11 490:29 492:8 499:47 502:3 507:13 515:34 516:3 519:3 521:11 528:36 537:11 538:15 540:25 541:15 546:29 547:6 553:28 554:14 558:3 559:6 564:23 565:23 566:4 571:1 576:4 582:34 584:12 588:11 589:5 590:16 594:18 598:5 604:45 611:16 613:5 614:18 617:11 620:20 622:6 627:2 631:22 632:23 638:16 641:12 644:25 653:26 655:6 660:16 664:28 671:28 672:22 682:13 684:37 691:9 698:22 700:19 702:3 706:24 710:23 714:31 719:6 720:13 721:1 722:12 731:23 732:15 734:14 738:34 741:2 747:29 748:4 749:13 752:4 759:15 762:9 763:26 769:14 772:7 774:20 779:10 781:37 785:14 794:2 797:13 801:36 807:10 813:40 816:19 817:7 819:24 825:40 833:10 841:2 844:31 847:17 849:25 851:11 853:15 864:28 870:23 873:2 877:16 878:2 880:21 881:10 888:49 889:2 895:19 896:13 899:15 901:3 908:35 913:15 915:14 917:13 918:10 922:13 931:22 932:1 934:28 938:2 939:49 948:12 957:23 959:15 963:2 964:33 965:3 966:13 978:23 979:27 984:19 987:13 989:18 997:31 1004:14 1005:6 1010:5 1011:20 1012:6 1016:19 1018:28 1024:22 1027:1 1034:16 1035:4 1036:10 1038:20 1045:1 1046:18 1047:29 1051:2 1053:25 1054:26 1065:30 1069:21 1075:4 1077:22 1082:24 1088:6 1091:19 1097:26 1098:37 1099:13 1114:3 1116:43 1117:4 1129:24 1130:26 1132:45 1136:4 1141:1 1151:1 1153:50 1159:2 1161:25 1163:23 1170:24 1176:27 1179:27 1180:24 1189:8 1198:38 1200:4 1202:4 1206:42 1209:5 1214:21 1222:29 1224:13 1228:17 1229:20 1238:28 1243:22 1246:5 1249:8 1250:38 1260:13 1265:31 1269:6 1275:20 1279:3 1281:28 1284:7 1287:23 1292:21 1294:28 1295:20 1304:2 1307:12 1308:10 1311:6 1314:22 1321:12 1323:10 1326:28"
def verify():
    A=construction();Aset=set(A);sec=defaultdict(list)
    for i,x in enumerate(A):
        for j in range(i+1,len(A)):
            y=A[j]
            sec[tuple((-u-v)%3 for u,v in zip(x,y))].append((i,j))
    low=sorted(p for p in sec if len(sec[p])<=12)
    assert len(low)==920
    pool=random.Random(20261103).sample(low,116)
    edges=[(j,i,k) for j,p in enumerate(pool) for i,k in sec[p]]
    assert len(edges)==1328
    nums=[0]*len(edges)
    pairs=[pair.split(':') for pair in W.split()]
    assert len(pairs)==345
    for index,weight in pairs:
        index=int(index);weight=int(weight)
        assert 0<=index<len(nums) and nums[index]==0 and 0<weight<=50
        nums[index]=weight
    old=[0]*236;new=[0]*116
    for (j,i,k),w in zip(edges,nums):
        old[i]+=w;old[k]+=w;new[j]+=w
    assert max(old)<=50 and min(new)>=50
    assert sum(old)==2*sum(nums)==2*sum(new)
    print("CERTIFIED: no cap enlargement by outsiders exclusively from this seeded 116-point pool")
    print("weights=345, denominator=50, max old load=",max(old),"min candidate coverage=",min(new))
if __name__=="__main__":
    verify()
