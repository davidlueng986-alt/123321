// E056: exact branch-and-bound gauge optimizer; node >=18; reads E051_CERTIFICATES.json and E054_RESULTS.json.
// The first five class offsets may be restricted to supported coefficient values:
// if >=2 classes have zero matches, adjust one to a supported value and the other to maintain zero sum.
// Thus an optimum has at most one unsupported offset, which is the balancing sixth class.
const fs=require('fs');
const data=JSON.parse(fs.readFileSync(process.argv[2]||'E051_CERTIFICATES.json'));
const prior=JSON.parse(fs.readFileSync(process.argv[3]||'E054_RESULTS.json')).results;
let output=[];
data.results.filter(x=>x.kind==='integer_farkas').forEach((r,idx)=>{
 const f=Array.from({length:6},()=>new Map());
 for(const [d,v] of r.nonzero){const k=d[0]==='c'?d[1]:3+d[1];f[k].set(v,(f[k].get(v)||0)+1)}
 const order=[0,1,2,3,4,5].sort((a,b)=>Math.max(...f[b].values())-Math.max(...f[a].values())||f[a].size-f[b].size);
 const suffix=Array(7).fill(0);
 for(let k=5;k>=0;k--)suffix[k]=suffix[k+1]+Math.max(...f[order[k]].values());
 let best=360-prior[idx].new_nonzero, offsets=prior[idx].offsets.slice(),nodes=0,prunes=0;
 function dfs(k,sum,score,chosen){
   nodes++;
   if(k===5){const v=-sum,tot=score+(f[order[5]].get(v)||0);if(tot>best){best=tot;offsets=Array(6).fill(0);[...chosen,v].forEach((x,j)=>offsets[order[j]]=x)}return}
   if(score+suffix[k]<=best){prunes++;return}
   for(const [v,count] of [...f[order[k]]].sort((a,b)=>b[1]-a[1])){
      if(score+count+suffix[k+1]<=best){prunes++;continue}
      dfs(k+1,sum+v,score+count,[...chosen,v])
   }
 }
 dfs(0,0,0,[]);
 if(offsets.reduce((a,b)=>a+b,0)!==0||f.reduce((a,m,j)=>a+(m.get(offsets[j])||0),0)!==best)throw Error('invalid result');
 output.push({index:idx,optimal_nonzero:360-best,offsets,nodes,prunes});
});
console.log(JSON.stringify({experiment:'E056 exact optimal gauge within zero-sum class offsets',results:output},null,2));
