#!/usr/bin/env node
'use strict';
const fs=require('fs'),assert=require('assert'),path=require('path');
const M=JSON.parse(fs.readFileSync(path.join(__dirname,'E061_near_triple.json'),'utf8')).squares;
const p=[0,2,3,1,5,6,4,8,9,7];
for(let k=0;k<3;k++){
 const S=M[k];let verified=0;
 for(let r=0;r<10;r++)for(let c=0;c<10;c++){
  assert.strictEqual(S[p[r]][p[c]],p[S[r][c]],`Egan ${k} row${r} col${c}`);
  verified++;
 }
 assert.strictEqual(verified,100);
}
// Nontrivial permutation p has disjoint cycles (1 2 3)(4 5 6)(7 8 9).
assert.notDeepStrictEqual(p,[...Array(10).keys()]);
let report={result:'NONTRIVIAL_AUTOTOPISM_VERIFIED_ON_EACH_EGAN_SQUARE',permutation:p,checked_cells_per_square:100,scope:'Egan published three squares; combine with McKay-Meynert-Myrvold 2007 theorem for existence impossibility if one such square lies in order10 triple'};
fs.writeFileSync(path.join(__dirname,'E063_SYMMETRY_WITNESS.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));