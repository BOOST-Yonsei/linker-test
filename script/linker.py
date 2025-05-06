#!/bin/python3

class LinkPage():
    def __init__(self):
        self.sections = []
        self.size = 0

    def add_section(self, sym, size):
        self.sections.append(sym)
        self.size += size

    def compile(self, page_size):
        assert len(self.sections) > 0
        assert 0 <= self.size <= page_size

        entries = [f"*({s})" for s in self.sections]
        return f"    . = ALIGN({page_size});\n" + "    " + "\n    ".join(entries)


class LinkSection():
    '''
    LinkSection {
        name: str = <name of section in binary>
        pages: list[LinkPage] = <list of pages>
    }
    '''
    def __init__(self, name):
        self.name = name
        self.pages = []

    def add_page(self, page):
        self.pages.append(page)

    def compile(self, page_size):
        assert len(self.pages) > 0
        entries = [x.compile(page_size) for x in self.pages]
        joined = '\n\n'.join(entries)
        total_length = len(self.pages) * page_size
        return (
            "ENTRY(_start)\n\n"
            "MEMORY {\n"
            "  RAM (rx) : ORIGIN = 0x400000, LENGTH = {total_length}\n"
            "}\n\n"
            f"SECTIONS {{\n"
            f"  . = ORIGIN(RAM);\n"
            f"  {self.name} : ALIGN({page_size}) {{\n"
            f"{joined}\n"
            f"  }} > RAM\n"
            f"}}"
        )
