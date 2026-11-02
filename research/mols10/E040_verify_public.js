#!/usr/bin/env node
'use strict';
// Standalone integer-only proof checker for E040 partial forbidden patterns.
// No third-party packages, no reliance on scipy or a SAT/LP solver.
const fs=require('fs'),assert=require('assert');
const Z=JSON.parse(fs.readFileSync(process.argv[2]||'E040_EXACT_MINIMAL_CORES.json','utf8'));
const key=x=>x.join(':');
const resources=(c,a,b,d)=>[['P',0,a,b],['P',1,a,d],['P',2,b,d],['C',0,c,a],['C',1,c,b],['C',2,c,d]];
let results=[];
for(const z of Z.results){
 const P=z.source_prefix, W=new Map(z.weights.map(([k,v])=>[key(k),v]));
 assert(P.length===3 && P.every(A=>A.length===4));
 for(const A of P){for(const row of A)assert(row.length===10&&new Set(row).size===10&&row.every(x=>x>=0&&x<10));
  for(let c=0;c<10;c++)assert(new Set(A.map(row=>row[c])).size===4)}
 for(const [s,t] of [[0,1],[0,2],[1,2]]){
  let used=new Set();for(let r=0;r<4;r++)for(let c=0;c<10;c++)used.add(P[s][r][c]+':'+P[t][r][c]);assert(used.size===40)}
 const F=Array.from({length:40},(_,j)=>{let r=Math.floor(j/10),c=j%10;return [r,c,P[0][r][c],P[1][r][c],P[2][r][c]]});
 const core=new Set(z.forced_cell_indices);assert(core.size===z.core_size);
 const score=(c,a,b,d)=>resources(c,a,b,d).reduce((s,k)=>s+(W.get(key(k))||0),0);
 const conflicts=(c,a,b,d)=>F.flatMap(([r,cc,x,y,v],j)=>
   ((cc===c&&(a===x||b===y||d===v))||(a===x&&b===y)||(a===x&&d===v)||(b===y&&d===v))?[j]:[]);
 let pos=0,forced=new Map();
 for(let c=0;c<10;c++)for(let a=0;a<10;a++)for(let b=0;b<10;b++)for(let d=0;d<10;d++){
  const w=score(c,a,b,d);if(w<=0)continue;pos++;
  const hit=conflicts(c,a,b,d);assert(hit.length>0 && hit.some(j=>core.has(j)));
  if(hit.length===1&&!forced.has(hit[0]))forced.set(hit[0],[c,a,b,d,w]);
 }
 assert(pos===z.positive_candidate_count);
 assert(forced.size===core.size && [...core].every(j=>forced.has(j)));
 for(const [j,c,a,b,d,w] of z.forcing_witnesses){
  assert(core.has(j));assert(score(c,a,b,d)===w&&w>0);
  assert.deepStrictEqual(conflicts(c,a,b,d),[j]);
 }
 assert(z.forcing_witnesses.length===core.size);
 const usedP=[new Set(),new Set(),new Set()],usedC=Array.from({length:3},()=>Array.from({length:10},()=>new Set()));
 for(const j of core){let [r,c,a,b,d]=F[j];usedP[0].add(a+':'+b);usedP[1].add(a+':'+d);usedP[2].add(b+':'+d);
  usedC[0][c].add(a);usedC[1][c].add(b);usedC[2][c].add(d)}
 const used=new Set();for(let p=0;p<3;p++)for(let v of usedP[p])used.add('P:'+p+':'+v);
 for(let s=0;s<3;s++)for(let c=0;c<10;c++)for(let v of usedC[s][c])used.add(key(['C',s,c,v]));
 let rhs=0;for(const [k,v] of W)if(!used.has(k))rhs+=v;assert(rhs===z.rhs&&rhs>0);
 let n=0,max=-Infinity;
 for(let c=0;c<10;c++)for(let a=0;a<10;a++)for(let b=0;b<10;b++)for(let d=0;d<10;d++){
  if(usedC[0][c].has(a)||usedC[1][c].has(b)||usedC[2][c].has(d))continue;
  if(usedP[0].has(a+':'+b)||usedP[1].has(a+':'+d)||usedP[2].has(b+':'+d))continue;
  let w=score(c,a,b,d);assert(w<=0);n++;max=Math.max(max,w);
 }
 assert(n===z.residual_candidate_count&&max===z.max_candidate_weight);
 results.push({motif:z.motif_index,core_cells:core.size,positive_candidates:pos,forced_witnesses:forced.size,residual_candidates:n,rhs,max});
}
const corrupted=JSON.parse(JSON.stringify(Z));corrupted.results[0].forcing_witnesses[0][2]=99;
let rejected=false;try{
 const [j,c,a,b,d,w]=corrupted.results[0].forcing_witnesses[0];
 const W=new Map(corrupted.results[0].weights.map(([k,v])=>[key(k),v]));
 assert(resources(c,a,b,d).reduce((s,k)=>s+(W.get(key(k))||0),0)===w);
}catch(e){rejected=true}assert(rejected);
console.log(JSON.stringify({status:'INDEPENDENT_EXACT_PASS',global_status:'OPEN',results,mutation_rejected:true}));
