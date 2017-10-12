class BaseExpander():
    @classmethod
    def get_instructions(cls):
        return {method: getattr(cls, method) for method in dir(cls) if hasattr(getattr(cls, method), 'is_instruction')}

    @classmethod
    def instruction(cls, f):
        f.is_instruction = True
        return staticmethod(f)
