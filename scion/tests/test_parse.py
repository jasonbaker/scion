from scion.parse import get_syntax_tree_from_str

def test_float():
    result = get_syntax_tree_from_str('3.5')
    assert result[0] == 3.5

def test_int():
    result = get_syntax_tree_from_str('3')
    assert result[0] == 3

def test_list():
    result = get_syntax_tree_from_str('(1 2 3)')
    assert result.asList() == [1, 2, 3]

def test_empty_list():
    result = get_syntax_tree_from_str('()')
    assert not result.asList()

def test_comment():
    result = get_syntax_tree_from_str('(1 #foo\n2)')
    assert result.asList() == [1, 2]

def test_var():
    result = get_syntax_tree_from_str('x')
    assert result.asList() == ['x']

def test_none():
    result = get_syntax_tree_from_str('nil')
    assert result.asList() == [None]
