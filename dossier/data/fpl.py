"""Datos oficiales de la Premier League via la API publica de Fantasy Premier League.

Es la unica fuente del proyecto con estadisticas de club de Anderson: ESPN solo
publica sus splits internacionales y el SDK de FotMob no expone endpoint de jugador.

Todos los numeros que devuelve este modulo son valores publicados por la API. No
hay estimaciones ni constantes escritas a mano: si un dato no esta disponible, la
funcion lo omite en vez de rellenarlo.
"""

from __future__ import annotations

from typing import Any, Iterable, Sequence

import requests

FPL_BASE = "https://fantasy.premierleague.com/api"
TIMEOUT = 20

ANDERSON_FPL_ID = 481
MIDFIELDER = 3

# Umbral de minutos para entrar en el grupo de comparacion. Sin el, los percentiles
# se inflan con suplentes que han jugado 40 minutos y tienen ratios por 90 absurdos.
PEER_MIN_MINUTES = 900

_SESSION = requests.Session()
_SESSION.headers.update({"User-Agent": "anderson-dossier/1.0 (+https://github.com)"})


class FplUnavailable(RuntimeError):
    """La API de FPL no respondio o devolvio algo que no sabemos leer."""


def _get(path: str) -> dict:
    try:
        response = _SESSION.get(f"{FPL_BASE}{path}", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise FplUnavailable(f"GET {path} fallo: {exc}") from exc
    except ValueError as exc:
        raise FplUnavailable(f"GET {path} no devolvio JSON valido: {exc}") from exc


# ── Descarga cruda ──────────────────────────────────────────────────────────

def bootstrap() -> dict:
    """Volcado general: jugadores, equipos, jornadas y posiciones."""
    return _get("/bootstrap-static/")


def element_summary(player_id: int = ANDERSON_FPL_ID) -> dict:
    """Historico por temporada, partido a partido y calendario de un jugador."""
    return _get(f"/element-summary/{player_id}/")


# ── Utilidades ──────────────────────────────────────────────────────────────

def _to_float(value: Any) -> float:
    """La API mezcla numeros y strings ('2.94'); normalizamos a float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def per_90(element: dict, field: str) -> float:
    """Convierte un total de temporada a tasa por 90 minutos."""
    minutes = _to_float(element.get("minutes"))
    if minutes <= 0:
        return 0.0
    return _to_float(element.get(field)) * 90.0 / minutes


def percentile(value: float, peers: Sequence[float]) -> float:
    """Percentil de `value` dentro de `peers`, repartiendo los empates a la mitad.

    Devuelve 0-100. Con lista vacia devuelve 0.
    """
    if not peers:
        return 0.0
    below = sum(1 for p in peers if p < value)
    ties = sum(1 for p in peers if p == value)
    return (below + 0.5 * ties) / len(peers) * 100.0


def rank_of(value: float, peers: Sequence[float]) -> int:
    """Puesto (1 = mejor) de `value` dentro de `peers`, ambos incluidos."""
    return sum(1 for p in peers if p > value) + 1


# ── Metricas comparables ────────────────────────────────────────────────────
# (clave i18n, campo de la API, modo). "field" = la API ya lo da por 90;
# "total" = es un acumulado de temporada y lo dividimos nosotros.

RADAR_METRICS: tuple[tuple[str, str, str], ...] = (
    ("xa90", "expected_assists", "total"),
    ("xg90", "expected_goals", "total"),
    ("creativity90", "creativity", "total"),
    ("tackles90", "tackles", "total"),
    ("recoveries90", "recoveries", "total"),
    ("influence90", "influence", "total"),
)

TABLE_METRICS: tuple[tuple[str, str, str], ...] = RADAR_METRICS + (
    ("xgi90", "expected_goal_involvements", "total"),
    ("cbi90", "clearances_blocks_interceptions", "total"),
    ("threat90", "threat", "total"),
    ("defcon90", "defensive_contribution", "total"),
)

# Rankings que la propia API publica, ya calculados sobre la posicion del jugador.
OFFICIAL_RANKS: tuple[tuple[str, str], ...] = (
    ("influence", "influence_rank_type"),
    ("creativity", "creativity_rank_type"),
    ("threat", "threat_rank_type"),
    ("ict", "ict_index_rank_type"),
    ("ppg", "points_per_game_rank_type"),
    ("selected", "selected_rank_type"),
)


def _metric_value(element: dict, field: str, mode: str) -> float:
    if mode == "field":
        return _to_float(element.get(field))
    return per_90(element, field)


def peers(
    boot: dict,
    element_type: int = MIDFIELDER,
    min_minutes: int = PEER_MIN_MINUTES,
) -> list[dict]:
    """Jugadores de la misma posicion con minutos suficientes para comparar."""
    return [
        e
        for e in boot["elements"]
        if e.get("element_type") == element_type
        and _to_float(e.get("minutes")) >= min_minutes
    ]


def percentile_profile(
    element: dict,
    peer_group: Sequence[dict],
    metrics: Iterable[tuple[str, str, str]] = RADAR_METRICS,
) -> list[dict]:
    """Percentil real del jugador en cada metrica frente a su grupo.

    Cada entrada: {key, value, percentile, rank, sample}. `key` es la clave de
    traduccion, no un texto: la etiqueta la pone la capa de i18n.
    """
    profile = []
    for key, field, mode in metrics:
        value = _metric_value(element, field, mode)
        peer_values = [_metric_value(p, field, mode) for p in peer_group]
        profile.append(
            {
                "key": key,
                "value": value,
                "percentile": percentile(value, peer_values),
                "rank": rank_of(value, peer_values),
                "sample": len(peer_values),
            }
        )
    return profile


# ── Vistas de dominio ───────────────────────────────────────────────────────

def find_player(boot: dict, player_id: int = ANDERSON_FPL_ID) -> dict:
    for element in boot["elements"]:
        if element.get("id") == player_id:
            return element
    raise FplUnavailable(f"El jugador {player_id} no aparece en bootstrap-static")


def team_names(boot: dict) -> dict[int, str]:
    return {t["id"]: t["name"] for t in boot["teams"]}


def season_state(boot: dict) -> dict:
    """En que punto de la temporada estamos.

    Importa para etiquetar bien: mientras la temporada no arranca, los totales de
    `elements` siguen siendo los de la campana anterior y con el equipo anterior.
    """
    events = boot.get("events", [])
    finished = [e for e in events if e.get("finished")]
    current = next((e for e in events if e.get("is_current")), None)
    following = next((e for e in events if e.get("is_next")), None)
    return {
        "started": bool(finished) or current is not None,
        "finished_gameweeks": len(finished),
        "total_gameweeks": len(events),
        "next_deadline": (following or {}).get("deadline_time"),
        "next_name": (following or {}).get("name"),
    }


def headline_stats(element: dict) -> dict:
    """Cifras de cabecera, todas tal cual las publica la API."""
    minutes = _to_float(element.get("minutes"))
    goals = int(element.get("goals_scored") or 0)
    assists = int(element.get("assists") or 0)
    return {
        "minutes": int(minutes),
        "starts": int(element.get("starts") or 0),
        "goals": goals,
        "assists": assists,
        "goal_involvements": goals + assists,
        "xg": _to_float(element.get("expected_goals")),
        "xa": _to_float(element.get("expected_assists")),
        "xgi": _to_float(element.get("expected_goal_involvements")),
        "tackles": int(element.get("tackles") or 0),
        "recoveries": int(element.get("recoveries") or 0),
        "cbi": int(element.get("clearances_blocks_interceptions") or 0),
        "yellow_cards": int(element.get("yellow_cards") or 0),
        "red_cards": int(element.get("red_cards") or 0),
        "bonus": int(element.get("bonus") or 0),
        "total_points": int(element.get("total_points") or 0),
        "points_per_game": _to_float(element.get("points_per_game")),
        "price": _to_float(element.get("now_cost")) / 10.0,
        "selected_by": _to_float(element.get("selected_by_percent")),
        "ict_index": _to_float(element.get("ict_index")),
        "joined": element.get("team_join_date"),
        "birth_date": element.get("birth_date"),
    }


def official_ranks(element: dict, peer_total: int) -> list[dict]:
    return [
        {"key": key, "rank": int(element.get(field) or 0), "sample": peer_total}
        for key, field in OFFICIAL_RANKS
        if element.get(field)
    ]


def season_history(summary: dict) -> list[dict]:
    """Una fila por temporada previa, en orden cronologico."""
    rows = []
    for season in summary.get("history_past", []):
        minutes = _to_float(season.get("minutes"))
        goals = int(season.get("goals_scored") or 0)
        assists = int(season.get("assists") or 0)
        rows.append(
            {
                "season": season.get("season_name", ""),
                "minutes": int(minutes),
                "goals": goals,
                "assists": assists,
                "goal_involvements": goals + assists,
                "xg": _to_float(season.get("expected_goals")),
                "xa": _to_float(season.get("expected_assists")),
                "points": int(season.get("total_points") or 0),
                "end_cost": _to_float(season.get("end_cost")) / 10.0,
            }
        )
    return rows


def upcoming_fixtures(summary: dict, names: dict[int, str], limit: int = 6) -> list[dict]:
    """Proximos partidos con rival y dificultad oficial (1 facil - 5 dificil)."""
    fixtures = []
    for fixture in summary.get("fixtures", [])[:limit]:
        is_home = bool(fixture.get("is_home"))
        opponent_id = fixture.get("team_a") if is_home else fixture.get("team_h")
        fixtures.append(
            {
                "event": fixture.get("event_name") or "",
                "opponent": names.get(opponent_id, "?"),
                "home": is_home,
                "difficulty": int(fixture.get("difficulty") or 0),
                "kickoff": fixture.get("kickoff_time"),
            }
        )
    return fixtures


def peer_cloud(
    boot: dict,
    peer_group: Sequence[dict],
    axes: tuple[tuple[str, str], tuple[str, str], tuple[str, str]] = (
        ("recoveries", "total"),
        ("expected_assists", "total"),
        ("expected_goals", "total"),
    ),
) -> list[dict]:
    """Un punto por centrocampista, con tres tasas por 90 como coordenadas.

    Alimenta la nube 3D: son los mismos {n} jugadores que sostienen los percentiles,
    así que la vista espacial y la tabla cuentan exactamente lo mismo.
    """
    names = team_names(boot)
    cloud = []
    for element in peer_group:
        x, y, z = (_metric_value(element, field, mode) for field, mode in axes)
        cloud.append(
            {
                "id": element.get("id"),
                "name": element.get("web_name", ""),
                "team": names.get(element.get("team"), ""),
                "minutes": int(_to_float(element.get("minutes"))),
                "x": x,
                "y": y,
                "z": z,
            }
        )
    return cloud


def axis_leaders(cloud: Sequence[dict]) -> dict[str, dict]:
    """Quién manda en cada eje. Es la vista en tabla de la nube: sin ella, los
    valores del gráfico 3D sólo se podrían leer pasando el ratón por encima."""
    leaders = {}
    for axis in ("x", "y", "z"):
        if cloud:
            best = max(cloud, key=lambda point: point[axis])
            leaders[axis] = {"name": best["name"], "team": best["team"], "value": best[axis]}
    return leaders


def priciest_midfielders(boot: dict, limit: int = 8) -> list[dict]:
    """Centrocampistas mas caros de la temporada, por precio de la API."""
    names = team_names(boot)
    mids = [e for e in boot["elements"] if e.get("element_type") == MIDFIELDER]
    mids.sort(key=lambda e: _to_float(e.get("now_cost")), reverse=True)
    return [
        {
            "name": e.get("web_name", ""),
            "team": names.get(e.get("team"), ""),
            "price": _to_float(e.get("now_cost")) / 10.0,
            "id": e.get("id"),
        }
        for e in mids[:limit]
    ]
