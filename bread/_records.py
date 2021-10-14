class FunctionHistory: 
    def __init__(self, function, inputs, inst, output):
        self.func = function 
        self.id = inst
        self.inputs = inputs
        self.output = output
        self.__name__ = self.func.funcname + "\\" + str(self.id)

    def __hash__(self):
        return hash(self.func.funcname) + self.id
    def __str__(self):
        return f"{self.func.funcname}\{self.id}: <{' '.join([str(x) for x in self.inputs])}> -> {str(self.output)}"
    def __repr__(self):
        return f"{self.func.funcname}\{self.id}: <{' '.join([str(x) for x in self.inputs])}> -> {str(self.output)}"

