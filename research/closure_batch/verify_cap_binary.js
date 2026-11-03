"use strict";
// Direct numeric base-3 arithmetic; imports neither the Python generator nor cap research code.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
function third(a,b) {
  let out=0,power=1;
  for(let i=0;i<7;i++){out+=((6-a%3-b%3)%3)*power;a=Math.floor(a/3);b=Math.floor(b/3);power*=3;}
  return out;
}
function verify(report) {
  assert.equal(report.schema,"ten-leaf-binary-countermodels-v1");
  assert.equal(report.root_cap7_status,"OPEN");
  const frame = new Set([0,...Array.from({length:7},(_,i)=>3**i)]);
  const invalid = new Set(frame);
  for(const a of frame)for(const b of frame)if(a<b)invalid.add(third(a,b));
  const groups = new Map();
  for(let p=0;p<2187;p+=3)if(!invalid.has(p)){
    let q=p,digits=[];for(let i=0;i<7;i++){digits.push(q%3);q=Math.floor(q/3);}
    const sum=digits.reduce((a,b)=>a+b,0),lam=[((1-sum)%3+3)%3,...digits.slice(1)];
    const tag=[0,...[0,1,2].map(x=>lam.filter(v=>v===x).length)].join(",");
    if(!groups.has(tag))groups.set(tag,[]);groups.get(tag).push(p);
  }
  const keys=[...groups.keys()].sort();assert.equal(keys.length,10);
  assert.equal([...groups.values()].reduce((s,v)=>s+v.length,0),701);
  assert.equal(report.cases.length,10);
  for(let branch=0;branch<10;branch++){
    const item=report.cases[branch],orbit=groups.get(keys[branch]);
    assert.equal(item.branch,branch);assert.equal(item.orbit_tag.join(","),keys[branch]);
    assert.equal(item.orbit_size,orbit.length);assert.equal(item.ninth_point,orbit[0]);
    const selected=new Set([...frame,item.ninth_point]);
    assert.deepEqual(item.selected_frame_codes,[...selected].sort((a,b)=>a-b));
    function checkPointSet(free){
      const all=[...selected,...free],set=new Set(all);
      assert.equal(set.size,all.length);
      assert.ok(all.every(x=>Number.isInteger(x)&&x>=0&&x<2187));
      // Every full-model 3AP with at least one fixed selected point is forbidden.
      // This covers both binary clauses and all secant-forced zeros without trusting a clause list.
      for(const s of selected)for(const p of all)if(p!==s)assert.ok(!set.has(third(s,p)),"binary/unit violation");
      return all;
    }
    const greedy=checkPointSet(item.greedy_free_codes);
    assert.ok(greedy.length>=237&&greedy.filter(x=>x%3===0).length>=89);
    const threshold=checkPointSet(item.threshold_free_codes);
    assert.equal(threshold.length,237);assert.equal(threshold.filter(x=>x%3===0).length,89);
    assert.ok(item.threshold_free_codes.every(p=>item.greedy_free_codes.includes(p)));
    const triple=item.violated_full_model_ternary;
    assert.equal(new Set(triple).size,3);
    assert.ok(triple.every(p=>item.threshold_free_codes.includes(p)));
    assert.equal(third(triple[0],triple[1]),triple[2]);
    assert.equal(item.full_root_status,"UNKNOWN");
  }
  return {status:"ALL_TEN_BINARY_COUNTERMODELS_VERIFIED",actualCaps:false,root:"OPEN"};
}
if(require.main===module){
  const report=JSON.parse(fs.readFileSync(path.join(__dirname,"cap_binary_countermodels.json"),"utf8"));
  console.log(JSON.stringify(verify(report)));
  const clone=x=>JSON.parse(JSON.stringify(x));
  const bad=clone(report);bad.cases[0].threshold_free_codes[0]=bad.cases[0].selected_frame_codes[0];
  assert.throws(()=>verify(bad));
  const badLine=clone(report);badLine.cases[0].violated_full_model_ternary[2]=-1;
  assert.throws(()=>verify(badLine));
  const missing=clone(report);missing.cases.pop();assert.throws(()=>verify(missing));
  console.log("3_CAP_COUNTERMODEL_MUTATIONS_REJECTED");
}
module.exports={verify};
