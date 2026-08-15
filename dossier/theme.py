"""Dirección: telemetría de banquillo.

La página se lee como el panel de instrumentos de un banquillo bajo focos, no como
un cuadro de mando. De ahí vienen las decisiones, y ninguna es decorativa:

  · La superficie es verde-negro de césped nocturno, no un gris neutro.
  · Un solo acento, ámbar de monitor CRT. El rojo queda reservado para avisos de dato.
  · Cero radios de esquina y cero degradados: los instrumentos no los tienen.
  · Los divisores son marcas de campo (línea de medio campo con su círculo central).
  · Las barras de percentil son segmentadas, como un vúmetro, no barras redondeadas.

Tipografía: sólo IBM Plex, que es una familia de ingeniería. Condensada para
titulares y cifras de portada; monoespaciada para todo dato tabular. Las cifras de
portada van en la condensada y no en la monoespaciada a propósito: los dígitos de
ancho fijo se ven sueltos a tamaño grande, y sólo aportan donde hay que alinear
columnas.

Contrastes medidos sobre la superficie #08110C (WCAG):
    #E9EFE6  16,38:1  AAA    tinta principal
    #FFB000  10,46:1  AAA    acento y sujeto
    #8FA394   7,15:1  AAA    tinta secundaria y nube de contexto
    #FF3B30   5,40:1  AA     avisos
"""

from __future__ import annotations

PITCH = "#08110C"       # césped nocturno: la superficie
PITCH_RISE = "#0D1712"  # banda alterna de fila
CHALK = "#E9EFE6"       # tiza: tinta principal y marcas de campo
CHALK_DIM = "#8FA394"   # tiza apagada: secundaria y nube de contexto
AMBER = "#FFB000"       # ámbar CRT: acento único, el sujeto
SIGNAL = "#FF3B30"      # rojo de señal: sólo avisos de dato
RULE = "rgba(233,239,230,0.16)"

# Opacidad de la nube de contexto en la pieza 3D. No es estética: a plena opacidad
# el sujeto ámbar y la nube quedan a 1,46:1 de luminancia. Rebajándola, la
# separación sube a ~5,6:1 sin tocar el tono.
CLOUD_ALPHA = 0.38


def meter_color(percentile: float) -> str:
    """Un percentil no es una categoría: es magnitud. Por eso un solo tono, y la
    intensidad hace el trabajo. Bajo, la barra apenas se enciende."""
    if percentile >= 90:
        return AMBER
    if percentile >= 60:
        return "rgba(255,176,0,0.78)"
    if percentile >= 30:
        return "rgba(255,176,0,0.52)"
    return "rgba(143,163,148,0.7)"


CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans+Condensed:wght@400;500;600;700&display=swap');

/* ── El armazón de Streamlit no forma parte del diseño ── */
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stHeader"],
[data-testid="stAppDeployButton"],
.stAppDeployButton,
#MainMenu, header, footer {{ display: none !important; }}

:root {{
    --pitch: {PITCH};
    --pitch-rise: {PITCH_RISE};
    --chalk: {CHALK};
    --chalk-dim: {CHALK_DIM};
    --amber: {AMBER};
    --signal: {SIGNAL};
    --rule: {RULE};
    --mono: 'IBM Plex Mono', ui-monospace, monospace;
    --cond: 'IBM Plex Sans Condensed', 'Arial Narrow', sans-serif;
}}

* {{ box-sizing: border-box; border-radius: 0 !important; }}

.stApp {{
    background: var(--pitch);
    /* Un solo gesto atmosférico: el halo de los focos sobre el campo. */
    background-image: radial-gradient(ellipse 900px 520px at 50% -8%,
        rgba(233,239,230,0.055) 0%, rgba(233,239,230,0) 70%);
    background-repeat: no-repeat;
}}
.stMainBlockContainer {{ max-width: 1240px; }}
.block-container {{ padding: 0 2rem 4rem !important; }}
p {{ margin: 0; }}

::-webkit-scrollbar {{ width: 10px; }}
::-webkit-scrollbar-track {{ background: var(--pitch); }}
::-webkit-scrollbar-thumb {{ background: #24332A; border: 3px solid var(--pitch); }}

/* Streamlit pinta los enlaces de su azul con más especificidad que un `a` a secas.
   Un solo acento en toda la página, y el acento es el ámbar. */
.stApp a, .stApp a:visited,
[data-testid="stMarkdownContainer"] a {{
    color: var(--amber) !important; text-decoration: none;
}}
.stApp a:hover {{ text-decoration: underline; }}
a:focus-visible, button:focus-visible, [role="radio"]:focus-visible,
[data-testid="stSegmentedControl"] button:focus-visible {{
    outline: 2px solid var(--amber);
    outline-offset: 2px;
}}

/* ── Raíl superior: identificación del sujeto, siempre visible ── */
.rail {{
    display: flex; align-items: center; gap: 1.25rem; flex-wrap: wrap;
    border-bottom: 1px solid var(--rule);
    padding: 0.7rem 0; margin-bottom: 2rem;
    font-family: var(--mono); font-size: 0.72rem; font-weight: 500;
    letter-spacing: 0.16em; text-transform: uppercase; color: var(--chalk-dim);
}}
.rail-live {{ color: var(--amber); }}
.rail-live::before {{
    content: ''; display: inline-block; width: 6px; height: 6px;
    background: var(--amber); margin-right: 0.5rem; vertical-align: 1px;
}}
.rail-sep {{ flex: 1; height: 1px; background: var(--rule); }}

/* ── Cabecera de sección: el número de forma y la fuente del dato ── */
.form-head {{ margin: 3.5rem 0 1.25rem; }}
.form-meta {{
    display: flex; align-items: center; gap: 1rem;
    font-family: var(--mono); font-size: 0.7rem; font-weight: 600;
    letter-spacing: 0.2em; text-transform: uppercase; color: var(--chalk-dim);
}}
.form-meta .rule {{ flex: 1; height: 1px; background: var(--rule); }}
.form-no {{ color: var(--amber); }}
.form-title {{
    font-family: var(--cond); font-size: clamp(1.6rem, 3.4vw, 2.5rem);
    font-weight: 700; text-transform: uppercase; letter-spacing: -0.01em;
    line-height: 1.05; color: var(--chalk); margin: 0.55rem 0 0;
}}
.stApp h2.form-title {{
    font-family: var(--cond); font-size: clamp(1.6rem, 3.4vw, 2.5rem);
    font-weight: 700; text-transform: uppercase; letter-spacing: -0.01em;
    line-height: 1.05; color: var(--chalk); margin: 0.55rem 0 0; padding: 0;
}}
.form-desc {{
    font-family: var(--cond); font-size: 1rem; font-weight: 400; line-height: 1.55;
    color: var(--chalk-dim); max-width: 68ch; margin-top: 0.5rem;
}}
.form-desc strong {{ color: var(--chalk); font-weight: 600; }}

/* ── Portada ── */
.hero {{ padding: 0.5rem 0 0; }}
.hero-name {{
    font-family: var(--cond); font-weight: 700; text-transform: uppercase;
    font-size: clamp(3.2rem, 11vw, 8.5rem); line-height: 0.84;
    letter-spacing: -0.035em; color: var(--chalk); margin: 0;
}}
.stApp h1.hero-name {{
    font-family: var(--cond); font-weight: 700; text-transform: uppercase;
    font-size: clamp(3.2rem, 11vw, 8.5rem); line-height: 0.84;
    letter-spacing: -0.035em; color: var(--chalk); margin: 0; padding: 0;
}}
.hero-given {{ display: block; color: var(--chalk-dim); font-weight: 400; }}
.hero-strip {{
    display: flex; align-items: baseline; gap: 1.5rem; flex-wrap: wrap;
    border-top: 1px solid var(--rule); margin-top: 1.5rem; padding-top: 0.85rem;
    font-family: var(--mono); font-size: 0.78rem; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--chalk-dim);
}}

/* El traspaso, dibujado como un pase: origen, trayectoria, destino. */
.move {{
    display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;
    margin-top: 1.75rem;
    font-family: var(--mono); font-size: 0.85rem; letter-spacing: 0.1em;
    text-transform: uppercase;
}}
.move-from {{ color: var(--chalk-dim); }}
.move-to {{ color: var(--chalk); font-weight: 600; }}
.move-path {{
    flex: 1; min-width: 60px; height: 1px; background: var(--rule);
    position: relative; max-width: 220px;
}}
.move-path::after {{
    content: ''; position: absolute; right: -1px; top: -3px;
    border-left: 7px solid var(--amber);
    border-top: 3.5px solid transparent; border-bottom: 3.5px solid transparent;
}}
.move-fee {{
    font-family: var(--cond); font-size: 1.5rem; font-weight: 700;
    color: var(--amber); letter-spacing: 0;
}}

/* ── Lecturas de instrumento: la cifra manda, la etiqueta sirve ── */
.readouts {{
    display: grid; grid-template-columns: repeat(6, 1fr);
    border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule);
    margin: 1.5rem 0;
}}
.readout {{ padding: 1.1rem 1rem; border-left: 1px solid var(--rule); }}
.readout:first-child {{ border-left: none; }}
.readout-label {{
    font-family: var(--mono); font-size: 0.72rem; font-weight: 500;
    letter-spacing: 0.14em; text-transform: uppercase; color: var(--chalk-dim);
}}
.readout-value {{
    font-family: var(--cond); font-size: 2.5rem; font-weight: 700;
    line-height: 1; color: var(--chalk); margin-top: 0.4rem;
    font-variant-numeric: proportional-nums;
}}
.readout-value.is-subject {{ color: var(--amber); }}
.readout-sub {{
    font-family: var(--mono); font-size: 0.7rem; color: var(--chalk-dim);
    margin-top: 0.35rem; letter-spacing: 0.04em;
}}

/* ── Vúmetro de percentiles ── */
.meter-row {{
    display: grid; grid-template-columns: minmax(150px, 1.5fr) 68px 1fr 74px;
    align-items: center; gap: 1rem; padding: 0.55rem 0;
    border-bottom: 1px solid var(--rule);
}}
.meter-row.head {{ border-bottom-color: var(--chalk-dim); }}
.meter-label {{
    font-family: var(--mono); font-size: 0.78rem; color: var(--chalk);
    letter-spacing: 0.02em;
}}
.meter-head {{
    font-family: var(--mono); font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.14em; text-transform: uppercase; color: var(--chalk-dim);
}}
.meter-value {{
    font-family: var(--mono); font-size: 0.8rem; color: var(--chalk);
    text-align: right; font-variant-numeric: tabular-nums;
}}
.meter-rank {{
    font-family: var(--mono); font-size: 0.74rem; color: var(--chalk-dim);
    text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap;
}}
/* Segmentos separados por hueco de superficie, no por borde. */
.meter {{ display: flex; gap: 2px; height: 12px; align-items: stretch; }}
.meter span {{ flex: 1; background: rgba(143,163,148,0.16); }}

/* ── Tablas ──
   Una tabla de nueve columnas no cabe en un móvil. Antes que apretar el texto hasta
   que se rompa, la tabla se desplaza dentro de su propio contenedor y la página no. */
.table-scroll {{ overflow-x: auto; }}
.row {{
    display: grid; align-items: center; gap: 0.5rem; padding: 0.5rem 0.75rem;
    border-bottom: 1px solid var(--rule);
    font-family: var(--mono); font-size: 0.8rem; color: var(--chalk);
    font-variant-numeric: tabular-nums;
}}
.row:nth-child(even) {{ background: var(--pitch-rise); }}
.row.head {{
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--chalk-dim);
    background: transparent; border-bottom-color: var(--chalk-dim);
}}
.row .num {{ text-align: right; }}
.row .subject {{ color: var(--amber); font-weight: 600; }}

/* ── Calendario: tira de partidos, no tarjetas ── */
.fixtures {{
    display: grid; grid-template-columns: repeat(6, 1fr);
    border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule);
}}
.fixture {{ padding: 0.9rem 0.75rem; border-left: 1px solid var(--rule); }}
.fixture:first-child {{ border-left: none; }}
.fixture-gw {{
    font-family: var(--mono); font-size: 0.72rem; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--chalk-dim);
}}
.fixture-opp {{
    font-family: var(--cond); font-size: 1.15rem; font-weight: 600;
    text-transform: uppercase; color: var(--chalk); margin: 0.3rem 0 0.15rem;
    line-height: 1.1;
}}
.fixture-venue {{
    font-family: var(--mono); font-size: 0.7rem; color: var(--chalk-dim);
    letter-spacing: 0.08em; text-transform: uppercase;
}}
/* La dificultad se codifica en pasos, no en color: cinco marcas, se llenan las que toca. */
.diff {{ display: flex; gap: 2px; margin-top: 0.6rem; }}
.diff span {{ height: 3px; flex: 1; background: rgba(143,163,148,0.2); }}
.diff span.on {{ background: var(--amber); }}

/* ── Alarma: cuando una fuente falla ──
   Es el único sitio donde aparece el rojo de señal. Si el rojo se usara para
   decorar, dejaría de avisar de nada. */
[data-testid="stAlert"] {{
    background: rgba(255,59,48,0.07) !important;
    border: none !important;
    border-left: 2px solid var(--signal) !important;
    padding: 0.85rem 1.1rem !important;
}}
[data-testid="stAlert"] p {{
    font-family: var(--cond) !important; font-size: 0.92rem !important;
    color: var(--chalk) !important;
}}
[data-testid="stAlert"] svg {{ fill: var(--signal) !important; color: var(--signal) !important; }}

/* ── Aviso de contexto ── */
.notice {{
    border-left: 2px solid var(--amber); padding: 0.9rem 0 0.9rem 1.1rem;
    margin: 1.5rem 0; background: rgba(255,176,0,0.045);
}}
.notice-title {{
    font-family: var(--mono); font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.18em; text-transform: uppercase; color: var(--amber);
}}
.notice-body {{
    font-family: var(--cond); font-size: 0.95rem; line-height: 1.6;
    color: var(--chalk-dim); margin-top: 0.4rem; max-width: 72ch;
}}
.notice-body strong {{ color: var(--chalk); font-weight: 600; }}

/* ── Lectura destacada ── */
.verdict {{
    border-top: 1px solid var(--chalk-dim); border-bottom: 1px solid var(--chalk-dim);
    padding: 1.5rem 0; margin: 1.5rem 0;
}}
.verdict p {{
    font-family: var(--cond); font-size: clamp(1.05rem, 2vw, 1.35rem);
    line-height: 1.5; color: var(--chalk-dim); max-width: 76ch;
}}
.verdict strong {{ color: var(--chalk); font-weight: 600; }}
.verdict em {{ color: var(--amber); font-style: normal; font-weight: 600; }}

/* ── Hemeroteca ── */
.news {{ border-bottom: 1px solid var(--rule); padding: 1rem 0; }}
.news-date {{
    font-family: var(--mono); font-size: 0.72rem; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--chalk-dim);
}}
.news-head {{
    font-family: var(--cond); font-size: 1.15rem; font-weight: 600;
    color: var(--chalk); line-height: 1.25; margin: 0.3rem 0;
}}
.news-desc {{
    font-family: var(--cond); font-size: 0.92rem; line-height: 1.55;
    color: var(--chalk-dim); max-width: 76ch;
}}
.news-link {{
    font-family: var(--mono); font-size: 0.72rem; letter-spacing: 0.1em;
    text-transform: uppercase;
}}

/* ── Metodología ── */
.method {{ border-top: 1px solid var(--rule); padding: 1rem 0 0; }}
.method-src {{
    font-family: var(--mono); font-size: 0.7rem; font-weight: 600;
    letter-spacing: 0.18em; text-transform: uppercase; color: var(--amber);
}}
.method p {{
    font-family: var(--cond); font-size: 0.92rem; line-height: 1.6;
    color: var(--chalk-dim); margin-top: 0.5rem;
}}
.method strong {{ color: var(--chalk); font-weight: 600; }}

/* ── Divisor: línea de medio campo con su círculo central ── */
.halfway {{
    position: relative; height: 1px; background: var(--rule);
    margin: 3.5rem 0 0; overflow: visible;
}}
.halfway::after {{
    content: ''; position: absolute; left: 50%; top: 50%;
    width: 46px; height: 46px; transform: translate(-50%, -50%);
    border: 1px solid var(--rule);
    border-radius: 50% !important;
}}

.footer {{
    border-top: 1px solid var(--rule); margin-top: 3.5rem; padding-top: 1.25rem;
    display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
    font-family: var(--mono); font-size: 0.7rem; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--chalk-dim);
}}

/* ── Selector de idioma, vestido de conmutador ──
   El texto vive en un <p> dentro del botón, así que hay que llegar hasta él o se
   queda con la tipografía por defecto de Streamlit. El gancho es `.st-key-lang`,
   que Streamlit genera a partir de la clave del widget y no cambia entre versiones
   como sí lo hacen las clases de emotion. */
.st-key-lang button {{
    background: transparent !important;
    border: 1px solid var(--rule) !important;
    color: var(--chalk-dim) !important;
    padding: 0.3rem 0.75rem !important;
    min-height: 0 !important;
}}
.st-key-lang button p {{
    font-family: var(--mono) !important; font-size: 0.72rem !important;
    font-weight: 500 !important; letter-spacing: 0.14em !important;
    text-transform: uppercase !important; color: inherit !important;
}}
.st-key-lang button:hover {{ border-color: var(--chalk-dim) !important; }}
.st-key-lang [data-testid="stBaseButton-segmented_controlActive"] {{
    border-color: var(--amber) !important;
    color: var(--amber) !important;
    background: rgba(255,176,0,0.08) !important;
}}

@media (max-width: 1000px) {{
    .readouts {{ grid-template-columns: repeat(3, 1fr); }}
    .readout:nth-child(4) {{ border-left: none; }}
    .readouts .readout:nth-child(-n+3) {{ border-bottom: 1px solid var(--rule); }}
    .fixtures {{ grid-template-columns: repeat(3, 1fr); }}
    .fixture:nth-child(4) {{ border-left: none; }}
}}
@media (max-width: 640px) {{
    .block-container {{ padding: 0 1rem 2.5rem !important; }}
    .readouts, .fixtures {{ grid-template-columns: repeat(2, 1fr); }}
    .readout:nth-child(odd), .fixture:nth-child(odd) {{ border-left: none; }}
    .meter-row {{ grid-template-columns: 1fr 60px; row-gap: 0.4rem; }}
    .meter-row .meter {{ grid-column: 1 / -1; }}
    .meter-rank {{ grid-column: 1 / -1; text-align: left; }}
    .hero-strip {{ gap: 0.75rem; font-size: 0.72rem; }}
    .table-scroll .row {{ min-width: 540px; }}
}}

@media (prefers-reduced-motion: reduce) {{
    * {{ animation: none !important; transition: none !important; }}
}}
</style>
"""
