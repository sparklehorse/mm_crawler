'''
# 无内嵌包装函数 装饰器函数只会在第一次原函数调用时调用
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
# 有内嵌包装函数 装饰器函数每次都会被调用
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

#带参数的装饰函数
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