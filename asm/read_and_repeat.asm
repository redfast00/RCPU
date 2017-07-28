.data
  .format string 'You wrote: %s, and that was %d characters long.\n'
  .printf 0
  .fgets 1
  .stdin_fileno 0
  .size 20
  .free_memory string 'AAAAAAAAAAAAAAAAAAA'


.text
  .global main:

main:
  ; Get string of size 20 from stdin
  LDV A, .stdin_fileno
  PSH A
  LDV A, .size
  PSH A
  LDV A, .free_memory
  PSH A
  LDV A, .fgets
  PSH A
  SYS
  ; Print the format string
  LDV A, .free_memory
  PSH A
  LDV A, .format
  PSH A
  LDV A, .printf
  PSH A
  SYS
  hlt