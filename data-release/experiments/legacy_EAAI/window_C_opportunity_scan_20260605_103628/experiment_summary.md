# 实验结果总结：机会扫描 (exp_003)

> 实验时间：2026-06-05
> 实验状态：completed
> 实验目的：验证 Landcover-aware EGSG 和 Residual Correction 两条路线的有效性

---

## 一、实验背景

基于 EGSG_250m（R²=0.4141）的封存方法，探索两条改进路线：

1. **方向 A：Landcover-aware EGSG** - 利用土地覆盖信息优化图构建
2. **方向 B：Residual Graph Correction** - 用 EGSG 修正 ML 模型残差

---

## 二、实验结果

### 2.1 图统计

| Graph | Undirected Edges | Mean Degree | LC Mismatch Ratio | Mean |ΔAGB| | P90 |ΔAGB| |
|-------|------------------|-------------|-------------------|------------|---------|
| Geo_kNN | 38,060 | 10.0 | — | 33.4 | 76.0 |
| EGSG_250m | 35,274 | 9.1 | — | 30.7 | 71.0 |
| EGSG_LC_soft_0.25 | 35,274 | 9.1 | 37.5% | 30.7 | 71.0 |
| EGSG_LC_soft_0.5 | 35,274 | 9.1 | 37.5% | 30.7 | 71.0 |
| EGSG_LC_soft_0.75 | 35,274 | 9.1 | 37.5% | 30.7 | 71.0 |
| EGSG_LC_hard | 29,605 | 7.6 | 47.4% | 29.4 | 68.0 |

### 2.2 方向 A：Landcover-aware EGSG

| Seed | RF | MLP | Geo_kNN | EGSG_250m | LC_soft_0.25 | LC_soft_0.5 | LC_soft_0.75 | LC_hard |
|------|-----|-----|---------|-----------|--------------|-------------|--------------|---------|
| 42 | 0.3725 | 0.3758 | 0.3625 | 0.4017 | 0.4099 | 0.4053 | 0.4050 | 0.3924 |
| 123 | 0.3548 | 0.3864 | 0.3688 | 0.4249 | 0.4178 | 0.4178 | 0.4234 | 0.4161 |
| 2025 | 0.3522 | 0.3610 | 0.3558 | 0.3825 | 0.3866 | 0.3884 | 0.3854 | 0.3808 |
| 7 | 0.3754 | 0.3915 | 0.3655 | 0.4308 | 0.4314 | 0.4335 | 0.4324 | 0.4133 |
| 13 | 0.3839 | 0.4024 | 0.3741 | 0.4304 | 0.4242 | 0.4251 | 0.4233 | 0.4193 |
| **Mean** | **0.3678** | **0.3834** | **0.3654** | **0.4141** | **0.4140** | **0.4140** | **0.4139** | **0.4044** |
| Std | 0.0137 | 0.0158 | 0.0069 | 0.0213 | 0.0173 | 0.0177 | 0.0188 | 0.0169 |

### 2.3 方向 B：Residual Graph Correction

| Seed | RF | MLP | EGSG_250m | RF+EGSG_res | MLP+EGSG_res |
|------|-----|-----|-----------|-------------|--------------|
| 42 | 0.3725 | 0.3758 | 0.4017 | 0.4024 | 0.3940 |
| 123 | 0.3548 | 0.3864 | 0.4249 | 0.3893 | 0.4172 |
| 2025 | 0.3522 | 0.3610 | 0.3825 | 0.3821 | 0.3985 |
| 7 | 0.3754 | 0.3915 | 0.4308 | 0.4141 | 0.4236 |
| 13 | 0.3839 | 0.4024 | 0.4304 | 0.4179 | 0.4234 |
| **Mean** | **0.3678** | **0.3834** | **0.4141** | **0.4012** | **0.4114** |
| Std | 0.0137 | 0.0158 | 0.0213 | 0.0155 | 0.0141 |

---

## 三、配对比较结果

### 3.1 R² 指标

| Comparison | Mean Diff | p(t-test) | p(Wilcoxon) | Cohen's d | Sig |
|------------|-----------|-----------|-------------|-----------|-----|
| RF vs EGSG_250m | -0.0463 | 0.003929 | 0.0625 | -2.6747 | ** |
| MLP vs EGSG_250m | -0.0306 | 0.000995 | 0.0625 | -3.8561 | *** |
| Geo_kNN vs EGSG_250m | -0.0487 | 0.002184 | 0.0625 | -3.1337 | ** |
| EGSG_LC_soft_0.25 vs EGSG_250m | -0.0001 | 0.981004 | 1.0 | -0.0113 | ns |
| EGSG_LC_soft_0.5 vs EGSG_250m | -0.0000 | 0.996992 | 1.0 | -0.0018 | ns |
| EGSG_LC_soft_0.75 vs EGSG_250m | -0.0002 | 0.937100 | 0.8125 | -0.0376 | ns |
| EGSG_LC_hard vs EGSG_250m | -0.0097 | 0.018479 | 0.0625 | -1.7167 | * |
| RF+EGSG_residual vs EGSG_250m | -0.0129 | 0.122341 | 0.1875 | -0.8740 | ns |
| MLP+EGSG_residual vs EGSG_250m | -0.0027 | 0.595309 | 0.625 | -0.2577 | ns |

### 3.2 RMSE 指标

| Comparison | Mean Diff | p(t-test) | Cohen's d | Sig |
|------------|-----------|-----------|-----------|-----|
| RF vs EGSG_250m | +0.0300 | 0.004739 | +2.5406 | ** |
| MLP vs EGSG_250m | +0.0199 | 0.001249 | +3.6326 | *** |
| Geo_kNN vs EGSG_250m | +0.0315 | 0.002595 | +2.9921 | ** |
| EGSG_LC_hard vs EGSG_250m | +0.0064 | 0.018241 | +1.7235 | * |
| RF+EGSG_residual vs EGSG_250m | +0.0086 | 0.122934 | +0.8721 | ns |
| MLP+EGSG_residual vs EGSG_250m | +0.0019 | 0.570800 | +0.2758 | ns |

### 3.3 MAE 指标

| Comparison | Mean Diff | p(t-test) | Cohen's d | Sig |
|------------|-----------|-----------|-----------|-----|
| RF vs EGSG_250m | +0.0230 | 0.007206 | +2.2607 | ** |
| MLP vs EGSG_250m | +0.0136 | 0.011614 | +1.9715 | * |
| Geo_kNN vs EGSG_250m | +0.0306 | 0.000561 | +4.4744 | *** |
| EGSG_LC_hard vs EGSG_250m | +0.0052 | 0.025943 | +1.5450 | * |
| MLP+EGSG_residual vs EGSG_250m | -0.0049 | 0.231837 | -0.6298 | ns |

---

## 四、结论

### 4.1 核心发现

| 问题 | 回答 |
|------|------|
| Landcover-aware EGSG 是否优于 EGSG_250m？ | 否。最佳 LC 变体 EGSG_LC_soft_0.5 ΔR²=-0.0000，p=0.997 ns |
| Residual correction 是否优于 EGSG_250m？ | 否。MLP+EGSG_residual ΔR²=-0.0027，p=0.595 ns |
| 哪个方向更值得继续？ | 均不值得。方向 A ΔR²=-0.0000，方向 B ΔR²=-0.0027 |
| 是否维持 EGSG_250m 为封存方法？ | 是 |
| 后续是否应转向数据扩展？ | 是。建议转向 ALOS PALSAR SAR / Hansen TCH / GEDI |

### 4.2 关键发现

1. **EGSG_250m 保持最优**：R²=0.4141，显著优于 RF/MLP/Geo_kNN
2. **Landcover 信息无效**：LC_soft 变体与 EGSG_250m 无显著差异
3. **Hard LC 过度剪枝**：LC_hard 显著低于 EGSG_250m（ΔR²=-0.0097，p=0.018）
4. **Residual correction 无效**：MLP+EGSG_res 与 EGSG_250m 无显著差异

### 4.3 后续建议

1. **数据扩展**：获取 ALOS PALSAR SAR、Hansen TCH、GEDI 等结构变量
2. **空间泛化实验**：设计 spatial holdout 验证 EGSG 鲁棒性
3. **论文定位**：从精度提升转向复杂地形空间泛化改进

---

## 五、输出文件

```
outputs/experiments/window_C_opportunity_scan_20260605_103628/
├── raw_seed_results.csv                 # 50 行 (10 方法 × 5 seeds)
├── paired_comparison_results.csv        # 27 行 (9 比较 × 3 指标)
├── graph_statistics.csv                 # 7 行 (7 种图)
├── landcover_egsg_report.md
├── residual_graph_correction_report.md
├── opportunity_scan_summary.md
├── experiment_summary.md                # 本文件
└── plots/
    ├── r2_boxplot_all.png
    ├── direction_a_comparison.png
    └── direction_b_comparison.png
```

---

*实验编号：exp_003*
*最后更新：2026-06-05*
