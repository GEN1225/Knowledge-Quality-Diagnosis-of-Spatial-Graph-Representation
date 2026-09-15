# 窗口M — GWR/克里金经典空间基线（exp_044，KAIS 缺口 B2）

**日期**: 20260824_140804
**状态**: completed

**GWR**: mgwr gaussian 固定带宽 100.0 km, spherical, 16 特征, 截距内置
**克里金**: pykrige 普通克里金 spherical 变异函数, 地理坐标, 支撑集 800 随机 train 点（可行性降级，报告注明）

## 结果（random 10 seeds / buffer_30 确定性）

| split | 方法 | R² |
|-------|------|-----|
| random | GWR | +0.3376±0.0211 |
| random | Kriging | +0.3252±0.0242 |
| buffer_30km | GWR | -0.1909±0.0000 |
| buffer_30km | Kriging | -1.1691±0.0000 |

## 与 exp_034 参考值对比

| split | GWR | Kriging | EGSG-GCN | Geo-GCN | RF | MLP |
|-------|-----|---------|----------|---------|----|-----|
| random | +0.3376 | +0.3252 | +0.4095 | +0.3618 | 0.364 | 0.3781 |
| buffer_30km | -0.1909 | -1.1691 | -0.1906 | -0.1367 | -0.1594 | -0.0796 |

## 退化判定

- GWR: random +0.3376 → buffer_30 -0.1909（退化 +0.5284）
- Kriging: random +0.3252 → buffer_30 -1.1691（退化 +1.4943）
- 若两者 buffer 下均大幅退化 → 『严格外推失效是所有局部空间方法的共性』成立，EGSG 边界主张非 GNN 特有。
- 若 GWR/克里金 buffer 下不退化 → EGSG 的失效边界是 GNN 特有现象，论文定位需改写（如实记录）。