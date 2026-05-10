import flet as ft

# Agregamos 'on_navigate' para recibir la función de navegación desde el main
def vista_inicio(page: ft.Page, on_navigate=None):

    def navigate_to(vista_fn):
        if on_navigate:
            # Ejecutamos la función de navegación que viene del main
            page.run_task(on_navigate, vista_fn)

    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(height=20),
            ft.Row(
                controls=[
                    ft.Icon(ft.Icons.FLIGHT_TAKEOFF, size=40, color="#00B4D8"),
                    ft.Text("SCV — Sistema de Control de Vuelos",
                            size=22, weight=ft.FontWeight.BOLD, color="white"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(color="#00B4D8", thickness=1),
            ft.Container(height=10),

            ft.Container(
                padding=ft.Padding(left=20, top=20, right=20, bottom=20),
                border_radius=12,
                bgcolor="#1E1E2E",
                content=ft.Column(
                    controls=[
                        ft.Text("¿Qué es Kalan?",
                                size=18, weight=ft.FontWeight.BOLD, color="#00B4D8"),
                        ft.Container(height=8),
                        ft.Text(
                            "Aplicación multiplataforma para el personal de catering aéreo. "
                            "Permite contar productos por vuelo usando voz y cámara, "
                            "eliminando errores manuales y generando reportes automáticos.",
                            size=14, color="#CCCCCC",
                        ),
                    ]
                )
            ),
            ft.Container(height=16),

            ft.Row(
                wrap=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    # Importamos las vistas necesarias dentro de las lambdas para evitar ciclos
                    _tarjeta("📷", "Escaneo", "Lee códigos de barras en tiempo real", 
                             on_click=lambda _: navigate_to(__import__('pantallas.escaneo', fromlist=['vista_escaneo']).vista_escaneo)),
                    
                    _tarjeta("🎙️", "Voz", "Dicta productos con comandos de voz",
                             on_click=lambda _: navigate_to(__import__('pantallas.voz_pantalla', fromlist=['vista_voz']).vista_voz)),
                    
                    _tarjeta("📄", "Reportes", "Genera PDFs del resumen del vuelo",
                             on_click=lambda _: navigate_to(__import__('pantallas.reportes', fromlist=['vista_reportes']).vista_reportes)),
                    
                    _tarjeta("✈️", "Vuelos", "Gestiona sesiones de vuelo abiertas"),
                ],
            ),
            ft.Container(height=20),

            ft.Container(
                padding=ft.Padding(left=20, top=12, right=20, bottom=12),
                border_radius=10,
                bgcolor="#0D3B66",
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.INFO_OUTLINE, color="#00B4D8"),
                        ft.Text("Versión 1.0  ·  Kalan Project",
                                size=12, color="#AAAAAA"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

def _tarjeta(icono, titulo, descripcion, on_click=None):
    return ft.Container(
        width=160,
        height=110,
        padding=ft.Padding(left=14, top=14, right=14, bottom=14),
        border_radius=12,
        bgcolor="#1E1E2E",
        ink=True, # Efecto visual de clic
        on_click=on_click,
        border=ft.Border(
            left=ft.BorderSide(width=1, color="#00B4D8"),
            top=ft.BorderSide(width=1, color="#00B4D8"),
            right=ft.BorderSide(width=1, color="#00B4D8"),
            bottom=ft.BorderSide(width=1, color="#00B4D8"),
        ),
        content=ft.Column(
            controls=[
                ft.Text(icono, size=26),
                ft.Text(titulo, size=13,
                        weight=ft.FontWeight.BOLD, color="white"),
                ft.Text(descripcion, size=11, color="#AAAAAA"),
            ],
            spacing=4,
        ),
    )