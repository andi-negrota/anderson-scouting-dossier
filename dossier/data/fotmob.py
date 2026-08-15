"""Clasificacion y lideres de la Premier League via FotMob.

El SDK expone liga y partidos, no jugadores: `FotMob` solo tiene `league`, `leagues`,
`match` y `matches`. Por eso FotMob aporta contexto de competicion (tabla y lideres
por categoria) y no estadisticas individuales de Anderson.
"""

from __future__ import annotations

from typing import Any

PREMIER_LEAGUE_ID = 47
SEASON = "2025/2026"


class FotmobUnavailable(RuntimeError):
    """FotMob no respondio, o el SDK que la sirve (parse_apis) no esta instalado en
    este entorno -- es el caso del despliegue publico, que se publica sin API keys
    propias y por tanto sin este SDK generado por cuenta."""


def _stats_payload(season: str = SEASON) -> dict:
    try:
        from parse_apis.fotmob_com_api import FotMob
    except ImportError as exc:
        raise FotmobUnavailable("El SDK de FotMob (parse_apis) no esta disponible") from exc

    try:
        stats = FotMob().league(PREMIER_LEAGUE_ID).stats(season=season)
    except Exception as exc:
        raise FotmobUnavailable(f"No se pudieron leer las estadisticas de liga: {exc}") from exc
    return getattr(stats, "_extra", {}) or {}


def _as_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def standings(season: str = SEASON) -> list[dict]:
    """Tabla completa. La app anterior tenia esta funcion pero no la usaba en ningun sitio."""
    extra = _stats_payload(season)
    tables = extra.get("overview", {}).get("table", [])
    if not tables:
        return []
    entries = tables[0].get("data", {}).get("table", {}).get("all", [])

    rows = []
    for entry in entries:
        scored, conceded = _split_score(entry.get("scoresStr", "0-0"))
        rows.append(
            {
                "rank": entry.get("idx", 0),
                "team": entry.get("name", ""),
                "short": entry.get("shortName", ""),
                "played": entry.get("played", 0),
                "wins": entry.get("wins", 0),
                "draws": entry.get("draws", 0),
                "losses": entry.get("losses", 0),
                "goals_for": scored,
                "goals_against": conceded,
                "goal_difference": entry.get("goalConDiff", 0),
                "points": entry.get("pts", 0),
                "qualification": entry.get("qualColor", ""),
            }
        )
    return sorted(rows, key=lambda r: r["rank"])


def _split_score(text: str) -> tuple[int, int]:
    """'52-33' -> (52, 33). Tolerante a formatos raros."""
    try:
        scored, conceded = text.split("-")
        return int(scored), int(conceded)
    except (ValueError, AttributeError):
        return 0, 0


def category_leaders(season: str = SEASON) -> dict[str, dict]:
    """Lider de cada categoria estadistica: goles, asistencias, rating, xG..."""
    extra = _stats_payload(season)
    leaders = {}
    for block in extra.get("stats", {}).get("players", []):
        participant = block.get("participant", {})
        leaders[block.get("header", "")] = {
            "player": participant.get("name", ""),
            "team": participant.get("teamName", ""),
            "value": _as_float(participant.get("value")),
        }
    return leaders
