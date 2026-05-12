import threading
import queue
import json


class VoskDependencyError(Exception):
    pass


class VoskListener:
    """Listener simple para Vosk que entrega textos reconocidos vía callback.

    Uso:
        listener = VoskListener(model_path="model", callback=mi_callback)
        listener.start()
        listener.stop()
    """

    def __init__(self, model_path="model", callback=None, samplerate=16000):
        self.model_path = model_path
        self.callback = callback
        self.samplerate = samplerate
        self._q = queue.Queue()
        self._running = False
        self._thread = None
        self._stream = None
        self._recognizer = None

    def _audio_callback(self, indata, frames, time, status):
        if status:
            try:
                print("Vosk audio status:", status)
            except Exception:
                pass
        # indata is bytes-like (RawInputStream)
        self._q.put(bytes(indata))

    def start(self):
        try:
            import sounddevice as sd
        except Exception as e:
            raise VoskDependencyError("Instala 'sounddevice' para usar reconocimiento por micrófono: " + str(e))

        try:
            from vosk import Model, KaldiRecognizer
        except Exception as e:
            raise VoskDependencyError("Instala 'vosk' y descarga un modelo Vosk: " + str(e))

        try:
            model = Model(self.model_path)
        except Exception as e:
            raise VoskDependencyError("No se pudo cargar el modelo Vosk en '{}': {}".format(self.model_path, e))

        self._recognizer = KaldiRecognizer(model, float(self.samplerate))
        self._running = True

        self._stream = sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, dtype='int16', channels=1, callback=self._audio_callback)
        self._stream.start()

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while self._running:
            try:
                data = self._q.get(timeout=0.1)
            except queue.Empty:
                continue

            if not data:
                continue

            try:
                if self._recognizer.AcceptWaveform(data):
                    res = json.loads(self._recognizer.Result())
                    text = res.get("text", "").strip()
                    if text and self.callback:
                        try:
                            self.callback(text)
                        except Exception:
                            pass
                else:
                    # enviar parcial para feedback rápido
                    resp = json.loads(self._recognizer.PartialResult())
                    partial = resp.get("partial", "").strip()
                    if partial and self.callback:
                        try:
                            self.callback(partial)
                        except Exception:
                            pass
            except Exception:
                # evitar que un error detenga el hilo
                continue

    def stop(self):
        self._running = False
        try:
            if self._stream is not None:
                self._stream.stop()
                self._stream.close()
        except Exception:
            pass
        try:
            if self._thread is not None:
                self._thread.join(timeout=0.5)
        except Exception:
            pass
