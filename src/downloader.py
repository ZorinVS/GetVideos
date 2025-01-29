import copy
import re

import yt_dlp

from src import os_utils
from src.utils import CustomLogger, get_error_message

DOWNLOAD_OPTIONS = {
    'format': 'bestvideo+bestaudio/best',
    'noplaylist': True,
    'timeout': 120,
    'merge_output_format': 'mp4',
    'retries': 5,  # пять попыток на случай ошибки
}


def download_video(video_url, progress_label, progress_bar, download_button, root):
    """ Загрузчик видео """
    def progress_hook(d):
        if d['status'] == 'downloading':
            # Удаление ANSI escape codes
            percentage_str = re.sub(r'\x1b\[[0-9;]*m', '', d.get('_percent_str', '0%')).strip('%')
            try:
                percentage = float(percentage_str)
            except ValueError:
                percentage = 0.0

            speed = d.get('_speed_str', '0 KiB/s')
            eta = d.get('eta', 0)
            progress_label.config(text=f'Downloading: {percentage:.2f}% | Speed: {speed} | ETA: {eta} sec')
            progress_bar['value'] = percentage
            root.update_idletasks()
        elif d['status'] == 'finished':
            progress_label.config(text='Download completed!')
            progress_bar['value'] = 100

    # Настройка параметров YoutubeDL
    opt = copy.deepcopy(DOWNLOAD_OPTIONS)
    opt['progress_hooks'] = [progress_hook]
    opt['logger'] = CustomLogger(progress_label, download_button)

    # Настройка папки загрузки
    platform = os_utils.extract_platform_from_url(video_url)
    download_path = os_utils.get_download_path(platform)
    opt['outtmpl'] = f'{download_path}/%(extractor)s_%(title)s_%(id)s.%(ext)s'

    try:  # запуск загрузки видео по введенному URL
        with yt_dlp.YoutubeDL(opt) as dl:
            dl.download([video_url])
    except yt_dlp.utils.DownloadError as e:
        progress_label.config(text=get_error_message(e))
