import json,hashlib,collections,datetime
from pathlib import Path
root=Path(__file__).resolve().parent
models=[]
for enc in ('cnf','pb'):
 for n in (4,5,6):
  for d in ('','_branches'):
   path=root/f'E065_n{n}{d}_{enc}.jsonl'
   if path.exists():
    xs=[json.loads(s) for s in path.read_text().splitlines()]
    models.append({'model':enc,'n':n,'case':d or 'global',
                   'total':len(xs),'status_hist':dict(collections.Counter(x['status'] for x in xs)),
                   'seconds':round(sum(x['seconds'] for x in xs),4)})
 for name in (f'E065_n10_results.jsonl',f'E065_n10_sample_{enc}.jsonl'):
  if enc=='pb' and name=='E065_n10_results.jsonl':continue
  if enc=='cnf' and name=='E065_n10_sample_pb.jsonl':continue
  path=root/name
  if path.exists():
   xs=[json.loads(s) for s in path.read_text().splitlines()]
   models.append({'model':enc,'n':10,'case':name,'total':len(xs),
                  'status_hist':dict(collections.Counter(x['status'] for x in xs)),
                  'seconds':round(sum(x['seconds'] for x in xs),4)})
rec=[]
for name in ('E065_n10_sample_cnf.jsonl','E065_n10_sample_pb.jsonl'):
 path=root/name
 xs=[json.loads(s) for s in path.read_text().splitlines()]
 rec.append({'file':name,'total':len(xs),'counts':dict(collections.Counter(x['status'] for x in xs)),
             'seconds':round(sum(x['seconds'] for x in xs),4)})
a={'experiment':'E065','problem':'3-MOLS(10)','status':'OPEN','normalization':'first-row identities in A/B/C plus A firstcolumn identity',
 'model_equivalence':'both encode FULL OA(n^2,5,n,2), no omission of ROW coordinate',
 'n10_base_cnf':{'variables':33000,'clauses':101740},
 'n10_full_pb':{'binary_choices':41338,'exactly_one_equations':1000},
 'order6_complete_firstcolumn_paratopy_classes':3,
 'order6_crosschecked':'CNF_Z3 and PB_Z3 both 3/3 UNSAT; independent C++ DLX 3/3 exhaustive =1203 nodes',
 'order10_16_cross_cycle_types':[{'engine':'CNF_Z3','status':'UNKNOWN 16/16','seconds':round(sum(json.loads(s)['seconds'] for s in (root/'E065_n10_sample_cnf.jsonl').read_text().splitlines()),3)},
                                 {'engine':'PB_Z3','status':'UNKNOWN 16/16','seconds':round(sum(json.loads(s)['seconds'] for s in (root/'E065_n10_sample_pb.jsonl').read_text().splitlines()),3)}],
 'global_10_branch_closed':0,'global_10_branches':1700,
 'notes':['No independently checked LRAT proof produced for order10','No 100/100/100 order10 witness','Z3 incremental uses same solver instance but measurable learned-clause reuse is not established','No credible numerical ETA'],
 'models':models,'sample':rec}
(root/'E065_SUMMARY.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps({'models':len(models),'status':a['status'],'order10_sample':rec}))