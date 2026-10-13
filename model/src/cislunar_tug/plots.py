"""Charts for the trade study (optional: requires matplotlib)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend: no display needed
import matplotlib.pyplot as plt  # noqa: E402

from .trades import Row  # noqa: E402

# Palette after the ESA deep navy and cyan (same as the report figures).
BLUE = "#003247"  # navy: round trips
ORANGE = "#0098db"  # cyan: round-trip time


def plot_power_trade(table_rows: list[Row], dense_rows: list[Row], path: Path, note: str = "") -> None:
    """Trade 1: round trips in the design life and round-trip time vs EP power."""
    fig, ax_trips = plt.subplots(figsize=(7, 4.2), dpi=150)
    ax_trips.step(
        [float(r["power_kw"]) for r in dense_rows],
        [int(r["trips_in_life"]) for r in dense_rows],
        where="post",
        color=BLUE,
    )
    ax_trips.set_xlabel("Electric propulsion power [kW]")
    ax_trips.set_ylabel("Round trips in 15 years [-]", color=BLUE)
    ax_trips.grid(True, color="#e4e3df", linewidth=0.6)
    ax_trips.set_axisbelow(True)
    ax_time = ax_trips.twinx()
    ax_time.plot(
        [float(r["power_kw"]) for r in dense_rows],
        [float(r["round_trip_years"]) for r in dense_rows],
        color=ORANGE,
    )
    ax_time.set_ylabel("Round-trip time [years]", color=ORANGE)
    labelled: set[int] = set()
    for row in table_rows:
        if int(row["trips_in_life"]) in labelled:
            continue  # one label per trip count, at the lowest power that gives it
        labelled.add(int(row["trips_in_life"]))
        ax_trips.annotate(
            f"{row['trips_in_life']}",
            (float(row["power_kw"]), int(row["trips_in_life"])),
            textcoords="offset points",
            xytext=(4, 4),
            fontsize=8,
        )
    # Thrust is what the mission requirement is written in; it is proportional
    # to power at fixed efficiency and Isp, so show it as a second x axis.
    n_per_kw = float(dense_rows[0]["thrust_n"]) / float(dense_rows[0]["power_kw"])
    ax_thrust = ax_trips.secondary_xaxis("top", functions=(lambda kw: kw * n_per_kw, lambda n: n / n_per_kw))
    ax_thrust.set_xlabel("Equivalent thrust [N]")
    ax_trips.set_title(
        _title("Power vs throughput (dry mass grows with power, A-23)", note), fontsize=9, pad=34
    )
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _title(text: str, note: str) -> str:
    """Chart title, with the overridden parameters on a second line if any."""
    return f"{text}\nVariant: {note}" if note else text
