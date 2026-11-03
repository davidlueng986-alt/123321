"use strict";
const fs=require("node:fs"),path=require("node:path"),assert=require("node:assert/strict");
const api=require("./finite_tools.js");
const read=name=>JSON.parse(fs.readFileSync(path.join(__dirname,name),"utf8"));
const fixture=read("row_cover_fixture.json"),core=read("row_cover_core.json");
const report={cap2:api.capMaximum(2),cap2Independent:api.bruteCap2(),cap3:api.capMaximum(3,2000000),
 oa3:api.solveOA(3),oa4:api.solveOA(4),oa5:api.solveOA(5),core:api.auditCore(fixture,core)};
report.oa10Options=api.buildOA(10).tuples.length;
report.negativeControls={
 corruptProof:api.expectReject(()=>{const r=JSON.parse(JSON.stringify(core));r.threeColor.children=[];api.auditCore(fixture,r);}),
 badCover:api.expectReject(()=>{const w=JSON.parse(JSON.stringify(fixture));w.remaining_integer_placements[0]=w.remaining_integer_placements[1];api.residualGraph(w);}),
 badCap:api.expectReject(()=>api.verifyCap([0,1,2],2))};
assert.deepStrictEqual(report,read("expected_results.json"));
console.log(JSON.stringify({status:"EXACT_BATCH_REPLAY_PASS",rootMols:"OPEN",rootCap7:"OPEN",report},null,2));
