from xml.etree.ElementTree import ElementTree as ET

class ErknmParser:
    def __init__(self):
        self.root = None
        self.ns = None

    def _set_root(self, xml_file_path:str):
        self.root = ET.parse(xml_file_path).getroot()


class KnmParser(ErknmParser):
    def __init__(self):
        super().__init__()

    def parse(self, xml_file_path:str):
        self._set_root(xml_file_path)

