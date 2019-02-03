.text
  .global main:

main:

; D = 0
LDV D, 0

loop:

; push D as the value leds will display
PSH D

; push address of leds, and write option
LDV B, (0b1000000000)
LSH B, 4
INC B
PSH B

; do a syscall (this takes an address and maybe a value off the stack)
SYS

; do nothing for a lot of cycles, so the result is visible
LDV A, 0
LDV C, while:
LDV B, 0
while:
INC B
NOP
NOP
NOP
NOP
JLT B, C

; increment D
INC D
JMP loop:
