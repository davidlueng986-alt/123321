"""E042 exact four-row isotopy embedding benchmark; standard library only.
Inputs: E037_ALL_CYCLES.json, E036_WITNESSES.json,
E040_EXACT_MINIMAL_CORES.json, E041_NEW_22_SPARSE_CERTIFICATE.json.
Run: python E042_replay.py 0 100; repeat with 100 100, 200 100,
300 100, 400 116. All input files in E042 reproducibility bundle.
"""
import itertools,json,time,collections,sys
from pathlib import Path
D=Path(__file__).parent
read=lambda f:json.loads((D/f).read_text())
cores=[{'name':'E040_21' if i==0 else 'E040_22','P':z['source_prefix'],'cells':z['forced_cell_indices']} for i,z in enumerate(read('E040_EXACT_MINIMAL_CORES.json')['results'][:2])]
z=read('E041_NEW_22_SPARSE_CERTIFICATE.json')
cores.append({'name':'E041_22','P':z['source_prefix'],'cells':z['forced_cell_indices']})

def embed(src,target,rp,sp):
    P=src['P'];groups={c:[] for c in range(10)}
    for j in src['cells']:groups[j%10].append(j//10)
    remaining=tuple(c for c in groups if groups[c])
    maps=[{} for _ in range(3)];backs=[{} for _ in range(3)]
    used=set();nodes=0
    def choices(c,d):
        if d in used:return None
        changes=[];tmp={};rev={}
        for r in groups[c]:
            for s in range(3):
                a=P[s][r][c];b=target[sp[s]][rp[r]][d]
                if maps[s].get(a,b)!=b or backs[s].get(b,a)!=a:return None
                if tmp.get((s,a),b)!=b or rev.get((s,b),a)!=a:return None
                if a not in maps[s] and (s,a) not in tmp:
                    tmp[s,a]=b;rev[s,b]=a;changes.append((s,a,b))
        return changes
    def dfs(cols):
        nonlocal nodes
        nodes+=1
        if not cols:return True
        best=None;options=None
        for c in cols:
            opt=[(d,t) for d in range(10) if (t:=choices(c,d)) is not None]
            if not opt:return False
            if options is None or (len(opt),-len(groups[c]))<(len(options),-len(groups[best])):
                best,options=c,opt
        for d,changes in options:
            used.add(d)
            for s,a,b in changes:maps[s][a]=b;backs[s][b]=a
            yes=dfs(tuple(c for c in cols if c!=best))
            for s,a,b in changes:del maps[s][a];del backs[s][b]
            used.remove(d)
            if yes:return True
        return False
    return dfs(remaining),nodes

def match(core,P):
    nodes=0
    for rp in itertools.permutations(range(4)):
        for sp in itertools.permutations(range(3)):
            yes,n=embed(core,P,rp,sp);nodes+=n
            if yes:return True,nodes
    return False,nodes

def main():
    prefixes=[x['prefix'] for c in read('E037_ALL_CYCLES.json')['cycle_results'] for x in c['results']]
    prefixes += [[sq[:4] for sq in w] for w in read('E036_WITNESSES.json')]
    assert len(prefixes)==516
    offset=int(sys.argv[1]) if len(sys.argv)>1 else 0
    limit=int(sys.argv[2]) if len(sys.argv)>2 else 100
    t=time.monotonic();hits=[];counts=collections.Counter();total_nodes=0
    for i,P in enumerate(prefixes[offset:offset+limit],start=offset):
        for core in cores:
            yes,n=match(core,P);total_nodes+=n;counts[core['name']]+=int(yes)
            if yes:hits.append([i,core['name']])
    for core in cores:assert match(core,core['P'])[0]
    result={'prefixes':len(prefixes),'sampled':len(prefixes[offset:offset+limit]),'checks':len(prefixes[offset:offset+limit])*len(cores),'matches':hits,'counts':dict(counts),'total_nodes':total_nodes,'seconds':round(time.monotonic()-t,3)}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
