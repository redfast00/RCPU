from . import arithmetic

_all_classes = [arithmetic.ArithmeticExpander]
mapping = {}
for c in _all_classes:
    mapping.update(c.get_instructions())