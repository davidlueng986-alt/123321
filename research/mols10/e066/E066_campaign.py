#!/usr/bin/env python3
"""CLOSED-only 3-MOLS(10) proof-carrying ALL-1700 branch campaign.

A correct standalone branch CNF is generated from E065 full 5-coordinate OA.
Only SAT independently validated against three 100/100/100 overlays, or UNSAT
with externally accepted LRAT proof retained on disk, may close a branch.
Every other solver return is UNKNOWN or ERROR. Never infer proof from a timeout.
"""
import argparse, collections, gzip, hashlib, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MOLS=ROOT.parent
E065=MOLS/'e065'
REPS=MOLS/'e064'/'E064_12_representatives.jsonl'
sys.path.insert(0,str(E065))
from E065_cnf import build as make_cnf
from E065_branch_dimacs import branch as make_branch
from E065_verify import from_solver_output, verify

COUNT=1700
SHARDS=17
BRANCHES_PER_SHARD=100

def digest(p):
    h=hashlib.sha256()
    with open(p,'rb') as fp:
        for block in iter(lambda:fp.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def reps():
    allreps=[json.loads(t) for t in REPS.read_text().splitlines() if t.strip()]
    assert len(allreps)==COUNT,len(allreps)
    assert len({(tuple(x['B_col0']),tuple(x['C_col0'])) for x in allreps})==COUNT
    for i,x in enumerate(allreps):
        a,b=x['B_col0'],x['C_col0']
        assert sorted(a)==list(range(10)) and sorted(b)==list(range(10))
        assert a[0]==b[0]==0
        assert all(10>r>0 and a[r]!=r and b[r]!=r and a[r]!=b[r] for r in range(1,10))
    return allreps

def cmd(args,timeout,output,slack=4):
    start=time.monotonic()
    with open(output,'w') as log:
        try:
            q=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,
                             check=False,timeout=timeout+slack)
            rc=q.returncode
        except subprocess.TimeoutExpired:
            rc=124
    return rc,round(time.monotonic()-start,3)

def read_lrat_verified(p):
    text=p.read_text(errors='replace')
    return re.search(r'(?m)^c\s+VERIFIED\s*$',text) is not None and 'NOT VERIFIED' not in text

def solve_branch(n,index,replist,base,tools,out,seconds,keep_cnf=False):
    """Do not trust SAT/UNSAT result without independent verification."""
    out.mkdir(parents=True,exist_ok=True)
    prefix=out/f'n{n}_b{index:04d}'
    cnf=prefix.with_suffix('.cnf')
    proof=prefix.with_suffix('.lrat')
    log=prefix.with_suffix('.solver.log')
    certlog=prefix.with_suffix('.checker.log')
    meta=make_branch(base,n,replist,index,cnf)
    cadical,check=tools
    rc,wall=cmd([cadical,'--lrat','--no-binary','--no-factor','-t',str(seconds),str(cnf),str(proof)],
                seconds,log,slack=8)
    result={'n':n,'branch':index,'status':'UNKNOWN',
            'solver_return_code':rc,'solver_seconds':wall,'base_sha256':digest(base),
            'branch_cnf_sha256':meta['sha256'],'B_col0':meta['B_col0'],'C_col0':meta['C_col0']}
    if rc==10:
        try:
            W=from_solver_output(log.read_text(errors='replace'),n)
            v=verify(W,n)
            assert W[0][0]==list(range(n))
            assert all(W[s][0]==list(range(n)) for s in range(3))
            assert [W[1][r][0] for r in range(n)]==meta['B_col0']
            assert [W[2][r][0] for r in range(n)]==meta['C_col0']
            witness={'status':'INDEPENDENT_FULL_WITNESS','n':n,'branch':index,'squares':W,'check':v,
                     'cnf_sha256':meta['sha256']}
            dst=prefix.with_suffix('.witness.json')
            dst.write_text(json.dumps(witness,indent=2)+'\n')
            result.update(status='SAT_WITNESS_VERIFIED',witness_file=dst.name,witness_sha256=digest(dst))
        except Exception as e:
            result.update(status='ERROR_SAT_VERIFICATION',error=str(e))
    elif rc==20:
        if not proof.exists() or proof.stat().st_size==0:
            result.update(status='ERROR_MISSING_UNSAT_PROOF')
        else:
            check_rc,check_t=cmd([check,str(cnf),str(proof)],max(60,seconds*10),certlog,slack=8)
            if check_rc==0 and read_lrat_verified(certlog):
                zpath=Path(str(proof)+'.gz')
                with proof.open('rb') as src,gzip.open(zpath,'wb',compresslevel=5) as dst:
                    shutil.copyfileobj(src,dst)
                result.update(status='UNSAT_LRAT_VERIFIED',
                              checker_return_code=check_rc,checker_seconds=check_t,
                              proof_file=zpath.name,proof_sha256=digest(zpath),
                              proof_raw_bytes=proof.stat().st_size)
            else:
                result.update(status='ERROR_LRAT_REJECTED',checker_return_code=check_rc,
                              checker_tail=certlog.read_text(errors='replace')[-1200:])
    elif rc in (0,124):
        result.update(status='UNKNOWN_BUDGET')
    else:
        result.update(status='ERROR_SOLVER_EXIT',solver_tail=log.read_text(errors='replace')[-1200:])
    if not result['status'].startswith('ERROR'):
        if proof.exists():proof.unlink()
        if not keep_cnf:cnf.unlink()
        if log.exists():log.unlink()
        if certlog.exists():certlog.unlink()
    return result

def calibrated_tools(args):
    assert Path(args.cadical).is_file() and os.access(args.cadical,os.X_OK)
    assert Path(args.lrat_check).is_file() and os.access(args.lrat_check,os.X_OK)
    return (str(Path(args.cadical).resolve()),str(Path(args.lrat_check).resolve()))

def calibration(args):
    tools=calibrated_tools(args)
    dir=Path(args.output).resolve();dir.mkdir(parents=True,exist_ok=True)
    # Order-5 first-column paratopy list, computed independently in E065.
    from E065_small_order_symmetry import group_orbits
    reps5,_,_=group_orbits(4)
    assert len(reps5)==2
    reps_file=dir/'order5_reps.jsonl'
    with reps_file.open('w') as f:
        for b,c in reps5:
            f.write(json.dumps({'B_col0':[0]+[x+1 for x in b],
                                'C_col0':[0]+[x+1 for x in c]})+'\n')
    base=dir/'n5_base.cnf';make_cnf(5,base)
    statuses=[]
    for i in range(2):
        res=solve_branch(5,i,reps_file,base,tools,dir,args.seconds,keep_cnf=True)
        statuses.append(res['status'])
        (dir/f'calibration_b{i}.json').write_text(json.dumps(res,indent=2)+'\n')
        print(json.dumps(res),flush=True)
    assert statuses==['UNSAT_LRAT_VERIFIED','SAT_WITNESS_VERIFIED'],statuses
    # A fake empty-clause proof must be rejected against the KNOWN SAT branch,
    # not against an UNSAT instance possibly already contradictory under unit propagation.
    bad=dir/'bogus.lrat';bad.write_text('1 0 0\n')
    chk=dir/'bogus.check.log'
    rc,_=cmd([tools[1],str(dir/'n5_b0001.cnf'),str(bad)],10,chk)
    assert rc!=0 or not read_lrat_verified(chk),'CRITICAL: fake UNSAT certificate accepted for known SAT CNF!'
    # A completely absent/truncated proof must fail even on the UNSAT instance.
    empty=dir/'empty.lrat';empty.write_text('')
    chk2=dir/'empty.check.log'
    rc2,_=cmd([tools[1],str(dir/'n5_b0000.cnf'),str(empty)],10,chk2)
    assert rc2!=0 or not read_lrat_verified(chk2),'CRITICAL: empty proof accepted!'
    print('PROOF_CHAIN_CALIBRATED',statuses,'SAT_FALSE_PROOF_REJECTED','EMPTY_PROOF_REJECTED',flush=True)

def sweep(args):
    assert 0<=args.shard<SHARDS
    allreps=reps()
    start=args.shard*BRANCHES_PER_SHARD
    stop=min(COUNT,start+BRANCHES_PER_SHARD)
    dest=Path(args.output).resolve();dest.mkdir(parents=True,exist_ok=True)
    tools=calibrated_tools(args)
    base=dest/'n10_base.cnf';make_cnf(10,base)
    ledger=dest/f'shard_{args.shard:02d}.jsonl'
    print('SHARD_START',json.dumps({'shard':args.shard,'start':start,'stop':stop,'base_sha256':digest(base)}),flush=True)
    with ledger.open('w',buffering=1) as f:
        for i in range(start,stop):
            result=solve_branch(10,i,REPS,base,tools,dest,args.seconds)
            f.write(json.dumps(result,separators=(',',':'))+'\n')
            print(json.dumps({'branch':i,'status':result['status'],'seconds':result['solver_seconds']}),flush=True)
            if result['status'].startswith('ERROR'):
                # Continue recording other branches; aggregate rejects unresolved/error.
                pass
    summary=collections.Counter(json.loads(x)['status'] for x in ledger.read_text().splitlines())
    (dest/f'shard_{args.shard:02d}_summary.json').write_text(json.dumps({'shard':args.shard,'start':start,'stop':stop,'counts':summary},indent=2)+'\n')
    assert sum(summary.values())==stop-start
    print('SHARD_FINISHED',args.shard,dict(summary),flush=True)

def aggregate(args):
    allreps=reps()
    root=Path(args.input).resolve();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    rec={};fail=[]
    inventory_file=ROOT/'E066_1700_BRANCH_INVENTORY.jsonl'
    if not inventory_file.exists():
        raise RuntimeError('Missing prevalidated 1700 branch SHA256 inventory; run E066_inventory.py')
    inventory=[json.loads(t) for t in inventory_file.read_text().splitlines() if t.strip()]
    assert len(inventory)==COUNT
    for shard in range(SHARDS):
        candidates=list(root.glob(f'**/shard_{shard:02d}.jsonl'))
        if len(candidates)!=1:
            fail.append({'shard':shard,'count':len(candidates)});continue
        for x in candidates[0].read_text().splitlines():
            q=json.loads(x);i=q['branch']
            if i in rec or i//BRANCHES_PER_SHARD!=shard:fail.append({'duplicate_or_wrong_shard':i});continue
            assert q['B_col0']==allreps[i]['B_col0'] and q['C_col0']==allreps[i]['C_col0']
            assert q['branch_cnf_sha256']==inventory[i]['branch_cnf_sha256'], 'Wrong branch CNF SHA256: '+str(i)
            if q['status']=='UNSAT_LRAT_VERIFIED':
                proof=list(root.glob(f'**/{q.get("proof_file", "NOT_ARCHIVED")}'))
                if len(proof)!=1 or digest(proof[0])!=q.get('proof_sha256'):
                    q['status']='ERROR_MISSING_OR_CORRUPT_UNSAT_PROOF'
                    fail.append({'proof_missing_or_corrupt':i})
            elif q['status']=='SAT_WITNESS_VERIFIED':
                witness=list(root.glob(f'**/{q.get("witness_file", "NOT_ARCHIVED")}'))
                if len(witness)!=1 or digest(witness[0])!=q.get('witness_sha256'):
                    q['status']='ERROR_MISSING_OR_CORRUPT_SAT_WITNESS'
                    fail.append({'witness_missing_or_corrupt':i})
                else:
                    w=json.loads(witness[0].read_text())
                    assert verify(w['squares'],10)['overlays']==[100,100,100]
                    assert w['branch']==i and w['cnf_sha256']==inventory[i]['branch_cnf_sha256']
            rec[i]=q
    missing=sorted(set(range(COUNT))-set(rec))
    if missing:fail.append({'missing':missing[:50],'missing_count':len(missing)})
    status=collections.Counter(q['status'] for q in rec.values())
    ledger=out/'E066_1700_RESULTS.jsonl'
    with ledger.open('w') as f:
        for i in range(COUNT):
            if i in rec:f.write(json.dumps(rec[i],separators=(',',':'))+'\n')
            else:f.write(json.dumps({'branch':i,'status':'NOT_RUN'},separators=(',',':'))+'\n')
    sat=[i for i in rec if rec[i]['status']=='SAT_WITNESS_VERIFIED']
    allunsat=len(rec)==COUNT and all(q['status']=='UNSAT_LRAT_VERIFIED' for q in rec.values())
    summary={'target':'3-MOLS(10)','status':'OPEN','branches_required':COUNT,'branches_with_records':len(rec),
             'complete_execution_coverage':not fail,'branch_statuses':dict(status),
             'missing_branches':missing,'errors':fail,'sat_witness_branch_ids':sat,
             'all_1700_verified_unsat':allunsat,'ledger_sha256':digest(ledger),
             'proof_policy':'Never treat timeout, solver UNSAT alone or unarchived LRAT as CLOSED.'}
    if sat:summary['status']='EXISTENCE_WITNESS_TO_INDEPENDENTLY_RECHECK'
    if allunsat:summary['status']='ALL_1700_PROOF_CHECKS_REPORTED__REQUIRE_GLOBAL_REPRODUCTION'
    (out/'E066_ALL_1700_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    (out/'E066_UNRESOLVED_INDEX.json').write_text(json.dumps(
        {'unresolved':[i for i in range(COUNT) if i not in rec or rec[i]['status'] not in ('SAT_WITNESS_VERIFIED','UNSAT_LRAT_VERIFIED')],
         'criterion':'Only independently checked SAT witness or archived verified LRAT closes a class'},
        indent=2)+'\n')
    print(json.dumps(summary),flush=True)
    if fail:sys.exit(2)

if __name__=='__main__':
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='mode',required=True)
    for name in ('calibrate','sweep'):
        sp=s.add_parser(name)
        sp.add_argument('--cadical',required=True)
        sp.add_argument('--lrat-check',required=True)
        sp.add_argument('--seconds',type=int,default=8)
        sp.add_argument('--output',required=True)
        if name=='sweep':sp.add_argument('--shard',type=int,required=True)
    sp=s.add_parser('aggregate');sp.add_argument('--input',required=True);sp.add_argument('--output',required=True)
    a=p.parse_args()
    if a.mode=='calibrate':calibration(a)
    elif a.mode=='sweep':sweep(a)
    else:aggregate(a)
