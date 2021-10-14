from ._records import FunctionHistory

class Variable:

    def __init__(self, initial_value, context, name=None):
        self.context = context 
        if name == None:
            name = type(initial_value)
        self.name = name
        self.calls = 1
        self.__name__ = name
        self.actions = []
        self.funcname = f"{name}_init"
        self.v = initial_value
        self.context._history(FunctionHistory(self, [self], self.calls, self))
    
    def __repr__(self):
        return f"b.Variable( {self.name} )"

    def __str__(self):
        return f"b.Variable( {self.name} )"
        
    def update(self, new_value):
        self.v = new_value
        return self

