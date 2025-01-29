import tkinter as tk
from threading import Thread
from tkinter import ttk

from src.downloader import download_video


def run_ui():
    """ Создание интерфейса """
    root = tk.Tk()
    root.title('Downloader')
    root.geometry('800x220')

    style = ttk.Style()  # стиль кнопки
    style.configure('TButton', font=('TkDefaultFont', 12))
    style.map('TButton',
              foreground=[('disabled', 'gray')],
              background=[('disabled', '#d9d9d9'), ('!disabled', '#0078d7')])

    def start_download():
        """ Запуск загрузки в отдельном потоке """
        video_url = entry_var.get().strip()
        if not video_url:
            progress_label.config(text='Please enter a URL!')
            return

        progress_label.config(text='Starting download...')
        progress_bar['value'] = 0
        download_button.config(state=tk.DISABLED)
        Thread(target=download_video, args=(video_url, progress_label, progress_bar, download_button, root)).start()

    def on_entry_change(*args):
        """ Проверка изменения ввода """
        video_url = entry_var.get().strip()
        download_button.config(state=tk.NORMAL if video_url else tk.DISABLED)

    entry_title = ttk.Label(root, text='URL to Download:')
    entry_title.pack(anchor=tk.NW, padx=10, pady=(20, 2))

    entry_var = tk.StringVar()
    entry_var.trace_add('write', on_entry_change)
    entry = ttk.Entry(root, textvariable=entry_var, width=90)
    entry.pack(anchor=tk.NW, padx=10, pady=0)

    progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
    progress_bar.pack(pady=(30, 5))

    progress_label = ttk.Label(root, text='Waiting...')
    progress_label.pack()

    download_button = ttk.Button(root, text='Get It', command=start_download, state=tk.DISABLED)
    download_button.pack(side=tk.BOTTOM, pady=20)

    root.mainloop()

