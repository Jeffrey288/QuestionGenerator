import numpy as np
import random

class Line:

    def __init__(
        self,
        a = None, b = None, c = None,
        m = None, xint = None, yint = None,
        pt1 = None, pt2 = None
    ):  
        def isDef(x): return (x is not None)
        
        """
        a, b, c
        m, xint
        m, yint
        m, pt1
        xint, yint
        pt1, pt2
        """
        pts = []
        if (isDef(xint)): pts.append(np.array([xint, 0.0]))
        if (isDef(yint)): pts.append(np.array([0.0, yint]))
        if (isDef(pt1)): pts.append(np.array(pt1))
        if (isDef(pt2)): pts.append(np.array(pt2))
        if (len(pts) == 0 and isDef(a) and isDef(b) and isDef(c)):
            self.a = a; self.b = b; self.c = c
        elif (len(pts) == 1 and isDef(m)):
            self.a = m; self.b = -1; self.c = pts[0][1] - m * pts[0][0]
        elif (len(pts) == 2 and not isDef(m)):
            m = (pts[1][1] - pts[0][1]) / (pts[1][1] - pts[0][1])
            self.a = m; self.b = -1; self.c = pts[0][1] - m * pts[0][0]
        else:
            raise TypeError("Invalid Initiation")
