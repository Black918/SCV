import flet as ft
import config_colors as theme
from pantallas.inicio import vista_inicio
from pantallas.escaneo import vista_escaneo
from pantallas.voz_pantalla import vista_voz
from pantallas.reportes import vista_reportes

async def main(page: ft.Page):
    # ── Configuración general ────────────────────────────────────────
    page.title = "SCV — Kalan"
    # Usar la paleta centralizada
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = theme.c("BACKGROUND")
    page.padding = 0

    # ── Función para navegar entre pantallas ─────────────────────────
    # Esta función cambia el contenido del contenedor central
    async def navegar(vista_fn, e=None):
        try:
            # Si volvemos al inicio, le pasamos la función navegar para las tarjetas
            if vista_fn == vista_inicio:
                contenido.content = vista_fn(page, on_navigate=navegar)
            else:
                # Para el resto de pantallas (escaneo, voz, etc.)
                contenido.content = vista_fn(page)
        except Exception as ex:
            print(f"Error al navegar: {ex}")
            # Fallback en caso de error de argumentos
            contenido.content = vista_fn(page)
            
        await page.close_drawer()
        page.update()

    # ── Área de contenido central ────────────────────────────────────
    # Iniciamos con la vista de inicio y le inyectamos la función navegar
    contenido = ft.Container(
        expand=True,
        padding=ft.Padding(left=20, top=10, right=20, bottom=10),
        content=vista_inicio(page, on_navigate=navegar),
    )

    # ── Elementos del menú lateral ───────────────────────────────────
    def item_menu(icono, texto, vista_fn):
        return ft.ListTile(
            leading=ft.Icon(icono, color=theme.c("ACCENT")),
            title=ft.Text(texto, color=theme.c("TEXT_MAIN"), size=14),
            hover_color=theme.c("CARD_BORDER"),
            # Usamos run_task porque 'navegar' es una función async.
            # Pasamos también el evento `e` por si la vista lo necesita.
            on_click=lambda e, fn=vista_fn: page.run_task(navegar, fn, e),
        )

    # ── Drawer (Menú Lateral) ────────────────────────────────────────
    drawer = ft.NavigationDrawer(
        bgcolor=theme.c("CARD_BG"),
        controls=[
            ft.Container(
                padding=ft.Padding(left=20, top=24, right=20, bottom=24),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.FLIGHT_TAKEOFF, color=theme.c("ACCENT"), size=32),
                        ft.Column(
                            controls=[
                                ft.Text("SCV", size=20, weight=ft.FontWeight.BOLD, color=theme.c("TITLE")),
                                ft.Text("Sistema de Control de Vuelos", size=11, color=theme.c("MUTED")),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=12,
                ),
            ),
            ft.Divider(color=theme.c("CARD_BORDER"), thickness=1),
            item_menu(ft.Icons.HOME_OUTLINED,   "Inicio",              vista_inicio),
            item_menu(ft.Icons.QR_CODE_SCANNER, "Escaneo",              vista_escaneo),
            item_menu(ft.Icons.MIC_OUTLINED,    "Movimientos por Voz", vista_voz),
            item_menu(ft.Icons.PICTURE_AS_PDF,  "Reportes",            vista_reportes),
            ft.Divider(color=theme.c("CARD_BORDER"), thickness=1),
            ft.Container(
                padding=ft.Padding(left=20, top=10, right=20, bottom=10),
                content=ft.Text("v1.0  ·  Kalan Project", size=11, color=theme.c("MUTED")),
            ),
        ],
    )

    page.drawer = drawer

    # ── Función para abrir el menú ───────────────────────────────────
    async def abrir_menu(e):
        # Mostrar el drawer de forma correcta usando la API async de Flet
        # (esto abre el menú desplegable en la esquina superior izquierda)
        await page.show_drawer()
        # No es estrictamente necesario llamar a page.update() después
        # de show_drawer(), pero lo dejamos para forzar refresco si hace falta.
        page.update()

    # ── AppBar (Barra Superior) ──────────────────────────────────────
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            icon_color=theme.c("BUTTON_TEXT"),
            on_click=abrir_menu,
        ),
        leading_width=48,
        title=ft.Text(
            "SCV — Kalan",
            color=theme.c("BUTTON_TEXT"),
            weight=ft.FontWeight.BOLD,
            size=17,
        ),
        bgcolor=theme.c("BUTTON_BG"),
        actions=[
            ft.IconButton(
                icon=ft.Icons.FLIGHT_TAKEOFF,
                icon_color=theme.c("ACCENT"),
                tooltip="Vuelo activo",
            ),
        ],
    )

    # Agregar el contenedor principal a la página
    page.add(contenido)

# Ejecución de la aplicación
if __name__ == "__main__":
    # Intentar abrir en navegador si la constante está disponible en esta
    # instalación de Flet; si no, probar con el identificador string y
    # finalmente volver a `ft.run(main)` como fallback.
    try:
        # Intentar ejecutar en navegador (cadena compatible con distintas versiones)
        ft.app(target=main, view="web_browser")
    except Exception:
        # Fallback a modo escritorio para instalaciones antiguas
        ft.run(main)
#aqui un cambio