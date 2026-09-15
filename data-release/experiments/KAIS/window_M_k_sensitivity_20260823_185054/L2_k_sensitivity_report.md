# L2: k 邻居数敏感性分析报告

**时间戳**: 20260823_185054\n
**数据集**: 2021 单年 (6638 样本, 清洗后)

**k 值**: [5, 10, 15, 20]

**图类型**: Geo-GCN, EGSG-GCN (threshold=250m)

**Splits**: random (60/20/20), buffer_30km, elevation_high_holdout

**Seeds**: [42, 123, 2025, 7, 13, 37, 61, 73, 97, 101]

## 汇总表 ( R2)

| Split | Graph Type | k=5 | k=10 | k=15 | k=20 |
|-------|------------|-----|------|------|------|
| buffer_30km | Geo-GCN | -0.1065±0.0441 | -0.1378±0.0745 | -0.1589±0.0600 | -0.1519±0.0472 |
| buffer_30km | EGSG-GCN | -0.2040±0.0282 | -0.2228±0.0341 | -0.2422±0.0435 | -0.2544±0.0500 |
| elevation_high_holdout | Geo-GCN | -0.2334±0.0416 | -0.2666±0.0317 | -0.2726±0.0294 | -0.2581±0.0282 |
| elevation_high_holdout | EGSG-GCN | -0.2519±0.2151 | -0.3212±0.1731 | -0.2914±0.1404 | -0.3455±0.1983 |
| random | Geo-GCN | 0.3572±0.0239 | 0.3618±0.0186 | 0.3644±0.0180 | 0.3688±0.0177 |
| random | EGSG-GCN | 0.3950±0.0218 | 0.4095±0.0230 | 0.4160±0.0215 | 0.4239±0.0212 |

## EGSG 优势 (Delta  R2 = EGSG - Geo)

| Split | k | Delta  R2 | p-value | Significant |
|-------|---|----------|---------|-------------|
| buffer_30km | 5 | -0.0976 | 0.000009 | Yes |
| buffer_30km | 10 | -0.0851 | 0.001853 | Yes |
| buffer_30km | 15 | -0.0833 | 0.000242 | Yes |
| buffer_30km | 20 | -0.1025 | 0.000053 | Yes |
| elevation_high_holdout | 5 | -0.0186 | 0.810922 | No |
| elevation_high_holdout | 10 | -0.0546 | 0.339530 | No |
| elevation_high_holdout | 15 | -0.0188 | 0.693904 | No |
| elevation_high_holdout | 20 | -0.0874 | 0.193538 | No |
| random | 5 | +0.0378 | 0.000000 | Yes |
| random | 10 | +0.0477 | 0.000001 | Yes |
| random | 15 | +0.0517 | 0.000000 | Yes |
| random | 20 | +0.0551 | 0.000000 | Yes |

## 连通性分析

| Graph Type | k | Isolated Nodes (mean) | Mean Degree (mean) |
|------------|---|-----------------------|--------------------|
| Geo-GCN | 5 | 0.0 | 5.0 |
| Geo-GCN | 10 | 0.0 | 10.0 |
| Geo-GCN | 15 | 0.0 | 15.0 |
| Geo-GCN | 20 | 0.0 | 20.0 |
| EGSG-GCN | 5 | 43.0 | 4.6 |
| EGSG-GCN | 10 | 6.0 | 9.1 |
| EGSG-GCN | 15 | 3.0 | 13.6 |
| EGSG-GCN | 20 | 1.0 | 18.1 |

## 核心问题回答

### 1. EGSG 优势在不同 k 下是否稳定？

EGSG 在 4/12 个 (split, k) 组合中优于 Geo-GCN。

**结论**: EGSG 优势不稳定，多数情况下不优于 Geo-GCN。

### 2. k=10 是否是合理 tradeoff？

各 k 值下 EGSG 平均优势:

- k=5: mean delta  R2 = -0.0261
- k=10: mean delta  R2 = -0.0307
- k=15: mean delta  R2 = -0.0168
- k=20: mean delta  R2 = -0.0449

k=10 的优势 -0.0307。
最佳 k 值为 15 (基于平均 delta  R2)。

**结论**: k=15 略优于 k=10，但 k=10 仍是合理选择。

### 3. 小 k 是否导致连通性问题？

EGSG-GCN k=5: 平均孤立节点 = 43.0
EGSG-GCN k=10: 平均孤立节点 = 6.0
Geo-GCN k=5: 平均孤立节点 = 0.0

**结论**: 小 k 下孤立节点不多，连通性问题不严重。

### 4. 大 k 是否引入更多虚假连接？

从  R2 角度观察:

- Geo-GCN buffer_30km: k=5  R2=-0.1065, k=20  R2=-0.1519, diff=-0.0455
- EGSG-GCN buffer_30km: k=5  R2=-0.2040, k=20  R2=-0.2544, diff=-0.0504
- Geo-GCN elevation_high_holdout: k=5  R2=-0.2334, k=20  R2=-0.2581, diff=-0.0247
- EGSG-GCN elevation_high_holdout: k=5  R2=-0.2519, k=20  R2=-0.3455, diff=-0.0935
- Geo-GCN random: k=5  R2=0.3572, k=20  R2=0.3688, diff=+0.0116
- EGSG-GCN random: k=5  R2=0.3950, k=20  R2=0.4239, diff=+0.0289

在 3 个组合中观察到 k=20 相对 k=10 性能下降，提示大 k 可能引入虚假连接。

### 5. 改变 k 能否挽救 EGSG 在严格 split 下的表现？

各 split 下最优 k:

- buffer_30km: 最优 k=15, delta  R2=-0.0833
- elevation_high_holdout: 最优 k=5, delta  R2=-0.0186

**结论**: 改变 k 无法挽救 EGSG 在严格空间 split 下的表现，问题在于空间外推而非 k 选择。

