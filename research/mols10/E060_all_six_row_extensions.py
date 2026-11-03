#!/usr/bin/env python3
"""Exhaustive all 84 six-row subsets of Jäger et al Figure3 triple.
For each fixed six-row prefix enumerate every compatible seventh triple row via
FULL candidate cross-product (numpy vectorization), then exhaustively extend
any seventh-row candidate to ten rows using E060_seven_row_completion.solve.
Scope is fixed 84 anchors only (one published 9x10 triple), not global.
"""
import json,itertools,time,numpy as np
from pathlib import Path
from E060_seven_row_completion import latin_rows,solve,check_full
SOURCE=str(Path(__file__).with_name('E059_2024_9x10_analysed.json')))

def gen_seventh(W):
  S=[np.asarray(latin_rows(Q),dtype=np.uint8) for Q in W]
  compat=[]
  for a,b in ((0,1),(0,2),(1,2)):
    used=np.zeros((10,10),dtype=bool)
    for r in range(6):
      for c in range(10):used[W[a][r][c],W[b][r][c]]=True
    good=np.ones((len(S[a]),len(S[b])),dtype=bool)
    for c in range(10):good &= ~used[S[a][:,c,None],S[b][None,:,c]]
    compat.append(good)
  triples=[]
  for ia,ib in zip(*np.nonzero(compat[0])):
    for ic in np.nonzero(compat[1][ia]&compat[2][ib])[0]:
      triples.append(tuple(tuple(int(v) for v in S[s][idx]) for s,idx in enumerate((ia,ib,ic))))
  return triples,[int(x.sum()) for x in compat],list(map(len,S))

def run():
  source=json.load(open(SOURCE))['published_9x10_rectangles']; t0=time.monotonic()
  out=[];status='UNSAT_FIXED_84_SIX_ROW_ANCHORS'
  for omitted in itertools.combinations(range(9),3):
    W=[[tuple(row) for i,row in enumerate(Q) if i not in omitted] for Q in source]
    newrows,pairs,opts=gen_seventh(W)
    report={'omitted':list(omitted),'seventh_row_triples':len(newrows),'pair_candidates':pairs,'seventh_row_options_per_square':opts,'finished':0,'unknown':0}
    for new in newrows:
      W7=[W[s]+[new[s]] for s in range(3)]
      faux=[Q+[Q[0],Q[0]] for Q in W7]
      rr=solve(faux,(7,8),wall_seconds) if False else solve(faux,(7,8),5.0)
      report['finished']+=1
      if rr['status']=='SAT':
        check_full(rr['witness']);report['status']='SAT';report['witness']=rr['witness'];status='SAT';break
      if rr['status']!='UNSAT_FIXED_SEVEN_ROWS':report['unknown']+=1
    report['status']=report.get('status') or ('UNKNOWN' if report['unknown'] else 'UNSAT_FIXED_SIX_ROWS')
    out.append(report)
    print(json.dumps({k:v for k,v in report.items() if k!='witness'}),flush=True)
    if status=='SAT':break
  result={'status':status if not sum(z['unknown'] for z in out) else 'UNKNOWN_PARTIAL',
          'source':'Jäger et al 2024 Figure3, original 9x10 partial triple',
          'scope':'84 anchored 6row restrictions only, not all global possibilities',
          'anchors':len(out),'total_seventh_row_triples':sum(x['seventh_row_triples'] for x in out),
          'complete_unsets':sum(x['status']=='UNSAT_FIXED_SIX_ROWS' for x in out),
          'unknown':sum(x['unknown'] for x in out),'seconds':round(time.monotonic()-t0,4),'results':out}
  json.dump(result,open(Path(__file__).with_name('E060_ALL_84_SIX_ROW_RESULTS.json'),'w'),indent=2)
  print('SUMMARY',json.dumps({k:v for k,v in result.items() if k!='results'}),flush=True)
if __name__=='__main__':run()