import math

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
        print("At Node " + str(self.swid))
        packet.hop_count += 1
        packet.ttl -= 1
        reset = False
        if(self.swid == packet.dst):
            network.done = True 
            print("Destination Reached")
            return True
        print("Packet swid " + str(packet.swid))
        if self.swid == packet.swid: 
            print("here")
            network.loop = True

        if packet.hop_count == (network.phase_size - 1): 
            packet.hop_count = 0
            network.phase_size *= network.b 
            packet.swid = math.inf  
            reset = True 
        
        if network.loop: 
            print("loop detected")
            #add reroute 
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

    def createSimpleTopology(self): 
        routingTables = {
            0 : {6 : 2}, 
            1 : {6 : 3},
            2 : {6 : 4},
            3 : {6 : 1},
            4 : {6 : 6},
            5 : {6 : 6},
        }
        for i in range (1, 7):
            self.nodes.append(Node(i, routingTables[i - 1]))
        self.links.append(Link(self.nodes[0], self.nodes[1]))
        self.links.append(Link(self.nodes[0], self.nodes[3])) 
        self.links.append(Link(self.nodes[3], self.nodes[2]))
        self.links.append(Link(self.nodes[2], self.nodes[1]))
        self.links.append(Link(self.nodes[2], self.nodes[4]))
        self.links.append(Link(self.nodes[4], self.nodes[5]))

class Network: 
     def __init__(self, b):  
         self.b = b 
         self.topology = Topology() 
         self.loop = False 
         self.done = False
         self.phase_size = 1

     def simulate(self, _src, _dst): 
         self.topology.createSimpleTopology()
         packet = Packet(src = _src , dst = _dst, ttl = 20)
         curr_node = next((x for x in self.topology.nodes if x.swid == packet.src), None)
         hops = 0 
         while(True): 
            hops += 1
            val = curr_node.unroller_alg(packet, self)
            if self.loop:
              break
            curr_node = next((x for x in self.topology.nodes if x.swid == curr_node.next_hop), None) 
            if self.done: 
                print("Routed successfully after " + hops + " hops")
                break 

        



network = Network(4)
network.simulate(1, 6)