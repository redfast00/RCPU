[![Build Status](https://travis-ci.org/redfast00/RCPU.svg?branch=master)](https://travis-ci.org/redfast00/RCPU)
[![codecov](https://codecov.io/gh/redfast00/RCPU/branch/master/graph/badge.svg)](https://codecov.io/gh/redfast00/RCPU)
# Documentation for RCPU

This is a CPU emulator written in Python, without dependencies. This project
is compatible with both Python 2.7 and 3.x.
The size of instructions and memory cells are 16 bits.
The specs for this project (CPU instructions and architecture) are heavily inspired by [16bitjs by Francis Strokes](https://francisstokes.wordpress.com/2017/07/20/16-bit-vm-in-javascript/).
This project consists of:
- An emulator written in Python.
- An assembler written in Python.
- Tests, you'll never guess it, also written in Python.
- A Brainfuck interpreter written in assembly that can be assembled with the included assembler.

See also [RCPU_C](https://github.com/redfast00/RCPU_C), a somewhat limited RCPU emulator written in C.

See also [RCPU_FPGA](https://github.com/redfast00/RCPU_FPGA) for an actual implementation of RCPU
in hardware.

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
To use the Brainfuck interpreter, just do:
```
python -m RCPU.assemble asm/brainfuck.asm brainfuck.out
python -m RCPU.emulate brainfuck.out
```
If you want easier aliases, you can install the project with:
```
python setup.py install
```
and then you can run the commands like:
```
rcpu_assemble asm/printf.asm printf.out
rcpu_emulate printf.out
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

Every instruction consists of 16 bits: the last 4 bits are the opcode
(indicating which instruction is used), the first 12 bits indicate
the arguments.
For example, the instruction `00000000 11 00 0000` (spaces added for
clarity) is a `MOV` instruction that copies the value in the `A`
register to the `D` register.

If there are any `X` in the instructions, that means that the value
is ignored. It's good practice to set these to 0. Note that when assembling to a file,
these instructions are big endian.


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
|`JLT`| `D, S`          | `XXXXXXXXSSDD1001` | Jump to memory address pointed to by the source register, if value in the `A` register is less than value in destination register|
|`PSH`| `S`             | `XXXXXXXXSSXX1010` | Push the value in source register onto the stack|
|`POP`| `D`             | `XXXXXXXXXXDD1011` | Pop the stack into the destination register|
|`SYS`|                 | `XXXXXXXXXXXX1100` | Perform a system call. This is described below in more detail.|
|`HLT`|                 | `XXXXXXXXXXXX1101` | Program halt|
|`JMP`| `M`             | `MMMMMMMMMMXX1110` | Jump to address in memory. Can only jump to memory up to 0x3FF.|
|`JMR`| `S`             | `XXXXXXXXSSXX1111` | Jump to the address pointed at by the source register|

## Pseudo-instructions

These pseudo-instructions aren't real instructions, but are macros
implemented in the assembler that can consist of multiple
instructions.

| Instruction                    | Description                                                                                                                                                                                                                                                                      |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `SWP D, S`                     | Swaps the values in the source and destination registers.                                                                                                                                                                                                                        |
| `LDV16 D, V`                   | Loads a 16-bits value into the destination register.                                                                                                                                                                                                                             |
| The aliased `ATH` instructions | `ADD`, `SUB`, `SUBS`, `MUL`, `DIV`, `DIVS`, `AND`, `OR`, `XOR` These instructions are aliases for the `ATH` instruction. The instructions ending in `S` load the result into the source register instead of into the destination register. Syntax for `D = D - S` is `SUB D, S`. |
| `LSH D, V`, `RSH D, V`         | Shifts the value in the destination address by the value and stores it back in the destination address.                                                                                                                                                                          |
| `INC D`, `DEC D`               | Increments or decrements the value in the destination register.                                                                                                                                                                                                                  |
| `NOT D`                        | Flips every bit of the destination register.                                                                                                                                                                                                                                     |

## Arithmetic Operation table

These are the possible values for the `O` (operation) argument in
the `ATH` instruction.

| Operation     | Value  | Notes                      |
|---------------|--------|----------------------------|
| `Add`         | `0000` |                            |
| `Subtract`    | `0001` | `dst - src`                |
| `Multiply`    | `0010` |                            |
| `Divide`      | `0011` | `dst / src`. Rounds down.  |
| `Left shift`  | `0100` | Operates on `src` register |
| `Right shift` | `0101` | Operates on `src` register |
| `And`         | `0110` |                            |
| `Or`          | `0111` |                            |
| `Xor`         | `1000` |                            |
| `Not`         | `1001` | Operates on `src` register |
| `Increment`   | `1010` | Operates on `dst` register |
| `Decrement`   | `1011` | Operates on `dst` register |

## System calls
Syscall numbers and arguments are passed via the stack. The syscall
number should be on top of the stack, followed by any arguments
needed.

For example the assembly code to call `printf '%d' 20`:
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

| Number | Function | Arguments                | Returns      | Notes                                                                                                         |
|--------|----------|--------------------------|--------------|---------------------------------------------------------------------------------------------------------------|
| `0`    | `printf` | `fmt, ...`               | `void`       | `fmt` is the address of the formatstring to print. Only supports `%s` and `%d` for respectively zero-terminated strings and numbers. Use `%%` for a literal `%`. |
| `1`    | `fgets`  | `*str, size, stream_num` | `chars_read` | Only supports stdin for now. Returns the number of characters read.                                           |
| `2`    | `getc`   | `stream_num`             | `char_read`  | Returns the ASCII code of the character that was read.                                                        |

# Roadmap

- [ ] Assembler
    - [x] add support for including files (\*.inc)
    - [ ] write .inc file for all syscalls
    - [ ] add support for macro's
    - [ ] add more expanders
        - [x] conditional branching (JNE, JGE, JEQ, JGT, JLE)
    - [x] add a way to reserve memory for strings
    - [x] add support for escaped characters in string
    - [ ] add optimizing step (for example, remove POP A, PSH A sequences)
- [ ] CPU: add more syscalls
    - [x] reading stdin
    - [ ] parsing input from stdin
    - [ ] reading/writing to files
- [ ] Docs
    - [X] Add branching pseudo-instructions + mention side effects (none :) )
- [ ] Make a compiler for a certain language (maybe a language like Forth?)
- [x] Write more tests, get coverage to 100%
    - [x] Assembler and emulator scripts
