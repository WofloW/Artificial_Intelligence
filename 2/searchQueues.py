import heapq
import search
import math

### this is a helper function that converts a string containing latitude or longitude
## represented as degrees.minutes.seconds (e.g. 37.47.44N) into a float.
def convertLatLong(str) :
    deg, minutes,seconds = str[:-1].split('.',2)
    minutes = float(minutes) + (float(seconds) / 60.0)
    deg = float(deg) + (minutes/ 60.0)
    return deg



class SearchQueue :
    def __init__(self,goal) :
        self.q = []
        self.goal = goal
    def insert(self, item) :
        pass
    def pop(self) :
        pass
    def isEmpty(self) :
        return self.q == []


    ### this is a helper function that converts latitude and longitude to the distance from node to goal
    def latlong_to_distance(self,node):
        latA = convertLatLong(self.goal.vertex.lat)*math.pi/180
        latB = convertLatLong(node.vertex.lat)*math.pi/180
        lonA = -convertLatLong(self.goal.vertex.longitude)*math.pi/180
        lonB = -convertLatLong(node.vertex.longitude)*math.pi/180
        A1= -lonA
        A2= -lonB
        A0=(A1-A2)/2
        B1= latA
        B2= latB
        B0= (B1-B2)/2
        f=math.sqrt(math.sin(B0)*math.sin(B0)+math.cos(B1)*math.cos(B2)*math.sin(A0)*math.sin(A0))
        h=2*f*6371.004
        return h
    def goalTest(self,node):
        return node.vertex == self.goal.vertex


### you complete this.
class BFSQueue(SearchQueue) :
    def insert(self, item) :
        self.q.append(item)
    def pop(self) :
        return self.q.pop(0)


### you complete this.
class DFSQueue(SearchQueue) :
    def insert(self, item) :
        self.q.append(item)
    def pop(self) :
        return self.q.pop()


### you complete this
class AStarQueue(SearchQueue) :
    def insert(self, item) :
        costf = self.latlong_to_distance(item) + item.cost
        heapq.heappush(self.q, (costf, item))
    def pop(self) :
        return heapq.heappop(self.q)


