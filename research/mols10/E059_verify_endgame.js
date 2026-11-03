#!/usr/bin/env node
'use strict'; const fs=require('fs');const d=JSON.parse(fs.readFileSync((__dirname+'/E059_2024_9x10_analysed.json')));const original=d.published_9x10_rectangles;
const P=[[0,1],[0,2],[1,2]],n=10;
function check(cond,m){if(!cond)throw Error(m)}
function ways(A){let missing=[];for(let c=0;c<n;c++){let seen=new Set(A.map(row=>row[c])),m=[];for(let v=0;v<n;v++)if(!seen.has(v))m.push(v);check(m.length===2,'not eight rows');missing.push(m)}
 let rows=[];let ans=[];
 function walk(c,seen){if(c===n){let y=ans.map((v,j)=>missing[j].find(w=>w!==v));check(new Set(y).size===10,'other row not Latin');rows.push([ans.slice(),y]);return;}
   for(let v of missing[c])if(!seen.has(v)){ans[c]=v;seen.add(v);walk(c+1,seen);seen.delete(v)}}
 walk(0,new Set());return rows;}
let items=[],total=0;
for(let omit=0;omit<9;omit++){
 const W=original.map(s=>s.filter((row,i)=>i!==omit));
 for(let s of W){for(let row of s)check(new Set(row).size===10,'bad Latin row')}
 let x=W.map(ways),cnt=0,max=0;
 for(let a of x[0])for(let b of x[1])for(let c of x[2]){
  cnt++;const S=[W[0].concat(a),W[1].concat(b),W[2].concat(c)];
  let counts=P.map(([i,j])=>new Set(S[i].flatMap((row,r)=>row.map((v,col)=>v+','+S[j][r][col]))).size);
  let sum=counts.reduce((u,v)=>u+v,0);max=Math.max(max,sum);
  check(sum<300,'FOUND COMPLETE TRIPLE: must report as witness');
 }
 check(cnt===x[0].length*x[1].length*x[2].length,'not all combinations');total+=cnt;
 items.push({omitted:omit,completions:x.map(v=>v.length),checked:cnt,max_overlay_sum:max});
}
check(total===5392,'unexpected count');console.log(JSON.stringify({status:'INDEPENDENT_ENDGAME_VERIFIED',fixed_prefixes:9,completed_squares_combinations:total,full_triples:0,results:items,scope:'ONLY 2024 Figure3 nine 8-row restrictions'}));
