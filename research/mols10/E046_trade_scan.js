#!/usr/bin/env node
"use strict";
// E046: exact integer-only local trade audit. Node.js >=18; no solver dependency.
// Run in research/mols10: node E046_trade_scan.js > E046_TRADE_RESULTS.json
const fs=require("fs");
function run(scans,certs){
function ids(c,a,b,d){return [10*a+b,100+10*a+d,200+10*b+d,300+10*c+a,400+10*c+b,500+10*c+d]}
function usedFor(S){
 const used=new Uint8Array(600);
 for(let s=0;s<3;s++){if(S[s].length!==4)throw Error("not k4");
  for(let r=0;r<4;r++)if(new Set(S[s][r]).size!==10)throw Error("nonlatin row");
  for(let c=0;c<10;c++)if(new Set(S[s].map(row=>row[c])).size!==4)return null;}
 for(let r=0;r<4;r++)for(let c=0;c<10;c++)for(const e of ids(c,S[0][r][c],S[1][r][c],S[2][r][c])){
  if(used[e])return null;used[e]=1;}return used;
}
function assess(used,weight,target){
 const deg=new Uint16Array(600);let candidates=0,max=-Infinity;
 for(let c=0;c<10;c++){const missing=[[],[],[]];
  for(let s=0;s<3;s++)for(let v=0;v<10;v++)if(!used[300+100*s+10*c+v])missing[s].push(v);
  for(const a of missing[0])for(const b of missing[1]){if(used[10*a+b])continue;
   for(const d of missing[2]){if(used[100+10*a+d]||used[200+10*b+d])continue;
    const R=ids(c,a,b,d);candidates++;for(const e of R)deg[e]++;
    if(weight){let score=0;for(const e of R)score+=weight[e];if(score>max)max=score;}
   }}}
 let zeros=0;for(let e=0;e<600;e++)if(!used[e]&&!deg[e])zeros++;
 let sum=0;if(weight)for(let e=0;e<600;e++)if(!used[e])sum+=weight[e];
 return {candidates,zeros,max,sum,targetZero:target!==null&&!used[target]&&!deg[target]};
}
const out={experiment:"E046",input_sha:{prefixes:"db9fc7211d681516e0d338473d95d8abe39af0df",certificates:"173d10f19aaf85c288d54a1282534838fa04b472"},cases:scans.cases.length,exact_source_pass:0,source_dual:0,source_zero:0,by_mask:{},examples:[],candidate_evaluations:0,scope:"fixed k4 prefixes and one fourth-row two-column swap; neither LP-feasible nor unrestricted status inferred"};
for(let mask=1;mask<=7;mask++)out.by_mask[mask]={attempts:0,valid:0,invalid:0,zero_support:0,positive_support:0,old_cert_survives:0,old_cert_breaks:0,escape_both:0};
for(let ix=0;ix<scans.cases.length;ix++){
 const S=scans.cases[ix].prefix.map(square=>square.map(row=>row.slice())),cert=certs.certificates[ix];
 if(cert.index!==ix)throw Error("misaligned");
 const old=usedFor(S);if(!old)throw Error("source invalid");
 let weight=null,target=null;
 if(cert.kind==="DUAL"){out.source_dual++;weight=new Int32Array(600);const un=[];
  for(let e=0;e<600;e++)if(!old[e]){un.push(e);weight[e]=-1;}
  for(const [i,d] of cert.delta)weight[un[i]]+=d;
 }else{out.source_zero++;const e=cert.demand;target=e[0]==="P"?100*e[1]+10*e[2]+e[3]:300+100*e[1]+10*e[2]+e[3];}
 const src=assess(old,weight,target);
 if(weight&&(src.sum!==cert.sum||src.max!==cert.max||src.sum<=0||src.max>0))throw Error("invalid source Farkas");
 if(!weight&&!src.targetZero)throw Error("invalid source zero");
 out.exact_source_pass++;
 for(let mask=1;mask<=7;mask++)for(let c=0;c<10;c++)for(let d=c+1;d<10;d++){
  const stat=out.by_mask[mask];stat.attempts++;
  for(let s=0;s<3;s++)if(mask&(1<<s))[S[s][3][c],S[s][3][d]]=[S[s][3][d],S[s][3][c]];
  const now=usedFor(S);
  if(!now)stat.invalid++;
  else{
   stat.valid++;const z=assess(now,weight,target);out.candidate_evaluations+=z.candidates;
   if(z.zeros)stat.zero_support++;else stat.positive_support++;
   const survives=weight?(z.sum>0&&z.max<=0):z.targetZero;
   if(survives)stat.old_cert_survives++;else stat.old_cert_breaks++;
   if(!z.zeros&&!survives){stat.escape_both++;
    if(out.examples.length<20)out.examples.push({source_index:ix,mask,swap:[c,d],candidates:z.candidates,old_dual_sum:z.sum,old_dual_max:z.max});}
  }
  for(let s=0;s<3;s++)if(mask&(1<<s))[S[s][3][c],S[s][3][d]]=[S[s][3][d],S[s][3][c]];
 }
}
return out;
}
const scans=JSON.parse(fs.readFileSync("E045_GUIDED_RESULTS.json","utf8"));
const certs=JSON.parse(fs.readFileSync("E045_CERTIFICATES.json","utf8"));
console.log(JSON.stringify(run(scans,certs),null,2));
