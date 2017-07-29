.data
  .format string '%d test'
  .printf 0

.text
  .global main:

main:
  ; Print 20
  LDV A, 20
  PSH A
  LDV A, .format
  PSH A
  LDV A, .printf
  PSH A
  SYS
  HLT