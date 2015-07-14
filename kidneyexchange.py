#!/usr/bin/python

from gurobipy import *

vertices  = range(5)
edges = { (0,1) : 1, (1,0) : 1, (0,2) : 1, (2,0) : 1,
          (0,4) : 1, (4,0) : 1, (1,4) : 1, (4,1) : 1,
          (1,3) : 1, (3,1) : 1, (2,3) : 1, (3,2) : 1,
          (3,4) : 1, (4,3) : 1 }

def twoCycle(vertices, edges):
    '''
    Returns a dictionary of 2 cycles. Keys: (u,v), Value: weight of cycle
    Note that u < v to not double count cycles.
    '''
    twoCycles = {}
    for edge in edges:
        u = edge[0]
        v = edge[1]
        if (u < v and (v,u) in edges):
            twoCycles[(u,v)] = edges[(u,v)] + edges[(v,u)]
    return twoCycles

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

twoCycles = twoCycle(vertices,edges)
threeCycles = threeCycle(vertices,edges)

for cycle in twoCycles:
    print cycle

for cycle in threeCycles:
    print cycle

m = Model()

c = {}

for cycle in twoCycles:
    c[cycle] = m.addVar(vtype=GRB.BINARY, name="c_%s" % str(cycle))

for cycle in threeCycles:
    c[cycle] = m.addVar(vtype=GRB.BINARY, name="c_%s" % str(cycle))

m.update()

for v in vertices:
    constraint = 0
    for cycle in c:
        if (v in cycle):
            constraint = constraint + c[cycle]
    m.addConstr( constraint <= 1 , name="v%d" % v)

m.setObjective( quicksum( c[cycle] * twoCycles[cycle] for cycle in twoCycles ) +
                quicksum( c[cycle] * threeCycles[cycle] for cycle in threeCycles ),
                GRB.MAXIMIZE )

m.optimize()

for v in m.getVars():
    if (v.X):
        print v
