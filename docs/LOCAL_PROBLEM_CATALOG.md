# 局部問題總目錄：服務主問題 OPEN → CLOSED

2026-11-03；本輪已識別的全部 24 項，不聲稱窮盡數學上一切可能局部問題。
唯一成功條件見 [MISSION.md](MISSION.md)。MOLS來源以 E061 為最新已讀報告；Cap以 CAP043 為最新已讀報告。
這是研究候選清單，不是同時啟動所有昂貴工作。先使用已知反例停止錯誤捷徑，再批次處理彼此獨立的關口。
狀態 REPORTED／PARTLY_ANSWERED 不等於本批獨立認證全部舊結果。

## M01 — 固定 Egan 指定兩方陣，只改第三個是否可能達到 100？

- 主線／parent：MOLS10／MOLS_EXISTS_OR_NOT
- 範圍：指定固定配對
- 驗收與方法：已有 E008/E010 精確上限 91 與 attaining witness。
- 現況：ANSWERED_NO
- 對 CLOSED 的作用：關閉該單方陣修補族；不排除任意新配對。
- 決策／下一步：保留證書，停止同族掃描。
- 既有證據索引（非一律本批重播）：`E008_E011_OPTIMALITY_PROOFS.md`

## M02 — 合法 k4/k7 前綴的六類 residual LP／整數 cover 是否必不可行？

- 主線／parent：MOLS10／MOLS_EXISTS_OR_NOT
- 範圍：column-symbol 與 pair-symbol 六類資源，缺 row 座標
- 驗收與方法：E059 精確 fractional 及 integral 見證。
- 現況：REFUTED
- 對 CLOSED 的作用：關閉 universal residual-infeasibility 捷徑；必須處理 row factorization。
- 決策／下一步：使用反例作模型負控制，不再堆同類 Farkas dual。
- 既有證據索引（非一律本批重播）：`E059_STRATEGY_REVISION.md`

## M03 — LP、unit、Hall、integral cover 哪些有額外排除力？

- 主線／parent：MOLS10／MOLS_EXISTS_OR_NOT
- 範圍：同一批已固定 input；pair-only 與 six-resource 分開
- 驗收與方法：等 walltime、相同分支順序、相同候選；量測邊際排除與成本。
- 現況：PARTLY_ANSWERED
- 對 CLOSED 的作用：移除被廉價方法涵蓋的昂貴步驟；不能推廣樣本比例。
- 決策／下一步：E031 的指定 12 例已被 unit 涵蓋；其餘需配對 benchmark。
- 既有證據索引（非一律本批重播）：`E032_REPORT.md`

## M04 — 很多失敗是否可由同一小型障礙解釋？

- 主線／parent：MOLS10／MOLS_EXISTS_OR_NOT
- 範圍：明列 pair-only core 或 full row-conflict core，不能混用
- 驗收與方法：對 core 給精確 UNSAT、最小性控制、合法嵌入推導。
- 現況：PARTLY_ANSWERED
- 對 CLOSED 的作用：可將整類候選安全剪枝；單一 core 不保證所有失敗都相同。
- 決策／下一步：87-edge core 的純線性 GF2 捷徑已失效；優先有 row 座標的可重用障礙。
- 既有證據索引（非一律本批重播）：`E032_REPORT.md`

## M05 — 對稱分類是否完整且沒有重複工作？

- 主線／parent：MOLS10／MOLS_EXISTS_OR_NOT
- 範圍：完整三方陣合法重標記與 partial frontier
- 驗收與方法：審核 normalizer 和 centralizer、輸出代表 manifest、證每個原解有代表。
- 現況：OPEN
- 對 CLOSED 的作用：完整覆蓋後才能把分支 UNSAT 合併到主命題。
- 決策／下一步：162959 僅是 A/B 二行 frontier；C 與全部後續不可遺漏。
- 既有證據索引（非一律本批重播）：`E033_REPORT.md`

## M06 — 固定 integral residual cover 是否能分配到缺失行？

- 主線／parent：MOLS10／MOLS_EXISTS_OR_NOT
- 範圍：一個固定 cover 的 placements；不是全部 covers
- 驗收與方法：衝突圖：同 column 或任一 square-symbol 連邊；精確 q=n-k 著色及證書 replay。
- 現況：ANSWERED_FOR_FIXTURE
- 對 CLOSED 的作用：把 relaxation 到完整 Latin rows 的缺口變成可判定義務。
- 決策／下一步：本批得到 k7 cover 的 12點22邊 vertex-critical 4-chromatic core；只能排除該 cover。
- 既有證據索引（非一律本批重播）：`../closure_batch/README.md`

## M07 — 新正交配對能否找到 8 個 disjoint common transversals 且殘圖二色？

- 主線／parent：MOLS10／MOLS_EXISTS_OR_NOT
- 範圍：指定任意新 A/B 配對；枚舉配對才有全域覆蓋
- 驗收與方法：E061：n-2 packing 加 residual bipartite 或 n-1 packing 自動補全。
- 現況：OPEN
- 對 CLOSED 的作用：成功直接產生第三方陣；固定 Egan max7 不推及其他配對。
- 決策／下一步：尋找新 pair species／conflict learning，不重複已耗盡 Egan 配對。
- 既有證據索引（非一律本批重播）：`E061_REPORT.md`

## M08 — 完整五座標 OA 模型是否精確、可重播，如何降低搜尋？

- 主線／parent：MOLS10／MOLS_EXISTS_OR_NOT
- 範圍：全部 normalized triples，十類資源
- 驗收與方法：每個原解映成 exact cover、任一 cover decode 並檢查三個 overlays；小階正負控制。
- 現況：IMPLEMENTED_CONTROLS_PASS
- 對 CLOSED 的作用：是有限完整解法；UNKNOWN 不關閉任何分支。
- 決策／下一步：本批獨立 reference implementation；n10 有41338選項1000等式。
- 既有證據索引（非一律本批重播）：`E060_REPORT.md; E061_REPORT.md`

## M09 — 歷史 9-row 來源保留六行能否延伸？

- 主線／parent：MOLS10／MOLS_EXISTS_OR_NOT
- 範圍：單一 2024 來源的84個指定 anchors
- 驗收與方法：完整行延伸窮舉，不只檢查結果 JSON。
- 現況：ANSWERED_NO_FOR_ANCHORS
- 對 CLOSED 的作用：排除這個固定來源的近鄰；不排除所有六行前綴。
- 決策／下一步：本地前次修正括號後重播431延伸；本次發佈保留來源範圍。
- 既有證據索引（非一律本批重播）：`E060_REPORT.md`

## M10 — 近 triple 的有限 trade neighborhood 是否已耗盡？

- 主線／parent：MOLS10／MOLS_EXISTS_OR_NOT
- 範圍：固定 Egan near-triple、明確 move set/depth
- 驗收與方法：完整枚舉指定 moves，驗證 Latin preservation 和總 overlay。
- 現況：ANSWERED_FOR_BOUNDED_MOVES
- 對 CLOSED 的作用：避免繼續在 rigid basin 內重複。
- 決策／下一步：E061 depth3 結果僅 restricted；若換 move family 需先寫可區分假說。
- 既有證據索引（非一律本批重播）：`E061_REPORT.md`

## C01 — 候選 <=287 的整條依賴與推導是否正確？

- 主線／parent：CAP7／CAP_MATCHED_BOUNDS
- 範圍：全域分類、110 completion、Fourier、刪點及有限 cases
- 驗收與方法：原文 theorem/proof 範圍、逐 implication 審核、精確 finite certificates。
- 現況：BLOCKED_FULL_REFEREE
- 對 CLOSED 的作用：可影響全域上界，但不會單獨令上下界相等。
- 決策／下一步：Theorem3.9原文範圍已核對；計算分類及全鏈未獨立重驗。
- 既有證據索引（非一律本批重播）：`CAP019_INDEPENDENT_287_UPPER_BOUND_AUDIT_2026-11-02.md`

## C02 — CAP027 的指定兩條相交高密度 quotient lines 是否不相容？

- 主線／parent：CAP7／CAP_MATCHED_BOUNDS
- 範圍：固定五 fibers 的7/6/6/7/4 sizes
- 驗收與方法：檢查CAP034全部30個實點及所有triples。
- 現況：REFUTED
- 對 CLOSED 的作用：停止兩線 UNSAT 捷徑；不代表 formal285 occupancy 全域可實現。
- 決策／下一步：保留 SAT witness 作回歸控制。
- 既有證據索引（非一律本批重播）：`CAP034_TWO_LINE_GLUE_SAT_WITNESS_2026-11-03.md`

## C03 — 236 附近至少多大重建才可能改善？

- 主線／parent：CAP7／CAP_MATCHED_BOUNDS
- 範圍：指定236構造與指定刪改定義
- 驗收與方法：精確 secant hitting／pair replacement isolation certificates。
- 現況：PARTLY_ANSWERED
- 對 CLOSED 的作用：關閉已證小 moves；不限制任意非局部構造。
- 決策／下一步：先使用已證<=16刪改範圍，不能無限延伸隔離界。
- 既有證據索引（非一律本批重播）：`STATE.json pair_replacement_audit / orbit_research`

## C04 — 哪些 imposed symmetry families 已證最優236？

- 主線／parent：CAP7／CAP_MATCHED_BOUNDS
- 範圍：明確 subgroup invariant families
- 驗收與方法：完整 orbit-union enumeration 和 exact objective。
- 現況：PARTLY_ANSWERED
- 對 CLOSED 的作用：停止已耗盡的對稱族；轉弱對稱／非對稱。
- 決策／下一步：不可把偏好對稱當全域 without-loss normalizer。
- 既有證據索引（非一律本批重播）：`C6_ORDER24_FULL_EXACT_236_CERTIFICATE_2026-11-01.md`

## C05 — 哪些對稱可安全破除，哪些不能？

- 主線／parent：CAP7／CAP_MATCHED_BOUNDS
- 範圍：fixed occupancy 與 unrestricted root 分開
- 驗收與方法：完整 stabilizer／frame group action 審核。
- 現況：PARTLY_ANSWERED
- 對 CLOSED 的作用：防止錯誤 symmetry-breaking 遺漏解；減少重複。
- 決策／下一步：固定occupancy的AGL4 stabilizer=identity不代表root無對稱。
- 既有證據索引（非一律本批重播）：`CAP037_FULL_AGL_STABILIZER_2026-11-03.md; CAP040_ROOT_FIRST_PROOF_DAG_2026-11-03.md`

## C06 — 哪些跨線連接首次產生真正 shared-fiber 矛盾？

- 主線／parent：CAP7／CAP_MATCHED_BOUNDS
- 範圍：指定有限 quotient subconfiguration；非任意285cap
- 驗收與方法：共用point variables，納入所有該局部範圍的3AP，保留SAT witness或UNSAT trace。
- 現況：OPEN
- 對 CLOSED 的作用：可形成可重用 compatibility cut；先證其對原物件是必要條件。
- 決策／下一步：不得重試已SAT的兩線；先定義會區分哪些假說，不預設有小矛盾。
- 既有證據索引（非一律本批重播）：`CAP031_SHARED_FIBER_EXACT_FACTORIZATION_2026-11-03.md`

## C07 — 十分支是否完整覆蓋所有237cap並可組成證明？

- 主線／parent：CAP7／CAP_MATCHED_BOUNDS
- 範圍：dense-H moment>=89、frame S7、全部 continuations
- 驗收與方法：獨立核對覆蓋、CNF與presolve、全部十個proof leaves。
- 現況：COVERAGE_REPORTED_ALL_LEAVES_UNKNOWN
- 對 CLOSED 的作用：全部有效UNSAT加236構造才會CLOSED=236。
- 決策／下一步：不能把S8的13分支直接與固定H混用；H09保留。
- 既有證據索引（非一律本批重播）：`CAP040_ROOT_FIRST_PROOF_DAG_2026-11-03.md; CAP043_SECANT_COLLISION_AUDIT_2026-11-03.md`

## C08 — cardinality counter 與 presolve 是否等價？

- 主線／parent：CAP7／CAP_MATCHED_BOUNDS
- 範圍：指定生成器及root CNF hash
- 驗收與方法：雙向 auxiliary extension、small truth tables、literal substitution及mapping。
- 現況：PARTLY_ANSWERED
- 對 CLOSED 的作用：確保SAT/UNSAT證據真的對應原問題。
- 決策／下一步：現有CAP039/041檢查可重用；不要把clause census當solver進展。
- 既有證據索引（非一律本批重播）：`CAP039_CARDINALITY_SUFFIX_AUDIT_2026-11-03.md; CAP041_ROOT_BRANCH_PRESOLVE_2026-11-03.md`

## C09 — 哪些 universal cuts 真能縮小root搜尋？

- 主線／parent：CAP7／CAP_MATCHED_BOUNDS
- 範圍：同一root leaf，等預算、保留全部原解
- 驗收與方法：先證cut sound，再比較加／不加cut的matched solver；證書隨新CNF重新綁定。
- 現況：OPEN
- 對 CLOSED 的作用：對完整窮舉作安全大塊刪除。
- 決策／下一步：更多單線cuts若不能改善root，停止同方向堆積。
- 既有證據索引（非一律本批重播）：`CAP040_ROOT_FIRST_PROOF_DAG_2026-11-03.md`

## C10 — 能否找到任意>=237構造？

- 主線／parent：CAP7／CAP_MATCHED_BOUNDS
- 範圍：不固定236鄰域或subgroup
- 驗收與方法：真實座標、互異性、所有pair第三點獨立檢查。
- 現況：OPEN
- 對 CLOSED 的作用：成功提高lower並否定最大值236，但exact maximum仍需matched upper。
- 決策／下一步：維持非局部構造路線；不把formal occupancy當點集。
- 既有證據索引（非一律本批重播）：`STATE.json`

## C11 — 完整include/exclude窮舉與安全bound是否正確？

- 主線／parent：CAP7／CAP_MATCHED_BOUNDS
- 範圍：全部F3^n子集；無額外對稱
- 驗收與方法：選點後排第三點，remaining-count bound；小階全掃描獨立比對。
- 現況：IMPLEMENTED_CONTROLS_PASS
- 對 CLOSED 的作用：提供不依賴短證明存在的完整後備法。
- 決策／下一步：本批n2精確4、n3精確9；n7未執行，不推新界。
- 既有證據索引（非一律本批重播）：`../closure_batch/README.md`

## F01 — gadget抽象關係、幾何可實現性和組合是否符合目標？

- 主線／parent：FRONTIER_HN／FRONTIER_HN
- 範圍：指定gadget family與有限size範圍
- 驗收與方法：different/equal查核、exact geometry、色數proof與composition。
- 現況：ARCHIVED_OPEN_OR_BOUNDED
- 對 CLOSED 的作用：可關閉整類錯誤gadget方法；>=6不自動解6vs7。
- 決策／下一步：本次不執行frontier-attack；保留原報告及root baseline審核。
- 既有證據索引（非一律本批重播）：`frontier-attack/research/hn-gadgets.md`

## F02 — normalized解能否重建成真正polynomial map？

- 主線／parent：FRONTIER_JC／FRONTIER_JC
- 範圍：指定degree/support歸約系統
- 驗收與方法：負冪消失、field與degree範圍、det與碰撞exact substitution。
- 現況：ARCHIVED_GAP
- 對 CLOSED 的作用：決定反例路線是否可行；necessary方向仍可用emptiness證degree bound。
- 決策／下一步：本次不執行；有限degree不是全域JC。
- 既有證據索引（非一律本批重播）：`frontier-attack/research/jacobian-reconstruction-literature.md`

## F03 — 是否有可用的嚴格rank及analytic-order證書？

- 主線／parent：FRONTIER_BSD／FRONTIER_BSD
- 範圍：指定E/Q與指定r,k
- 驗收與方法：代數上下界相等、低階導數真零、第k階嚴格非零。
- 現況：ARCHIVED_GAP
- 對 CLOSED 的作用：沒有證書能力時停止擴大數值掃描。
- 決策／下一步：本次不執行；rank equality不等於full BSD。
- 既有證據索引（非一律本批重播）：`frontier-attack/research/bsd-rank-tooling.md`

## 每次執行仍須補齊

固定 input hash、parent 推導橋樑、完整覆蓋集合、negative control、證據產物、checker、budget及PASS/FAIL/UNKNOWN後續動作。
新局部命題若不會改變表示法、覆蓋、構造或根證明的下一步，先不排進執行批次。
一般局部不可行不自動排除祖先：若祖先還有其他covers／continuations，必須保留。
