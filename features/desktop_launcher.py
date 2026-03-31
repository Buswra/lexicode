import socket
import sys
import threading
import time
from urllib.request import urlopen

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from werkzeug.serving import make_server

try:
    from .app import app, init_db
    from .config import APP_NAME, DEFAULT_HOST
except ImportError:
    from app import app, init_db
    from config import APP_NAME, DEFAULT_HOST


class ServerThread(threading.Thread):
    def __init__(self, host: str, port: int):
        super().__init__(daemon=True)
        self._server = make_server(host, port, app, threaded=True)
        self._app_context = app.app_context()
        self._app_context.push()

    def run(self):
        self._server.serve_forever()

    def shutdown(self):
        self._server.shutdown()
        self._app_context.pop()


def find_free_port(start: int = 5000, end: int = 5100) -> int:
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            if sock.connect_ex((DEFAULT_HOST, port)) != 0:
                return port
    return start


def wait_for_server(url: str, timeout: float = 10.0) -> bool:
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            with urlopen(url, timeout=1.0) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.15)
    return False


class LexiCodeWindow(QMainWindow):
    def __init__(self, url: str, server: ServerThread):
        super().__init__()
        self.server = server
        self.setWindowTitle(APP_NAME)
        self.resize(1280, 900)
        self.setMinimumSize(1024, 720)

        self.browser = QWebEngineView(self)
        self.setCentralWidget(self.browser)
        self.browser.loadFinished.connect(self._handle_load_finished)
        self.browser.setUrl(QUrl(url))

    def _handle_load_finished(self, ok: bool):
        if not ok:
            self.browser.setHtml(
                """
                <html><body style='font-family:Segoe UI,Arial,sans-serif;background:#0f172a;color:white;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;'>
                    <div style='max-width:560px;padding:24px;text-align:center;'>
                        <h2>LexiCode başlatılamadı</h2>
                        <p>Uygulama arka plan servisi zamanında yanıt vermedi. Lütfen uygulamayı tekrar açın.</p>
                    </div>
                </body></html>
                """
            )

    def closeEvent(self, event):
        try:
            self.server.shutdown()
        finally:
            super().closeEvent(event)


def main():
    init_db()
    port = find_free_port()
    url = f"http://{DEFAULT_HOST}:{port}"

    server = ServerThread(DEFAULT_HOST, port)
    server.start()

    if not wait_for_server(url):
        raise RuntimeError("LexiCode arka plan servisi başlatılamadı.")

    qt_app = QApplication(sys.argv)
    window = LexiCodeWindow(url, server)
    qt_app.aboutToQuit.connect(server.shutdown)
    window.show()
    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()
