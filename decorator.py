'''
# ����Ƕ��װ���� װ��������ֻ���ڵ�һ��ԭ��������ʱ����
def deco(func):
    print("before myfunc() called.")
    func()
    print("after myfunc() called.")
    return func

@deco
def myfunc():
    print(" myfunc() called.")

myfunc()
myfunc()
'''
'''
# ����Ƕ��װ���� װ��������ÿ�ζ��ᱻ����
def deco(func):
    def warper():
        print("before myfunc() called.")
        func()
        print("after myfunc() called.")
        return func
    return warper


@deco
def myfunc():
    print(" myfunc() called.")

myfunc()
myfunc()
'''

#��������װ�κ���
def deco(func):
    def warper(a, b):
        print("before myfunc() called.")
        ret = func(a, b)
        print("after myfunc() called. ret=", ret)
        return ret
    return warper


@deco
def myfunc(a, b):
    print(" myfunc() called.")
    return a+b

myfunc(1,2)
myfunc(3,4)