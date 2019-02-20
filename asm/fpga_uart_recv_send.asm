.text
  .global main:

; (blocking) reads one char from uart to the D register
; pollutes A, B, C, D
uart_read_char:
  ; push address of misc.in (which contains if uart is writeable/readable), and read option
  LDV B, (0b110)
  PSH B
  SYS
  ; pop read value in B
  POP B
  ; get second-to-last bit: AND with 2
  LDV A, 2
  AND A, B
  ; if A now contains 2, that means we can read from uart
  LDV C, uart_read_char:
  LDV B, 2
  ; if A == 0, then A < B and we will retry
  JLT B, C

  ; read from uart to D register

  LDV A, (0b1010)
  PSH A
  SYS
  POP D
  RET

; (blocking) write the D register to uart
; pollutes A, B, C
uart_send_char:
    LDV B, (0b110)
    PSH B
    SYS
    ; pop read value in B
    POP B
    ; get last bit: AND with 1
    LDV A, 1
    AND A, B
    ; if A now contains 1, that means we can write to uart
    LDV C, uart_send_char:
    LDV B, 1
    ; if A == 0, then A < B and we will retry
    JLT B, C

    ; else write to uart
    PSH D
    LDV A, (0b1001)
    PSH A
    SYS
    RET

main:
    LDV A, uart_send_char:
     ; '|'
    LDV D, 124
    CAL A
    LDV A, uart_send_char:
    ; '>'
    LDV D, 62
    CAL A
    LDV A, uart_read_char:
    CAL A
    ; D contains the read character
    INC D
    LDV A, uart_send_char:
    CAL A
    JMP main:
