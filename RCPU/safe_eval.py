# https://stackoverflow.com/a/30516254
import ast
import math

locals = {key: value for (key, value) in vars(math).items() if key[0] != '_'}
locals.update({"abs": abs, "complex": complex, "min": min, "max": max, "pow": pow, "round": round})


class Visitor(ast.NodeVisitor):
    def visit(self, node):
        if not isinstance(node, self.whitelist):
            raise ValueError(node)
        return super(Visitor, self).visit(node)

    whitelist = (ast.Module, ast.Expr, ast.Load, ast.Expression, ast.Add, ast.Sub, ast.UnaryOp, ast.Num, ast.BinOp,
                 ast.Mult, ast.Div, ast.Pow, ast.BitOr, ast.BitAnd, ast.BitXor, ast.USub, ast.UAdd, ast.FloorDiv, ast.Mod,
                 ast.LShift, ast.RShift, ast.Invert, ast.Call, ast.Name)


def safe_eval(expr, locals={}):
    if any(elem in expr for elem in '\n#'):
        raise ValueError(expr)
    try:
        node = ast.parse(expr.strip(), mode='eval')
        Visitor().visit(node)
        return eval(compile(node, "<string>", "eval"), {'__builtins__': None}, locals)
    except ValueError:
        raise ValueError(expr)
