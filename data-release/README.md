# Processed dataset and experiment outputs

Companion data release for the manuscript:

> **Knowledge Quality Diagnosis of Spatial Graph Representations: When Does Geographic
> Proximity Encode Reliable Predictive Knowledge?**
>
> Submitted to *Knowledge and Information Systems* (KAIS).

This repository contains the **processed dataset** and the **per-experiment result tables**
behind every figure and table in the paper. Raw satellite imagery (≈54 GB of MODIS / ASTER /
ESA-CCI / ALOS scenes) is **not** included — only the derived, model-ready table and the
experiment outputs computed from it.

**174 files, ≈5.5 MB** — 170 data and output files (all listed in `_manifest.json`), plus this
README, its Chinese counterpart, and a `.gitignore`. Largest single file: 1.1 MB. Nothing comes
close to GitHub's 50 MB warning threshold.

---

## Contents

1. [Background in brief](#1-background-in-brief)
2. [Quick start](#2-quick-start)
3. [Terminology and split protocols](#3-terminology-and-split-protocols)
4. [The dataset (`data/`)](#4-the-dataset-data)
5. [Experiment outputs (`experiments/`)](#5-experiment-outputs-experiments)
6. [Mapping: manuscript artifact → source directory](#6-mapping-manuscript-artifact--source-directory)
7. [Why `legacy_EAAI/` is here](#7-why-legacy_eaai-is-here)
8. [Reproducing Table 2 from the dataset](#8-reproducing-table-2-from-the-dataset)
9. [How this selection was made](#9-how-this-selection-was-made)
10. [Canonical values](#10-canonical-values)
11. [Requirements](#11-requirements)
12. [License and citation](#12-license-and-citation)

---

## 1. Background in brief

Geographic *k*-nearest-neighbour graphs (Geo kNN) are a default spatial representation in
geospatial machine learning, on the assumption that nearby locations carry similar labels. In
complex terrain that assumption breaks: many of a node's nearest neighbours differ sharply in
elevation and in label.

The paper (a) introduces **edge-level** metrics that quantify this — mean absolute label and
elevation differences, `MAD_y` and `MAD_h` — and a **split-level** support metric, the Local
Support Index (**LSI**); (b) uses that diagnosis to build the **Elevation-Gated Spatial Graph
(EGSG)**, which prunes edges whose endpoint elevation difference exceeds a threshold τ;
and (c) maps where the resulting benefit does and does not transfer.

Headline results, on the 6,638-node clean sample with 10 seeds:

| Setting | Geo kNN *R*² | EGSG *R*² | Δ*R*² | *p* |
|---|---|---|---|---|
| Random split (local interpolation) | 0.362 ± 0.019 | 0.409 ± 0.023 | **+0.048** | 6.0 × 10⁻⁷ |
| Buffer-30 km holdout (strict extrapolation) | −0.137 ± 0.075 | −0.191 ± 0.034 | **−0.054** | 0.027 |

So the gating gain reverses under strict extrapolation — where LSI is exactly zero — and the
direction of the effect is consistent across all 10 seeds in both settings. The benefit also
transfers to two further targets (NDVI, land surface temperature) but with
**target-dependent** gating thresholds.

One detail worth carrying into any reuse: the uncorrected Geo kNN + GCN is **not**
significantly better than a random forest (Δ*R*² = −0.002, *p* = 0.49). The improvement comes
from elevation-gated edge pruning, not from the GNN architecture.

---

## 2. Quick start

```python
import pandas as pd

FEAT = ["ndvi_mean", "elevation_mean", "lai_mean", "fpar_mean",
        "lst_mean", "et_mean", "agb_label"]

df = pd.read_parquet("data/20260520_single_year_2021_scaled_ndvi.parquet")
print(df.shape)                     # (8000, 32)

clean = df[df[FEAT].notna().all(axis=1)]
print(len(clean))                   # 6638  — the sample every experiment uses

clean[["lon", "lat", "elevation_mean", "agb_label", "ndvi_mean"]].head()
```

To find the CSVs behind a specific figure or table, read `_manifest.json` (see
[§5](#what-the-manifest-records)) or the mapping in [§6](#6-mapping-manuscript-artifact--source-directory).

---

## 3. Terminology and split protocols

Terms used throughout the file names and the mapping table.

| Term | Meaning |
|---|---|
| **Geo kNN** | Graph where each node connects to its *k* = 10 nearest neighbours by great-circle distance. The baseline. |
| **EGSG** | Elevation-Gated Spatial Graph. Removes, from the Geo kNN edge set, every edge whose endpoint elevation difference exceeds τ. |
| **τ** | The elevation gate threshold. Calibrated at **250 m** for the AGB target; the paper sweeps it and reports target-dependent optima. |
| **`MAD_y`, `MAD_h`** | Edge-level diagnostics: the **mean absolute** label difference and elevation difference over the graph's edges. (Despite the name, *mean*, not median — see [§8](#8-reproducing-table-2-from-the-dataset).) |
| **LSI** | Local Support Index. For test node *i*, `LSI_i(r,τ) = Σ_{j∈V_train} 1[d_ij ≤ r] · 1[|h_i − h_j| ≤ τ]` — how many training neighbours lie within radius *r* **and** within the elevation gate. Zero means no usable local support. |
| **Clean protocol** | 60/20/20 partition, 10 seeds, *N* = 6,638. All experiments use the same 10 seeds: `42, 123, 2025, 7, 13, 37, 61, 73, 97, 101`. |
| **Transductive** | The random split is a transductive setting: test nodes are present in the graph and their features contribute to message passing. Noted here because it affects how the random-split numbers should be read. |

### The eight spatial splits

Central to the paper's argument, and they appear in the file names of every split experiment.
`R²` is mean ± std over 10 seeds; negative values mean worse than predicting the mean.

| Split | *N*_test | Geo kNN *R*² | EGSG *R*² | Δ*R*² | *p* |
|---|---|---|---|---|---|
| Random | 1,328 | 0.362 ± 0.019 | 0.409 ± 0.023 | +0.048 | 6.0 × 10⁻⁷ |
| Block 50 km | 1,043 | 0.257 ± 0.068 | 0.305 ± 0.056 | +0.047 | 1.6 × 10⁻⁵ |
| Block 100 km | 1,797 | 0.226 ± 0.123 | 0.292 ± 0.112 | +0.066 | 4.0 × 10⁻⁵ |
| **Buffer 30 km** | 1,042 | **−0.137 ± 0.075** | **−0.191 ± 0.034** | **−0.054** | **0.027** |
| **Buffer 50 km** | 1,042 | **−0.140 ± 0.062** | **−0.223 ± 0.060** | **−0.083** | **0.007** |
| Elevation low | 2,191 | −7.053 ± 3.419 | −0.573 ± 0.477 | +6.480 † | 1.3 × 10⁻⁴ |
| Elevation mid | 2,256 | 0.041 ± 0.028 | 0.123 ± 0.014 | +0.082 | 1.1 × 10⁻⁵ |
| Elevation high | 2,191 | −0.449 ± 0.213 | −0.517 ± 0.388 | −0.068 | 0.594 |

† In the elevation-low split both methods fail (*R*² < 0); the large positive Δ*R*² reflects
the Geo kNN collapse to −7.05, not usable EGSG accuracy.

* **Block split** — the study region is divided into blocks; whole blocks are held out for
  testing.
* **Buffer split** — a 30 km (or 50 km) buffer is cut around the test region and *removed
  from training*, so no training node lies within that distance of any test node. This is the
  strict-extrapolation setting.
* **Elevation holdout** — an elevation band is held out entirely. These combine near-zero
  local support with extreme covariate shift, so their degradation exceeds what support
  removal alone would predict.

Note that buffer and elevation holdouts do not only remove support — they also induce
covariate shift (e.g. Δelevation ≈ −683 m under buffer-30 km). The paper keeps these factors
separate rather than attributing everything to support removal.

---

## 4. The dataset (`data/`)

The study area is the southeastern Tibetan Plateau. Each row is one sampling node; the
primary table has 8,000 rows and 32 columns.

| File | Role |
|---|---|
| `20260520_single_year_2021_scaled_ndvi.parquet` | **Primary dataset.** Every experiment in the paper uses this file. |
| `20260521_single_year_2021_with_potapov_chm.parquet` | Tree-canopy-height variant → the canopy-height control. |
| `20260521_single_year_2021_scaled_ndvi_with_gedi.parquet` | GEDI canopy-height variant → same control. |
| `20260523_single_year_2021_with_alos_smoke.parquet` | ALOS PALSAR variant → the SAR-texture control (*N* = 335). |

### The clean subset (*N* = 6,638)

The paper reports *N* = 6,638. This is **not** a column in the file — it is the subset of rows
for which all seven modelling inputs are present:

```
ndvi_mean, elevation_mean, lai_mean, fpar_mean, lst_mean, et_mean, agb_label
```

```python
clean = df[df[FEAT].notna().all(axis=1)]
assert len(clean) == 6638
```

Counts you will meet when re-deriving subsets, so you can tell which filter produced them:

* **8,000** — the full pool, untouched. This is the "archived pool" column of Table 2.
* **7,728** — a valid AGB label *and* a valid NDVI. A weaker filter: still includes rows
  missing LAI, FPAR, LST or ET.
* **7,038** — valid vegetation inputs (`veg_missing == 0`, on top of AGB and NDVI). This is
  the row count of the LST target in `edge_quality_diag.csv`; it is not quoted in the paper.

### Feature groups

Matches Table 1 (*Data sources and feature list*).

| Group | Columns | Dims |
|---|---|---|
| Coordinates / ID | `lon`, `lat`, `tile`, `node_id`, `year` | — |
| Vegetation (NDVI composites) | `ndvi_mean`, `ndvi_std`, `ndvi_median`, `ndvi_q25`, `ndvi_q75`, `ndvi_q90`, `ndvi_range` | 7 |
| Vegetation auxiliary (MODIS MCD15A3H.061) | `lai_mean`, `fpar_mean` | 2 |
| Thermal (MODIS MOD11A2.061) | `lst_mean` | 1 |
| Moisture (MODIS MOD16A2GF.061) | `et_mean` | 1 |
| Terrain (ASTER GDEM v3) | `elevation_mean`, `slope_mean`, `aspect_sin`, `aspect_cos`, `curvature_mean` | 5 |
| Land cover (MODIS MCD12Q1.061) | `lc_type` | — |
| Target label (ESA Biomass CCI v5.0) | `agb_label` | — |
| Quality / masking | `*_valid_ratio` (`ndvi`, `dem`, `lai`, `fpar`, `lst`, `et`), `veg_missing`, `hydro_missing`, `landcover_missing` | — |

Conventions:

* `agb_label` is in Mg/ha. The NDVI composites are stored **scaled** (per-year standardised).
* Terrain columns carry a `_mean` suffix although they are single-valued per node — this
  matches the upstream naming and is kept for traceability.
* `*_valid_ratio` and `*_missing` are QC columns, **not** counted among the feature
  dimensions of Table 1.
* `elevation_mean` ranges 146–5,383 m over the full pool and 282–5,279 m over the 6,638-node
  clean subset.
* `lon` spans 93.00–98.00 °E, `lat` 28.02–30.50 °N.

---

## 5. Experiment outputs (`experiments/`)

Each subdirectory is one experiment run, kept under its original run name.

```
experiments/
├── KAIS/                     22 runs from the main experimental campaign
├── e3_spatial_flagship/      per-node Δŷ tables behind the spatial map (Fig. 6)
├── e2_mi_knee/               MI-by-elevation CSV read directly by the Fig. 11 script
├── backbone_10seed_20260914/ 10-seed rerun behind the cross-backbone table (Table 6)
└── legacy_EAAI/              4 earlier runs + 2 tables supplying remaining ablation rows
```

### Anatomy of a run directory

Not every run has every file, but the usual pattern is:

| File | Contents |
|---|---|
| `*_raw.csv` | Per-seed raw results — one row per (seed, method, split, …) |
| `*_paired.csv` | Per-seed paired differences, the input to the paired *t*-tests |
| `*_summary.csv` | Aggregated mean ± std over seeds |
| `*_report.md` | Human-readable write-up the run produced |
| `run_log.txt` | Invocation record: configuration, node counts, timings |
| `plots/` | Figures the run itself produced (not necessarily the paper's versions) |

### What the manifest records

`_manifest.json` is a flat list, one entry per file:

```json
{
  "path": "experiments/KAIS/window_M_k_sensitivity_20260823_185054/L2_k_sensitivity_summary.csv",
  "bytes": 3660,
  "sha256_16": "…",
  "source": "<ROOT>/最最终终的文档/实验归档/实验输出_40批/window_M_k_sensitivity_20260823_185054/…",
  "supports": "tab:k"
}
```

`supports` names the manuscript artifact each file backs; `sha256_16` is the first 16 hex
digits of the file's SHA-256, so you can verify a copy.

---

## 6. Mapping: manuscript artifact → source directory

Table numbers refer to the current manuscript.

| Artifact | Source |
|---|---|
| Table 1 (`tab:data`) — data sources and features | the dataset itself; `KAIS/window_M_data_consistency_20260825_004359` (coordinate and variogram checks); `legacy_EAAI/tables/20260521_hansen_tch_partial_correlation.csv` |
| Table 2 (`tab:diag`) — Geo kNN diagnosis | **computed directly from `data/`** — see [§8](#8-reproducing-table-2-from-the-dataset); `KAIS/window_M_second_variable_ablation_20260823_210315/edge_quality_diag.csv` is a cross-check |
| Table 3 (`tab:tau`) — EGSG threshold sensitivity | `KAIS/window_M_gate_threshold_sweep_20260823_212454` |
| Table 4 (`tab:main`) — clean random-split results | `KAIS/window_M_terrain_aware_20260824_190303`, `KAIS/window_M_efficiency_20260823_203946` (train-time column), `KAIS/window_M_xgboost_baseline_20260823_181555`, `KAIS/window_M_xgboost_tuned_20260823_182349` |
| Table 5 (`tab:k`) — *k* sensitivity | `KAIS/window_M_k_sensitivity_20260823_185054` |
| Table 6 (`tab:bb`) — cross-backbone | `backbone_10seed_20260914/` |
| Table 7 (`tab:splits`) — spatial generalization | `KAIS/window_M_buffer_split_strict_20260823_200451`, `KAIS/window_M_block_elev_10seeds_20260826_195611` |
| Table 8 (`tab:lsi`) — LSI under spatial splits | same two runs |
| Table 9 (`tab:second`) — threshold sweep, three targets | `KAIS/window_M_gate_threshold_sweep_20260823_212454` |
| Table 10 (`tab:abl`) — ablations and controls | `KAIS/window_M_agb_elevation_ablation_20260824_132928`, `KAIS/window_M_random_edge_pruning_20260824_133952`, `KAIS/window_M_negative_transfer_addback_20260824_134652`, `KAIS/window_M_backfill_ablation_20260903_095741`, `KAIS/window_M_backfill_ablation_buffer_20260903_100859`, **plus `legacy_EAAI/`** ([§7](#7-why-legacy_eaai-is-here)) |
| Table 11 (`tab:terrain`) — terrain-aware comparison | `KAIS/window_M_terrain_aware_20260824_190303` |
| Fig. 1 — study area overview | `data/` (plus a hillshade basemap, not included in this release) |
| Fig. 3 — Geo kNN edge-quality diagnostics | `data/` |
| Fig. 4 — threshold sensitivity | `KAIS/window_M_gate_threshold_sweep_20260823_212454` |
| Fig. 5 — model comparison | `KAIS/window_M_lightgbm_20260823_184037`, `KAIS/window_M_adaptive_threshold_20260824_190248` |
| Fig. 6 — spatial distribution of Δŷ | `e3_spatial_flagship/` |
| Fig. 7 — spatial generalization under strict protocols | `KAIS/window_M_buffer_split_strict_20260823_200451`, `KAIS/window_M_block_elev_10seeds_20260826_195611`, `KAIS/window_M_buffer_scan_20260824_135305` |
| Fig. 8 — LSI vs covariates | `KAIS/window_M_block_elev_10seeds_20260826_195611` (`lsi_agg_by_split_10seeds.csv`), `KAIS/window_M_buffer_split_strict_20260823_200451` |
| Fig. 9 — three-target threshold sensitivity | `KAIS/window_M_gate_threshold_sweep_20260823_212454` |
| Fig. 10 — edge-quality metrics vs *R*² | `KAIS/window_M_gate_threshold_sweep_20260823_212454` |
| Fig. 11 — edge-level mutual information | `e2_mi_knee/mi_by_bin.csv`, `KAIS/window_M_info_theory_20260824_185758` |
| Fig. 12 — τ-selection protocols | `KAIS/window_M_tau_selection_protocol_20260824_235917` |
| §5.5 second target and extrapolation | `KAIS/window_M_second_variable_20260823_205126`, `KAIS/window_M_second_variable_buffer_20260826_FULL` |
| §5.5 GWR / ordinary kriging controls | `KAIS/window_M_gwr_kriging_20260824_135657` |

Fig. 2 is a schematic and has no data source. The paper's own figure filenames
(`FigN.png`) are historical labels and do **not** match the figure numbers in the typeset
manuscript.

---

## 7. Why `legacy_EAAI/` is here

Several rows of Table 10 trace to runs from an earlier phase of the project rather than to the
main campaign. Each match was verified by locating the exact printed value in the run's
paired-comparison CSV.

| Table 10 row | Printed | Source |
|---|---|---|
| Land-cover gating, soft | +0.000, *p* = 0.997 | `legacy_EAAI/window_C_opportunity_scan_20260605_103628` |
| Land-cover gating, hard | −0.010, *p* = 0.018 | same |
| DEM-residual gating | −0.003, *p* = 0.595 | same |
| Tree-canopy-height gating | −0.006, *p* = 0.311 | `legacy_EAAI/window_D_canopy_height_fair_compare_20260608_101316` |
| SAR texture features (*N* = 335) | +0.054, *p* = 0.235 | `legacy_EAAI/window_G_sar_palsar_20260608_111717` |
| Elevation-gate significance rerun | referenced by the main scripts | `legacy_EAAI/window_B_significance_clean_20260604_180905` |

---

## 8. Reproducing Table 2 from the dataset

Table 2 (*Knowledge quality diagnosis of the Geo kNN graph*) needs no experiment output — it
is a direct computation on the 6,638 clean rows, and we verified it reproduces from
`data/20260520_single_year_2021_scaled_ndvi.parquet` alone.

Conventions needed to match it:

* **Graph.** *k* = 10 nearest neighbours by great-circle distance (Earth radius 6,371 km),
  **directed** edges — every node points to its 10 neighbours, so edge count = 10 × *N*.
  Neighbours are found on an equirectangular projection; using a great-circle search instead
  moves the edge-length figures by ~0.6 %.
* **`MAD` means *mean* absolute difference**, matching the abstract's wording ("mean absolute
  label and elevation differences"). For the clean subset, mean |Δelevation| = 513.7 m and
  mean |ΔAGB| = 33.5 Mg ha⁻¹ (printed: 512.4 and 33.4). The median absolute deviations are
  417.9 m and 25.0 Mg ha⁻¹ — far apart, so the distinction matters if you recompute.

Our recomputation versus the printed values:

| Quantity | Recomputed | Printed |
|---|---|---|
| Directed edges (*k* = 10) | 66,380 | 66,380 |
| Mean edge length | 5.02 km | 4.99 km |
| P90 edge length | 7.82 km | 7.78 km |
| MAD_h (mean abs. difference) | 513.7 m | 512.4 m |
| P90 \|Δelevation\| | 1,088.1 m | 1,085.0 m |
| MAD_y (mean abs. difference) | 33.5 Mg/ha | 33.4 Mg/ha |
| P90 \|ΔAGB\| | 77.0 Mg/ha | 76.0 Mg/ha |
| Edges with \|Δelevation\| > 800 m | 14,361 (21.63 %) | 14,210 (21.41 %) |
| Edges with \|ΔAGB\| > 70 Mg/ha | 8,168 (12.30 %) | 8,125 (12.24 %) |
| Land-cover mismatch among those | 61.1 % | 60.6 % |

The edge-length and elevation rows differ by ~0.3–0.6 %, consistent with kNN tie-breaking
among near-equidistant neighbours; the counts and rates agree to within ~1 %.

---

## 9. How this selection was made

Every directory here satisfies at least one checkable criterion:

* **A — read by a figure script.** The path appears as a module-level constant in one of the
  scripts generating the paper's 12 figures.
* **B — contains a printed number.** A value printed in the manuscript matches a cell of one
  of the run's CSVs at the printed precision.
* **C — referenced by name.** A script from the main campaign names the directory as a string.

Directories failing all three were left out. The main exclusions, with reasons:

* **The MVF experiment family** — removed from the manuscript during revision; not reported.
* **Superseded reruns** — earlier repeats of the same experiment (runs sharing a `window_M_*`
  name but an older timestamp), and the first pass of the information-theory batch
  (`window_M_info_theory_20260824_185542`). That first pass is excluded because its
  `tau_star_crosscheck.csv` carries a naive knee estimator that matches no target
  (`AGB 2500 vs 250`, `LST 2500 vs 1000`, `NDVI 2500 vs 100`), whereas the retained run gives
  `AGB 250`, `LST 500`, `NDVI 200` and reproduces the figure. All other CSVs in the two runs
  are byte-identical. Run logs belonging to superseded runs were likewise not carried over —
  each included `run_log.txt` corresponds to the retained run's timestamp.
* **The *LooseGAT* / *CTA* construction family** (`egsg_cta_ablation`, `egsg_improve_ablation`)
  — discussed qualitatively in the text, but **none of their numbers are printed** in the
  manuscript. Every value in those runs fails criterion B.
* **The deprecated 50k cross-year dataset** and the intermediate feature caches.
* **The six other per-year node tables (2015–2020).** Only 2021 is used; the others were built
  for a year-sensitivity check that the manuscript does not report.
* **Intermediate diagnostic runs** (`window_M_elev_probe`, `window_M_k3_point`, and the
  `geo_knn_misconnect_20260604` report) whose numbers entered the manuscript only after
  recomputation on the final clean protocol.

---

## 10. Canonical values

Where a value appears at more than one precision across the manuscript and this release, the
canonical set is:

| Quantity | Value |
|---|---|
| EGSG-250 m *R*² (random split) | 0.4095 |
| Geo kNN *R*² (random split) | 0.3618 |
| Headline Δ*R*² | +0.048 |
| Paired *t*-test *p* | 6.0 × 10⁻⁷ |
| 95 % CI | [+0.039, +0.056] |
| EGSG τ = 250 m directed edges | 60,698 |
| Geo kNN directed edges | 66,380 |
| EGSG τ = 250 m mean degree | 18.3 (6 isolated vertices, 0.09 %) |

A few run logs and summary files in this release record an **earlier value of 0.4097** for the
EGSG random-split *R*². That came from a baseline-drifted run and was superseded. It is
preserved here rather than rewritten so the run records stay traceable — where such a file
disagrees with the manuscript, **the manuscript is correct**.

---

## 11. Requirements

Reading the data needs only:

```
python >= 3.9
pandas
pyarrow        # for read_parquet
```

No other dependencies. The CSVs are plain comma-separated, UTF-8 with BOM
(`utf-8-sig` if you read them with a strict decoder).

---

## 12. License and citation

* **Data license:** to be added by the authors before publication.
* **Source products:** all inputs are openly licensed — ESA Biomass CCI v5.0, MODIS
  (MCD15A3H.061, MOD11A2.061, MOD16A2GF.061, MCD12Q1.061), ASTER GDEM v3, ALOS PALSAR
  mosaic, and Hansen tree-canopy-height. See the manuscript's *Data Availability* statement
  for DOIs.
* **Code:** the analysis and figure-generation code is not part of this release.

If you use these data, please cite the manuscript above.
