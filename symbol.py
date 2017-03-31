import math


#==================================================
#   Abstract Node
#==================================================
class NodeAbstract:
    def __init__(self):
        pass
    def eval(self):
        pass
    def differentiate(self, variable):
        pass
    def __add__(self, rhs):
        return NodePlus(self, rhs)
    def __sub__(self, rhs):
        return NodeMinus(self, rhs)
    def __mul__(self, rhs):
        return NodeMul(self, rhs)
    def __div__(self, rhs):
        return NodeDiv(self, rhs)
    def nterm(self):
        return 0
    def reduction(self):
        return self

class NodeUnary(NodeAbstract):
    def nterm(self):
        return 1
class NodeBinary(NodeAbstract):
    def nterm(self):
        return 2

#==================================================
#   Terminal Node
#==================================================
class NodeVariable(NodeUnary):
    def __init__(self, name):
        self.name = name
    def eval(self, binder):
        if self.name in binder:
            return binder[self.name]
        else:
            raise
    def __eq__(self, lhs):
        return self.name == lhs.name
    def differentiate(self, var):
        if self == var:
            return NodeDouble(1.0)
        else:
            return NodeDouble(0.0)
    def __str__(self):
        return self.name

class NodeDouble(NodeUnary):
    def __init__(self, value):
        if isinstance(value, float):
            self.value = value
        else:
            raise
    def eval(self, binder):
        return self.value
    def __eq__(self, lhs):
        return self.value == lhs.value
    def differentiate(self, var):
        return NodeDouble(0.0)
    def __str__(self):
        return "{}".format(self.value)

#==================================================
#   Unary Expression
#==================================================
class NodePow(NodeAbstract):
    def __init__(self, val, exponent):
        if not (isinstance(val, NodeUnary)  and isinstance(exponent, NodeUnary)):
            raise
        self.val = val
        self.exponent = exponent
        
    def eval(self, binder):
        v = self.val.eval(binder)
        exp = self.exponent.eval(binder)
        return math.pow(v, exp)
    def __str__(self):
        return "({} ^ {})".format(self.val, self.exponent)
#==================================================
#   Expression Node
#==================================================
class NodeMinus(NodeBinary):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def eval(self, binder):
        return self.lhs.eval(binder) - self.rhs.eval(binder)
    def differentiate(self, var):
        return self.lhs.differentiate(var) - self.rhs.differentiate(var)
    def __str__(self):
        return "({}) - ({})".format(self.lhs, self.rhs)

class NodePlus(NodeBinary):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def eval(self, binder):
        return self.lhs.eval(binder) + self.rhs.eval(binder)
    def differentiate(self, var):
        return self.lhs.differentiate(var) + self.rhs.differentiate(var)
    def __str__(self):
        return "({}) + ({})".format(self.lhs, self.rhs)

class NodeMul(NodeBinary):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def eval(self, binder):
        return self.lhs.eval(binder) * self.rhs.eval(binder)
    def differentiate(self, var):
        d_lterm = NodeMul( self.lhs.differentiate(var), self.rhs)
        d_rterm = NodeMul( self.lhs, self.rhs.differentiate(var) )
        return NodePlus(d_lterm, d_rterm)
    def __str__(self):
        return "{} * {}".format(self.lhs, self.rhs)
    

class NodeDiv(NodeBinary):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def eval(self, binder):
        return self.lhs.eval(binder) / self.rhs.eval(binder)
    def __str__(self):
        return "{} / {}".format(self.lhs, self.rhs)




c1 = NodeDouble(1.0)
c5 = NodeDouble(5.0)
x = NodeVariable("x")

binder = dict()
binder["x"] = 0.56


expr = c1 * x + c5
print "{} = {}".format(expr.__str__(), expr.eval(binder))
print "{} = {}".format(expr.differentiate(x).__str__(), expr.differentiate(x).eval(binder) )
