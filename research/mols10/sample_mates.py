"""Sample orthogonal mates B of one fixed Latin square A.

Uses randomized exact-cover search on all single-A transversals, then
independently checks each pair and its joint A/B transversals.
Heuristic sample, NOT an exhaustive search of 3-MOLS(10).
"""
import argparse, hashlib, json, random
from pathlib import Path
from exact_cover import exact_cover
from verify import analyze

def transversals_single(a):
    n=len(a)
    out=[];path=[]
    def rec(i,cols,vals):
        if i==n:
            out.append(tuple(path));return
        for j in range(n):
            cb=1<<j;ab=1<<a[i][j]
            if cols&cb or vals&ab: continue
            path.append(j);rec(i+1,cols|cb,vals|ab);path.pop()
    rec(0,0,0)
    return out

def transversals_pair(a,b):
    n=len(a)
    out=[];path=[];support=[0]*(n*n)
    def rec(i,cols,av,bv):
        if i==n:
            out.append(tuple(path))
            for row,j in enumerate(path):support[row*n+j]+=1
            return
        for j in range(n):
            cb=1<<j;ab=1<<a[i][j];bb=1<<b[i][j]
            if cols&cb or av&ab or bv&bb: continue
            path.append(j);rec(i+1,cols|cb,av|ab,bv|bb);path.pop()
    rec(0,0,0,0)
    return out,support

def make_mate(a,trans,seed,*,node_budget=100000,second_budget=2.0):
    perm=list(trans);random.Random(seed).shuffle(perm)
    result=exact_cover(perm,len(a),max_nodes=node_budget,max_seconds=second_budget)
    if result["status"]!="SAT_EXACT": return None,result
    n=len(a); b=[[-1]*n for _ in range(n)]
    for symbol,k in enumerate(result["indices"]):
        for i,j in enumerate(perm[k]):b[i][j]=symbol
    assert analyze([a,b],n)[0]["orthogonal"]
    symbols={value:j for j,value in enumerate(b[0])}
    return [[symbols[x] for x in row] for row in b],result

def main():
    pa=argparse.ArgumentParser()
    pa.add_argument("--input",default="near_triple.json")
    pa.add_argument("--square-index",type=int,default=0)
    pa.add_argument("--samples",type=int,default=40)
    pa.add_argument("--seed-start",type=int,default=0)
    pa.add_argument("--output",default="sampling_report.json")
    args=pa.parse_args()
    a=json.loads(Path(args.input).read_text())["squares"][args.square_index]
    t=transversals_single(a)
    seen={};results=[]
    for seed in range(args.seed_start,args.seed_start+args.samples):
        b,res=make_mate(a,t,seed)
        if b is None:
            results.append({"seed":seed,"status":res["status"],"nodes":res["nodes"]})
            continue
        digest=hashlib.sha256(json.dumps(b,separators=(",",":")).encode()).hexdigest()
        if digest in seen: continue
        seen[digest]=seed
        trans,support=transversals_pair(a,b)
        row={"seed":seed,"digest":digest,"mate":b,"solver_nodes":res["nodes"],
             "transversals":len(trans),"unsupported_cells":sum(v==0 for v in support)}
        if len(trans)>=len(a) and all(support):
            candidate=exact_cover(trans,len(a),max_nodes=100000,max_seconds=3.0)
            row["extension_attempt"]={k:v for k,v in candidate.items() if k!="indices"}
            if candidate["status"]=="SAT_EXACT":
                c=[[-1]*len(a) for _ in range(len(a))]
                for symbol,idx in enumerate(candidate["indices"]):
                    for i,j in enumerate(trans[idx]): c[i][j]=symbol
                assert all(q["orthogonal"] for q in analyze([a,b,c],len(a)))
                row["full_three_mols_witness"]=[a,b,c]
                results.append(row)
                break
        results.append(row)
    report={"input":args.input,"square_index":args.square_index,
            "samples_requested":args.samples,"single_square_transversals":len(t),
            "unique_mates":len(seen),"results":results}
    Path(args.output).write_text(json.dumps(report,indent=2)+"\n")
    compact=[(r["transversals"],r["unsupported_cells"])
             for r in results if "mate" in r]
    print("SAMPLED",args.samples,"UNIQUE",len(seen),"SINGLE TRANS",len(t),
          "MAX",max([x[0] for x in compact] or [0]),
          "MIN_UNSUPPORTED",min([x[1] for x in compact] or [len(a)**2]),
          "QUALIFIED",sum(x[0]>=len(a) and x[1]==0 for x in compact))

if __name__=="__main__":main()
