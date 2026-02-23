#!/usr/bin/env python3
"""
Render static interval diagrams for intersection docs using Plotly.

All figures are written as SVG for crisp rendering.
"""

from collections import Counter
from pathlib import Path
import warnings

import plotly.graph_objects as go


AA = [(2, 23)]
BB = [(8, 12), (14, 15), (20, 30)]

WHOLE = [(2, 23)]
WHOLE_X3 = [(2, 23), (2, 23), (2, 23)]
WHOLE_WITH_B = [(2, 23), (8, 12), (14, 15), (20, 30)]
PIECE = [(8, 12), (14, 15), (20, 23)]
INVERSE = [(2, 8), (12, 14), (15, 20)]
PIECE_REQ3 = [(8, 12), (20, 23)]


PALETTE = {
    "aa": "#66c2a5",
    "bb": "#8da0cb",
    "out": "#fc8d62",
    "out2": "#e78ac3",
}


def draw_track(fig: go.Figure, y_center: float, intervals, color: str, edgecolor="#1f2937") -> None:
    counts = Counter(intervals)
    for i, ((start, end), count) in enumerate(sorted(counts.items(), key=lambda x: (x[0][0], x[0][1]))):
        fig.add_shape(
            type="rect",
            x0=start,
            x1=end,
            y0=y_center - 0.22,
            y1=y_center + 0.22,
            fillcolor=color,
            line={"color": edgecolor, "width": 1},
            opacity=0.92,
        )
        label = f"{start}-{end}" + (f" x{count}" if count > 1 else "")
        text_y = y_center + (0.07 if i % 2 else -0.07)
        fig.add_annotation(
            x=(start + end) / 2,
            y=text_y,
            text=label,
            showarrow=False,
            font={"size": 12, "color": "#111827"},
            xanchor="center",
            yanchor="middle",
        )


def render(tracks, out_path: Path, title: str) -> None:
    all_coords = [coord for _, intervals, _ in tracks for interval in intervals for coord in interval]
    xmin = min(all_coords) - 1
    xmax = max(all_coords) + 1

    y_positions = list(range(len(tracks), 0, -1))
    fig = go.Figure()

    for y, (label, intervals, color) in zip(y_positions, tracks):
        draw_track(fig, y, intervals, color)

    fig.update_layout(
        title={"text": title, "x": 0.01, "xanchor": "left", "font": {"size": 18}},
        margin={"l": 96, "r": 24, "t": 44, "b": 52},
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8fafc",
        font={"family": "Arial, sans-serif", "size": 13, "color": "#111827"},
        xaxis={
            "title": {"text": "Genomic coordinate", "font": {"size": 14}},
            "range": [xmin, xmax],
            "showgrid": True,
            "gridcolor": "#d7dde4",
            "gridwidth": 1,
            "zeroline": False,
        },
        yaxis={
            "range": [0.5, len(tracks) + 0.5],
            "tickmode": "array",
            "tickvals": y_positions,
            "ticktext": [label for label, _, _ in tracks],
            "tickfont": {"size": 13},
            "showgrid": False,
            "zeroline": False,
        },
        showlegend=False,
    )
    fig.update_xaxes(showline=True, linecolor="#c8d1dc", mirror=False, ticks="outside")
    fig.update_yaxes(showline=True, linecolor="#c8d1dc", mirror=False, ticks="")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    height = max(170, int(62 * len(tracks) + 28))
    fig.write_image(str(out_path), format="svg", width=1200, height=height, scale=1)


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    out_dir = root / "docs" / "images" / "intersection"

    def tr(label, intervals, role="out"):
        return (label, intervals, PALETTE[role])

    figures = [
        ("output1", "whole-wide A (one row)", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output1", WHOLE)]),
        ("output1b", "whole A (one per overlap)", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output1b", WHOLE_X3)]),
        ("output1c", "whole A + whole B", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output1c", WHOLE_WITH_B)]),
        ("output2", "piece A + whole B", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output2", PIECE)]),
        ("output3", "piece A + piece B", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output3", PIECE)]),
        ("inverse", "inverse (A minus overlap)", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("inverse", INVERSE)]),
        (
            "subtract-equivalence",
            "bedtools subtract equivalence",
            [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("bedtools subtract", INVERSE), tr("bedder inverse", INVERSE, "out2")],
        ),
        ("output5", "piece output (default requirement)", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output5", PIECE)]),
        ("output6", "whole-wide with 3bp requirement", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output6", WHOLE)]),
        ("output7", "piece with B requirement + piece mode", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output7", PIECE_REQ3)]),
        ("output8", "piece with B requirement (default mode)", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output8", PIECE)]),
        ("output9", "python n_overlapping", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output9", WHOLE)]),
        ("output10", "python total_b_overlap (piece)", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output10", WHOLE)]),
        ("output11", "python total_b_overlap (whole-wide)", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output11", WHOLE)]),
        ("output12", "python total_b_overlap by piece", [tr("aa", AA, "aa"), tr("bb", BB, "bb"), tr("output12", PIECE)]),
    ]

    for stem, title, tracks in figures:
        render(tracks=tracks, out_path=out_dir / f"{stem}.svg", title=title)


if __name__ == "__main__":
    warnings.simplefilter("ignore", DeprecationWarning)
    main()
