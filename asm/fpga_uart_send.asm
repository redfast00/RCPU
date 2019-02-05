.text
  .global main:

main:
retry:

; push address of misc.in (which contains if uart is writeable), and read option
LDV B, (0b110)
PSH B
SYS
; pop read value in B
POP B
; get last bit: AND with 1
LDV A, 1
AND A, B
; if A now contains 1, that means we can write to uart
LDV C, retry:
LDV B, 1
; if A == 0, then A < B and we will retry
JLT B, C

; else write to uart
; 0b0111_0110 = 'v'
LDV A, (0b0111_0110)
PSH A
LDV A, (0b1001)
PSH A
SYS
JMP main:

HLT
