# 方向 B: Residual Graph Correction 报告

**时间戳**: 20260605_103628

**Seeds**: [42, 123, 2025, 7, 13]

## 实验设计

1. 训练 RF/MLP 基模型，获得 train/val/test 预测
2. 计算残差: residual = y_true - y_base_pred (仅 train 和 val)
3. 用 EGSG 图训练 GCN 预测残差，val 用于 early stopping
4. 最终预测: y_final = y_base_pred + residual_gcn_pred

## 方法对比

| Method | R² (mean±std) | RMSE (mean±std) | MAE (mean±std) | ΔR² vs EGSG_250m |
|--------|---------------|-----------------|----------------|------------------|
| RF | 0.3678±0.0137 | 0.7996±0.0226 | 0.6142±0.0149 | -0.0463 |
| MLP | 0.3834±0.0158 | 0.7895±0.0171 | 0.6048±0.0100 | -0.0306 |
| EGSG_250m | 0.4141±0.0213 | 0.7696±0.0176 | 0.5912±0.0113 | +0.0000 |
| RF+EGSG_residual | 0.4012±0.0155 | 0.7782±0.0222 | 0.5936±0.0162 | -0.0129 |
| MLP+EGSG_residual | 0.4114±0.0141 | 0.7714±0.0164 | 0.5862±0.0115 | -0.0027 |

## 配对比较 (vs EGSG_250m, R²)

| Comparison | Mean Diff | p(t-test) | p(Wilcoxon) | Cohen's d | Sig |
|------------|-----------|-----------|-------------|-----------|-----|
| RF+EGSG_residual vs EGSG_250m | -0.0129 | 0.122341 | 0.187500 | -0.8740 | ns |
| MLP+EGSG_residual vs EGSG_250m | -0.0027 | 0.595309 | 0.625000 | -0.2577 | ns |

## 结论

**最佳 Residual 变体**: MLP+EGSG_residual (R²=0.4114)，未超过 EGSG_250m (R²=0.4141)，ΔR²=-0.0027

