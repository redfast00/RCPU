from .utils import execute_code
from RCPU.assembler.utils import AssemblerException
import pytest

def test_unknown_reg():
    program = '''
        .data
        .teststr string 'ABCDEF'
        .text
        .global main:
        main:
        LDV G, .teststr
        HLT
    '''
    with pytest.raises(AssemblerException) as excinfo:
        c = execute_code(program)
    assert "Unknown register" in str(excinfo.value)

def test_too_big_LDV():
    program = '''
        .text
        .global main:
        main:
        LDV A, 2000000
        HLT
    '''
    with pytest.raises(AssemblerException) as excinfo:
        c = execute_code(program)
    assert "LDV: Memory address" in str(excinfo.value)

def test_too_big_LDA():
    program = '''
        .text
        .global main:
        main:
        LDA A, 2000000
        HLT
    '''
    with pytest.raises(AssemblerException) as excinfo:
        c = execute_code(program)
    assert "LDA: Memory address" in str(excinfo.value)

def test_too_big_LDM():
    program = '''
        .text
        .global main:
        main:
        LDM A, 2000000
        HLT
    '''
    with pytest.raises(AssemblerException) as excinfo:
        c = execute_code(program)
    assert "LDM: Memory address" in str(excinfo.value)

def test_too_big_JMP():
    program = '''
        .text
        .global main:
        main:
        JMP 2000000
        HLT
    '''
    with pytest.raises(AssemblerException) as excinfo:
        c = execute_code(program)
    assert "JMP: Memory address" in str(excinfo.value)