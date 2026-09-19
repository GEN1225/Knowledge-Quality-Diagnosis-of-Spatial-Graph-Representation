# 窗口M — buffer 尺寸扫描（exp_043，KAIS 缺口 B1）

**日期**: 20260824_135305
**状态**: completed

## 结果（10 seeds, mean±std）

| split | 方法 | R² |
|-------|------|-----|
| random | EGSG-GCN | +0.4095±0.0230 |
| random | Geo-GCN | +0.3618±0.0186 |
| buffer_10km | EGSG-GCN | -0.1432±0.0397 |
| buffer_10km | Geo-GCN | -0.1340±0.0447 |
| buffer_20km | EGSG-GCN | -0.1519±0.0297 |
| buffer_20km | Geo-GCN | -0.1353±0.0335 |
| buffer_30km | EGSG-GCN | -0.1906±0.0337 |
| buffer_30km | Geo-GCN | -0.1367±0.0750 |
| buffer_50km | EGSG-GCN | -0.2232±0.0595 |
| buffer_50km | Geo-GCN | -0.1403±0.0616 |
| buffer_80km | EGSG-GCN | -0.2390±0.0600 |
| buffer_80km | Geo-GCN | -0.1220±0.0635 |

## ΔR² 与 LSI 曲线

| buffer | ΔR²(EGSG-Geo) | p | LSI | n_train | n_test |
|--------|----------------|----|-----|---------|--------|
| buffer_10km | -0.0091 | 0.4782 | 2.3 | 5467 | 1042 |
| buffer_20km | -0.0166 | 0.2117 | 0.4 | 5334 | 1042 |
| buffer_30km | -0.0539 | 0.0267 | 0.0 | 5217 | 1042 |
| buffer_50km | -0.0829 | 0.0066 | 0.0 | 4917 | 1042 |
| buffer_80km | -0.1170 | 0.0000 | 0.0 | 4433 | 1042 |

## 锚点检查（3-seed 子集 vs exp_034 封存修复值）

```
  buffer30 EGSG-GCN   本协议3seed=-0.1990 封存=-0.2190 Δ=+0.0200 [OK]
  buffer30 Geo-GCN    本协议3seed=-0.1302 封存=-0.1290 Δ=-0.0012 [OK]
  buffer50 EGSG-GCN   本协议3seed=-0.2142 封存=-0.2410 Δ=+0.0268 [OK]
  buffer50 Geo-GCN    本协议3seed=-0.1301 封存=-0.1190 Δ=-0.0111 [OK]
```

## 判读

- ΔR² 随 buffer 的曲线给出失效边界的相位图；LSI 曲线给出机制轴。
- 注：LSI 为结构性诊断（train 区全量，与 seed 无关）；buffer 增大时 train 区缩小，LSI 与 n_train 联动。