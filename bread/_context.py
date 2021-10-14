from ._function import Function
from ._variable import Variable

class Context:
    def __init__(self):
        self.record = []

    def _history(self, function):
        self.record.append(function)
    
    def function(self, function):
        return Function(function, self)

    def variable(self, initial, name=None):
        return Variable(initial, self, name)

ctx = Context()
