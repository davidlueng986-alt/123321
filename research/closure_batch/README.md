# Closure batch 2026-11-03：可重用row-factorization障礙與完整有限後備法

更新：[第二批報告](FORCED_PREFIX_REPORT.md) 已將固定cover障礙提升到完整指定prefix的排除，
加入已驗證的60-literal normalized OA nogood及root搜尋介面，並對Cap十分支提供binary-only
relaxation的明確SAT countermodels。主問題仍OPEN；沒有已量測的root加速。
**根狀態：3-MOLS(10) OPEN；exact r3(7) OPEN。**
本批的局部答案及控制不構成主問題成功。核心規約見 [MISSION](../../docs/MISSION.md)。

## 新的精確局部問題：固定residual cover能否補成缺失行？
輸入源：E059_INTEGRAL_K7_WITNESS.json，
GitHub blob b3e6711ad78a8dc912e2b6c3d94d1a6994895478（歷史Egan–Wanless配對來源，見E059）。
本批複製為row_cover_fixture.json，保留其來源與scope。
七個已固定行後剩30個placements (column,A,B,C)，完整覆蓋180個六類資源。
先從原prefix重建used resources，再加入placements，逐項驗證無重複／無缺失。

**一般lemma。** 給合法k-row prefix和某個完整整數residual cover。
令q=n-k，建立placements conflict graph：同column或任一square-symbol相同便連邊。
此固定cover可分配為q個完整合法缺失行 iff conflict graph可q色。
必要方向：同一行不能共享任何上述資源。
充分方向：每個column有q個placements，彼此成clique，故q色時每色每column恰一個；
每色有n個點，三個symbols各不重複，因此每行皆permutation。
六類cover已保證column與pair不重複，故得到完整MOLS。
這個lemma不宣稱每個前綴只有這一個residual cover。

## 本批結果與可移植證書
- 完整30點conflict graph有120邊，不可3色。
- 抽出12點22邊induced core；原placement indices（0-based）：
  15,17,18,19,20,21,22,24,25,26,27,28。
- 33-node完整分支證書證其不可3色；一個4色見證證χ=4。
- 對每個單點刪除，附一個合法3色見證，故為vertex-deletion-minimal；
  **不是全圖大小最小core或新文獻紀錄的聲明**。
- checker不信任DSATUR選點：逐node查vertex未賦值、全部允許colors恰有一個child、
  終端的確無允許color。先固定vertex0為color0是全域顏色重命名對稱，
  每個可能著色都可如此重命名，無漏解。
- 破壞proof、重複placement及錯誤cap三個negative controls皆被拒絕。

此core可作模板：若另一個固定cover的row-conflict graph含它的已驗證injective
subgraph embedding，同樣不能分成三行。尚未測試其他covers的命中率／marginal pruning。
**不能據此說整個七行prefix不可延伸**，因為可能存在其他residual covers。
所以本批關閉的只是這份cover的factorization問題；global orbits closed仍0。

## 完整有限reference implementations及控制
finite_tools.js實作：
- 全五座標十類資源OA exact-cover回溯（不固定歷史pair）。
- 無額外對稱的cap include/exclude與remaining-count安全bound。
- 原物件獨立檢查、graph color proof replay及core核對。
- 9點平面全部512 subsets的獨立triple-sum掃描。

實際在V8執行與發佈同一份pure-JavaScript函式，deterministic、無seed：
| 控制 | 結果 |
|---|---|
| cap dimension2 | 完整最優4；119 nodes；獨立512-subset掃描也得4 |
| cap dimension3 | 完整最優9；75573 nodes；附合法9點見證 |
| 3-MOLS order3 | 完整UNSAT；4 nodes |
| 3-MOLS order4 | SAT；17 nodes；16/16/16 |
| 3-MOLS order5 | SAT；28 nodes；25/25/25 |
| normalized full OA order10 | 41338選項、1000等式；只核對模型規模，未執行全搜尋 |
| row cover core | χ=4，12點22邊，全部12個單點刪除3色控制 |
| 根問題 | 仍OPEN，無新的237cap或100/100/100 |

小階EXHAUSTIVE結果是供獨立完整重跑的枚舉，不附通用formal UNSAT trace；
不可把known small cases的重現當新數學突破。大問題若node budget耗盡必回UNKNOWN_BUDGET。
本批全n7/fulln10枚舉未執行，也不因有限性聲稱可實用。

## 重播
需要Node.js 18+，無npm依賴：
```bash
node research/closure_batch/run_batch.js
```
runner重新取得全部控制、獨立核對core證書，與expected_results.json逐欄比較。
在目前executor沒有shell的情況下，函式已在V8 isolate執行；
此Node CLI wrapper尚待GitHub Actions獨立重播，不能預先聲稱CI GREEN。

檔案：
- finite_tools.js：完整reference搜尋與獨立checkers。
- row_cover_fixture.json：既有exact integral cover。
- row_cover_core.json：33-node證書、4色見證、全部12個deletion-colorings。
- expected_results.json：本次實際輸出快照；不是自行認證主結論。
- run_batch.js：重跑與snapshot比對。

## 與既有批次關係
上一個local環境的E059/E060、CAP034、CAP040–042重播及有界SAT pilot結果
已在對話記錄，這裡不杜撰遺失的raw logs。
當時兩個根SAT pilots均UNKNOWN，沒有排除完整分支。
E060腳本多餘右括號的修正需在原分支檢查最新檔案後再套用，
不以本批檔案覆蓋其他人的新修正。

本批發布改變的是方法、局部證據與程式；唯一成功目標仍是主問題OPEN→CLOSED。
