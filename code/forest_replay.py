"""Independent finite-order comparison using an unrestricted rooted forest recurrence."""
from math import sqrt
import numpy as np


def maxima(n, max_radius):
    # An allowed edge to branch of b vertices contributes b(n-b).
    # Track the number of children reaching the maximum permitted height,
    # clipped to 2. Components are indexed by order b-1 after deletion
    # of their root. -10^15 is a sentinel below all possible test scores.
    bad=-10**15
    last=np.full((3,n),bad,dtype=np.int64)
    last[0,0]=0
    vals={}
    for radius in range(1,max_radius+1):
        sizes=np.arange(1,n,dtype=np.int64)
        edge=sizes*(n-sizes)
        if radius==1:
            short=np.full(n-1,bad,dtype=np.int64)
            long=np.full(n-1,bad,dtype=np.int64)
            long[0]=int(edge[0])
        else:
            short=edge+last[0,:n-1]
            long=edge+last[1:,:n-1].max(axis=0)
        current=np.full((3,n),bad,dtype=np.int64)
        current[0,0]=0
        for s in range(1,n):
            old=current[:,s-1::-1]
            current[0,s]=np.max(old[0,:]+short[:s])
            current[1,s]=max(np.max(old[0,:]+long[:s]),np.max(old[1,:]+short[:s]))
            current[2,s]=max(np.max(old[1,:]+long[:s]),np.max(old[2,:]+short[:s]),np.max(old[2,:]+long[:s]))
        vals[2*radius]=int(current[2,n-1])
        side=current[1:,:n-1].max(axis=0)
        vals[2*radius+1]=int(np.max(side+side[::-1]+edge))
        last=current
    return vals


if __name__ == '__main__':
    for n in (10,30,54,100,250,1000,3000):
        result=maxima(n,4)
        print('n',n,'M_d for d=4..9:',[result[k] for k in range(4,10)])
        print('diam8 remainder / sqrt(n)',(result[8]-(4*n*n-sqrt(70)*n**1.5-n))/sqrt(n))
