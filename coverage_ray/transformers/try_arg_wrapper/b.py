from c import add


class TestAdd:
    def __init__(self, b, c):
        self.b = b
        self.c = c

    def add(self):
        return self.b+self.c


def sub(a, b):
    return a-b


def mul(a, b):
    return a*b


def obj_func(tadd):
    return tadd.add()
