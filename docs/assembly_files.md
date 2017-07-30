# Syntax for assembly files

## Comments and indentation
Comments are lines beginning with (optional) whitespace and a semicolon (`;`).
Indentation gets ignored.

## Sections
Every assembly file can contain two sections: an optional `.data` section and a
 required `.text` section. The `.data` section
 comes first in the file.

### .data section
The `.data` section contains data like strings and constants. There are three
 types of resources in the `.data` sections: number constants, strings and allocations.

- Number constants look like `.num 5`: `.num` is the name of the label and `5` is
 the constant. Number constants aren't modifiable at runtime since when the binary
 gets assembled, they just get replaced in the instructions.

- Strings look like `.str string 'Test \n'`: `.str` is the name of the label and
 `Test \n` is the string that will be placed in memory. Strings are modifiable
 at runtime. If the label isn't used in the `.text` section, the string won't be
 placed in the binary.

- Allocations look like `.alloc allocate 5`: `.alloc` is the name of the label and
 `5` is the size of the buffer that will be allocated when the binary is assembled.
 Memory will only be allocated if the label is used in the `.text` section.
 The allocated memory will be "dirty", so you can't count on it having a certain value.

### .text section
The `.text` section contains an entrypoint, instructions and labels:

- The entrypoint comes at the beginning of the `.text` section and looks like
 `.global main:`, where `main:` is the label that the program will start at.

- Instructions aren't case sensitive, but are uppercase in the documentation for
 legibility and consistency. An instruction can reference a resource declared in
 the `.data` section. For example `LDV A, .const` will load the number declared in
 the `.data` section by the `.const` label into the `A` register.

- Labels can be placed in instructions and as arguments in instructions. A label
 will have the value of the place in the binary when the binary is assembled. The
 main use for labels is for branching instructions.


## Example of assembly file
This program prints "Your text was (This is a test) and you number was (5)" to
 stdout.
```
.data
    .teststring string 'This is a test'
    .testnumber 5
    .format string 'Your text was (%s) and your number was (%d)\n'
    .sys_printf 0

.text
.global main:
    main:
        ; Push the number onto the stack
        LDV A, .testnumber
        PSH A
        ; Push the address of the string onto the stack
        LDV A, .teststring
        PSH A
        LDV A, .format
        PSH A
        ; Push the syscall number of prinf onto the stack
        LDV A, .sys_printf
        PSH A
        SYS
        HLT
```
