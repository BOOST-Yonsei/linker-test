#!/bin/python3

import re
from collections import defaultdict
from extract import extract_symbol_size

def get_page_info(obj, page_size):
    '''
    obj: Path-like object pointing to ELF binary

    returns {function name: [start address, last address]},
            {function name: [start page, last page]},
            min page, max page
    '''
    pg_min = 1 << 64
    pg_max = 0

    info = {}
    multipage = {}
    for name, _, size, addr in extract_symbol_size(obj, section="Tt"):
        if size <= 0:
            continue

        lastaddr = addr + size - 1
        info[name] = (addr, lastaddr)

        pg_start = addr // page_size
        pg_last = lastaddr // page_size
        if pg_start != pg_last:
            multipage[name] = (pg_start, pg_last, size)

        pg_min = min(pg_min, pg_start)
        pg_max = max(pg_max, pg_last)

    return info, multipage, pg_min, pg_max

def get_trace_functions(path):
    '''
    path: Path-like object pointing to trace data file

    returns [function name]

    TODO: Add function exit context instead of entry only
    '''
    pattern = re.compile(r"\|\s+([a-zA-Z0-9_]+)\(\)")
    functions = []
    with open(path) as f:
        for line in f:
            res = pattern.search(line)
            if res:
                functions.append(res.group(1))

    return functions

def get_page_sequence(func_info, trace, page_size, page_min = 0):
    '''
    func_info   : {function name : [start address, last address]}
    trace       : [function name]
    page_min    : min page accessed
    '''
    log = []
    missing = defaultdict(int)  # Likely due to compiler inlining
    for func in trace:
        if func not in func_info:
            missing[func] += 1
            continue

        addr, lastaddr = func_info[func]
        for pg in range(addr // page_size, lastaddr // page_size + 1):
            log.append(pg - page_min)

    return log, missing

def get_accessed_size(func_info, trace, page_size):
    '''
    func_info   : {function name : [start address, last address]}
    trace       : [function name]

    returns sum(size of functions accessed in trace)
    '''
    size = 0
    for func in set(trace):
        if func in func_info:
            start, last = func_info[func]
            size += last - start + 1

    return size, -(size // -page_size)


if __name__ == "__main__":
    from sys import argv
    import json
    if len(argv) < 3:
        print(f"Usage: {argv[0]} [path-to-binary] [path-to-trace] <page size>")
        exit(1)

    bin_file = argv[1]
    trace_file = argv[2]
    page_size = 4096 if len(argv) <= 3 else argv[3]

    func_info, multipage, pg_min, pg_max = get_page_info(bin_file, page_size)
    trace = get_trace_functions(trace_file)
    page_seq, missing = get_page_sequence(func_info, trace, page_size, pg_min)
    access_size, access_pg = get_accessed_size(func_info, trace, page_size)

    try:
        print(f"Page range: 0x{pg_min:_X}, 0x{pg_max:_X}")
        print(f"Page count: {pg_max - pg_min + 1}")
        print(f"Pages accessed: {len(set(page_seq))}")
        print(f"Minimum required: {access_size:,} B -> {access_pg:} pages")
        print("Missing (inlined) functions:")
        print(json.dumps(missing))
        print("Functions across page boundaries:")
        print(json.dumps(multipage))
        print("Accessed page id:")
        print(page_seq)
    except:
        ...
