import logging
import xml.etree.cElementTree as ET
from abc import ABC, abstractmethod
from xml.etree.ElementTree import ParseError, ElementTree, Element

logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


class BaseErknmParser(ABC):
    def __init__(self):
        self.root = None
        self.ns = None

    def _set_root(self, xml_file_path: str):
        try:
            tree: ElementTree[Element[str]] = ET.parse(source=xml_file_path)
            self.root = tree.getroot()
            logger.info('Successfully set root element')
            self._extract_ns()
            logger.info('Successfully set namespace element')
        except (FileNotFoundError, ParseError) as e:
            raise ValueError(f'Ошибка парсинга файла {xml_file_path}.')

    def _extract_ns(self):
        if self.root is not None:
            self.ns = {
                'ns': self.root.tag.split('}')[0].strip('{')
            } if '}' in self.root.tag else {}

    @abstractmethod
    def parse(self, xml_file_path: str):
        pass


class KnmParser(BaseErknmParser):
    def __init__(self):
        super().__init__()

    def parse(self, xml_file_path: str):
        self._set_root(xml_file_path)


class PvParser(BaseErknmParser):
    def __init__(self):
        super().__init__()

    def parse(self, xml_file_path: str):
        self._set_root(xml_file_path)


class ParserFactory:
    @staticmethod
    def get_parser(xml_type: str):
        parsers = {
            'knm': KnmParser,
            'pv': PvParser,
        }
        if xml_type not in parsers:
            raise ValueError(f'Неизвестный тип XML файла')
