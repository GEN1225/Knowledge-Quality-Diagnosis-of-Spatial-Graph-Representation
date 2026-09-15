# 窗口D: Canopy Height / TCH 同子集公平对照报告

**时间戳**: 20260608_101316

**数据集**: 2021 TCH overlay (8000 样本)

**Clean protocol**: train-only scaler, val-based early stopping, 5 seeds

## 1. 子集定义

| 子集 | 样本数 | 说明 |
|------|--------|------|
| full_dataset | 6638 | base_valid 全量 |
| tch_valid_subset | 3686 | TCH 有效 |
| tch_missing_subset | 2952 | TCH 缺失 |
| gedi_valid_subset | 3948 | GEDI 有效 |
| both_valid_subset | 2023 | TCH+GEDI 均有效 |

## 2. Missingness Bias 诊断

| 指标 | Full | TCH valid | TCH missing | p(valid vs missing) |
|------|------|-----------|-------------|---------------------|
| full | n=6638 | AGB=50.9±41.7 | elev=3652±957 | NDVI=0.730±0.198 |
| tch_valid | n=3686 | AGB=69.2±40.1 | elev=3188±916 | NDVI=0.859±0.067 |
| tch_missing | n=2952 | AGB=28.1±31.1 | elev=4232±636 | NDVI=0.568±0.187 |

**AGB 差异**: tch_valid=69.2, tch_missing=28.1, diff=41.1, p=0.00e+00
**Elevation 差异**: tch_valid=3188, tch_missing=4232, diff=-1045m, p=0.00e+00
**NDVI 差异**: tch_valid=0.859, tch_missing=0.568, diff=0.291, p=0.00e+00

## 3. 同子集公平对照结果

| 方法 | 子集 | R² (mean±std) | 样本数 |
|------|------|---------------|--------|
| RF_noCH | tch_valid | 0.2373±0.0238 | 3686 |
| RF_CH | tch_valid | 0.2465±0.0282 | 3686 |
| MLP_noCH | tch_valid | 0.2376±0.0335 | 3686 |
| MLP_CH | tch_valid | 0.2656±0.0271 | 3686 |
| Geo_kNN_noCH | tch_valid | 0.2828±0.0274 | 3686 |
| EGSG_noCH | tch_valid | 0.3130±0.0359 | 3686 |
| EGSG_CH | tch_valid | 0.3066±0.0440 | 3686 |
| EGSG_CH_3x3 | tch_valid | 0.3055±0.0436 | 3686 |
| EGSG_noCH_GEDI_sub | gedi_valid | 0.3841±0.0307 | 3948 |
| EGSG_GEDI | gedi_valid | 0.3973±0.0407 | 3948 |
| EGSG_CH_GEDI | gedi_valid | 0.2828±0.0402 | 2023 |

## 4. 配对比较

| 比较 | 子集 | ΔR² | Paired t p | Cohen's d | Sig |
|------|------|-----|------------|-----------|-----|
| RF_CH vs RF_noCH | tch_valid | +0.0091 | 0.126089 | +0.8623 | ns |
| MLP_CH vs MLP_noCH | tch_valid | +0.0280 | 0.009910 | +2.0644 | ** |
| EGSG_CH vs EGSG_noCH | tch_valid | -0.0064 | 0.310992 | -0.5182 | ns |
| EGSG_CH_3x3 vs EGSG_noCH | tch_valid | -0.0075 | 0.223127 | -0.6443 | ns |
| EGSG_GEDI vs EGSG_noCH_GEDI_sub | gedi_valid | +0.0132 | 0.105723 | +0.9313 | ns |
| EGSG_CH_GEDI vs EGSG_noCH_GEDI_sub | gedi_valid | -0.1013 | 0.029863 | -1.4769 | * |

## 5. 核心问题回答

### 5.1 第一次和第二次为什么结果不一致？

第一次扫描将 +TCH (3686 样本) 与全量 baseline (6638 样本) 直接比较 R²，但 TCH 有效子集存在严重选择偏差：
- AGB: tch_valid=69.2 vs tch_missing=28.1 (diff=41.1)
- Elevation: tch_valid=3188 vs tch_missing=4232 (diff=-1045m)
- NDVI: tch_valid=0.859 vs tch_missing=0.568
TCH 子集偏向低海拔、高 AGB、高 NDVI 的森林区，分布与全量样本差异显著。不同子集上 baseline R² 不同，直接比较 R² 绝对值会产生误导。

### 5.2 TCH valid subset 是否存在选择偏差？

**是，存在显著选择偏差**。TCH 有效子集的 AGB 均值 (69.2) 显著高于 TCH 缺失子集 (28.1)，差异 41.1 Mg/ha (p=0.00e+00)。

### 5.3 在同一 TCH-valid 子集上，TCH 是否显著提升？

**EGSG_CH vs EGSG_noCH**: ΔR²=-0.0064, p=0.310992。**未达到显著**。
**RF_CH vs RF_noCH**: ΔR²=+0.0091, p=0.126089。未显著。
**MLP_CH vs MLP_noCH**: ΔR²=+0.0280, p=0.009910。显著。

### 5.4 GEDI 1km 是否有实际增益？

**EGSG_GEDI vs EGSG_noCH_GEDI_sub**: ΔR²=+0.0132, p=0.105723。未显著。

GEDI L3 1km 由于空间分辨率较粗，在当前样本尺度下只适合作为辅助结构背景变量，不建议作为主特征。

### 5.5 是否可以更新 EGSG 封存方法？

TCH 的表观增益主要受到有效覆盖子集选择偏差影响，当前不能作为全量 EGSG 的可靠升级依据。维持 EGSG-250m 封存结论不变。

### 5.6 是否值得继续扩展 TCH/SAR/canopy height 方向？

当前 TCH (30m) 和 GEDI (1km) 的独立增益有限。未来可考虑：
1. 获取 ALOS PALSAR-2 全覆盖数据（单瓦片增益 +4.3%）
2. 使用 GEDI L2A 足迹级数据（25m，但下载量 47GB）
3. 多源结构变量整合（SAR + TCH + GEDI）
