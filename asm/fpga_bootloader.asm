.text
  .global main:

; (blocking) reads one char from uart to the D register
; pollutes A, B, C, D
; needs 1 stack space
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
; needs 2 stack space
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

; blocking, reads two chars from uart into a 16-bit value into the D register
; the first character is the most significant byte, the second character the least
; pollutes A, B, C, D
read_16_bits_from_uart:
    LDV A, uart_read_char:
    CAL A
    ; D contains the first 8 bits of the address, shift it and push it onto the stack
    LSH D, 7
    LSH D, 1
    PSH D
    LDV A, uart_read_char:
    CAL A
    ; D now contains the last 8 bits of the address

    POP C
    ; C now contains the first 8 bits of the address

    OR D, C
    ; now D contains the full address
    RET

main:
    ; send a single '>'
    LDV A, uart_send_char:
    LDV D, 62
    CAL A

    LDV A, read_16_bits_from_uart:
    CAL A
    ; push the address onto the stack
    PSH D
    LDV A, read_16_bits_from_uart:
    CAL A
    ; the value to load is now in the D register
    POP C
    LDP C, D
    ; The first ever instruction will be a jump to main
    ; this makes it easy to transfer control flow to the now-loaded program:
    ; you just need to overwrite the jump in address 0 with a jump to your loaded program
    JMP 0
