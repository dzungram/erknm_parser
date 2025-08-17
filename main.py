import os
import xml.etree.ElementTree as ET

from zipfile import ZipFile
from pathlib import Path
from parser import PvParser



def xml_parse(xml_file_path: str):
    source_file = Path(xml_file_path)
    if not source_file.exists():
        raise FileNotFoundError(f'Файл {xml_file_path} не существует.')
    if source_file.suffix.lower() != '.xml':
        raise ValueError(f'Файл {xml_file_path} не является файлом XML.')
    
    root = ET.parse(source=xml_file_path)
    
    return root

def extract_zip(zip_file: str, extract_to: str = 'data') -> list[str]:
    """
    
    Извлекает файлы из архива zip и возвращает список извлеченных файлов

    :param zip_file: Путь к файлу архива zip
    :type zip_file: str
    
    :param extract_to: Путь для извлечения файлов
    :type extract_to: str
    
    :raises FileNotFoundError: Если файл не существует
    :raises ValueError: Если файл не является архивом zip

    :rtype: list
    :return: Список извлеченных файлов
    """

    source_file = Path(zip_file)

    if not source_file.exists():
        raise FileNotFoundError(f'Файл {zip_file} не найден.')
    
    if source_file.suffix.lower() != '.zip':
        raise ValueError(f'Файл должен быть архивом zip.')
    
    os.makedirs(name=extract_to, exist_ok=True)
    extracted_files: list = []

    with ZipFile(file=zip_file) as zipf:
        for item in zipf.filelist:
            if item.filename.lower().endswith('.xml'):
                zipf.extract(member=item.filename, path=extract_to)
                extracted_path: str = str(Path(extract_to) / item.filename)
                extracted_files.append(extracted_path)
    
    return extracted_files


if __name__ == '__main__':
    pv = PvParser()
    pv.parse(xml_file_path='data/28836821.xml')