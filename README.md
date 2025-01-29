# GetVideos

GetVideos - простое приложение для скачивания видео, разработанное на Python 
с использованием [Tkinter](https://docs.python.org/3/library/tkinter.html), которое позволяет 
пользователям загружать видео с [различных платформ](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md), 
введя URL видео.

Загрузки видео осуществляются с помощью [yt-dlp](https://github.com/yt-dlp/yt-dlp), форка популярного инструмента 
**youtube-dl**, который поддерживает широкий спектр сайтов и платформ для скачивания контента.

## Организация загрузок

Этот проект был разработан с учётом стандартных путей файловой системы macOS. 
Все загруженные видеофайлы сохраняются в папке **`GotVideos`**, которая автоматически создается 
в стандартной папке **`Downloads`** пользователя.

Для упрощения работы с файлами, проект использует систему их организации. В зависимости от платформы, 
с которой был загружен контент (например, YouTube, Instagram и др), файлы автоматически распределяются 
в соответствующие подкаталоги внутри **`GotVideos`**. Это позволяет легко найти видео, загруженные 
с разных платформ, и поддерживать порядок в папке загрузок.

### Логика работы организации файлов

1. **Если папка `GotVideos` уже существует и содержит подкаталоги**:
   - Старые файлы перераспределяются по папкам, соответствующим платформам (например, YouTube, Instagram и т. д.).
   - При загрузке нового файла он сохраняется в папку, соответствующую платформе, извлеченной из URL.

2. **Если в папке `GotVideos` нет подкаталогов**:
   - Если все файлы в корне папки принадлежат одной платформе, новые файлы сохраняются в той же папке.
   - Если файлы принадлежат разным платформам, они распределяются по отдельным папкам для каждой платформы.

3. **Создание папок для платформ**:
   - Для каждой платформы (например, YouTube, Instagram и т. д.) будет создана отдельная папка внутри **`GotVideos`**. Если файл загружается с новой платформы, она автоматически создается.

4. **Обработка существующих файлов**:
   - Если файл с таким же именем уже существует в папке, новый файл может быть перезаписан, если в настройках разрешена замена, или он будет удален, если установлена настройка для удаления новых файлов.


## Запуск проекта

```bash
python3 main.py
```
