#!/usr/bin/env node
/* Independent exact replay of E038 triadic resource-forcing contradictions.
No SciPy, no Python, no SAT/LP solver. */
'use strict';const fs=require('fs');
const D=JSON.parse(fs.readFileSync(__dirname+'/E038_CERTIFICATES.json','utf8'));
const W=JSON.parse(fs.readFileSync(__dirname+'/E038_TRIADS.json','utf8'));
function assert(x,m){if(!x)throw Error(m)}
const P=[[0,1],[0,2],[1,2]],key=x=>x.join(':');
function checkTriad(z){
 const c=D.certificates.find(x=>x.index===z.index&&key(x.cycle)===key(z.cycle));
 assert(c&&c.kind==='EXACT_INTEGER_FARKAS','source not certified');
 const S=c.prefix,n=10,k=4;const used=P.map(([i,j])=>new Set());
 for(let s=0;s<3;s++){
  assert(S[s].length===k,'k');for(const row of S[s])assert(row.length===n&&new Set(row).size===n,'Latin row');
  for(let col=0;col<n;col++)assert(new Set(S[s].map(row=>row[col])).size===k,'Latin col');
 }
 for(let p=0;p<3;p++){const [i,j]=P[p];for(let r=0;r<k;r++)for(let col=0;col<n;col++)used[p].add(S[i][r][col]+':'+S[j][r][col]);assert(used[p].size===n*k,'orthogonal')}
 const all=new Set();for(let p=0;p<3;p++)for(let a=0;a<n;a++)for(let b=0;b<n;b++)if(!used[p].has(a+':'+b))all.add(key(['P',p,a,b]));
 for(let s=0;s<3;s++)for(let col=0;col<n;col++)for(let a=0;a<n;a++)if(!S[s].some(row=>row[col]===a))all.add(key(['C',s,col,a]));
 const w=z.witness;const a=w.positive[0],b=w.positive[1],d=w.negative;
 assert(key(a)!==key(b)&&key(a)!==key(d)&&key(b)!==key(d),'distinct');
 assert(a.slice(0,2).join(':')!==b.slice(0,2).join(':'),'positive demands same class');
 assert([a,b,d].every(x=>all.has(key(x))),'not residual demand');
 let count=0,positiveCovered=[0,0],negativeCovered=0;
 for(let col=0;col<n;col++){
  const avail=[0,1,2].map(s=>Array.from({length:n},(_,i)=>i).filter(x=>!S[s].some(row=>row[col]===x)));
  for(const A of avail[0])for(const B of avail[1])for(const C of avail[2]){
   if(used[0].has(A+':'+B)||used[1].has(A+':'+C)||used[2].has(B+':'+C))continue;
   const q=new Set([key(['P',0,A,B]),key(['P',1,A,C]),key(['P',2,B,C]),key(['C',0,col,A]),key(['C',1,col,B]),key(['C',2,col,C])]);
   const p0=+q.has(key(a)),p1=+q.has(key(b)),minus=+q.has(key(d));
   assert(p0+p1-minus<=0,'invalid triad inequality');
   positiveCovered[0]+=p0;positiveCovered[1]+=p1;negativeCovered+=minus;count++;
  }
 }
 assert(count===w.candidate_count,'candidate count mismatch');
 assert(positiveCovered.every(x=>x>0)&&negativeCovered>0,'degenerate zero support');
 return count;
}
let beyond=0,max=0;
for(const z of W.results){const n=checkTriad(z);max=Math.max(max,n);if(!z.hall15)beyond++}
assert(W.results.length===59&&beyond===51,'totals');
let bad=JSON.parse(JSON.stringify(W.results[0]));bad.witness.negative=['P',0,0,0];
let reject=false;try{checkTriad(bad)}catch(e){reject=true}assert(reject,'mutation accepted');
console.log(JSON.stringify({status:'PASS',verified_triads:W.results.length,beyond_Hall15:beyond,mutation_rejected:reject,max_candidates:max,global_status:'OPEN',scope:'fixed prefixes only'}));