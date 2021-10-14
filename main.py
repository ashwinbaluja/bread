import bread as b

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

add(d, e, output=d)


add_1(d, output=d)

add(d, f, output=f)


add_1(d, output=d)

add_1(f, output=f)

add(d, f, output=f)

add3(f, e, d, output=f)

add3(f, c, e, output=e)


print(f.v, c.v)

graph = b.Graph()
