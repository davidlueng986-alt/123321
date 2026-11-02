#!/usr/bin/env node
// Independent verifier for E036_reproduce.py output. Node.js stdlib only.
const fs=require('fs');const crypto=require('crypto');const n=10;
const buf=fs.readFileSync('E036_WITNESSES.json','utf8').trim();
const W=JSON.parse(buf), assert=(b,m)=>{if(!b)throw Error(m)};
assert(W.length===156,'expected 156 representatives');
const id=Array.from({length:n},(_,i)=>i),f=id.map(i=>i^1);
function check(R){assert(R.length===3,'3 squares');for(const S of R){assert(S.length===6,'6 rows');for(const row of S)assert(row.length===n&&new Set(row).size===n&&row.every(x=>Number.isInteger(x)&&x>=0&&x<n),'Latin row');for(let c=0;c<n;c++)assert(new Set(S.map(row=>row[c])).size===6,'Latin column');}for(const [i,j] of [[0,1],[0,2],[1,2]]){const P=new Set();for(let r=0;r<6;r++)for(let c=0;c<n;c++)P.add(R[i][r][c]+','+R[j][r][c]);assert(P.size===60,'orthogonality prefix');}}
for(const R of W){check(R);for(let s=0;s<3;s++)assert(R[s][0].every((x,c)=>x===c),'first row');assert(R[0][1].every((x,c)=>x===f[c]),'canonical f');for(let c=0;c<n;c++)assert(new Set([c,R[0][1][c],R[1][1][c],R[2][1][c]]).size===4,'row1 disjoint');}
let corrupt=JSON.parse(JSON.stringify(W[0]));corrupt[0][2][0]=corrupt[0][2][1];let rejected=false;try{check(corrupt)}catch(e){rejected=true}assert(rejected,'corruption negative control');
const gens=[];for(let k=0;k<5;k++){let p=id.slice();[p[2*k],p[2*k+1]]=[p[2*k+1],p[2*k]];gens.push(p)}for(let k=0;k<4;k++){let p=id.slice(),a=2*k,b=a+2;[p[a],p[b]]=[p[b],p[a]];[p[a+1],p[b+1]]=[p[b+1],p[a+1]];gens.push(p)}
const invs=gens.map(p=>{let q=[];for(let i=0;i<n;i++)q[p[i]]=i;return q});const seen=new Set();
for(const R of W){const g=R[1][1],key=g.join('');assert(!seen.has(key),'duplicate orbit');const q=[key];seen.add(key);for(let t=0;t<q.length;t++){const h=[...q[t]].map(Number);for(let j=0;j<gens.length;j++){const p=gens[j],inv=invs[j],v=p.map(x=>inv[h[x]]).join('');if(!seen.has(v)){seen.add(v);q.push(v)}}}}
let total=0;let g=Array(n).fill(0);function enumerate(c,mask){if(c===n){total++;assert(seen.has(g.join('')),'missing orbit');return;}for(let v=0;v<n;v++)if(v!==c&&v!==(c^1)&&!(mask>>v&1)){g[c]=v;enumerate(c+1,mask|1<<v)}}enumerate(0,0);
assert(total===440192&&seen.size===total,'exhaustive orbit coverage');
const sha=crypto.createHash('sha256').update(JSON.stringify(W)).digest('hex');assert(sha==='5b198704a6cd24cae9ba57b7f938ce121aba182df1fc78738d39ab92a2aff66f','certificate SHA256');
console.log(JSON.stringify({status:'PASS',f_cycle_type:'2+2+2+2+2',g_orbits:156,legal_g:total,valid_6_row_prefixes:W.length,overlay_each:[60,60,60],corruption_rejected:true,sha256:sha,global_status:'OPEN'}));
