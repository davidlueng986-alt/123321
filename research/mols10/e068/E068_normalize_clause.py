#!/usr/bin/env python3
"""Transform a valid Egan partial-pair no-transversal core into E065 first-row/first-column gauge.
Adds a full-5D OA SAT clause that is logically implied by all 100/100/100 solutions.
"""
from __future__ import annotations
import json,pathlib
from E068_independent_verify import witness, valid_witness
ROOT=pathlib.Path(__file__).resolve().parent

def n10_id(s,r,c,v):return 1+(((s*10+r)*10+c)*10+v)

def main():
    A,B=json.loads((ROOT/'E061_near_triple.json').read_text())['squares'][:2]
    n=10;raw=[A,B]
    maps=[]
    for M in raw:
        smap={M[0][c]:c for c in range(n)}
        assert len(smap)==n
        maps.append(smap)
    relabeled=[[[maps[s][raw[s][r][c]] for c in range(n)] for r in range(n)] for s in range(2)]
    assert all(M[0]==list(range(n)) for M in relabeled)
    rowmap={r:relabeled[0][r][0] for r in range(n)}
    assert sorted(rowmap.values())==list(range(n)) and rowmap[0]==0
    normalized=[[[None]*n for r in range(n)] for s in range(2)]
    for s in range(2):
        for old_r in range(n):normalized[s][rowmap[old_r]]=relabeled[s][old_r][:]
    assert all(M[0]==list(range(n)) for M in normalized)
    assert [normalized[0][r][0] for r in range(n)]==list(range(n))
    assert all(sorted(normalized[s][r])==list(range(n)) for s in range(2) for r in range(n))
    assert all(sorted(normalized[s][r][c] for r in range(n))==list(range(n)) for s in range(2) for c in range(n))
    assert len({(normalized[0][r][c],normalized[1][r][c]) for r in range(n) for c in range(n)})==100
    best=json.loads((ROOT/'E068_best_core.json').read_text())
    known_list=sorted([[s,rowmap[r],c,maps[s][v]] for s,r,c,v in best['known_symbols']])
    assert len(known_list)==best['literal_count']
    known={(s,r,c):v for s,r,c,v in known_list}
    anch=[rowmap[best['anchor'][0]],best['anchor'][1]]
    assert witness(n,known,tuple(anch)) is None
    for i,(s,r,c,v) in enumerate(known_list):
        reduced=dict(known);assert reduced.pop((s,r,c))==v
        assert valid_witness(n,reduced,tuple(anch),witness(n,reduced,tuple(anch))),('no witness',i)
    # DIMACS literal x(s,r,c,v) one-hot assignments, negated to exclude this core.
    lits=[-n10_id(s,r,c,v) for s,r,c,v in known_list]
    assert len(lits)==len(set(lits))==best['literal_count']
    record={'n':10,'source':'Egan-Wanless orthogonal pair partial obstruction','normalization':'independent symbol relabel: three first rows identity; row permutation A[:,0]=identity',
      'row_map_old_to_new':[rowmap[r] for r in range(n)],'symbol_map_old_to_new':[{str(k):v for k,v in maps[s].items()} for s in range(2)],
      'anchor_normalized':anch,'known_literals':known_list,'literal_count':len(lits),'nogood_dimacs_literals':lits,
      'is_implied_by_full_OA':True,'proof':'Any third-square symbol class yields a transversal through anchor; exhaustive wildcard-relaxed enumeration shows no such transversal when all listed A/B assignments hold.',
      'full_branch_classes_excluded':0}
    all_cores=json.loads((ROOT/'E068_all_12_anchors.json').read_text())['results']
    all_cuts=[]
    for core in all_cores:
        anchor2=[rowmap[core['anchor'][0]],core['anchor'][1]]
        known2=sorted([[s,rowmap[r],c,maps[s][v]] for s,r,c,v in core['known_symbols']])
        assert witness(10,{(s,r,c):v for s,r,c,v in known2},tuple(anchor2)) is None
        ls=[-n10_id(s,r,c,v) for s,r,c,v in known2]
        all_cuts.append({'anchor':anchor2,'count':len(ls),'known_symbols':known2,'dimacs_literals':ls})
    assert len(all_cuts)==12 and len({tuple(x['dimacs_literals']) for x in all_cuts})==12
    (ROOT/'E068_all_12_sound_nogoods.json').write_text(json.dumps({'n':10,'cuts':all_cuts,'proof_scope':'sound implied clauses for any complete OA(100,5,10,2)'},indent=2)+'\n')
    (ROOT/'E068_12_nogoods.dimacs.txt').write_text(''.join(' '.join(map(str,x['dimacs_literals']))+' 0\n' for x in all_cuts))
    (ROOT/'E068_normalized_sound_nogood.json').write_text(json.dumps(record,indent=2)+'\n')
    (ROOT/'E068_nogood_dimacs_clause.txt').write_text(' '.join(map(str,lits))+' 0\n')
    print(json.dumps({'anchor':anch,'literals':len(lits),'max_var':max(-x for x in lits),'B_firstcol':[normalized[1][r][0] for r in range(n)]},indent=2))
if __name__=='__main__':main()
