import RCPU.assembler.parser as p

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

def test_parse_instruction():
    assert ("MOV", ["B", "A"]) == p.parse_instruction("MOV B,A")
    assert ("MOV", ["B", "A"]) == p.parse_instruction("MOV B, A")
    assert ("SYS", []) == p.parse_instruction("SYS")
    assert ("PSH", ["A"]) == p.parse_instruction("psh A")
    assert ("LDV", ["D", "done:"]) == p.parse_instruction("ldv D, done:")
    assert ("LDV", ["b", ".times"]) == p.parse_instruction("ldv b, .times")