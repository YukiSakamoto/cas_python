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
        if isinstance(rhs, float):
            rhs_ = NodeDouble(rhs)
        else:
            rhs_ = rhs
        return NodePlus(self, rhs_)
    def __sub__(self, rhs):
        if isinstance(rhs, float):
            rhs_ = NodeDouble(rhs)
        else:
            rhs_ = rhs
        return NodeMinus(self, rhs_)
    def __mul__(self, rhs):
        if isinstance(rhs, float):
            rhs_ = NodeDouble(rhs)
        else:
            rhs_ = rhs
        return NodeMul(self, rhs_)
    def __div__(self, rhs):
        if isinstance(rhs, float):
            rhs_ = NodeDouble(rhs)
        else:
            rhs_ = rhs
        return NodeDiv(self, rhs_)
    def nterm(self):
        return 0
    def reduction(self):
        return self
    def partial_apply(self, partial_binder):
        self.partial_binder = partial_binder

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
        if self in binder:
            return binder[self]
        else:
            raise
    def __hash__(self):
        return hash(self.name)
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
    def reduction(self):
        red_l = self.lhs.reduction()
        red_r = self.rhs.reduction()
        if isinstance(red_l, NodeDouble) and red_l == NodeDouble(0.0):
            return NodeDouble(1.0)
        elif isinstance(red_r, NodeDouble) and red_l == NodeDouble(0.0):
            return NodeDouble(1.0)
        else:
            return NodePow(red_l, red_r)

class NodeSin(NodeAbstract):
    def __init__(self, theta):
        self.theta = theta
    def eval(self, binder):
        theta_ = self.theta.eval(binder)
        return math.sin(theta_)
    def __str__(self):
        return "sin({})".format(self.theta)
    def differentiate(self, var):
        return self.theta.differentiate(var) * NodeCos(self.theta)

class NodeCos(NodeAbstract):
    def __init__(self, theta):
        self.theta = theta
    def eval(self, binder):
        theta_ = self.theta.eval(binder)
        return math.cos(theta_)
    def __str__(self):
        return "cos({})".format(self.theta)
    def differentiate(self, var):
        return NodeDouble(-1.0) * self.theta.differentiate(var) * NodeSin(self.theta)

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
    def reduction(self):
        red_l = self.lhs.reduction()
        red_r = self.rhs.reduction()
        if isinstance(red_l, NodeDouble) and red_l == NodeDouble(0.0):
            return red_r
        elif isinstance(red_r, NodeDouble) and red_r == NodeDouble(0.0):
            return red_l
        else:
            return NodePlus(red_l, red_r)

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
    def reduction(self):
        red_l = self.lhs.reduction()
        red_r = self.rhs.reduction()
        if isinstance(red_l, NodeDouble) and red_l == NodeDouble(0.0):
            return NodeDouble(0.0)
        elif isinstance(red_l, NodeDouble) and red_l == NodeDouble(1.0):
            return red_r
        elif isinstance(red_r, NodeDouble) and red_r == NodeDouble(0.0):
            return NodeDouble(0.0)
        elif isinstance(red_r, NodeDouble) and red_r == NodeDouble(1.0):
            return red_l
        else:
            return NodeMul(red_l, red_r)

class NodeDiv(NodeBinary):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    def eval(self, binder):
        return self.lhs.eval(binder) / self.rhs.eval(binder)
    def __str__(self):
        return "{} / {}".format(self.lhs, self.rhs)

def sin(val):
    return NodeSin(val)

def steepest_descent(function, var_list, start_coord, 
        max_cycle = 5, grad_criteria = 0.05, diff_criteria = 0.05, factor = 0.1):
    # var_list: list of variables
    # start_coord : dict of variables and its values

    if factor <= 0:
        raise

    print function
    current_coord = start_coord
    partial_differential_map = dict() 
    for var in var_list:
        partial_differential_map[var] = function.differentiate(var).reduction() 
        print "df/d{}  = {}".format(var, partial_differential_map[var])

    diff = float('inf')
    grad = float('inf')
    prev_val = float('inf')

    for ncycle in range(max_cycle):
        val = function.eval(current_coord)
        grad_map = dict()
        for var, par_diff in partial_differential_map.items():
            grad_map[var] = par_diff.eval(current_coord)
        diff = val - prev_val
        grad = sum(grad_map.values() )

        print "Value: {}  Diff: {}  Grad: {} Coord: {}".format(val, diff, grad, current_coord)
        if ncycle == 0 and  abs(grad) < grad_criteria:
            print "break1"
            break
        elif abs(grad) < grad_criteria and abs(diff) < diff_criteria:
            print "break2"
            break
        else:
            # enter the next step
            for (var, t) in grad_map.items():
                current_coord[var] = current_coord[var] - t * factor
            prev_val = val
        
    return 0

