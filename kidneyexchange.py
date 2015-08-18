#!/usr/bin/python

from gurobipy import *

# Note that these are in in different format than data received
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

def optimize(vertices, edges, output=False):
    twoCycles = twoCycle(vertices,edges)
    threeCycles = threeCycle(vertices,edges)

    m = Model()

    if not output:
        m.params.OutputFlag = 0

    m.setParam('TimeLimit', 10)
    
    c = {}

    for cycle in twoCycles:
        c[cycle] = m.addVar(vtype=GRB.BINARY, name="c_%s" % str(cycle))

    for cycle in threeCycles:
        c[cycle] = m.addVar(vtype=GRB.BINARY, name="c_%s" % str(cycle))

    m.update()

    for v in vertices:
        constraint = []
        for cycle in c:
            if (v in cycle):
                constraint.append(c[cycle])
        if constraint:
            m.addConstr( quicksum( constraint[i] for i in range(len(constraint)) ) <= 1 , name="v%d" % v)

    m.setObjective( quicksum( c[cycle] * twoCycles[cycle] for cycle in twoCycles ) +
                    quicksum( c[cycle] * threeCycles[cycle] for cycle in threeCycles ),
                    GRB.MAXIMIZE )

    m.optimize()
    
    if (m.status != 2):
        return ["error"]

    solution = []

    for cycle in c:
        if (c[cycle].X > .5):
            solution.append(cycle)

    return solution

# Because javascript does not have tuples, need to change data structures
# We receive edges as {edgeweight: list of edges (as arrays)} and want to transform
# this to {edge (as tuple): edgeweight}
def transform(nodes, edges, output=False):
    newNodes = range(len(nodes))
    newEdges = {}
    for edgeweight in edges:
        for edge in edges[edgeweight]:
            newEdges[(edge[0], edge[1])] = float(edgeweight)
    return optimize(newNodes, newEdges, output)

def handleoptimize(jsdict):
    if 'nodes' in jsdict and 'edges' in jsdict:
        solution = transform(jsdict['nodes'], jsdict['edges'])
        return {'solution': solution }

if __name__ == '__main__':
    import json
    jsdict = json.load(sys.stdin)
    jsdict = handleoptimize(jsdict)
    print 'Content-Type: application/json\n\n'
    print json.dumps(jsdict)
