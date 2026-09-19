# -*- coding: utf-8 -*-
"""
GAT / APPNP / GraphSAGE 的 10 种子补跑。

策略：**先复现，再扩展**。
  phase=repro : 用已知的 5 种子 [42,123,2025,7,13] 跑，核对是否命中论文 tab:bb 现有数值。
                命中 => 该 harness 可信 => 才允许扩到 10 种子。
  phase=full  : 用 10 种子 [42,123,2025,7,13,37,61,73,97,101] 跑全部四个骨干。

为了不改动任何数值口径，本脚本 **import 原 window_I 脚本**，直接复用它的
build_egsg / build_geo / GCN / GraphSAGE / GAT / APPNPNet / MLP / train_gnn / train_rf，
只把 DATASET 指到本机路径、把 SEEDS 换成命令行给的列表。
主循环逐行照抄 window_I 的 main()（原第 161-230 行）。

用法：
  python _rerun_backbone_10seed.py repro
  python _rerun_backbone_10seed.py full
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

EAAI = Path(r"C:\Users\admin\Desktop\experiment_datasets_export_20260609 (2)"
            r"\experiment_datasets_export_20260609\_归档_遥感版_EAAI_20260612\code\experiments")
sys.path.insert(0, str(EAAI))
import window_I_backbone_comparison as wi  # noqa: E402

LOCAL_DS = Path(r"C:\Users\admin\Desktop\experiment_datasets_export_20260609 (2)"
                r"\experiment_datasets_export_20260609\主数据集_逐年scaled"
                r"\20260520_single_year_2021_scaled_ndvi.parquet")
wi.DATASET = LOCAL_DS

OUT_ROOT = Path(r"C:\Users\admin\Desktop\experiment_datasets_export_20260609 (2)"
                r"\experiment_datasets_export_20260609\_补跑_backbone_10seed_20260914")

SEED_SETS = {
    "repro": [42, 123, 2025, 7, 13],
    "full":  [42, 123, 2025, 7, 13, 37, 61, 73, 97, 101],
}

# 论文 tab:bb 现有数值（5 种子行的核对靶子；GCN 行是 10 种子，仅供参照）
PAPER = {
    "GCN":   (0.362, 0.019, 0.409, 0.023),
    "GAT":   (0.368, 0.015, 0.427, 0.022),
    "APPNP": (0.374, 0.016, 0.403, 0.023),
    "SAGE":  (0.415, 0.025, 0.413, 0.024),
}


def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "repro"
    seeds = SEED_SETS[phase]
    outdir = OUT_ROOT / phase
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"=== 补跑 phase={phase}  seeds={seeds} ===")
    print(f"数据集: {wi.DATASET}  (存在={wi.DATASET.exists()})")
    print(f"输出: {outdir}")

    # ── 数据加载：逐行照抄 window_I.main() 第 161-170 行 ──
    df = pd.read_parquet(wi.DATASET)
    feat_cols = [c for c in wi.BASE_COLS if c in df.columns]
    valid = df[feat_cols + ["agb_label"]].notna().all(axis=1) & (df["agb_label"] > 0)
    dfv = df[valid].reset_index(drop=True)
    X_raw = dfv[feat_cols].values.astype(np.float64)
    y_raw = dfv["agb_label"].values.astype(np.float64)
    X_raw = np.where(np.isinf(X_raw), np.nan, X_raw)
    y_raw = np.where(np.isinf(y_raw), np.nan, y_raw)
    clean = ~np.isnan(X_raw).any(axis=1) & np.isfinite(y_raw)
    X_c, y_c = X_raw[clean], y_raw[clean]
    n = len(X_c)
    lon = dfv["lon"].values[clean]
    lat = dfv["lat"].values[clean]
    elev_arr = dfv["elevation_mean"].values[clean]
    print(f"  特征数={len(feat_cols)}  样本数 n={n}")

    # ── 建图 + 指纹核对（官方锚点：EGSG 数组宽 121,396 / geo 132,760）──
    t0 = time.time()
    egsg_ei, egsg_ew = wi.build_egsg(lon, lat, elev_arr)
    t_egsg = time.time() - t0
    t0 = time.time()
    geo_ei, geo_ew = wi.build_geo(lon, lat)
    t_geo = time.time() - t0
    print(f"  EGSG 数组宽={egsg_ei.shape[1]:>7}  ({t_egsg:.1f}s)   官方锚点 121,396  "
          f"{'命中' if egsg_ei.shape[1] == 121396 else '★不一致★'}")
    print(f"  geo  数组宽={geo_ei.shape[1]:>7}  ({t_geo:.1f}s)   官方锚点 132,760  "
          f"{'命中' if geo_ei.shape[1] == 132760 else '★不一致★'}")

    # ── 主循环：逐行照抄 window_I.main() 第 177-228 行 ──
    configs = [
        ("RF", "rf", None, None), ("MLP", "mlp", None, None),
        ("GCN+Geo", "gcn", geo_ei, geo_ew), ("GCN+EGSG", "gcn", egsg_ei, egsg_ew),
        ("SAGE+Geo", "sage", geo_ei, geo_ew), ("SAGE+EGSG", "sage", egsg_ei, egsg_ew),
        ("GAT+Geo", "gat", geo_ei, geo_ew), ("GAT+EGSG", "gat", egsg_ei, egsg_ew),
        ("APPNP+Geo", "appnp", geo_ei, geo_ew), ("APPNP+EGSG", "appnp", egsg_ei, egsg_ew),
    ]
    MODEL = {"mlp": wi.MLP, "gcn": wi.GCN, "sage": wi.GraphSAGE,
             "gat": wi.GAT, "appnp": wi.APPNPNet}

    results = []
    for cfg_name, cfg_type, ei, ew in configs:
        print(f"  [{cfg_name}] ", end="", flush=True)
        t_cfg = time.time()
        r2_list = []
        for seed in seeds:
            idx = np.arange(n)
            ti, tmp = wi.train_test_split(idx, test_size=wi.VAL_RATIO + wi.TEST_RATIO,
                                          random_state=seed)
            vi, tei = wi.train_test_split(tmp, test_size=wi.TEST_RATIO / (wi.VAL_RATIO + wi.TEST_RATIO),
                                          random_state=seed)
            tm = np.zeros(n, dtype=bool); vm = np.zeros(n, dtype=bool); testm = np.zeros(n, dtype=bool)
            tm[ti] = True; vm[vi] = True; testm[tei] = True
            xs = wi.StandardScaler(); Xs = np.zeros_like(X_c)
            Xs[tm] = xs.fit_transform(X_c[tm]); Xs[vm] = xs.transform(X_c[vm]); Xs[tei] = xs.transform(X_c[tei])
            Xs = np.nan_to_num(Xs, nan=0.0)
            ys = wi.StandardScaler(); ys_arr = np.zeros_like(y_c)
            ys_arr[tm] = ys.fit_transform(y_c[tm].reshape(-1, 1)).flatten()
            ys_arr[vm] = ys.transform(y_c[vm].reshape(-1, 1)).flatten()
            ys_arr[tei] = ys.transform(y_c[tei].reshape(-1, 1)).flatten()

            if cfg_type == "rf":
                r2, rmse, mae = wi.train_rf(Xs, ys_arr, tm, testm, seed); ep = 0
            else:
                # MLP 无图：照抄 window_I 第 199-200 行，传 (2,0) 空边而非 None
                _ei = np.zeros((2, 0), dtype=np.int64) if cfg_type == "mlp" else ei
                _ew = None if cfg_type == "mlp" else ew
                r2, rmse, mae, ep = wi.train_gnn(MODEL[cfg_type], Xs, ys_arr, _ei, _ew,
                                                 tm, vm, testm, seed)
            results.append({"method": cfg_name, "seed": seed, "r2": r2,
                            "rmse": rmse, "mae": mae, "best_epoch": ep})
            r2_list.append(r2)
        print(f"R2={np.mean(r2_list):.4f}+-{np.std(r2_list):.4f}   ({time.time()-t_cfg:.0f}s)")

    df_res = pd.DataFrame(results)
    df_res.to_csv(outdir / "raw_seed_results_backbone.csv", index=False, encoding="utf-8-sig")

    # ── 配对比较（照抄 window_I 第 217-230 行）──
    comps = [("GCN+EGSG", "GCN+Geo"), ("SAGE+EGSG", "SAGE+Geo"), ("GAT+EGSG", "GAT+Geo"),
             ("APPNP+EGSG", "APPNP+Geo"), ("GCN+EGSG", "RF"), ("GCN+EGSG", "MLP")]
    from scipy import stats as sp_stats
    comp_results = []
    for ma, mb in comps:
        a = df_res[df_res["method"] == ma]["r2"].values
        b = df_res[df_res["method"] == mb]["r2"].values
        if len(a) == len(b) and len(a) > 0:
            t, p = sp_stats.ttest_rel(a, b)
            diff = a - b
            d = np.mean(diff) / np.std(diff) if np.std(diff) > 0 else 0
            comp_results.append({"comparison": f"{ma} vs {mb}", "mean_diff": np.mean(a) - np.mean(b),
                                 "ttest_p": p, "cohens_d": d})
    pd.DataFrame(comp_results).to_csv(outdir / "paired_comparison_backbone.csv",
                                      index=False, encoding="utf-8-sig")

    # ── 汇总 + 与论文对照 ──
    print("\n" + "=" * 78)
    print(f"phase={phase}  seeds={len(seeds)}")
    print(f"{'Backbone':<11}{'Geo(本次)':>18}{'EGSG(本次)':>18}{'dR2':>9}{'p':>12}")
    print("-" * 78)
    summary = {}
    for b in ["GCN", "SAGE", "GAT", "APPNP"]:
        ge = df_res[df_res["method"] == f"{b}+Geo"]["r2"].values
        eg = df_res[df_res["method"] == f"{b}+EGSG"]["r2"].values
        _, p = sp_stats.ttest_rel(eg, ge)
        summary[b] = (ge.mean(), ge.std(), eg.mean(), eg.std(), eg.mean() - ge.mean(), p)
        print(f"{b:<11}{ge.mean():>11.4f}+-{ge.std():.4f}{eg.mean():>11.4f}+-{eg.std():.4f}"
              f"{eg.mean()-ge.mean():>+9.4f}{p:>12.3e}")
    rf = df_res[df_res["method"] == "RF"]["r2"]
    mlp = df_res[df_res["method"] == "MLP"]["r2"]
    print(f"{'RF':<11}{'':>18}{rf.mean():>11.4f}+-{rf.std():.4f}")
    print(f"{'MLP':<11}{'':>18}{mlp.mean():>11.4f}+-{mlp.std():.4f}")

    print("\n-- 与论文 tab:bb 对照（3 位小数）--")
    for b, (pg, pgs, pe, pes) in PAPER.items():
        g, gs, e, es, d, p = summary[b]
        flag = "命中" if (round(g, 3) == pg and round(e, 3) == pe) else "★不符★"
        print(f"  {b:<10} 本次 Geo {g:.3f}/{gs:.3f}  EGSG {e:.3f}/{es:.3f}   |   "
              f"论文 Geo {pg:.3f}/{pgs:.3f}  EGSG {pe:.3f}/{pes:.3f}   => {flag}")

    print(f"\n输出目录: {outdir}")


if __name__ == "__main__":
    main()
