"""Textos en español e inglés.

Todo texto visible vive aquí. Las secciones nunca llevan cadenas literales, así que
añadir un idioma es añadir una clave por entrada y nada más.
"""

from __future__ import annotations

from datetime import datetime

LANGUAGES = {"es": "Español", "en": "English"}
DEFAULT_LANGUAGE = "es"

MONTHS: dict[str, tuple[str, ...]] = {
    "es": ("ene", "feb", "mar", "abr", "may", "jun",
           "jul", "ago", "sep", "oct", "nov", "dic"),
    "en": ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"),
}

STRINGS: dict[str, dict[str, str]] = {
    # ── Chrome ──
    "app_title": {
        "es": "Elliot Anderson · Informe de scouting",
        "en": "Elliot Anderson · Scouting Dossier",
    },
    "sidebar_title": {"es": "Informe de scouting", "en": "Scouting Dossier"},
    "sidebar_sources": {"es": "FPL · ESPN · FotMob", "en": "FPL · ESPN · FotMob"},
    "language": {"es": "Idioma", "en": "Language"},
    "nav_position": {"es": "Centrocampista", "en": "Midfielder"},
    "gameweek": {"es": "Jornada {number}", "en": "Gameweek {number}"},
    "table_season": {"es": "Temporada", "en": "Season"},

    # ── Panel de instrumentos ──
    "form_no": {"es": "Forma {number}", "en": "Form {number}"},
    "source": {"es": "Fuente", "en": "Source"},
    "rail_live": {"es": "Lectura en vivo", "en": "Live read"},
    "rail_subject": {"es": "Sujeto", "en": "Subject"},
    # La tesis de portada se calcula: es la métrica en la que mejor puesto ocupa.
    # Si sus números cambian, cambia la frase.
    "hero_thesis": {
        "es": "Puesto <em>{rank} de {sample}</em> de la Premier League en {metric}.",
        "en": "Ranks <em>{rank} of {sample}</em> in the Premier League for {metric}.",
    },

    # ── Pieza 3D ──
    "cloud_title": {
        "es": "Los centrocampistas de la Premier, en tres ejes",
        "en": "Premier League midfielders, on three axes",
    },
    "cloud_desc": {
        "es": (
            "Los mismos <strong>{sample} centrocampistas</strong> que sostienen los "
            "percentiles, colocados por sus tres tasas por 90. El suelo lleva marcas de "
            "campo que no son adorno: el círculo es el <strong>50% central</strong> del "
            "grupo y las dos rectas son sus medianas. Gira la vista con el ratón."
        ),
        "en": (
            "The same <strong>{sample} midfielders</strong> behind the percentiles, placed "
            "by their three per-90 rates. The pitch markings on the floor are not "
            "decoration: the circle is the group's <strong>middle 50%</strong> and the two "
            "lines are its medians. Drag to rotate."
        ),
    },
    "cloud_peers": {"es": "Centrocampistas de la Premier", "en": "Premier League midfielders"},
    "cloud_middle": {"es": "50% central del grupo", "en": "Middle 50% of the group"},
    "cloud_empty": {
        "es": (
            "Todavía no hay centrocampistas con minutos suficientes esta temporada "
            "para formar el grupo de comparación. Vuelve cuando avancen más jornadas."
        ),
        "en": (
            "No midfielders have played enough minutes yet this season to form the "
            "comparison group. Check back once more matchweeks have passed."
        ),
    },
    "cloud_reading": {
        "es": "Lectura exacta",
        "en": "Exact values",
    },
    "cloud_reading_desc": {
        "es": (
            "En tres dimensiones se estima una posición, no se lee un valor. Estas son "
            "las cifras del sujeto y quién manda en cada eje."
        ),
        "en": (
            "Three dimensions give you a position, not a value. Here are the subject's "
            "figures and who leads each axis."
        ),
    },
    "cloud_axis": {"es": "Eje", "en": "Axis"},
    "cloud_subject_value": {"es": "Anderson", "en": "Anderson"},
    "cloud_leader": {"es": "Líder del eje", "en": "Axis leader"},

    # Posiciones tal y como las nombra ESPN, para no dejarlas en inglés en la vista ES.
    "position_goalkeeper": {"es": "Portero", "en": "Goalkeeper"},
    "position_defender": {"es": "Defensa", "en": "Defender"},
    "position_midfielder": {"es": "Centrocampista", "en": "Midfielder"},
    "position_forward": {"es": "Delantero", "en": "Forward"},

    # ── Portada ──
    "hero_move": {
        "es": "Nottingham Forest al Manchester City",
        "en": "Nottingham Forest to Manchester City",
    },
    "hero_fee_label": {
        "es": "Récord del club, según ESPN",
        "en": "Club record fee, per ESPN",
    },
    "hero_agreed": {"es": "Acuerdo: {date}", "en": "Agreed: {date}"},
    "hero_completed": {"es": "Fichaje cerrado: {date}", "en": "Move completed: {date}"},
    "badge_city": {"es": "Manchester City", "en": "Manchester City"},
    "badge_record": {"es": "Récord del club", "en": "Club record"},
    "badge_age": {"es": "{age} años", "en": "{age} years old"},
    "badge_england": {"es": "Internacional con Inglaterra", "en": "England international"},

    # ── Aviso de contexto ──
    "context_banner_title": {"es": "Qué estás viendo", "en": "What you are looking at"},
    "context_banner_body": {
        "es": (
            "La temporada 2026/27 aún no ha empezado (jornada 1 el {deadline}). "
            "Todas las cifras de club de esta página son de la <strong>2025/26 en el "
            "Nottingham Forest</strong>, la última que Anderson ha disputado. La API de "
            "Fantasy Premier League ya lo lista bajo el Manchester City porque el fichaje "
            "se cerró el 2 de julio de 2026."
        ),
        "en": (
            "The 2026/27 season has not started yet (gameweek 1 on {deadline}). "
            "Every club figure on this page is from <strong>2025/26 at Nottingham "
            "Forest</strong>, the last season Anderson played. The Fantasy Premier League "
            "API already lists him under Manchester City because the transfer closed on "
            "2 July 2026."
        ),
    },

    # ── Cifras de cabecera ──
    "kpi_eyebrow": {
        "es": "Temporada 2025/26 · Nottingham Forest",
        "en": "2025/26 season · Nottingham Forest",
    },
    "kpi_title": {
        "es": "La temporada que provocó el fichaje",
        "en": "The season that triggered the move",
    },
    "kpi_desc": {
        "es": "Totales de la Premier League 2025/26 publicados por la API oficial de Fantasy Premier League.",
        "en": "Premier League 2025/26 totals as published by the official Fantasy Premier League API.",
    },
    "kpi_minutes": {"es": "Minutos", "en": "Minutes"},
    "kpi_minutes_sub": {"es": "{starts} titularidades", "en": "{starts} starts"},
    "kpi_ga": {"es": "Goles + asistencias", "en": "Goals + assists"},
    "kpi_ga_sub": {"es": "{goals} G · {assists} A", "en": "{goals} G · {assists} A"},
    "kpi_xgi": {"es": "xG + xA", "en": "xG + xA"},
    "kpi_xgi_sub": {"es": "{xg} xG · {xa} xA", "en": "{xg} xG · {xa} xA"},
    "kpi_recoveries": {"es": "Recuperaciones", "en": "Recoveries"},
    "kpi_recoveries_sub": {"es": "{per90} por 90", "en": "{per90} per 90"},
    "kpi_tackles": {"es": "Entradas", "en": "Tackles"},
    "kpi_tackles_sub": {"es": "{cbi} despejes/bloqueos/int.", "en": "{cbi} clearances/blocks/int."},
    "kpi_points": {"es": "Puntos FPL", "en": "FPL points"},
    "kpi_points_sub": {"es": "{ppg} por partido", "en": "{ppg} per game"},

    # ── Percentiles ──
    "pct_eyebrow": {"es": "Perfil comparado", "en": "Comparative profile"},
    "pct_title": {
        "es": "Percentiles frente a los centrocampistas de la Premier",
        "en": "Percentiles against Premier League midfielders",
    },
    "pct_desc": {
        "es": (
            "Cada valor es una tasa por 90 minutos comparada con los <strong>{sample} "
            "centrocampistas</strong> de la Premier League con 900 minutos o más en la "
            "2025/26. Percentil 100 = el mejor de esos {sample}."
        ),
        "en": (
            "Each value is a per-90 rate compared against the <strong>{sample} Premier "
            "League midfielders</strong> with 900 or more minutes in 2025/26. "
            "Percentile 100 = best of those {sample}."
        ),
    },
    "pct_metric": {"es": "Métrica", "en": "Metric"},
    "pct_value": {"es": "Por 90", "en": "Per 90"},
    "pct_rank": {"es": "Puesto", "en": "Rank"},
    "pct_percentile": {"es": "Percentil", "en": "Percentile"},
    "metric_xa90": {"es": "xA por 90", "en": "xA per 90"},
    "metric_xg90": {"es": "xG por 90", "en": "xG per 90"},
    "metric_xgi90": {"es": "xG + xA por 90", "en": "xG + xA per 90"},
    "metric_creativity90": {"es": "Creatividad por 90", "en": "Creativity per 90"},
    "metric_influence90": {"es": "Influencia por 90", "en": "Influence per 90"},
    "metric_threat90": {"es": "Amenaza por 90", "en": "Threat per 90"},
    "metric_tackles90": {"es": "Entradas por 90", "en": "Tackles per 90"},
    "metric_recoveries90": {"es": "Recuperaciones por 90", "en": "Recoveries per 90"},
    "metric_cbi90": {
        "es": "Despejes + bloqueos + int. por 90",
        "en": "Clearances + blocks + int. per 90",
    },
    "metric_defcon90": {"es": "Aportación defensiva por 90", "en": "Defensive contribution per 90"},
    "radar_player": {"es": "Anderson", "en": "Anderson"},
    "radar_median": {
        "es": "Centrocampista mediano (percentil 50)",
        "en": "Median midfielder (50th percentile)",
    },

    # ── Lectura del perfil ──
    "read_eyebrow": {"es": "Lectura", "en": "Read"},
    "read_title": {"es": "Qué dice el perfil", "en": "What the profile says"},
    "read_body": {
        "es": (
            "Anderson lidera a los {sample} centrocampistas de la Premier en "
            "<strong>recuperaciones por 90</strong> ({rec}), y está en el percentil "
            "{tackles_pct} en entradas. Su <strong>xG por 90 es de solo {xg}</strong> "
            "(percentil {xg_pct}): no es un centrocampista de llegada. El perfil que dibujan "
            "los datos es el de un <strong>pivote que recupera y distribuye</strong>, no el "
            "de un interior de área."
        ),
        "en": (
            "Anderson leads all {sample} Premier League midfielders in "
            "<strong>recoveries per 90</strong> ({rec}), and sits in the {tackles_pct}th "
            "percentile for tackles. His <strong>xG per 90 is just {xg}</strong> "
            "({xg_pct}th percentile): he is not a late-arriving goal threat. The data "
            "describes a <strong>ball-winning, distributing holder</strong>, not a "
            "box-crashing number eight."
        ),
    },

    # ── Rankings oficiales ──
    "ranks_eyebrow": {
        "es": "Rankings oficiales de la Premier",
        "en": "Official Premier League rankings",
    },
    "ranks_title": {"es": "Su puesto entre centrocampistas", "en": "Where he ranks among midfielders"},
    "ranks_desc": {
        "es": "Puestos que publica la propia API, ya calculados sobre todos los centrocampistas de la liga.",
        "en": "Ranks published by the API itself, already computed across every midfielder in the league.",
    },
    "rank_influence": {"es": "Influencia", "en": "Influence"},
    "rank_creativity": {"es": "Creatividad", "en": "Creativity"},
    "rank_threat": {"es": "Amenaza", "en": "Threat"},
    "rank_ict": {"es": "Índice ICT", "en": "ICT index"},
    "rank_ppg": {"es": "Puntos por partido", "en": "Points per game"},
    # Es un puesto, no un porcentaje: se muestra como "#15", así que la etiqueta
    # tiene que decir "el 15.º más elegido" y no "jugadores que lo tienen".
    "rank_selected": {"es": "Más elegido", "en": "Most selected"},
    "rank_prefix": {"es": "Puesto", "en": "Rank"},

    # ── Curva de desarrollo ──
    "curve_eyebrow": {"es": "Trayectoria", "en": "Trajectory"},
    "curve_title": {"es": "Seis temporadas de progresión", "en": "Six seasons of progression"},
    "curve_desc": {
        "es": (
            "Minutos y puntos por temporada desde su debut. No es una proyección: son los "
            "totales históricos que devuelve la API para cada campaña."
        ),
        "en": (
            "Minutes and points per season since his debut. Not a projection: these are the "
            "historical totals the API returns for each campaign."
        ),
    },
    "curve_minutes": {"es": "Minutos", "en": "Minutes"},
    "curve_points": {"es": "Puntos FPL", "en": "FPL points"},
    "curve_xgi": {"es": "xG + xA", "en": "xG + xA"},

    # ── El salto ──
    "jump_eyebrow": {"es": "El salto", "en": "The step up"},
    "jump_title": {"es": "Del Forest al City en la tabla", "en": "From Forest to City in the table"},
    "jump_desc": {
        "es": "Cómo acabaron ambos clubes la Premier League 2025/26, según FotMob.",
        "en": "How both clubs finished the 2025/26 Premier League, per FotMob.",
    },
    "jump_position": {"es": "Puesto", "en": "Position"},
    "jump_points": {"es": "Puntos", "en": "Points"},
    "jump_gd": {"es": "Diferencia de goles", "en": "Goal difference"},

    # ── Calendario ──
    "fixtures_eyebrow": {"es": "Lo que viene", "en": "What is next"},
    "fixtures_title": {"es": "Primeras jornadas con el City", "en": "First gameweeks at City"},
    "fixtures_desc": {
        "es": "Calendario y dificultad oficial (1 = fácil, 5 = difícil) publicados por la Premier League.",
        "en": "Fixtures and official difficulty (1 = easy, 5 = hard) as published by the Premier League.",
    },
    "fixtures_home": {"es": "Casa", "en": "Home"},
    "fixtures_away": {"es": "Fuera", "en": "Away"},
    "fixtures_difficulty": {"es": "Dificultad", "en": "Difficulty"},

    # ── Mercado ──
    "market_eyebrow": {"es": "Contexto de mercado", "en": "Market context"},
    "market_title": {"es": "Precio y propiedad en FPL", "en": "FPL price and ownership"},
    "market_desc": {
        "es": (
            "Precio de salida de Anderson frente a los centrocampistas más caros del juego. "
            "Es el único dato de valoración que publica una API: el importe del traspaso "
            "procede de la información de ESPN enlazada más abajo, no de una fuente de datos."
        ),
        "en": (
            "Anderson's starting price against the priciest midfielders in the game. It is the "
            "only valuation figure any API publishes: the transfer fee comes from the ESPN "
            "reporting linked below, not from a data source."
        ),
    },
    "market_price": {"es": "Precio FPL", "en": "FPL price"},
    "market_owned": {"es": "Porcentaje de equipos que lo tienen", "en": "Share of teams that own him"},

    # ── Selección ──
    "intl_eyebrow": {"es": "Selección", "en": "International"},
    "intl_title": {"es": "Campaña internacional 2026", "en": "2026 international campaign"},
    "intl_desc": {
        "es": (
            "Únicos datos que ESPN publica de Anderson: no tiene splits de club ni historial "
            "de partidos. Son {competitions} competiciones y {starts} titularidades en total."
        ),
        "en": (
            "The only Anderson data ESPN publishes: it has no club splits and no gamelog. "
            "{competitions} competitions and {starts} starts in total."
        ),
    },
    "intl_competition": {"es": "Competición", "en": "Competition"},
    "intl_starts": {"es": "Tit.", "en": "Starts"},
    "intl_goals": {"es": "G", "en": "G"},
    "intl_assists": {"es": "A", "en": "A"},
    "intl_shots": {"es": "Tiros", "en": "Shots"},
    "intl_sot": {"es": "A puerta", "en": "On target"},
    "intl_fouls_committed": {"es": "F. com.", "en": "Fouls"},
    "intl_fouls_drawn": {"es": "F. recibidas", "en": "Fouls drawn"},
    "intl_cards": {"es": "TA", "en": "YC"},

    # ── Noticias ──
    "news_eyebrow": {"es": "Hemeroteca", "en": "Coverage"},
    "news_title": {"es": "El traspaso en la prensa", "en": "The transfer in the press"},
    "news_desc": {
        "es": "Noticias del jugador que devuelve ESPN, de la más reciente a la más antigua.",
        "en": "Player news returned by ESPN, most recent first.",
    },
    "news_read": {"es": "Leer en ESPN", "en": "Read on ESPN"},

    # ── Metodología ──
    "method_eyebrow": {"es": "Metodología", "en": "Methodology"},
    "method_title": {"es": "De dónde sale cada dato", "en": "Where each number comes from"},
    "method_fpl": {
        "es": (
            "<strong>Fantasy Premier League</strong> (API oficial y pública). Toda la "
            "estadística de club: minutos, goles, asistencias, xG, xA, entradas, "
            "recuperaciones, precio, propiedad y calendario. Los percentiles los calcula "
            "este proyecto sobre los {sample} centrocampistas con 900 minutos o más."
        ),
        "en": (
            "<strong>Fantasy Premier League</strong> (official public API). All club "
            "statistics: minutes, goals, assists, xG, xA, tackles, recoveries, price, "
            "ownership and fixtures. Percentiles are computed by this project across the "
            "{sample} midfielders with 900 or more minutes."
        ),
    },
    "method_espn": {
        "es": (
            "<strong>ESPN</strong>. Ficha biométrica, splits de selección y noticias. No "
            "publica estadística de club de este jugador."
        ),
        "en": (
            "<strong>ESPN</strong>. Biometrics, international splits and news. It publishes "
            "no club statistics for this player."
        ),
    },
    "method_fotmob": {
        "es": (
            "<strong>FotMob</strong>. Clasificación de la Premier League 2025/26. Su SDK no "
            "expone endpoint de jugador, así que no aporta datos individuales."
        ),
        "en": (
            "<strong>FotMob</strong>. 2025/26 Premier League table. Its SDK exposes no player "
            "endpoint, so it contributes no individual data."
        ),
    },
    # Solo aparece cuando ESPN/FotMob no están disponibles (la build pública): sin
    # esto, la sección de metodología seguiría citando fuentes que no aportaron
    # nada visible en esta build, que es justo lo que este proyecto evita.
    "method_public_note_title": {"es": "Sobre esta build", "en": "About this build"},
    "method_public_note": {
        "es": (
            "Esta build pública muestra sólo lo que sale de la API pública de Fantasy "
            "Premier League. Las secciones de ESPN y FotMob usan un SDK privado por "
            "cuenta que no viaja con el repositorio — no es un fallo de red, es que "
            "esta build no las incluye. Funcionan en la versión local, junto con el "
            "resto del código, en el repositorio."
        ),
        "en": (
            "This public build shows only what comes from the public Fantasy Premier "
            "League API. The ESPN and FotMob sections use a private, per-account SDK "
            "that doesn't ship with the repository — it's not a network failure, this "
            "build simply doesn't include them. They work in the local version, along "
            "with the rest of the code, in the repository."
        ),
    },
    "method_limits_title": {"es": "Límites", "en": "Limits"},
    "method_limits": {
        "es": (
            "El importe del traspaso no procede de ninguna API: lo publica ESPN y aquí va "
            "enlazado a su fuente. Esta página no contiene proyecciones, ratings subjetivos "
            "ni comparaciones con jugadores históricos: todo número que aparece es "
            "verificable en la fuente citada."
        ),
        "en": (
            "The transfer fee comes from no API: ESPN reports it and it is linked to its "
            "source here. This page contains no projections, no subjective ratings and no "
            "comparisons with historical players: every number shown is verifiable at the "
            "cited source."
        ),
    },

    # ── Errores ──
    "error_fpl": {
        "es": "No se pudieron cargar los datos de la Premier League. Detalle: {detail}",
        "en": "Premier League data could not be loaded. Detail: {detail}",
    },
    "error_espn": {
        "es": "ESPN no respondió, así que faltan la ficha, la selección y las noticias. Detalle: {detail}",
        "en": "ESPN did not respond, so biometrics, international data and news are missing. Detail: {detail}",
    },
    "error_fotmob": {
        "es": "FotMob no respondió, así que falta la clasificación. Detalle: {detail}",
        "en": "FotMob did not respond, so the league table is missing. Detail: {detail}",
    },

    # ── Pie ──
    "footer": {
        "es": "Python · Streamlit · Plotly. Datos de Fantasy Premier League, ESPN y FotMob.",
        "en": "Python · Streamlit · Plotly. Data from Fantasy Premier League, ESPN and FotMob.",
    },
    # Variante para cuando ESPN/FotMob no están en la build: el pie no puede decir
    # que hay datos de fuentes que no aportaron nada visible en esta página.
    "footer_fpl_only": {
        "es": "Python · Streamlit · Plotly. Datos de Fantasy Premier League.",
        "en": "Python · Streamlit · Plotly. Data from Fantasy Premier League.",
    },
    "footer_updated": {"es": "Datos leídos en vivo de cada API", "en": "Data read live from each API"},
}


def format_date(value: str | None, lang: str = DEFAULT_LANGUAGE) -> str:
    """Fecha ISO a '23 jul 2026'. Devuelve el valor tal cual si no sabe leerlo,
    que es mejor que tragarse el dato o reventar la página por una fecha rara."""
    if not value:
        return ""
    text = str(value).replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        try:
            parsed = datetime.strptime(text[:10], "%Y-%m-%d")
        except ValueError:
            return str(value)
    months = MONTHS.get(lang, MONTHS[DEFAULT_LANGUAGE])
    return f"{parsed.day} {months[parsed.month - 1]} {parsed.year}"


def t(key: str, lang: str = DEFAULT_LANGUAGE, **fmt) -> str:
    """Texto traducido. Con clave desconocida devuelve la propia clave, que en
    pantalla canta lo suficiente como para detectarlo en cuanto pasa."""
    entry = STRINGS.get(key)
    if entry is None:
        return key
    text = entry.get(lang) or entry.get(DEFAULT_LANGUAGE, key)
    return text.format(**fmt) if fmt else text


def position(raw: str, lang: str = DEFAULT_LANGUAGE) -> str:
    """Traduce la posición que da ESPN. Si aparece una que no conocemos, se muestra
    tal cual en vez de inventar una traducción."""
    key = f"position_{str(raw).strip().lower()}"
    return t(key, lang) if key in STRINGS else str(raw)


def gameweek(raw: str, lang: str = DEFAULT_LANGUAGE) -> str:
    """'Gameweek 3' -> 'Jornada 3'. Sin número reconocible, devuelve el original."""
    digits = "".join(ch for ch in str(raw) if ch.isdigit())
    return t("gameweek", lang, number=digits) if digits else str(raw)

