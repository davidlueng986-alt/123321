#!/usr/bin/env node
'use strict';
// Independent integer-only E041 certificate checker. No solver dependencies.
const fs=require('fs'),assert=require('assert');
const z=JSON.parse(fs.readFileSync(process.argv[2]||'E041_NEW_22_SPARSE_CERTIFICATE.json','utf8'));
const P=z.source_prefix,core=new Set(z.forced_cell_indices);
const K=k=>k.join(':');
const W=new Map(z.weights.map(([k,v])=>[K(k),v]));
const R=(c,a,b,d)=>[['P',0,a,b],['P',1,a,d],['P',2,b,d],['C',0,c,a],['C',1,c,b],['C',2,c,d]];
const score=(c,a,b,d)=>R(c,a,b,d).reduce((s,k)=>s+(W.get(K(k))||0),0);
assert(P.length===3&&P.every(Q=>Q.length===4));
for(const Q of P){
 for(const row of Q)assert(row.length===10&&new Set(row).size===10&&row.every(v=>Number.isInteger(v)&&v>=0&&v<10));
 for(let c=0;c<10;c++)assert(new Set(Q.map(row=>row[c])).size===4);
}
for(const [s,t] of [[0,1],[0,2],[1,2]]){
 let pairs=new Set();for(let r=0;r<4;r++)for(let c=0;c<10;c++)pairs.add(P[s][r][c]+':'+P[t][r][c]);
 assert(pairs.size===40);
}
assert(core.size===22&&z.core_size===22&&[...core].every(j=>j>=0&&j<40));
assert(W.size===7&&z.weights.every(([k,v])=>Number.isInteger(v)&&Math.abs(v)===1));
const F=Array.from({length:40},(_,j)=>{const r=Math.floor(j/10),c=j%10;return [r,c,P[0][r][c],P[1][r][c],P[2][r][c]]});
const conflicts=(c,a,b,d)=>[...core].filter(j=>{
 const [r,cc,x,y,v]=F[j];
 return (cc===c&&(a===x||b===y||d===v))||(a===x&&b===y)||(a===x&&d===v)||(b===y&&d===v);
});
const used=new Set();
for(const j of core){
 const [r,c,a,b,d]=F[j];
 for(const k of R(c,a,b,d)){assert(!used.has(K(k)));used.add(K(k));}
}
let rhs=0;for(const [k,v] of W)if(!used.has(k))rhs+=v;
assert(rhs===z.rhs&&rhs>0);
let pos=0,remaining=0,max=-Infinity;const forced=new Map();
for(let c=0;c<10;c++)for(let a=0;a<10;a++)for(let b=0;b<10;b++)for(let d=0;d<10;d++){
 const w=score(c,a,b,d),hit=conflicts(c,a,b,d);
 if(w>0){pos++;assert(hit.length>0);if(hit.length===1&&!forced.has(hit[0]))forced.set(hit[0],[c,a,b,d,w]);}
 if(R(c,a,b,d).every(k=>!used.has(K(k)))){remaining++;assert(w<=0);max=Math.max(max,w);}
}
assert(pos===z.positive_candidate_count&&remaining===z.residual_candidate_count&&max===z.max_candidate_weight);
assert(forced.size===core.size&&[...core].every(j=>forced.has(j)));
assert(z.singleton_witnesses.length===core.size);
for(const [j,c,a,b,d,w] of z.singleton_witnesses){
 assert(core.has(j)&&score(c,a,b,d)===w&&w>0);
 assert.deepStrictEqual(conflicts(c,a,b,d),[j]);
}
// Mutation test: a corrupted +10 weight must create an allowed positive placement.
const altered=JSON.parse(JSON.stringify(z));altered.weights[0][1]+=10;
const AW=new Map(altered.weights.map(([k,v])=>[K(k),v]));
let rejected=false;
for(let c=0;c<10&&!rejected;c++)for(let a=0;a<10&&!rejected;a++)for(let b=0;b<10&&!rejected;b++)for(let d=0;d<10;d++){
 if(R(c,a,b,d).every(k=>!used.has(K(k)))){
  const w=R(c,a,b,d).reduce((s,k)=>s+(AW.get(K(k))||0),0);
  if(w>0){rejected=true;break;}
 }
}
assert(rejected,'corrupt dual not rejected');
console.log(JSON.stringify({status:'INDEPENDENT_EXACT_PASS',scope:'FIXED_22_CELL_PATTERN',core:core.size,dual_support:W.size,rhs,positive_candidates:pos,remaining_candidates:remaining,max_candidate_weight:max,singleton_witnesses:forced.size,mutation_rejected:rejected,global_status:'OPEN'}));
