# Documentation for RCPU

Everything fits inside 16-bits

## General purpose registers

|Register    |Value  |
|-------------|-------|
|`A`        |`00` |
|`B`   |`01` |
|`C`   |`10` |
|`D`     |`11` |

## Other registers

|Register    |Purpose  |
|-------------|-------|
|`IP`        |`Instruction pointer` |
|`SP`   |`Stack pointer` |

## Instructions

|Instruction|Arguments|16 bit representation |Description|
|-----------|---------|-------------------------|-------------|
|`MOV`| `D, S`          | `XXXXXXXXSSDD0000` | Move value at source register to destination register|
|`LDV`| `D, V`          | `VVVVVVVVVVDD0001` | Load a value into destination register. |
|`LDA`| `D, M`          | `MMMMMMMMMMDD0010` | Load a value from memory into destination register|
|`LDM`| `D, M`          | `MMMMMMMMMMDD0011` | Load the value in destination register into memory|
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
|`JMP`| `M`             | `MMMMMMMMMMMM1110` | Jump to address in memory. Can only reference memory up to 0xFFF.|
|`JMR`| `S`             | `XXXXXXXXSSXX1111` | Jump to the address pointed at by the source register|

## Arithmetic Operation table

|Operation    |Value  |
|-------------|-------|
|`Add`        |`0000` |
|`Subtract`   |`0001` |
|`Multiply`   |`0010` |
|`Divide`     |`0011` |
|`Left shift` |`0100` |
|`Right shift`|`0101` |
|`And`        |`0111` |
|`Or`         |`1000` |
|`Xor`        |`1001` |
|`Not`        |`1010` |

## System calls
