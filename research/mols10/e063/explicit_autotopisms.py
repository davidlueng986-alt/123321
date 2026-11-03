import runpy,json
from pathlib import Path
D=Path(__file__).parent
V=runpy.run_path(str(D/'classify_C.py'))
Q=V['Q']; n=10;allowed=V['allowed'];act=V['act'];perms=V['perms'];orbits=V['orbits']
cert=[]
for orbit in orbits:
 j=orbit[0]
 automorphisms=[]
 for a in allowed:
  for perm in perms:
   m={**a['fixed_relabel'],**dict(zip((1,2,3),perm))}
   if all(m[Q[j][r][c]]==Q[j][a['r'][r]][a['c'][c]] for r in range(n) for c in range(n)):
    assert sorted(a['r'])==list(range(n)) and sorted(a['c'])==list(range(n)) and sorted(m.values())==list(range(n))
    automorphisms.append({'row_perm':a['r'],'col_perm':a['c'],'sym_perm':[m[v] for v in range(n)]})
 p=next((p for p in automorphisms if p['row_perm']!=list(range(n)) or p['col_perm']!=list(range(n)) or p['sym_perm']!=list(range(n))),None)
 if p: cert.append({'C_index':j,'orbit_size':len(orbit),'autotopisms':len(automorphisms),'nontrivial':p})
 print('ORBIT',j,'size',len(orbit),'aut_group',len(automorphisms),'excluded_by_known_theorem',bool(p),flush=True)
assert len(cert)==3 and all(x['orbit_size']==6 for x in cert)
json.dump({'theorem':'McKay-Meynert-Myrvold 2007: any order10 Latin square in three MOLS has trivial autoparatopism group','known_reference':'https://doi.org/10.1002/jcd.20105','scope':'C completions of ONE fixed partial C7 pattern; 3 out of 14 symmetry orbits excluded using published theorem','excluded_orbits':cert,'remaining_orbits':11,'not_global_solution':True},open(D/'E063_symmetric_C_exclusions.json','w'),indent=2)
print('EXACT_SYMMETRIC_C_PATTERN_EXCLUSIONS',len(cert),'of',len(orbits),'classes,',sum(x['orbit_size'] for x in cert),'of',len(Q),'labelled C completions')