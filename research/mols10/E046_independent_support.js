#!/usr/bin/env node
"use strict";
// E046 second implementation, independent of E046_trade_scan.js. Bitmask column occupancy.
const fs=require("fs"),assert=require("assert");
const data=JSON.parse(fs.readFileSync("E045_GUIDED_RESULTS.json","utf8"));
function check(S){
 const col=Array.from({length:3},()=>Array(10).fill(0));
 const pair=Array.from({length:3},()=>new Uint8Array(100));
 for(let c=0;c<10;c++)for(let r=0;r<4;r++){
  const a=S[0][r][c],b=S[1][r][c],z=S[2][r][c];
  for(let s=0;s<3;s++){const v=S[s][r][c];if(col[s][c]&(1<<v))return null;col[s][c]|=1<<v;}
  for(const [k,id] of [[0,10*a+b],[1,10*a+z],[2,10*b+z]]){if(pair[k][id])return null;pair[k][id]=1;}
 }
 const degree=new Uint16Array(600);let candidates=0;
 for(let c=0;c<10;c++)for(let a=0;a<10;a++){
  if(col[0][c]&(1<<a))continue;
  for(let b=0;b<10;b++){
   if((col[1][c]&(1<<b))||pair[0][10*a+b])continue;
   for(let z=0;z<10;z++){
    if((col[2][c]&(1<<z))||pair[1][10*a+z]||pair[2][10*b+z])continue;
    candidates++;
    for(const id of [10*a+b,100+10*a+z,200+10*b+z,300+10*c+a,400+10*c+b,500+10*c+z])degree[id]++;
   }
  }
 }
 let zeros=0;
 for(let k=0;k<3;k++)for(let id=0;id<100;id++)if(!pair[k][id]&&!degree[k*100+id])zeros++;
 for(let s=0;s<3;s++)for(let c=0;c<10;c++)for(let v=0;v<10;v++)
  if(!(col[s][c]&(1<<v))&&!degree[300+100*s+10*c+v])zeros++;
 return {zeros,candidates};
}
const expected=JSON.parse(fs.readFileSync("E046_TRADE_RESULTS.json","utf8")).by_mask;
const result={};
for(let mask=1;mask<=7;mask++)result[mask]={valid:0,zero_support:0,positive_support:0};
for(const rec of data.cases){
 const S=rec.prefix.map(A=>A.map(row=>row.slice()));
 for(let mask=1;mask<=7;mask++)for(let c=0;c<10;c++)for(let d=c+1;d<10;d++){
  for(let s=0;s<3;s++)if(mask&(1<<s))[S[s][3][c],S[s][3][d]]=[S[s][3][d],S[s][3][c]];
  const z=check(S);
  if(z){result[mask].valid++;if(z.zeros)result[mask].zero_support++;else result[mask].positive_support++;}
  for(let s=0;s<3;s++)if(mask&(1<<s))[S[s][3][c],S[s][3][d]]=[S[s][3][d],S[s][3][c]];
 }
}
for(let mask=1;mask<=7;mask++){
 const a=result[mask],b=expected[mask];
 assert(a.valid===b.valid&&a.zero_support===b.zero_support&&a.positive_support===b.positive_support,"mismatch mask "+mask);
}
console.log(JSON.stringify({status:"PASS",source_cases:data.cases.length,results:result},null,2));
