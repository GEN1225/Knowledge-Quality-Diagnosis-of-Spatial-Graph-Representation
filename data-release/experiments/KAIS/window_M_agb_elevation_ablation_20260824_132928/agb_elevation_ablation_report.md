# 窗口M — AGB 高程特征消融（exp_040，KAIS 缺口 A3）

**日期**: 20260824_133645
**状态**: completed

## 结果（10 seeds, mean±std）

| 方法 | R² |
|------|-----|
| MLP_full | +0.3781±0.0213 |
| MLP_noelev | +0.3439±0.0254 |
| RF_full | +0.3640±0.0230 |
| RF_noelev | +0.3158±0.0252 |
| Geo_noelev | +0.3401±0.0185 |
| EGSG_noelev | +0.3998±0.0251 |

- 高程特征边际贡献: MLP +0.0342 / RF +0.0482
- **EGSG 拓扑恢复率: 163.6%**；Geo 拓扑恢复率: -11.0%
- EGSG_noelev vs Geo_noelev 配对: ΔR²=+0.0597, p=0.000000

## 锚点核验

- MLP_full: 本实验 +0.3781 vs 封存 +0.3781
- RF_full: 本实验 +0.3640 vs 封存 +0.3640

## 判定

- EGSG_noelev 显著优于 Geo_noelev 且恢复率高 → 门控拓扑本身编码地形知识（主目标证据成立）
- EGSG_noelev ≈ Geo_noelev → AGB 上拓扑增益依赖 elevation 特征在图中传递（与 LST 不同，如实记录）