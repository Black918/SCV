import flet as ft

def vista_voz(page: ft.Page):
    estado_mic = ft.Text("Micrófono inactivo", size=13, color="#AAAAAA")
    texto_reconocido = ft.Text("", size=16, color="#90E0EF",
                                italic=True, text_align="center") # Usamos string "center"

    historial = ft.ListView(expand=True, spacing=8, padding=8)

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
        on_click=toggle_mic,
    )

    def agregar_comando_mock(e):
        historial.controls.insert(
            0,
            ft.Container(
                padding=10,
                border_radius=8,
                bgcolor="#1E1E2E",
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.RECORD_VOICE_OVER, color="#00B4D8", size=18),
                        ft.Column(
                            controls=[
                                ft.Text("agregar 10 comidas", color="white", size=13),
                                ft.Text("12:34:05", color="#AAAAAA", size=11),
                            ],
                            spacing=2,
                        )
                    ]
                )
            )
        )
        page.update()

    btn_simular = ft.OutlinedButton(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.PLAY_ARROW, size=20),
                ft.Text("Simular comando (prueba)", size=14),
            ],
            alignment="center", # Usamos string para evitar fallos de constantes
            tight=True,
        ),
        style=ft.ButtonStyle(
            side=ft.BorderSide(color="#00B4D8"),
            color="#00B4D8",
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=agregar_comando_mock,
        width=400,
    )

    return ft.Column(
        controls=[
            ft.Container(height=10),
            ft.Text("Movimientos por Voz", size=20, weight="bold", color="white"),
            ft.Divider(color="#00B4D8", thickness=1),

            # Indicador de estado
            ft.Container(
                padding=10,
                border_radius=10,
                bgcolor="#0D3B66",
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.GRAPHIC_EQ, color="#00B4D8"),
                        estado_mic,
                    ],
                )
            ),

            ft.Container(height=10),

            # Panel del micrófono
            ft.Container(
                height=160,
                border_radius=16,
                bgcolor="#12121F",
                content=ft.Column(
                    controls=[
                        btn_mic,
                        ft.Text("Toca para hablar", size=12, color="#555577"),
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                ),
            ),

            # Caja de texto reconocido (CORREGIDA SIN min_height)
            ft.Container(
                padding=15,
                border_radius=10,
                bgcolor="#1E1E2E",
                height=80, # Cambiado de min_height a height fijo
                content=texto_reconocido,
                alignment=ft.Alignment(0, 0),
            ),

            ft.Text("Comandos reconocidos:", size=13, color="#AAAAAA"),

            ft.Container(
                expand=True,
                border_radius=10,
                bgcolor="#12121F",
                padding=6,
                content=historial,
            ),

            # Botón inferior
            ft.Container(
                content=ft.Row([btn_simular], alignment="center"),
                # `ft.padding.only` no existe en Flet 0.85.0 — usar `ft.Padding`
                padding=ft.Padding(top=10, bottom=20)
            ),
        ],
        spacing=10,
        expand=True,
    )