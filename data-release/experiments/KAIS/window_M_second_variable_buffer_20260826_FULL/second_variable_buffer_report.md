# 窗口M — 补实验 B：NDVI/LST buffer_30 外推 10-seed 正式版报告

**日期**: 20260826_224811
**状态**: completed
**协议**: 与 exp_034 变体B / exp_037 / exp_038 完全一致（跨区边删除；scaler 仅 train fit；
val 早停 patience 10；val 按 seed 从 train 区划分 0.25；10 seeds [42, 123, 2025, 7, 13, 37, 61, 73, 97, 101]）
**任务**: LST 目标 lst_mean（特征 VEG+TERRAIN 14 维）；NDVI 目标 ndvi_mean（特征 TERRAIN+HYDRO 7 维）
**与历史实验关系**: LST buffer_30 与 exp_038 同协议重跑核对（历史 10-seed 值 Geo 0.4627/EGSG 0.4454 p=0.082）；
NDVI buffer_30 为新数据（exp_038 未跑）；random 锚点对照 exp_037

## 1. 结果汇总（10 seeds, mean±std）

| 任务 | split | 方法 | R² | RMSE | MAE | 退化 vs random |
|------|-------|------|-----|------|-----|----------------|
| LST | random | RF | +0.7275±0.0142 | 0.5189 | 0.3959 | +0.0000 |
| LST | random | MLP | +0.7013±0.0160 | 0.5433 | 0.4125 | +0.0000 |
| LST | random | Geo-GCN | +0.8094±0.0124 | 0.4339 | 0.3318 | +0.0000 |
| LST | random | EGSG-GCN | +0.7905±0.0126 | 0.4549 | 0.3565 | +0.0000 |
| LST | buffer_30km | RF | +0.1216±0.0230 | 1.0979 | 0.8449 | +0.6059 |
| LST | buffer_30km | MLP | +0.0320±0.0289 | 1.1525 | 0.9148 | +0.6693 |
| LST | buffer_30km | Geo-GCN | +0.4627±0.0349 | 0.8584 | 0.6781 | +0.3467 |
| LST | buffer_30km | EGSG-GCN | +0.4454±0.0219 | 0.8723 | 0.6806 | +0.3451 |
| NDVI | random | RF | +0.6604±0.0159 | 0.5804 | 0.4116 | +0.0000 |
| NDVI | random | MLP | +0.6435±0.0198 | 0.5945 | 0.4252 | +0.0000 |
| NDVI | random | Geo-GCN | +0.3779±0.0188 | 0.7858 | 0.5829 | +0.0000 |
| NDVI | random | EGSG-GCN | +0.6378±0.0120 | 0.5995 | 0.4276 | +0.0000 |
| NDVI | buffer_30km | RF | +0.3629±0.0116 | 0.8791 | 0.6856 | +0.2975 |
| NDVI | buffer_30km | MLP | +0.3040±0.0300 | 0.9186 | 0.7034 | +0.3396 |
| NDVI | buffer_30km | Geo-GCN | -0.0502±0.0348 | 1.1285 | 0.8809 | +0.4281 |
| NDVI | buffer_30km | EGSG-GCN | +0.1884±0.0261 | 0.9921 | 0.7660 | +0.4494 |

## 2. 锚点检查（同协议复现，|Δ|<0.02 视为 OK）

```
  LST   random       RF         本实验3seed=+0.7285 历史=+0.7285 Δ=-0.0000 [OK]
  LST   random       MLP        本实验3seed=+0.7089 历史=+0.7089 Δ=-0.0000 [OK]
  LST   random       Geo-GCN    本实验3seed=+0.8168 历史=+0.8168 Δ=-0.0000 [OK]
  LST   random       EGSG-GCN   本实验3seed=+0.7939 历史=+0.7939 Δ=+0.0000 [OK]
  NDVI  random       RF         本实验3seed=+0.6647 历史=+0.6647 Δ=+0.0000 [OK]
  NDVI  random       MLP        本实验3seed=+0.6378 历史=+0.6378 Δ=+0.0000 [OK]
  NDVI  random       Geo-GCN    本实验3seed=+0.3834 历史=+0.3834 Δ=-0.0000 [OK]
  NDVI  random       EGSG-GCN   本实验3seed=+0.6414 历史=+0.6414 Δ=+0.0000 [OK]
  LST   buffer_30km  RF         本实验3seed=+0.1296 历史=+0.1296 Δ=+0.0000 [OK]
  LST   buffer_30km  MLP        本实验3seed=+0.0483 历史=+0.0483 Δ=-0.0000 [OK]
  LST   buffer_30km  Geo-GCN    本实验3seed=+0.4320 历史=+0.4320 Δ=+0.0000 [OK]
  LST   buffer_30km  EGSG-GCN   本实验3seed=+0.4366 历史=+0.4366 Δ=-0.0000 [OK]
```

锚点结论: 全部通过，协议与历史实验逐位一致

## 3. 核心检验（配对 10 seeds）

- LST random: EGSG vs Geo-GCN ΔR²=-0.0189, p=0.000119（***），d=-2.04
- LST buffer_30km: EGSG vs Geo-GCN ΔR²=-0.0173, p=0.082273（ns），d=-0.62
- NDVI random: EGSG vs Geo-GCN ΔR²=+0.2599, p=0.000000（***），d=+26.32
- NDVI buffer_30km: EGSG vs Geo-GCN ΔR²=+0.2386, p=0.000000（***），d=+5.10

## 4. 退化幅度（random → buffer_30km，同方法配对）

| 任务 | 方法 | ΔR² | p | 显著性 |
|------|------|-----|---|--------|
| LST | RF | +0.6059 | 0.000000 | *** |
| LST | MLP | +0.6693 | 0.000000 | *** |
| LST | Geo-GCN | +0.3467 | 0.000000 | *** |
| LST | EGSG-GCN | +0.3451 | 0.000000 | *** |
| NDVI | RF | +0.2975 | 0.000000 | *** |
| NDVI | MLP | +0.3396 | 0.000000 | *** |
| NDVI | Geo-GCN | +0.4281 | 0.000000 | *** |
| NDVI | EGSG-GCN | +0.4494 | 0.000000 | *** |

## 5. 结论（论文 §5.8 口径）

- LST buffer_30：GNN 仍保持正 R²（Geo +0.4627 /
  EGSG +0.4454），
  无 AGB 式崩塌 → 外推退化是目标场结构依赖的
- NDVI buffer_30：见上表（新数据）
- EGSG vs Geo 在 buffer_30 的差异方向与 AGB 对照（-0.054, p=0.027）

## 6. 输出文件

- second_variable_buffer_raw.csv / _summary.csv / _paired.csv
- plots/fig_second_variable_buffer_LST.png, _NDVI.png
