#!/usr/bin/python

vertices  = range(5)
edges = { (0,1) : 1, (1,0) : 1, (0,2) : 1, (2,0) : 1,
          (0,4) : 1, (4,0) : 1, (1,4) : 1, (4,1) : 1,
          (1,3) : 1, (3,1) : 1, (2,3) : 1, (3,2) : 1,
          (3,4) : 1, (4,3) : 1 }

def threeCycle(vertices, edges):
    '''
    Returns a dictionary of 3 cycles. Keys: (u,w,v), Value: weight of cycle
    Note that w is always the lowest numbered vertex to not double
    (or triple) count cycles.
    '''
    threeCycles = {}
    for edge in edges:
        u = edge[0]
        v = edge[1]
        for w in vertices:
            if (w >= u or w >= v ):
                break
            if ( (u,w) in edges and (w,v) in edges ):
                threeCycles[(u,w,v)] = edges[(u,v)] + edges[(u,w)] + edges[(w,v)]
    return threeCycles

threeCycles = threeCycle(vertices,edges)

for cycle in threeCycles:
    print cycle
