#!/usr/bin/env node
'use strict';
// Standalone integer-only verifier. No SciPy, no MILP, no generator imports.
const fs=require('fs');
const near=JSON.parse(fs.readFileSync(process.argv[2]||'near_triple.json','utf8'));
const certs=JSON.parse(fs.readFileSync(process.argv[3]||'E034_FOUR_ROW_EXACT_DUALS.json','utf8')).certificates;
const S=near.squares;const n=10, pairs=[[0,1],[0,2],[1,2]];
function ok(x,m){if(!x)throw Error(m)}
for(let s=0;s<3;s++){
 ok(S[s].length===n,'square rows');
 for(let r=0;r<n;r++)ok([...S[s][r]].sort((a,b)=>a-b).every((v,i)=>v===i),'Latin row');
 for(let c=0;c<n;c++)ok([...Array(n)].map((_,r)=>S[s][r][c]).sort((a,b)=>a-b).every((v,i)=>v===i),'Latin col');
}
const overlay=pairs.map(([a,b])=>new Set(Array.from({length:n*n},(_,i)=>`${S[a][Math.floor(i/n)][i%n]},${S[b][Math.floor(i/n)][i%n]}`)).size);
ok(overlay.join(',')==='100,100,91','near-triple overlay count '+overlay);
function combinations(arr,k){if(k===0)return [[]];if(arr.length<k)return [];return [...combinations(arr.slice(1),k-1).map(x=>[arr[0],...x]),...combinations(arr.slice(1),k)];}
const all=[];
for(const I of combinations([...Array(n).keys()],4)){
 const valid=pairs.every(([a,b])=>new Set(I.flatMap(r=>Array.from({length:n},(_,c)=>`${S[a][r][c]},${S[b][r][c]}`))).size===40);
 if(valid)all.push(I.join(','));
}
ok(all.length===39,'expected 39 valid subsets');
ok(certs.length===39,'expected 39 certificates');
const seen=new Set();let columns=0,minsum=Infinity,maxColumn=-Infinity;
for(const C of certs){
 const I=C.rows;const key=I.join(',');ok(all.includes(key),'non-valid 4-row subset '+key);ok(!seen.has(key),'duplicate subset');seen.add(key);
 ok(C.status==='EXACT_INTEGER_FARKAS'&&C.constraints===600,'metadata');
 const w=C.weights;ok(w.length===600&&w.every(Number.isSafeInteger),'weights');
 const total=w.reduce((a,b)=>a+b,0);ok(total>0&&total===C.sum,'positive dual sum');minsum=Math.min(minsum,total);
 const miss=[];
 for(let s=0;s<3;s++){
  miss[s]=[];
  for(let c=0;c<n;c++)miss[s][c]=[...Array(n).keys()].filter(v=>!I.some(r=>S[s][r][c]===v));
 }
 const used=pairs.map(([a,b])=>new Set(I.flatMap(r=>Array.from({length:n},(_,c)=>`${S[a][r][c]},${S[b][r][c]}`))));
 const edges=pairs.map((_,p)=>{
  let E=[];for(let a=0;a<n;a++)for(let b=0;b<n;b++)if(!used[p].has(`${a},${b}`))E.push(`${a},${b}`);
  return new Map(E.map((e,i)=>[e,i]));
 });
 const m=6,ncell=m*n,nrow=m*3*n,ncol=3*n*m;
 let nc=0;
 for(let r=0;r<m;r++)for(let c=0;c<n;c++){
  for(const a of miss[0][c])for(const b of miss[1][c])for(const d of miss[2][c]){
   if(used[0].has(`${a},${b}`)||used[1].has(`${a},${d}`)||used[2].has(`${b},${d}`))continue;
   const v=[a,b,d];let sum=w[r*n+c];
   for(let s=0;s<3;s++){
    sum+=w[ncell+(r*3+s)*n+v[s]];
    sum+=w[ncell+nrow+(s*n+c)*m+miss[s][c].indexOf(v[s])];
   }
   for(let p=0;p<3;p++){
    const e=[[a,b],[a,d],[b,d]][p].join(',');ok(edges[p].has(e),'pair map');
    sum+=w[ncell+nrow+ncol+p*n*m+edges[p].get(e)];
   }
   ok(sum<=0,'dual column violated at '+key+' '+[r,c,a,b,d]+' '+sum);
   maxColumn=Math.max(maxColumn,sum);nc++;
  }
 }
 ok(nc===C.variables,'candidate count mismatch '+key);
 columns+=nc;
}
console.log(JSON.stringify({status:'ALL_39_INDEPENDENT_INTEGER_FARKAS_CERTIFICATES_PASS',near_triple_overlays:overlay,valid_four_row_subsets:all.length,checked_candidate_columns:columns,min_dual_sum:minsum,max_candidate_dual_sum:maxColumn,claim:'No full 3-MOLS(10) can agree with this specified near-triple on four complete common rows; does not settle unrestricted 3-MOLS(10).'}));
