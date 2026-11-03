import json,runpy,itertools
from pathlib import Path
D=Path(__file__).parent
v=runpy.run_path(str(D/'classify_C.py'))
acs=[]
for a in v['allowed']:
 for perm in itertools.permutations((1,2,3)):
  sy={**a['fixed_relabel'],**dict(zip((1,2,3),perm))}
  acs.append({'row_perm':a['r'],'col_perm':a['c'],'symbol_perm':[sy[i] for i in range(10)]})
assert len(acs)==18
json.dump({'actions':acs,'expected_orbits':v['orbits']},open(D/'E063_group_actions.json','w'),indent=2)