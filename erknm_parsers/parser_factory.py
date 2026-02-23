class ErknmParserFactory:

    def __init__(self):
        self.parsers = []

    def register_parser(self, parser_class):
        self.parsers.append(parser_class)

    def get_parser(self, file_path: str):
        for parser_class in self.parsers:
            parser = parser_class(file_path)
            if parser.can_parse():
                return parser
        return None