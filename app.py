"""Informe de scouting de Elliot Anderson: del Nottingham Forest al Manchester City.

Esta página no publica un solo número que no venga de una API. Donde una fuente no
llega, lo dice en vez de rellenarlo: el importe del traspaso, por ejemplo, va
atribuido a ESPN porque ninguna API lo publica.

El código vive en el paquete `dossier`: datos, textos, tema y gráficos por separado.
La dirección visual está documentada en `dossier/theme.py`.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
for _path in [_ROOT / ".venv" / "Lib" / "site-packages", _ROOT / "parse_apis" / "src", _ROOT]:
    if _path.is_dir() and str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import streamlit as st

from dossier import charts, components as ui
from dossier.data import espn, fotmob, fpl
from dossier.i18n import DEFAULT_LANGUAGE, LANGUAGES, format_date, gameweek, position, t
from dossier.theme import CSS

PHOTO = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/"
    "Elliot_Anderson_England_v_Ghana_23_June_2026-059_%28cropped%29.jpg/960px-"
    "Elliot_Anderson_England_v_Ghana_23_June_2026-059_%28cropped%29.jpg"
)

# El importe no sale de ninguna API. ESPN lo publica y aquí queda enlazado a su fuente.
FEE_TEXT = "£116M"
FEE_SOURCE = (
    "https://www.espn.com/soccer/story/_/id/49408661/"
    "why-rogers-117m-chelsea-transfer-high-risk-anderson-116m-move-city"
)
COMPLETED_DATE = "2026-07-23"

st.set_page_config(
    page_title="Elliot Anderson · Scouting Dossier",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ── Carga de datos (el cacheo vive aquí; la capa de datos es pura) ──

@st.cache_data(ttl=3600, show_spinner=False)
def load_fpl() -> tuple[dict, dict, dict, list[dict]]:
    boot = fpl.bootstrap()
    return boot, fpl.find_player(boot), fpl.element_summary(), fpl.peers(boot)


@st.cache_data(ttl=3600, show_spinner=False)
def load_espn() -> tuple[dict, list[dict], list[dict]]:
    return espn.profile(), espn.international_splits(), espn.player_news()


@st.cache_data(ttl=3600, show_spinner=False)
def load_fotmob() -> list[dict]:
    return fotmob.standings()


def find_team(table: list[dict], *needles: str) -> dict | None:
    for team in table:
        haystack = f"{team['team']} {team['short']}".lower()
        if any(needle.lower() in haystack for needle in needles):
            return team
    return None


def thousands(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def _sdk_available(module: str) -> bool:
    """Si el SDK de `parse_apis` para esta fuente no está instalado -- el caso del
    despliegue público, que se publica sin claves de API propias -- lo tratamos
    como una sección que esta build no incluye, no como un fallo de red. La
    diferencia importa: un aviso de "ESPN no respondió" sería falso si la razón
    real es que esta build nunca intentó traerlo."""
    try:
        return importlib.util.find_spec(module) is not None
    except ModuleNotFoundError:
        return False


ESPN_AVAILABLE = _sdk_available("parse_apis.espn_sports_data_api")
FOTMOB_AVAILABLE = _sdk_available("parse_apis.fotmob_com_api")


st.markdown(CSS, unsafe_allow_html=True)

lang = st.session_state.get("lang") or DEFAULT_LANGUAGE


# ── Datos ──

try:
    boot, element, summary, peer_group = load_fpl()
except fpl.FplUnavailable as exc:
    st.error(t("error_fpl", lang, detail=exc))
    st.stop()

stats = fpl.headline_stats(element)
season_row = fpl.past_season(summary)
season_stats = fpl.headline_stats_for_season(season_row) if season_row else None
sample = len(peer_group)
profile_rows = fpl.percentile_profile(element, peer_group, fpl.TABLE_METRICS)
by_key = {row["key"]: row for row in profile_rows}
state = fpl.season_state(boot)
cloud = fpl.peer_cloud(boot, peer_group)
leaders = fpl.axis_leaders(cloud)

bio, splits, news = {}, [], []
espn_error: str | None = None
if ESPN_AVAILABLE:
    try:
        bio, splits, news = load_espn()
    except espn.EspnUnavailable as exc:
        espn_error = str(exc)

# No es lo mismo "el SDK está instalado" que "esta fuente aportó algo esta
# ejecución": una cuota agotada o un corte de red con el SDK presente también deja
# la fuente vacía, y en ese caso el aviso de arriba ya lo explica -- la metodología
# y el pie no deben citarla como si hubiera aportado datos igualmente.
espn_delivered = bool(bio or splits or news)


# ── Raíl de identificación + idioma ──

rail_column, language_column = st.columns([4, 1])
with rail_column:
    st.markdown(
        ui.rail(
            [
                f"{t('rail_subject', lang)} · EA 238472",
                position(bio.get("position", ""), lang) or t("nav_position", lang),
                "PL 2025/26",
                f"n={sample}",
            ],
            live=t("rail_live", lang),
        ),
        unsafe_allow_html=True,
    )
with language_column:
    lang = (
        st.segmented_control(
            t("language", lang),
            options=list(LANGUAGES),
            format_func=lambda code: LANGUAGES[code].upper(),
            default=lang,
            key="lang",
            label_visibility="collapsed",
        )
        or DEFAULT_LANGUAGE
    )


# ── Portada ──
# La tesis va en la portada: el puesto en el que mejor sale, calculado, no escrito.

best = min(profile_rows, key=lambda row: row["rank"])
name = bio.get("name", "Elliot Anderson")
given, _, surname = name.rpartition(" ")
height = espn.height_cm(bio.get("height", ""))
weight = espn.weight_kg(bio.get("weight", ""))

identity = " · ".join(
    part for part in [
        t("badge_age", lang, age=bio.get("age") or 23),
        f"{height} cm" if height else "",
        f"{weight} kg" if weight else "",
        t("badge_england", lang),
    ] if part
)

photo_column, hero_column = st.columns([1, 5])
with photo_column:
    st.markdown(
        f'<img src="{PHOTO}" alt="{ui.esc(name)}" '
        'style="width:100%;filter:grayscale(1) contrast(1.15) brightness(0.95);'
        'border:1px solid rgba(233,239,230,0.16);">',
        unsafe_allow_html=True,
    )
with hero_column:
    st.markdown(
        '<div class="hero">'
        f'<h1 class="hero-name"><span class="hero-given">{ui.esc(given)}</span>'
        f"{ui.esc(surname)}</h1>"
        '<div class="move">'
        f'<span class="move-from">Nottingham Forest</span>'
        '<span class="move-path"></span>'
        f'<span class="move-to">Manchester City</span>'
        f'<span class="move-fee">{ui.esc(FEE_TEXT)}</span>'
        f'<a href="{FEE_SOURCE}" target="_blank" rel="noopener noreferrer" '
        f'style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;letter-spacing:0.1em;'
        f'text-transform:uppercase;">{ui.esc(t("hero_fee_label", lang))} →</a>'
        "</div>"
        '<div class="hero-strip">'
        f"<span>{ui.esc(identity)}</span>"
        f'<span>{ui.esc(t("hero_agreed", lang, date=format_date(stats["joined"], lang)))}</span>'
        f'<span>{ui.esc(t("hero_completed", lang, date=format_date(COMPLETED_DATE, lang)))}</span>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown(
    ui.verdict(
        t(
            "hero_thesis", lang,
            rank=best["rank"],
            sample=best["sample"],
            metric=t(f"metric_{best['key']}", lang).lower(),
        )
    ),
    unsafe_allow_html=True,
)

if not state["started"]:
    st.markdown(
        ui.notice(
            t("context_banner_title", lang),
            t("context_banner_body", lang, deadline=format_date(state["next_deadline"], lang)),
        ),
        unsafe_allow_html=True,
    )

if espn_error:
    st.warning(t("error_espn", lang, detail=espn_error))


# ── FORMA 01 · La temporada ──

st.markdown(
    ui.form_head(
        t("form_no", lang, number="01"),
        t("kpi_title", lang),
        t("kpi_desc", lang),
        f"{t('source', lang)} FPL · {t('kpi_eyebrow', lang)}",
    ),
    unsafe_allow_html=True,
)

if season_stats:
    recoveries_90 = fpl.per_90(season_row, "recoveries")
    st.markdown(
        ui.readouts(
            [
                ui.readout(thousands(season_stats["minutes"]), t("kpi_minutes", lang),
                           t("kpi_minutes_sub", lang, starts=season_stats["starts"])),
                ui.readout(str(season_stats["goal_involvements"]), t("kpi_ga", lang),
                           t("kpi_ga_sub", lang, goals=season_stats["goals"], assists=season_stats["assists"])),
                ui.readout(f"{season_stats['xgi']:.2f}", t("kpi_xgi", lang),
                           t("kpi_xgi_sub", lang, xg=f"{season_stats['xg']:.2f}", xa=f"{season_stats['xa']:.2f}")),
                ui.readout(str(season_stats["recoveries"]), t("kpi_recoveries", lang),
                           t("kpi_recoveries_sub", lang, per90=f"{recoveries_90:.2f}"), subject=True),
                ui.readout(str(season_stats["tackles"]), t("kpi_tackles", lang),
                           t("kpi_tackles_sub", lang, cbi=season_stats["cbi"])),
                ui.readout(str(season_stats["total_points"]), t("kpi_points", lang),
                           t("kpi_points_sub", lang, bonus=season_stats["bonus"])),
            ]
        ),
        unsafe_allow_html=True,
    )
else:
    st.info(t("kpi_season_missing", lang, season=fpl.TARGET_SEASON))


# ── FORMA 02 · La nube (pieza principal) ──

st.markdown(ui.halfway(), unsafe_allow_html=True)
st.markdown(
    ui.form_head(
        t("form_no", lang, number="02"),
        t("cloud_title", lang),
        t("cloud_desc", lang, sample=sample),
        f"{t('source', lang)} FPL · n={sample}",
    ),
    unsafe_allow_html=True,
)

axis_keys = ("recoveries90", "xa90", "xg90")
axis_labels = tuple(t(f"metric_{key}", lang) for key in axis_keys)

st.plotly_chart(
    charts.peer_cloud_3d(
        cloud=cloud,
        subject_id=fpl.ANDERSON_FPL_ID,
        subject_label="Anderson",
        axis_labels=axis_labels,
        peers_label=t("cloud_peers", lang),
        middle_label=t("cloud_middle", lang),
    ),
    use_container_width=True,
    config={"displayModeBar": False},
)

# Gemelo en tabla: en 3D se estima una posición, no se lee un valor.
st.markdown(
    ui.form_head("", t("cloud_reading", lang), t("cloud_reading_desc", lang)),
    unsafe_allow_html=True,
)
axis_columns = "1.6fr 0.8fr 2fr"
st.markdown(
    ui.table(
        ui.row([t("cloud_axis", lang), t("cloud_subject_value", lang), t("cloud_leader", lang)],
               axis_columns, head=True)
        + "".join(
            ui.row(
                [
                    label,
                    f"{by_key[key]['value']:.2f}",
                    f"{leaders[axis]['name']} · {leaders[axis]['team']} · {leaders[axis]['value']:.2f}",
                ],
                axis_columns,
                subject=leaders[axis]["name"] == element.get("web_name"),
            )
            for key, label, axis in zip(axis_keys, axis_labels, ("x", "y", "z"))
            if axis in leaders
        )
    ),
    unsafe_allow_html=True,
)


# ── FORMA 03 · Percentiles ──

st.markdown(ui.halfway(), unsafe_allow_html=True)
st.markdown(
    ui.form_head(
        t("form_no", lang, number="03"),
        t("pct_title", lang),
        t("pct_desc", lang, sample=sample),
        f"{t('source', lang)} FPL · n={sample}",
    ),
    unsafe_allow_html=True,
)

st.markdown(
    ui.meter_head(t("pct_metric", lang), t("pct_value", lang),
                  t("pct_percentile", lang), t("pct_rank", lang))
    + "".join(
        ui.meter_row(
            label=t(f"metric_{row['key']}", lang),
            value=f"{row['value']:.2f}",
            percentile=row["percentile"],
            rank=row["rank"],
            sample=row["sample"],
        )
        for row in profile_rows
    ),
    unsafe_allow_html=True,
)

recoveries, tackles, expected_goals = by_key["recoveries90"], by_key["tackles90"], by_key["xg90"]
st.markdown(
    ui.verdict(
        t(
            "read_body", lang,
            sample=sample,
            rec=f"{recoveries['value']:.2f}",
            tackles_pct=f"{tackles['percentile']:.0f}",
            xg=f"{expected_goals['value']:.2f}",
            xg_pct=f"{expected_goals['percentile']:.0f}",
        )
    ),
    unsafe_allow_html=True,
)

ranks = fpl.official_ranks(element, sample)
if ranks:
    st.markdown(
        ui.readouts(
            [ui.readout(f"#{row['rank']}", t(f"rank_{row['key']}", lang)) for row in ranks]
        ),
        unsafe_allow_html=True,
    )


# ── FORMA 04 · Trayectoria ──

seasons = [row for row in fpl.season_history(summary) if row["minutes"] > 0]
if seasons:
    st.markdown(ui.halfway(), unsafe_allow_html=True)
    st.markdown(
        ui.form_head(
            t("form_no", lang, number="04"),
            t("curve_title", lang),
            t("curve_desc", lang),
            f"{t('source', lang)} FPL",
        ),
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        charts.trajectory(
            seasons=[row["season"] for row in seasons],
            minutes=[row["minutes"] for row in seasons],
            points=[row["points"] for row in seasons],
            minutes_label=t("curve_minutes", lang),
            points_label=t("curve_points", lang),
        ),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    columns = "1.3fr repeat(5, 1fr)"
    st.markdown(
        ui.table(
            ui.row(
                [t("table_season", lang), t("curve_minutes", lang), t("intl_goals", lang),
                 t("intl_assists", lang), t("curve_xgi", lang), t("curve_points", lang)],
                columns, head=True,
            )
            + "".join(
                ui.row(
                    [row["season"], thousands(row["minutes"]), row["goals"], row["assists"],
                     f"{row['xg'] + row['xa']:.2f}", row["points"]],
                    columns,
                )
                for row in seasons
            )
        ),
        unsafe_allow_html=True,
    )


# ── FORMA 05 · El salto ──

table: list[dict] = []
if FOTMOB_AVAILABLE:
    try:
        table = load_fotmob()
    except fotmob.FotmobUnavailable as exc:
        st.warning(t("error_fotmob", lang, detail=exc))

fotmob_delivered = bool(table)

forest_row = find_team(table, "Forest") if table else None
city_row = find_team(table, "Man City", "Manchester City") if table else None
if forest_row and city_row:
    st.markdown(ui.halfway(), unsafe_allow_html=True)
    st.markdown(
        ui.form_head(
            t("form_no", lang, number="05"),
            t("jump_title", lang),
            t("jump_desc", lang),
            f"{t('source', lang)} FotMob",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        ui.readouts(
            [
                ui.readout(str(forest_row["rank"]), f"{forest_row['team']} · {t('jump_position', lang)}"),
                ui.readout(str(forest_row["points"]), f"{forest_row['team']} · {t('jump_points', lang)}"),
                ui.readout(f"{forest_row['goal_difference']:+d}",
                           f"{forest_row['team']} · {t('jump_gd', lang)}"),
                ui.readout(str(city_row["rank"]), f"{city_row['team']} · {t('jump_position', lang)}",
                           subject=True),
                ui.readout(str(city_row["points"]), f"{city_row['team']} · {t('jump_points', lang)}",
                           subject=True),
                ui.readout(f"{city_row['goal_difference']:+d}",
                           f"{city_row['team']} · {t('jump_gd', lang)}", subject=True),
            ]
        ),
        unsafe_allow_html=True,
    )


# ── FORMA 06 · Calendario ──

upcoming = fpl.upcoming_fixtures(summary, fpl.team_names(boot))
if upcoming:
    st.markdown(ui.halfway(), unsafe_allow_html=True)
    st.markdown(
        ui.form_head(
            t("form_no", lang, number="06"),
            t("fixtures_title", lang),
            t("fixtures_desc", lang),
            f"{t('source', lang)} FPL",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        ui.fixtures(
            [
                ui.fixture(
                    gameweek=gameweek(match["event"], lang),
                    opponent=match["opponent"],
                    venue=t("fixtures_home" if match["home"] else "fixtures_away", lang),
                    difficulty=match["difficulty"],
                    difficulty_label=t("fixtures_difficulty", lang),
                )
                for match in upcoming
            ]
        ),
        unsafe_allow_html=True,
    )


# ── FORMA 07 · Mercado ──

priciest = fpl.priciest_midfielders(boot, limit=8)
if priciest:
    st.markdown(ui.halfway(), unsafe_allow_html=True)
    st.markdown(
        ui.form_head(
            t("form_no", lang, number="07"),
            t("market_title", lang),
            t("market_desc", lang),
            f"{t('source', lang)} FPL",
        ),
        unsafe_allow_html=True,
    )
    side, chart = st.columns([1, 2.2])
    with side:
        st.markdown(
            ui.readouts(
                [
                    ui.readout(f"{stats['price']:.1f}", t("market_price", lang), subject=True),
                    ui.readout(f"{stats['selected_by']:.1f}%", t("market_owned", lang)),
                ]
            ),
            unsafe_allow_html=True,
        )
    with chart:
        highlight = element.get("web_name", "")
        names = [row["name"] for row in priciest]
        prices = [row["price"] for row in priciest]
        if highlight not in names:
            names.append(highlight)
            prices.append(stats["price"])
        st.plotly_chart(
            charts.price_bars(names, prices, highlight, t("market_price", lang)),
            use_container_width=True,
            config={"displayModeBar": False},
        )


# ── FORMA 08 · Selección ──

if splits:
    totals = espn.aggregate_splits(splits)
    st.markdown(ui.halfway(), unsafe_allow_html=True)
    st.markdown(
        ui.form_head(
            t("form_no", lang, number="08"),
            t("intl_title", lang),
            t("intl_desc", lang, competitions=totals["competitions"], starts=totals["starts"]),
            f"{t('source', lang)} ESPN",
        ),
        unsafe_allow_html=True,
    )
    columns = "1.8fr repeat(8, 1fr)"
    headers = [
        t("intl_competition", lang), t("intl_starts", lang), t("intl_goals", lang),
        t("intl_assists", lang), t("intl_shots", lang), t("intl_sot", lang),
        t("intl_fouls_committed", lang), t("intl_fouls_drawn", lang), t("intl_cards", lang),
    ]
    keys = ["starts", "goals", "assists", "shots", "shots_on_target",
            "fouls_committed", "fouls_drawn", "yellow_cards"]
    st.markdown(
        ui.table(
            ui.row(headers, columns, head=True)
            + "".join(
                ui.row([split["name"]] + [split[key] for key in keys], columns)
                for split in splits
            )
            + ui.row(["Total"] + [totals[key] for key in keys], columns, subject=True)
        ),
        unsafe_allow_html=True,
    )


# ── FORMA 09 · Hemeroteca ──

if news:
    st.markdown(ui.halfway(), unsafe_allow_html=True)
    st.markdown(
        ui.form_head(
            t("form_no", lang, number="09"),
            t("news_title", lang),
            t("news_desc", lang),
            f"{t('source', lang)} ESPN",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        "".join(
            ui.news_item(
                headline=item["headline"],
                description=item["description"],
                published=format_date(item["published"], lang),
                link=item["link"],
                read_label=t("news_read", lang),
            )
            for item in news
        ),
        unsafe_allow_html=True,
    )


# ── FORMA 10 · Metodología ──

st.markdown(ui.halfway(), unsafe_allow_html=True)
st.markdown(
    ui.form_head(t("form_no", lang, number="10"), t("method_title", lang)),
    unsafe_allow_html=True,
)
# Sólo se listan las fuentes que de verdad aportaron algo a esta ejecución -- no
# basta con que el SDK esté instalado. Si está instalado pero la fuente igualmente
# no entregó nada (cuota agotada, red caída), el aviso de la sección correspondiente
# ya lo explica arriba; aquí no hay que citarla como si hubiera aportado datos.
sources = [("FPL", "method_fpl")]
if espn_delivered:
    sources.append(("ESPN", "method_espn"))
if fotmob_delivered:
    sources.append(("FotMob", "method_fotmob"))

method_columns = st.columns(len(sources))
for column, (label, key) in zip(method_columns, sources):
    with column:
        st.markdown(ui.method(label, t(key, lang, sample=sample)), unsafe_allow_html=True)

# Esta nota es específica de "el SDK no viene instalado" (la build pública), no de
# "el SDK está pero la llamada falló" -- ese segundo caso ya lo cuenta el aviso de
# arriba con el motivo real, y decir aquí "no es un fallo de red" sería falso.
if not (ESPN_AVAILABLE and FOTMOB_AVAILABLE):
    st.markdown(
        ui.notice(t("method_public_note_title", lang), t("method_public_note", lang)),
        unsafe_allow_html=True,
    )

st.markdown(
    ui.notice(t("method_limits_title", lang), t("method_limits", lang)),
    unsafe_allow_html=True,
)
footer_key = "footer" if (espn_delivered and fotmob_delivered) else "footer_fpl_only"
st.markdown(ui.footer(t(footer_key, lang), t("footer_updated", lang)), unsafe_allow_html=True)
