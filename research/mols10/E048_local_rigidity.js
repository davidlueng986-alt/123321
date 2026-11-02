#!/usr/bin/env node
'use strict';
// E048: independent exact finite enumerations; no LP or floating point.
// Run: node research/mols10/E048_local_rigidity.js
const fs=require('fs'),assert=require('assert'),path=require('path');
const base=__dirname;
const read=f=>JSON.parse(fs.readFileSync(path.join(base,f),'utf8'));
const src=read('E047_SOURCES.json').sources;
const E44=read('E044_RESULTS.json').cases;
const E45=read('E045_GUIDED_RESULTS.json').cases;
const E47=read('E047_REGENERATED.json').records;
const clone=S=>S.map(X=>X.map(r=>r.slice()));
function reconstruct(rec){
 const [sid,a,b,c,d,m,n]=rec;const V=clone(src[String(sid)]);
 for(let s=0;s<3;s++){
  if(m&(1<<s))[V[s][3][a],V[s][3][b]]=[V[s][3][b],V[s][3][a]];
  if(n&(1<<s))[V[s][3][c],V[s][3][d]]=[V[s][3][d],V[s][3][c]];
 }
 return V;
}
function perms(a){if(!a.length)return [[]];return a.flatMap((x,i)=>perms(a.filter((_,j)=>j!==i)).map(y=>[x,...y]));}
const P=perms([0,1,2,3]);assert.equal(P.length,24);
function overlays(S,p=[0,1,2,3],q=[0,1,2,3],n=10){
 for(const [i,j] of [[0,1],[0,2],[1,2]]){
  const seen=new Uint8Array(n*n);
  for(let r=0;r<4;r++)for(let c=0;c<n;c++){
   const ri=i===0?r:i===1?p[r]:q[r],rj=j===0?r:j===1?p[r]:q[r];
   const idx=n*S[i][ri][c]+S[j][rj][c];if(seen[idx])return false;seen[idx]=1;
  }
 }
 return true;
}
function latin(S){
 for(const X of S){
  for(const row of X)if(row.length!==10||new Set(row).size!==10)return false;
  for(let c=0;c<10;c++)if(new Set(X.map(row=>row[c])).size!==4)return false;
 }
 return true;
}
const all=[...Object.values(src),...E47.map(reconstruct),...E44.map(x=>x.prefix),...E45.map(x=>x.prefix)];
assert.equal(all.length,1573);
const unique=new Map(all.map(S=>[JSON.stringify(S),S]));
assert.equal(unique.size,1565);
let alignments=0,nonidentity=0;
for(const S of unique.values()){
 assert(latin(S)&&overlays(S));
 for(const p of P)for(const q of P)if(overlays(S,p,q)){
  alignments++;if(p.some((v,i)=>v!==i)||q.some((v,i)=>v!==i))nonidentity++;
 }
}
assert.equal(alignments,1565);assert.equal(nonidentity,0);
function trades(S){
 const T=[];
 for(let z=0;z<3;z++)for(let r=0;r<4;r++)for(let s=r+1;s<4;s++)
 for(let c=0;c<10;c++)for(let d=c+1;d<10;d++)
 if(S[z][r][c]===S[z][s][d]&&S[z][r][d]===S[z][s][c])T.push([z,r,s,c,d]);
 return T;
}
function choose(A,k,cb,lo=0,stack=[]){
 if(!k){cb(stack);return;}
 for(let i=lo;i<=A.length-k;i++){stack.push(A[i]);choose(A,k-1,cb,i+1,stack);stack.pop();}
}
function apply(S,T){
 const V=clone(S);
 for(const [z,r,s,c,d] of T){
  [V[z][r][c],V[z][s][c]]=[V[z][s][c],V[z][r][c]];
  [V[z][r][d],V[z][s][d]]=[V[z][s][d],V[z][r][d]];
 }
 return V;
}
let proposal=0,valid=[0,0,0,0,0],intercalates=0,witness=null;
for(const [sid,S] of Object.entries(src)){
 const T=trades(S);intercalates+=T.length;
 for(let k=1;k<=4;k++)choose(T,k,subset=>{
  proposal++;const V=apply(S,subset);
  if(latin(V)&&overlays(V)){valid[k]++;witness={source:sid,trades:subset.map(x=>x.slice()),prefix:V};}
 });
}
assert.equal(intercalates,60);assert.equal(proposal,2895);
assert.deepStrictEqual(valid,[0,1,0,0,0]);
assert.equal(witness.source,'0');
assert.deepStrictEqual(witness.trades,[[1,0,1,1,4]]);
// Exact support obstruction: resource C(column=9,symbol=5) cannot be covered.
const S=witness.prefix,used=new Set();
function resources(c,a,b,z){return [10*a+b,100+10*a+z,200+10*b+z,300+10*c+a,400+10*c+b,500+10*c+z];}
for(let r=0;r<4;r++)for(let c=0;c<10;c++)for(const x of resources(c,S[0][r][c],S[1][r][c],S[2][r][c])){assert(!used.has(x));used.add(x);}
assert.equal(used.size,240);assert(!used.has(595));
let candidates=0,cover595=0;
for(let c=0;c<10;c++)for(let a=0;a<10;a++)for(let b=0;b<10;b++)for(let z=0;z<10;z++){
 const R=resources(c,a,b,z);if(R.some(x=>used.has(x)))continue;
 candidates++;if(R.includes(595))cover595++;
}
assert.equal(candidates,416);assert.equal(cover595,0);
const controls={};
for(const n of [5,7,11]){
 const F=[1,2,3].map(s=>Array.from({length:4},(_,r)=>Array.from({length:n},(_,c)=>(r+s*c)%n)));
 controls[n]=0;for(const p of P)for(const q of P)if(overlays(F,p,q,n))controls[n]++;
}
assert.deepStrictEqual(controls,{5:6,7:18,11:105});
console.log(JSON.stringify({status:'PASS',source_records:all.length,distinct_prefixes:unique.size,row_alignment_proposals:unique.size*576,row_alignment_valid:alignments,row_alignment_nonidentity:nonidentity,static_intercalates:intercalates,intercalate_subset_proposals:proposal,valid_intercalate_by_size:valid,unique_valid_trade:{source:witness.source,trades:witness.trades,legal_residual_candidates:candidates,zero_support_resource:595},positive_controls:controls},null,2));
