#!/usr/bin/env python3
"""CAP046: EXACT formal countermodel to aggregate max-89 moments + quadratic spectra.

This is *not* a 237-point cap. It only proves that a selected family of
aggregate necessary conditions cannot itself refute a 237-cap. CPU/stdlib.
"""
from itertools import product
from collections import Counter
import json

# Every listed profile has three slice counts totaling 237, and max <=89.
# Fourth field is the number of projective normal directions with that profile.
HISTOGRAM = (
    ((59,89,89),126), ((60,88,89),129), ((71,81,85),2),
    ((73,77,87),5), ((73,80,84),1), ((75,77,85),1),
    ((76,79,82),126), ((76,80,81),297), ((78,78,81),112),
    ((78,79,80),294),
)
def quadratic_form_rank6_spectrum():
    # Every 6D nonzero normal is paired with its negative.
    counts=[0,0,0]
    for u in product(range(3),repeat=6):
        if not any(u):continue
        q=sum(x*x for x in u)%3
        counts[q]+=1
    assert all(c%2==0 for c in counts)
    return tuple(c//2 for c in counts)

def certify():
    M=237
    assert all(sum(p)==M and max(p)<=89 and min(p)>=0 for p,n in HISTOGRAM)
    normals=sum(n for p,n in HISTOGRAM)
    second=sum(n*sum(x*x for x in p) for p,n in HISTOGRAM)
    third=sum(n*sum(x**3 for x in p) for p,n in HISTOGRAM)
    expected_second=364*M*M+729*M
    expected_third=121*M*(M-1)*(M-2)+1092*M*(M-1)+1093*M
    qcounts=[0,0,0];different=0
    for p,n in HISTOGRAM:
        residues=sorted(x%3 for x in p)
        if residues==[0,1,2]:different+=n
        else:
            assert len(set(residues))==1
            qcounts[residues[0]]+=n
    qactual=quadratic_form_rank6_spectrum()
    assert normals==1093
    assert second==expected_second and third==expected_third
    assert different==729 and tuple(qcounts)==qactual==(112,126,126)
    return {'type':'FORMAL_INTEGER_HISTOGRAM_NOT_A_CAP',
            'hypothetical_size':M,'largest_slice':89,
            'normal_directions':normals,'S2':second,'S3':third,
            'type1_directions':different,'type0_quadresidue_counts':qcounts,
            'valid_rank6_quadratic_spectrum':list(qactual),
            'pointwise_directional_consistency_checked':False,
            'actual_cap_constructed':False,
            'logical_conclusion':'S2/S3 moments, barycenter type split and quadratic-rank value counts ALONE do not rule out maximum hyperplane size 89 at M=237.'}
if __name__=='__main__':print(json.dumps(certify(),sort_keys=True))
