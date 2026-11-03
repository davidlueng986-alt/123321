#!/usr/bin/env node
// E059 independent exact certificate checks, plain JS, no Python/SciPy.
'use strict';
const fs=require('fs'),n=10,P=[[0,1],[0,2],[1,2]];
const fail=(s)=>{throw Error(s)}, check=(x,s)=>{if(!x)fail(s)};
function prefixCheck(S){
 const k=S[0].length;check(S.length===3,'three squares');
 for(const A of S){check(A.length===k,'k rows');
  for(const row of A)check(row.length===10&&new Set(row).size===10&&row.every(x=>Number.isInteger(x)&&x>=0&&x<10),'Latin rows');
  for(let c=0;c<10;c++)check(new Set(A.map(row=>row[c])).size===k,'Latin columns');
 }
 for(const [a,b] of P){const pairs=new Set();for(let r=0;r<k;r++)for(let c=0;c<n;c++)pairs.add(S[a][r][c]+','+S[b][r][c]);check(pairs.size===k*n,'overlay '+a+b)}
 return k;
}
function resources(S){const k=prefixCheck(S);const out=new Set();
 for(let i=0;i<3;i++){const [a,b]=P[i];const seen=new Set();for(let r=0;r<k;r++)for(let c=0;c<n;c++)seen.add(S[a][r][c]+','+S[b][r][c]);
  for(let x=0;x<n;x++)for(let y=0;y<n;y++)if(!seen.has(x+','+y))out.add('P:'+i+':'+x+':'+y);
 }
 for(let i=0;i<3;i++)for(let c=0;c<n;c++){const seen=new Set(S[i].map(row=>row[c]));for(let x=0;x<n;x++)if(!seen.has(x))out.add('C:'+i+':'+c+':'+x)}
 check(out.size===6*n*(n-k),'resource count');return out;
}
function terms(c,a,b,d){return ['P:0:'+a+':'+b,'P:1:'+a+':'+d,'P:2:'+b+':'+d,'C:0:'+c+':'+a,'C:1:'+c+':'+b,'C:2:'+c+':'+d]}
function verifyIntegral(path){const z=JSON.parse(fs.readFileSync(path,'utf8'));const S=z.prefix,r=resources(S),m=new Map();
 const k=S[0].length;check(z.remaining_integer_placements.length===n*(n-k),'placements');
 for(const xyz of z.remaining_integer_placements){check(xyz.length===4,'placement length');const [c,a,b,d]=xyz;
  for(const key of terms(c,a,b,d)){check(r.has(key),'forbidden resource '+key);m.set(key,(m.get(key)||0)+1)}
 }
 check(m.size===r.size,'missing resources');for(const key of r)check(m.get(key)===1,'resource not exactly once '+key);
 return {k,placements:z.remaining_integer_placements.length,resources:r.size,status:'PASS'};
}
function verifyFractional(path){const z=JSON.parse(fs.readFileSync(path,'utf8')),S=z.squares_first4_rows,r=resources(S),m=new Map();
 for(const x of z.weights){const [u,v,w,num,den]=x;check(num===1&&den===2,'not halves');
  for(let c=0;c<n;c++)for(const key of terms(c,(c+u)%n,(c+v)%n,(c+w)%n)){
   check(r.has(key),'forbidden resource '+key);m.set(key,(m.get(key)||0)+1)
  }
 }
 check(m.size===r.size,'missing resources');for(const key of r)check(m.get(key)===2,'resource not exact half-half '+key);
 return {k:4,orbits:z.weights.length,nonzero_placements:10*z.weights.length,resources:r.size,status:'PASS'};
}
const files=[(__dirname+'/E059_PRIMAL_WITNESS.json'),(__dirname+'/E059_INTEGRAL_PRIMAL_WITNESS.json'),(__dirname+'/E059_INTEGRAL_K7_WITNESS.json')];
const checked=[verifyFractional(files[0]),verifyIntegral(files[1]),verifyIntegral(files[2])];
// Deliberate corruption test: remove one integer placement and make sure checker rejects.
const bad=JSON.parse(fs.readFileSync(files[2],'utf8'));bad.remaining_integer_placements.pop();const badpath=(__dirname+'/E059_DELIBERATE_BAD_WITNESS.json');fs.writeFileSync(badpath,JSON.stringify(bad));
let mutationRejected=false;try{verifyIntegral(badpath)}catch(e){mutationRejected=true}
check(mutationRejected,'negative mutation not rejected');
console.log(JSON.stringify({status:'INDEPENDENT_EXACT_ALL_PASS',controls:checked,mutationRejected:true}));
