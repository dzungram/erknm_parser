import logging
import xml.etree.cElementTree as ET
from abc import ABC, abstractmethod
from typing import Dict, List
from xml.etree.ElementTree import ParseError, ElementTree, Element

logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

KNM_TYPES = ['выездная проверка', 'профилактический визит']

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
    def parse(self, xml_file_path: str) -> dict:
        pass

    def _find_attrib(self, parent: Element[str], path: str) -> Dict[str, str]:
        """Парсит атрибуты тега XML

        :param parent: Родительский элемент
        :type parent: Element[str]
        :param path: Путь по namespace
        :type path: str
        :return Dict[str, str]: `Словарь значений атрибутов`
        """
        element = parent.find(path, self.ns)
        return element.attrib if element else {}



class KnmParser(BaseErknmParser):
    def __init__(self):
        super().__init__()

    def parse(self, xml_file_path: str) -> Dict:
        """Парсит XML файл
        
        :param xml_file_path: Путь к файлу XML
        :type xml_file_path: str

        :return dict: `Словарь словарей`
        """
        self._set_root(xml_file_path)
        return {
            'knm_date': self._parse_date()
        }

    def _parse_date(self) -> Dict[str, str]:
        """Парсит и возвращает словарь с датами КНМ

        :return Dict[str, str]: `Словарь с датами`
        """
        knm_date = {}
        if self.root:
            knm_date = self.root.attrib
        return knm_date

    def _parse_kind_control(self) -> Dict[str, str]:
        """Парсит вид контроля

        :return dict: `Словарь с видом контроля`
        """
        element = None
        if self.root:
            element = self.root.find('tns:KIND_CONTROL', self.ns)
        if element:    
            return element.attrib
        return {}
    
    def _parse_kind_knm(self) -> Dict[str, str]:
        element = None
        if self.root:
            element = self.root.find('tns:KIND_KNM', self.ns)
        if element:
            return element.attrib
        return {}

    def _parse_organizations(self) -> Dict[str, Dict[str, str]]:
        """Парсит и возвращает реквизиты организации

        :return Dict: `Реквизиты организации`
        """
        if self.root:
            org = self.root.find('tns:ORGANIZATIONS', self.ns)
            if org:
                okved = org.find('tns:OKVEDS', self.ns)
                return {
                    'organizations': org.attrib,
                    'okveds': okved.attrib if okved else {}
                }
        return {}
    
    def _parse_objects(self) -> Dict:
        if self.root:
            objects_node = self.root.find('tns:OBJECTS', self.ns)
            if objects_node:
                return {
                    'object_type': self._find_attrib(objects_node, 'tns:OBJECT_TYPE'),
                    'object_kind': self._find_attrib(objects_node, 'tns:OBJECT_KIND'),
                    'object_sub_kind': self._find_attrib(objects_node, 'tns:OBJECT_SUB_KIND'),
                    'risk_category': self._find_attrib(objects_node, 'tns:RISK_CATEGORY')
                }
        return {}
    
    def _parse_inspectors(self) -> List[Dict[str, str]]:
        """Парсит и возвращает список инспекторов, участвующих в проверке

        :return List: Список инспекторов
        """
        inspectors = []
        if self.root:
            for element in self.root.findall('tns:INSPECTORS', self.ns):
                position = element.find('tns:INSPECTOR_POSITION', self.ns)
                inspectors.append(
                    {
                        'full_name': element.get('INSPECTORS_FULL_NAME'),
                        'guid': element.get('GUID'),
                        'position': position.get('TITLE') if position else '',
                    }
                )
        return inspectors
    
    def _parse_places(self) -> str | None:
        """Парсит и возвращает адрес местонахождения объекта проверки
        
        :return str: Адрес местонахождения
        """
        if self.root:
            element = self.root.find('tns:PLACES', self.ns)
            return element.text if element else ''
        return ''

    def _parse_decision(self) -> Dict[str | None, str | None]:
        """Парсит и возвращает решение по КНМ

        :return dict: Словарь с решением по КНМ
        """
        if self.root:
            element = self.root.find('tns:DECISION', self.ns)
            if element:
                title = element.find('tns:TITLE_SIGNER', self.ns)
                return {
                    'signer': element.get('FIO_SIGNER'),
                    'title': title.get('TITLE') if title else '',
                }
        return {}
    
    def _parse_reason_risk(self):

        element = self.root.find('tns:REASON_RISK', self.ns) if self.root else None
        reason = element.find('tns:REASON', self.ns) if element else None
        reason_type = reason.find('tns:REASON_TYPE', self.ns) if reason else None

        kind_knm = self._parse_kind_knm()
        
        
        return {}


class PvParser(BaseErknmParser):
    def __init__(self):
        super().__init__()

    def parse(self, xml_file_path: str):
        self._set_root(xml_file_path)
        return {

        }


class ParserFactory:
    @staticmethod
    def get_parser(xml_type: str):
        parsers = {
            'knm': KnmParser,
            'pv': PvParser,
        }
        if xml_type not in parsers:
            raise ValueError(f'Неизвестный тип XML файла')
