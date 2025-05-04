#!/bin/python3
from extract import extract_symbol_size
from linker import *

target_bin = "./build/array.o"
symbols = extract_symbol_size(target_bin, section="Tt")
mid = len(symbols) // 2

page1 = LinkPage()
for s in symbols[:mid]:
    page1.add_section(f".text.{s[0]}", s[2])

page2 = LinkPage()
for s in symbols[mid:]:
    page2.add_section(f".text.{s[0]}", s[2])

text = LinkSection(".text")
text.add_page(page1)
text.add_page(page2)

script = text.compile(4 * 1024)
with open("linker/array.bfd.t", "w") as f:
    f.write(script)
