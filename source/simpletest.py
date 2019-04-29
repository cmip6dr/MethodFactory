from MethodFactory import Add

def m1(self,x):
    print ('%s received' % x )

@Add(m1,name='test')
class C1(object):
    pass

c = C1()
c.test( 'Message' )
