.PHONY: clean help

SRCS=$(wildcard src/*.c)
OPTS=-std=c11 -Werror -Wpedantic -Wall -Wredundant-decls

help:
	@echo 'make <target> will build and execute <target>'
	@echo -e '\tValid targets:' $(SRCS:src/%.c=%)

clean:
	rm -rf build/*
	rm -rf linker/*

# > Binary relocation for array.c
build/array.o: src/array.c build
	gcc $(OPTS) -ffunction-sections -c -o $@ $<

linker/array.bfd.t: script/array.py build/array.o
	./script/array.py

build/array.opt: linker/array.bfd.t src/array.c
	gcc $(OPTS) -ffunction-sections -T linker/array.bfd.t src/array.c -o $@
	# gcc $(OPTS) -ffunction-sections -Wl,--section-ordering-file $^ -o $@
# < Binary relocation for array.c



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Rules below this point are default rules for compiling without relocation #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Execute target
.PRECIOUS: build/%
%: build/%
	./$<

# Build target
build/%:: src/%.c build
	gcc $(OPTS) -o $@ -Wall $<

build:
	mkdir -p build
