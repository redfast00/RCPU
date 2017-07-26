from . import arithmetic
from . import utilexpander

_all_classes = [arithmetic.ArithmeticExpander, utilexpander.UtilExpander]
mapping = {}
for c in _all_classes:
    mapping.update(c.get_instructions())