"use strict";
// Exact finite reference tools. Root problems remain OPEN unless full criteria hold.
function check(c,m){if(!c)throw Error(m);}
function verifyTriple(S){const n=S[0].length,T=Array.from({length:n},(_,i)=>i).join(",");
 check(S.length===3,"three squares required");
 for(const Q of S){check(Q.length===n,"height");for(const r of Q)check(r.length===n&&[...r].sort((a,b)=>a-b).join(",")===T,"row");
 for(let j=0;j<n;j++)check(Q.map(r=>r[j]).sort((a,b)=>a-b).join(",")===T,"column");}
 const pairs=[[0,1],[0,2],[1,2]].map(([a,b])=>new Set(S[a].flatMap((r,i)=>r.map((v,j)=>v*n+S[b][i][j]))).size);
 check(pairs.every(x=>x===n*n),"orthogonality");return pairs;
}
function residualGraph(w){
 const S=w.prefix,n=S[0][0].length,k=S[0].length,P=w.remaining_integer_placements;
 check(S.length===3&&k<n&&P.length===n*(n-k),"dimensions");
 const C=Array.from({length:3},()=>Array.from({length:n},()=>new Set()));
 const E=Array.from({length:3},()=>new Set()),pp=[[0,1],[0,2],[1,2]];
 const add=(col,v)=>{check(Number.isInteger(col)&&col>=0&&col<n,"column index");
 v.forEach((x,s)=>{check(Number.isInteger(x)&&x>=0&&x<n&&!C[s][col].has(x),"column resource");C[s][col].add(x);});
 pp.forEach(([a,b],i)=>{const x=v[a]*n+v[b];check(!E[i].has(x),"pair resource");E[i].add(x);});};
 for(const Q of S){check(Q.length===k,"height");for(const row of Q)check(row.length===n&&new Set(row).size===n&&row.every(v=>Number.isInteger(v)&&v>=0&&v<n),"partial Latin row");}
 for(let r=0;r<k;r++)for(let c=0;c<n;c++)add(c,S.map(Q=>Q[r][c]));
 for(const p of P){check(p.length===4,"placement tuple");add(p[0],p.slice(1));}
 check(C.flat().every(x=>x.size===n)&&E.every(x=>x.size===n*n),"incomplete six-resource cover");
 return {n,k,placements:P,graph:P.map((p,i)=>P.map((q,j)=>i!==j&&p.some((v,z)=>v===q[z])))};
}
function solve(G,K,limit=100000){let nodes=0;const c=Array(G.length).fill(-1);if(c.length)c[0]=0;
function dfs(){if(++nodes>limit)return{status:"UNKNOWN"};let v=-1,best=-1;for(let a=0;a<G.length;a++)if(c[a]<0){const sat=new Set(G[a].flatMap((e,b)=>e&&c[b]>=0?[c[b]]:[])).size;const key=sat*1000+G[a].filter(Boolean).length;if(key>best){best=key;v=a;}}if(v<0)return{status:"SAT",colors:c.slice()};const allowed=Array.from({length:K},(_,x)=>x).filter(x=>!G[v].some((e,b)=>e&&c[b]===x));const children=[];for(const x of allowed){c[v]=x;let r=dfs();c[v]=-1;if(r.status!=="UNSAT")return r;children.push({color:x,proof:r});}return{status:"UNSAT",vertex:v,children};}
return{...dfs(),nodes};}
function verifyColoring(G,K,c){check(Array.isArray(c)&&c.length===G.length,"color size");
 c.forEach(x=>check(Number.isInteger(x)&&x>=0&&x<K,"color range"));
 for(let a=0;a<G.length;a++)for(let b=a+1;b<G.length;b++)check(!G[a][b]||c[a]!==c[b],"edge colors");return true;}
function verifyUnsat(G,K,proof){
 const c=Array(G.length).fill(-1);if(c.length)c[0]=0;
 function replay(p){check(p.status==="UNSAT","not UNSAT node");const v=p.vertex;
 check(Number.isInteger(v)&&v>=0&&v<c.length&&c[v]===-1,"branch vertex");
 // Every still-allowed named color must have exactly one child; no heuristic trusted.
 const allowed=Array.from({length:K},(_,x)=>x).filter(x=>!G[v].some((e,b)=>e&&c[b]===x));
 check(Array.isArray(p.children)&&p.children.length===allowed.length,"missing branch");
 check(new Set(p.children.map(x=>x.color)).size===allowed.length,"duplicate branch");
 for(const x of p.children){check(allowed.includes(x.color),"invalid color branch");c[v]=x.color;replay(x.proof);c[v]=-1;}}
 check(G.length>0,"empty graph is colorable");replay(proof);return true;
}
function auditCore(w,result){const {graph:G}=residualGraph(w),ids=result.originalVertices;
 check(new Set(ids).size===ids.length&&ids.every(x=>Number.isInteger(x)&&x>=0&&x<G.length),"core IDs");
 const H=ids.map(a=>ids.map(b=>G[a][b]));
 check(JSON.stringify(H)===JSON.stringify(result.graph),"core graph differs");
 verifyUnsat(H,3,result.threeColor);verifyColoring(H,4,result.fourColor.colors);
 check(result.deletionControls.length===H.length,"deletion controls incomplete");
 check(new Set(result.deletionControls.map(x=>x.deletedVertex)).size===H.length,"duplicate deletion");
 for(const d of result.deletionControls){check(Number.isInteger(d.deletedVertex)&&d.deletedVertex>=0&&d.deletedVertex<H.length,"deletion index");
 const keep=H.map((_,i)=>i).filter(i=>i!==d.deletedVertex);
 verifyColoring(keep.map(a=>keep.map(b=>H[a][b])),3,d.result.colors);}
 return {vertices:H.length,edges:H.reduce((s,r)=>s+r.filter(Boolean).length,0)/2,
 chromaticNumber:4,vertexDeletionMinimal:true,globalMolsStatus:"OPEN",scope:"Only row factorization of the supplied exact integral residual cover"};
}
function vector(code,n){const v=[];for(let j=0;j<n;j++){v.push(code%3);code=Math.floor(code/3);}return v;}
function pack(v){let t=0,p=1;for(const x of v){t+=x*p;p*=3;}return t;}
function third(a,b){return a.map((x,i)=>(6-x-b[i])%3);}
function verifyCap(codes,n){check(new Set(codes).size===codes.length,"duplicate cap point");
 const N=3**n;check(codes.every(i=>Number.isInteger(i)&&i>=0&&i<N),"point range");
 const S=new Set(codes),v=codes.map(i=>vector(i,n));
 for(let i=0;i<v.length;i++)for(let j=i+1;j<v.length;j++)check(!S.has(pack(third(v[i],v[j]))),"collinear triple");return true;}
function capMaximum(n,nodeLimit=1000000){
 check(Number.isInteger(n)&&n>=1&&n<=7,"dimension 1..7");
 const N=3**n,V=Array.from({length:N},(_,i)=>vector(i,n)),chosen=[];
 let best=[],nodes=0,interrupted=false;
 function pop(x){let s=0;while(x){x&=x-1n;s++;}return s;}
 function dfs(mask){if(interrupted)return;if(++nodes>nodeLimit){interrupted=true;return;}
 if(chosen.length>best.length)best=chosen.slice();if(chosen.length+pop(mask)<=best.length)return;
 let i=0;while((mask&(1n<<BigInt(i)))===0n)i++;
 const rest=mask&~(1n<<BigInt(i));let live=rest;
 for(const j of chosen)live&=~(1n<<BigInt(pack(third(V[i],V[j]))));
 chosen.push(i);dfs(live);chosen.pop();dfs(rest);}
 dfs((1n<<BigInt(N))-1n);verifyCap(best,n);
 return {dimension:n,status:interrupted?"UNKNOWN_BUDGET":"EXHAUSTIVE_OPTIMUM",best:best.length,witness:best,nodes,
 scope:"All subsets in this dimension; no imposed symmetry",standaloneUnsatTrace:false};
}
function bruteCap2(){let best=0;for(let mask=0;mask<512;mask++){const P=[];for(let j=0;j<9;j++)if(mask>>j&1)P.push(j);
 // independent triple-sum checker, distinct from pair-blocking search
 let good=true;for(let a=0;a<P.length;a++)for(let b=a+1;b<P.length;b++)for(let c=b+1;c<P.length;c++){
 const A=[P[a]%3,Math.floor(P[a]/3)],B=[P[b]%3,Math.floor(P[b]/3)],C=[P[c]%3,Math.floor(P[c]/3)];
 if(A.every((x,i)=>(x+B[i]+C[i])%3===0))good=false;}
 if(good)best=Math.max(best,P.length);}return best;}
function buildOA(n){const tuples=[],resources=[];const m=10*n*n;
 for(let r=0;r<n;r++)for(let c=0;c<n;c++)for(let a=0;a<n;a++)for(let b=0;b<n;b++)for(let d=0;d<n;d++){
 if(r===0){if(a!==c||b!==c||d!==c)continue;}
 else if(a===c||b===c||d===c||a===b||a===d||b===d||(c===0&&a!==r))continue;
 const row=[r*n+c];[a,b,d].forEach((v,s)=>row.push(n*n+2*s*n*n+r*n+v,n*n+(2*s+1)*n*n+c*n+v));
 [[a,b],[a,d],[b,d]].forEach(([x,y],s)=>row.push(7*n*n+s*n*n+x*n+y));
 check(new Set(row).size===10&&row.every(x=>x>=0&&x<m),"resource encoding");tuples.push([r,c,a,b,d]);resources.push(row);}
 return {n,tuples,resources,equalities:m};
}
function solveOA(n,nodeLimit=100000){const M=buildOA(n),used=Array(M.equalities).fill(false),inc=Array.from({length:M.equalities},()=>[]);
 M.resources.forEach((row,j)=>row.forEach(x=>inc[x].push(j)));const chosen=[];let nodes=0,unknown=false,witness=null;
 function dfs(){if(++nodes>nodeLimit){unknown=true;return false;}if(chosen.length===n*n){witness=chosen.slice();return true;}
 let candidates=null;for(let r=0;r<inc.length;r++)if(!used[r]){const options=inc[r].filter(j=>M.resources[j].every(x=>!used[x]));
 if(options.length===0)return false;if(candidates===null||options.length<candidates.length)candidates=options;if(candidates.length===1)break;}
 for(const j of candidates){chosen.push(j);M.resources[j].forEach(x=>used[x]=true);if(dfs())return true;
 M.resources[j].forEach(x=>used[x]=false);chosen.pop();if(unknown)return false;}return false;}
 dfs();const result={n,options:M.tuples.length,equalities:M.equalities,nodes,status:witness?"SAT":unknown?"UNKNOWN_BUDGET":"UNSAT_EXHAUSTIVE",standaloneUnsatTrace:false};
 if(witness){const S=Array.from({length:3},()=>Array.from({length:n},()=>Array(n).fill(-1)));
 for(const j of witness){const [r,c,a,b,d]=M.tuples[j];[a,b,d].forEach((v,s)=>S[s][r][c]=v);}
 result.overlays=verifyTriple(S);result.witness=S;}return result;
}
function expectReject(f){let rejected=false;try{f();}catch(e){rejected=true;}check(rejected,"negative control accepted");return true;}
const api={residualGraph,solve,verifyColoring,verifyUnsat,auditCore,capMaximum,bruteCap2,verifyCap,buildOA,solveOA,verifyTriple,expectReject};
if(typeof module!=="undefined")module.exports=api;
