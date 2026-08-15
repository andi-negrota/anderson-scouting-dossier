# Elliot Anderson · Informe de scouting

Data app en Streamlit sobre el traspaso de Elliot Anderson del Nottingham Forest al
Manchester City (julio de 2026). Bilingüe (español / inglés).

> Nota: el directorio se sigue llamando `laliga-analytics` por su origen. El proyecto
> ya no tiene nada que ver con LaLiga.

## Qué hace

Construye el perfil del jugador **sólo con datos que publica alguna API**, y calcula
sus percentiles reales frente a los 126 centrocampistas de la Premier League con 900
minutos o más en la temporada 2025/26.

Secciones: cifras de la temporada, radar de percentiles, rankings oficiales, curva de
progresión de seis temporadas, comparación Forest/City en la tabla, calendario con
dificultad, precio y propiedad en FPL, campaña internacional, hemeroteca y metodología.

## Fuentes

| Fuente | Qué aporta |
| --- | --- |
| **Fantasy Premier League** (API pública) | Toda la estadística de club: minutos, goles, asistencias, xG, xA, entradas, recuperaciones, precio, propiedad y calendario |
| **ESPN** (vía Parse SDK) | Ficha biométrica, splits de selección y noticias del jugador |
| **FotMob** (vía Parse SDK) | Clasificación de la Premier League 2025/26 |

Dos límites conocidos, documentados también dentro de la propia web:

- ESPN **no publica estadística de club** de este jugador, sólo internacional. Su
  `gamelog` viene vacío. Por eso los datos de club salen de FPL.
- El SDK de FotMob **no expone endpoint de jugador** (`league`, `leagues`, `match`,
  `matches`), así que aporta contexto de competición y nada individual.
- El **importe del traspaso** no lo publica ninguna API. La cifra que aparece (£116M)
  es la que informa ESPN y está enlazada a su fuente.

## Dirección visual

**Telemetría de banquillo.** La página se lee como el panel de instrumentos de un
banquillo bajo focos, no como un cuadro de mando genérico. Cada decisión sale del
tema, no de una paleta bonita:

| Elemento | Decisión | Por qué |
| --- | --- | --- |
| Superficie | `#08110C`, verde-negro de césped nocturno | No es un gris neutro: es el campo de noche |
| Acento | `#FFB000`, ámbar de monitor CRT, **único** | Un solo acento; el rojo queda reservado a avisos de dato |
| Tipografía | Sólo IBM Plex (Sans Condensed + Mono) | Una familia de ingeniería, no el trío de moda |
| Bordes | Radio 0 en toda la página, sin degradados | Los instrumentos no tienen esquinas redondeadas |
| Divisores | Línea de medio campo con su círculo central | Marca de campo, no una raya decorativa |
| Percentiles | Vúmetro de 20 segmentos | Cada segmento vale 5 puntos: se puede contar, no sólo estimar |
| Dificultad del rival | 5 marcas de las que se encienden las que toca | La escala oficial es 1-5; no hace falta traducirla a un color |
| Secciones | `FORMA nn` + fuente del dato en la cabecera | La procedencia sostiene toda la página, así que va en el encabezado |

Contrastes medidos sobre la superficie, no estimados a ojo: la peor combinación de
texto de la página está en **7,15:1** (WCAG AA exige 4,5:1; AAA, 7:1).

## La pieza 3D

Los 126 centrocampistas colocados por tres tasas por 90 (recuperaciones, xA, xG),
con Anderson destacado. Tres detalles que no son adorno:

- **Las marcas de campo del suelo son datos.** El "círculo central" es la región
  intercuartílica del grupo y la "línea de medio campo" son sus medianas. Una elipse
  dibujada en un espacio de datos se lee como información, así que es información.
- **El sujeto se codifica por cuatro canales** (tono, tamaño, etiqueta directa y línea
  de caída al suelo). Sólo con el tono, la separación de luminancia contra la nube
  sería de 1,46:1; la nube va al 38% de opacidad para subirla a ~5,6:1.
- **La lectura exacta vive en una tabla debajo.** En tres dimensiones se estima una
  posición, no se lee un valor.

La trayectoria son **dos paneles apilados y no un gráfico de doble eje**: alinear dos
escalas distintas en un mismo dibujo inventa una correlación que no está en los datos.

## Estructura

```
app.py                      orquestación y render (sin lógica de datos)
dossier/
    data/fpl.py             API de Fantasy Premier League, percentiles, nube 3D
    data/espn.py            perfil, splits internacionales, noticias
    data/fotmob.py          clasificación de la Premier
    i18n.py                 todos los textos, en español e inglés
    theme.py                paleta, contrastes medidos y CSS
    components.py           piezas del panel, con escapado de HTML
    charts.py               figuras de Plotly
tests/test_dossier.py       percentiles, i18n, escapado y render en ambos idiomas
```

La capa de datos **no importa Streamlit**: se puede ejecutar y probar sin levantar la
web. El cacheo (`st.cache_data`) se aplica desde `app.py`.

## Pruebas

```bash
.venv/Scripts/python -m pytest tests -v
```

## Ejecutar

```bash
uv sync
uv run streamlit run app.py
```

O con el venv del proyecto:

```bash
.venv/Scripts/streamlit run app.py
```

## Servidor MCP

`.mcp.json` declara el servidor `fantasy-pl` (paquete `fpl-mcp`), que expone los datos
de Fantasy Premier League como herramientas MCP. Es una ayuda para explorar los datos
desde el agente; **la web no depende de él**: `dossier/data/fpl.py` llama directamente
a la API pública.

## Criterio editorial

La página no contiene proyecciones, ratings subjetivos ni comparaciones con jugadores
históricos. Todo número que aparece es verificable en la fuente citada, y donde una
fuente no llega, la web lo dice en lugar de rellenarlo.
