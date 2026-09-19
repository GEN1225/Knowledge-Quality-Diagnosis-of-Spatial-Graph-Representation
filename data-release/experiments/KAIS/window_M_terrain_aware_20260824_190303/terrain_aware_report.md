# 窗口M — terrain-aware 深度学习方法对比（exp_048）

**日期**: 20260824_202654
**状态**: completed

## 结果（10 seeds, mean±std）

| split | 方法 | R² |
|-------|------|-----|
| random | Geo-GCN | +0.3618±0.0186 |
| random | EGSG-GCN | +0.4095±0.0230 |
| random | SoftG-GCN | +0.4057±0.0236 |
| random | ElevEdge-NNConv | +0.4173±0.0218 |
| random | ElevGAT-GATv2 | +0.4036±0.0259 |
| random | Elev3D-GCN | +0.3676±0.0185 |
| buffer_30km | Geo-GCN | -0.1367±0.0750 |
| buffer_30km | EGSG-GCN | -0.1906±0.0337 |
| buffer_30km | SoftG-GCN | -0.2146±0.0332 |
| buffer_30km | ElevEdge-NNConv | -0.1229±0.0730 |
| buffer_30km | ElevGAT-GATv2 | -0.0934±0.0503 |
| buffer_30km | Elev3D-GCN | -0.1700±0.0513 |

## 配对检验 vs Geo-GCN

| split | 方法 | ΔR² vs Geo | p |
|-------|------|------------|---|
| random | EGSG-GCN | +0.0477 | 0.0000 |
| random | SoftG-GCN | +0.0439 | 0.0000 |
| random | ElevEdge-NNConv | +0.0555 | 0.0000 |
| random | ElevGAT-GATv2 | +0.0418 | 0.0000 |
| random | Elev3D-GCN | +0.0058 | 0.0067 |
| buffer_30km | EGSG-GCN | -0.0539 | 0.0267 |
| buffer_30km | SoftG-GCN | -0.0779 | 0.0085 |
| buffer_30km | ElevEdge-NNConv | +0.0138 | 0.6794 |
| buffer_30km | ElevGAT-GATv2 | +0.0433 | 0.1463 |
| buffer_30km | Elev3D-GCN | -0.0333 | 0.1057 |

## 锚点检查

```
  random Geo-GCN    本协议=+0.3618 封存=+0.3618 Δ=-0.0000 [OK]
  random EGSG-GCN   本协议=+0.4095 封存=+0.4095 Δ=-0.0000 [OK]
  b30 Geo-GCN    本协议3seed=-0.1302 封存=-0.1290 Δ=-0.0012 [OK]
  b30 EGSG-GCN   本协议3seed=-0.1990 封存=-0.2190 Δ=+0.0200 [OK]
```

anchor_ok=True

## 判读

- random：terrain-aware 软机制（SoftG/NNConv/GATv2/3D）能否达到硬门控水平 → 硬门控归纳偏置的价值
- buffer30：外推 regime 下各地形感知机制的退化模式 → 边界主张的扩展