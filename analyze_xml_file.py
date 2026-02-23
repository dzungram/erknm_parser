import xml.etree.cElementTree as ET
from pathlib import Path

def analyze_xml_file(file_paths: list) -> dict:

    structures = {}

    for file_path in file_paths:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            structures[file_path] = {
                'root_tag': root.tag,
                'root_attributes': root.attrib,
                'child_tags': [child.tag for child in root],
                'sample_size': len(root)
            }
        except Exception as e:
            print(f'Error {file_path}: {e}')

    return structures

if __name__ == '__main__':
    p = Path('data')
    absolute_paths = []
    for item in p.iterdir():
        if item.is_file() and item.suffix == '.xml':
            absolute_paths.append(str(item.resolve()))

    for file, info in analyze_xml_file(absolute_paths).items():
        print(f'{file}: {info}')