# 窗口M — buffer/elevation split 扩 10 seeds 报告（跨区边删除协议，KAIS 修改策略第 3 项）

**日期**: 20260823_200451
**状态**: completed
**协议**: 跨区边删除（删除 test↔非test 边，保留 test 区内边与非 test 区边）；scaler 仅 train fit；
early stopping 在 val；val 按 seed 从 train 区划分（0.25）；10 seeds [42, 123, 2025, 7, 13, 37, 61, 73, 97, 101]
**样本数**: 6638（与封存协议一致）
**与 exp_033 的关系**: exp_033 = 变体A（完全隔离 test 节点）；本实验 = 变体B（跨区边删除）。
封存修复值锚点检查结果见第 3 节。

## 1. 结果汇总（10 seeds, mean±std）

| split | 方法 | R² | RMSE | MAE | 收敛轮数(mean ep) | 退化 vs random |
|-------|------|-----|------|-----|-------------------|----------------|
| random | RF | +0.3640±0.0230 | 0.7967 | 0.6118 | - | +0.0000 |
| random | MLP | +0.3781±0.0213 | 0.7878 | 0.6033 | 238 | +0.0000 |
| random | Geo-GCN | +0.3618±0.0186 | 0.7981 | 0.6195 | 287 | +0.0000 |
| random | EGSG-GCN | +0.4095±0.0230 | 0.7676 | 0.5884 | 295 | +0.0000 |
| buffer_30km | RF | -0.1594±0.0259 | 0.7012 | 0.5820 | - | +0.5235 |
| buffer_30km | MLP | -0.0796±0.0171 | 0.6767 | 0.5422 | 234 | +0.4577 |
| buffer_30km | Geo-GCN | -0.1367±0.0750 | 0.6941 | 0.5706 | 263 | +0.4985 |
| buffer_30km | EGSG-GCN | -0.1906±0.0337 | 0.7106 | 0.5698 | 294 | +0.6000 |
| buffer_50km | RF | -0.1846±0.0347 | 0.7275 | 0.6048 | - | +0.5486 |
| buffer_50km | MLP | -0.0828±0.0203 | 0.6956 | 0.5603 | 219 | +0.4609 |
| buffer_50km | Geo-GCN | -0.1403±0.0616 | 0.7136 | 0.5889 | 247 | +0.5020 |
| buffer_50km | EGSG-GCN | -0.2232±0.0595 | 0.7392 | 0.5903 | 297 | +0.6327 |
| elev_high | RF | -0.3578±0.0863 | 0.7742 | 0.6669 | - | +0.7218 |
| elev_high | MLP | -0.0897±0.0266 | 0.6938 | 0.5308 | 208 | +0.4678 |
| elev_high | Geo-GCN | -0.4486±0.2127 | 0.7981 | 0.5566 | 273 | +0.8103 |
| elev_high | EGSG-GCN | -0.5170±0.3879 | 0.8133 | 0.5874 | 293 | +0.9264 |

## 2. 协议复刻检查（random 参考组）

- EGSG-GCN random: R²=0.4095±0.0230（封存参考 0.4097±0.0230）

## 3. 锚点检查（3-seed 子集 vs 封存修复值）

```
  buffer_30km  EGSG-GCN   本协议3seed=-0.1990  封存=-0.2190 Δ=+0.0200 [OK]
  buffer_30km  Geo-GCN    本协议3seed=-0.1302  封存=-0.1290 Δ=-0.0012 [OK]
  buffer_50km  EGSG-GCN   本协议3seed=-0.2142  封存=-0.2410 Δ=+0.0268 [OK]
  buffer_50km  Geo-GCN    本协议3seed=-0.1301  封存=-0.1190 Δ=-0.0111 [OK]
  elev_high    EGSG-GCN   本协议3seed=-0.6498  封存=-0.4800 Δ=-0.1698 [CHECK]
  elev_high    Geo-GCN    本协议3seed=-0.4440  封存=-0.2590 Δ=-0.1850 [CHECK]
```

锚点结论: 存在 |Δ|≥0.15 项，需进一步核对协议

## 4. 核心检验（配对 10 seeds）

- EGSG vs Geo-GCN buffer_30: ΔR²=-0.0539，p=0.026671（*），d=-0.8366
- EGSG vs Geo-GCN buffer_50: ΔR²=-0.0829，p=0.006641（**），d=-1.1093
- EGSG vs Geo-GCN elev_high: ΔR²=-0.0684，p=0.594388（ns），d=-0.1746
- EGSG 退化幅度: buffer_30 +0.6000 / buffer_50 +0.6327 / elev_high +0.9264

## 5. 结论

- 10-seed 统计功效下的边界主张（跨区边删除协议，与封存修复意图一致）。
- 论文口径：EGSG 适用边界为 random split / 局部空间插值，不声明严格空间外推能力。

## 6. 输出文件

- buffer_split_strict_10seeds_raw.csv / _summary.csv / _paired.csv
- plots/fig_spatial_strict_10seeds_r2.png, plots/fig_egsg_gain_by_split_strict_10seeds.png
