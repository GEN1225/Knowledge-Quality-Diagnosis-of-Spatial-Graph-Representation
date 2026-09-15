# Window C: EGSG 后续创新机会扫描 — 总结报告

**时间戳**: 20260605_103628

**Seeds**: [42, 123, 2025, 7, 13] (快速判断阶段)

**EGSG-250m 封存基线**: R² = 0.4097 ± 0.0230 (10 seeds, clean protocol)

**本次 EGSG-250m (5 seeds)**: R² = 0.4141 ± 0.0213

## 全部方法汇总

| Method | R² (mean±std) | RMSE (mean±std) | MAE (mean±std) | ΔR² vs EGSG_250m |
|--------|---------------|-----------------|----------------|------------------|
| EGSG_250m | 0.4141±0.0213 | 0.7696±0.0176 | 0.5912±0.0113 | +0.0000 |
| EGSG_LC_soft_0.5 | 0.4140±0.0177 | 0.7697±0.0198 | 0.5921±0.0130 | -0.0000 |
| EGSG_LC_soft_0.25 | 0.4140±0.0173 | 0.7697±0.0202 | 0.5921±0.0120 | -0.0001 |
| EGSG_LC_soft_0.75 | 0.4139±0.0188 | 0.7697±0.0192 | 0.5917±0.0122 | -0.0002 |
| MLP+EGSG_residual | 0.4114±0.0141 | 0.7714±0.0164 | 0.5862±0.0115 | -0.0027 |
| EGSG_LC_hard | 0.4044±0.0169 | 0.7759±0.0154 | 0.5963±0.0089 | -0.0097 |
| RF+EGSG_residual | 0.4012±0.0155 | 0.7782±0.0222 | 0.5936±0.0162 | -0.0129 |
| MLP | 0.3834±0.0158 | 0.7895±0.0171 | 0.6048±0.0100 | -0.0306 |
| RF | 0.3678±0.0137 | 0.7996±0.0226 | 0.6142±0.0149 | -0.0463 |
| Geo_kNN | 0.3654±0.0069 | 0.8011±0.0181 | 0.6218±0.0109 | -0.0487 |

## 核心问题回答

### 1. Landcover-aware EGSG 是否优于 EGSG-250m？

**否**。最佳 LC 变体 EGSG_LC_soft_0.5 R²=0.4140 ≤ EGSG_250m R²=0.4141，ΔR²=-0.0000，p=0.996992 ns

### 2. Residual Graph Correction 是否优于 EGSG-250m？

**否**。MLP+EGSG_residual R²=0.4114 ≤ EGSG_250m R²=0.4141，ΔR²=-0.0027，p=0.595309 ns

### 3. 哪个方向更值得继续？

**两个方向均未超过 EGSG-250m**。

- 方向 A 最佳 ΔR²=-0.0000
- 方向 B 最佳 ΔR²=-0.0027

### 4. 是否维持 EGSG-250m 为封存方法？

**是**。所有候选方向均未超过 EGSG-250m，维持 EGSG-250m 为封存方法。

### 5. 后续是否应转向 SAR/canopy height/TCH 数据扩展？

当前图结构优化方向均无显著增益，建议转向**数据扩展**方向：

1. **ALOS PALSAR-2 L-band SAR**：烟测已显示 +5.5% R2 增益潜力
2. **Hansen TCH 树冠高度**：+1.8% R2，partial r=0.22 (p<1e-40)
3. **GEDI L3 冠层高度**：+1.0% R2（受 1km 分辨率限制）

数据扩展可能比图结构优化更有效地突破 R² ≈ 0.38 天花板。

## 输出文件

- 原始结果: `F:\pythoncode\大模型项目\融合图的训练\outputs\experiments\window_C_opportunity_scan_20260605_103628\raw_seed_results.csv`
- 配对比较: `F:\pythoncode\大模型项目\融合图的训练\outputs\experiments\window_C_opportunity_scan_20260605_103628\paired_comparison_results.csv`
- 图统计: `F:\pythoncode\大模型项目\融合图的训练\outputs\experiments\window_C_opportunity_scan_20260605_103628\graph_statistics.csv`
- 方向 A 报告: `F:\pythoncode\大模型项目\融合图的训练\outputs\experiments\window_C_opportunity_scan_20260605_103628\landcover_egsg_report.md`
- 方向 B 报告: `F:\pythoncode\大模型项目\融合图的训练\outputs\experiments\window_C_opportunity_scan_20260605_103628\residual_graph_correction_report.md`
- 图表: `F:\pythoncode\大模型项目\融合图的训练\outputs\experiments\window_C_opportunity_scan_20260605_103628\plots/`
