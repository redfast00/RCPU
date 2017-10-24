include syscall
.data
  .format string '%d test\n'

.text
  .global main:

main:
  ; Print 20
  LDV A, 20
  PSH A
  LDV A, .format
  PSH A
  LDV A, .sys_printf
  PSH A
  SYS
  HLT