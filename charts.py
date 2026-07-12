import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ── Palette — matches theme.py's CSS variables ──────────────────────────────
BG      = "#0a0a0f"
PANEL   = "#12121a"
GRID    = "#1e1e2e"
TEXT    = "#e8e8f0"
MUTED   = "#5a5a7a"
ACCENT  = "#00e5a0"
ACCENT2 = "#00ffb3"
AMBER   = "#ffb020"
RED     = "#ff4d6d"

FONT = dict(family="JetBrains Mono, monospace", color=TEXT, size=11)
TITLE_FONT = dict(family="JetBrains Mono, monospace", color=MUTED, size=11)


def _base_layout(fig, height=None, title=None):
    # Plotly's Python API doesn't accept title=None cleanly for this compound
    # property — it still creates an empty title object that renders as a
    # literal "undefined" string in the browser. Omit the key entirely
    # instead of passing None when there's no title.
    layout_kwargs = dict(
        paper_bgcolor=BG,
        plot_bgcolor=PANEL,
        font=FONT,
        margin=dict(l=10, r=10, t=36 if title else 10, b=10),
        height=height,
    )
    if title:
        layout_kwargs["title"] = dict(text=title, font=TITLE_FONT, x=0.01)
    fig.update_layout(**layout_kwargs)
    return fig


def price_heatmap(numeric_df, title=None):
    """numeric_df: rows=outcome labels, columns=bookmaker labels, values=price
    (float, NaN for missing). Returns a Plotly heatmap with each price
    annotated in its cell. Color is normalized PER ROW (min-max within that
    outcome only) rather than across the whole matrix — different markets
    have wildly different price scales (e.g. Over 4.5 @ 6.00 vs BTTS @ 1.72),
    so a global scale would drown out the real signal: which bookmaker has
    the best price for THIS specific outcome. The annotated text always
    shows the true raw price regardless of the normalized color."""
    if numeric_df.empty or numeric_df.shape[1] == 0:
        return None
    z = numeric_df.to_numpy(dtype=float)
    text = [[f"{v:.2f}" if pd.notna(v) else "" for v in row] for row in z]

    row_min = np.nanmin(z, axis=1)
    row_max = np.nanmax(z, axis=1)
    row_span = row_max - row_min
    tied = (row_span == 0)[:, None]
    z_norm = (z - row_min[:, None]) / np.where(row_span == 0, 1, row_span)[:, None]
    # A tied row (every bookmaker offers the same price) has no worst price
    # to contrast against — treat every valid cell as "best", not "worst".
    z_norm = np.where(tied & ~np.isnan(z), 1.0, z_norm)

    fig = go.Figure(data=go.Heatmap(
        z=z_norm,
        x=list(numeric_df.columns),
        y=list(numeric_df.index),
        colorscale=[[0.0, GRID], [0.5, "#0f3d2e"], [1.0, ACCENT2]],
        zmin=0, zmax=1,
        text=text,
        texttemplate="%{text}",
        textfont=dict(family="JetBrains Mono, monospace", size=10, color=TEXT),
        hovertemplate="%{y}<br>%{x}: %{text}<extra></extra>",
        showscale=False,
        xgap=3, ygap=3,
    ))
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=10))
    fig.update_xaxes(tickfont=dict(size=10), side="top")
    return _base_layout(fig, height=max(160, 34 * len(numeric_df.index) + 60), title=title)


def edge_bar_chart(labels, values, title=None, color=ACCENT, suffix="%"):
    """Horizontal bar chart — e.g. top edges vs. market average, or
    arbitrage opportunities ranked by margin. labels/values are parallel
    lists; values are plotted as-is (caller controls ordering)."""
    if not labels:
        return None
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker_color=color,
        text=[f"+{v:.1f}{suffix}" for v in values],
        textposition="outside",
        textfont=dict(family="JetBrains Mono, monospace", color=TEXT, size=10),
        cliponaxis=False,
    ))
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=10))
    fig.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False, tickfont=dict(size=10))
    return _base_layout(fig, height=max(180, 34 * len(labels) + 60), title=title)


def coverage_heatmap(coverage_df, title=None):
    """coverage_df: rows=bookmaker labels, columns=coverage categories
    (e.g. 'Match Odds', 'Player Props'), values=odds count (int, 0 if none).
    Returns a Plotly heatmap — darker/empty cells show gaps in bookmaker
    coverage at a glance."""
    if coverage_df.empty:
        return None
    z = coverage_df.to_numpy(dtype=float)
    text = [[str(int(v)) if v else "—" for v in row] for row in z]

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=list(coverage_df.columns),
        y=list(coverage_df.index),
        colorscale=[[0.0, GRID], [0.08, GRID], [1.0, ACCENT]],
        text=text,
        texttemplate="%{text}",
        textfont=dict(family="JetBrains Mono, monospace", size=10, color=TEXT),
        hovertemplate="%{y}<br>%{x}: %{z}<extra></extra>",
        showscale=False,
        xgap=3, ygap=3,
    ))
    fig.update_yaxes(tickfont=dict(size=10))
    fig.update_xaxes(tickfont=dict(size=10), side="top")
    return _base_layout(fig, height=max(160, 28 * len(coverage_df.index) + 60), title=title)
