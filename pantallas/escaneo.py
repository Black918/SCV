import flet as ft
import config_colors as theme

def vista_escaneo(page: ft.Page):
    vuelo_actual = ft.Text("Sin vuelo activo", size=13, color=theme.c("MUTED"))

    productos_escaneados = ft.ListView(
        expand=True,
        spacing=8,
        padding=ft.Padding(left=8, top=8, right=8, bottom=8),
    )

    campo_sku = ft.TextField(
        label="SKU / Código de barras",
        hint_text="Escanea o escribe el código",
        bgcolor=theme.c("CARD_BG"),
        border_color=theme.c("ACCENT"),
        focused_border_color=theme.c("ACCENT"),
        color=theme.c("TEXT_MAIN"),
        prefix_icon=ft.Icons.QR_CODE_SCANNER,
        expand=True,
    )

    def agregar_mock(e):
        if campo_sku.value.strip():
            productos_escaneados.controls.append(
                ft.Container(
                    padding=ft.Padding(left=14, top=10, right=14, bottom=10),
                    border_radius=8,
                    bgcolor=theme.c("CARD_BG"),
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color=theme.c("ACCENT"), size=18),
                            ft.Text(campo_sku.value.strip(),
                                    color=theme.c("TEXT_MAIN"), size=14, expand=True),
                            ft.Text("x1", color=theme.c("MUTED"), size=13),
                        ]
                    )
                )
            )
            campo_sku.value = ""
            page.update()

    # --- BOTÓN CORREGIDO (Sin el argumento 'text' para evitar errores) ---
    btn_cerrar = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.PICTURE_AS_PDF, size=20),
                ft.Text("Cerrar Vuelo y Generar Reporte", size=14, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ),
        bgcolor=theme.c("BUTTON_BG"),
        color=theme.c("BUTTON_TEXT"),
        width=400,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )

    return ft.Column(
        controls=[
            ft.Container(height=10),
                ft.Text("Escaneo de Productos", size=20,
                    weight=ft.FontWeight.BOLD, color=theme.c("TEXT_MAIN")),
                ft.Divider(color=theme.c("ACCENT"), thickness=1),

            # Vuelo activo
            ft.Container(
                padding=ft.Padding(left=16, top=10, right=16, bottom=10),
                border_radius=10,
                bgcolor=theme.c("BUTTON_BG"),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.FLIGHT, color=theme.c("ACCENT")),
                        ft.Text("Vuelo activo: ", color=theme.c("MUTED"), size=13),
                        vuelo_actual,
                    ]
                )
            ),

            ft.Container(height=8),

            # Área de cámara (placeholder)
            ft.Container(
                height=180,
                border_radius=12,
                bgcolor=theme.c("CARD_BG"),
                border=ft.Border(
                    left=ft.BorderSide(width=2, color=theme.c("CARD_BORDER")),
                    top=ft.BorderSide(width=2, color=theme.c("CARD_BORDER")),
                    right=ft.BorderSide(width=2, color=theme.c("CARD_BORDER")),
                    bottom=ft.BorderSide(width=2, color=theme.c("CARD_BORDER")),
                ),
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.CAMERA_ALT_OUTLINED,
                                size=50, color=theme.c("ACCENT")+"50" if theme.c("ACCENT") else None),
                        ft.Text("Cámara — próximamente",
                                color=theme.c("MUTED"), size=13),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),

            ft.Container(height=8),

            # Input manual
            ft.Row(
                controls=[
                    campo_sku,
                    ft.IconButton(
                        icon=ft.Icons.ADD_CIRCLE,
                        icon_color=theme.c("ACCENT"),
                        icon_size=32,
                        tooltip="Agregar producto",
                        on_click=agregar_mock,
                    ),
                ]
            ),

            ft.Text("Productos escaneados:", size=13, color=theme.c("MUTED")),

            ft.Container(
                expand=True,
                border_radius=10,
                bgcolor=theme.c("CARD_BG"),
                padding=ft.Padding(left=6, top=6, right=6, bottom=6),
                content=productos_escaneados,
            ),

            # Área del botón inferior
            ft.Container(
                content=ft.Row([btn_cerrar], alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.Padding(top=10, bottom=20, left=0, right=0)
            ),
        ],
        spacing=10,
        expand=True,
    )