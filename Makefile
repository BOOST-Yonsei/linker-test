.PHONY: clean help

SRCS=$(wildcard src/*.c)
OPTS=-std=c11 -Werror -Wpedantic -Wall -Wredundant-decls

help:
	@echo 'make <target> will build and execute <target>'
	@echo -e '\tValid targets:' $(SRCS:src/%.c=%)

clean:
	rm -rf build/

# Execute target
.PRECIOUS: build/%
%: build/%
	./$<

# Build target
build/%:: src/%.c
	mkdir -p build
	gcc $(OPTS) -o $@ -Wall $<
