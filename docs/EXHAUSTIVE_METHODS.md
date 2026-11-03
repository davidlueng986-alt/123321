# 完整窮舉與「包圍」：即使遠超十億年也列出
2026-11-03。根目標依 [MISSION.md](MISSION.md)；沒有任何新 solved 聲明。

## 完整性與時間是兩件事
MOLS10 與 F3^7 Cap Set 都是固定有限問題，因此有保證數學上終止的暴力方法。
實際程式仍會受記憶體、stack、整數表示、checkpoint等工程限制；不宣稱一個runtime能跑到天荒地老。
有限且完整不等於實用、分支少不等於更快；本批沒有可信主問題 ETA。

下表是假設每秒完整檢查 10^12 個候選的「全掃規模換算」，故意極度樂觀；
不是實測walltime、最佳演算法時間下界，也不是剪枝後預測。每年採31557600秒。

| 空間 | 候選數 | 該假設下全掃年數 |
|---|---:|---:|
| 三個10×10符號矩陣 | 10^300 | 3.17×10^280 |
| 三首行正規化後的row permutations | (10!)^27 ≈1.299×10^177 | 4.12×10^157 |
| full normalized OA的100選項子集粗界 | C(41338,100)≈4.10×10^303 | 1.30×10^284 |
| F3^7全部子集 | 2^2187≈2.252×10^658 | 7.14×10^638 |
| F3^7只枚舉237點集合 | C(2187,237)≈2.017×10^324 | 6.39×10^304 |

OA子集粗界比row-permutation粗界更大，不表示OA solver更慢；
表示法的有效性在於constraint propagation，不能只比較這些粗候選數。

## MOLS10：三種完整路線
### A. 全部row permutations
先獨立重標記三個方陣的symbols，令每個row0都是identity。
之後對每個row位置，枚舉三個permutations；column有重複或任一pair overlay重複便停止該branch。
沒有重複的partial state保留全部合法後續。深度10找到完整原物件即證存在；
全部分支耗盡才證不存在。partial high score不是完成百分比。
覆蓋依據是任何原解均可合法重標記到此空間，不固定歷史A/B。

### B. 完整五座標exact cover / Algorithm X
每個選項(r,c,a,b,d)覆蓋十個resources：
cell(r,c)、三方陣各自row-symbol與column-symbol共六類、三組pair-symbol。
每個resource恰一次，等價於完整3-MOLS。選最少候選resource窮舉其所有選項；
這只是選路heuristic，不丟分支。節點budget耗盡必須UNKNOWN。
本批finite_tools.js實作此完整模型；n10有41338選項／1000等式。
n3完整UNSAT、n4/n5真實SAT控制已執行；沒有n10解或全域UNSAT。

### C. 完整SAT / CP + proof-carrying split
全部constraints必須包含row coordinate。可直接解全模型，
或按已證12種f／162959個(f,g)frontier分片，但C與全部continuations必須完整。
SAT解碼三個矩陣並獨立查100/100/100。
UNSAT要有proof trace、原解=>編碼解的橋樑、全部assumptions與分片覆蓋。
任一條件缺失仍UNKNOWN；solver本身回UNSAT不是無條件主結論。

### 精確配對窮舉的另一種分解
枚舉所有正交A/B，再對每對求共同transversal exact partition。
E061的n-1 packing或n-2 packing加二色residual是精確closure criterion。
枚舉一個固定Egan pair不覆蓋其他pair；全部pairs的完整分類仍可能天文昂貴。

## Cap Set：三種完整路線
### A. 全部子集include/exclude
每個點二選一；若選x,y，強制排除第三點−x−y。
「已選數+尚可選數 <= incumbent」是安全upper bound，可停止該節點。
全域最大搜索完成後，incumbent見證和完整剩餘排除共同確定exact值。
finite_tools.js提供dimension<=7的一般reference implementation；本批只完整跑n2,n3。
預設有限node budget；只有返回EXHAUSTIVE_OPTIMUM才是該dimension完整搜尋。

### B. 門檻E(k)
E(k)=存在至少k點cap。可以枚舉全部k-subsets，或用include/exclude。
若E(k)為假，更大集合也不可能，因cap性質對子集遺傳。
有236真實構造時，¬E(237)就令exact236 CLOSED；E(237)只提高lower。
在保守[236,2187]範圍用至多11次threshold decisions可二分exact值，
但每個decision都可能極慢，這不是11次便很容易的聲明。

### C. 全域SAT與已證框架覆蓋
直接2187點Boolean變數、每條3AP禁止三點全選、at-least-k counter。
可以不用任何外部cap分類就編碼完整有限空間。
採CAP040 dense-H十分支時，另依賴moment>=89及低維界的適用性，
且必須保留全部十葉。固定CAP027 occupancy只是一條條件性問題，
其UNSAT不推出所有285cap不存在。H09的35 forced zeros不能刪除該分支。

## 「包圍」如何加在完整枚舉上
每項增強都須先給安全性證明，再量測效果：
1. 對稱：每個原解至少有一個代表；不要用喜歡的對稱當WLOG。
2. universal cuts：所有原解均滿足，失敗可排除整個subtree。
3. 可重用obstruction：經已驗證的嵌入，將固定core提升成一類候選的排除。
4. 分支上界：只在已證不可能超過incumbent時剪掉。
5. 合併等價子問題：memo key必須包含決定continuation的全部資訊。
6. checkpoint與分散式：manifest覆蓋、hash、無漏分片；分散本身不減少總工作。
7. 對每個新增cut做正控制、負控制、同模型等budget比較；不用僅node數宣稱speedup。
不保證存在小型obstruction或短證明。找不到就保留原完整方法，不改成抽樣後宣稱全域結論。

## frontier-attack：只列方法邊界，本次不執行
- HN：枚舉有限graphs，對每個做k-colouring與平面unit-distance可實現性判定；
  固定graph的real polynomial existential問題可判定。
  由緊緻性，平面不可k色有有限見證；此方向可半判定。若平面可k色，
  這個無界graph枚舉不保證停止，不能因久未找到便證可色。
- 平面JC：逐degree建立係數及碰撞的complex polynomial方程，非零條件可用auxiliary inverse。
  每個固定degree的代數可行性可判定；degree無已證上界時，
  全部低degree無反例不推出全域JC。此處是collision-disproof route，非全域決定法。
- BSD：曲線可以枚舉，但「對每條曲線總能取得嚴格rank與analytic-order證書」
  不是已建立的通用假設；不可把無界曲線掃描描述為保證終止的雙向解法。
- 在可枚舉形式系統中dovetail搜尋P/¬P證明只能覆蓋其中可證的命題；
  不假設某固定形式系統對所有真命題完整。

這些半判定路線與MOLS10／CAP7的固定有限全枚舉有本質分別。
