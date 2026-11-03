#!/usr/bin/env node
'use strict';
// Independently validates positive full 5-coordinate OA certificates and
// structural experiment metadata. It does NOT independently replay all 84
// UNSAT search trees; run E060_all_six_row_extensions.py for that.
const fs=require('fs'),path=require('path');
const dir=__dirname,assert=(c,m)=>{if(!c)throw Error(m)};
const milp=JSON.parse(fs.readFileSync(path.join(dir,'E060_GLOBAL_OA_MILP_RESULTS.json')));
for(const rec of milp){if(rec.status==='SAT'){
 let squares=rec.witness,n=rec.n;assert(squares.length===3,'square count');
 let T=new Set(Array.from({length:n},(_,i)=>i));
 for(const Q of squares){assert(Q.length===n,'rows');
  for(let r of Q)assert(r.length===n&&new Set(r).size===n&&r.every(v=>T.has(v)),'invalid Latin row');
  for(let c=0;c<n;c++)assert(new Set(Q.map(row=>row[c])).size===n,'Latin col')}
 for(const [a,b] of [[0,1],[0,2],[1,2]]){
  let e=new Set();for(let r=0;r<n;r++)for(let c=0;c<n;c++)e.add(squares[a][r][c]+','+squares[b][r][c]);
  assert(e.size===n*n,'non-orthogonal');}
 }else assert(rec.status==='UNKNOWN_BUDGET'||rec.status==='UNSAT_EXHAUSTIVE','bad status');}
assert(milp.some(r=>r.n===10&&r.status==='UNKNOWN_BUDGET'),'no order10 budget record');
const z=JSON.parse(fs.readFileSync(path.join(dir,'E060_ALL_84_SIX_ROW_RESULTS.json')));
assert(z.anchors===84&&z.results.length===84&&z.unknown===0,'incomplete anchored runs');
let uniq=new Set();let total=0;
for(const r of z.results){assert(r.status==='UNSAT_FIXED_SIX_ROWS','incomplete anchor');
 let key=r.omitted.join(',');assert(!uniq.has(key),'duplicate');uniq.add(key);
 assert(r.finished===r.seventh_row_triples&&r.unknown===0,'unsearched seventh row');
 assert(r.pair_candidates.length===3&&r.pair_candidates.every(x=>Number.isInteger(x)),'bad pair stats');
 total+=r.seventh_row_triples}
assert(total===431,'unexpected aggregate');
console.log(JSON.stringify({status:'VALIDATED_METADATA_AND_FULL_SAT_WITNESSES',full_order4_5:milp.filter(x=>x.status==='SAT').map(x=>({n:x.n,overlays:x.overlays})),order10:milp.find(x=>x.n===10)?.status,anchored_case_count:84,seven_row_extensions_checked:total,caveat:'UNSAT proof requires re-running Python enumerator; metadata check alone is NOT an independent UNSAT verifier'}));