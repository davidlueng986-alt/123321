#!/usr/bin/env node
// Independent sparse motif verifier: independently enumerate candidate cells and check inequalities.
const fs=require('fs');
const P=[[0,1],[0,2],[1,2]];
const motifs=JSON.parse(fs.readFileSync(__dirname+'/E038_PUBLIC_12_CERTIFICATES.json','utf8')).witnesses;
function assert(b,msg){if(!b)throw Error(msg)}
function verify(m){
 const S=m.prefix,n=10,k=4,used=P.map(([s,t])=>new Set(S[s].flatMap((row,r)=>row.map((v,col)=>v+':'+S[t][r][col]))));
 for(let s=0;s<3;s++){
  assert(S[s].length===k,'row count');
  for(const row of S[s])assert(new Set(row).size===n,'row Latin');
  for(let col=0;col<n;col++)assert(new Set(S[s].map(row=>row[col])).size===k,'column Latin');
 }
 assert(used.every(x=>x.size===k*n),'orthogonality');
 const w=new Map();let total=0;
 for(const [key,val] of m.weights){const v=key.join(':');assert(!w.has(v)&&Number.isInteger(val)&&val!==0,'duplicate/invalid weight');w.set(v,val);total+=val;}
 assert(total===m.weight_sum&&total>0&&w.size===m.support,'positive sum');
 let cand=0, max=-Infinity;
 for(let col=0;col<n;col++){
  const A=[0,1,2].map(s=>Array.from({length:n},(_,i)=>i).filter(v=>!S[s].some(row=>row[col]===v)));
  for(const a of A[0])for(const b of A[1])for(const z of A[2]){
   if(used[0].has(a+':'+b)||used[1].has(a+':'+z)||used[2].has(b+':'+z))continue;
   cand++;
   const d=[['P',0,a,b],['P',1,a,z],['P',2,b,z],['C',0,col,a],['C',1,col,b],['C',2,col,z]];
   const score=d.reduce((sum,key)=>sum+(w.get(key.join(':'))||0),0);
   max=Math.max(max,score);assert(score<=0,'sparse dual violated');
  }
 }
 return {cycle:m.cycle,support:m.support,positive_sum:total,candidates:cand,max};
}
assert(motifs.length===12,'12 cycle types');
const results=motifs.map(verify);
const mutated=JSON.parse(JSON.stringify(motifs[0]));mutated.weight_sum+=1;
let rejects=false;try{verify(mutated)}catch(e){rejects=true}assert(rejects,'corrupted sparse witness accepted');
console.log(JSON.stringify({status:'PASS',types:results.length,supports:results.map(x=>x.support),all_positive_sums:results.every(x=>x.positive_sum>0),mutation_rejected:rejects,scope:'12 FIXED 4-row prefixes only'}));