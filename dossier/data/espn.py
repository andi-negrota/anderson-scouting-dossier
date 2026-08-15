"""Perfil, splits internacionales y noticias del jugador via ESPN.

Aviso sobre el alcance de esta fuente: para Anderson, ESPN solo publica splits de
seleccion (Mundial 2026 y amistosos). No devuelve estadisticas de club ni gamelog
-- se comprobo consultando la API, y `athlete.gamelog` viene vacio. Cualquier cifra
de club sale de dossier.data.fpl, no de aqui.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from parse_apis.espn_sports_data_api import ESPN

ANDERSON_ESPN_ID = "238472"

# Claves de estadistica que ESPN usa en los splits, con su etiqueta corta.
SPLIT_STATS: tuple[tuple[str, str], ...] = (
    ("STRT", "starts"),
    ("G", "goals"),
    ("A", "assists"),
    ("SHOT", "shots"),
    ("SOG", "shots_on_target"),
    ("FC", "fouls_committed"),
    ("FA", "fouls_drawn"),
    ("YC", "yellow_cards"),
    ("RC", "red_cards"),
)


class EspnUnavailable(RuntimeError):
    """ESPN no respondio, o el SDK que la sirve (parse_apis) no esta instalado en
    este entorno -- es el caso del despliegue publico, que se publica sin API keys
    propias y por tanto sin este SDK generado por cuenta."""


def _client() -> "ESPN":
    try:
        from parse_apis.espn_sports_data_api import ESPN
    except ImportError as exc:
        raise EspnUnavailable("El SDK de ESPN (parse_apis) no esta disponible") from exc
    return ESPN()


def _league():
    try:
        from parse_apis.espn_sports_data_api import League
    except ImportError as exc:
        raise EspnUnavailable("El SDK de ESPN (parse_apis) no esta disponible") from exc
    return League.PREMIER_LEAGUE


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def height_cm(raw: str) -> int | None:
    """ESPN publica la altura como `5' 10"`. La pasamos a centímetros."""
    try:
        feet, inches = str(raw).replace('"', "").split("'")
        return round(int(feet.strip()) * 30.48 + int(inches.strip()) * 2.54)
    except (ValueError, AttributeError):
        return None


def weight_kg(raw: str) -> int | None:
    """ESPN publica el peso como `150 lbs`."""
    try:
        pounds = float(str(raw).lower().replace("lbs", "").strip())
        return round(pounds * 0.45359237)
    except (ValueError, AttributeError):
        return None


def profile() -> dict:
    """Ficha biometrica. `jersey` puede venir vacio: el jugador acaba de fichar."""
    try:
        athlete = _client().athlete(ANDERSON_ESPN_ID)
        data = athlete.profile(league=_league())
    except Exception as exc:  # el SDK envuelve errores de red en tipos propios
        raise EspnUnavailable(f"No se pudo leer el perfil: {exc}") from exc

    return {
        "name": data.name,
        "first_name": getattr(data, "first_name", "") or data.name.split()[0],
        "age": data.age or 0,
        "height": data.height or "",
        "weight": data.weight or "",
        "position": data.position or "",
        "jersey": data.jersey or "",
    }


def international_splits() -> list[dict]:
    """Splits que ESPN publica, uno por competicion, sin reordenar ni filtrar.

    La version anterior de la app intentaba elegir "el mejor split" con una lista de
    prioridades encabezada por Premier League. Como ninguno de los splits de Anderson
    es de club, la heuristica caia al ultimo elemento y acababa presentando sus
    numeros del Mundial como si fueran los de la Premier.
    """
    try:
        overview = _client().athlete(ANDERSON_ESPN_ID).overview(league=_league())
    except Exception as exc:
        raise EspnUnavailable(f"No se pudo leer el overview: {exc}") from exc

    statistics = overview.statistics or {}
    splits = []
    for split in statistics.get("splits", []):
        values = split.get("stats", {})
        row = {"name": split.get("display_name", "")}
        row.update({label: _as_int(values.get(key)) for key, label in SPLIT_STATS})
        splits.append(row)
    return splits


def aggregate_splits(splits: list[dict]) -> dict:
    """Suma de todos los splits. Evita las incoherencias del texto anterior, que
    hablaba de 6 partidos y 18 faltas cuando su propia tabla sumaba 9 y 22."""
    totals = {label: 0 for _, label in SPLIT_STATS}
    for split in splits:
        for label in totals:
            totals[label] += split.get(label, 0)
    totals["competitions"] = len(splits)
    return totals


def player_news(limit: int = 6) -> list[dict]:
    """Noticias del jugador.

    La app anterior tenia una funcion `get_player_news` que ignoraba el player_id y
    pedia titulares genericos de la liga -- y ademas nunca llegaba a llamarse. Estas
    si son las noticias del atleta, que es donde esta documentado el traspaso.
    """
    try:
        overview = _client().athlete(ANDERSON_ESPN_ID).overview(league=_league())
    except Exception as exc:
        raise EspnUnavailable(f"No se pudieron leer las noticias: {exc}") from exc

    items = []
    for item in (overview.news or [])[:limit]:
        data = item if isinstance(item, dict) else getattr(item, "__dict__", {})
        items.append(
            {
                "headline": data.get("headline", ""),
                "description": data.get("description", "") or "",
                "published": data.get("published", ""),
                "link": data.get("link", ""),
                "type": data.get("type", ""),
            }
        )
    return items
