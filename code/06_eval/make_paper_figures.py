"""
论文实验图表生成（Figure 4: 主结果）。
数据源: assets/experiments/full_low/*.json + /tmp 各评估结果
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "paper", "figures")

# 配色（色盲友好）
C_A, C_B, C_C, C_D = "#4C72B0", "#DD8452", "#55A868", "#C44E52"

# ---------- Fig 4a: clean vs cloaked 位精度分布（冲突） ----------
# 数据：干净 100 张 vs 遮蔽 1000 张
clean = json.load(open("/tmp/clean100_dec.json"))
cloak = json.load(open("/tmp/soft_B_q-1.json"))  # B 组 sw2 在遮蔽图上
accs_clean = [r["bit_accuracy"] for r in clean["results"]]
accs_cloak = [r["bit_accuracy"] for r in cloak["results"]]

fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

# 4a: 直方图
ax = axes[0]
ax.hist(accs_clean, bins=20, alpha=0.6, color=C_A, label="clean faces", density=True)
ax.hist(accs_cloak, bins=30, alpha=0.6, color=C_C, label="cloaked faces", density=True)
ax.axvline(0.95, ls="--", color="gray", lw=1)
ax.text(0.955, ax.get_ylim()[1]*0.95, "TPR@95%", fontsize=8)
ax.set_xlabel("bit accuracy")
ax.set_ylabel("density")
ax.set_title("(a) Cloaking breaks watermark decoding")
ax.legend(fontsize=8)

# 4b: scaling_w 扫描（鲁棒性 vs 质量）
sw = [2.0, 4.0, 5.0, 6.0]
tpr95 = [6.0, 40.0, 70.0, 75.0]   # clean TPR@95% (20 张 pilot)
tpr50 = [0.0, 0.0, 0.0, 20.0]     # JPEG50 TPR@95%
psnr = [38.0, 33.0, 30.2, 28.8]
ax = axes[1]
ax2 = ax.twinx()
l1, = ax.plot(sw, tpr95, "o-", color=C_A, label="clean TPR@95%")
l2, = ax.plot(sw, tpr50, "s--", color=C_D, label="JPEG50 TPR@95%")
l3, = ax2.plot(sw, psnr, "^-", color=C_B, label="PSNR (dB)")
ax.set_xlabel("watermark strength $\\beta$ (scaling_w)")
ax.set_ylabel("TPR@95% (%)")
ax2.set_ylabel("PSNR (dB)")
ax.set_title("(b) Strength calibration trade-off")
ax.legend(handles=[l1, l2, l3], fontsize=8, loc="center right")

# 4c: 四组对照（1000 张）
groups = ["A\ncloak", "B\n+WM global", "C\n+WM safe-region"]
keep = [47.4, 36.1, 42.1]
sim = [0.426, 0.480, 0.452]
wm = [None, 99.2, 98.6]
x = np.arange(3)
ax = axes[2]
b1 = ax.bar(x - 0.18, keep, 0.36, color=[C_A, C_B, C_C], label="retention (keep%)")
ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=9)
ax.set_ylabel("cloaking retention (%)")
ax.set_ylim(0, 60)
for xi, v in zip(x, keep):
    ax.text(xi - 0.18, v + 1, f"{v:.1f}", ha="center", fontsize=8)
ax2b = ax.twinx()
ax2b.plot(x, [s*100 for s in sim], "D-", color="k", markersize=5, label="mean sim (×100)")
ax2b.set_ylabel("mean embedding sim", color="k")
ax2b.set_ylim(30, 55)
ax.set_title("(c) Main comparison (n=1,000, $\\beta$=6)")
ax.legend(fontsize=8, loc="upper left")

plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig4_main_results.png"), dpi=300, bbox_inches="tight")
print("saved fig4_main_results.png")

# ---------- Fig 5: JPEG 鲁棒性（BER TPR） ----------
fig, ax = plt.subplots(figsize=(6, 4.5))
jpeg = ["clean", "JPEG80", "JPEG50"]
B_ber = [99.2, 99.6, 93.7]
C_ber = [98.6, 99.0, 92.7]
B_sw2 = [6.0, 16.2, 0.3]
x = np.arange(3)
ax.plot(x, B_ber, "o-", color=C_B, lw=2, label="B: global ($\\beta$=6)")
ax.plot(x, C_ber, "s-", color=C_C, lw=2, label="C: safety-region ($\\beta$=6)")
ax.plot(x, B_sw2, "x--", color=C_A, lw=2, label="B: global ($\\beta$=2)")
ax.set_xticks(x); ax.set_xticklabels(jpeg)
ax.set_ylabel("detection TPR (BER≤0.25) (%)")
ax.set_ylim(0, 105)
ax.legend(fontsize=9)
ax.set_title("JPEG robustness of watermark detection")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig5_jpeg_robustness.png"), dpi=300, bbox_inches="tight")
print("saved fig5_jpeg_robustness.png")

# ---------- Fig 6: BER 阈值敏感性曲线（θ TPR/FPR 权衡） ----------
import json as _json
data = _json.load(open(os.path.join(ROOT, "assets/experiments/new_results_20260817.json")))
curves = data["ber_curve"]["curves"]
ths = [c["theta"] for c in curves]
tpr_lowB = [c["tpr_low_B"]*100 for c in curves]
tpr_lowC = [c["tpr_low_C"]*100 for c in curves]
tpr_midB = [c["tpr_mid_B"]*100 for c in curves]
fpr_low = [c["fpr_low"]*100 for c in curves]
fpr_mid = [c["fpr_mid"]*100 for c in curves]

fig, ax = plt.subplots(figsize=(6.2, 4.5))
ax.plot(ths, tpr_lowB, "o-", color=C_B, lw=2, label="TPR B: global (low, $\\beta$=6)")
ax.plot(ths, tpr_lowC, "s-", color=C_C, lw=2, label="TPR C: safety-region (low, $\\beta$=6)")
ax.plot(ths, tpr_midB, "^-", color="#C44E52", lw=2, label="TPR B (mid, $\\beta$=6)")
ax.plot(ths, fpr_low, "x--", color=C_A, lw=2, label="FPR (low, unwatermarked)")
ax.plot(ths, fpr_mid, "d--", color="#8C6D31", lw=2, label="FPR (mid, unwatermarked)")
ax.axvline(0.25, ls=":", color="gray", lw=1)
ax.text(0.255, 5, "$\\theta$=0.25", fontsize=8, color="gray")
ax.set_xlabel("detection threshold $\\theta$ (BER)")
ax.set_ylabel("TPR / FPR (%)")
ax.set_ylim(0, 105)
ax.legend(fontsize=8, loc="lower right")
ax.set_title("BER threshold sensitivity: TPR vs FPR")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "fig6_ber_curve.png"), dpi=300, bbox_inches="tight")
print("saved fig6_ber_curve.png")
