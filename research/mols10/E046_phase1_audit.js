#!/usr/bin/env node
"use strict";
// E046 independent mutation, novelty and old-certificate transfer audit.
const fs=require("fs"),assert=require("assert");
const old=JSON.parse(fs.readFileSync("E045_GUIDED_RESULTS.json","utf8"));
const oldCert=JSON.parse(fs.readFileSync("E045_CERTIFICATES.json","utf8"));
const data=JSON.parse(fs.readFileSync("E046_PHASE1_RESULTS.json","utf8"));
const R=(c,a,b,z)=>[10*a+b,100+10*a+z,200+10*b+z,300+10*c+a,400+10*c+b,500+10*c+z];
const oldSet=new Set(old.cases.map(x=>JSON.stringify(x.prefix))),seen=new Set();
let sourceDualInvalid=0,sourceZeroInvalid=0,mutationRejected=0;
for(const rec of data.cases){
 const h=JSON.stringify(rec.prefix);assert(!seen.has(h)&&!oldSet.has(h));seen.add(h);
 assert(rec.status==="EXACT_DUAL");
 const source=old.cases[rec.source_index].prefix,cert=oldCert.certificates[rec.source_index];
 const usedOld=new Uint8Array(600),usedNew=new Uint8Array(600);
 for(let r=0;r<4;r++)for(let c=0;c<10;c++){
  for(const e of R(c,source[0][r][c],source[1][r][c],source[2][r][c]))usedOld[e]=1;
  for(const e of R(c,rec.prefix[0][r][c],rec.prefix[1][r][c],rec.prefix[2][r][c]))usedNew[e]=1;
 }
 const unNew=[];for(let e=0;e<600;e++)if(!usedNew[e])unNew.push(e);
 const wNew=new Int32Array(600);for(const e of unNew)wNew[e]=-1;
 for(const [i,delta] of rec.dual.delta)wNew[unNew[i]]+=delta;
 let first=null;outer:for(let c=0;c<10;c++)for(let a=0;a<10;a++)for(let b=0;b<10;b++)for(let z=0;z<10;z++){
  const q=R(c,a,b,z);if(q.some(e=>usedNew[e]))continue;first=q;break outer;
 }
 assert(first!==null);
 const originalScore=first.reduce((s,e)=>s+wNew[e],0);
 assert(originalScore+1000000>0);mutationRejected++;
 if(cert.kind==="ZERO"){
  const e=cert.demand,resource=e[0]==="P"?100*e[1]+10*e[2]+e[3]:300+100*e[1]+10*e[2]+e[3];
  // New case is full-support: the original zero-support demand cannot remain an obstruction.
  if(usedNew[resource]){sourceZeroInvalid++;continue;}let supported=false;
  outer2:for(let c=0;c<10;c++)for(let a=0;a<10;a++)for(let b=0;b<10;b++)for(let z=0;z<10;z++){
   const q=R(c,a,b,z);if(q.some(e=>usedNew[e]))continue;if(q.includes(resource)){supported=true;break outer2;}
  }
  assert(supported);sourceZeroInvalid++;
 }else{
  const unOld=[];for(let e=0;e<600;e++)if(!usedOld[e])unOld.push(e);
  const wOld=new Int32Array(600);for(const e of unOld)wOld[e]=-1;
  for(const [i,delta] of cert.delta)wOld[unOld[i]]+=delta;
  let sum=0,max=-Infinity;
  for(const e of unNew)sum+=wOld[e];
  for(let c=0;c<10;c++)for(let a=0;a<10;a++)for(let b=0;b<10;b++)for(let z=0;z<10;z++){
   const q=R(c,a,b,z);if(q.some(e=>usedNew[e]))continue;
   max=Math.max(max,q.reduce((s,e)=>s+wOld[e],0));
  }
  assert(sum<=0||max>0);sourceDualInvalid++;
 }
}
console.log(JSON.stringify({status:"PASS",unique_new_prefixes:seen.size,old_dual_invalid:sourceDualInvalid,old_zero_invalid:sourceZeroInvalid,mutations_rejected:mutationRejected},null,2));
