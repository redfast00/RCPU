.text
  .global main:

test:
    LDV A, 20
    PSH A
    POP D
    RET

main:
    LDV A, test:
    CAL A
    HLT
