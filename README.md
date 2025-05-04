# Binary relocation with linker script

This repo contains a sample program and various scripts to re-order the location of its functions within the compiled binary.

This repo has been tested for GCC under linux

## Extracting function symbols

Compile with `-ffunction-sections -c` to assign a separate ELF section for each function. The `-c` option is needed to create an object file otherwise the compiler will merge the sections back into a single `.text` section automatically.

The section name of each function will be `.text.{function name}`.

Extracting the symbol and its size can be done using `nm --print-size`.  
Section letter `T` and `t` indicates it is in the `.text` section, where the lowercase suggests the symbol is local only.

## Compiling source with linker script

Compile with the following flags to compile source code with the given linker file:

`-ffunction-sections -Wl,--section-ordering-file <linker file>`
