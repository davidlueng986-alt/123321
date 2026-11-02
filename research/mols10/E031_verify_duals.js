// Standalone Node.js exact verifier, no optimizer or dependency on Python code.
// Reads E031_DUAL_CERTIFICATES.json from argv[2]. Integer arithmetic after
// multiplying all rational weights by the LCM of denominators (here 1 or 2).
const fs=require('fs');
const filename=process.argv[2]||'E031_DUAL_CERTIFICATES.json';
const certs=JSON.parse(fs.readFileSync(filename,'utf8'));
function gcd(a,b){while(b){[a,b]=[b,a%b]}return a}
function lcm(a,b){return a/gcd(a,b)*b}
function verify(D){
 if(D.status!=='EXACT_RATIONAL_DUAL')throw Error('wrong status');
 const S=D.source_squares,n=D.n,k=S[0].length;
 if(S.length!==3||S.some(A=>A.length!==k))throw Error('shape');
 for(const A of S){
  for(const row of A)if(row.length!==n||new Set(row).size!==n||row.some(x=>x<0||x>=n))throw Error('not row Latin');
  for(let c=0;c<n;c++)if(new Set(A.map(r=>r[c])).size!==k)throw Error('not column partial Latin');
 }
 const axes=[[0,1],[0,2],[1,2]], remaining=[];
 for(let p=0;p<3;p++){
  const [s,t]=axes[p],seen=new Set();
  for(let r=0;r<k;r++)for(let c=0;c<n;c++){
   const z=`${S[s][r][c]},${S[t][r][c]}`;
   if(seen.has(z))throw Error('duplicate pair in partial');seen.add(z)
  }
  const miss=new Set();
  for(let a=0;a<n;a++)for(let b=0;b<n;b++){
   const z=`${a},${b}`;if(!seen.has(z))miss.add(z)
  }
  remaining.push(miss)
 }
 const den=D.certificate.reduce((v,z)=>lcm(v,z.denominator),1), weight=new Map();
 for(const w of D.certificate){
  const p=axes.findIndex(a=>a[0]===w.pair_axis[0]&&a[1]===w.pair_axis[1]);
  if(p<0)throw Error('axis');
  const key=`${p}:${w.edge.join(',')}`;
  if(!remaining[p].has(w.edge.join(','))||weight.has(key))throw Error('bad certificate support');
  if(den%w.denominator)throw Error('non-integer scaling');
  weight.set(key,w.numerator*(den/w.denominator));
 }
 const sum=[...weight.values()].reduce((a,b)=>a+b,0);
 if(sum<=0||sum*D.dual_sum[1]!==D.dual_sum[0]*den)throw Error('nonpositive dual');
 let checked=0;
 for(const ab of remaining[0]){
  const [a,b]=ab.split(',').map(Number);
  for(let c=0;c<n;c++){
   const ac=`${a},${c}`,bc=`${b},${c}`;
   if(!remaining[1].has(ac)||!remaining[2].has(bc))continue;
   const val=(weight.get(`0:${ab}`)||0)+(weight.get(`1:${ac}`)||0)+(weight.get(`2:${bc}`)||0);
   if(val>0)throw Error(`dual triangle violated ${a},${b},${c}: ${val}`);
   checked++;
  }
 }
 if(checked!==D.candidate_triples)throw Error('triple count mismatch');
 return {sample:D.sample_index,order:n,fixed_rows:k,checked_triangles:checked,dual_sum:D.dual_sum.join('/'),passed:true}
}
console.log(JSON.stringify(certs.map(verify),null,2));
