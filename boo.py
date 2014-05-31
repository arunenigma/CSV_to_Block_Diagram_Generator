class A(object):
    name = 'a'

    def __init__(self):
        self.name = 'A'


class B(A):
    name = 'b'

    def __init__(self):
        super(B, self).__init__()
        self.name = 'B'

    def boo(self):
        print self.name + 'boo'


class C(A):
    name = 'c'

    def __init__(self):
        super(C, self).__init__()
        self.name = 'C'

    def boo(self):
        print self.name + 'coo'


class D(C, B):
    name = 'd'

    def __init__(self):
        super(D, self).__init__()

if __name__ == '__main__':
    a = A()
    print a.name
    print A.name

    d = D()
    #print D.__mro__
    print d.name
    d.boo()