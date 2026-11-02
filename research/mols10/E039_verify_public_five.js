#!/usr/bin/env node
"use strict";
// Independent exact integer replay of E039's public five-demand Farkas obstruction.
// Proves ONLY that the attached fixed four-row prefix cannot be extended.
const fs=require("fs");
const Z=JSON.parse(fs.readFileSync(process.argv[2]||"E039_PUBLIC_FIVE_DEMAND.json","utf8"));
const assert=(p,m)=>{if(!p)throw Error(m)};
function replay(z){
 const S=z.prefix,n=10,k=4,P=[[0,1],[0,2],[1,2]];
 const full=Array.from({length:n},(_,i)=>i).join(",");
 assert(S.length===3,"three squares");
 for(const A of S){
  assert(A.length===k,"four rows");
  for(const row of A)assert([...row].sort((a,b)=>a-b).join(",")===full,"row Latin");
  for(let c=0;c<n;c++)assert(new Set(A.map(row=>row[c])).size===k,"column Latin");
 }
 const used=P.map(([i,j])=>new Set(S[i].flatMap((row,r)=>row.map((v,c)=>v+":"+S[j][r][c]))));
 for(const set of used)assert(set.size===40,"pair overlay 40");
 const key=d=>d.join(":");
 const W=new Map();let sum=0;
 for(const [d,v] of z.weights){
  assert(Number.isSafeInteger(v)&&v!==0&&!W.has(key(d)),"weight");
  assert(z.classes.some(cl=>key(cl)===key(d.slice(0,2))),"class");
  W.set(key(d),v);sum+=v;
 }
 assert(sum>0&&sum===z.weight_sum,"positive Farkas sum");
 let count=0,max=-Infinity;
 for(let c=0;c<n;c++){
  const allowed=[0,1,2].map(s=>Array.from({length:n},(_,x)=>x).filter(v=>!S[s].some(row=>row[c]===v)));
  for(const a of allowed[0])for(const b of allowed[1])for(const d of allowed[2]){
   if(used[0].has(a+":"+b)||used[1].has(a+":"+d)||used[2].has(b+":"+d))continue;
   const resources=[["P",0,a,b],["P",1,a,d],["P",2,b,d],["C",0,c,a],["C",1,c,b],["C",2,c,d]];
   const value=resources.reduce((v,x)=>v+(W.get(key(x))||0),0);
   assert(value<=0,"Farkas inequality violated at "+[c,a,b,d]);
   if(value>max)max=value;
   count++;
  }
 }
 assert(count===z.candidate_count&&max===z.max_candidate_weight,"candidate count or max");
 return {status:"EXACT_FIVE_DEMAND_PASS",candidates:count,weight_sum:sum,nonzero:W.size,scope:"FIXED_PREFIX_ONLY"};
}
const result=replay(Z);
const bad=JSON.parse(JSON.stringify(Z));bad.weights[0][1]=1000000;
let rejected=false;try{replay(bad)}catch(e){rejected=true}
assert(rejected,"mutation must be rejected");
console.log(JSON.stringify({...result,mutation_rejected:true,global_status:"OPEN"}));
