# MOLS10 | Milestone M068 — 唯一目標：OPEN → CLOSED

**版本：2026-11-06（UTC 日期）｜全域狀態：OPEN｜目前沒有完整 SAT witness、沒有 unrestricted UNSAT proof。**

> 這份是 Math Agent 與其他 AI/研究者的 **authoritative handoff**，不是宣稱難題已解決的論文。新的結論須依據證據更新；過去已推翻的假設絕不可再次當作公理。研究目標只有一個：**將 3-MOLS(10) 的數學狀態由 OPEN 改為 CLOSED**。

## 1. 題目、形式化及驗收

題目：是否存在三個 `10×10` Latin squares `A,B,C`，分別每行、每列恰好含 `0..9`，且三組二元疊加 `(A,B),(A,C),(B,C)` 各有 **100 種不同 ordered pairs**？等價地，是否存在 `OA(100,5,10,2)`？現有歷史基線近似三方的 overlays 是 `100/100/91`，**不是** triple。正式來源：Egan–Wanless 2016, https://doi.org/10.1090/mcom/3010；Bright–Keita–Stevens 2026, https://doi.org/10.37236/13960 。

- **CLOSED — YES：**公開 A/B/C 三個完整方陣；以與求解器分離的 checker 驗證全部 Latin 行列及三組 `100/100/100`。只需 **任何一個** witness，不需其餘 1,699 分支有解答。
- **CLOSED — NO：**給予不受限制的普遍數學矛盾，或者證明 **全部可能解均在已檢查的完備分類內**，並給予所有剩餘類別的可獨立核驗 UNSAT 證明（LRAT/其他 sound checker + 如有新增數學 cuts，必須另證 cuts sound）。
- **`UNKNOWN_BUDGET` 永遠不等於 UNSAT。**只確認某個固定 pair、特定 4×4 subsquare、局部前綴或 relaxation 不可延伸，均 **不是** 全域不存在證明。

## 2. 四條明確通向 CLOSED 的路線（可並行）

| 路線 | Proof obligation（必須真正成立） | 現時證據 | 完成標準 |
|---|---|---|---|
| **R1 數學剪枝／包圍** | 對任意合法 partial state 導出**可檢查且 sound** 的 global nogood、排除大量完整 continuations；所有留下的空間仍須用其他方式決定 | E067 root-level spectral 與 GF(2) rank 各掃 1,700 類、直接排除 0；深層 cuts 尚未驗證 | **剪枝本身不是 CLOSED。**只有連同剩餘搜索範圍完全排除或找到 SAT，才結案 |
| **R2 一個完整 SAT witness** | 建出三個 10×10 Latin 方陣、獨立驗證 `100/100/100` | 100/100/91 舊例；E061–E067 沒有完整解 | 一個獨立檢查通過的完整 triple → **立即 CLOSED YES** |
| **R3 Global UNSAT proof** | 已證明完備的 1,700 canonical branches 全部有 checked UNSAT；**或**未分支/full selector OA formula 有完整 proof | E064 有完整 first-column paratopy inventory；E065 full 5D SAT/PB；E066 1,700 bounded runs 全 UNKNOWN | 對原題全部解的形式化排除（證書 + coverage）→ **CLOSED NO** |
| **R4 Universal mathematics theorem（假設存在導出矛盾）** | 假定 `OA(100,5,10,2)` 存在；從 parity、rank、incidence、transversal 等正確必要條件導出不可避免的 contradiction，**沒有額外未證明前提** | 已知必要條件很多，但互不矛盾；E059 反例否定過度樂觀 LP/ILP lemma | 一條 unrestricted 正確論證即可 **CLOSED NO**，可以完全不做 1,700 次 SAT |

**邏輯提醒：**「1,700」是 *一個* 完備的分支覆蓋方法，並不是不可更改的下界；R1/R4 可能一條定理排除大量乃至全部分支，R2 只需一個 witness。

## 3. 目前已知且有可重播證據的狀態（E001–E067 摘要）

| 時期 | 做過甚麼 | 驗證範圍 / 教訓 | 原題是否 CLOSED |
|---|---|---|---|
| E001–E030 | 歷史 orthogonal pairs、Egan near triple、common transversals、fixed-pair extension、Latin trades、partial exact cover | 特定 pairs 的不可延伸與 local obstruction，不可提升成全域 | **NO** |
| E031–E058 | 精確 LP/Farkas 證書、partial-prefix 穷舉、robustness、特定前綴變換、分支正規化 | 許多固定-prefix UNSAT 真實，但沒有任何一整個 unrestricted branch 被覆蓋；過度 polishing 的邊際價值很低 | **NO** |
| **E059（重要反例）** | 對 universal 4-row fractional infeasibility 與 4-/7-row integer residual obstruction 找到**正確 counterexamples** | 舊 4-coordinate residual solver 遺漏 `ROW` coordinate；不能代表真正 5D OA | **NO；停用錯誤 general lemma** |
| E060–E062 | Full 5D OA-DLX、pairs+transversal packing；掃描 2,781 個公開 pairs；Egan pair 的 complete 14 transversals、最多 7 disjoint | 限於提供的 pairs。普通 pair sampling 不構成推翻 3-MOLS(10) 的證據 | **NO** |
| E063–E064 | 完整 3×9 first-column Latin rectangle 的 isotopy/paratopy 分類 | `16,085 ordered → 2,877 isotopy → 1,700 paratopy representatives`；小階 4/5 SAT、6 全類 exhaustive UNSAT 控制通過；數字與已發表分類一致 | **NO；但得到 complete proof frontier** |
| E065 | Full OA Boolean CNF（33,000 vars，101,740 clauses），另有 41,338 placements/1,000 exact-one PB solver | 小階 SAT/UNSAT 互相交叉檢查，n=10 抽樣仍 UNKNOWN | **NO** |
| **E066** | 完整 1,700 分支的 proof-producing bounded campaign；分支 CNF 101,758 clauses；保留全部 ledger | **1,700/1,700 attempted；SAT=0、verified UNSAT=0、`UNKNOWN_BUDGET`=1,700；合計 13,658.466 solver seconds（約 3.79 累計 CPU hours）**。這不是完工 ETA | **NO；0/1,700 closed** |
| **E067** | spectral 5-net `A²=25I+20J`、全部五種 4-net projections GF(2) rank，上述 1,700 類 root-level 審核；兩個完成 pairs 的 transversal packing | root spectral 0/1,700 排除且證明在 19 點固定結構下自動滿足；GF(2) 0/1,700 排除。Egan pair 14 common / max packing 7；crimped pair 0 common / max0。**這些是完整 pair，不是 1,700 root branches** | **NO** |

**已知文獻邊界：**Gill–Wanless 消滅 18,526,320 個具有非平凡 GF(2) relation 的 **完整 orthogonal pair species**，不是 1,700 個 first-column branches；Bright–Keita–Stevens 2026 的 4×4 subsquare 結果亦屬受限問題。不可混淆集合。

## 4. 目前真實瓶頸與已排除的錯誤方向

**主要問題未經證明是 CPU 不夠。**目前 generic CNF/CDCL 在 1,700 個 huge branches 中沒有完成任何一個 order-10 branch；直接延長相同 timeout 無法形成可信 ETA。主要研究障礙是 constraints 的 propagation strength、combinatorial explosion、proof-generation cost、以及 full 5D 關係的數學特性。

- **切勿重做**：E052–E057 固定前綴 Farkas 證書打磨；Egan 100/100/91 微小 trades；已被 E059 反證的 universal 4-row residual LP/ILP 路線；無效的 19-point root spectral screen；把所有合法 GF(2) rank 當成「可能延伸」的錯誤充分條件。
- **可利用但要加深**：五個 4-net projection 的 GF(2) rank=37；對完整或足夠深的 orthogonal A/B 做 common-transversal **maximum disjoint packing=10** 必要檢查；任何已發現的 nogood 必須在其完整前提下證明有效。
- **研究哲學**：從 P 或 ¬P 的證明義務倒推。對每個 lemma 先找 counterexample，測試對小階正例的 soundness，再量度它實際剪掉多少 *仍合法的延伸搜尋樹*，不是數多少歷史固定-prefix 異常。

## 5. 下一個執行 Milestones（不是未來結果承諾）

| Milestone | 目標／Deliverable | 驗收（可被判定） | 狀態 |
|---|---|---|---|
| **M0：Research State Freeze** | 本文件 + machine status + GitHub/Drive 雙保存 + 完整 proof obligations | E066 ledger 1,700 狀態重算、舊誤判與脆弱假設明示；雙端 URL 可開 | **本次交付** |
| **M1：First Proof-Sound Deep Cut** | Partial A/B common-transversal upper bound 或 4-net GF(2) overapprox rank upper bound，帶 exact counterexample audit | 通過 GF(5) positive control，對真正不可延伸的 Egan pair 及**不完全 pair**嚴格提前剪枝；每個剪枝附可重現程式 | **IN PROGRESS** |
| **M2：Transferable Global Nogoods** | 從局部 sound obstruction 生成可多分支重用且等價 / valid 的 SAT constraints | 大量實際 solver nodes/conflicts 下降且無誤排除已知正例；交叉驗證 proof lifting | **NOT STARTED** |
| **M3：Constructive Dual Search** | 聯合構造 A/B + 10 disjoint common transversals，或 full OA(100,5,10,2) SAT | 若找到 witness，獨立驗證 100/100/100；否則必須保留 UNKNOWN | **ONGOING / NO WITNESS** |
| **M4：Global Proof Search** | 1,700 可能性經 sound cuts 減少後作 proof-carrying search；或直接對 full selector OA 證 UNSAT | 任何 UNSAT 有 checked proof；所有 branch coverage 完整；逐步記錄每個真正 closed branch | **0/1,700** |
| **M5：CLOSED** | 獨立重播 + 雙端永久歸檔 + 明確科學歸屬 | SAT witness **或** unrestricted verified nonexistence proof | **NOT ACHIEVED** |

**不設定憑空的完工時間**；若 deep-cut 在合理測試下毫無 pruning gain，就不應無限優化同一弱 invariant，改研究新的 5D / transversal / geometric necessary condition。

## 6. 研究資料位置（唯一共同交接入口）

### GitHub：具版本、程式、可重播實驗

- Repository: https://github.com/davidlueng986-alt/123321
- Research root: https://github.com/davidlueng986-alt/123321/tree/math-agent-mols10/research/mols10
- 目前狀態：[`STATE.json`](https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/STATE.json)
- 全域 proof program：[`GOAL_BACKWARD_PROOF_PROGRAM.md`](https://github.com/davidlueng986-alt/123321/blob/math-agent-mols10/research/mols10/GOAL_BACKWARD_PROOF_PROGRAM.md)，但歷史中已被 E059 反證的部分不可當作 active theorem
- 對應 Milestone（在此 commit 新增）：`research/mols10/MILESTONE_CLOSED_2026-11-06.md`、`research/mols10/CLOSED_PROOF_OBLIGATIONS.json`、`research/mols10/MILESTONE_INDEX.md`
- 全域分類：[`e064`](https://github.com/davidlueng986-alt/123321/tree/math-agent-mols10/research/mols10/e064)
- 完整 SAT：[`e065`](https://github.com/davidlueng986-alt/123321/tree/math-agent-mols10/research/mols10/e065)
- 全量求解：[`e066`](https://github.com/davidlueng986-alt/123321/tree/math-agent-mols10/research/mols10/e066)
- 最近數學 audit：[`e067`](https://github.com/davidlueng986-alt/123321/tree/math-agent-mols10/research/mols10/e067)

### Google Drive：共享與交接（同一份 authoritative 狀態）

- **Math Agent 專案：**`My Drive / Math Agent /`
- **本題研究資料夾：**`My Drive / Math Agent / 04_EXPERIMENTS_AND_PROOFS / MOLS10 /`  
  URL: https://drive.google.com/drive/folders/1-Unm0P7vD-B5VMg-9vrARTKEU8j67MxO
- **Living Research Journal：**https://docs.google.com/document/d/1NDPWEMM3Cf5HrhdOcV6pVE9tCI-kxKbavxcfIBFva3k/edit
- **已保存 E066 全量 ledger ZIP：**https://drive.google.com/file/d/1YunKMnAaoafaB9m5_ISSfNyXfSaB2BpG/view
- **E067 原始碼及全量 audit ZIP：**https://drive.google.com/file/d/1u4An8sL8HCix88a9V1mVXB1AA-9ALgmo/view
- **本次 milestone：**Drive 同目錄內 `MILESTONE_CLOSED_2026-11-06.md`、`CLOSED_PROOF_OBLIGATIONS.json`、`MILESTONE_INDEX.md`。新實驗加入相同目錄，GitHub 同步精確檔案。

**同步聲明：**兩處均是保存地點，但截至本 milestone，歷史大檔有些以 ZIP 保存在 Drive，而非已逐個鏡像到 GitHub；禁止宣稱「每個歷史附件兩端逐檔 mirror」而未核對。**任何新 E068+ 研究都應雙端存放 source、fixture、results、report、SHA manifest（原始大資料可採可核驗 ZIP + GitHub 來源與 digest）。**

## 7. Agent Handoff 必讀、行動順序

1. 讀本 milestone、`STATE.json`、E059 strategy revision、E064/E065/E066/E067 的原始報告及 E066 ledger；確認仍 OPEN；核對最新正式文獻是否已有人 CLOSED。
2. 選 R1/R2/R3/R4 中一條，先寫 **從中間 lemma → 最終 CLOSED 的嚴格蘊含關係**、失敗條件、scope；如只排除個別 pairs，明確標「局部」。
3. **立即執行**可測試的 code/math attempt；產生數據與反例；必要時反駁本 milestone 的假設；不得停於哲學描述。
4. 任何新的數學 pruning clause 必須有 soundness proof（或可核查的保守 relaxation）、positive controls 和 negative controls；錯誤排除正例立即停用該方法。
5. `SAT` 由獨立 checker 重播；`UNSAT` 需完整 proof；`UNKNOWN` 原樣保留。不可把 SAT solver 的 unverified output 當作定理。
6. 更新本 milestone 中的**證據與狀態**，不得悄悄覆寫歷史結果；新實驗獨立 `E068_*` 等；將結果和 SHA 同時同步 GitHub + Google Drive + Living Journal。
7. 已停用的每小時自動研究不自行恢復；所有後續長期搜尋必須有使用者明確啟動的執行環境和可追蹤 job，不保證本聊天會持續背景執行。

### Minimal success test

- `python3 verify.py <candidate.json>`（與求解器分離）並檢驗 3x Latin rows/cols 和全部 pair overlays=100 → YES。
- 或 verified complete coverage theorem + 1,700 explicit verified UNSAT / one sound global UNSAT proof / one universal contradiction → NO。
- **其餘任何結果：OPEN。**
