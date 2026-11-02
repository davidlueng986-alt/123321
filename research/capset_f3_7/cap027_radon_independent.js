// CAP-027 independent Node.js modular arithmetic checker. No dependencies.
'use strict';
const assert=require('node:assert/strict');
const vecs=k=>{const a=[];for(let z=0;z<3**k;z++){let q=z,v=Array(k).fill(0);for(let i=k-1;i>=0;i--){v[i]=q%3;q=Math.floor(q/3)}a.push(v)}return a};
const P=vecs(4),N=P.filter(u=>u.some(x=>x)&&u.find(x=>x!==0)===1);
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0)%3;
const chosen=new Set(Array.from({length:11},(_,i)=>(7*i)%81));
const f=P.map((x,i)=>3+(x[0]===0&&x[1]===0?1:0)+(chosen.has(i)?3:0));
assert.equal(f.reduce((a,b)=>a+b,0),285);assert.equal(Math.max(...f),7);
let max6=0,min6=1e6;
for(const u of N)for(let t=0;t<3;t++){let s=0;for(let i=0;i<81;i++)if(dot(u,P[i])===t)s+=f[i];assert.equal(s%3,0);assert.ok(s<=109);max6=Math.max(max6,s);min6=Math.min(min6,s)}
const spaces=new Map();
for(const u of N)for(const v of N){const elems=[];for(let a=0;a<3;a++)for(let b=0;b<3;b++)elems.push(u.map((x,i)=>(a*x+b*v[i])%3).join(''));const key=[...new Set(elems)].sort().join('|');if(new Set(elems).size===9&&!spaces.has(key))spaces.set(key,[u,v])}
assert.equal(spaces.size,130);
let max5=0,min5=1e6;
for(const [u,v] of spaces.values()){
 const g=Array(9).fill(0);
 for(let k=0;k<81;k++)g[3*dot(u,P[k])+dot(v,P[k])]+=f[k];
 for(const val of g){assert.ok(val<=45);max5=Math.max(max5,val);min5=Math.min(min5,val)}
 const a=g[0]%3,b=((g[3]-g[0])%3+3)%3,c=((g[1]-g[0])%3+3)%3;
 for(let i=0;i<3;i++)for(let j=0;j<3;j++)assert.equal(g[3*i+j]%3,(a+b*i+c*j)%3);
}
const rank=rows=>{let a=rows.map(x=>x.map(y=>y%3)),r=0,n=a[0].length;for(let j=0;j<n;j++){let k=r;while(k<a.length&&!a[k][j])k++;if(k===a.length)continue;[a[r],a[k]]=[a[k],a[r]];if(a[r][j]===2)a[r]=a[r].map(x=>2*x%3);for(let i=0;i<a.length;i++)if(i!==r&&a[i][j]){let m=a[i][j];a[i]=a[i].map((x,q)=>(x-m*a[r][q]+6)%3)}r++}return r};
const R=[];for(const u of N)for(let t=0;t<3;t++)R.push(P.map(x=>+(dot(u,x)===t)));
assert.equal(rank(R),15);
console.log(JSON.stringify({test:'CAP027 independent JS',radon_rank:15,planes:spaces.size,grids:spaces.size*9,max5,min5,max6,min6,fiber_sum:285,cap_witness:false}));
