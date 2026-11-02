#!/usr/bin/env node
"use strict";
// Independent integer-only replay. Does NOT import Python model or LP solver.
const fs=require("fs"),assert=require("assert");
const scans=JSON.parse(fs.readFileSync("E045_GUIDED_RESULTS.json","utf8"));
const certs=JSON.parse(fs.readFileSync("E045_CERTIFICATES.json","utf8"));
const N=10;
function resources(c,a,b,d){return [10*a+b,100+10*a+d,200+10*b+d,300+10*c+a,400+10*c+b,500+10*c+d];}
function demandId(e){return e[0]==="P"?100*e[1]+10*e[2]+e[3]:300+100*e[1]+10*e[2]+e[3];}
function verifyPrefix(S){
 assert(S.length===3&&S.every(s=>s.length===4));
 const used=new Set();
 for(let s=0;s<3;s++){
  for(let r=0;r<4;r++)assert(S[s][r].length===10&&new Set(S[s][r]).size===10&&S[s][r].every(v=>Number.isInteger(v)&&v>=0&&v<10));
  for(let c=0;c<10;c++)assert(new Set(S[s].map(row=>row[c])).size===4);
 }
 for(let r=0;r<4;r++)for(let c=0;c<10;c++){
  const a=S[0][r][c],b=S[1][r][c],d=S[2][r][c];
  for(const e of resources(c,a,b,d)){assert(!used.has(e),"repeated resource");used.add(e);}
 }
 assert(used.size===240);
 return used;
}
function checkOne(rec,cert){
 const used=verifyPrefix(rec.prefix),un=[];
 for(let e=0;e<600;e++)if(!used.has(e))un.push(e);
 assert(un.length===360);
 const idx=new Map(un.map((e,i)=>[e,i]));
 let weight=null;
 if(cert.kind==="DUAL"){
  weight=new Array(un.length).fill(-1);
  for(const [i,delta] of cert.delta){assert(Number.isInteger(i)&&i>=0&&i<360&&Number.isInteger(delta));weight[i]+=delta;}
  assert(weight.reduce((a,b)=>a+b,0)===cert.sum&&cert.sum>0);
 }
 let count=0,max=-Infinity,zeroCount=0;
 const target=cert.kind==="ZERO"?demandId(cert.demand):null;
 if(target!==null)assert(idx.has(target));
 for(let c=0;c<10;c++)for(let a=0;a<10;a++)for(let b=0;b<10;b++)for(let d=0;d<10;d++){
  const R=resources(c,a,b,d);
  if(R.some(e=>used.has(e)))continue;
  count++;
  if(cert.kind==="DUAL"){
   const v=R.reduce((sum,e)=>sum+weight[idx.get(e)],0);
   if(v>max)max=v;
   assert(v<=0,"dual inequality violated");
  }else if(R.includes(target))zeroCount++;
 }
 if(cert.kind==="DUAL")assert(max===cert.max&&max<=0);
 else assert(cert.kind==="ZERO"&&zeroCount===0);
 return count;
}
assert(scans.cases.length===574&&certs.certificates.length===574&&certs.failed.length===0);
const digests=new Set();let dual=0,zero=0,total=0;
for(let i=0;i<574;i++){
 const rec=scans.cases[i],cert=certs.certificates[i];assert(cert.index===i);
 assert(!digests.has(rec.sha256));digests.add(rec.sha256);
 total+=checkOne(rec,cert);
 if(cert.kind==="DUAL")dual++;else zero++;
}
assert(dual===544&&zero===30);
const first=certs.certificates.find(c=>c.kind==="DUAL");
const mutation=JSON.parse(JSON.stringify(first));
const r=scans.cases[mutation.index],used=verifyPrefix(r.prefix);
let victim=-1;
for(let c=0;c<10&&victim<0;c++)for(let a=0;a<10&&victim<0;a++)for(let b=0;b<10&&victim<0;b++)for(let d=0;d<10&&victim<0;d++){
 const es=resources(c,a,b,d);if(es.some(e=>used.has(e)))continue;
 const un=[...Array(600).keys()].filter(e=>!used.has(e));victim=un.indexOf(es[0]);
}
assert(victim>=0);mutation.delta.push([victim,1000000]);mutation.sum+=1000000;
let rejected=false;try{checkOne(r,mutation);}catch(e){rejected=true;}
assert(rejected,"mutation was not rejected");
console.log(JSON.stringify({verified:574,dual,zero,total_candidates:total,distinct:digests.size,mutation_rejected:rejected,status:"PASS"},null,2));
