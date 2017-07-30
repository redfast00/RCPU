[![Build Status](https://travis-ci.org/redfast00/RCPU.svg?branch=master)](https://travis-ci.org/redfast00/RCPU)
[![codecov](https://codecov.io/gh/redfast00/RCPU/branch/master/graph/badge.svg)](https://codecov.io/gh/redfast00/RCPU)
# Documentation for RCPU

This is a VM CPU emulator written in Python.
The size of instructions and memory cells are 16 bits.
The specs for this project (CPU instructions and architecture) are heavily inspired by [16bitjs by Francis Strokes](https://francisstokes.wordpress.com/2017/07/20/16-bit-vm-in-javascript/).

## Installation and usage

Just clone the GitHub repo
```
git clone https://github.com/redfast00/RCPU
```
Assemble an assembly file with:
```
python -m RCPU.assemble asm/printf.asm printf.out
```
and then execute it with:
```
python -m RCPU.emulate printf.out
```
If you want easier aliases, you can install the project with:
```
python setup.py install
```
and then you can run the commands like:
```
assemble asm/printf.asm printf.out
emulate printf.out
```

## General purpose registers

|Register|Value|
|--------|-----|
|`A`     |`00` |
|`B`     |`01` |
|`C`     |`10` |
|`D`     |`11` |

## Other registers

|Register |Purpose              |
|---------|---------------------|
|`IP`     |`Instruction pointer`|
|`SP`     |`Stack pointer`      |

## Instructions

|Instruction|Arguments|16 bit representation |Description|
|-----------|---------|-------------------------|-------------|
|`MOV`| `D, S`          | `XXXXXXXXSSDD0000` | Move value at source register to destination register|
|`LDV`| `D, V`          | `VVVVVVVVVVDD0001` | Load a value into destination register. The maximum value that can be loaded is 0x3FF (1023). |
|`LDA`| `D, M`          | `MMMMMMMMMMDD0010` | Load a value from memory into destination register. The maximum memory address that can be loaded from is 0x3FF.|
|`LDM`| `D, M`          | `MMMMMMMMMMDD0011` | Load the value in destination register into memory. The maximum memory address that can be loaded to is 0x3FF.|
|`LDR`| `D, S`          | `XXXXXXXXSSDD0100` | Load the value from memory pointed at by the source register into the destination register|
|`LDP`| `D, S`          | `XXXXXXXXSSDD0101` | Load the value in source register into the memory address pointed to by destination register|
|`ATH`| `D, S, O, M, B` | `BBBMOOOOSSDD0110` | Perform an arithmetic operation on the source and destination registers. O specifies the operation (listed below) and M is the mode, where 0 = place result in destination register and 1 = place result in source register. If the instruction is right or left shift then B specifies the shifting value|
|`CAL`| `D`             | `XXXXXXXXXXDD0111` | Call a function in memory pointed at by the destination register|
|`RET`|                 | `XXXXXXXXXXXX1000` | Return from function|
|`JLT`| `D, S`          | `XXXXXXXXSSDD1001` | Jump to memory address pointed at by the source register, if value in the A register is less than value in destination register|
|`PSH`| `S`             | `XXXXXXXXSSXX1010` | Push the value in source register onto the stack|
|`POP`| `D`             | `XXXXXXXXXXDD1011` | Pop the stack into the destination register|
|`SYS`|                 | `XXXXXXXXXXXX1100` | Perform a system call. This is described below in more detail.|
|`HLT`|                 | `XXXXXXXXXXXX1101` | Program halt|
|`JMP`| `M`             | `MMMMMMMMMMXX1110` | Jump to address in memory. Can only jump to memory up to 0x3FF.|
|`JMR`| `S`             | `XXXXXXXXSSXX1111` | Jump to the address pointed at by the source register|

## Pseudo-instructions

| Instruction                    | Description                                                                                                                                                                                                                                                                      |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `SWP D, S`                     | Swaps the values in the source and destination registers.                                                                                                                                                                                                                        |
| `LDV16 D, V`                   | Loads a 16-bits value into the destination register.                                                                                                                                                                                                                             |
| The aliased `ATH` instructions | `ADD`, `SUB`, `SUBS`, `MUL`, `DIV`, `DIVS`, `AND`, `OR`, `XOR` These instructions are aliases for the `ATH` instruction. The instructions ending in `S` load the result into the source register instead of into the destination register. Syntax for `D = D - S` is `SUB D, S`. |
| `LSH D, V`, `RSH D, V`         | Shifts the value in the destination address by the value and stores it back in the destination address.                                                                                                                                                                          |
| `INC D`, `DEC D`               | Increments or decrements the value in the destination register.                                                                                                                                                                                                                  |
| `NOT D`                        | Flips every bit of the destination register.                                                                                                                                                                                                                                     |

## Arithmetic Operation table

|Operation    |Value  |
|-------------|-------|
|`Add`        |`0000` |
|`Subtract`   |`0001` |
|`Multiply`   |`0010` |
|`Divide`     |`0011` |
|`Left shift` |`0100` |
|`Right shift`|`0101` |
|`And`        |`0110` |
|`Or`         |`0111` |
|`Xor`        |`1000` |
|`Not`        |`1001` |
|`Increment`  |`1010` |
|`Decrement`  |`1011` |

## System calls
Syscall numbers and arguments are passed via the stack. For example the assembly code to call `printf '%d' 20`:
```
.data
  .format string '%d'
  .printf 0

.text
  .global main:

main:
  ; Push 20
  LDV A, 20
  PSH A
  ; Push the address of the format string
  LDV A, .format
  PSH A
  ; Push the syscall number
  LDV A, .printf
  PSH A
  sys
  hlt
```

### Syscall table

| Number | Function | Arguments                | Notes                                                                              |
|--------|----------|--------------------------|------------------------------------------------------------------------------------|
| `0`    | `printf` | `fmt, ...`               | Only supports `%s` and `%d` for respectively zero-terminated strings and numbers.  |
| `1`    | `fgets`  | `*str, size, stream_num` | Only supports stdin for now.                                                       |

# Roadmap

- [ ] Assembler
    - [ ] add support for including files (\*.inc), write .inc file for all syscalls
    - [ ] add support for macro's
    - [ ] add more expanders
        - [ ] conditional branching (NEQ, ...)
    - [x] add a way to reserve memory for strings
    - [x] add support for escaped characters in string
- [ ] CPU: add more syscalls
    - [x] reading stdin
    - [ ] parsing input from stdin
    - [ ] reading/writing to files
- [ ] Make a compiler for a certain language (maybe a language like Forth?)
- [x] Write more tests, get coverage to 100%
    - [x] Assembler and emulator scripts