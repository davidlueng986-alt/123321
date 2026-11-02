#!/usr/bin/env python3
"""CAP-021: exact-integer 6D-slice forcing certificate (stdlib, CPU-only).

The M=287/288 conditional cases require the separately audited CAP-017B
two-near-maximal-slices tangent lemma and 110-cap completion.
Moment-compatible histograms are NOT cap constructions.
"""
import json
import unittest

N = (3**7 - 1)//2
# M, assumed max section, exclude pairs of >=110 sections, alpha, beta,
# gamma, expected profile count, expected negative sum.
CASES = (
    (286,109,False,40,10893,193029098,161,-2468100),
    (287,110,True,82,22401,399662803,175,-4531050),
    (288,111,True,589,161442,2900219904,189,-29038176),
)
# Histograms satisfy ONLY global moments, NOT geometric incidence.
FORMAL_MODELS = {
    285: {(109,109,67):152,(101,96,88):3,(98,94,93):2,
          (96,95,94):826,(95,95,95):110},
    287: {(111,109,67):140,(111,96,80):2,(110,109,68):6,
          (101,94,92):1,(98,95,94):47,(97,97,93):1,
          (96,96,95):896},
}

# A stronger negative control: a formal 287-direction histogram matching
# BOTH global S2/S3 moments and the projective value counts of an actual
# rank-2 quadratic form Q=x1^2+x2^2 on F3^7: (121,486,486).
# It is NOT a point-set witness and need not satisfy per-direction geometry.
GAUSSIAN_RANK2_MODEL = {
    (112,109,66):33,(111,109,67):109,(100,95,92):3,
    (98,98,91):13,(98,95,94):2,(97,96,94):344,
    (97,95,95):468,(96,96,95):121,
}

def moments(m):
    """Projective-normal sums of 1, S2, S3 for an m-point cap in F3^7."""
    return (N,364*m*m+729*m,
            121*m*(m-1)*(m-2)+1092*m*(m-1)+1093*m)

def s2(t): return sum(x*x for x in t)
def s3(t): return sum(x*x*x for x in t)

def profiles(m,upper,conditional=False):
    for a in range(min(m,upper),-1,-1):
        for b in range(min(a,m-a),-1,-1):
            c=m-a-b
            if c<0 or c>b: continue
            if conditional and a>=110 and b>=110:
                # In our M=287/288, upper<=111 cases c>=66;
                # CAP-017B gives c<=64 whenever both a,b>=110.
                assert c>=66
                continue
            yield (a,b,c)

def certificate(m,upper,conditional,alpha,beta,gamma,n_expected,sum_expected):
    ps=list(profiles(m,upper,conditional))
    assert len(ps)==n_expected
    vals=[alpha*s3(t)-beta*s2(t)+gamma for t in ps]
    assert min(vals)==0
    n,m2,m3=moments(m)
    total=alpha*m3-beta*m2+gamma*n
    assert total==sum_expected and total<0
    return {"M":m,"max_slice_assumed":upper,"conditional_CAP017B":conditional,
            "admissible_profiles":len(ps),"functional":[alpha,-beta,gamma],
            "minimum":min(vals),"zero_profiles":[list(t) for t,v in zip(ps,vals) if v==0],
            "global_sum":total,"moments":[n,m2,m3]}

def check_formal_model(m,rows,max_section):
    assert all(sum(t)==m and 0<=t[2]<=t[1]<=t[0]<=max_section
               and isinstance(k,int) and k>=0 for t,k in rows.items())
    got=(sum(rows.values()),sum(k*s2(t) for t,k in rows.items()),
         sum(k*s3(t) for t,k in rows.items()))
    assert got==moments(m)
    return {"M":m,"max_section":max_section,
            "histogram":[[list(t),k] for t,k in rows.items()],
            "moments":list(got),"WARNING":"FORMAL_MOMENT_MODEL_NOT_A_CAP"}

class TestCAP021(unittest.TestCase):
    def test_exact_functionals(self):
        for row in CASES:
            with self.subTest(M=row[0]): certificate(*row)
    def test_285_formal_countermodel(self):
        check_formal_model(285,FORMAL_MODELS[285],109)
    def test_287_formal_countermodel(self):
        check_formal_model(287,FORMAL_MODELS[287],111)
    def test_287_requires_tangent_exclusion(self):
        t=(110,110,67)
        self.assertEqual(sum(t),287)
        self.assertLess(82*s3(t)-22401*s2(t)+399662803,0)
        self.assertIn(t,list(profiles(287,110,False)))
        self.assertNotIn(t,list(profiles(287,110,True)))
    def test_rank2_gaussian_aggregate_negative_control(self):
        check_formal_model(287,GAUSSIAN_RANK2_MODEL,112)
        q=[0,0,0]
        for t,n in GAUSSIAN_RANK2_MODEL.items():
            residue_counts=[sum(x%3==r for x in t) for r in range(3)]
            self.assertEqual(sorted(residue_counts),[0,1,2])
            q[residue_counts.index(2)]+=n
            self.assertFalse(t[0]>=110 and t[1]>=110)
        self.assertEqual(q,[121,486,486])
        # Q=x1^2+x2^2: zero count 3^5, each nonzero value 4*3^5,
        # projectivize by dividing nonzero vectors by 2.
        self.assertEqual(((3**5-1)//2,2*3**5,2*3**5),tuple(q))
    def test_no_claim_below_286(self):
        self.assertEqual(max(t[0] for t in FORMAL_MODELS[285]),109)

if __name__=="__main__":
    print(json.dumps({"certificates":[certificate(*r) for r in CASES],
      "formal_models":[check_formal_model(m,FORMAL_MODELS[m],109 if m==285 else 111)
                       for m in (285,287)],
      "random_seed":None,"gpu_used":False,"external_solver_required":False},
      indent=2,sort_keys=True))
    unittest.main(verbosity=2)
