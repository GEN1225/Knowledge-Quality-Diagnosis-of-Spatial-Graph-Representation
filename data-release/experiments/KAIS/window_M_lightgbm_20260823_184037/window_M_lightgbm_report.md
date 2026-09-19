# 窗口M 补充 — LightGBM 基线 + 轻量调参对照报告

**日期**: 20260823_184037
**状态**: completed
**对应修改策略**: KAIS 补实验第 1 项（XGBoost/LightGBM 对比）的 LightGBM 部分

## 1. 目的

补全修改策略第 1 项的 LightGBM 基线，并同时给出调参对照（预防"LightGBM 未调参"质疑）。
一轮同时产出 LightGBM_fixed（固定配置）与 LightGBM_tuned（轻量网格调参）两组结果。

## 2. 协议

- 固定配置: n_estimators=500, learning_rate=0.05, num_leaves=31, subsample=0.8, colsample_bytree=0.8, min_child_samples=20
- 调参网格: num_leaves {15,31,63} x learning_rate {0.05,0.1} x subsample {0.8,1.0} = 12 组合
- 选择方式: 每种子内 train 拟合、**val 集选优**、test 只评一次（无泄露）
- 同 SEEDS、同 split、同 scaler 协议（与封存 clean protocol 完全一致）

## 3. 各种子最优超参

| seed | num_leaves | learning_rate | subsample | val R² | test R² |
|------|------------|---------------|-----------|--------|---------|
| 42 | 15 | 0.05 | 0.8 | 0.3327 | 0.3598 |
| 123 | 15 | 0.05 | 1.0 | 0.3803 | 0.3535 |
| 2025 | 15 | 0.05 | 0.8 | 0.3303 | 0.3495 |
| 7 | 15 | 0.05 | 1.0 | 0.4017 | 0.3825 |
| 13 | 15 | 0.05 | 1.0 | 0.3410 | 0.3815 |
| 37 | 15 | 0.05 | 1.0 | 0.3796 | 0.4060 |
| 61 | 15 | 0.05 | 1.0 | 0.3718 | 0.3856 |
| 73 | 15 | 0.05 | 1.0 | 0.3965 | 0.3416 |
| 97 | 15 | 0.05 | 0.8 | 0.3590 | 0.3059 |
| 101 | 15 | 0.05 | 1.0 | 0.2990 | 0.3512 |

## 4. 结果（10 seeds, mean±std）

| 方法 | R² | RMSE | MAE |
|------|-----|------|-----|
| LightGBM_fixed | 0.3465±0.0294 | 0.8075±0.0196 | 0.6148±0.0143 |
| **LightGBM_tuned** | **0.3617±0.0283** | **0.7980±0.0195** | **0.6078±0.0144** |
| XGBoost_fixed | 0.3524±0.0291 | 0.8038±0.0183 | 0.6119±0.0132 |
| XGBoost_tuned | 0.3608±0.0292 | 0.7986±0.0207 | 0.6078±0.0140 |
| RF | 0.3640±0.0230 | 0.7967±0.0181 | 0.6118±0.0124 |
| MLP | 0.3781±0.0213 | 0.7878±0.0161 | 0.6033±0.0091 |
| Geo_kNN | 0.3617±0.0187 | 0.7982±0.0143 | 0.6194±0.0091 |
| EGSG_250m | 0.4097±0.0230 | 0.7675±0.0143 | 0.5883±0.0092 |

## 5. 核心检验

- EGSG_250m vs LightGBM_fixed: ΔR² = +0.0632，p = 0.000001
- **EGSG_250m vs LightGBM_tuned: ΔR² = +0.0480，p = 0.000015（***），Cohen's d = +2.6500**
- LightGBM_tuned vs LightGBM_fixed: ΔR² = +0.0152，p = 0.000004
- LightGBM_tuned vs XGBoost_tuned: ΔR² = +0.0009，p = 0.688435

## 6. 结论

EGSG_250m 在 LightGBM 调参后仍保持显著优势，'EGSG 优于全部 ML 基线'主张稳健，可写入投稿稿。

## 7. 输出文件

- raw_seed_results_lightgbm.csv — LightGBM 固定+调参逐种子结果
- tuned_hyperparams_by_seed.csv — 每种子最优超参
- merged_seed_results.csv — 八方法完整合并结果
- paper_comparison_table_lightgbm.csv — 论文对比表（含 LightGBM）
- paired_comparison_results_lightgbm.csv — 全部配对检验
- plots/method_r2_boxplot_lightgbm.png — 八方法箱线图
