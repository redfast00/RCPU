import RCPU.assembler.preprocessor as p


def test_remove_whitespace():
    lines = [
        "\tMOV 1, 5   ",
        "    MOV 5,6\t"
    ]
    assert p.remove_whitespace(lines) == ["MOV 1, 5", "MOV 5,6"]


def test_remove_comments():
    lines = [
        ";this is a comment;",
        "MOV 4, 6",
        ";another comment"
    ]
    assert p.remove_comments(lines) == ["MOV 4, 6"]


def test_split_into_sections():
    lines = [".data", '.test string "TEST"', '.lambda 5', '.text',
             "MOV A, 5", "LDV A, 5"]
    assert p.split_into_sections(lines) == (['.test string "TEST"', '.lambda 5'],
                                            ["MOV A, 5", "LDV A, 5"])
    lines = [".data", ".text", "MOV A, 5"]
    assert p.split_into_sections(lines) == ([], ["MOV A, 5"])
    lines = [".text", "MOV A, 5"]
    assert p.split_into_sections(lines) == ([], ["MOV A, 5"])


def test_find_index():
    assert p.find_index(['.test', 'test', 't'], '.test') == 0
    assert p.find_index(['one', 'two', 'three'], 'four') is None
