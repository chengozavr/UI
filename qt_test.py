import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel, QLineEdit,
    QCheckBox, QPushButton, QFileDialog, QMessageBox, QTextEdit
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        try:
            process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            for line in process.stdout:
                self.progress.emit(line.strip())
            process.wait()
            if process.returncode == 0:
                self.finished.emit(True, "Видео успешно скачано.")
            else:
                self.finished.emit(False, "Произошла ошибка при скачивании.")
        except Exception as e:
            self.finished.emit(False, f"Ошибка: {e}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qt_test")
        self.setFixedSize(500, 300)

        user = os.getlogin()
        icon_path = rf"C:\Users\{user}\AppData\Roaming\qt_test\assets\ico\dog.ico"
        self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Вкладка "Скачать"
        self.download_tab = QWidget()
        self.tabs.addTab(self.download_tab, "Скачать")
        dl_layout = QVBoxLayout(self.download_tab)

        dl_layout.addWidget(QLabel("Ссылка на видео:"))
        self.url_entry = QLineEdit()
        dl_layout.addWidget(self.url_entry)

        self.audio_only_cb = QCheckBox("Только аудио")
        dl_layout.addWidget(self.audio_only_cb)

        self.download_btn = QPushButton("Скачать")
        dl_layout.addWidget(self.download_btn)
        self.download_btn.clicked.connect(self.download_video)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        dl_layout.addWidget(self.output_box)

        # Вкладка "Настройки"
        self.settings_tab = QWidget()
        self.tabs.addTab(self.settings_tab, "Настройки")
        settings_layout = QVBoxLayout(self.settings_tab)

        settings_layout.addWidget(QLabel("Путь для сохранения:"))
        self.save_path_entry = QLineEdit()
        self.save_path_entry.setText(rf"C:\Users\{user}\Videos")
        settings_layout.addWidget(self.save_path_entry)

        self.browse_btn = QPushButton("Выбрать папку")
        settings_layout.addWidget(self.browse_btn)
        self.browse_btn.clicked.connect(self.choose_folder)

        settings_layout.addWidget(QLabel("Формат (например bestvideo+bestaudio или mp4):"))
        self.format_entry = QLineEdit()
        settings_layout.addWidget(self.format_entry)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if folder:
            self.save_path_entry.setText(folder)

    def download_video(self):
        url = self.url_entry.text().strip()
        if not url:
            QMessageBox.critical(self, "Ошибка", "Введите ссылку на видео.")
            return

        user = os.getlogin()
        yt_dlp_path = rf"C:\Users\{user}\AppData\Roaming\qt_test\bin\yt-dlp.exe"
        save_path = self.save_path_entry.text().strip()
        video_format = self.format_entry.text().strip()
        audio_only = self.audio_only_cb.isChecked()

        cmd = [yt_dlp_path, "-P", save_path]

        if audio_only:
            cmd += ["--extract-audio", "--audio-format", "mp3"]
        elif video_format:
            cmd += ["-f", video_format]

        cmd.append(url)

        self.output_box.clear()
        self.download_btn.setEnabled(False)
        self.thread = DownloadThread(cmd)
        self.thread.progress.connect(self.output_box.append)
        self.thread.finished.connect(self.download_finished)
        self.thread.start()

    def download_finished(self, success, message):
        self.download_btn.setEnabled(True)
        QMessageBox.information(self, "Завершено" if success else "Ошибка", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
