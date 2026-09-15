# 窗口M — 补实验 A：block / elevation low-mid split 扩 10 seeds 报告（跨区边删除协议）

**日期**: 20260826_195611
**状态**: completed
**协议**: 与 exp_034 变体B（window_M_buffer_split_10seeds_strict.py）逐行一致：
跨区边删除（删除 test↔非test 边，保留 test 区内边与非 test 区边）；scaler 仅 train fit；
early stopping 在 val；val 按 seed 从 train 区划分（0.25）；10 seeds [42, 123, 2025, 7, 13, 37, 61, 73, 97, 101]
**样本数**: 6638（6638 干净口径，与封存协议一致）
**目的**: 为图重制任务补齐表 7 的 block_50km / block_100km / elev_low / elev_mid 10-seed 行；
并全量重算 8 splits 的 LSI（r=30km, τ=250m，6638 口径），供 Fig 8 重制。

## 1. 结果汇总（10 seeds, mean±std）

| split | 方法 | R² | RMSE | MAE | 收敛轮数(mean ep) | 退化 vs random |
|-------|------|-----|------|-----|-------------------|----------------|
| random | RF | +0.3640±0.0230 | 0.7967 | 0.6118 | - | +0.0000 |
| random | MLP | +0.3781±0.0213 | 0.7878 | 0.6033 | 238 | +0.0000 |
| random | Geo-GCN | +0.3618±0.0186 | 0.7981 | 0.6195 | 287 | +0.0000 |
| random | EGSG-GCN | +0.4095±0.0230 | 0.7676 | 0.5884 | 295 | +0.0000 |
| block_50km | RF | +0.2948±0.0445 | 0.8484 | 0.6553 | - | +0.0693 |
| block_50km | MLP | +0.3205±0.0508 | 0.8327 | 0.6394 | 273 | +0.0576 |
| block_50km | Geo-GCN | +0.2573±0.0683 | 0.8689 | 0.6783 | 287 | +0.1045 |
| block_50km | EGSG-GCN | +0.3048±0.0559 | 0.8415 | 0.6486 | 298 | +0.1047 |
| block_100km | RF | +0.2831±0.1231 | 0.8141 | 0.6285 | - | +0.0809 |
| block_100km | MLP | +0.3112±0.1146 | 0.7992 | 0.6097 | 217 | +0.0669 |
| block_100km | Geo-GCN | +0.2257±0.1227 | 0.8462 | 0.6533 | 270 | +0.1361 |
| block_100km | EGSG-GCN | +0.2918±0.1123 | 0.8085 | 0.6170 | 272 | +0.1176 |
| elev_low | RF | -0.0834±0.0664 | 1.1799 | 0.9434 | - | +0.4474 |
| elev_low | MLP | +0.0836±0.0757 | 1.0848 | 0.8615 | 160 | +0.2945 |
| elev_low | Geo-GCN | -7.0526±3.4186 | 3.1567 | 2.7755 | 225 | +7.4144 |
| elev_low | EGSG-GCN | -0.5728±0.4770 | 1.4074 | 1.1311 | 250 | +0.9823 |
| elev_mid | RF | +0.0750±0.0127 | 0.8680 | 0.6812 | - | +0.2890 |
| elev_mid | MLP | +0.1411±0.0123 | 0.8365 | 0.6394 | 247 | +0.2370 |
| elev_mid | Geo-GCN | +0.0405±0.0282 | 0.8840 | 0.6859 | 263 | +0.3213 |
| elev_mid | EGSG-GCN | +0.1225±0.0143 | 0.8455 | 0.6627 | 296 | +0.2870 |

## 2. 协议复刻检查（random 参考组）

- EGSG-GCN random: R²=0.4095±0.0230（封存参考 0.4097±0.0230）

## 3. LSI 汇总（8 splits，6638 口径，r=30km, τ=250m）

- random: LSI=28.0701±0.4959 (n_test≈1328)
- block_50km: LSI=18.0185±4.0295 (n_test≈1043)
- block_100km: LSI=6.7865±1.4748 (n_test≈1797)
- elev_low: LSI=2.3679±0.0000 (n_test≈2191)
- elev_mid: LSI=7.9437±0.0000 (n_test≈2256)
- elev_high: LSI=5.8115±0.0000 (n_test≈2191)
- buffer_30km: LSI=0.0000±0.0000 (n_test≈1042)
- buffer_50km: LSI=0.0000±0.0000 (n_test≈1042)

## 4. 核心检验（配对 10 seeds）

- EGSG vs Geo-GCN block_50km: ΔR²=+0.0474，p=0.000016（***），d=+2.6267
  - random vs block_50km (EGSG-GCN): 退化=+0.1047，p=0.000349（***）
  - random vs block_50km (Geo-GCN): 退化=+0.1045，p=0.000671（***）
- EGSG vs Geo-GCN block_100km: ΔR²=+0.0662，p=0.000040（***），d=+2.3480
  - random vs block_100km (EGSG-GCN): 退化=+0.1176，p=0.008316（**）
  - random vs block_100km (Geo-GCN): 退化=+0.1361，p=0.007651（**）
- EGSG vs Geo-GCN elev_low: ΔR²=+6.4798，p=0.000126（***），d=+2.0223
  - random vs elev_low (EGSG-GCN): 退化=+0.9823，p=0.000109（***）
  - random vs elev_low (Geo-GCN): 退化=+7.4144，p=0.000075（***）
- EGSG vs Geo-GCN elev_mid: ΔR²=+0.0819，p=0.000011（***），d=+2.7616
  - random vs elev_mid (EGSG-GCN): 退化=+0.2870，p=0.000000（***）
  - random vs elev_mid (Geo-GCN): 退化=+0.3213，p=0.000000（***）

## 5. 结论

- block/elev low/mid 10-seed 数值可直接填入表 7（替换旧 5-seed window_J 行）。
- LSI 8 splits 全量重算值可直接用于 Fig 8 重制（D(s) 与 LSI 相关性重算）。

## 6. 输出文件

- block_elev_10seeds_raw.csv / _summary.csv / _paired.csv
- lsi_by_split_10seeds.csv / lsi_agg_by_split_10seeds.csv
- plots/fig_block_elev_10seeds_r2.png, plots/fig_egsg_gain_block_elev_10seeds.png
