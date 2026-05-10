import flet as ft

def vista_reportes(page: ft.Page):

    vuelos_mock = [
        {"numero": "AM452", "estado": "cerrado", "fecha": "08/05/2025"},
        {"numero": "AM118", "estado": "abierto",  "fecha": "08/05/2025"},
        {"numero": "AM309", "estado": "cerrado", "fecha": "07/05/2025"},
    ]

    def color_estado(estado):
        return "#00B4D8" if estado == "abierto" else "#AAAAAA"

    tarjetas = []
    for v in vuelos_mock:
        tarjetas.append(
            ft.Container(
                padding=ft.Padding(left=14, top=14, right=14, bottom=14),
                border_radius=10,
                bgcolor="#1E1E2E",
                border=ft.Border(
                    left=ft.BorderSide(width=1, color=color_estado(v["estado"])),
                    top=ft.BorderSide(width=1, color=color_estado(v["estado"])),
                    right=ft.BorderSide(width=1, color=color_estado(v["estado"])),
                    bottom=ft.BorderSide(width=1, color=color_estado(v["estado"])),
                ),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.FLIGHT, color=color_estado(v["estado"])),
                        ft.Column(
                            controls=[
                                ft.Text(f"Vuelo {v['numero']}",
                                        color="white",
                                        weight=ft.FontWeight.BOLD, size=14),
                                ft.Text(v["fecha"], color="#AAAAAA", size=12),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Chip(
                            # Estilizar el texto directamente en `ft.Text` porque
                            # `label_style` no es soportado en Flet 0.85.0
                            label=ft.Text(v["estado"].upper(), size=11,
                                          color=color_estado(v["estado"])),
                            bgcolor="#0D3B66" if v["estado"] == "abierto"
                                    else "#2A2A3E",
                        ),
                        ft.IconButton(
                            icon=ft.Icons.PICTURE_AS_PDF,
                            icon_color="#00B4D8",
                            tooltip="Generar PDF",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        )

    return ft.Column(
        controls=[
            ft.Container(height=10),
            ft.Text("Reportes de Vuelos", size=20,
                    weight=ft.FontWeight.BOLD, color="white"),
            ft.Divider(color="#00B4D8", thickness=1),

            ft.Row(
                controls=[
                    ft.TextField(
                        label="Buscar vuelo",
                        hint_text="Ej. AM452",
                        bgcolor="#1E1E2E",
                        border_color="#00B4D8",
                        color="white",
                        prefix_icon=ft.Icons.SEARCH,
                        expand=True,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.FILTER_LIST,
                        icon_color="#00B4D8",
                        tooltip="Filtrar",
                    ),
                ]
            ),

            ft.Container(height=6),
            ft.Text("Vuelos registrados:", size=13, color="#AAAAAA"),

            ft.Column(
                controls=tarjetas,
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),

            ft.Container(height=10),
            ft.ElevatedButton(
                # `text` no es soportado en esta versión; usar `content` con `ft.Text`.
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.DOWNLOAD, color="white"),
                        ft.Text("Exportar todos los reportes", color="white"),
                    ],
                    alignment="center",
                ),
                bgcolor="#00B4D8",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                width=float("inf"),
            ),
            ft.Container(height=10),
        ],
        spacing=10,
        expand=True,
    )