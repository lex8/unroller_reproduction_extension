import math
import csv
import sys

class Packet: 
     def __init__(self, src, dst, ttl):  
        self.ttl = ttl
        self.src = src
        self.dst = dst
        self.hop_count = 0
        self.swid = math.inf

class Node: 
    def __init__(self, swid, routing):
      self.swid = swid 
      self.routing = routing
      self.next_hop = -1

    #unroller method based on https://github.com/kucejan/unroller/blob/master/unroller.p4app/unroller.p4 and conversations with Jan Kucera
    def unroller_alg(self, packet, network): 
        packet.hop_count += 1
        packet.ttl -= 1
        reset = False
        if(self.swid == packet.dst):
            network.done = True 
            return True
       
        if self.swid == packet.swid: 
            network.loop = True

        if packet.hop_count >= (network.phase_size - 1): 
            packet.hop_count = 0
            network.phase_size *= network.b 
            packet.swid = math.inf  
            reset = True 
        
        if network.loop: 
            return False
        
        if reset or packet.swid > self.swid: 
            packet.swid = self.swid 
        self.next_hop = self.routing[packet.dst]
        return True
    
class Link: 
    def __init__(self, nodeA, nodeB): 
        self.nodeA = nodeA 
        self.nodeB = nodeB 

class Topology: 
    def __init__(self): 
        self.links = []
        self.nodes = []
        self.nodeSwids = []
        self.routingTable = {}

    def createSimpleTopology(self): 
        self.routingTable = {
            0 : {6 : 2, 5: 2}, 
            1 : {6 : 3, 5: 3},
            2 : {6 : 4, 5: 4},
            3 : {6 : 1, 5: 1},
            4 : {6 : 6, 5: 5},
            5 : {6 : 6, 5: 5},
        }

        for i in range (1, 7):
            self.nodes.append(Node(i, self.routingTable[i - 1]))

        self.links.append(Link(self.nodes[0], self.nodes[1]))
        self.links.append(Link(self.nodes[0], self.nodes[3])) 
        self.links.append(Link(self.nodes[3], self.nodes[2]))
        self.links.append(Link(self.nodes[2], self.nodes[1]))
        self.links.append(Link(self.nodes[2], self.nodes[4]))
        self.links.append(Link(self.nodes[4], self.nodes[5]))

    def createRoutingTableFromPath(self, path):
      with open(path) as csvfile:
        tableItems = csv.reader(csvfile)
        for i, ti in enumerate(tableItems):
          lineDict = {int(i.split(":")[0].strip()) : int(i.split(":")[1].strip()) for i in ti}
          self.routingTable[i] = lineDict
          self.nodes.append(Node(i + 1, lineDict))
          self.nodeSwids.append(i + 1)

    def createTopologyFromPath(self, path):
      self.links.clear() 
      with open(path) as csvfile:
        topologyItems = csv.reader(csvfile, delimiter=',')
        for ti in topologyItems:
          self.links.append(Link(self.nodes[int(ti[0]) - 1 ], self.nodes[int(ti[1]) - 1]))

class Network: 
     def __init__(self, b):  
         self.b = b 
         self.loop = False 
         self.done = False
         self.phase_size = 1
         self.hops = 0 
     

     def simulate(self, _src, _dst, fromSource): 
         self.loop = False
         self.done = False
         self.hops = 0 
         packet = Packet(src = _src , dst = _dst, ttl = 20)
         curr_node = next((x for x in self.topology.nodes if x.swid == packet.src), None)
         while(True): 
            self.hops += 1
            val = curr_node.unroller_alg(packet, self)
            if self.loop:
              # re route from source
              if fromSource: 
                self.rerouteFromPath(self.netBfs(packet.src, packet.dst))
              # re route from curr 
              else: 
                self.rerouteFromPath(self.netBfs(curr_node.swid, packet.dst))
             
              return self.hops
            curr_node = next((x for x in self.topology.nodes if x.swid == curr_node.next_hop), None) 
            if self.done: 
                return self.hops

     def netBfs(self, src, dst): 
         q = []
         seen = [] 
         q.append((src, [src]))
         seen.append(src)
         while len(q) > 0: 
             curr, path = q[0]
             q.pop(0)
             if curr ==dst:
                 return path
             for link in [x for x in self.topology.links if x.nodeA.swid == curr or x.nodeB.swid == curr]:
                 if link.nodeA.swid != curr and link.nodeA.swid not in seen:
                    newPath = path.copy()
                    newPath.append(link.nodeA.swid)
                    seen.append(link.nodeA.swid)
                    q.append((link.nodeA.swid, newPath))
                    self.hops += 1
                 elif link.nodeB.swid not in seen: 
                    newPath = path.copy()
                    newPath.append(link.nodeB.swid)
                    seen.append(link.nodeB.swid)
                    q.append((link.nodeB.swid, newPath))
                    self.hops += 1


     def rerouteFromPath(self, path):
            dest = path[-1]
            for i in range(0, len(path) - 1):
               entry = path[i] - 1
               self.topology.routingTable[entry][dest] = path[i + 1]
            temp = []
            for i in range (1, len(self.topology.nodes) + 1):
                temp.append(Node(i, self.topology.routingTable[i - 1]))
            self.topology.nodes = temp
            return self.topology.routingTable

def fullRun(metadata): 
  original_stdout = sys.stdout 
  fromSource = False
  metaFile = open(metadata)
  file_name = metaFile.readline().strip()
  for i in range(0, 2):
    temp = "reroute_curr" 
    if(fromSource):
      temp = "reroute_src"
    f = open(temp + "_" + file_name + ".csv" , 'w' )
    sys.stdout = f 
    print("LoopVal, B, b, Hops")
    for b in range(2, 10): 
      metaFile = open(metadata)
      metaFile.readline().strip()
      topoPath = metaFile.readline().strip()
      folderPath = metaFile.readline().strip()
      dest = int(metaFile.readline().strip())
      while (True): 
        loopSize = metaFile.readline().strip() 
        if loopSize == "EOF": 
          break
        loopNum = int(loopSize.split("L")[1])
        loopDesc = metaFile.readline().strip() 
        for i in range (0, 4): 
          infoBStart = metaFile.readline().strip() 
          valB = infoBStart.split(":")[0].strip()
          start = int(infoBStart.split(":")[1].strip())
          fullPath = folderPath + loopSize + "_" + valB + ".csv"
          network = Network(b)
          network.topology = Topology()
          network.topology.createRoutingTableFromPath(fullPath)
          network.topology.createTopologyFromPath(topoPath)
          hops = network.simulate(start, dest, fromSource)
          #hops2 = 0
          hops2 = network.simulate(start, dest, fromSource)
          print(str(loopNum) + "," + valB[1] + "," + str(b) + "," +  str(hops + hops2))
          fromSource = True
  sys.stdout = original_stdout

network = Network(4)
network.topology = Topology()

if len(sys.argv) > 1:
  for i in range(1, len(sys.argv)):
    #The next argument is the path to a cv containing routing table data
    if sys.argv[i] == "-rt":
      network.topology.createRoutingTableFromPath(sys.argv[i + 1])

    #The next argument is the path to a cv containing topology data
    elif sys.argv[i] == "-t":
      network.topology.createTopologyFromPath(sys.argv[i + 1])
    elif sys.argv[i] == "-f": 
      fullRun(sys.argv[i + 1])
else:
  network.topology.createSimpleTopology()
