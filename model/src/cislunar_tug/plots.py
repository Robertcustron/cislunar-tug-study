"""Charts for the trade study (optional: requires matplotlib)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend: no display needed
import matplotlib.pyplot as plt  # noqa: E402

from .trades import Row  # noqa: E402

BLUE = "#1f5f99"
ORANGE = "#c46a1b"


def plot_thrust_sweep(table_rows: list[Row], dense_rows: list[Row], path: Path) -> None:
    """Round-trip time and round trips in life vs EP power (Step 4 main chart).

    Args:
        table_rows: The configured thrust levels (MDN §6.3), drawn as labelled points.
        dense_rows: A fine sweep over the same range, drawn as continuous curves so
            the trip-count steps appear at the correct power.
        path: PNG output path.
    """
    fig, ax_time = plt.subplots(figsize=(7, 4.2), dpi=150)

    ax_time.plot(
        [float(r["power_kw"]) for r in dense_rows],
        [float(r["round_trip_years"]) for r in dense_rows],
        color=BLUE,
    )
    ax_time.plot(
        [float(r["power_kw"]) for r in table_rows],
        [float(r["round_trip_years"]) for r in table_rows],
        "o",
        color=BLUE,
    )
    ax_time.set_xlabel("Electric propulsion power [kW]")
    ax_time.set_ylabel("Round-trip time [years]", color=BLUE)
    ax_time.grid(True, alpha=0.3)

    ax_trips = ax_time.twinx()
    ax_trips.step(
        [float(r["power_kw"]) for r in dense_rows],
        [int(r["trips_in_life"]) for r in dense_rows],
        where="post",
        color=ORANGE,
    )
    ax_trips.set_ylabel("Round trips in design life [-]", color=ORANGE)

    for row in table_rows:
        ax_time.annotate(
            f"{row['trips_in_life']} trips",
            (float(row["power_kw"]), float(row["round_trip_years"])),
            textcoords="offset points",
            xytext=(6, 6),
            fontsize=8,
        )

    ax_time.set_title("Power vs round-trip time (constant dry mass, Issue 2 baseline)")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
