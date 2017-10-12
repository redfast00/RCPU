import RCPU.assembler.assembler as a
import pytest


def test_create_resourcetable():
    data = [".format string 'test'", '.test string "test"', '.number 5']
    expected = {
        '.format': 'test',
        '.test': 'test',
        '.number': 5
    }
    assert a.create_resourcetable(data) == expected


def test_replace_labels():
    text = [
        "main:",
        "JMP main:",
        "JMP test:",
        "MOV A,B",
        "MOV A,test:",
        "test:",
        "HLT"]
    expected = [
        "JMP 0",
        "JMP 4",
        "MOV A,B",
        "MOV A,4",
        "HLT"
    ]
    assert a.replace_labels(text) == expected


def test_generate_datasection():
    resourcetable = {'.first': 'firstval', '.second': 'secondval', '.number': 42}
    text = [
        "MOV A, .first",
        "MOV B, .first"
    ]
    # Check that string is only included once
    t, d = a.generate_datasection(text, resourcetable)
    assert t == ["MOV A, 2", "MOV B, 2"]
    assert d == [ord(char) for char in "firstval"] + [0]
    # Check that numbers are included
    text = [
        "MOV A, .number"
    ]
    t, d = a.generate_datasection(text, resourcetable)
    assert t == ["MOV A, 42"]
    assert d == []
    # Check that an unsupported type in the resourcetable raises an Exception
    resourcetable = {'.first': [1, 2, 3]}
    text = ["MOV A, .first"]
    with pytest.raises(Exception) as excinfo:
        t, d = a.generate_datasection(text, resourcetable)
    assert "Unsupported resource type" in str(excinfo.value)


def test_replace_entrypoint():
    text = [".global main:", "main:", "INC A", "JMP main:"]
    expected = ["JMP main:", "main:", "INC A", "JMP main:"]
    assert a.replace_entrypoint(text) == expected
