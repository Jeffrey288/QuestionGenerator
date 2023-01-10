import random
import numpy as np
import math
from functools import reduce

def is_int(x): return (abs(x - int(x)) < 1e-6)

# https://github.com/nbice1/Polynomial-Class/blob/master/Polynomial-Class.py
class Polynomial:
    # @property
    # def coeffs(self): return self.coeffs
    # @coeffs.setter
    # def coeffs(self, val):
    #     if not all(isinstance(item, int) for item in val):
    #         val = [int(item) for item in val]
    #     self._coeffs = val

    def __init__(self, coefficients):
        coeffs = []
        for r in coefficients:
            coeffs.append(float(r))
        self.coeffs = coeffs
        
    # string representation of polynomials of the form 'a(0)z**n +...+ a(n-1)z + a(n)', where a(i) are the coeffs
    def __str__(self):
        string = ""
        add_str = " + "
        for n in range(len(self.coeffs)):
            n_coeff = str(self.coeffs[n])
            if n < len(self.coeffs) - 2:
                string = string + n_coeff + "z**"+ \
                str(len(self.coeffs) - n - 1) + add_str
            elif n < len(self.coeffs) - 1:
                string = string + n_coeff + "z" + add_str
            else:
                string = string + n_coeff
        return string
    def __repr__(self):
        return str(self)
    
    # method returns the coefficient attached to the variable raised to the ith power
    def coeff(self, i):
        if 0 <= i < len(self.coeffs):
            return self.coeffs[-1 - i]
        else:
            return 0.0

    # method for adding two polynomials and returning their sum
    def add(self, other):
        rev_poly = []
        rev_self_coeffs = self.coeffs[::-1]
        rev_other_coeffs = other.coeffs[::-1]
        
        #loops over reversed lists of coeffs, adding together coeffs at the same position in the list (corresponding to the 
        #variable raised to the same power), followed by adding extra terms in case the initial polynomial has higher degree
        for n in range(len(rev_self_coeffs)):
            if n <= len(rev_other_coeffs) - 1:
                rev_poly.append(rev_self_coeffs[n] + rev_other_coeffs[n])
            else:
                rev_poly.append(rev_self_coeffs[n])
                
        #if condition catches extra terms in case the second polynomial has higher degree
        if len(rev_other_coeffs) > len(rev_self_coeffs):
            for n in range(len(rev_self_coeffs), len(rev_other_coeffs)):
                rev_poly.append(rev_other_coeffs[n])
                
        #the new list of coeffs is created by reversing the constructed list rev_poly, followed by returning the new 
        #initialized polynomial
        new_poly = rev_poly[::-1]
        return Polynomial(new_poly)
    def __add__(self, other):
        return self.add(other)
    
    # method for multiplying two polynomials and returning the resulting polynomial
    def mul(self, other):
        new_poly = Polynomial([0])
        rev_self_coeffs = self.coeffs[::-1]
        rev_other_coeffs = other.coeffs[::-1]
        
        for n in range(len(rev_self_coeffs)):
            if n == 0:
                rev_poly_term = [r * rev_self_coeffs[n] for \
                r in rev_other_coeffs]
            else:
                rev_poly_term = [0 for m in range(n)] + \
                [r * rev_self_coeffs[n] for r in rev_other_coeffs]
            poly_term = rev_poly_term[::-1]
            new_poly = new_poly + Polynomial(poly_term)
        return new_poly
    def __mul__(self, other):
        return self.mul(other)
    
    # method for evaluating a polynomial by setting the variable z equal to the input value v
    def val(self, v):
        rev_self_coeffs = self.coeffs[::-1]
        value = 0
        
        for n in range(len(rev_self_coeffs)):
            value = value + rev_self_coeffs[n]*(v**(n))
        return value
    def __call__(self, v):
        return self.val(v)

    def roots(self):
        return list(np.roots(self.coeffs))

    def div(self, poly):
        q, r = np.polydiv(np.array(self.coeffs), np.array(poly.coeffs))
        return Polynomial(q), Polynomial(r)


from fractions import Fraction
def randomLinearRoot(f = 0.3, a = None) -> Fraction:
    if a is None:
        if (random.random() < f):
            return Fraction(random.choice([1, -1]) * random.randint(2, 9), random.randint(2, 5))
        else:
            return random.choice([1, -1]) * random.randint(1, 8)
    else:
        return Fraction(random.choice([1, -1]) * random.randint(2, 9), a)

def polynomialFromRoot(root: Fraction) -> Polynomial:
    return Polynomial([root.denominator, -root.numerator])

def randomLinearFactor(f = 0.3):
    return polynomialFromRoot(randomLinearRoot(f))

def factors(n: int):    
    # https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
    return list(set(map(int, (reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))))

def randomQuadraticFactor(option: str = "distinct", a = None, f = 0.8) -> Polynomial:
    if option == "distinct-int":
        a1 = None if a is None else random.choice(factors(abs(a)))
        a2 = None if a1 is None else int(a / a1)
        root1 = randomLinearRoot(a = a1)
        while (root2 := randomLinearRoot(a = a2)) == root1: pass
        return polynomialFromRoot(root1) * polynomialFromRoot(root2)
    elif option == "equal-int":
        root1 = randomLinearRoot()
        return polynomialFromRoot(root1) * polynomialFromRoot(root1)

    while True:
        if a is None:
            a = (1 if (random.random() < f) else random.randint(2, 4)) #  random.choice([1, -1]) * 
        b = random.randrange(-13, 13)
        thresh = b**2 - 4 * a
        # b^ - 4ac = disc
        # 
        try:
            if option == "distinct":
                # b^2 - 4ac > 0 -> c < thresh (a > 0)
                if a < 0: c = random.randrange(max(-13, math.ceil(thresh)), 13)
                else: c = random.randrange(-13, min(math.floor(thresh), 13))
            elif option == "equal": # no recommended
                # b^2 - 4ac > 0 -> c < thresh (a > 0)
                c = thresh
            elif option == "complex":
                if a > 0: c = random.randrange(max(-13, math.ceil(thresh)), 13)
                else: c = random.randrange(-13, min(math.floor(thresh), 13))
            else:
                c = random.randrange(-13, 13)
        except:
            continue
        
        return Polynomial([a, b, c])

        
# # print(polynomialFromRoot(randomLinearRoot()))
# count = 0
# ones = 0
# while True:
#     count += 1
#     k = (randomQuadraticFactor("equal-int"))  
#     print(k)
#     # if (k.coeffs[0] == 1): ones += 1
#     # print(ones, count)/

x = randomLinearFactor(f = 0.5)
q = randomQuadraticFactor()
r = randomLinearFactor()
p = x * q + r
print(f"""
When {p} is dividied by {q}, the remainder is {r}.
""")

while True:
    r1 = randomLinearRoot(f = 0.5)
    r2 = randomLinearRoot()
    r3 = randomLinearRoot()
    if (r1 == -r2 or r2 == -r3 or r3 == -r1): continue
    x1 = polynomialFromRoot(r1)
    x2 = polynomialFromRoot(r2)
    x3 = polynomialFromRoot(r3)
    p = x1 * x2 * x3
    xr = randomQuadraticFactor("distinct-int", a = random.choice(factors(p.coeff(3))))
    q, r = p.div(xr)
    if (abs(r.coeff(0)) < 10 and abs(r.coeff(1)) < 70
    and is_int(r.coeff(0)) and is_int(r.coeff(1))
    and r.coeff(0) != 0 and r.coeff(1) != 0): break
print(f"""
Let f(x) = {p}. When f(x) is divided by {xr}, the remainder is {r}.
It is given that {x1} is a factor of f(x).
""")


"""


"""



