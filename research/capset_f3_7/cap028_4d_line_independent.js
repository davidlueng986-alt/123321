#!/usr/bin/env node
'use strict';
const A774=[[0,0,1,0],[0,0,1,2],[0,0,2,1],[0,1,0,1],[0,2,0,2],[0,2,1,2],[0,2,2,1],[1,0,1,0],[1,0,1,1],[1,0,2,2],[1,2,1,0],[1,2,1,2],[1,2,2,1],[1,2,2,2],[2,0,0,0],[2,0,2,1],[2,1,2,2],[2,2,0,1]],A766=[[0,0,0,1],[0,0,2,2],[0,1,0,1],[0,1,2,0],[0,1,2,1],[0,2,0,0],[0,2,2,2],[1,1,1,0],[1,1,1,2],[1,2,0,2],[1,2,1,0],[1,2,1,2],[2,1,1,0],[2,1,1,1],[2,2,0,0],[2,2,1,0],[2,2,1,1],[1,1,2,0],[2,1,2,1]];
const enc=a=>a.reduce((s,x)=>3*s+x,0);
const dec=i=>{let a=[];for(let j=0;j<4;j++){a.unshift(i%3);i=Math.floor(i/3);}return a;};
const p=Array.from({length:81},(_,i)=>dec(i));
function verify(a){
 const s=new Set(a.map(enc));if(s.size!==a.length)throw Error('duplicates');
 for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)
  if(s.has(enc(a[i].map((x,k)=>(6-x-a[j][k])%3))))throw Error('3AP');
 return a.length;
}
// Independently replay the exact 17-point seed extension census.
const seed=A766.slice(0,-2);
const canExtend=(a)=>{try{verify(a);return true;}catch(_){return false;}};
const single=p.filter(x=>!new Set(seed.map(enc)).has(enc(x))&&canExtend(seed.concat([x])));
const pairs=[];
for(let i=0;i<single.length;i++)for(let j=i+1;j<single.length;j++)
 if(canExtend(seed.concat([single[i],single[j]])))pairs.push([single[i],single[j]]);
const balanced=pairs.filter(([a,b])=>[0,1,2].every(k=>seed.concat([a,b]).filter(x=>x[0]===k).length===[7,6,6][k]));
if(single.length!==5||pairs.length!==3||balanced.length!==1||
 enc(balanced[0][0])!==enc([1,1,2,0])||enc(balanced[0][1])!==enc([2,1,2,1]))
 throw Error('17-to-19 exact extension census');
const ns=p.filter(x=>x.some(z=>z)&&x.find(z=>z)!==2);
const chosen=new Set(Array.from({length:11},(_,i)=>7*i%81));
const f=p.map((x,i)=>3+Number(x[0]===0&&x[1]===0)+3*Number(chosen.has(i)));
const ls=new Map();
for(const u of ns)for(const x of p){
 const line=[0,1,2].map(k=>enc(x.map((v,i)=>(v+k*u[i])%3))).sort((a,b)=>a-b);
 ls.set(line.join(','),line);
}
if(ls.size!==1080||verify(A774)!==18||verify(A766)!==19)throw Error('setup');
let hist={},m1=0,m2=0,max=0;
for(const line of ls.values()){
 const q=line.map(i=>f[i]).sort((a,b)=>b-a),key=q.join(',');
 hist[key]=(hist[key]||0)+1;
 const m=q.reduce((a,b)=>a+b,0);
 max=Math.max(max,m);m1+=m;m2+=m*(m-1)/2;
}
const expected={'3,3,3':496,'4,3,3':193,'4,4,4':5,'6,3,3':217,'6,4,3':55,'6,6,3':31,'6,6,4':4,'7,3,3':55,'7,4,4':6,'7,6,3':16,'7,6,6':1,'7,7,4':1};
for(const [k,v] of Object.entries(expected))if(hist[k]!==v)throw Error('profile '+k);
if(Object.keys(hist).length!==12||max!==19||m1!==11400||m2!==56382)throw Error('moments');
console.log(JSON.stringify({witnesses:[18,19],lines:ls.size,profiles:12,max,m1,m2}));
