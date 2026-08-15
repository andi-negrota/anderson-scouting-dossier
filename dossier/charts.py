"""Figuras de Plotly.

Tres decisiones que conviene dejar escritas:

1. La pieza 3D dibuja marcas de campo en el suelo, pero **no son decoración**. El
   "círculo central" es la región intercuartílica de los 126 centrocampistas y la
   "línea de medio campo" son sus medianas. Una elipse dibujada en un espacio de
   datos se lee como información, así que es información.

2. El 3D se lee mal para un valor exacto. Por eso la comparación fina vive en los
   vúmetros y en la tabla de percentiles, y la nube aporta lo que la tabla no puede:
   dónde cae el sujeto dentro de la masa, de un vistazo.

3. La trayectoria son dos paneles apilados y no un gráfico de doble eje. Alinear dos
   escalas distintas en un mismo dibujo inventa una correlación que no está en los
   datos; es el error más frecuente en visualización.

La nube va al 38% de opacidad por contraste medido, no por gusto: a plena opacidad
el sujeto ámbar y la nube quedan a 1,46:1 de luminancia.
"""

from __future__ import annotations

import math
from statistics import median
from typing import Sequence

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .theme import AMBER, CHALK, CHALK_DIM, CLOUD_ALPHA, PITCH

TRANSPARENT = "rgba(0,0,0,0)"
GRID = "rgba(233,239,230,0.10)"
MONO = "IBM Plex Mono, monospace"
COND = "IBM Plex Sans Condensed, sans-serif"

CLOUD_RGBA = f"rgba(143,163,148,{CLOUD_ALPHA})"


def _quartiles(values: Sequence[float]) -> tuple[float, float, float]:
    """Mediana y cuartiles sin depender de numpy."""
    ordered = sorted(values)
    if not ordered:
        return 0.0, 0.0, 0.0
    mid = median(ordered)
    half = len(ordered) // 2
    lower = median(ordered[:half]) if half else mid
    upper = median(ordered[-half:]) if half else mid
    return lower, mid, upper


def _ellipse(cx: float, cy: float, rx: float, ry: float, points: int = 96):
    step = 2 * math.pi / points
    xs = [cx + rx * math.cos(i * step) for i in range(points + 1)]
    ys = [cy + ry * math.sin(i * step) for i in range(points + 1)]
    return xs, ys


def peer_cloud_3d(
    cloud: Sequence[dict],
    subject_id: int,
    subject_label: str,
    axis_labels: tuple[str, str, str],
    peers_label: str,
    middle_label: str,
) -> go.Figure:
    """Los centrocampistas de la Premier en tres ejes, con el sujeto destacado.

    Codificación del sujeto por cuatro canales a la vez (tono, tamaño, etiqueta
    directa y línea de caída al suelo), porque sólo con el tono la separación de
    luminancia contra la nube sería insuficiente.
    """
    peers = [p for p in cloud if p["id"] != subject_id]
    subject = next((p for p in cloud if p["id"] == subject_id), None)

    xs = [p["x"] for p in cloud]
    ys = [p["y"] for p in cloud]
    x_lo, x_mid, x_hi = _quartiles(xs)
    y_lo, y_mid, y_hi = _quartiles(ys)

    figure = go.Figure()

    # ── Suelo: medianas y región intercuartílica ──
    figure.add_trace(
        go.Scatter3d(
            x=[min(xs), max(xs)], y=[y_mid, y_mid], z=[0, 0],
            mode="lines", line=dict(color=GRID, width=2),
            hoverinfo="skip", showlegend=False,
        )
    )
    figure.add_trace(
        go.Scatter3d(
            x=[x_mid, x_mid], y=[min(ys), max(ys)], z=[0, 0],
            mode="lines", line=dict(color=GRID, width=2),
            hoverinfo="skip", showlegend=False,
        )
    )
    ellipse_x, ellipse_y = _ellipse(x_mid, y_mid, (x_hi - x_lo) / 2, (y_hi - y_lo) / 2)
    figure.add_trace(
        go.Scatter3d(
            x=ellipse_x, y=ellipse_y, z=[0] * len(ellipse_x),
            mode="lines", line=dict(color="rgba(233,239,230,0.30)", width=2),
            name=middle_label, hoverinfo="skip",
        )
    )

    # ── La masa ──
    figure.add_trace(
        go.Scatter3d(
            x=[p["x"] for p in peers],
            y=[p["y"] for p in peers],
            z=[p["z"] for p in peers],
            mode="markers",
            marker=dict(size=5, color=CLOUD_RGBA, line=dict(width=0)),
            name=peers_label,
            customdata=[[p["name"], p["team"], p["minutes"]] for p in peers],
            hovertemplate=(
                "<b>%{customdata[0]}</b> · %{customdata[1]}<br>"
                f"{axis_labels[0]}: %{{x:.2f}}<br>"
                f"{axis_labels[1]}: %{{y:.2f}}<br>"
                f"{axis_labels[2]}: %{{z:.2f}}<extra></extra>"
            ),
        )
    )

    # ── El sujeto ──
    if subject:
        figure.add_trace(
            go.Scatter3d(
                x=[subject["x"], subject["x"]],
                y=[subject["y"], subject["y"]],
                z=[0, subject["z"]],
                mode="lines", line=dict(color="rgba(255,176,0,0.55)", width=3),
                hoverinfo="skip", showlegend=False,
            )
        )
        figure.add_trace(
            go.Scatter3d(
                x=[subject["x"]], y=[subject["y"]], z=[subject["z"]],
                mode="markers+text",
                marker=dict(size=11, color=AMBER, line=dict(width=2, color=PITCH)),
                text=[subject_label], textposition="top center",
                textfont=dict(family=MONO, size=13, color=AMBER),
                name=subject_label,
                hovertemplate=(
                    f"<b>{subject_label}</b><br>"
                    f"{axis_labels[0]}: %{{x:.2f}}<br>"
                    f"{axis_labels[1]}: %{{y:.2f}}<br>"
                    f"{axis_labels[2]}: %{{z:.2f}}<extra></extra>"
                ),
            )
        )

    axis_style = dict(
        backgroundcolor=TRANSPARENT,
        gridcolor=GRID,
        zerolinecolor=GRID,
        showbackground=False,
        color=CHALK_DIM,
        tickfont=dict(family=MONO, size=10, color=CHALK_DIM),
    )

    figure.update_layout(
        paper_bgcolor=TRANSPARENT,
        plot_bgcolor=TRANSPARENT,
        height=560,
        margin=dict(l=0, r=0, t=10, b=0),
        scene=dict(
            xaxis=dict(title=dict(text=axis_labels[0], font=dict(family=MONO, size=11, color=CHALK_DIM)), **axis_style),
            yaxis=dict(title=dict(text=axis_labels[1], font=dict(family=MONO, size=11, color=CHALK_DIM)), **axis_style),
            zaxis=dict(title=dict(text=axis_labels[2], font=dict(family=MONO, size=11, color=CHALK_DIM)), **axis_style),
            aspectmode="cube",
            camera=dict(eye=dict(x=1.65, y=1.5, z=0.85)),
        ),
        legend=dict(
            orientation="h", yanchor="top", y=0.02, xanchor="center", x=0.5,
            font=dict(family=MONO, size=11, color=CHALK_DIM),
            bgcolor=TRANSPARENT, itemsizing="constant",
        ),
        hoverlabel=dict(
            bgcolor="#0D1712", bordercolor=CHALK_DIM,
            font=dict(family=MONO, size=12, color=CHALK),
        ),
    )
    return figure


def trajectory(
    seasons: Sequence[str],
    minutes: Sequence[int],
    points: Sequence[int],
    minutes_label: str,
    points_label: str,
) -> go.Figure:
    """Dos paneles apilados con eje x común. Una escala por panel, nunca dos en uno."""
    figure = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.09,
        subplot_titles=(minutes_label.upper(), points_label.upper()),
    )
    figure.add_trace(
        go.Bar(
            x=list(seasons), y=list(minutes),
            marker_color=CLOUD_RGBA, marker_line=dict(width=0),
            hovertemplate="%{x}<br>%{y:,} " + minutes_label.lower() + "<extra></extra>",
            showlegend=False,
        ),
        row=1, col=1,
    )
    # Sólo la última temporada va en ámbar: es la que motiva el fichaje.
    point_colors = [CLOUD_RGBA] * (len(points) - 1) + [AMBER] if points else []
    figure.add_trace(
        go.Bar(
            x=list(seasons), y=list(points),
            marker_color=point_colors, marker_line=dict(width=0),
            hovertemplate="%{x}<br>%{y} " + points_label.lower() + "<extra></extra>",
            showlegend=False,
        ),
        row=2, col=1,
    )

    figure.update_layout(
        paper_bgcolor=TRANSPARENT, plot_bgcolor=TRANSPARENT,
        height=430, bargap=0.45,
        margin=dict(l=10, r=10, t=30, b=30),
        font=dict(family=MONO, size=11, color=CHALK_DIM),
        hoverlabel=dict(bgcolor="#0D1712", bordercolor=CHALK_DIM,
                        font=dict(family=MONO, size=12, color=CHALK)),
    )
    figure.update_xaxes(showgrid=False, linecolor=GRID,
                        tickfont=dict(family=MONO, size=11, color=CHALK_DIM))
    figure.update_yaxes(gridcolor=GRID, linecolor=TRANSPARENT, zeroline=False,
                        tickfont=dict(family=MONO, size=10, color=CHALK_DIM))
    for annotation in figure.layout.annotations:
        annotation.font = dict(family=MONO, size=11, color=CHALK_DIM)
        annotation.x = 0
        annotation.xanchor = "left"
    return figure


def price_bars(
    names: Sequence[str],
    prices: Sequence[float],
    highlight: str,
    axis_label: str,
) -> go.Figure:
    """Una serie, un color, y el sujeto destacado. Nunca una rampa por valor."""
    colors = [AMBER if name == highlight else CLOUD_RGBA for name in names]
    figure = go.Figure(
        go.Bar(
            x=list(prices), y=list(names), orientation="h",
            marker_color=colors, marker_line=dict(width=0),
            text=[f"{price:.1f}" for price in prices],
            textposition="outside",
            textfont=dict(family=MONO, size=12, color=CHALK),
            hovertemplate="%{y}<br>%{x:.1f}<extra></extra>",
            showlegend=False,
        )
    )
    figure.update_layout(
        paper_bgcolor=TRANSPARENT, plot_bgcolor=TRANSPARENT,
        height=360, bargap=0.42,
        margin=dict(l=10, r=44, t=10, b=44),
        font=dict(family=MONO, size=11, color=CHALK_DIM),
        xaxis=dict(
            title=dict(text=axis_label, font=dict(family=MONO, size=11, color=CHALK_DIM)),
            gridcolor=GRID, linecolor=TRANSPARENT, zeroline=False,
            range=[0, max(prices) * 1.15 if prices else 1],
            tickfont=dict(family=MONO, size=10, color=CHALK_DIM),
        ),
        yaxis=dict(
            autorange="reversed", showgrid=False, linecolor=GRID,
            tickfont=dict(family=MONO, size=11, color=CHALK_DIM),
        ),
        hoverlabel=dict(bgcolor="#0D1712", bordercolor=CHALK_DIM,
                        font=dict(family=MONO, size=12, color=CHALK)),
    )
    return figure
