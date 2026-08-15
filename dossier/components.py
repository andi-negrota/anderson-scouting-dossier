"""Piezas del panel de instrumentos.

Todo lo que venga de una API pasa por `esc()` antes de entrar en el marcado.

Dos marcas propias de esta dirección, y ninguna es capricho:

  · El percentil se dibuja como un vúmetro de 20 segmentos separados por hueco de
    superficie, no como una barra continua redondeada. Cada segmento vale 5 puntos,
    así que la escala se puede contar con el dedo además de estimarse a ojo.
  · La dificultad del rival son cinco marcas de las que se encienden las que toca.
    La escala oficial va de 1 a 5: cinco marcas la representan sin traducirla a un
    color que habría que ir a buscar a una leyenda.
"""

from __future__ import annotations

from html import escape
from typing import Iterable, Sequence

from .theme import meter_color

METER_SEGMENTS = 20
DIFFICULTY_STEPS = 5


def esc(value: object) -> str:
    return escape(str(value), quote=True)


# ── Raíl de identificación ──

def rail(items: Sequence[str], live: str = "") -> str:
    cells = "".join(f"<span>{esc(item)}</span>" for item in items)
    live_html = f'<span class="rail-live">{esc(live)}</span>' if live else ""
    return f'<div class="rail">{cells}<span class="rail-sep"></span>{live_html}</div>'


# ── Cabecera de sección ──

def form_head(number: str, title: str, description: str = "", source: str = "") -> str:
    """El número de forma y la fuente no decoran: esta página se sostiene sobre la
    procedencia de cada dato, así que la fuente va en la cabecera de cada sección."""
    source_html = f"<span>{esc(source)}</span>" if source else ""
    desc_html = f'<p class="form-desc">{description}</p>' if description else ""
    return (
        '<div class="form-head">'
        '<div class="form-meta">'
        f'<span class="form-no">{esc(number)}</span>'
        '<span class="rule"></span>'
        f"{source_html}"
        "</div>"
        f'<h2 class="form-title">{esc(title)}</h2>'
        f"{desc_html}"
        "</div>"
    )


def halfway() -> str:
    """Divisor: la línea de medio campo con su círculo."""
    return '<div class="halfway"></div>'


# ── Lecturas de instrumento ──

def readout(value: str, label: str, sub: str = "", subject: bool = False) -> str:
    mark = " is-subject" if subject else ""
    sub_html = f'<p class="readout-sub">{esc(sub)}</p>' if sub else ""
    return (
        '<div class="readout">'
        f'<p class="readout-label">{esc(label)}</p>'
        f'<p class="readout-value{mark}">{esc(value)}</p>'
        f"{sub_html}"
        "</div>"
    )


def readouts(cards: Iterable[str]) -> str:
    return f'<div class="readouts">{"".join(cards)}</div>'


# ── Vúmetro de percentiles ──

def meter_head(metric: str, value: str, percentile: str, rank: str) -> str:
    return (
        '<div class="meter-row head">'
        f'<span class="meter-head">{esc(metric)}</span>'
        f'<span class="meter-head" style="text-align:right;">{esc(value)}</span>'
        f'<span class="meter-head">{esc(percentile)}</span>'
        f'<span class="meter-head" style="text-align:right;">{esc(rank)}</span>'
        "</div>"
    )


def meter_row(label: str, value: str, percentile: float, rank: int, sample: int) -> str:
    lit = round(percentile / (100 / METER_SEGMENTS))
    color = meter_color(percentile)
    segments = "".join(
        f'<span style="background:{color};"></span>' if index < lit else "<span></span>"
        for index in range(METER_SEGMENTS)
    )
    return (
        '<div class="meter-row">'
        f'<span class="meter-label">{esc(label)}</span>'
        f'<span class="meter-value">{esc(value)}</span>'
        f'<span class="meter" role="img" aria-label="percentil {percentile:.0f}">{segments}</span>'
        f'<span class="meter-rank">{rank}/{sample}</span>'
        "</div>"
    )


# ── Tablas ──

def table(rows_html: str) -> str:
    """Envuelve una tabla para que se desplace ella y no la página en pantallas
    estrechas."""
    return f'<div class="table-scroll">{rows_html}</div>'


def row(cells: Sequence[str], template: str, head: bool = False, subject: bool = False) -> str:
    css = "row head" if head else ("row subject" if subject else "row")
    first, *rest = cells
    body = f"<span>{esc(first)}</span>"
    body += "".join(f'<span class="num">{esc(cell)}</span>' for cell in rest)
    return f'<div class="{css}" style="grid-template-columns:{template};">{body}</div>'


# ── Calendario ──

def fixture(gameweek: str, opponent: str, venue: str, difficulty: int, difficulty_label: str) -> str:
    steps = "".join(
        f'<span class="{"on" if index < difficulty else ""}"></span>'
        for index in range(DIFFICULTY_STEPS)
    )
    return (
        '<div class="fixture">'
        f'<p class="fixture-gw">{esc(gameweek)}</p>'
        f'<p class="fixture-opp">{esc(opponent)}</p>'
        f'<p class="fixture-venue">{esc(venue)}</p>'
        f'<span class="diff" role="img" '
        f'aria-label="{esc(difficulty_label)} {difficulty}/{DIFFICULTY_STEPS}">{steps}</span>'
        "</div>"
    )


def fixtures(cards: Iterable[str]) -> str:
    return f'<div class="fixtures">{"".join(cards)}</div>'


# ── Bloques de texto ──

def notice(title: str, body: str) -> str:
    return (
        '<div class="notice">'
        f'<p class="notice-title">{esc(title)}</p>'
        f'<p class="notice-body">{body}</p>'
        "</div>"
    )


def verdict(body: str) -> str:
    return f'<div class="verdict"><p>{body}</p></div>'


def news_item(headline: str, description: str, published: str, link: str, read_label: str) -> str:
    safe_link = link if str(link).startswith(("https://", "http://")) else ""
    link_html = (
        f'<p style="margin-top:0.5rem;"><a class="news-link" href="{esc(safe_link)}" '
        f'target="_blank" rel="noopener noreferrer">{esc(read_label)} →</a></p>'
        if safe_link
        else ""
    )
    desc_html = f'<p class="news-desc">{esc(description)}</p>' if description else ""
    return (
        '<div class="news">'
        f'<p class="news-date">{esc(published)}</p>'
        f'<p class="news-head">{esc(headline)}</p>'
        f"{desc_html}{link_html}"
        "</div>"
    )


def method(source: str, body: str) -> str:
    return f'<div class="method"><p class="method-src">{esc(source)}</p><p>{body}</p></div>'


def footer(left: str, right: str) -> str:
    return f'<div class="footer"><span>{esc(left)}</span><span>{esc(right)}</span></div>'
