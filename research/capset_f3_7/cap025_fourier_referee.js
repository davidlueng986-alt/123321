// CAP-025 independent integer-only Fourier/convolution referee, no dependencies or randomness.
// node research/capset_f3_7/cap025_fourier_referee.js
"use strict";
const audit=function audit(){
 const N=729,blocks=[[0,1,2],[0,1,3],[0,2,4],[0,3,5],[0,4,5],[1,2,5],[1,3,4],[1,4,5],[2,3,4],[2,3,5]];
 const ok=(c,m)=>{if(!c)throw Error(m)};
 const vec=Array.from({length:N},(_,i)=>{let a=[];for(let j=0;j<6;j++){a.push(i%3);i=Math.floor(i/3)}return a});
 const enc=a=>a.reduce((s,v,i)=>s+v*3**i,0);
 const add=(x,y)=>enc(vec[x].map((v,i)=>(v+vec[y][i])%3));
 const dot=(x,y)=>vec[x].reduce((s,v,i)=>s+v*vec[y][i],0)%3;
 function H(complement){
  let out=new Set();
  for(let x=0;x<N;x++){let v=vec[x];if(v.every(t=>t!==0)&&v.filter(t=>t===2).length%2===0)out.add(x)}
  for(let mask=0;mask<64;mask++){let idx=[];for(let i=0;i<6;i++)if(mask>>i&1)idx.push(i);if(idx.length!==3)continue;
   let match=blocks.some(b=>b.every(i=>idx.includes(i)));if(match===complement)continue;
   for(let s=0;s<8;s++){let v=[0,0,0,0,0,0];idx.forEach((i,j)=>v[i]=(s>>j&1)?2:1);out.add(enc(v))}
  }ok(out.size===112,"112 construction");return out
 }
 const apply=(h,m)=>new Set([...h].map(x=>enc(m.map(row=>row.reduce((s,v,i)=>s+v*vec[x][i],0)%3))));
 function verifyCap(h){ok(h.size===112,"size");for(let x of h)for(let y of h)if(x!==y)ok(!h.has(enc(vec[x].map((v,i)=>(9-v-vec[y][i])%3))),"3AP")}
 function high(h){let D=[];for(let u=1;u<N;u++){if(vec[u].find(v=>v!==0)!==1)continue;let counts=[0,0,0];for(let x of h)counts[dot(u,x)]++;ok(counts[1]===counts[2],"not centered");let f=counts[0]-counts[1];ok(f===-23||f===4,"Fourier spectrum");if(f===-23){ok(counts.join()==="22,45,45","high slice");D.push(u)}else ok(counts.join()==="40,36,36","low slice")}ok(D.length===56,"high direction count");return new Set(D)}
 function pair(label,h1,h2){verifyCap(h1);verifyCap(h2);let D1=high(h1),D2=high(h2),common=[...D1].filter(u=>D2.has(u)),m=common.length,r=new Int32Array(N);for(let x of h1)for(let y of h2)r[add(x,y)]++;for(let z=0;z<N;z++){let orth=common.reduce((s,u)=>s+(dot(u,z)===0),0);let formula=z===0?2*m:16+4*(Number(h1.has(z))+Number(h2.has(z)))+3*orth-m;ok(r[z]===formula,"convolution mismatch "+label+" "+z)}let intersection=[...h1].filter(x=>h2.has(x)).length;ok(intersection===2*m,"dual intersection");return {pair:label,mstar:m,intersection,holes:[...r].filter(t=>t===0).length,formula_errors:0}}
 let h=H(false),hp=H(true),t1=[[1,1,0,0,0,0],[0,1,0,0,0,0],[0,0,1,1,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]],t2=[[1,0,1,0,0,0],[0,1,0,1,0,0],[0,0,1,0,0,0],[0,0,0,1,1,0],[0,0,0,0,1,1],[0,0,0,0,0,1]],t3=[[2,0,0,0,0,0],[0,1,0,0,0,0],[0,0,2,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]];
 let cases=[pair("H-H",h,h),pair("H-Hprime",h,hp),pair("H-T1(H)",h,apply(h,t1)),pair("H-T2(H)",h,apply(h,t2)),pair("H-T3(Hprime)",h,apply(hp,t3)),pair("T1(H)-T2(Hprime)",apply(h,t1),apply(hp,t2))];
 let deletion_checks=[],sorted=[...h].sort((a,b)=>a-b);
 for(let d=0;d<=4;d++){let d1=new Set(sorted.slice(0,Math.ceil(d/2))),d2=new Set(sorted.slice(Math.ceil(d/2),d)),r=new Int32Array(N);for(let x of h)if(!d1.has(x))for(let y of h)if(!d2.has(y))r[add(x,y)]++;let holes=[...r].filter(v=>v===0).length;ok(holes===d,"identical dual deletion exception "+d);deletion_checks.push({d,holes})}
 return {experiment:"CAP-025",projective_normals:364,full_convolution_vectors_per_case:729,cases,identical_dual_deletions:deletion_checks,scope:"finite tests, not a universal proof or exhaustive GL(6,3)"}
};
console.log(JSON.stringify(audit(),null,2));
