import bread as b
import time


d = b.variable(2, name="var1")
e = b.variable(3, name="var2")
c = b.variable(0, name="var3")
f = b.variable(0, name="var4")

tracked = [d, e, c]

@b.function
def add_1(x):
    return x.v + 1

@b.function
def add(x, y):
    return x.v + y.v

@b.function
def add3(x, y, z):
    return x.v + y.v + z.v

add(d, e, output=d) #1 

add_1(d, output=d) #1

add(d, f, output=f) #2

add_1(d, output=d) #2 

add_1(f, output=f) #3

add(d, f, output=f) #3

add3(f, e, d, output=f) #1

add3(f, c, e, output=e) #2

add_1(e, output=e) #4 


graph = b.Graph()
