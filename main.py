import sys
import os
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt, QTimer

from ui import MainWindow
from utils import is_admin, relaunch_as_admin, asset

# Esconde o console no Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


def main():
    if not is_admin():
        relaunch_as_admin()
        return

    app = QApplication(sys.argv)

    # Splash com GIF animado
    splash = QSplashScreen()
    splash.setWindowFlag(Qt.WindowStaysOnTopHint)
    movie = QMovie(asset("assets/splash.gif"))
    movie.start()

    def update_splash():
        pixmap = movie.currentPixmap()
        if not pixmap.isNull():
            splash.setPixmap(pixmap)

    movie.frameChanged.connect(update_splash)
    update_splash()
    splash.show()

    window = MainWindow()

    def launch():
        window.show()
        splash.finish(window)

    QTimer.singleShot(2000, launch)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()