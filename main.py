import flet as ft
from pantallas.inicio import vista_inicio
from pantallas.escaneo import vista_escaneo
from pantallas.voz_pantalla import vista_voz
from pantallas.reportes import vista_reportes


async def main(page: ft.Page):
    # ── Configuración general ────────────────────────────────────────
    page.title = "SCV — Kalan"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0A0A1A"
    page.padding = 0

    # ── Área de contenido central ────────────────────────────────────
    contenido = ft.Container(
        expand=True,
        padding=ft.Padding(left=20, top=10, right=20, bottom=10),
        content=vista_inicio(page),
    )

    # ── Función para navegar entre pantallas ─────────────────────────
    async def navegar(vista_fn, e=None):
        contenido.content = vista_fn(page)
        await page.close_drawer()
        page.update()

    # ── Elementos del menú lateral ───────────────────────────────────
    def item_menu(icono, texto, vista_fn):
        return ft.ListTile(
            leading=ft.Icon(icono, color="#00B4D8"),
            title=ft.Text(texto, color="white", size=14),
            hover_color="#1E1E2E",
            on_click=lambda e, fn=vista_fn: page.run_task(navegar, fn, e),
        )

    # ── Drawer ───────────────────────────────────────────────────────
    drawer = ft.NavigationDrawer(
        bgcolor="#12121F",
        controls=[
            ft.Container(
                padding=ft.Padding(left=20, top=24, right=20, bottom=24),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.FLIGHT_TAKEOFF, color="#00B4D8", size=32),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "SCV",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color="white",
                                ),
                                ft.Text(
                                    "Sistema de Control de Vuelos",
                                    size=11,
                                    color="#AAAAAA",
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=12,
                ),
            ),
            ft.Divider(color="#333344", thickness=1),
            item_menu(ft.Icons.HOME_OUTLINED,   "Inicio",              vista_inicio),
            item_menu(ft.Icons.QR_CODE_SCANNER, "Escaneo",             vista_escaneo),
            item_menu(ft.Icons.MIC_OUTLINED,    "Movimientos por Voz", vista_voz),
            item_menu(ft.Icons.PICTURE_AS_PDF,  "Reportes",            vista_reportes),
            ft.Divider(color="#333344", thickness=1),
            ft.Container(
                padding=ft.Padding(left=20, top=10, right=20, bottom=10),
                content=ft.Text("v1.0  ·  Kalan Project", size=11, color="#444466"),
            ),
        ],
    )

    page.drawer = drawer

    # ── Función para abrir el menú ───────────────────────────────────
    async def abrir_menu(e):
        await page.show_drawer()

    # ── AppBar ───────────────────────────────────────────────────────
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            icon_color="white",
            on_click=abrir_menu,
        ),
        leading_width=48,
        title=ft.Text(
            "SCV — Kalan",
            color="white",
            weight=ft.FontWeight.BOLD,
            size=17,
        ),
        bgcolor="#12121F",
        actions=[
            ft.IconButton(
                icon=ft.Icons.FLIGHT_TAKEOFF,
                icon_color="#00B4D8",
                tooltip="Vuelo activo",
            ),
        ],
    )

    page.add(contenido)


ft.app(target=main)