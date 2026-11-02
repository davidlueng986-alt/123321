#!/usr/bin/env node
/* Independent exact verifier for E038 certificates: no Python, SciPy, LP or MILP.
   Rebuilds every allowed cell placement, all six resource demands, and all Latin constraints.
   Each proof excludes only the specified FIXED four-row prefix. */
'use strict';
const fs=require('fs'),crypto=require('crypto');
const file=process.argv[2]||__dirname+'/E038_CERTIFICATES.json';
const data=JSON.parse(fs.readFileSync(file,'utf8'));
function check(cond,msg){if(!cond)throw Error(msg)}
const P=[[0,1],[0,2],[1,2]];
const key=x=>x.join(':');
function build(S){
 const n=S[0][0].length,k=S[0].length,range=Array.from({length:n},(_,i)=>i),used=[];
 check(S.length===3&&S.every(A=>A.length===k),'three squares same rows');
 for(const A of S){
  for(const row of A)check(row.length===n&&new Set(row).size===n&&row.every(x=>Number.isInteger(x)&&x>=0&&x<n),'row Latin');
  for(let c=0;c<n;c++)check(new Set(A.map(row=>row[c])).size===k,'column Latin');
 }
 for(const [s,t] of P){let U=new Set();for(let r=0;r<k;r++)for(let c=0;c<n;c++)U.add(S[s][r][c]+':'+S[t][r][c]);check(U.size===n*k,'overlay');used.push(U)}
 const missing=Array.from({length:3},(_,s)=>Array.from({length:n},(_,c)=>range.filter(v=>!S[s].some(row=>row[c]===v))));
 const E=[];
 for(let p=0;p<3;p++)for(let a=0;a<n;a++)for(let b=0;b<n;b++)if(!used[p].has(a+':'+b))E.push(['P',p,a,b]);
 for(let s=0;s<3;s++)for(let c=0;c<n;c++)for(const v of missing[s][c])E.push(['C',s,c,v]);
 check(E.length===6*n*(n-k),'resource demands');
 const keys=new Map(E.map((e,i)=>[key(e),i]));
 const T=[];
 for(let c=0;c<n;c++)for(const a of missing[0][c])for(const b of missing[1][c])for(const z of missing[2][c]){
  if(used[0].has(a+':'+b)||used[1].has(a+':'+z)||used[2].has(b+':'+z))continue;
  const es=[['P',0,a,b],['P',1,a,z],['P',2,b,z],['C',0,c,a],['C',1,c,b],['C',2,c,z]];
  const indexes=es.map(e=>keys.get(key(e)));
  check(indexes.every(x=>Number.isInteger(x)),'candidate resource missing');
  T.push(indexes);
 }
 return {E,T,n,k};
}
function verify(cert){
 const {E,T,n,k}=build(cert.prefix);check(n===10&&k===4,'scope');
 if(cert.kind==='ZERO_SUPPORT'){
  const d=E.findIndex(x=>key(x)===key(cert.demand));check(d>=0,'demand not in residual');
  check(!T.some(c=>c.includes(d)),'demand has support');
  return {kind:'ZERO_SUPPORT',candidates:T.length};
 }
 check(cert.kind==='EXACT_INTEGER_FARKAS','unknown kind');
 const w=cert.weights;check(w.length===E.length&&w.every(Number.isSafeInteger),'weights');
 const sum=w.reduce((a,b)=>a+b,0);check(sum===cert.weight_sum&&sum>0,'nonpositive Farkas sum');
 let max=-Infinity;
 for(const candidate of T){const score=candidate.reduce((s,i)=>s+w[i],0);if(score>max)max=score;check(score<=0,'dual violated by a candidate')}
 check(max===cert.max_candidate_weight,'max mismatch');check(T.length===cert.candidates,'candidate count mismatch');
 return {kind:'EXACT_INTEGER_FARKAS',candidates:T.length,sum,max};
}
function positiveControl(){
 const n=5,S=[1,2,3].map(a=>Array.from({length:4},(_,r)=>Array.from({length:n},(_,c)=>(r+a*c)%n)));
 const {E,T}=build(S);check(E.length===30,'affine control resource count');
 const covers=Array(E.length).fill(0);
 for(let c=0;c<n;c++){
  const [a,b,z]=[1,2,3].map(q=>(4+q*c)%n);
  const candidate=[['P',0,a,b],['P',1,a,z],['P',2,b,z],['C',0,c,a],['C',1,c,b],['C',2,c,z]];
  const ids=candidate.map(x=>E.findIndex(y=>key(x)===key(y)));
  check(ids.every(x=>x>=0),'affine candidate missing');
  check(T.some(t=>t.every((v,i)=>v===ids[i])),'affine completion absent');
  for(const id of ids)covers[id]++;
 }
 check(covers.every(x=>x===1),'affine complete cover');return true;
}
check(positiveControl(),'positive control failed');
const totals={EXACT_INTEGER_FARKAS:0,ZERO_SUPPORT:0};let maxCand=0;
for(const c of data.certificates){const v=verify(c);totals[v.kind]++;maxCand=Math.max(maxCand,v.candidates)}
check(data.certificates.length===360&&totals.EXACT_INTEGER_FARKAS===317&&totals.ZERO_SUPPORT===43,'totals');
// Negative control: corrupt a valid Farkas certificate to break an exact invariant.
const first=data.certificates.find(x=>x.kind==='EXACT_INTEGER_FARKAS');
const bad={...first,weights:first.weights.slice()};bad.weights[0]+=10000;
let rejected=false;try{verify(bad)}catch(e){rejected=true}check(rejected,'corrupted dual was accepted');
const supp=data.certificates.find(x=>x.kind==='ZERO_SUPPORT');
const bad2={...supp,demand:['C',0,0,0]};
let rejected2=false;try{verify(bad2)}catch(e){rejected2=true}check(rejected2,'corrupted support certificate was accepted');
const sha=crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
console.log(JSON.stringify({status:'PASS',scope:'360 sampled fixed prefixes only',counts:totals,positive_control_n5:true,dual_mutation_rejected:rejected,support_mutation_rejected:rejected2,max_candidates:maxCand,sha256:sha,global_status:'OPEN'}));