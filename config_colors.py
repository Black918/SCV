"""Paleta de colores centralizada - Paleta 1: Profesional Alta Visibilidad
Usar este archivo para mantener consistencia de colores en la app.
"""

PALETTE = {
    # Fondo y tarjetas
    "BACKGROUND": "#FFFFFF",
    "CARD_BG": "#FFFFFF",
    "CARD_BORDER": "#EAECEF",

    # Textos
    "TEXT_MAIN": "#24292E",
    "TITLE": "#0366D6",

    # Acentos y botones
    "ACCENT": "#00C3E3",
    "ICON_INACTIVE": "#6A737D",
    "BUTTON_BG": "#0366D6",
    "BUTTON_TEXT": "#FFFFFF",

    # Soportes/neutral
    "MUTED": "#6A737D",
}

def c(key):
    return PALETTE.get(key)
