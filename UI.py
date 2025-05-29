
import logging
import subprocess
import tkinter as tk
import os
#import win32api
from tkinter import ttk, messagebox

user = os.getlogin()
# Основное окно
root = tk.Tk()
root.title("UI")
root.geometry("500x300")
root.iconbitmap(rf"C:\Users\{user}\AppData\Roaming\UI\assets\ico\dog.ico")


# Переменные и элементы, которые будут использоваться в функции
format_var = tk.StringVar()
audio_only = tk.BooleanVar()
save_path_var = tk.StringVar(value = rf"C:\Users\{user}\Videos")

# Создаём вкладки
tab_control = ttk.Notebook(root)
main_tab = ttk.Frame(tab_control)
settings_tab = ttk.Frame(tab_control)

tab_control.add(main_tab, text='Скачать')
tab_control.add(settings_tab, text='Настройки')
tab_control.pack(expand=1, fill="both")

# Вкладка "Скачать"
tk.Label(main_tab, text="Ссылка на видео:").pack(pady=5)
url_entry = tk.Entry(main_tab, width=60)
url_entry.pack(pady=5)

# Функция — теперь все нужные переменные уже существуют
def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Ошибка", "Введите ссылку на видео.")
        return

    cmd = rf"C:\users\{user}\AppData\Roaming\UI\bin\yt-dlp.exe","-f", "bestvideo+bestaudio","-P", save_path_var.get(), url # ← вот это
    
    if format_var.get():
        cmd += ["-f", format_var.get()]
    if audio_only.get():
        cmd += ["--extract-audio", "--audio-format", "mp3"]

    try:
        subprocess.run(cmd, check=True,  creationflags=subprocess.CREATE_NO_WINDOW)
        messagebox.showinfo("Успех", "Видео скачано.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Ошибка", "Не удалось скачать видео.")

tk.Button(main_tab, text="Скачать", command=download_video).pack(pady=10)

# Вкладка "Настройки"
tk.Label(settings_tab, text="Формат (например bestvideo+bestaudio или mp4):").pack(pady=5)
tk.Entry(settings_tab, textvariable=format_var, width=40).pack(pady=5)
tk.Checkbutton(settings_tab, text="Скачать только аудио", variable=audio_only).pack(pady=5)

# Запуск GUI
root.mainloop()