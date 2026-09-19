# 处理后数据集与实验输出

投稿论文的配套数据包：

> **Knowledge Quality Diagnosis of Spatial Graph Representations: When Does Geographic
> Proximity Encode Reliable Predictive Knowledge?**
>
> 投稿至 *Knowledge and Information Systems* (KAIS)

本仓库装的是**处理后的数据集**和**支撑论文全部图表的分实验输出表**。原始遥感影像
（约 54 GB 的 MODIS / ASTER / ESA-CCI / ALOS 原始景）**不在**其中——只放派生出来的、
可直接建模的表，以及在这些表上跑出来的实验输出。

共 174 个文件，**约 5.5 MB**——其中 170 个数据/输出文件（全部登记在 `_manifest.json`），
外加中英文 README 与 `.gitignore`。单文件最大 1.1 MB，离 GitHub 的 50 MB 警告线很远。

---

## 〇、背景与术语

**论文在做什么。** 地理 *k* 近邻图（Geo kNN）是地理机器学习的默认空间表示，前提是"离得近
的样本标签也相近"。在复杂地形下这个前提被系统性违背：很多最近邻在**高程**和**标签**上都差
得很远。论文（a）提出**边级**诊断量 `MAD_y` / `MAD_h`（标签差与高程差的**平均绝对值**）和
**划分级**支撑度量 LSI；（b）据此构造 **EGSG**（Elevation-Gated Spatial Graph，剪掉两端高程差
超过 τ 的边）；（c）划出这个收益**能**与**不能**迁移的边界。

核心结果（6,638 清洗样本、10 种子）：

| 设定 | Geo kNN *R*² | EGSG *R*² | Δ*R*² | *p* |
|---|---|---|---|---|
| 随机划分（局部插值） | 0.362 ± 0.019 | 0.409 ± 0.023 | **+0.048** | 6.0 × 10⁻⁷ |
| 30 km 缓冲留出（严格外推） | −0.137 ± 0.075 | −0.191 ± 0.034 | **−0.054** | 0.027 |

即：门控收益在严格外推下**反号**（此时 LSI 恰为 0），且两个设定里 10 个种子的方向全部一致。
收益也能迁移到 NDVI 与地表温度两个目标，但**门控阈值是目标依赖的**。

一个复用时要留意的细节：未加门控的 Geo kNN + GCN **并不显著优于随机森林**
（Δ*R*² = −0.002，*p* = 0.49）——增益完全来自高程门控剪边，不是 GNN 结构本身。

**术语表**

| 术语 | 含义 |
|---|---|
| **Geo kNN** | 每个节点连到按大圆距离最近的 *k* = 10 个邻居。基线。 |
| **EGSG** | 在 Geo kNN 边集上，剪掉两端高程差超过 τ 的边。 |
| **τ** | 高程门控阈值。AGB 目标标定为 **250 m**；论文做了扫描，最优值随目标变。 |
| **`MAD_y` / `MAD_h`** | 边级诊断量：全图边上标签差、高程差的**平均绝对值**（注意是*平均*不是中位，见第三节）。 |
| **LSI** | Local Support Index。测试节点 *i*：`LSI_i(r,τ) = Σ_{j∈V_train} 1[d_ij ≤ r]·1[|h_i − h_j| ≤ τ]`——半径 *r* 内**且**过高程门控的训练邻居数。为 0 即无可用局部支撑。 |
| **清洗口径** | 60/20/20 划分、10 种子、*N* = 6,638。种子固定为 `42, 123, 2025, 7, 13, 37, 61, 73, 97, 101`。 |
| **转导** | 随机划分是转导设定：测试节点也在图里、其特征参与消息传递。读随机划分的数字时要注意这点。 |

**八种空间划分**（论文论证的骨架，split 实验的文件名里都会出现）。
*R*² 为 10 种子 mean ± std；负值表示比"直接预测均值"还差。

| 划分 | *N*_test | Geo kNN *R*² | EGSG *R*² | Δ*R*² | *p* |
|---|---|---|---|---|---|
| Random | 1,328 | 0.362 ± 0.019 | 0.409 ± 0.023 | +0.048 | 6.0 × 10⁻⁷ |
| Block 50 km | 1,043 | 0.257 ± 0.068 | 0.305 ± 0.056 | +0.047 | 1.6 × 10⁻⁵ |
| Block 100 km | 1,797 | 0.226 ± 0.123 | 0.292 ± 0.112 | +0.066 | 4.0 × 10⁻⁵ |
| **Buffer 30 km** | 1,042 | **−0.137 ± 0.075** | **−0.191 ± 0.034** | **−0.054** | **0.027** |
| **Buffer 50 km** | 1,042 | **−0.140 ± 0.062** | **−0.223 ± 0.060** | **−0.083** | **0.007** |
| Elevation low | 2,191 | −7.053 ± 3.419 | −0.573 ± 0.477 | +6.480 † | 1.3 × 10⁻⁴ |
| Elevation mid | 2,256 | 0.041 ± 0.028 | 0.123 ± 0.014 | +0.082 | 1.1 × 10⁻⁵ |
| Elevation high | 2,191 | −0.449 ± 0.213 | −0.517 ± 0.388 | −0.068 | 0.594 |

† 高程低区两种方法都失败（*R*² < 0）；那个很大的正 Δ*R*² 反映的是 Geo kNN 崩到 −7.05，
不是 EGSG 可用。

* **Block 划分**——研究区分块，整块留出做测试。
* **Buffer 划分**——测试区外围切出 30 km（或 50 km）缓冲带并**从训练集中移除**，
  保证任何训练节点都不落在测试节点的该距离内。这是严格外推设定。
* **Elevation holdout**——整条高程带留出。它同时带来近零支撑和极端协变量漂移，
  所以退化幅度超过"仅移除支撑"能解释的量。

注意 buffer 与高程留出**不只是移除支撑，还引入了协变量漂移**（buffer-30 下
Δ高程 ≈ −683 m）。论文把这两个因素分开讨论，没有把退化全算在支撑移除头上。

---

## 一、数据集（`data/`）

研究区为青藏高原东南部。每行一个采样节点，主表 8000 行 × 32 列。

| 文件 | 用途 |
|---|---|
| `20260520_single_year_2021_scaled_ndvi.parquet` | **主数据集**，论文全部实验都用它 |
| `20260521_single_year_2021_with_potapov_chm.parquet` | 树冠高变体 → 树冠高对照 |
| `20260521_single_year_2021_scaled_ndvi_with_gedi.parquet` | GEDI 树冠高变体 → 同一对照 |
| `20260523_single_year_2021_with_alos_smoke.parquet` | ALOS PALSAR 变体 → SAR 纹理对照（*N* = 335） |

### 清洗子集 *N* = 6,638 的口径

论文里的 *N* = 6,638 **不是表里的某一列**，而是"七个建模输入全部非空"的那批行：

```
ndvi_mean, elevation_mean, lai_mean, fpar_mean, lst_mean, et_mean, agb_label
```

按这七列取非空，得到**恰好 6,638 行**：

```python
import pandas as pd

FEAT = ["ndvi_mean", "elevation_mean", "lai_mean", "fpar_mean",
        "lst_mean", "et_mean", "agb_label"]

df = pd.read_parquet("data/20260520_single_year_2021_scaled_ndvi.parquet")
clean = df[df[FEAT].notna().all(axis=1)]
assert len(clean) == 6638
```

复算时可能遇到的其他行数，以便分辨是哪个口径：

* **8,000** —— 全池未清洗。这是表 2 的 "archived pool" 列。
* **7,728** —— 有 AGB 标签且有 NDVI。更松的口径，仍包含 LAI/FPAR/LST/ET 缺失的行。
* **7,038** —— 植被输入有效（在 AGB 与 NDVI 之上再加 `veg_missing == 0`）。
  这是 `edge_quality_diag.csv` 里 LST 目标的行数，论文未引用该数字。

### 特征分组

对应论文表 1（Data sources and feature list）。

| 组 | 列 | 维数 |
|---|---|---|
| 坐标 / ID | `lon`, `lat`, `tile`, `node_id`, `year` | — |
| 植被（NDVI 合成） | `ndvi_mean`, `ndvi_std`, `ndvi_median`, `ndvi_q25`, `ndvi_q75`, `ndvi_q90`, `ndvi_range` | 7 |
| 植被辅助（MODIS MCD15A3H.061） | `lai_mean`, `fpar_mean` | 2 |
| 热（MODIS MOD11A2.061） | `lst_mean` | 1 |
| 水（MODIS MOD16A2GF.061） | `et_mean` | 1 |
| 地形（ASTER GDEM v3） | `elevation_mean`, `slope_mean`, `aspect_sin`, `aspect_cos`, `curvature_mean` | 5 |
| 土地覆盖（MODIS MCD12Q1.061） | `lc_type` | — |
| 目标标签（ESA Biomass CCI v5.0） | `agb_label` | — |
| 质量 / 掩膜 | `*_valid_ratio`（`ndvi`/`dem`/`lai`/`fpar`/`lst`/`et`）、`veg_missing`、`hydro_missing`、`landcover_missing` | — |

几点约定：

* `agb_label` 单位 Mg/ha；NDVI 合成列存的是**逐年的标准化（scaled）**值。
* 地形列虽带 `_mean` 后缀但每节点只有一个值——沿用上游命名，为的是可追溯。
* `*_valid_ratio` 与 `*_missing` 是质控列，**不计入**表 1 的特征维数。
* `elevation_mean` 全池范围 146–5,383 m，6,638 节点清洗子集范围 282–5,279 m。
* `lon` 范围 93.00–98.00 °E，`lat` 范围 28.02–30.50 °N。

### 快速上手

```python
import pandas as pd

FEAT = ["ndvi_mean", "elevation_mean", "lai_mean", "fpar_mean",
        "lst_mean", "et_mean", "agb_label"]

df = pd.read_parquet("data/20260520_single_year_2021_scaled_ndvi.parquet")
print(df.shape)                     # (8000, 32)

clean = df[df[FEAT].notna().all(axis=1)]
print(len(clean))                   # 6638 —— 全部实验用的就是这批

clean[["lon", "lat", "elevation_mean", "agb_label", "ndvi_mean"]].head()
```

---

## 二、实验输出（`experiments/`）

每个子目录是一次实验 run，沿用原始 run 名。里面放逐种子原始结果、配对检验表、汇总表，
以及（若该 run 产生过）`run_log.txt` 运行日志。除另有说明外，全部实验用同 10 个种子：
`42, 123, 2025, 7, 13, 37, 61, 73, 97, 101`。

**一个 run 目录里通常有什么：**

| 文件 | 内容 |
|---|---|
| `*_raw.csv` | 逐种子原始结果，一行一个 (seed, method, split, …) |
| `*_paired.csv` | 逐种子配对差值，配对 *t* 检验的输入 |
| `*_summary.csv` | 按种子聚合的 mean ± std |
| `*_report.md` | 该 run 自己产出的可读报告 |
| `run_log.txt` | 运行记录：配置、节点数、计时 |
| `plots/` | 该 run 自己画的图（不一定是论文里那版） |

**`_manifest.json` 的字段**：`path`（包内路径）、`bytes`、`sha256_16`（文件 SHA-256 前
16 位，可据此校验副本）、`source`（原始归档位置）、`supports`（该文件支撑论文哪个图表）。

```
experiments/
├── KAIS/                     主实验期 22 个 run
├── e3_spatial_flagship/      空间 Δŷ 图（版面 6）的逐节点表
├── e2_mi_knee/               版面 11 脚本直接读的 MI-按高程 CSV
├── backbone_10seed_20260914/ 跨骨干表（表 6）的 10 种子重跑
└── legacy_EAAI/              4 个早期 run + 2 张表，提供表 10 的剩余行
```

**逐文件**的对应关系记在 `_manifest.json` 里（路径、字节数、sha256、来源、支撑哪个图表）。
**逐图表**的完整对应关系见英文 `README.md` 第 6 节（Mapping: manuscript artifact →
source directory）。简表：表1←数据集本身；**表2←由 `data/` 直接算出**；表3/表9/版面4/9/10
←`gate_threshold_sweep`；表4←`terrain_aware` + `efficiency` + 两个 xgboost；表5←`k_sensitivity`；
表6←`backbone_10seed_20260914/`；表7/表8/版面7/8←`buffer_split_strict` + `block_elev_10seeds`；
表10←五个 `window_M` run + `legacy_EAAI/`；表11←`terrain_aware`；版面6←`e3_spatial_flagship/`；
版面11←`e2_mi_knee/` + `info_theory_185758`；版面12←`tau_selection_protocol`。

### `legacy_EAAI/` 为什么在这里

表 10（消融与对照）有几行来自本项目**前一阶段**的 run，不属于主实验期。
每一条都是靠在配对检验 CSV 里**精确定位正文印出的那个值**核实的：

| 表 10 行 | 印出值 | 来源 |
|---|---|---|
| 土地覆盖门控（软） | +0.000, *p* = 0.997 | `legacy_EAAI/window_C_opportunity_scan_20260605_103628` |
| 土地覆盖门控（硬） | −0.010, *p* = 0.018 | 同上 |
| DEM 残差门控 | −0.003, *p* = 0.595 | 同上 |
| 树冠高门控 | −0.006, *p* = 0.311 | `legacy_EAAI/window_D_canopy_height_fair_compare_20260608_101316` |
| SAR 纹理特征（*N* = 335） | +0.054, *p* = 0.235 | `legacy_EAAI/window_G_sar_palsar_20260608_111717` |
| 高程门控显著性复跑 | 主实验期脚本引用 | `legacy_EAAI/window_B_significance_clean_20260604_180905` |

---

## 三、表 2 可由数据集直接复算

表 2（Geo kNN 图的知识质量诊断）**不需要任何实验输出**——它是在 6,638 行清洗子集上的
直接统计量。我们验证过：只用 `data/20260520_single_year_2021_scaled_ndvi.parquet`
就能复现它。对齐口径要注意两点：

* **图**：*k* = 10 近邻，大圆距离（地球半径 6,371 km），**有向**边——每个节点指向它的
  10 个邻居，故边数 = 10 × *N*。近邻搜索在等距圆柱投影面上做；若改用大圆搜索，
  边长类数字会差约 0.6%。
* **表里的 `MAD` 是"平均绝对差"，不是"中位绝对偏差"**。清洗子集上
  平均 |Δ高程| = 513.7 m、平均 |ΔAGB| = 33.5 Mg/ha（正文印 512.4 / 33.4）；
  若按中位绝对偏差算是 417.9 m / 25.0 Mg/ha。两种定义差得很远，不能混。

复算值与正文的逐行对照见英文 `README.md` 第 8 节。摘要里"mean absolute label and elevation
differences"的措辞也印证了 `MAD` = 平均绝对差这一读法。

---

## 四、入选判据

这里的每个目录至少满足以下之一（都可复算）：

* **A — 图脚本直接读的路径**：该路径作为模块级常量出现在生成论文 12 张图的脚本里。
* **B — 含正文印出的数字**：正文某值与某 CSV 的某格在印出精度上相等。
* **C — 被脚本按名字引用**：主实验期脚本以字符串形式引用过该目录。

三条都不满足的一律不收。主要排除项及理由：

* **MVF 实验族**——改稿时已从论文删除，结果不报告。
* **被取代的重跑**——同名 `window_M_*` 但时间戳更早的重复 run；以及信息论批次的第一次
  （`window_M_info_theory_20260824_185542`）。排除它的原因：其 `tau_star_crosscheck.csv`
  用的是朴素膝点估计，三个目标全不匹配（`AGB 2500 vs 250`、`LST 2500 vs 1000`、
  `NDVI 2500 vs 100`），而保留的那次给出 `AGB 250`、`LST 500`、`NDVI 200` 并能复现图。
  两次 run 的其余 CSV **逐字节相同**。
* **LooseGAT / CTA 构造族**（`egsg_cta_ablation`、`egsg_improve_ablation`）——正文只做定性
  讨论，**没有任何数字被印出**，其中全部数值都不满足判据 B。
* **已弃用的 50k 跨年数据集**与中间特征缓存。
* **另外六份逐年节点表（2015–2020）**——只有 2021 在用；其余是为一项论文未报告的
  年份敏感性检查建的。
* **中间诊断 run**（`window_M_elev_probe`、`window_M_k3_point`、`geo_knn_misconnect_20260604`
  报告）——它们的数字都是在最终清洗口径上重算之后才进入正文的。

---

## 五、规范数值

同一量在不同位置可能以不同精度出现。规范值如下：

| 量 | 值 |
|---|---|
| EGSG-250m *R*²（随机划分） | 0.4095 |
| Geo kNN *R*²（随机划分） | 0.3618 |
| 头条 Δ*R*² | +0.048 |
| 配对 *t* 检验 *p* | 6.0 × 10⁻⁷ |
| 95 % CI | [+0.039, +0.056] |
| EGSG τ = 250 m 有向边 | 60,698 |
| Geo kNN 有向边 | 66,380 |

本包里有少数 run log 与汇总文件记的是**更早的 0.4097**（EGSG 随机划分 *R*²）。那个值来自
一次基线漂移的旧 run，已被取代。这里**保留原样而不改写**，是为了让 run 记录可追溯——
凡这类文件与正文冲突，**以正文为准**。

---

## 六、环境要求

读数据只需要：

```
python >= 3.9
pandas
pyarrow        # 读 parquet 用
```

无其他依赖。CSV 是 UTF-8 with BOM 的普通逗号分隔文件（严格解码器请用 `utf-8-sig`）。

---

## 七、许可与引用

* **数据许可**：待作者在发表前补上。
* **源产品**：全部输入都是开放许可——ESA Biomass CCI v5.0，MODIS（MCD15A3H.061、
  MOD11A2.061、MOD16A2GF.061、MCD12Q1.061），ASTER GDEM v3，ALOS PALSAR mosaic，
  Hansen 树冠高。DOI 见正文的 *Data Availability* 声明。
* **代码**：分析与图生成代码不在本包内。

若使用本数据，请引用上述论文。
