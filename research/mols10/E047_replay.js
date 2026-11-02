#!/usr/bin/env node
'use strict';
// Independent exact integer replay; requires E047_REGENERATED.json from E047_reproduce.py.
const fs=require('fs'),assert=require('assert');
const src=JSON.parse(fs.readFileSync('E047_SOURCES.json','utf8')).sources;
const D=JSON.parse(fs.readFileSync('E047_REGENERATED.json','utf8'));
const ids=(c,a,b,z)=>[10*a+b,100+10*a+z,200+10*b+z,300+10*c+a,400+10*c+b,500+10*c+z];
function make(U,a,b,c,d,m,n){const V=U.map(X=>X.map(row=>row.slice()));for(let s=0;s<3;s++){if(m>>s&1)[V[s][3][a],V[s][3][b]]=[V[s][3][b],V[s][3][a]];if(n>>s&1)[V[s][3][c],V[s][3][d]]=[V[s][3][d],V[s][3][c]];}return V;}
function usedOf(S){const used=new Set();for(let s=0;s<3;s++){for(let r=0;r<4;r++)assert(new Set(S[s][r]).size===10);for(let c=0;c<10;c++)assert(new Set(S[s].map(row=>row[c])).size===4);}for(let r=0;r<4;r++)for(let c=0;c<10;c++){const R=ids(c,S[0][r][c],S[1][r][c],S[2][r][c]);for(const e of R){assert(!used.has(e));used.add(e)}}assert(used.size===240);return used;}
function verify(row){const [sid,a,b,c,d,m,n,cert]=row,S=make(src[sid],a,b,c,d,m,n),used=usedOf(S),free=[];for(let e=0;e<600;e++)if(!used.has(e))free.push(e);assert(free.length===360);const index=new Map(free.map((e,i)=>[e,i]));let weights=null,zeroId=-1;
if(cert[0]==='D'){weights=Array(360).fill(-1);for(const [i,v] of cert[2])weights[i]+=v;assert(weights.reduce((x,y)=>x+y,0)===cert[1]&&cert[1]>0)}else{assert(cert[0]==='Z');const e=cert[1];zeroId=e[0]==='P'?100*e[1]+10*e[2]+e[3]:300+100*e[1]+10*e[2]+e[3];assert(index.has(zeroId))}
let count=0,zcount=0;for(let c=0;c<10;c++)for(let a=0;a<10;a++)for(let b=0;b<10;b++)for(let z=0;z<10;z++){const R=ids(c,a,b,z);if(R.some(e=>used.has(e)))continue;count++;if(weights){assert(R.reduce((sum,e)=>sum+weights[index.get(e)],0)<=0)}else if(R.includes(zeroId))zcount++}assert(zcount===0);return count;}
const seen=new Set();let total=0,dual=0,zero=0;for(const r of D.records){const key=r.slice(0,7).join(',');assert(!seen.has(key));seen.add(key);total+=verify(r);if(r[7][0]==='D')dual++;else zero++;}
assert(seen.size===479&&dual===400&&zero===79);
const mutated=JSON.parse(JSON.stringify(D.records.find(x=>x[7][0]==='D')));mutated[7][1]+=1000000;mutated[7][2].push([0,1000000]);let rejected=false;try{verify(mutated)}catch(e){rejected=true}assert(rejected);
const pairs=[];for(let a=0;a<10;a++)for(let b=a+1;b<10;b++)pairs.push([a,b]);let valid=0;
function isValid(S){for(let s=0;s<3;s++){for(let r=0;r<4;r++)if(new Set(S[s][r]).size!==10)return false;for(let c=0;c<10;c++)if(new Set(S[s].map(row=>row[c])).size!==4)return false;}const used=new Set();for(let r=0;r<4;r++)for(let c=0;c<10;c++){const R=ids(c,S[0][r][c],S[1][r][c],S[2][r][c]);for(const e of R.slice(0,3)){if(used.has(e))return false;used.add(e)}}return used.size===120;}
for(const [sid,U] of Object.entries(src)){let local=0;for(let i=0;i<45;i++)for(let j=i+1;j<45;j++){const [a,b]=pairs[i],[c,d]=pairs[j];if(new Set([a,b,c,d]).size!==4)continue;for(let m=1;m<8;m++)for(let n=1;n<8;n++){const V=make(U,a,b,c,d,m,n);if(isValid(V)){local++;assert(seen.has([sid,a,b,c,d,m,n].join(',')))}}}assert(local===D.counts[sid]);valid+=local;}
assert(valid===479);console.log(JSON.stringify({status:'PASS',proposals:246960,valid,dual,zero,legal_placements:total,mutation_rejected:rejected},null,2));
