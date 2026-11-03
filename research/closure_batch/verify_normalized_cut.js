"use strict";
// Independent bridge to the existing unrestricted, normalized full-OA numbering.
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const {buildOA} = require("./finite_tools.js");

function verifyCut(prefix, proof, cut) {
  const n = prefix[0][0].length;
  const hash = crypto.createHash("sha256").update(JSON.stringify(prefix)).digest("hex");
  assert.equal(cut.prefix_sha256, hash);
  assert.equal(proof.prefix_sha256, hash);
  assert.equal(proof.status, "NO_COMPLETION_OF_THIS_PREFIX");
  assert.equal(cut.n, n);
  assert.equal(cut.numbering, "finite_tools.buildOA(n).tuples index + 1");
  // Independent symbol bijections induced by the three first rows.
  const maps = prefix.map(Q => new Map(Q[0].map((value, col) => [value, col])));
  const labels = prefix[0].map(row => maps[0].get(row[0]));
  assert.equal(new Set(labels).size, prefix[0].length);
  assert.deepEqual(labels, cut.physical_to_normalized_row);
  const model = buildOA(n);
  const lookup = new Map(model.tuples.map((p, i) => [p.join(","), i+1]));
  const tuples = [], literals = [];
  for (let row = 0; row < prefix[0].length; row++) {
    for (let col = 0; col < n; col++) {
      const tuple = [labels[row], col, ...prefix.map((Q, s) => maps[s].get(Q[row][col]))];
      const id = lookup.get(tuple.join(","));
      assert.ok(id, "Every normalized assumption must be an actual model option");
      if (labels[row] !== 0) { tuples.push(tuple); literals.push(-id); }
    }
  }
  assert.deepEqual(cut.normalized_tuples, tuples);
  assert.deepEqual(cut.clause, literals);
  assert.equal(new Set(literals).size, literals.length);
  return {options: model.tuples.length, clauseLength: literals.length,
    scope: "Guarded exclusion of this exact normalized partial assignment", rootStatus: "OPEN"};
}

if (require.main === module) {
  const read = name => JSON.parse(fs.readFileSync(path.join(__dirname, name), "utf8"));
  // This stage does not substitute for the separate mathematical certificate checker.
  console.log(JSON.stringify(verifyCut(read("row_cover_fixture.json").prefix,
    read("forced_prefix_certificate.json"), read("normalized_oa_cut.json"))));
}
module.exports = {verifyCut};
