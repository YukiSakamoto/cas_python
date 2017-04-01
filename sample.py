from symbol import *

c1 = NodeDouble(1.0)
c5 = NodeDouble(5.0)
x = NodeVariable("x")

binder = dict()
binder["x"] = 0.56

s = NodeCos(c5)
print s
print s.differentiate(x).reduction()

expr =  x * 5.0 * x
print "{} = {}".format(expr, expr.eval(binder))
print "{} = {}".format(expr.differentiate(x), expr.differentiate(x).eval(binder) )
print "{} = {}".format(expr.differentiate(x).reduction(), expr.differentiate(x).eval(binder) )


