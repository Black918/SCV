import flet as ft
import config_colors as theme


def vista_voz(page: ft.Page):
    estado_mic = ft.Text("Micrófono inactivo", size=13, color=theme.c("MUTED"))
    texto_reconocido = ft.Text("", size=16, color=theme.c("ACCENT"),
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
            estado_mic.color = theme.c("MUTED")
            btn_mic.icon = ft.Icons.MIC_OFF
            btn_mic.icon_color = theme.c("ACCENT")
            texto_reconocido.value = ""
        page.update()

    btn_mic = ft.IconButton(
        icon=ft.Icons.MIC_OFF,
        icon_color=theme.c("ACCENT"),
        icon_size=64,
        on_click=toggle_mic,
    )

    def agregar_comando_mock(e):
        historial.controls.insert(
            0,
            ft.Container(
                padding=10,
                border_radius=8,
                bgcolor=theme.c("CARD_BG"),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.RECORD_VOICE_OVER, color=theme.c("ACCENT"), size=18),
                        ft.Column(
                            controls=[
                                ft.Text("agregar 10 comidas", color=theme.c("TEXT_MAIN"), size=13),
                                ft.Text("12:34:05", color=theme.c("MUTED"), size=11),
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
                ft.Icon(ft.Icons.PLAY_ARROW, size=20, color=theme.c("ACCENT")),
                ft.Text("Simular comando (prueba)", size=14, color=theme.c("TEXT_MAIN")),
            ],
            alignment="center", # Usamos string para evitar fallos de constantes
            tight=True,
        ),
        style=ft.ButtonStyle(
            side=ft.BorderSide(color=theme.c("ACCENT")),
            color=theme.c("ACCENT"),
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=agregar_comando_mock,
        width=400,
    )

    return ft.Column(
        controls=[
            ft.Container(height=10),
            ft.Text("Movimientos por Voz", size=20, weight="bold", color=theme.c("TEXT_MAIN")),
            ft.Divider(color=theme.c("ACCENT"), thickness=1),

            # Indicador de estado
            ft.Container(
                padding=10,
                border_radius=10,
                bgcolor=theme.c("BUTTON_BG"),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.GRAPHIC_EQ, color=theme.c("ACCENT")),
                        estado_mic,
                    ],
                )
            ),

            ft.Container(height=10),

            # Panel del micrófono
            ft.Container(
                height=160,
                border_radius=16,
                bgcolor=theme.c("CARD_BG"),
                content=ft.Column(
                    controls=[
                        btn_mic,
                        ft.Text("Toca para hablar", size=12, color=theme.c("MUTED")),
                    ],
                    alignment="center",
                    horizontal_alignment="center",
                ),
            ),

            # Caja de texto reconocido (CORREGIDA SIN min_height)
            ft.Container(
                padding=15,
                border_radius=10,
                bgcolor=theme.c("CARD_BG"),
                height=80, # Cambiado de min_height a height fijo
                content=texto_reconocido,
                alignment=ft.Alignment(0, 0),
            ),

            ft.Text("Comandos reconocidos:", size=13, color=theme.c("MUTED")),

            ft.Container(
                expand=True,
                border_radius=10,
                bgcolor=theme.c("CARD_BG"),
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