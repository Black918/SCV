import flet as ft
import config_colors as theme
import threading
import base64
import cv2
import numpy as np
import time
from collections import deque, defaultdict
import hashlib
import os
import contextlib
from pantallas.camara_escaner import camera_panel
try:
    from pyzbar.pyzbar import decode
except Exception:
    def decode(_):
        return []

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

    # --- Cámara / lector de códigos ---
    class CameraListener:
        def __init__(self, device=0, callback_frame=None, callback_barcode=None):
            self.device = device
            self.callback_frame = callback_frame
            self.callback_barcode = callback_barcode
            self._running = False
            self._thread = None
            self._cap = None
            self._recent = deque(maxlen=8)
            self._last_confirmed = defaultdict(lambda: 0.0)
            self._last_frame_hash = None

        def start(self):
            if self._running:
                return True
            try:
                self._cap = cv2.VideoCapture(self.device)
            except Exception:
                self._cap = None
            if not self._cap or not self._cap.isOpened():
                return False
            self._running = True
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            return True

        def _run(self):
            last_send = 0.0
            interval = 0.12  # ~8 fps to reduce flicker and improve stability
            while self._running:
                try:
                    ret, frame = self._cap.read()
                    if not ret:
                        time.sleep(0.01)
                        continue

                    # Decodificar códigos de barras con preprocesado para mayor robustez
                    try:
                        results = self._try_decode(frame)
                        if results:
                            nowt = time.time()
                            for data in results:
                                # voting via recent buffer
                                self._recent.append(data)
                                count = sum(1 for x in self._recent if x == data)
                                # confirmar si aparece >=2 veces en buffer y no fue confirmada recientemente
                                if count >= 2 and (nowt - self._last_confirmed.get(data, 0)) > 1.5:
                                    try:
                                        if self.callback_barcode:
                                            self.callback_barcode(data)
                                        self._last_confirmed[data] = nowt
                                    except Exception:
                                        pass
                    except Exception:
                        pass

                    # Enviar frame con throttling para evitar parpadeo
                    now = time.time()
                    if now - last_send >= interval:
                        last_send = now
                        try:
                            _, buf = cv2.imencode('.png', frame)
                            buf_bytes = buf.tobytes()
                            # usar hash para evitar enviar frames idénticos y reducir parpadeo
                            h = hashlib.md5(buf_bytes).hexdigest()
                            if h != self._last_frame_hash:
                                self._last_frame_hash = h
                                b64 = base64.b64encode(buf_bytes).decode('ascii')
                                src = f"data:image/png;base64,{b64}"
                                if self.callback_frame:
                                    try:
                                        self.callback_frame(src)
                                    except Exception:
                                        pass
                            else:
                                # si es idéntico, no actualizar imagen
                                pass
                        except Exception:
                            pass
                    else:
                        # small sleep to avoid busy loop
                        time.sleep(0.005)
                except Exception:
                    time.sleep(0.01)
                    continue

        def capture_and_decode(self):
            """Captura un frame puntual y procesa decodificación y callback de frame."""
            if not self._cap:
                return
            try:
                ret, frame = self._cap.read()
                if not ret:
                    return
                # intentar decodificar usando el mismo pipeline robusto
                try:
                    results = self._try_decode(frame)
                    if results:
                        nowt = time.time()
                        for data in results:
                            if (nowt - self._last_confirmed.get(data, 0)) > 1.5:
                                try:
                                    if self.callback_barcode:
                                        self.callback_barcode(data)
                                    self._last_confirmed[data] = nowt
                                except Exception:
                                    pass
                except Exception:
                    pass
                # enviar frame
                try:
                    _, buf = cv2.imencode('.png', frame)
                    b64 = base64.b64encode(buf.tobytes()).decode('ascii')
                    src = f"data:image/png;base64,{b64}"
                    if self.callback_frame:
                        try:
                            self.callback_frame(src)
                        except Exception:
                            pass
                except Exception:
                    pass
            except Exception:
                pass

        def stop(self):
            self._running = False
            try:
                if self._cap:
                    self._cap.release()
            except Exception:
                pass
            try:
                if self._thread is not None:
                    self._thread.join(timeout=0.5)
            except Exception:
                pass

        def _preprocess(self, frame):
            """Devuelve una lista de variantes procesadas del frame para intentar decodificar.
            Incluye: imagen original, escala de grises aumentada, ecualización, y recorte central.
            """
            variants = []
            try:
                # original (convertir a RGB si es necesario)
                variants.append(frame)

                # gris y ecualizado
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # CLAHE para mejorar contraste en zonas con poca iluminación
                try:
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                    eq = clahe.apply(gray)
                except Exception:
                    eq = cv2.equalizeHist(gray)
                variants.append(eq)

                # suavizado ligero para reducir ruido
                blur = cv2.GaussianBlur(eq, (3,3), 0)
                variants.append(blur)

                # recorte central (muchos códigos se centran en pantalla)
                h, w = gray.shape[:2]
                ch, cw = int(h*0.6), int(w*0.6)
                y0 = max(0, (h-ch)//2)
                x0 = max(0, (w-cw)//2)
                crop = frame[y0:y0+ch, x0:x0+cw]
                variants.append(crop)

                # también añadir versión grande (resize) para mejorar lectura de líneas finas
                try:
                    scale_w = 800
                    scale = scale_w / float(w)
                    if scale > 1:
                        big = cv2.resize(gray, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_LINEAR)
                        variants.append(big)
                except Exception:
                    pass
            except Exception:
                pass
            return variants

        def _try_decode(self, frame):
            """Intenta decodificar usando varias variantes y suprime warnings C de zbar."""
            results = []
            try:
                import contextlib, os, sys
                variants = self._preprocess(frame)
                for v in variants:
                    try:
                        with open(os.devnull, 'w') as devnull:
                            with contextlib.redirect_stderr(devnull):
                                barcodes = decode(v)
                        if barcodes:
                            for barcode in barcodes:
                                try:
                                    data = barcode.data.decode('utf-8')
                                except Exception:
                                    data = str(barcode.data)
                                if data:
                                    results.append(data)
                            # si encontramos en esta variante, retornamos resultados (priorizar primera variante que funcione)
                            if results:
                                return results
                    except Exception:
                        continue
            except Exception:
                pass
            return results

    cam_listener = {"obj": None}
    # Elementos UI para cámara
    # Inicializar sin `src` vacío para evitar la validación de Flet
    # Placeholder PNG 1x1 (transparent) para evitar validación de src vacío
    placeholder_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
    placeholder_src = f"data:image/png;base64,{placeholder_b64}"
    cam_image = ft.Image(src=placeholder_src, width=380, height=200)
    btn_cam = ft.IconButton(
        icon=ft.Icons.VIDEOCAM,
        icon_color=theme.c("ACCENT"),
        icon_size=28,
        tooltip="Iniciar/Detener cámara",
    )

    # scanned_codes removed: allow duplicates, use cooldown logic instead

    def on_frame_update(src: str):
        try:
            cam_image.src = src
            try:
                cam_image.update()
            except Exception:
                page.update()
        except Exception:
            pass

    def on_barcode_detected(data: str):
        if not data:
            return
        # Rellenar campo SKU y agregar automáticamente (permitir duplicados)
        try:
            campo_sku.value = data
            agregar_mock(None)
        except Exception:
            try:
                # Fallback: añadir manualmente si agregar_mock falla
                productos_escaneados.controls.append(
                    ft.Container(
                        padding=ft.Padding(left=14, top=10, right=14, bottom=10),
                        border_radius=8,
                        bgcolor=theme.c("CARD_BG"),
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.CHECK_CIRCLE, color=theme.c("ACCENT"), size=18),
                                ft.Text(data, color=theme.c("TEXT_MAIN"), size=14, expand=True),
                                ft.Text("x1", color=theme.c("MUTED"), size=13),
                            ]
                        )
                    )
                )
                page.update()
            except Exception:
                pass

    def toggle_camera(e):
        if cam_listener.get("obj") is None:
            # iniciar
            cam_listener["obj"] = CameraListener(device=0, callback_frame=on_frame_update, callback_barcode=on_barcode_detected)
            try:
                cam_listener["obj"].start()
                btn_cam.icon = ft.Icons.VIDEOCAM_OFF
                btn_cam.icon_color = "#FF6B6B"
            except Exception as ex:
                try:
                    productos_escaneados.controls.insert(0, ft.Text(f"Error cámara: {ex}", color=theme.c("MUTED")))
                except Exception:
                    pass
        else:
            # detener -> antes de liberar, capturar y decodificar un frame final
            try:
                try:
                    # intentar procesar un frame final para captar códigos visibles
                    cam_listener["obj"].capture_and_decode()
                except Exception:
                    pass
                cam_listener["obj"].stop()
            except Exception:
                pass
            cam_listener["obj"] = None
            btn_cam.icon = ft.Icons.VIDEOCAM
            btn_cam.icon_color = theme.c("ACCENT")
        try:
            page.update()
        except Exception:
            pass

    # asignar callback al botón ahora que toggle_camera existe
    try:
        btn_cam.on_click = toggle_camera
    except Exception:
        pass

    # NO iniciar cámara automáticamente; el usuario la inicia con el botón
    try:
        cam_listener["obj"] = None
    except Exception:
        cam_listener["obj"] = None

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

    content_column = ft.Column(
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
                    camera_panel(cam_image, btn_cam, "Cámara (presiona el icono para iniciar)"),

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
        scroll=ft.ScrollMode.AUTO,
    )

    return content_column