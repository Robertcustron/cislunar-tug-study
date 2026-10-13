"""Draw the study report figures from the model outputs and the study documents.

The data in every figure is read from files in the repository:

- model/results/baseline/*.csv   (run `cislunar-tug run` first)
- requirements/*.csv
- docs/logical-architecture.md   (component exchange table, section 5)
- docs/trl-and-cost.md           (critical technology table)

A few annotations restate fixed design-point facts in words (25 kW, 9 trips,
5+1 strings, 54 matings, the 1.66-year SR-04 limit); they match the files above
but are typed, so update them if the design point changes.

Run from the repository root:

    python report/figures/make_figures.py

The figures are written next to this script as PDF (for LaTeX) and PNG (for
previews). They are report figures, not Capella diagrams: the Capella exports
live in capella/diagrams/ and are shown in Appendix B of the report.
"""

from __future__ import annotations

import csv
import math
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "model" / "results" / "baseline"
REQS = ROOT / "requirements"
OUT = Path(__file__).resolve().parent

# Palette after the ESA deep navy and cyan, plus a light slate and neutrals.
ESA_NAVY, ESA_SLATE, ESA_CYAN = "#003247", "#335e6f", "#0098db"
BLUE, ORANGE, AQUA = ESA_NAVY, ESA_CYAN, "#8aa5b0"  # main series, highlight, third category
BLUE_LIGHT, ORANGE_LIGHT = "#9fcbe3", "#b3dff4"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8984"
GRID, SURFACE, PANEL = "#e4e3df", "#ffffff", "#f4f3f0"

FULL_W, HALF_W = 6.3, 3.05  # inches (16 cm text width)

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Liberation Sans", "DejaVu Sans"],
        "font.size": 8,
        "axes.titlesize": 8.5,
        "axes.labelsize": 8,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK2,
        "axes.linewidth": 0.6,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "legend.frameon": False,
        "legend.fontsize": 7.5,
        "pdf.fonttype": 42,
        "savefig.dpi": 220,
    }
)


# ----------------------------------------------------------------------------- data


def read_csv(path: Path) -> list[dict[str, str]]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def design_row() -> dict[str, str]:
    for r in read_csv(RESULTS / "power_trade.csv"):
        if float(r["power_kw"]) == 25.0:
            return r
    raise ValueError("25 kW design point missing from power_trade.csv")


def component_exchanges() -> list[dict[str, str]]:
    """Parse the component exchange table (section 5) of docs/logical-architecture.md."""
    text = (ROOT / "docs" / "logical-architecture.md").read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        m = re.match(r"\|\s*(CE-\d+)\s*\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|", line)
        if m:
            src, dst = [s.strip() for s in m.group(3).split("→")]
            rows.append(
                {
                    "id": m.group(1),
                    "name": m.group(2).strip(),
                    "from": src,
                    "to": dst,
                    "kind": m.group(5).strip(),
                }
            )
    if len(rows) != 20:
        raise ValueError(f"Expected 20 component exchanges, found {len(rows)}")
    return rows


def sr_refs(text: str) -> list[str]:
    """System requirement IDs in a derived_from cell, with ranges such as "SR-14 to SR-16" expanded."""
    ids: list[str] = []
    for a, b in re.findall(r"SR-(\d+)(?:\s*to\s*SR-(\d+))?", text):
        lo, hi = int(a), int(b or a)
        ids += [f"SR-{i:02d}" for i in range(lo, hi + 1)]
    return ids


def critical_technologies() -> list[tuple[str, int, int]]:
    """(ID, TRL now, target TRL) from the critical technology table of docs/trl-and-cost.md."""
    text = (ROOT / "docs" / "trl-and-cost.md").read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 6 and re.fullmatch(r"CT-\d", cells[0]) and cells[3].startswith("**"):
            rows.append((cells[0], int(cells[3].strip("*")), int(cells[5].split()[0])))
    if len(rows) != 5:
        raise ValueError(f"Expected 5 critical technologies, found {len(rows)}")
    return rows


def save(fig, name: str, close: bool = True) -> None:
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", pad_inches=0.02)
    if close:
        plt.close(fig)
    print(f"  {name}")


# ----------------------------------------------------------------------------- figures


def fig_concept() -> None:
    """Mission concept: staging orbit, spiral out, NRHO, return. Schematic, not to scale."""
    from matplotlib.path import Path as MPath

    d = design_row()
    out_d, ret_d = float(d["outbound_days"]), float(d["return_days"])
    trips, rt = int(d["trips_in_life"]), float(d["round_trip_years"])
    xe = float(d["propellant_per_trip_t"])

    fig = plt.figure(figsize=(FULL_W, 3.05))
    ax = fig.add_axes([0.0, 0.34, 1.0, 0.66])
    tx = fig.add_axes([0.0, 0.0, 1.0, 0.31])
    tx.axis("off")
    ax.set_xlim(-2.75, 11.0)
    ax.set_ylim(-2.05, 2.05)
    ax.set_aspect("equal")
    ax.axis("off")

    # Earth: flat disc with a darker limb, and the GTO-class staging orbit
    ax.add_patch(Circle((0, 0), 0.34, color=ESA_SLATE, zorder=6))
    ax.add_patch(Circle((-0.04, 0.04), 0.27, color=ESA_CYAN, zorder=6))
    ax.add_patch(Ellipse((0.62, 0), 2.3, 0.78, fill=False, ec=ESA_NAVY, lw=1.0, zorder=4))
    ax.text(0, -0.42, "Earth", ha="center", va="top", color=INK2, fontsize=6.4, zorder=7)
    ax.text(-2.7, -1.88, "Staging orbit (GTO-class)", ha="left", va="center", color=ESA_NAVY, fontsize=6.2)
    ax.plot([-0.85, 0.85], [-1.74, -0.385], color=ESA_NAVY, lw=0.5, zorder=7)

    # Outbound: low-thrust spiral (drawn clockwise) from the staging-orbit apogee ...
    k, r0, flat = 0.056, 1.77, 0.47
    t_end = 5.5 * math.pi - 0.18
    xs, ys = [], []
    for i in range(700):
        t = t_end * i / 699
        r = r0 + k * t
        xs.append(r * math.cos(t))
        ys.append(-flat * r * math.sin(t))
    ax.plot(xs, ys, color=ESA_CYAN, lw=0.85, zorder=3, solid_capstyle="round")
    # ... and leaves tangentially towards the Moon
    r_e = r0 + k * t_end
    dx = k * math.cos(t_end) - r_e * math.sin(t_end)
    dy = -flat * (k * math.sin(t_end) + r_e * math.cos(t_end))
    n = math.hypot(dx, dy)
    p0 = (xs[-1], ys[-1])
    p1 = (p0[0] + 3.0 * dx / n, p0[1] + 3.0 * dy / n)
    path = MPath([p0, p1, (6.2, 2.0), (8.66, 1.4)], [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4])
    ax.add_patch(
        FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=8, color=ESA_CYAN, lw=1.5, zorder=3)
    )
    ax.text(
        5.0,
        1.52,
        f"Outbound \u2248 {out_d:.0f} d",
        ha="center",
        va="top",
        color=ESA_NAVY,
        fontsize=6.6,
        fontweight="bold",
    )
    ax.text(5.0, 1.22, "25 kW solar-electric, 5 t cargo", ha="center", va="top", color=INK2, fontsize=6.1)

    # Moon and NRHO (elongated loop around the Moon; periapsis close to the Moon)
    ax.add_patch(Ellipse((9.0, 0.38), 0.74, 2.36, fill=False, ec=ESA_NAVY, lw=1.0, zorder=4))
    ax.add_patch(Circle((9.0, -0.5), 0.18, color="#a9b4ba", ec=ESA_SLATE, lw=0.6, zorder=5))
    ax.text(9.0, -0.9, "Moon", ha="center", va="top", color=INK2, fontsize=6.4)
    ax.text(9.45, 1.3, "NRHO", ha="left", va="center", color=ESA_NAVY, fontsize=7.2, fontweight="bold")

    # Return leg
    ax.add_patch(
        FancyArrowPatch(
            (8.66, -0.4),
            (1.8, -0.2),
            connectionstyle="arc3,rad=-0.36",
            arrowstyle="-|>",
            mutation_scale=8,
            color=ESA_NAVY,
            lw=1.2,
            ls=(0, (3.5, 2)),
            zorder=5,
        )
    )
    ax.text(
        5.45,
        -1.6,
        f"Return \u2248 {ret_d:.0f} d",
        ha="center",
        va="top",
        color=ESA_NAVY,
        fontsize=6.6,
        fontweight="bold",
    )
    ax.text(5.45, -1.86, "lighter tug, up to 0.5 t cargo", ha="center", va="top", color=INK2, fontsize=6.1)

    def badge(x, y, n, axes=ax, **kw):
        axes.add_patch(Circle((x, y), 0.17, color=ESA_NAVY, ec="white", lw=1.0, zorder=8, **kw))
        axes.text(
            x,
            y,
            str(n),
            ha="center",
            va="center",
            color="white",
            fontsize=6.0,
            fontweight="bold",
            zorder=9,
            **kw,
        )

    badge(-0.55, 0.42, 1)
    badge(0.95, 0.42, 2)
    badge(3.2, 1.55, 3)
    badge(8.4, 0.75, 4)
    badge(9.6, -0.45, 5)
    badge(5.45, -1.3, 6)
    badge(2.45, -0.72, 7)
    ax.text(
        11.0,
        -2.05,
        "Schematic, not to scale",
        ha="right",
        va="bottom",
        color=MUTED,
        fontsize=6.0,
        style="italic",
    )

    items = [
        "Ariane 64 to the GTO-class staging orbit: the cargo and a\npassive xenon propellant module, one launch per trip",
        "Capture the cargo and module as one stack; transfer the\nxenon (up to 21 days); release the empty module",
        f"Outbound spiral with 25 kW of electric propulsion, 1.46 N:\n2.64 km/s, about {out_d:.0f} days with 5 t of cargo",
        "Approach after clearance, dock and hand over the\ncargo in NRHO",
        "Collect up to 0.5 t of return cargo (optional)",
        f"Return spiral, about {ret_d:.0f} days with the lighter tug",
        f"Hand over the return cargo, refuel {xe:.2f} t of xenon and\nrepeat: {trips} round trips of {rt:.1f} years in 15 years",
    ]
    tx.plot([0.0, 1.0], [1.0, 1.0], color=GRID, lw=0.8, transform=tx.transAxes, clip_on=False)
    col_x = [0.015, 0.515]
    for i, t in enumerate(items):
        c, row = (0, i) if i < 4 else (1, i - 4)
        x, y = col_x[c], 0.9 - row * 0.245
        tx.plot(
            [x + 0.008],
            [y - 0.055],
            "o",
            ms=8.0,
            color=ESA_NAVY,
            mec="white",
            mew=0.8,
            transform=tx.transAxes,
            clip_on=False,
        )
        tx.text(
            x + 0.008,
            y - 0.055,
            str(i + 1),
            transform=tx.transAxes,
            ha="center",
            va="center",
            color="white",
            fontsize=5.6,
            fontweight="bold",
        )
        tx.text(
            x + 0.03,
            y,
            t,
            transform=tx.transAxes,
            ha="left",
            va="top",
            fontsize=6.5,
            color=INK,
            linespacing=1.12,
        )
    save(fig, "fig01_mission_concept")


def fig_flowdown() -> None:
    """System requirements flowed down to PROP, PWR and DRI (links from the CSV derived_from column)."""
    subs = read_csv(REQS / "subsystem_requirements.csv")
    sys_ids = sorted({s for r in subs for s in sr_refs(r["derived_from"])}, key=lambda s: int(s[3:]))
    sys_text = {r["id"]: r["requirement"] for r in read_csv(REQS / "system_requirements.csv")}
    group_col = {"PROP": ORANGE, "PWR": BLUE, "DRI": AQUA}
    names = {
        "PROP": "Electric propulsion (PROP)",
        "PWR": "Electrical power (PWR)",
        "DRI": "Docking and refuelling interface (DRI)",
    }
    # Short labels for the figure only; the full text is in requirements/*.csv
    sys_short = {
        "SR-05": "15-year life, at least 9 round trips",
        "SR-07": "1.46 N at 2,100 s",
        "SR-08": "3,400 kg of usable xenon",
        "SR-09": "2,550 kg of xenon replenished per trip",
        "SR-10": "22.8 t of xenon over life",
        "SR-11": "25 kW to the thrusters at end of life",
        "SR-12": "Platform powered through 2.5 h eclipses",
        "SR-13": "Performance after the life dose",
        "SR-14": "Autonomous rendezvous and capture",
        "SR-15": "Dock only after approach clearance",
        "SR-16": "One standard docking interface",
        "SR-17": "Cargo release velocity",
        "SR-22": "Propellant reserve for disposal",
        "SR-25": "Cargo and module captured as one stack",
    }
    sub_short = {
        "PROP-01": "1.46 N with one thruster failed",
        "PROP-02": "3,400 kg xenon, 9 refills",
        "PROP-03": "90,000 h of thrusting over life",
        "PROP-04": "Disposal reserve (TBD)",
        "PROP-05": "Exchangeable module of 0.4 t or less",
        "PROP-06": "Proximity thrust for capture",
        "PWR-01": "25 kW to the PPUs plus 2 kW platform",
        "PWR-02": "Array sized for the life dose",
        "PWR-03": "2.5 h eclipse at 60 % DoD, 8.8 kWh",
        "PWR-04": "29.1 kW array at end of life",
        "DRI-01": "One androgynous docking port",
        "DRI-02": "2,550 kg of xenon in 21 days",
        "DRI-03": "At least 54 mating cycles",
        "DRI-04": "Release velocity (TBD)",
    }

    def label(table, key, fallback):
        return table.get(key) or (fallback[:40] + "...")

    order = [r for g in ("PROP", "PWR", "DRI") for r in subs if r["subsystem"] == g]
    gap = 1.7
    units = len(order) - 1 + 2 * gap
    ry, y, prev, heads = {}, 0.0, None, {}
    for r in order:
        if r["subsystem"] != prev:
            if prev:
                y += gap
            heads[r["subsystem"]] = 1 - (y - 0.95) / units
        ry[r["id"]] = 1 - y / units
        y += 1
        prev = r["subsystem"]
    ly = {s: 1 - i / (len(sys_ids) - 1) for i, s in enumerate(sys_ids)}

    fig, ax = plt.subplots(figsize=(FULL_W, 3.45))
    ax.axis("off")
    xl, xr = 0.425, 0.6
    for r in order:
        for s in sr_refs(r["derived_from"]):
            if s in ly:
                ax.plot(
                    [xl + 0.004, xr - 0.004],
                    [ly[s], ry[r["id"]]],
                    color=group_col[r["subsystem"]],
                    lw=0.9,
                    alpha=0.6,
                    solid_capstyle="round",
                )
    for s in sys_ids:
        ax.plot(xl, ly[s], "o", ms=4.5, color=INK, mec=SURFACE, mew=1.2, zorder=3)
        ax.text(
            0.068, ly[s], label(sys_short, s, sys_text[s]), ha="left", va="center", fontsize=6.5, color=INK
        )
        ax.text(0.0, ly[s], s, ha="left", va="center", fontsize=6.5, color=INK2, fontweight="bold")
    for r in order:
        ax.plot(xr, ry[r["id"]], "o", ms=4.5, color=group_col[r["subsystem"]], mec=SURFACE, mew=1.2, zorder=3)
        ax.text(
            xr + 0.012,
            ry[r["id"]],
            r["id"],
            ha="left",
            va="center",
            fontsize=6.5,
            color=INK2,
            fontweight="bold",
        )
        ax.text(
            xr + 0.098,
            ry[r["id"]],
            label(sub_short, r["id"], r["requirement"]),
            ha="left",
            va="center",
            fontsize=6.5,
            color=INK,
        )
    for g, yh in heads.items():
        ax.text(xr - 0.006, yh, names[g], ha="left", va="center", fontsize=6.6, color=INK, fontweight="bold")
        ax.plot([xr - 0.006 - 0.012], [yh], "s", ms=4.5, color=group_col[g])
    ax.text(0.0, 1.1, "System requirements", ha="left", fontsize=7.4, fontweight="bold", color=INK)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-0.04, 1.16)
    save(fig, "fig02_flowdown")


def fig_power_trade() -> None:
    rows = read_csv(RESULTS / "power_trade.csv")
    p = [float(r["power_kw"]) for r in rows]
    trips = [int(r["trips_in_life"]) for r in rows]
    rt = [float(r["round_trip_years"]) for r in rows]
    thrust = {float(r["power_kw"]): float(r["thrust_n"]) for r in rows}

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(HALF_W, 3.2), sharex=True, gridspec_kw={"hspace": 0.18})
    for a in (a1, a2):
        a.grid(axis="y")
        a.set_axisbelow(True)
        a.axvspan(24, 25, color=PANEL, zorder=0)
    a1.step(p, trips, where="post", color=MUTED, lw=0.8, zorder=1)
    a1.plot(p, trips, "o", color=BLUE, ms=4, mec=SURFACE, mew=1.0, zorder=3)
    a1.plot([25], [trips[p.index(25.0)]], "o", color=ORANGE, ms=6, mec=SURFACE, mew=1.2, zorder=4)
    a1.set_ylabel("Round trips in 15 years")
    a1.set_ylim(3, 18)
    a1.annotate(
        f"Design point\n25 kW, {thrust[25.0]:.2f} N, 9 trips",
        xy=(25, 9),
        xytext=(29.5, 5.0),
        fontsize=6.6,
        color=INK,
        arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6),
    )
    a1.annotate(
        "26 kW: 10 trips on a\n4 % power margin",
        xy=(26, 10),
        xytext=(15.5, 12.6),
        fontsize=6.6,
        color=INK2,
        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6),
    )

    a2.plot(p, rt, color=BLUE, lw=1.6)
    a2.plot([25], [rt[p.index(25.0)]], "o", color=ORANGE, ms=6, mec=SURFACE, mew=1.2, zorder=4)
    a2.axhline(1.66, color=INK2, lw=0.7, ls=(0, (3, 2)))
    a2.text(47.5, 1.70, "SR-04 limit 1.66 yr", ha="right", va="bottom", fontsize=6.4, color=INK2)
    a2.set_ylabel("Round trip [years]")
    a2.set_xlabel("Electric propulsion power at the PPU inputs [kW]")
    a2.set_ylim(0.6, 3.1)
    a2.set_xticks([12, 18, 24, 30, 36, 42, 48])
    save(fig, "fig03_power_trade")


def fig_logical_architecture() -> None:
    """Logical Architecture Blank in the Capella style: components, allocated functions and all
    component exchanges of docs/logical-architecture.md (section 5). Drawn for a landscape page."""
    ces = {c["id"]: c for c in component_exchanges()}
    W, H = 1640, 1010
    s = 1.4  # font scale for a figure printed at about 60 % on a landscape page
    font = plt.rcParams["font.sans-serif"]
    txt = "#1E1E1E"
    sys_fill, sys_edge = "#DCE9F6", "#4F7FB0"
    lc_fill, lc_edge = "#FFFFFF", "#2F5F94"
    act_fill, act_edge = "#EEF1F4", "#6C7A89"
    fn_fill, fn_edge = "#CFEAC0", "#4E8A3A"
    af_fill, af_edge = "#E3F1D9", "#6E9B5A"
    style = {  # by component exchange kind in the document: colour, width, dash
        "Power": ("#B85C00", 2.6, "-"),
        "Xenon": ("#12857A", 2.6, "-"),
        "Mechanical": ("#7A4A1E", 2.6, "-"),
        "Data": ("#2F67B1", 1.2, (0, (5, 3))),
        "Radio": ("#7B4FA0", 1.3, (0, (2, 2))),
        "Heat": ("#C0392B", 1.8, (0, (1, 1.5))),
    }

    fig, ax = plt.subplots(figsize=(W / 100, H / 100))
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)

    def box(x0, y0, x1, y1, label, fill, edge, sub="", actor=False, lw=1.3, z=1, fs=8.3):
        ax.add_patch(
            FancyBboxPatch(
                (x0, y0),
                x1 - x0,
                y1 - y0,
                boxstyle="square,pad=0",
                facecolor=fill,
                edgecolor=edge,
                lw=lw,
                zorder=z,
            )
        )
        ax.text(
            x0 + 7,
            y0 + 13,
            ("☺ " if actor else "") + label,
            fontsize=fs * s,
            fontweight="bold",
            color=txt,
            family=font,
            va="center",
            zorder=z + 4,
        )
        if sub:
            ax.text(
                x1 - 7,
                y0 + 13,
                sub,
                fontsize=6.6 * s,
                color="#555555",
                family=font,
                va="center",
                ha="right",
                zorder=z + 4,
            )

    def note(x, y, text, ha="right"):
        ax.text(
            x,
            y,
            text,
            fontsize=6.0 * s,
            color="#2F5F94",
            family=font,
            ha=ha,
            va="center",
            zorder=8,
            style="italic",
        )

    def fn(cx, cy, label, fid, actor=False, w=156, h=46):
        fill, edge = (af_fill, af_edge) if actor else (fn_fill, fn_edge)
        ax.add_patch(
            FancyBboxPatch(
                (cx - w / 2, cy - h / 2),
                w,
                h,
                boxstyle="round,pad=0,rounding_size=7",
                facecolor=fill,
                edgecolor=edge,
                lw=1.1,
                zorder=6,
            )
        )
        ax.text(
            cx,
            cy - 6,
            label,
            fontsize=6.4 * s,
            color=txt,
            family=font,
            ha="center",
            va="center",
            zorder=7,
            linespacing=1.0,
        )
        ax.text(
            cx,
            cy + 15,
            fid,
            fontsize=5.6 * s,
            color="#2F5A22",
            family=font,
            ha="center",
            va="center",
            zorder=7,
        )

    def route(cid, pts, lpos, ha="center"):
        c = ces[cid]
        col, w, ls = style[c["kind"]]
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=col, lw=w, ls=ls, zorder=4, solid_capstyle="butt")
        ax.add_patch(
            FancyArrowPatch(
                pts[-2],
                pts[-1],
                arrowstyle="-|>",
                mutation_scale=12 if w > 2 else 10,
                color=col,
                lw=0,
                zorder=5,
                shrinkA=0,
                shrinkB=0,
            )
        )
        ax.text(
            lpos[0],
            lpos[1],
            f"{cid}\n{c['name']}",
            fontsize=5.6 * s,
            color=col,
            ha=ha,
            va="center",
            family=font,
            zorder=9,
            linespacing=1.0,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.4, alpha=0.93),
        )

    box(240, 140, 1335, 885, "Cislunar Cargo Tug", sys_fill, sys_edge, lw=1.5, z=0, fs=8.0)
    ax.text(
        1327, 874, "Logical System", fontsize=6.4 * s, color="#555555", family=font, ha="right", va="center"
    )
    comps = [
        (260, 165, 470, 455, "Electrical power", "LC-2 PWR", "100 V bus · 29.1 kW EOL · 8.8 kWh"),
        (530, 165, 925, 330, "Command and data handling", "LC-5 CDH", ""),
        (980, 165, 1320, 330, "Communications", "LC-6 COMMS", ""),
        (530, 390, 925, 580, "Electric propulsion", "LC-1 PROP", "5+1 strings · 25 kW · ≥ 3,400 kg Xe"),
        (980, 390, 1320, 580, "Guidance, navigation and control", "LC-3 GNC", ""),
        (260, 505, 470, 600, "Thermal control", "LC-7 TCS", ""),
        (260, 715, 470, 830, "Structure", "LC-8 STR", ""),
        (
            530,
            630,
            1320,
            865,
            "Docking and refuelling interface",
            "LC-4 DRI",
            "1 androgynous port + xenon coupling · 54 matings",
        ),
    ]
    for x0, y0, x1, y1, name, lid, keyf in comps:
        box(x0, y0, x1, y1, name, lc_fill, lc_edge, sub=lid, z=2, fs=7.2)
        if keyf:
            note(x1 - 8, y1 - 12, keyf)
    note(462, 590, "3.3 kW")
    box(560, 22, 1335, 112, "Ground Segment", act_fill, act_edge, actor=True, fs=7.6)
    box(30, 190, 205, 280, "Sun", act_fill, act_edge, actor=True, fs=7.6)
    box(30, 600, 205, 690, "Propellant Module", act_fill, act_edge, actor=True, fs=7.2)
    box(30, 700, 205, 860, "Launch Vehicle", act_fill, act_edge, actor=True, fs=7.6)
    box(1385, 215, 1610, 885, "Lunar Orbit Destination", act_fill, act_edge, actor=True, fs=7.2)
    box(690, 915, 900, 1005, "Cargo Customer", act_fill, act_edge, actor=True, fs=7.6)

    funcs = {
        "SF-03.5": ("Generate\nelectrical power", 365, 222),
        "SF-03.6": ("Store and distribute\nelectrical power", 365, 292),
        "LF-06": ("Discharge and\nisolate batteries", 365, 362),
        "SF-07.1": ("Perform disposal\nmanoeuvre", 630, 222),
        "LF-02": ("Validate and\nroute commands", 825, 222),
        "SF-03.9": ("Manage modes\nand failures", 630, 290),
        "LF-03": ("Collect and\nformat telemetry", 825, 290),
        "LF-01": ("Receive radio\nmessages", 1150, 222),
        "LF-04": ("Transmit\ntelemetry", 1150, 290),
        "SF-03.1": ("Generate\nthrust", 630, 447),
        "SF-03.2": ("Store and feed\npropellant", 825, 447),
        "LF-05": ("Vent residual\npropellant", 630, 517),
        "LF-09": ("Provide proximity\nthrust", 825, 517),
        "SF-03.3": ("Determine orbit\nand attitude", 1065, 447),
        "SF-03.4": ("Control trajectory\nand attitude", 1235, 447),
        "SF-03.10": ("Rendezvous and\nproximity navigation", 1065, 517),
        "LF-07": ("Control temperatures\nand reject heat", 365, 556),
        "LF-08": ("Carry loads and\nlauncher interface", 365, 780),
        "SF-01": ("Capture cargo in\nEarth staging orbit", 630, 690),
        "SF-02": ("Receive propellant\nin orbit", 825, 690),
        "SF-04": ("Hand over cargo at\nlunar destination", 1235, 690),
        "SF-06": ("Hand over return\ncargo in Earth orbit", 825, 805),
        "SF-05": ("Collect return\ncargo", 1235, 805),
    }
    for fid, (lab, x, y) in funcs.items():
        fn(x, y, lab, fid)
    actf = [
        ("Plan end-of-life\ndisposal", 700, 70, "ACT-14"),
        ("Monitor and command\ntransport", 1150, 70, "ACT-13"),
        ("Provide\nsunlight", 117, 240, "A-20"),
        ("Supply propellant\nin orbit", 117, 648, "ACT-18"),
        ("Launch cargo and\npropellant", 117, 780, "ACT-04"),
        ("Clear approach\nand docking", 1497, 290, "ACT-15"),
        ("Receive delivered\ncargo", 1497, 745, "ACT-16"),
        ("Provide return\ncargo", 1497, 830, "ACT-17"),
        ("Receive returned\ncargo", 795, 968, "ACT-03"),
    ]
    for lab, x, y, src in actf:
        fn(x, y, lab, src, actor=True)

    routes = {
        "CE-01": ([(470, 425), (530, 425)], (500, 447)),
        "CE-02": ([(780, 630), (780, 580)], (788, 605), "left"),
        "CE-03": ([(980, 455), (925, 455)], (952, 474)),
        "CE-04": ([(640, 330), (640, 390)], (648, 360), "left"),
        "CE-05": ([(530, 200), (470, 200)], (500, 224)),
        "CE-06": ([(880, 330), (880, 362), (1065, 362), (1065, 390)], (972, 349)),
        "CE-07": ([(1200, 580), (1200, 630)], (1208, 605), "left"),
        "CE-08": ([(980, 214), (925, 214)], (952, 194)),
        "CE-09": ([(925, 300), (980, 300)], (952, 318)),
        "CE-10": ([(530, 560), (470, 560)], (500, 540)),
        "CE-11": ([(205, 790), (260, 790)], (232, 768)),
        "CE-12": ([(205, 712), (530, 712)], (365, 696)),
        "CE-13": ([(205, 648), (530, 648)], (365, 632)),
        "CE-14": ([(1070, 112), (1070, 165)], (1062, 140), "right"),
        "CE-15": ([(1250, 165), (1250, 112)], (1258, 140), "left"),
        "CE-16": ([(1385, 290), (1320, 290)], (1352, 270)),
        "CE-17": ([(1320, 745), (1385, 745)], (1352, 725)),
        "CE-18": ([(1385, 830), (1320, 830)], (1352, 810)),
        "CE-19": ([(780, 865), (780, 915)], (788, 890), "left"),
        "CE-20": ([(205, 240), (260, 240)], (232, 220)),
    }
    missing = set(ces) - set(routes)
    if missing:
        raise ValueError(f"No route for {sorted(missing)}: update the figure layout")
    for cid, r in routes.items():
        route(cid, r[0], r[1], r[2] if len(r) > 2 else "center")

    names = [
        ("Power", "Power (electrical energy, sunlight)"),
        ("Xenon", "Xenon"),
        ("Mechanical", "Cargo and mechanical"),
        ("Data", "On-board data"),
        ("Radio", "Radio link"),
        ("Heat", "Heat"),
    ]
    for i, (k, lab) in enumerate(names):
        col, w, ls = style[k]
        x, y = 1340 + (i // 3) * 160, 925 + (i % 3) * 26
        ax.plot([x, x + 30], [y, y], color=col, lw=w, ls=ls)
        ax.text(
            x + 36,
            y,
            lab.replace(" (electrical energy, sunlight)", ""),
            fontsize=6.0 * s,
            va="center",
            family=font,
            color=txt,
        )
    save(fig, "fig04_logical_architecture")


def fig_power_modes() -> None:
    rows = read_csv(RESULTS / "power_budget.csv")
    nominal = next(r for r in rows if r["component"].startswith("Total (nominal)"))
    margined = next(r for r in rows if r["component"].startswith("Total with"))
    modes = [k for k in rows[0] if k not in ("id", "component")]
    nom = [float(nominal[m]) / 1000 for m in modes]
    mar = [float(margined[m]) / 1000 - n for m, n in zip(modes, nom)]
    fig, ax = plt.subplots(figsize=(HALF_W, 2.35))
    x = range(len(modes))
    ax.bar(x, nom, width=0.55, color=BLUE, label="Nominal load")
    ax.bar(
        x,
        mar,
        bottom=nom,
        width=0.55,
        color=BLUE_LIGHT,
        label="20 % margin",
        edgecolor=SURFACE,
        linewidth=1.0,
    )
    ax.axhline(2.0, color=ORANGE, lw=1.2)
    ax.text(
        len(modes) - 0.6,
        2.04,
        "Platform allocation 2 kW (A-21)",
        ha="right",
        va="bottom",
        fontsize=6.4,
        color=INK,
    )
    worst = max(range(len(modes)), key=lambda i: nom[i] + mar[i])
    ax.text(
        worst,
        nom[worst] + mar[worst] + 0.04,
        f"{nom[worst] + mar[worst]:.2f}",
        ha="center",
        va="bottom",
        fontsize=6.4,
        color=INK,
    )
    ax.set_xticks(list(x))
    ax.set_xticklabels([m.capitalize() for m in modes], rotation=35, ha="right", fontsize=6.6)
    ax.set_ylabel("Platform load [kW]")
    ax.set_ylim(0, 2.3)
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=6.4, ncol=2)
    save(fig, "fig05_power_modes")


def fig_mass() -> None:
    rows = [r for r in read_csv(RESULTS / "mass_budget.csv") if r["lc"].startswith("LC-")]
    names = {
        "LC-1": "Electric propulsion",
        "LC-2": "Electrical power",
        "LC-3": "GNC",
        "LC-4": "Docking and refuelling",
        "LC-5": "Command and data",
        "LC-6": "Communications",
        "LC-7": "Thermal control",
        "LC-8": "Structure",
    }
    rows.sort(key=lambda r: float(r["with_margin_kg"]))
    totals = read_csv(RESULTS / "mass_budget.csv")
    tot = next(r for r in totals if r["lc"] == "Total")
    sysm = next(r for r in totals if r["lc"].startswith("Total with"))
    param = float(design_row()["dry_mass_t"]) * 1000

    fig, (a1, a2) = plt.subplots(
        1, 2, figsize=(FULL_W, 2.3), gridspec_kw={"width_ratios": [1.3, 1], "wspace": 0.5}
    )
    y = range(len(rows))
    nom = [float(r["nominal_kg"]) for r in rows]
    mar = [float(r["maturity_margin_kg"]) for r in rows]
    a1.barh(y, nom, height=0.6, color=BLUE, label="Nominal")
    a1.barh(
        y,
        mar,
        left=nom,
        height=0.6,
        color=BLUE_LIGHT,
        label="Maturity margin (5/10/20 %)",
        edgecolor=SURFACE,
        linewidth=1.0,
    )
    for i, r in enumerate(rows):
        a1.text(
            nom[i] + mar[i] + 18,
            i,
            f"{float(r['with_margin_kg']):,.0f}",
            va="center",
            fontsize=6.3,
            color=INK2,
        )
    a1.set_yticks(list(y))
    a1.set_yticklabels([names[r["lc"]] for r in rows], fontsize=6.6)
    a1.set_xlabel("Dry mass [kg]")
    a1.set_xlim(0, 1300)
    a1.grid(axis="x")
    a1.set_axisbelow(True)
    a1.legend(loc="lower right", fontsize=6.2)

    steps = [
        ("Bottom-up\nnominal", float(tot["nominal_kg"]), BLUE),
        ("+ maturity\nmargins", float(tot["with_margin_kg"]), BLUE),
        ("+ 20 %\nsystem", float(sysm["with_margin_kg"]), BLUE),
        ("Parametric\nbaseline", param, ORANGE),
    ]
    for i, (lab, v, c) in enumerate(steps):
        a2.bar(i, v / 1000, width=0.55, color=c)
        a2.text(i, v / 1000 + 0.08, f"{v / 1000:.2f} t", ha="center", va="bottom", fontsize=6.6, color=INK)
    a2.set_xticks(range(len(steps)))
    a2.set_xticklabels([s[0] for s in steps], fontsize=6.2)
    a2.set_ylabel("Tug dry mass [t]")
    a2.set_ylim(0, 7.2)
    a2.grid(axis="y")
    a2.set_axisbelow(True)
    save(fig, "fig06_mass_budget")


def fig_trl() -> None:
    short = {
        "CT-1": "Long-life 5 kW Hall thruster string",
        "CT-2": "Xenon transfer from a passive module",
        "CT-3": "39 kW array and 100 V power control",
        "CT-4": "Rendezvous and capture of a passive stack",
        "CT-5": "Propulsion-module exchange (backup path)",
    }
    cts = [(cid, short[cid], now, tgt) for cid, now, tgt in critical_technologies()]
    fig, ax = plt.subplots(figsize=(HALF_W, 1.9))
    for i, (cid, name, now, tgt) in enumerate(reversed(cts)):
        ax.plot([now, tgt], [i, i], color=GRID, lw=3.2, solid_capstyle="round", zorder=1)
        ax.plot(now, i, "o", color=ORANGE, ms=6.5, mec=SURFACE, mew=1.2, zorder=3)
        ax.plot(tgt, i, "o", color=BLUE, ms=6.5, mec=SURFACE, mew=1.2, zorder=3)
    ax.set_yticks(range(len(cts)))
    ax.set_yticklabels([c for c, *_ in reversed(cts)], fontsize=7)
    ax.set_xlim(1.5, 7.5)
    ax.set_xticks(range(2, 8))
    ax.set_xlabel("TRL for this application")
    ax.grid(axis="x")
    ax.set_axisbelow(True)
    ax.plot([], [], "o", color=ORANGE, ms=5, label="Today")
    ax.plot([], [], "o", color=BLUE, ms=5, label="Target, end of Phase B1")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=6.6, handletextpad=0.2)
    save(fig, "fig07_trl")


def fig_campaign() -> None:
    rows = read_csv(RESULTS / "launch_campaign.csv")
    fig, ax = plt.subplots(figsize=(HALF_W, 2.0))
    x = range(len(rows))
    tug = [int(r["tug_launches"]) for r in rows]
    direct = [int(r["direct_launches_same_cargo"]) for r in rows]
    w = 0.32
    ax.bar([i - w / 2 - 0.02 for i in x], tug, width=w, color=BLUE, label="Tug (1 tug + resupply launches)")
    ax.bar(
        [i + w / 2 + 0.02 for i in x],
        direct,
        width=w,
        color=ORANGE,
        label=f"Direct, {float(rows[0]['direct_cargo_per_launch_t']):.1f} t per launch",
    )
    for i in x:
        ax.text(i - w / 2 - 0.02, tug[i] + 0.2, str(tug[i]), ha="center", fontsize=6.6, color=INK)
        ax.text(i + w / 2 + 0.02, direct[i] + 0.2, str(direct[i]), ha="center", fontsize=6.6, color=INK)
    ax.set_xticks(list(x))
    ax.set_xticklabels(
        [
            f"{float(r['cargo_per_trip_t']):g} t per trip\n({float(r['cargo_over_life_t']):g} t in total)"
            for r in rows
        ],
        fontsize=6.4,
    )
    ax.set_ylabel("Ariane 64 launches")
    ax.set_ylim(0, 13)
    ax.set_yticks([0, 2, 4, 6, 8, 10, 12])
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.18), ncol=1, fontsize=6.2)
    save(fig, "fig08_launch_campaign")


if __name__ == "__main__":
    print("Writing report figures to", OUT.relative_to(ROOT))
    fig_concept()
    fig_flowdown()
    fig_power_trade()
    fig_logical_architecture()
    fig_power_modes()
    fig_mass()
    fig_trl()
    fig_campaign()
