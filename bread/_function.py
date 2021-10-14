from ._variable import Variable
from ._records import FunctionHistory

import inspect

class Function:
    def __init__(self, function, context):
        self.context = context
        self.calls = 0
        self.function = function 
        self.funcname = function.__name__
        
        if callable(function):
            self.funcsig = len(inspect.signature(function).parameters)
        else:
            self.funcsig = 0
        self.f = self._get_function()

    def __call__(self, *args, output=None, **kwargs):
        self.calls += 1
        if output != None:
            output.update(self.f(output, *args, **kwargs))
        else:
            return self.f(output, *args)

    def derivative(self, function):
        self.derivative = function
        return function

    def _get_function(self):
        def innerfunction(output, *args, **kwargs):
            variables = [] 
            paramnum = len([*args])
            if paramnum == self.funcsig:
                for i in args:
                    variables.append(i)
            else:
                raise TypeError(f"{self.funcname}() takes {self.funcsig} positional arguments but {paramnum} were given")
            self.context._history(FunctionHistory(self, variables, self.calls, output))

            return self.function(*args, **kwargs)

        return innerfunction