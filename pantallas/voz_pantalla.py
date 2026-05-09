import flet as ft

def vista_voz(page: ft.Page):
    estado_mic = ft.Text("Micrófono inactivo", size=13, color="#AAAAAA")
    texto_reconocido = ft.Text("", size=16, color="#90E0EF",
                                italic=True, text_align=ft.TextAlign.CENTER)

    historial = ft.ListView(expand=True, spacing=8, padding=ft.Padding(left=8, top=8, right=8, bottom=8))

    escuchando = {"activo": False}

    def toggle_mic(e):
        escuchando["activo"] = not escuchando["activo"]
        if escuchando["activo"]:
            estado_mic.value = "🔴  Escuchando..."
            estado_mic.color = "#FF6B6B"
            btn_mic.icon = ft.Icons.MIC
            btn_mic.icon_color = "#FF6B6B"
            texto_reconocido.value = "Di un comando, por ejemplo:\n\"Agregar 10 comidas\""
        else:
            estado_mic.value = "Micrófono inactivo"
            estado_mic.color = "#AAAAAA"
            btn_mic.icon = ft.Icons.MIC_OFF
            btn_mic.icon_color = "#00B4D8"
            texto_reconocido.value = ""
        page.update()

    btn_mic = ft.IconButton(
        icon=ft.Icons.MIC_OFF,
        icon_color="#00B4D8",
        icon_size=64,
        tooltip="Activar/desactivar micrófono",
        on_click=toggle_mic,
    )

    def agregar_comando_mock(e):
        historial.controls.insert(
            0,
            ft.Container(
                padding=ft.padding.symmetric(horizontal=14, vertical=10),
                border_radius=8,
                bgcolor="#1E1E2E",
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.RECORD_VOICE_OVER,
                                color="#00B4D8", size=18),
                        ft.Column(
                            controls=[
                                ft.Text("agregar 10 comidas",
                                        color="white", size=13),
                                ft.Text("12:34:05",
                                        color="#AAAAAA", size=11),
                            ],
                            spacing=2,
                        )
                    ]
                )
            )
        )
        page.update()

    return ft.Column(
        controls=[
            ft.Container(height=10),
            ft.Text("Movimientos por Voz", size=20,
                    weight=ft.FontWeight.BOLD, color="white"),
            ft.Divider(color="#00B4D8", thickness=1),

            # Indicador de estado
            ft.Container(
                padding=ft.Padding(left=16, top=10, right=16, bottom=10),
                border_radius=10,
                bgcolor="#0D3B66",
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.GRAPHIC_EQ, color="#00B4D8"),
                        estado_mic,
                    ],
                    spacing=10,
                )
            ),

            ft.Container(height=10),

            # Botón micrófono central
            ft.Container(
                height=160,
                border_radius=16,
                bgcolor="#12121F",
                content=ft.Column(
                    controls=[
                        btn_mic,
                        ft.Text("Toca para hablar",
                                size=12, color="#555577"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                ),
            ),

            ft.Container(
                padding=ft.Padding(left=12, top=12, right=12, bottom=12),
                border_radius=10,
                bgcolor="#1E1E2E",
                min_height=60,
                content=texto_reconocido,
                alignment=ft.alignment.center,
            ),

            ft.Text("Comandos reconocidos:", size=13, color="#AAAAAA"),

            ft.Container(
                expand=True,
                border_radius=10,
                bgcolor="#12121F",
                padding=ft.Padding(left=6, top=6, right=6, bottom=6),
                content=historial,
            ),

            # Botón de prueba (se quitará cuando esté funcional)
            ft.OutlinedButton(
                text="Simular comando (prueba)",
                icon=ft.Icons.PLAY_ARROW,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(color="#00B4D8"),
                    color="#00B4D8",
                ),
                on_click=agregar_comando_mock,
                width=float("inf"),
            ),
            ft.Container(height=10),
        ],
        spacing=10,
        expand=True,
    )