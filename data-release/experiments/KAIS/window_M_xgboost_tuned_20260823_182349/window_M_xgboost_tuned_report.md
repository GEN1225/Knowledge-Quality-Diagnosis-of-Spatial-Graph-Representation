# 窗口M 补充 — XGBoost 轻量调参对照报告

**日期**: 20260823_182349
**状态**: completed
**对应修改策略**: KAIS 补实验第 1 项（XGBoost 对比）的稳健性补充

## 1. 目的

回应潜在审稿质疑："XGBoost 未调参"。在 clean protocol 下对 XGBoost 做轻量网格搜索，
证明即使调参后的 XGBoost 也无法超越 EGSG_250m。

## 2. 协议

- 网格: max_depth {4,6,8} x learning_rate {0.05,0.1} x subsample {0.8,1.0} = 12 组合
- 其余固定: n_estimators=500, colsample_bytree=0.8
- 选择方式: 每种子内 train 拟合、**val 集选优**、test 只评一次（无泄露）
  ——与 GNN/MLP 用 val 做 early stopping 的协议角色一致
- 同 SEEDS、同 split、同 scaler 协议（与封存 clean protocol 完全一致）

## 3. 各种子最优超参

| seed | max_depth | learning_rate | subsample | val R² | test R² |
|------|-----------|---------------|-----------|--------|---------|
| 42 | 6 | 0.05 | 1.0 | 0.3369 | 0.3637 |
| 123 | 6 | 0.05 | 1.0 | 0.3859 | 0.3519 |
| 2025 | 6 | 0.05 | 0.8 | 0.3449 | 0.3364 |
| 7 | 4 | 0.05 | 0.8 | 0.3805 | 0.3862 |
| 13 | 6 | 0.05 | 1.0 | 0.3385 | 0.3795 |
| 37 | 4 | 0.05 | 0.8 | 0.3745 | 0.4012 |
| 61 | 4 | 0.05 | 1.0 | 0.3791 | 0.3828 |
| 73 | 4 | 0.05 | 0.8 | 0.3886 | 0.3526 |
| 97 | 4 | 0.05 | 1.0 | 0.3653 | 0.2992 |
| 101 | 4 | 0.05 | 0.8 | 0.2951 | 0.3549 |

## 4. 结果（10 seeds, mean±std）

| 方法 | R² | RMSE | MAE |
|------|-----|------|-----|
| RF | 0.3640±0.0230 | 0.7967±0.0181 | 0.6118±0.0124 |
| MLP | 0.3781±0.0213 | 0.7878±0.0161 | 0.6033±0.0091 |
| XGBoost_fixed | 0.3524±0.0291 | 0.8038±0.0183 | 0.6119±0.0132 |
| **XGBoost_tuned** | **0.3608±0.0292** | **0.7986±0.0207** | **0.6078±0.0140** |
| Geo_kNN | 0.3617±0.0187 | 0.7982±0.0143 | 0.6194±0.0091 |
| EGSG_250m | 0.4097±0.0230 | 0.7675±0.0143 | 0.5883±0.0092 |

## 5. 核心检验

- EGSG_250m vs XGBoost_tuned: ΔR² = +0.0488，p = 0.000012（***），Cohen's d = +2.7171
- XGBoost_tuned vs XGBoost_fixed: ΔR² = +0.0084，p = 0.026508

## 6. 结论

EGSG_250m 在 XGBoost 调参后仍保持显著优势，论文'EGSG 优于全部 ML 基线'主张稳健，可写入投稿稿。

## 7. 输出文件

- raw_seed_results_tuned.csv — 调参后逐种子结果
- tuned_hyperparams_by_seed.csv — 每种子最优超参
- merged_seed_results.csv — 六方法完整合并结果
- paper_comparison_table_tuned.csv — 论文对比表（含 tuned）
- paired_comparison_results_tuned.csv — 全部配对检验
- plots/method_r2_boxplot_xgboost_tuned.png — 六方法箱线图
