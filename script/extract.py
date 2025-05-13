#!/bin/python3
from subprocess import run

def extract_symbol_size(obj, *, section=""):
    '''
    obj: Path-like object pointing to ELF binary
    section: Sequence of characters holding section letter to include
    
    returns [symbol name, section letter, symbol size, start address]
    '''
    def parse(line):
        parts = line.split()    # [start address, size, section letter, symbol]
        if len(parts) == 2:
            return [parts[1], parts[0], 0, 0]
        if len(parts) == 3:
            return [parts[2], parts[1], 0, int(parts[0], 16)]

        return [parts[3], parts[2], int(parts[1], 16), int(parts[0], 16)]

    output = run(["nm", "--print-size", obj], text=True, capture_output=True)

    if output.returncode != 0:
        raise ValueError(output.stderr)

    parsed = [parse(x) for x in output.stdout.splitlines()]
    return parsed if section == "" else [x for x in parsed if x[1] in section]

if __name__ == "__main__":
    from sys import argv
    if len(argv) < 2:
        print(f"Usage: {argv[0]} [path-to-binary] <section letter>")
        print("\tRefer to `man nm` to see the list of section letters")
        exit(1)

    target_bin = argv[1]
    section = "" if len(argv) <= 2 else argv[2]
    symbols = extract_symbol_size(target_bin, section=section)
    for s in symbols:
        print(s)
