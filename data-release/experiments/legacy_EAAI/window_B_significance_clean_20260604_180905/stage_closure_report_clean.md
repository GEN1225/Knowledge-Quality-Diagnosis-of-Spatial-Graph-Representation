# EGSG 高程门控空间图阶段封存报告 (Clean Protocol)

**版本**: 正式封存版 (clean protocol)

**时间戳**: 20260604_180905

## 重要声明

- 旧版结果 (commit 2dcfcf0) 为 pre-clean 版本，存在 StandardScaler 数据泄露和 test-set early stopping，**不作为最终论文引用数值**
- 本报告为 clean protocol 版本，scaler 仅在 train 上 fit，early stopping 在 val set 上进行

## 最终结果

| 方法 | R² (mean±std) | RMSE (mean±std) | MAE (mean±std) |
|------|---------------|-----------------|----------------|
| RF | 0.3641±0.0231 | 0.7967±0.0181 | 0.6117±0.0124 |
| MLP | 0.3787±0.0217 | 0.7874±0.0159 | 0.6030±0.0092 |
| Geo_kNN | 0.3617±0.0187 | 0.7982±0.0143 | 0.6194±0.0091 |
| EGSG_250m | 0.4097±0.0230 | 0.7675±0.0143 | 0.5883±0.0092 |

## 显著性结论

- EGSG_250m vs Geo_kNN: ΔR²=+0.0480, p=0.000001, d=+3.9733 ***
- EGSG_250m vs RF: ΔR²=+0.0456, p=0.000003, d=+3.2009 ***
- EGSG_250m vs MLP: ΔR²=+0.0309, p=0.000016, d=+2.6395 ***
- Geo_kNN vs RF: ΔR²=-0.0024, p=0.465422, d=-0.2410 ns

## 封存状态

**已封存**。

EGSG-250m 方向已完成 clean protocol 验证，不再继续优化。

## 后续可恢复条件

- 获得更完整 SAR / canopy height / TCH 覆盖
- 需要写论文方法章节
- 需要补充审稿人要求的消融实验
- 需要与新模型 backbone 结合验证
