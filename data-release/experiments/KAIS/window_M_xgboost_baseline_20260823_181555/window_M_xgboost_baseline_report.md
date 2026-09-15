# 窗口M XGBoost 基线实验报告

**日期**: 20260823_181555
**状态**: completed
**对应修改策略**: KAIS 补实验第 1 项（XGBoost 对比）

## 1. 实验目的

在 clean random split 协议下补充 XGBoost 基线，验证 EGSG_250m 是否仍显著优于
所有传统机器学习基线（RF / MLP / XGBoost）。

## 2. 协议

- 数据集: 2021 逐年 scaled parquet，清洗后 n=6638
- Split: 60/20/20 random，SEEDS=[42, 123, 2025, 7, 13, 37, 61, 73, 97, 101]
- Scaler 只在 train 上 fit；MLP 在 val 上 early stopping
- XGBoost 超参: n_estimators=500, max_depth=6, learning_rate=0.05,
  subsample=0.8, colsample_bytree=0.8（固定，不调优）
- EGSG_250m / Geo_kNN 结果复用已封存参考 CSV（同协议同种子）

## 3. 协议复刻校验

通过：复跑 RF 与 MLP 的 R² 均值与参考值的偏差在
±0.005 容差内，split/数据与封存协议一致，XGBoost 结果可信。

## 4. 结果（10 seeds, mean±std）

| 方法 | R² | RMSE | MAE |
|------|-----|------|-----|
| RF | 0.3640±0.0230 | 0.7967±0.0181 | 0.6118±0.0124 |
| MLP | 0.3781±0.0213 | 0.7878±0.0161 | 0.6033±0.0091 |
| **XGBoost** | **0.3524±0.0291** | **0.8038±0.0183** | **0.6119±0.0132** |
| Geo_kNN | 0.3617±0.0187 | 0.7982±0.0143 | 0.6194±0.0091 |
| EGSG_250m | 0.4097±0.0230 | 0.7675±0.0143 | 0.5883±0.0092 |

## 5. 核心检验：EGSG_250m vs XGBoost

- ΔR² = +0.0573（EGSG 0.4097 vs XGBoost 0.3524）
- 配对 t 检验 p = 0.000006（***）
- Wilcoxon p = 0.001953
- Cohen's d = +2.9832

## 6. 结论

EGSG_250m 显著优于 XGBoost 基线，论文'EGSG 优于全部 ML 基线'主张得到支持。

## 7. 输出文件

- raw_seed_results.csv — 新跑 RF/MLP/XGBoost 逐种子结果
- merged_seed_results.csv — 合并参考 EGSG/Geo 后的完整结果
- paper_comparison_table.csv — 论文 5 方法对比表
- paired_comparison_results.csv — 全部配对检验
- replication_check.csv — 协议复刻校验
- plots/method_r2_boxplot_with_xgboost.png — 5 方法 R² 箱线图
