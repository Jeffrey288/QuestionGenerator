from sympy import *

t = symbols('t')

hey = sympify('-33/2*t**2+3/4*t+423')
hey2 = Poly(hey).all_coeffs()
print(hey2)
hey3 = [Mul(UnevaluatedExpr(Rational(coeff)), UnevaluatedExpr(t**i)) for i, coeff in enumerate(hey2[::-1])]
UnevaluatedExpr(Rational(-33,2))
pprint(hey)
pprint(hey3)