__author__ = 'wei fang'

import cPickle as pickle
import argparse

### build graph: 
### takes as input a file in the form:
## a b dist time
### where a and b are destinations, dist is the distance between them, and 
### time is the time needed to travel between them and constructs a graph.

### This graph should be represented as an adjacency list, and stored as a 
### dictionary, with the key in the dictionary being the source of an edge and 
### the value being a tuple containing the destination, distance, and cost.
### For example:
### g[a] = (b,dist,time)

class Graph:
    adjlist = {}
    print_graph_temp ={}
    vertices_list = {}
    def __init__(self, infile=None):
        self.adjlist = {}
#        print 'init'
        if infile:
            self.buildGraph(infile)

    ### method to print a graph.
    def __repr__(self):
        print 'graph:'
        print self.print_graph_temp

    ### helper methods to construct edges and vertices. Use these in buildGraph.
    def createVertex(self, inStr):
        name, lat,longitude = inStr.split(" ",2)
        lat = lat.split("=")[1]
        longitude = longitude.split("=")[1][:-1]
        return Vertex(name, lat, longitude)

    def createEdges(self, inStr):
        src, dest, dist, time = inStr.split(" ",4)
        dist=dist.split("=")[1][:-2]
        time=time.split("=")[1][:-3]
        e1 = Edge(src,dest,dist, time)
        e2 = Edge(dest,src,dist, time)
        return e1,e2

### method that takes as input a file name and constructs the graph described 
### above.
    def buildGraph(self, infile):
        flag_edges = True
#load the vertices
#        print 'start loading vertices'
        instr1 = infile.readline()
        instr1 = infile.readline()
        while 'lat' in instr1:
            self.vertices_list[self.createVertex(instr1).name]= [self.createVertex(instr1).lat, self.createVertex(instr1).longitude]
            instr1 = infile.readline()
#        print self.vertices_list


#load the edges
#        print 'start loading edges'
        instr1 = infile.readline()
        while 'km' in instr1:
            if self.createEdges(instr1)[0].src in self.adjlist:
                self.adjlist[self.createEdges(instr1)[0].src][self.createEdges(instr1)[0].dest] = float(self.createEdges(instr1)[0].distance)
            else:
                self.adjlist[self.createEdges(instr1)[0].src] ={self.createEdges(instr1)[0].dest:float(self.createEdges(instr1)[0].distance)}

            if self.createEdges(instr1)[1].src in self.adjlist:
                self.adjlist[self.createEdges(instr1)[1].src][self.createEdges(instr1)[1].dest] = float(self.createEdges(instr1)[1].distance)
            else:
                self.adjlist[self.createEdges(instr1)[1].src] ={self.createEdges(instr1)[1].dest:float(self.createEdges(instr1)[1].distance)}
            instr1 = infile.readline()

        for i in self.vertices_list.keys():
            for j in self.adjlist[i].keys():
                if i not in self.print_graph_temp.keys():
                    self.print_graph_temp[i] = (i,j,self.adjlist[i][j])
                else:
                    self.print_graph_temp[i] =  self.print_graph_temp[i]+(i,j,self.adjlist[i][j])
#        print 'graph'
#        print self.adjlist
        return self.print_graph_temp

### this method should take as input the name of a starting vertex
### and compute Dijkstra's algorithm,
### returning a dictionary that maps destination cities to
### a tuple containing the length of the path, and the vertices that form the path.
### Wikipedia has pseudo-Code for this - now translate it to Python,
### But do NOT copy any actual python code from anywhere else on the web
    def dijkstra(self, source):
        dist = {}
        prev = {}
        for i in self.vertices_list.keys():
            dist[i] = float("infinity")
            prev[i] = ''
        dist[source] = 0
        prev[source] = source
        for t in self.vertices_list.keys():
            self.adjlist[t][t] = 0.0
#debug
#        print self.adjlist
        list = self.vertices_list.keys()
        u = source
#debug
#        print list
        while list:
            min_dist = float("infinity")
            for j in list:
                if self.adjlist[u][j] < min_dist:
                    min_dist = dist[j]
                    u = j
#            print u
            list.remove(u)
            if min_dist == float("infinity"):
                break
            for v in self.adjlist[u].keys():
                alt = dist[u] + self.adjlist[u][v]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
        for i in self.vertices_list.keys():
            while 'Alcatraz' not in prev[i]:
                prev[i] = prev[prev[i]]+','+prev[i]

#        print dist
#        print prev
        d_graph = {}
        for t in self.vertices_list.keys():
            d_graph[t] = (dist[t],[prev[t]])
#        print d_graph
        return d_graph



### classes representing vertices and edges

class Vertex:
    def __init__(self, name, lat, longitude):
        self.name = name
        self.lat = lat
        self.longitude = longitude
    def __hash__(self):
        return hash(self.name)
    def __eq__(self, other):
        return self.name == other.name
    

class Edge:
    def __init__(self, src, dest, distance, time) :
        self.src = src
        self.dest = dest
        self.distance = distance
        self.time = time


### usage: buildGraph {--pfile=outfile} {-d=startNode} infile
### if --pfile=outfile is provided, write a pickled version of the graph 
### to outfile. Otherwise, print it to standard output.
### if --d=startNode is provided, compute dijkstra with the given starting node
###  as source

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''function that can read in graph data as provided
    in the sample input file and construct an adjacency list''')
    parser.add_argument('-d', type=str, help='''if --d=startNode is provided, compute dijkstra with the given starting node''')
    parser.add_argument('--pfile', type=argparse.FileType('w'), help='''the name of a file to use as output''')
    parser.add_argument('file', type=argparse.FileType('r'), help='''the name of a file to use as input''')
    args = parser.parse_args()
#    args = parser.parse_args(['sfdata.txt','-d','Alcatraz'])
    graph2 = Graph(args.file)

    if args.d:
        dijkstra_graph = graph2.dijkstra(args.d)
        print 'Dijkstra solution  start node of '+args.d
        print dijkstra_graph
    if args.pfile:
        pickle.dump(graph2, args.pfile)
    else:
        graph2.__repr__()
