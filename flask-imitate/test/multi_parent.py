#encoding:utf8


class A(object):
    def run(self):
        print 'A.run'

class B(object):
    def run(self):
        print 'B.run'
        

class C(object):
    def run(self):
        print 'C.run'

# 根据顺序调用        
class D(B,C,A):
    """
    multi parent
    """

def test_case_1():
    d=D()
    d.run()
test_case_1()