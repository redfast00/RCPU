from .utils import execute_code


def test_printf(capsys):
    program = '''
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
    '''
    c = execute_code(program)
    out, err = capsys.readouterr()
    assert out == "20 test"
    assert c.registers.sp == 0
