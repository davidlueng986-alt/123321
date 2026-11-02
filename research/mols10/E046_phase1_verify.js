#!/usr/bin/env node
"use strict";
// Independent integer-only verification; does not import Python LP implementation.
const fs=require("fs"),assert=require("assert");
const data=JSON.parse(fs.readFileSync("E046_PHASE1_RESULTS.json","utf8"));
function resources(c,a,b,d){return [10*a+b,100+10*a+d,200+10*b+d,300+10*c+a,400+10*c+b,500+10*c+d]}
let duals=0,zeros=0,feasibleNumerical=0,unknown=0,placements=0;
for(const rec of data.cases){
 const S=rec.prefix,used=new Uint8Array(600);
 assert(S.length===3);
 for(let s=0;s<3;s++){
  assert(S[s].length===4);
  for(let r=0;r<4;r++)assert(new Set(S[s][r]).size===10);
  for(let c=0;c<10;c++)assert(new Set(S[s].map(row=>row[c])).size===4);
 }
 for(let r=0;r<4;r++)for(let c=0;c<10;c++){
  const R=resources(c,S[0][r][c],S[1][r][c],S[2][r][c]);
  for(const e of R){assert(!used[e]);used[e]=1;}
 }
 const un=[];for(let e=0;e<600;e++)if(!used[e])un.push(e);
 assert(un.length===360);
 let w=null;
 if(rec.status==="EXACT_DUAL"){
  w=new Int32Array(600);for(const e of un)w[e]=-1;
  for(const [i,delta] of rec.dual.delta){assert(i>=0&&i<360);w[un[i]]+=delta;}
  assert(un.reduce((s,e)=>s+w[e],0)===rec.dual.sum&&rec.dual.sum>0);
 }
 const deg=new Uint16Array(600);let mx=-Infinity,n=0;
 for(let c=0;c<10;c++)for(let a=0;a<10;a++)for(let b=0;b<10;b++)for(let d=0;d<10;d++){
  const R=resources(c,a,b,d);if(R.some(e=>used[e]))continue;
  n++;for(const e of R)deg[e]++;
  if(w){const score=R.reduce((s,e)=>s+w[e],0);if(score>mx)mx=score;assert(score<=0);}
 }
 placements+=n;assert(n===rec.variables);
 if(w){assert(mx===rec.dual.max);duals++;}
 else if(rec.status==="NUMERICAL_LP_FEASIBLE"){assert(rec.max_residual<1e-6);feasibleNumerical++;}
 else if(rec.status.startsWith("UNKNOWN"))unknown++;
 else throw Error("unexpected status "+rec.status);
}
console.log(JSON.stringify({cases:data.cases.length,exact_duals:duals,numerical_lp_feasible:feasibleNumerical,unknown,placements,status:"PASS"},null,2));
