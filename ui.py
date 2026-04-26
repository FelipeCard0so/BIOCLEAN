from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QCheckBox, QMessageBox, QProgressBar, QFrame
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from cleaner import Cleaner
from utils import asset


class Worker(QThread):
    update_log      = Signal(str)
    update_progress = Signal(int)
    finished        = Signal(str)

    def __init__(self, include_prefetch):
        super().__init__()
        self.include_prefetch = include_prefetch

    def run(self):
        cleaner = Cleaner(
            logger=self.update_log.emit,
            on_progress=self.update_progress.emit
        )
        cleaner.run_all(include_prefetch=self.include_prefetch)
        self.finished.emit(cleaner.freed_human())


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BioClean")
        self.setFixedSize(520, 580)
        self.setWindowIcon(QIcon(asset("assets/icone.ico")))  # ícone da janela
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #04B2D9;
                color: #023859;
                font-family: Segoe UI;
                font-size: 13px;
            }
            QPushButton {
                background-color: #048ABF;
                color: #ffffff;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover  { background-color: #0378a6; }
            QPushButton:disabled { background-color: #7ecfe8; color: #a0c8d8; }

            QProgressBar {
                border: none;
                border-radius: 6px;
                background-color: #027da6;
                height: 18px;
                text-align: center;
                color: white;
                font-weight: bold;
                font-size: 11px;
            }
            QProgressBar::chunk {
                border-radius: 6px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #0af0a0
                );
            }

            QTextEdit {
                background-color: #027da6;
                color: #d0f4ff;
                border-radius: 8px;
                padding: 6px;
                font-family: Consolas;
                font-size: 11px;
            }
            QCheckBox { font-size: 12px; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 12)
        layout.setSpacing(10)

        # Título
        title = QLabel("BioClean")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 48px; font-weight: bold; letter-spacing: 2px;"
            "color: #023859; padding: 4px 0px;"
        )

        # Card de espaço liberado
        self.freed_card = QFrame()
        self.freed_card.setStyleSheet("""
            QFrame {
                background-color: #027da6;
                border-radius: 10px;
                padding: 4px;
            }
        """)
        card_layout = QHBoxLayout(self.freed_card)
        card_layout.setContentsMargins(16, 8, 16, 8)

        icon_lbl = QLabel("💾")
        icon_lbl.setStyleSheet("font-size: 22px; background: transparent;")

        self.freed_label = QLabel("— GB liberados")
        self.freed_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #00f0c0;"
            "background: transparent;"
        )

        card_layout.addWidget(icon_lbl)
        card_layout.addWidget(self.freed_label)
        card_layout.addStretch()

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setFixedHeight(22)

        # Checkbox
        self.checkbox_log = QCheckBox("Salvar log no Desktop")

        # Botões
        btn_layout = QHBoxLayout()
        self.btn_full = QPushButton("⚡ Limpeza Completa")
        self.btn_safe = QPushButton("🛡 Sem Prefetch")
        self.btn_full.clicked.connect(lambda: self.start_clean(True))
        self.btn_safe.clicked.connect(lambda: self.start_clean(False))
        btn_layout.addWidget(self.btn_full)
        btn_layout.addWidget(self.btn_safe)

        # Log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("Os logs de limpeza aparecerão aqui...")

        # Rodapé
        footer = QLabel("Criado por: Felipe Cardoso")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-size: 11px; color: #025e80;")

        layout.addWidget(title)
        layout.addWidget(self.freed_card)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.checkbox_log)
        layout.addLayout(btn_layout)
        layout.addWidget(self.log_area)
        layout.addWidget(footer)

    def log(self, message):
        self.log_area.append(message)

    def set_buttons_enabled(self, enabled: bool):
        self.btn_full.setEnabled(enabled)
        self.btn_safe.setEnabled(enabled)

    def start_clean(self, include_prefetch):
        confirm = QMessageBox.question(
            self, "Confirmação",
            "⚠️ Esta limpeza é agressiva. Deseja continuar?"
        )
        if confirm != QMessageBox.Yes:
            return

        self.log_area.clear()
        self.progress_bar.setValue(0)
        self.freed_label.setText("Calculando...")
        self.set_buttons_enabled(False)

        self.worker = Worker(include_prefetch)
        self.worker.update_log.connect(self.log)
        self.worker.update_progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.finish)
        self.worker.start()

    def finish(self, freed_str: str):
        self.progress_bar.setValue(100)
        self.freed_label.setText(f"✔ {freed_str} liberados")
        self.set_buttons_enabled(True)

        # Salva log no Desktop se checkbox marcado
        if self.checkbox_log.isChecked():
            self._save_log_to_desktop(freed_str)

        QMessageBox.information(
            self, "Finalizado",
            f"✔ Limpeza concluída!\n\n💾 Espaço liberado: {freed_str}"
        )

    def _save_log_to_desktop(self, freed_str: str):
        from utils import get_desktop_path, generate_log_filename
        import os

        desktop = get_desktop_path()
        filename = generate_log_filename()
        filepath = os.path.join(desktop, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"BioClean — Relatório de Limpeza\n")
                f.write(f"{'=' * 40}\n")
                f.write(f"Espaço liberado: {freed_str}\n")
                f.write(f"{'=' * 40}\n\n")
                f.write(self.log_area.toPlainText())

            QMessageBox.information(
                self, "Log salvo",
                f"📄 Log salvo em:\n{filepath}"
            )
        except Exception as e:
            QMessageBox.warning(
                self, "Erro ao salvar log",
                f"Não foi possível salvar o log:\n{str(e)}"
            )