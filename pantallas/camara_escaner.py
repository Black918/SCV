import flet as ft

# Pequeño helper para construir el panel de cámara
def camera_panel(image_control: ft.Image, btn_control: ft.IconButton, hint: str = "Cámara") -> ft.Container:
    """Devuelve un Container estilizado que contiene la imagen de la cámara
    y el botón para iniciar/detener. Mantener simple y reutilizable.
    """
    return ft.Container(
        height=260,
        border_radius=12,
        bgcolor="#FFFFFF00",  # transparente por defecto, el tema controla el fondo
        border=ft.Border(
            left=ft.BorderSide(width=2, color="#e6e6e6"),
            top=ft.BorderSide(width=2, color="#e6e6e6"),
            right=ft.BorderSide(width=2, color="#e6e6e6"),
            bottom=ft.BorderSide(width=2, color="#e6e6e6"),
        ),
        padding=ft.Padding(10, 10, 10, 10),
        content=ft.Column(
            controls=[
                image_control,
                ft.Row(
                    controls=[
                        btn_control,
                        ft.Text(hint, size=13, color="#777777"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
