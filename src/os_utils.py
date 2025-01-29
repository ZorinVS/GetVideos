import os
import re
import shutil

ROOT_FOLDER_NAME = 'GotVideos'
DOWNLOADS_PATH = os.path.join(os.path.expanduser('~'), 'Downloads')
ROOT_VIDEOS_PATH = os.path.join(DOWNLOADS_PATH, ROOT_FOLDER_NAME)

os.makedirs(ROOT_VIDEOS_PATH, exist_ok=True)


def extract_platform_from_url(url):
    """ Извлечение названия платформы из URL """
    match = re.search(r'https?://(?:www\.)?([^.]+)', url)
    return match.group(1) if match else match


def search_platform_in_filename(platform, filename):
    """ Поиск платформы в названии файла/папки """
    return re.search(platform, filename, re.I)


def is_there_platform(platform=None, filename=None, match=None):
    """ Проверка на наличие файлов полученных с определенной платформы """
    if match is None:
        match = search_platform_in_filename(platform, filename)
    return bool(match)


def get_download_path(platform):
    """
    Выдает путь, куда будет загружен файл

    Логика работы:
    - Если в корневой папке уже существуют подкаталоги, то:
        1. Выполняется организация старых файлов
        2. Возвращается путь к подкаталогу, соответствующему указанной платформе
    - Если в корневой папке отсутствуют подкаталоги, проверяются файлы в папке:
        1. Если все файлы относятся к одной платформе, загрузка остаётся в корневой папке
        2. Если файлы относятся к разным платформам, они распределяются в соответствующие папки
    """

    download_path = ROOT_VIDEOS_PATH

    for item in os.scandir(ROOT_VIDEOS_PATH):
        if item.name == '.DS_Store':  # пропуск системного файла
            continue

        if item.is_dir():  # при наличии папок используется организация файлов
            download_path = os.path.join(ROOT_VIDEOS_PATH, platform)
            organize_files(ROOT_VIDEOS_PATH)
            break
        else:  # при наличии файлов, полученных с разных платформ, используется организация файлов
            if not is_there_platform(platform, item.name):
                download_path = os.path.join(ROOT_VIDEOS_PATH, platform)
                organize_files(ROOT_VIDEOS_PATH)
                break

    return download_path


def organize_files(source_directory, replace_existing=True):
    """
    Организует файлы в папке, перемещая их в подкаталоги в зависимости от платформы

    Название каждого файла делится на части с использованием символа "_".
    Первая часть интерпретируется как имя платформы, и файлы с таким именем
    перемещаются в созданные для каждой платформы папки.
    Если в имени файла отсутствует название платформы, файл остаётся в корневой директории без изменений.

    :param source_directory: Путь к директории, в которой находятся файлы для организации
    :param replace_existing: Определяет поведение при обнаружении уже существующего файла:
        - True: Существующий файл заменяется новым
        - False: Новый файл удаляется, а существующий остаётся на месте
    """

    for item in os.scandir(source_directory):
        if item.name == '.DS_Store':  # пропуск системного файла
            continue

        if item.is_file():
            platform = item.name.split('_')[0] if len(item.name.split('_')) > 1 else None
            if platform:
                to_path = os.path.join(source_directory, platform)
                os.makedirs(to_path, exist_ok=True)

                if os.path.exists(os.path.join(to_path, item.name)):
                    if replace_existing:  # замена старого файла
                        os.remove(os.path.join(to_path, item.name))
                        shutil.move(item.path, to_path)
                    else:
                        os.remove(item.path)  # удаление нового файла
                else:
                    shutil.move(item.path, to_path)
