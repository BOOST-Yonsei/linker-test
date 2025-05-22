#!/bin/python3

import re
from tracepage import get_page_info, get_accessed_size, get_page_sequence

def parse_ktrace(path):
    '''
    Example
    #           TASK-PID     CPU#  |||||  TIMESTAMP  FUNCTION
    #              | |         |   |||||     |         |
        kworker/3:1-51      [003] d..3.    11.064989: update_min_vruntime <ffffffdfdbeddc0c> <-update_curr <ffffffdfdbee2388>
        kworker/3:1-51      [003] d..3.    11.064989: cpuacct_charge <ffffffdfdbefcf3c> <-update_curr <ffffffdfdbee2478>
        kworker/3:1-51      [003] d..3.    11.064990: __update_load_avg_se <ffffffdfdbef28c4> <-update_load_avg <ffffffdfdbee14f4>
    '''
    funcs = set()
    pattern = re.compile(r":\s+([a-zA-Z0-9_]+)\s+")
    with open(path) as f:
        for line in f:
            res = pattern.search(line)
            if res:
                funcs.add(res.group(1))

    return funcs

def generate_linker(funcs, format="gold"):
    '''
    Format for gold linker
    '''
    if format == "gold":
        body = '\n'.join(map(lambda s: f".text.{s}", funcs))
        catch = ".text.*"
    elif format == "bfd":
        body = '\n'.join(map(lambda s: f"*(.text.{s})", funcs))
        catch = "*(.text.*)"
    elif format == "lld":
        body = '\n'.join(funcs)
        raise ValueError(f"How to do catch all without messing up hibernate section?")
    else:
        raise ValueError(f"Unknown format: {format}")
    return f".text : {{\n{body}\n{catch}\n}}"


if __name__ == "__main__":
    from sys import argv
    if len(argv) < 2:
        print(f"Usage: {argv[0]} [path-to-trace]\n\tGenerate linker script to coalesce functions based on trace data")
        print()
        print(f"Usage: {argv[0]} [path-to-trace] <path-to-binary>\n\tAnalyze page access of trace data for the given binary")
        exit(1)

    if len(argv) == 2:
        trace = parse_ktrace(argv[1])
        output = generate_linker(trace, "bfd")
        print(output)
    else:
        pgsize = 4096
        func_info, multipage, pg_min, pg_max = get_page_info(argv[2], pgsize)
        trace = parse_ktrace(argv[1])
        page_seq, missing = get_page_sequence(func_info, trace, pgsize, pg_min)
        access_size, access_pg = get_accessed_size(func_info, trace, pgsize)

        try:
            print(f"Page range: 0x{pg_min:_X}, 0x{pg_max:_X}")
            print(f"Page count: {pg_max - pg_min + 1}")
            print(f"Pages accessed: {len(set(page_seq))}")
            print(f"Minimum required: {access_size:,} B -> {access_pg:} pages")
        except:
            ...
