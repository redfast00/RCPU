#!/bin/bash

# compile, assemble and emulate

LANG=brainfuck

if [ $# -ne 1 ]; then
  echo "Arguments"
  exit 1
fi

python3 -m RCPU.compile $1 $LANG > assembly.asm.out
python3 -m RCPU.assemble assembly.asm.out final.out
python3 -m RCPU.emulate final.out
