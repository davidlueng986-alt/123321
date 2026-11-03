# Math research branches

2026-11-03：此文件是導覽，不是研究內容已合併 main 的聲明。

- MOLS10: `math-agent-mols10`，資料在 `research/mols10/`；完成條件為完整100/100/100見證，或完整無解證明及覆蓋。
- Cap Set: `research/capset-f3-7`，資料在 `research/capset_f3_7/`；完成條件為 exact r3(7)，上下界相等。
- 共用方法、24項局部問題及完整窮舉：各研究branch的 `docs/MISSION.md`、`docs/LOCAL_PROBLEM_CATALOG.md`、`docs/EXHAUSTIVE_METHODS.md`。
- 可重播有限控制與row-factorization證書：各研究branch的 `research/closure_batch/`。
- `math-agent-lean-verifier` 是驗證workspace，不表示任何open problem已解。
- 另一個repo [frontier-attack](https://github.com/davidlueng986-alt/frontier-attack) 的HN、JC、BSD是獨立主題；不能用一題的局部結果代替另一題的根結論。

## Checkout 與重播
```bash
git clone https://github.com/davidlueng986-alt/123321.git
cd 123321
git switch math-agent-mols10
node research/closure_batch/run_batch.js
# 或 git switch research/capset-f3-7
```
請以branch的最新README與STATE為準；CI通過只代表列出的checks，不自動變更主狀態。
main 的FinSight程式與歷史沒有因導覽更新而被替換或合併研究碼。
