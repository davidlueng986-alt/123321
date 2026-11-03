#!/usr/bin/env node
'use strict';
const assert=require('assert'),fs=require('fs'),path=require('path');
const src=JSON.parse(fs.readFileSync(path.join(__dirname,'E061_near_triple.json'),'utf8')).squares;
const n=10;
function check(A,B){let base='0123456789';for(let T of [A,B]){
 for(let row of T)assert.strictEqual([...row].sort().join(''),base);
 for(let c=0;c<n;c++)assert.strictEqual([...Array(n)].map((_,r)=>T[r][c]).sort().join(''),base);
 }let pairs=new Set();for(let r=0;r<n;r++)for(let c=0;c<n;c++)pairs.add(A[r][c]+','+B[r][c]);assert.strictEqual(pairs.size,100);
}
function key(A,B){return JSON.stringify([A,B]);}
function comps(A,B,x,y){
 let cells=[];
 for(let r=0;r<n;r++)for(let c=0;c<n;c++)if(A[r][c]===x||A[r][c]===y)cells.push([r,c]);
 assert.strictEqual(cells.length,20);
 let seen=new Set(),out=[];
 for(let p=0;p<20;p++){
  if(seen.has(p))continue;
  seen.add(p);let q=[p],comp=[];
  while(q.length){let i=q.pop();let [r,c]=cells[i];comp.push([r,c]);
   for(let j=0;j<20;j++){
    if(seen.has(j))continue;let [rr,cc]=cells[j];
    if(r===rr||c===cc||B[r][c]===B[rr][cc]){seen.add(j);q.push(j);}
   }
  }out.push(comp);
 }return out;
}
function next(A,B){let res=[];
 for(let side=0;side<2;side++){
  let X=side?B:A,Y=side?A:B;
  for(let x=0;x<n;x++)for(let y=x+1;y<n;y++){
   let C=comps(X,Y,x,y);
   if(C.length===1)continue;
   for(let s=1;s<(1<<C.length)-1;s++){
    let Z=X.map(r=>r.slice());
    for(let i=0;i<C.length;i++)if((s>>i)&1)for(let [r,c] of C[i])Z[r][c]=Z[r][c]===x?y:x;
    let pair=side?[Y,Z]:[Z,Y];check(...pair);res.push(pair);
   }
  }
 }
 return res;
}
function transversals(A,B){let byA=Array.from({length:n},()=>[]),T=[];for(let r=0;r<n;r++)for(let c=0;c<n;c++)byA[A[r][c]].push([r,c]);
 let cols=new Array(n).fill(-1);
 function rec(a,rs,cs,bs){if(a===n){T.push(cols.slice());return;}
  for(let [r,c] of byA[a]){let rr=1<<r,cc=1<<c,bb=1<<B[r][c];
   if(rs&rr||cs&cc||bs&bb)continue;
   cols[r]=c;rec(a+1,rs|rr,cs|cc,bs|bb);cols[r]=-1;
  }
 }rec(0,0,0,0);return T;
}
function calc(){let A=src[0],B=src[2];check(A,B);
 let q=[[A,B]],seen=new Set([key(A,B)]),hist={},edges=0,maxT=0;
 for(let qi=0;qi<q.length;qi++){
  let [A,B]=q[qi],T=transversals(A,B);hist[T.length]=(hist[T.length]||0)+1;
  maxT=Math.max(maxT,T.length);
  for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++){
   let intersection=0;for(let r=0;r<n;r++)if(T[i][r]===T[j][r])intersection++;
   assert(intersection>=1,'two disjoint transversals found; stored graph max1 would be wrong');
  }
  for(let [AA,BB] of next(A,B)){
   edges++;let k=key(AA,BB);
   if(!seen.has(k)){seen.add(k);q.push([AA,BB]);}
  }
  assert(q.length<=3000,'unexpected large component; stop rather than overclaim');
 }
 assert.strictEqual(q.length,64);assert.strictEqual(edges,384);
 assert.deepStrictEqual(hist,{'1':48,'7':8,'10':8});
 let result={status:'INDEPENDENT_COMPLETE',pairs:q.length,edges,max_total_transversals:maxT,
 max_pairwise_disjoint:1,transversal_hist:hist};
 fs.writeFileSync(path.join(__dirname,'E063_INDEPENDENT_TRADE_COMPONENT_RESULT.json'),JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify(result));
}
calc();