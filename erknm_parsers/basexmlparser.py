from abc import ABC, abstractmethod

class BaseXMLParser(ABC):
    """Минимальный абстрактный класс"""

    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def validate(self):
        """Проверка файла ЕРКНМ"""
        pass

    @abstractmethod
    def parse(self):
        """Основной метод парсинга"""
        pass