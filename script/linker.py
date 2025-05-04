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

        # return f"{self.sections[0]} = ALIGN({page_size})\n" + "\n".join(self.symbols[1:])
        return "\n".join(map(lambda s: f"*({s})", self.sections))


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
        # return f"{self.name} ALIGN({page_size}): {{\n{"\n".join(entries)}\n}}"
        return f"{self.name} : {{\n{'\n'.join(entries)}\n}}"

'''
TODO: Add support for page alignment
The lines commented out were early attempts at alignment but they are not the correct linker syntax...
'''
