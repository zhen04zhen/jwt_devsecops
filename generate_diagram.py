import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(22, 8))
ax.set_xlim(0, 22)
ax.set_ylim(-7, 2.5)
ax.axis("off")
fig.patch.set_facecolor("white")

GREEN      = "#4CAF50"
GRAY       = "#888888"
LINE_COLOR = "#AAAAAA"
LW         = 2.2
Y_MAIN     = 0
R_MAIN     = 0.38
R_SUB      = 0.30

# parallel=True  → bracket style（並行）
# parallel=False → arrow style（循序）
stages = [
    {"x": 0.6,  "label": "Start",          "color": GRAY,  "subtasks": [],                                                   "parallel": True},
    {"x": 2.8,  "label": "Repo Scan",       "color": GREEN, "subtasks": ["Secret Scan\n(Gitleaks)"],                          "parallel": True},
    {"x": 5.4,  "label": "Build",           "color": GREEN, "subtasks": ["Install Deps\n(pip install)"],                      "parallel": True},
    {"x": 8.8,  "label": "Static Analysis", "color": GREEN, "subtasks": ["Unit Tests\n(pytest)", "SAST\n(ShiftLeft)", "Dependency Scan\n(pip-audit)"], "parallel": False},
    {"x": 13.4, "label": "Package",         "color": GREEN, "subtasks": ["Docker Build"],                                     "parallel": True},
    {"x": 16.2, "label": "Image Analysis",  "color": GREEN, "subtasks": ["Container Scan\n(Trivy)", "Dockerfile Scan\n(Dockle)"], "parallel": False},
    {"x": 19.4, "label": "Reports",         "color": GREEN, "subtasks": ["Upload\nArtifacts"],                                "parallel": True},
    {"x": 21.0, "label": "End",             "color": GRAY,  "subtasks": [],                                                   "parallel": True},
]

# Main horizontal line
ax.plot([0.6, 21.0], [Y_MAIN, Y_MAIN], color=LINE_COLOR, lw=LW, zorder=1)

for stage in stages:
    x        = stage["x"]
    color    = stage["color"]
    subs     = stage["subtasks"]
    parallel = stage["parallel"]

    # Main circle
    c = plt.Circle((x, Y_MAIN), R_MAIN, color=color, zorder=3)
    ax.add_patch(c)
    sym = "✓" if color == GREEN else ""
    ax.text(x, Y_MAIN, sym, ha="center", va="center",
            fontsize=13, color="white", fontweight="bold", zorder=4)

    # Stage label above
    ax.text(x, Y_MAIN + R_MAIN + 0.25, stage["label"],
            ha="center", va="bottom", fontsize=9.5,
            fontweight="bold", color="#333333")

    if not subs:
        continue

    n       = len(subs)
    sub_gap = 1.55

    # Trunk from main circle down to first sub
    trunk_top    = Y_MAIN - R_MAIN
    trunk_bottom = Y_MAIN - R_MAIN - sub_gap * 0.55
    ax.plot([x, x], [trunk_top, trunk_bottom],
            color=LINE_COLOR, lw=LW * 0.85, zorder=2)

    if parallel:
        # ── Bracket style（並行）──
        rail_x  = x - 0.52
        first_y = Y_MAIN - R_MAIN - sub_gap
        last_y  = first_y - sub_gap * (n - 1)

        if n > 1:
            ax.plot([rail_x, rail_x], [first_y, last_y],
                    color=LINE_COLOR, lw=LW * 0.75, zorder=2,
                    solid_capstyle="round")

        for i, task in enumerate(subs):
            sy = first_y - sub_gap * i

            if n > 1:
                ax.plot([rail_x, x - R_SUB], [sy, sy],
                        color=LINE_COLOR, lw=LW * 0.75, zorder=2)
            else:
                ax.plot([x, x], [trunk_bottom, sy + R_SUB],
                        color=LINE_COLOR, lw=LW * 0.75, zorder=2)

            sc = plt.Circle((x, sy), R_SUB, color=GREEN,
                             ec="white", lw=1.2, zorder=3)
            ax.add_patch(sc)
            ax.text(x, sy, "✓", ha="center", va="center",
                    fontsize=10, color="white", fontweight="bold", zorder=4)
            ax.text(x, sy - R_SUB - 0.12, task,
                    ha="center", va="top", fontsize=8.2, color="#444444")

            if i == 0 and n > 1:
                ax.plot([x, x], [trunk_bottom, sy + R_SUB],
                        color=LINE_COLOR, lw=LW * 0.75, zorder=2)

    else:
        # ── Arrow style（循序）──
        first_y = Y_MAIN - R_MAIN - sub_gap

        for i, task in enumerate(subs):
            sy = first_y - sub_gap * i

            if i == 0:
                # trunk to first sub
                ax.annotate("", xy=(x, sy + R_SUB),
                            xytext=(x, trunk_bottom),
                            arrowprops=dict(arrowstyle="-|>",
                                            color=LINE_COLOR, lw=LW * 0.85))
            else:
                # arrow from previous sub to this one
                prev_y = first_y - sub_gap * (i - 1)
                ax.annotate("", xy=(x, sy + R_SUB),
                            xytext=(x, prev_y - R_SUB),
                            arrowprops=dict(arrowstyle="-|>",
                                            color=LINE_COLOR, lw=LW * 0.85))

            sc = plt.Circle((x, sy), R_SUB, color=GREEN,
                             ec="white", lw=1.2, zorder=3)
            ax.add_patch(sc)
            ax.text(x, sy, "✓", ha="center", va="center",
                    fontsize=10, color="white", fontweight="bold", zorder=4)
            ax.text(x, sy - R_SUB - 0.12, task,
                    ha="center", va="top", fontsize=8.2, color="#444444")

plt.tight_layout(pad=0.5)
plt.savefig(
    "C:/Users/zhen9/Desktop/DevSecOps/jwt-devsecops/pipeline_diagram.png",
    dpi=150, bbox_inches="tight", facecolor="white"
)
print("Done")
