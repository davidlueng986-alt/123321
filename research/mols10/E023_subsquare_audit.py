#!/usr/bin/env python3
"""Independent exhaustive 4x4 subsquare-compatibility audit (E023)."""
import itertools,json,collections

OMEGA={
 'Z4': [[(r+c)%4 for c in range(4)] for r in range(4)],
 'V4': [[r^c for c in range(4)] for r in range(4)]
}
TYPES={'R':[1]*8+[4]*2,'S':[1]*7+[3]*3,'T':[1]*7+[2,3,4],
'U':[1]*6+[2]*2+[3]*2,'V':[1]*6+[2]*3+[4],
'W':[1]*5+[2]*4+[3],'X':[1]*4+[2]*6}

def compatible(L,cols,vals):
    return all(not (L[r][c]==v and L[r][d]==w)
        for r in range(4) for (c,v),(d,w) in itertools.combinations(zip(cols,vals),2))

def independent_compatible(L,cols,vals):
    witnesses=[next(r for r in range(4) if L[r][c]==v) for c,v in zip(cols,vals)]
    return len(set(witnesses))==len(witnesses)

def audit():
    stats={};full={}
    for name,L in OMEGA.items():
        out={}; rows=[]
        for k in range(1,5):
            valid=[]
            for cols in itertools.combinations(range(4),k):
                for vals in itertools.permutations(range(4),k):
                    x=compatible(L,cols,vals)
                    assert x==independent_compatible(L,cols,vals)
                    if x:valid.append((cols,vals))
            out[str(k)]={'compatible_partial_rows':len(valid),
                'total_partial_rows':len(list(itertools.combinations(range(4),k)))*
                  len(list(itertools.permutations(range(4),k)))}
            if k==4:rows=valid
        stats[name]=out
        full[name]=[list(v) for c,v in rows]
        if name=='V4':
            ext={}
            for k in range(1,5):
                multiplicities=[]
                for cols in itertools.combinations(range(4),k):
                    for vals in itertools.permutations(range(4),k):
                        if compatible(L,cols,vals):
                            multiplicities.append(sum(all(p[c]==v for c,v in zip(cols,vals))
                                for p in full[name]))
                ext[str(k)]=dict(collections.Counter(multiplicities))
            stats[name]['extension_multiplicities']=ext
            assert ext['2']=={1:48} and ext['3']=={1:32} and ext['1']=={2:16}
    assert stats['Z4']['4']['compatible_partial_rows']==0
    assert stats['V4']['4']['compatible_partial_rows']==8
    table={case:{
        'Z4_compatible':all(stats['Z4'][str(k)]['compatible_partial_rows']>0
                            for k in TYPES[case[0]]+TYPES[case[1]]),
        'V4_compatible':all(stats['V4'][str(k)]['compatible_partial_rows']>0
                            for k in TYPES[case[0]]+TYPES[case[1]])
        } for case in ['SX','UX','VX','WX','XX','UU','UW','WW']}
    assert table['VX']=={'Z4_compatible':False,'V4_compatible':True}
    return {'source':'https://github.com/curtisbright/Myrvold-MOLS/blob/master/verify.py',
        'method':'exhaustive combinations of columns and injective symbols, independent row-witness replay',
        'counts':stats,'full_compatible_permutations':full,
        'residual_type_necessary_local_feasibility':table,
        'caution':'Local feasibility is not a global SAT witness; Z4 excluded for any row with four white entries.'}
if __name__=='__main__':
    print(json.dumps(audit(),indent=2))
