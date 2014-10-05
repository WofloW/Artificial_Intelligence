#!/usr/bin/env python
import buildGraph
import searchQueues
import argparse




### A NodeFactory is a helper class that is used to create new Nodes.
### It stores the graph representing our problem and uses it to find successors.
class NodeFactory :
    def __init__(self, inputgraph) :
        self.inputgraph = inputgraph

    ### return a list of all nodes reachable from this state
    ### you complete this. 
    ### For a given node, find the corresponding vertex in the input graph.
    ### Find the vertices it is connected to, and generate a Node for each
    ### one. Update parentState and cost to reflect the new edge added to the
    ### solution.
    ### nlist is a list of successor nodes.

    def successors(self, oldstate) :
        #add code here
        nlist=[]
        edge_list = self.inputgraph.adjlist[oldstate.vertex.name]
        for i in edge_list[1:]:
            current_vertex = self.inputgraph.adjlist[i.dest][0]
            nlist.append(Node(current_vertex, oldstate, float(i.distance[:-2])+oldstate.cost, oldstate.depth+1))
        return nlist



class Node:
    def __init__(self, vertex, parentState=None, cost=0, depth=0) :
        self.vertex = vertex
        self.parent = parentState
        self.cost = cost
        self.depth = depth
    def isGoal(self, goalTest) :
        return goalTest(self)
    def isStart(self) :
        return self.parent is None
    def __repr__(self) :
        return self.vertex.__repr__()
    def __hash__(self) :
        return self.vertex.__hash__()
    ## you do this.
    def __lt__(self, other) :
        return self.cost < other.cost
    def __le__(self, other) :
        return self.cost <= other.cost
    def __gt__(self, other) :
        return self.cost > other.cost
    def __ge__(self, other) :
        return self.cost >= other.cost
    def __eq__(self, other) :
        return self.vertex == other.vertex
    def __ne__(self, other) :
        return self.vertex != other.vertex
        
### search takes as input a search queue, the initial state,
### a node factory,
### a function that returns true if the state provided as input is the goal,
### and the maximum depth to search in the search tree.
### It should print out the solution and the number of nodes enqueued, dequeued,
###  and expanded.
def search(queue, initialState, factory, goalTest, maxdepth) :
    closedList = {}
    nodesEnqueued = 1
    nodesDequeued = 0
    nodesExpanded = 0

    queue.insert(initialState)
    while not queue.isEmpty():
        nodesDequeued = nodesDequeued +1
        if isinstance(queue,searchQueues.AStarQueue):
            current = queue.pop()[1]
        else:
            current = queue.pop()
        if current.isGoal(goalTest):
            return current,nodesEnqueued,nodesDequeued,nodesExpanded
        if factory.inputgraph.adjlist[current.vertex.name] == []:
            continue
        if current.depth < maxdepth:
            nodesExpanded = nodesExpanded+1
            for i in factory.successors(current):
                if i not in closedList.keys():
#                if i not in queue.q:
                    queue.insert(i)
                    nodesEnqueued = nodesEnqueued+1
            closedList[current]= True
    return queue.goal,nodesEnqueued,nodesDequeued,nodesExpanded


def search_IDAStar(queue, initialState, factory, goalTest, cost_limit) :
    closedList = {}
    nodesEnqueued = 1
    nodesDequeued = 0
    nodesExpanded = 0
    min_cost=float("inf")

    queue.insert(initialState)
    while not queue.isEmpty():
        nodesDequeued = nodesDequeued +1
        current = queue.pop()
        cost = current[0]
        current = current[1]
        if current.isGoal(goalTest):
            return current,nodesEnqueued,nodesDequeued,nodesExpanded,cost
        if factory.inputgraph.adjlist[current.vertex.name] == []:
            continue
        if cost > cost_limit:
            if cost <min_cost:
                min_cost=cost
        else:
            nodesExpanded = nodesExpanded+1
            for i in factory.successors(current):
                if i not in closedList.keys():
                    queue.insert(i)
                    nodesEnqueued = nodesEnqueued+1
            closedList[current]= True
    return queue.goal,nodesEnqueued,nodesDequeued,nodesExpanded,min_cost




### you complete this. 
### While there are states in the queue,
###   1. Dequeue
###   2. If this is the goal, stop
###   3. If not, insert in the closed list and generate successors
###   4. If successors are not in the closed list, enqueue them.
### code for printing out a sequence of states that leads to a solution
def printSolution(node) :
    print "Solution *** "
    print "cost: ", node.cost, "km"
    moves = []
    current = node
    while not current.isStart():
        moves.append(current)
        current = current.parent
    moves.append(current)
    moves.reverse()
    for move in moves :
        print move


### usage: search --search=[BFS| DFS | AStar] {-l=depthLimit} {-i}
###               initialState goal infile
###
### If -l is provided, only search to the given depth.
### if -i is provided, use an iterative deepening version (only applies
        ### to DFS, 10pts extra credit for IDA*)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''search --search=[BFS| DFS | AStar] {-l=depthLimit} {-i}
                                                    initialState goal infile''')
    parser.add_argument('--search', type=str, choices=['BFS','DFS','AStar'],
                        help='''choose method you want to use for search [BFS| DFS| AStar]''')
    parser.add_argument('-l', type=int, default=float('inf'), help='''depthLimit of the tree''')
    parser.add_argument('-i', action="store_true", help='''use an iterative deepening version only applies to DFS''')
    parser.add_argument('initialState', type=str, help='''starting point of this search''')
    parser.add_argument('goal', type=str, help='''goal of this search''')
    parser.add_argument('infile', type=str, help='''the name of a file to use as input''')
    args = parser.parse_args()

#    args = parser.parse_args('--search AStar -i CableCarMuseum GhirardelliSquare sfdata2.txt'.split())
    # args = parser.parse_args("--search BFS  Pier39 TransamericaPyramid  inputFile".split())

    g = buildGraph.Graph(args.infile)

    nf= NodeFactory(g)
    goal = Node(nf.inputgraph.adjlist[args.goal][0], None, float("infinity"))
    initialState= Node(nf.inputgraph.adjlist[args.initialState][0],None,0,0)

    if args.search == 'BFS':
    # for example if BFS is the input, start by:
        q = searchQueues.BFSQueue(goal)
    elif args.search == 'DFS':
        q = searchQueues.DFSQueue(goal)
    elif args.search == 'AStar':
        q = searchQueues.AStarQueue(goal)
    else:
        print '--search [BFS DFS AStar]'

    #if -i is provided, use an iterative deepening version (only applies to DFS)
    if args.i and args.search == 'DFS':
        # Avoid that (args.l = inf) causes infinite loop when initialState can't reach the goal
        if args.l == float('inf'):
            args.l = len(nf.inputgraph.adjlist.keys())-1
        depth = 1
        while depth<=args.l:
            calc_goal,nodesEnqueued,nodesDequeued,nodesExpanded=search(q, initialState, nf, q.goalTest, depth)
            if calc_goal.cost != float('inf'):
                break
            depth = depth +1
    elif args.i and args.search == 'AStar':
        cost_limit = q.latlong_to_distance(initialState)
        temp = float('inf')
        #Avoid infinite loop when initialState can't reach the goal
        while temp != cost_limit:
            calc_goal,nodesEnqueued,nodesDequeued,nodesExpanded, limit=search_IDAStar(q, initialState, nf, q.goalTest, cost_limit)
            temp = cost_limit
            cost_limit = limit
            if calc_goal.cost != float('inf'):
                break
    else:
        calc_goal,nodesEnqueued,nodesDequeued,nodesExpanded=search(q, initialState, nf, q.goalTest, args.l)

    print "nodesEnqueued:", nodesEnqueued
    print "nodesDequeued:", nodesDequeued
    print "nodesExpanded:", nodesExpanded
    printSolution(calc_goal)

    

