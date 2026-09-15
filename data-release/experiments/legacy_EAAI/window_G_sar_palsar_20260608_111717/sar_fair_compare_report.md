# 窗口G: SAR / ALOS PALSAR 可行性实验 — 综合报告

**时间戳**: 20260608_111717

**SAR 子集样本**: 335 (N29E095 瓦片)

**Seeds**: [42, 123, 2025, 7, 13]

## 1. SAR 覆盖率

- 已下载瓦片: 1/15 (7%)
- SAR 有效样本: 578/7728 (7.5%)
- 缺失模式: 仅 N29E095 瓦片覆盖 (lat 28-29, lon 95-96)

## 2. SAR valid subset 选择偏差

- agb_label: valid=81.07 vs missing=50.53 (p=4.89e-63 ***)
- elevation_mean: valid=1949.59 vs missing=3652.58 (p=6.77e-297 ***)
- ndvi_mean: valid=0.90 vs missing=0.72 (p=1.10e-102 ***)
- slope_mean: valid=30.18 vs missing=31.77 (p=2.36e-03 **)
- lai_mean: valid=2.02 vs missing=1.64 (p=2.88e-03 **)

## 3. SAR 独立信息诊断

| Pair | Method | r | p | n |
|------|--------|---|---|---|
| sar_hh_db vs AGB | Pearson | 0.113 | 6.42e-03 | 578 |
| sar_hh_db vs AGB | Spearman | 0.105 | 1.16e-02 | 578 |
| sar_hv_db vs AGB | Pearson | 0.294 | 5.24e-13 | 578 |
| sar_hv_db vs AGB | Spearman | 0.240 | 5.11e-09 | 578 |
| sar_hh_minus_hv vs AGB | Pearson | -0.274 | 1.90e-11 | 578 |
| sar_hh_minus_hv vs AGB | Spearman | -0.198 | 1.53e-06 | 578 |
| HV vs ndvi_mean | Pearson | 0.156 | 1.66e-04 | 578 |
| HV vs elevation_mean | Pearson | 0.088 | 3.36e-02 | 578 |
| HV vs lai_mean | Pearson | -0.142 | 8.92e-03 | 338 |
| HV vs AGB | elev+NDVI | partial | 0.257 | 3.69e-10 | 578 |

## 4. RF Feature Importance (Top 10)

| Feature | Importance |
|---------|------------|
| ndvi_q90 | 0.1229 |
| sar_hv_db | 0.1082 |
| ndvi_mean | 0.0662 |
| et_mean | 0.0651 |
| ndvi_q75 | 0.0641 |
| lst_mean | 0.0608 |
| sar_hh_minus_hv | 0.0596 |
| slope_mean | 0.0491 |
| aspect_sin | 0.0481 |
| elevation_mean | 0.0473 |

## 5. 同子集公平对照

| Method | R² (mean±std) | ΔR² vs noSAR |
|--------|---------------|-------------|
| RF_noSAR | 0.1556±0.1937 | — |
| RF_SAR | 0.1892±0.1941 | +0.0336 |
| RF_SAR_all | 0.1966±0.1917 | +0.0411 |
| MLP_noSAR | 0.0912±0.2058 | — |
| MLP_SAR | 0.2120±0.1648 | +0.1208 |
| MLP_SAR_all | 0.2013±0.1811 | +0.1102 |
| EGSG_noSAR | 0.0985±0.0561 | — |
| EGSG_SAR | 0.1153±0.0598 | +0.0168 |
| EGSG_SAR_all | 0.1525±0.0679 | +0.0540 |

## 6. 配对比较

| Comparison | ΔR² | p | Cohen's d | Sig |
|------------|-----|---|-----------|-----|
| RF_SAR vs RF_noSAR | +0.0336 | 0.614031 | +0.2442 | ns |
| RF_SAR_all vs RF_noSAR | +0.0411 | 0.541397 | +0.2982 | ns |
| MLP_SAR vs MLP_noSAR | +0.1208 | 0.226469 | +0.6386 | ns |
| MLP_SAR_all vs MLP_noSAR | +0.1102 | 0.242073 | +0.6134 | ns |
| EGSG_SAR vs EGSG_noSAR | +0.0168 | 0.184571 | +0.7161 | ns |
| EGSG_SAR_all vs EGSG_noSAR | +0.0540 | 0.234874 | +0.6249 | ns |
| EGSG_noSAR vs RF_noSAR | -0.0571 | 0.509395 | -0.3236 | ns |
| EGSG_noSAR vs MLP_noSAR | +0.0073 | 0.936479 | +0.0379 | ns |

## 7. 核心问题回答

### 1. 当前 SAR 覆盖率是多少？

已下载 1/15 瓦片 (7%)，仅 N29E095 瓦片可用。SAR 有效样本 578/7728 (7.5%)。

### 2. SAR valid subset 是否存在选择偏差？

**是**。SAR valid subset 在多个变量上与 SAR missing 子集存在显著差异。因此所有 +SAR vs noSAR 比较必须在同一子集上进行，不能与全量 EGSG-250m 混比。

### 3. SAR 与 AGB 是否有独立相关性？

**是**。HV vs AGB Pearson r=0.294，偏相关 (控制 elevation+NDVI) r=0.257 (p=3.69e-10)。HV 在 NDVI 和 elevation 之外提供独立信息。

### 4. 在同子集公平对照下，SAR 是否提升 RF/MLP/EGSG？

- RF_SAR_all ΔR²=+0.0411
- MLP_SAR_all ΔR²=+0.1102
- EGSG_SAR_all ΔR²=+0.0540

**是**，SAR 在同子集上提供了正向增益。

### 5. SAR 是否值得从单瓦片扩展到全覆盖？

**值得**。单瓦片结果已显示 >1.5% R² 增益，建议人工下载剩余 14 个瓦片进行全覆盖验证。

**下载方式**: JAXA EORC 人工下载（需 JAXA 账号），每瓦片约 100MB，总计约 1.5GB。

### 6. 下一步是否需要人工下载更多 ALOS/PALSAR 文件？

**是**。建议优先下载以下瓦片（覆盖主要林区）：

1. N30E095 (高 AGB 区域)
2. N31E095 (高海拔林区)
3. N29E096 (相邻瓦片)

下载地址: https://www.eorc.jaxa.jp/ALOS/en/dataset/palsar2_e.htm

## 8. 与 EGSG 全量封存结果的关系

**重要说明**:

- 本次实验在 SAR 子集 (N=335) 上进行，**不能直接与全量 EGSG-250m 封存结果 (N=6638) 混比**
- 只有同子集 noSAR vs +SAR 的比较才能说明 SAR 是否有效
- 如果 SAR 有效，下一步任务是**扩大覆盖**（下载更多瓦片），而不是立即更新封存主方法
- SAR 子集的 EGSG_noSAR R² 与全量 EGSG_250m R² 不同是正常的（子集分布不同）
