"""Pruebas del informe.

Se ejecutan con la app real y con las APIs reales, así que tardan y necesitan red.
Están pensadas como comprobación de que la página entera se renderiza y de que la
capa de textos está completa, no como test unitario rápido.

    .venv/Scripts/python -m pytest tests -v
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
for path in [ROOT, ROOT / "parse_apis" / "src"]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from dossier.data import espn, fotmob, fpl  # noqa: E402
from dossier.i18n import LANGUAGES, STRINGS, format_date, gameweek, position, t  # noqa: E402


# ── Build pública: sin el SDK de ESPN/FotMob ──
# El despliegue público (Streamlit Community Cloud) no lleva parse_apis, porque su
# contenido generado es privado por cuenta. Esta build tiene que degradar con
# gracia: seguir importando y devolver un error de dominio, nunca un crash.

def test_data_layer_survives_missing_espn_fotmob_sdk(monkeypatch):
    # `None` en sys.modules es el truco estándar de Python para forzar ImportError
    # sin tocar ningún archivo real ni el sys.path.
    monkeypatch.setitem(sys.modules, "parse_apis.espn_sports_data_api", None)
    monkeypatch.setitem(sys.modules, "parse_apis.fotmob_com_api", None)

    with pytest.raises(espn.EspnUnavailable):
        espn.profile()
    with pytest.raises(espn.EspnUnavailable):
        espn.international_splits()
    with pytest.raises(espn.EspnUnavailable):
        espn.player_news()
    with pytest.raises(fotmob.FotmobUnavailable):
        fotmob.standings()

    # Es justo esta señal la que app.py usa para decidir si intenta cargar la
    # sección: si find_spec deja de detectar el módulo, no se llega a llamar y no
    # se muestra ningún aviso de error -- la sección simplemente no está en el build.
    assert importlib.util.find_spec("parse_apis.espn_sports_data_api") is None
    assert importlib.util.find_spec("parse_apis.fotmob_com_api") is None


# ── Capa de textos ──

def test_every_string_has_every_language():
    missing = [
        (key, lang)
        for key, entry in STRINGS.items()
        for lang in LANGUAGES
        if not entry.get(lang)
    ]
    assert not missing, f"Traducciones que faltan: {missing}"


def test_app_only_uses_keys_that_exist():
    """Si app.py pide una clave inexistente, `t` devuelve la clave y se ve en pantalla."""
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    # El lookbehind evita capturar `.get("name")`, que también termina en `t(`.
    used = set(re.findall(r'(?<![\w.])t\(\s*"([a-z0-9_]+)"', source))
    # Las claves de métricas y rankings se componen en tiempo de ejecución.
    dynamic = {f"metric_{key}" for key, _, _ in fpl.TABLE_METRICS}
    dynamic |= {f"rank_{key}" for key, _ in fpl.OFFICIAL_RANKS}
    unknown = {key for key in used if key not in STRINGS} - dynamic
    assert not unknown, f"Claves usadas en app.py que no existen en i18n: {unknown}"


def test_dynamic_keys_exist():
    for key, _, _ in fpl.TABLE_METRICS:
        assert f"metric_{key}" in STRINGS, f"Falta metric_{key}"
    for key, _ in fpl.OFFICIAL_RANKS:
        assert f"rank_{key}" in STRINGS, f"Falta rank_{key}"


@pytest.mark.parametrize(
    "raw,lang,expected",
    [
        ("2026-07-23T16:00:11.000+00:00", "es", "23 jul 2026"),
        ("2026-08-21T17:30:00Z", "en", "21 Aug 2026"),
        ("2026-07-02", "es", "2 jul 2026"),
        ("no es una fecha", "es", "no es una fecha"),
        (None, "es", ""),
    ],
)
def test_format_date(raw, lang, expected):
    assert format_date(raw, lang) == expected


def test_position_and_gameweek():
    assert position("Midfielder", "es") == "Centrocampista"
    assert position("Midfielder", "en") == "Midfielder"
    assert position("Sweeper", "es") == "Sweeper"  # desconocida: se deja tal cual
    assert gameweek("Gameweek 3", "es") == "Jornada 3"
    assert gameweek("sin numero", "es") == "sin numero"


# ── Percentiles ──

def test_percentile_is_a_share_of_the_group():
    peers = [1.0, 2.0, 3.0, 4.0]
    assert fpl.percentile(5.0, peers) == 100.0
    assert fpl.percentile(0.0, peers) == 0.0
    assert fpl.percentile(2.5, peers) == 50.0
    assert fpl.percentile(1.0, peers) == 12.5  # un empate cuenta la mitad


def test_percentile_handles_empty_group():
    assert fpl.percentile(5.0, []) == 0.0


def test_rank_counts_from_one():
    peers = [1.0, 2.0, 3.0]
    assert fpl.rank_of(3.0, peers) == 1
    assert fpl.rank_of(0.5, peers) == 4


def test_per_90_without_minutes_is_zero():
    """División por cero: un jugador sin minutos no puede tener tasa por 90."""
    assert fpl.per_90({"minutes": 0, "tackles": 5}, "tackles") == 0.0


# ── Render completo ──

def test_peer_cloud_matches_the_percentile_group():
    """La nube 3D y los percentiles tienen que hablar de los mismos jugadores. Si se
    desincronizan, el gráfico y la tabla contarían cosas distintas."""
    boot = fpl.bootstrap()
    peers = fpl.peers(boot)
    cloud = fpl.peer_cloud(boot, peers)

    assert len(cloud) == len(peers)
    assert {point["id"] for point in cloud} == {peer["id"] for peer in peers}
    assert all(point["name"] and point["team"] for point in cloud)

    subject = next(point for point in cloud if point["id"] == fpl.ANDERSON_FPL_ID)
    element = fpl.find_player(boot)
    assert subject["x"] == pytest.approx(fpl.per_90(element, "recoveries"))


def test_axis_leaders_are_the_maximum_of_each_axis():
    cloud = [
        {"id": 1, "name": "A", "team": "T", "minutes": 900, "x": 1.0, "y": 5.0, "z": 2.0},
        {"id": 2, "name": "B", "team": "T", "minutes": 900, "x": 9.0, "y": 1.0, "z": 3.0},
    ]
    leaders = fpl.axis_leaders(cloud)
    assert leaders["x"]["name"] == "B"
    assert leaders["y"]["name"] == "A"
    assert leaders["z"]["value"] == 3.0


def test_meter_lights_one_segment_per_five_points():
    """El vúmetro tiene 20 segmentos, así que cada uno vale 5 puntos de percentil."""
    from dossier import components as ui

    assert ui.meter_row("m", "1.00", 100.0, 1, 126).count("background:") == ui.METER_SEGMENTS
    assert ui.meter_row("m", "1.00", 0.0, 126, 126).count("background:") == 0
    assert ui.meter_row("m", "1.00", 50.0, 60, 126).count("background:") == ui.METER_SEGMENTS // 2


def test_markup_escapes_values_from_the_apis():
    from dossier import components as ui

    hostile = '<img src=x onerror="alert(1)">'
    assert "<img" not in ui.news_item(hostile, hostile, "1 ene 2026", "", "leer")
    assert "&lt;img" in ui.news_item(hostile, "", "1 ene 2026", "", "leer")
    assert "javascript:" not in ui.news_item("t", "", "", "javascript:alert(1)", "leer")


@pytest.mark.slow
def test_app_renders_in_both_languages():
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=240)
    app.run()
    assert not app.exception, f"La app falló en español: {app.exception}"

    spanish = " ".join(element.value for element in app.markdown)
    assert "Nottingham Forest" in spanish
    assert "Percentiles frente a" in spanish
    assert "Jornada" in spanish
    assert "Forma 01" in spanish

    # El selector es un conmutador con clave "lang"; fijarla equivale a pulsarlo.
    app.session_state["lang"] = "en"
    app.run()
    assert not app.exception, f"La app falló en inglés: {app.exception}"

    english = " ".join(element.value for element in app.markdown)
    assert "Percentiles against" in english
    assert "Gameweek" in english
    assert "Form 01" in english
    assert "Percentiles frente a" not in english, "Quedó texto en español con idioma inglés"


@pytest.mark.slow
def test_app_renders_the_public_build_without_espn_or_fotmob(monkeypatch):
    """Esta es la build que se despliega en Streamlit Community Cloud: sin el SDK
    de parse_apis. Tiene que cargar limpia -- las secciones de ESPN/FotMob
    simplemente no aparecen, y no se muestra ningún aviso de error, porque no es
    un fallo: es que esta build nunca las incluyó."""
    from streamlit.testing.v1 import AppTest

    monkeypatch.setitem(sys.modules, "parse_apis.espn_sports_data_api", None)
    monkeypatch.setitem(sys.modules, "parse_apis.fotmob_com_api", None)

    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=240)
    app.run()
    assert not app.exception, f"La build pública falló al cargar: {app.exception}"
    assert not app.warning, f"La build pública no debe mostrar avisos de error: {app.warning}"

    # El primer bloque markdown es el <style> inyectado, con comentarios que citan
    # los mismos nombres de sección ("Hemeroteca", etc.) -- se excluye para no
    # confundir un comentario CSS con contenido renderizado.
    text = " ".join(
        element.value for element in app.markdown if not element.value.startswith("<style")
    )
    # Lo que SÍ debe seguir, porque sale de FPL (API pública, sin SDK privado):
    assert "Nottingham Forest" in text
    assert "Percentiles frente a" in text
    assert "Los centrocampistas de la Premier, en tres ejes" in text
    # Lo que NO debe aparecer, porque depende del SDK ausente:
    assert "Hemeroteca" not in text
    assert "Campaña internacional" not in text
    assert "Del Forest al City en la tabla" not in text

    # La metodología no debe citar fuentes que no aportaron nada visible. OJO: "ESPN"
    # a secas sigue apareciendo en la portada como atribución del importe del
    # traspaso (eso es correcto y no depende del SDK), así que se comprueban frases
    # concretas de las tarjetas de metodología y del pie, no la palabra suelta.
    assert "Ficha biométrica, splits de selección y noticias" not in text  # tarjeta ESPN
    assert "no aporta datos individuales" not in text  # tarjeta FotMob
    assert "Datos de Fantasy Premier League, ESPN y FotMob" not in text  # pie completo
    assert "Sobre esta build" in text
    assert "según ESPN" in text  # la cita del traspaso sí debe seguir
