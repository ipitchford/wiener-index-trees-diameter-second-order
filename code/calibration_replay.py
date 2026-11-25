"""Independent numerical sanity checks for the quartic certificate and its mesh trial."""
from math import isqrt, sqrt

a = sqrt((7 - sqrt(7))/6)
def ratio(x):
    return 1/(2*x) + x - x**3/7
K = ratio(a)
lo, hi = sqrt(2), 3
for _ in range(64):
    m = (lo + hi)/2
    if ratio(m) >= K:
        lo = m
    else:
        hi = m
b = (lo+hi)/2
def V(t,x):
    if x > b*sqrt(t):
        return K*x*t**1.5
    return t*t/2 + t*x*x - x**4/7
def dyadic(h):
    top = h+.5
    x=a*sqrt(top)
    m=x
    k=1
    A=0
    E=0
    while m*m/2>=1:
        bot = int(m*m/2)+.5
        A += k*(top*top-bot*bot)/2
        E += k*(top-bot)*m*m
        top=bot
        m=m/2
        k*=2
    A+=k*(top*top-.25)/2
    E+=k*(top-.5)*m*m
    return (A+E)/(x*(h+.5)**1.5)
grid = [j/64 for j in range(257)]
err = max(V(1,u+w)-V(1,u)-V(1,w) for u in grid for w in grid)
print("a, b and K",a,b,K)
print("worst split excess",err,"over",len(grid)**2,"pairs")
for h in [10,100,1000,10000,100000,1000000]:
    print("h",h,"cost normalised by (h+.5)^1.5",dyadic(h))
print("tree constant",K/2**1.5)
