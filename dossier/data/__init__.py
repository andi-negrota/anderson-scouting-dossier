"""Acceso a datos. Cada modulo expone funciones puras que devuelven dicts/listas.

Ninguno importa Streamlit: el cacheo se aplica desde app.py. Asi la capa de datos
se puede ejecutar y testear sin levantar la web.
"""

from . import espn, fotmob, fpl

__all__ = ["espn", "fotmob", "fpl"]
