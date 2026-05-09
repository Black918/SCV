import flet as ft

def vista_escaneo(page: ft.Page):
    vuelo_actual = ft.Text("Sin vuelo activo", size=13, color="#AAAAAA")

    productos_escaneados = ft.ListView(
        expand=True,
        spacing=8,
        padding=ft.Padding(left=8, top=8, right=8, bottom=8),
    )

    campo_sku = ft.TextField(
        label="SKU / Código de barras",
        hint_text="Escanea o escribe el código",
        bgcolor="#1E1E2E",
        border_color="#00B4D8",
        focused_border_color="#90E0EF",
        color="white",
        prefix_icon=ft.Icons.QR_CODE_SCANNER,
        expand=True,
    )

    def agregar_mock(e):
        if campo_sku.value.strip():
            productos_escaneados.controls.append(
                ft.Container(
                    padding=ft.Padding(left=14, top=10, right=14, bottom=10),
                    border_radius=8,
                    bgcolor="#1E1E2E",
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.CHECK_CIRCLE, color="#00B4D8", size=18),
                            ft.Text(campo_sku.value.strip(),
                                    color="white", size=14, expand=True),
                            ft.Text("x1", color="#AAAAAA", size=13),
                        ]
                    )
                )
            )
            campo_sku.value = ""
            page.update()

    return ft.Column(
        controls=[
            ft.Container(height=10),
            ft.Text("Escaneo de Productos", size=20,
                    weight=ft.FontWeight.BOLD, color="white"),
            ft.Divider(color="#00B4D8", thickness=1),

            # Vuelo activo
            ft.Container(
                padding=ft.Padding(left=16, top=10, right=16, bottom=10),
                border_radius=10,
                bgcolor="#0D3B66",
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.FLIGHT, color="#00B4D8"),
                        ft.Text("Vuelo activo: ", color="#AAAAAA", size=13),
                        vuelo_actual,
                    ]
                )
            ),

            ft.Container(height=8),

            # Área de cámara (placeholder)
            ft.Container(
                height=180,
                border_radius=12,
                bgcolor="#12121F",
                border=ft.Border(
                    left=ft.BorderSide(width=2, color="#00B4D8"),
                    top=ft.BorderSide(width=2, color="#00B4D8"),
                    right=ft.BorderSide(width=2, color="#00B4D8"),
                    bottom=ft.BorderSide(width=2, color="#00B4D8"),
                ),
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.CAMERA_ALT_OUTLINED,
                                size=50, color="#00B4D850"),
                        ft.Text("Cámara — próximamente",
                                color="#555577", size=13),
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
                        icon_color="#00B4D8",
                        icon_size=32,
                        tooltip="Agregar producto",
                        on_click=agregar_mock,
                    ),
                ]
            ),

            ft.Text("Productos escaneados:", size=13, color="#AAAAAA"),

            ft.Container(
                expand=True,
                border_radius=10,
                bgcolor="#12121F",
                padding=ft.Padding(left=6, top=6, right=6, bottom=6),
                content=productos_escaneados,
            ),

            ft.ElevatedButton(
                text="Cerrar Vuelo y Generar Reporte",
                icon=ft.Icons.PICTURE_AS_PDF,
                bgcolor="#00B4D8",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                width=float("inf"),
            ),
            ft.Container(height=10),
        ],
        spacing=10,
        expand=True,
    )