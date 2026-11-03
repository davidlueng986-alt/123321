"use strict";
const fs=require("node:fs"),path=require("node:path"),assert=require("node:assert/strict");
const {execFileSync}=require("node:child_process");
const {verifyCut}=require("./verify_normalized_cut.js");
const {solveOA,violatesNogood}=require("./finite_tools.js");
function loadVerifiedCut(){
  // Fail closed: never use the learned clause if its independent premise checker fails.
  execFileSync("python3",[path.join(__dirname,"verify_forced_prefix.py")],{timeout:60000,stdio:["ignore","pipe","pipe"]});
  const read=name=>JSON.parse(fs.readFileSync(path.join(__dirname,name),"utf8"));
  const cut=read("normalized_oa_cut.json");
  verifyCut(read("row_cover_fixture.json").prefix,read("forced_prefix_certificate.json"),cut);
  return cut;
}
if(require.main===module){
  const cut=loadVerifiedCut();
  assert.equal(cut.n,10);
  const all=new Set(cut.clause.map(x=>-x));
  assert.ok(violatesNogood(all,cut.clause));
  all.delete(-cut.clause[0]);assert.ok(!violatesNogood(all,cut.clause));
  const budget=16; // Smoke test only, not a claim about runtime or closed branches.
  const baseline=solveOA(10,budget),withCut=solveOA(10,budget,[cut.clause]);
  assert.equal(baseline.status,"UNKNOWN_BUDGET");assert.equal(withCut.status,"UNKNOWN_BUDGET");
  assert.equal(baseline.nodes,withCut.nodes);assert.equal(withCut.learnedPrunes,0);
  console.log(JSON.stringify({status:"CERTIFIED_NOGOOD_INTEGRATION_PASS",budget,baseline,withCut,
    observedSpeedup:false,rootStatus:"OPEN"},null,2));
}
module.exports={loadVerifiedCut};
