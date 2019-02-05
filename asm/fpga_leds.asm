.text
  .global main:

; displays the value in the D register
; pollutes the A register
leds_display:
    PSH D
    ; push address of leds, and write option
    LDV A, (0b1000000000)
    LSH A, 4
    INC A
    PSH A
    SYS
    RET

sleep:
    LDV A, 0
    LDV C, while_sleep:
    LDV B, 0
    while_sleep:
    INC B
    NOP
    NOP
    NOP
    NOP
    JLT B, C
    RET

main:
    LDV A, leds_display:
    LDV D, (0b11010)
    CAL A

    LDV A, sleep:
    CAL A

    LDV A, leds_display:
    LDV D, (0b00110)
    CAL A

    LDV A, sleep:
    CAL A

    JMP main:
