import numpy as np
from scipy.spatial.transform import Rotation as R

# A=np.array([ 2, 11 ,-1] )
# B=np.array([6, 3,9])
# C=np.cross(A, B)
# C=C/np.gcd.reduce(C)/9
# E=5/9*(A+4*B)/5
# G=E-C
# print(C)
# print(E)
# print(G)

def is_int(x): return np.all(np.abs(x - np.int_(x)) < 1e-6)

def centroid(x, y, z): return (x + y + z)/3

def incenter(x, y, z):
    a = np.linalg.norm(y-z)
    b = np.linalg.norm(x-z)
    c = np.linalg.norm(x-y)
    return (a*x + b*y + c*z)/(a + b + c)

def circumcenter(x, y, z):
    n = np.cross(x-y, y-z)
    lx = np.cross(y-z, n)
    ly = np.cross(x-z, n)
    temp = np.linalg.inv(np.vstack((lx[:2], -ly[:2])).T) @ (x - y)[:2] / 2
    return (y+z)/2 + temp[0] * lx

def orthocenter(x, y, z):
    n = np.cross(x-y, y-z)
    lx = np.cross(y-z, n)
    ly = np.cross(x-z, n)
    temp = np.linalg.inv(np.vstack((lx[:2], -ly[:2])).T) @ (y - x)[:2]
    return x + temp[0] * lx


def proj(x, y):
    return y * np.dot(x, y) / np.dot(y, y)

# A,B,C,G=(11, -2, 2), (1, 8, 6) ,(7, 4, 4), (-7, -10, 4)
# A=np.array(A)
# B=np.array(B)
# C=np.array(C)
# M=np.array(G)
# AD=proj(B-A,C-A)
# #AD = OD-OA=>OD=AD+OA
# D = A+AD
# AE=proj(C-A,B-A)
# E = A+AE
# DB=B-D
# EC=C-E
# print(AD,AE,DB,EC)
# print(np.dot(B-A,C-A), np.dot(A-C,A-C), (C-A), B-A)
# F=(A+C)/2
# G=(A+B)/2
# print(F, G)
# K=np.array([11,-2,6])
# print(np.dot(K-A, np.cross(B-A,C-A)))
# print(np.linalg.norm(M-K), np.linalg.norm(M-A)**2)
# # P=G-(A-G)
# # print(np.linalg.norm(P-G), P)
# exit()
# A = [5, 9 ,0]; A=np.array(A)
# B= [ 1,  2, -1]; B=np.array(B)
# C= [-6, -2, -2]; C=np.array(C)
# H= [ 20., -17.,  -1.]; H=np.array(H)
# print(np.linalg.norm(A-B), np.linalg.norm(A-C), np.linalg.norm(C-B))

# print(B-A, C-B, C-A)
# print(np.cross(B-A, C-B))
# print(np.cross(C-B, np.cross(B-A, C-B)))
# print(np.cross(C-A, np.cross(B-A, C-B)))

# exit()
# A = np.array([2, 11, -1])
# B = np.array([6, 3, 9])
# C = np.array([4, 5, 6])
while True:
    A = np.random.randint(24, size=(3)) - 12
    B = np.random.randint(24, size=(3)) - 12
    C = np.random.randint(24, size=(3)) - 12
    # A = np.array([4, -3, 5])
    # B = np.array([6, 7, 8])
    # C = np.random.randint(100, size=(3)) - 12
    # c, b, a = np.linalg.norm(A-B), np.linalg.norm(A-C), np.linalg.norm(C-B)
    # if (a!=b or b!=c): continue
    # print("yay")
    try:
        G = centroid(A, B, C)
        I = incenter(A, B, C)
        H = orthocenter(A, B, C)
        O = circumcenter(A, B, C)
    except KeyboardInterrupt:
        exit()
    except:
        continue
    if (not is_int(O)): continue
    if (not np.all(abs(O) < 40)): continue
    if (np.all(np.int_(O) == A)): continue
    if (np.all(np.int_(O) == B)): continue
    if (np.all(np.int_(O) == C)): continue
    if (not is_int(H)): continue
    if (not np.all(abs(H) < 40)): continue
    if (np.all(np.int_(H) == A)): continue
    if (np.all(np.int_(H) == B)): continue
    if (np.all(np.int_(H) == C)): continue
    # if (np.linalg.norm(A-B) != np.linalg.norm(B-C) and ): continue
    # if (np.all(H != O)): continue

    print(tuple(A), tuple(B), tuple(C), tuple(np.int_(O)), tuple(np.int_(H))) # tuple((I)), tuple((G)), tuple((H))
    c, b, a = np.linalg.norm(A-B), np.linalg.norm(A-C), np.linalg.norm(C-B)
    print(a, b, c, a==b, b==c, a==c)
    # print(centroid(A, B, C))
    # print(incenter(A, B, C))
    # print(orthocenter(A, B, C))
    # print(circumcenter(A, B, C))  
