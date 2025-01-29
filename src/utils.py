import tkinter as tk


class CustomLogger:
    """ Кастомный логгер """
    def __init__(self, progress_label, download_button):
        self.progress_label = progress_label
        self.download_button = download_button

    def debug(self, msg):
        if 'has already been downloaded' in msg:
            self.progress_label.config(text='The video has already been downloaded')
            self.download_button.config(state=tk.DISABLED)

    def warning(self, msg):
        pass

    def error(self, msg):
        self.progress_label.config(text=f'Error: {msg}')
        self.download_button.config(state=tk.DISABLED)


def get_error_message(err):
    """ Получение сообщения об ошибке """

    if 'unable to extract' in str(err).lower():
        return 'Error: Unable to extract data. Please check the URL'
    if 'unsupported URL' in str(err).lower():
        return 'Error: Unsupported URL. Please use a valid link'
    if 'http error' in str(err).lower():
        return 'Error: The site is unreachable or the link is invalid'

    return 'Error: Failed to download the video'
