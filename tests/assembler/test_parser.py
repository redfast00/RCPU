import RCPU.assembler.parser as p
import pytest

def test_is_label():
    assert(p.is_label('label:'))
    assert(p.is_label('a:'))

def test_is_instruction():
    assert(p.is_instruction("ldv a, 0"))
    assert(p.is_instruction("ldv D, .result"))
    assert(p.is_instruction("ldv D, done:"))

def test_parse_resource():
    assert (".test", 5) == p.parse_resource(".test 5")
    assert (".str", "test") == p.parse_resource(".str string 'test'")
    assert (".tst", " *1* ") == p.parse_resource(".tst string ' *1* '")
    assert (".tst", "test\n") == p.parse_resource(".tst string 'test\\n'")
    label, allocated = p.parse_resource(".alloc allocate 20")
    assert label == '.alloc'
    assert len(allocated) == 19
    with pytest.raises(Exception) as excinfo:
        p.parse_resource(".test list [1,2]")
        assert "Unknown resource type" in str(excinfo.value)
    with pytest.raises(Exception) as excinfo:
        p.parse_resource(".alloc allocate 0")
        assert "Size of allocated memory" in str(excinfo.value)

def test_parse_instruction():
    assert ("MOV", ["B", "A"]) == p.parse_instruction("MOV B,A")
    assert ("MOV", ["B", "A"]) == p.parse_instruction("MOV B, A")
    assert ("SYS", []) == p.parse_instruction("SYS")
    assert ("PSH", ["A"]) == p.parse_instruction("psh A")
    assert ("LDV", ["D", "done:"]) == p.parse_instruction("ldv D, done:")
    assert ("LDV", ["b", ".times"]) == p.parse_instruction("ldv b, .times")

def test_parse_global():
    assert "main:" == p.parse_global(".global main:")

def test_is_reference():
    assert not p.is_reference("50")
    assert p.is_reference(".test")

def test_unparse_instruction():
    assert "MOV A,B" == p.unparse_instruction("MOV", ["A","B"])
    assert "SYS" == p.unparse_instruction("SYS", [])
    assert "PSH A" == p.unparse_instruction("PSH", ["A"])