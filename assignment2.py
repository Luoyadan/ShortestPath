"""
CS141 Assignment2_Shortpath
Author : Yadan Luo
UC Riverside, Nov. 30 2016
"""
#!/usr/bin/python

import sys
import re
import time
import os

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(\\d+)")

vertices=[]
edges=[]
	#the format of out put is Trace, xnn means the lenths 
    #    0   1   2 
    # 0 x00 x01 x02
    # 1 x10 x11 x12
    # 2 x20 x21 x22
    # Where xij is the length of the shortest path between i anpathPairs j
	#same in both
	# File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>

def BellmanFord(G):
    # Fill in your Bellman-Ford algorithm here
    # The pathPairs list will contain the list of vertex pairs and their weights [((s,t),w),...]
    pathPairs=[]
    d = []   
    for source in range(len(G[0])):            #iterate through every node
        d = [float("inf")]*(len(G[0]))              #start a fresh list of infinite edge lengths
        d[source] = 0                               #the source node has 0 distance to itself    
        for k in range(1, len(G[0])-1):
            check = 0
            for i in range(len(G[0])):             #iterate through all vertices
                for j in range(len(G[0])):           #iterate through 
                    if(G[1][i][j] != float("inf")):     #Check that the edge exists
                        if(d[j] > d[i] + float(G[1][i][j])):     #Check if d[v] > d[u]+d(u,v)
                            d[j] = d[i] + float(G[1][i][j])
                            check = 1
            if check == 0 : 
                break
                    
        pathPairs.append(d)                                 #stick the list into pathPairs
        
    # check negative cycle
    flag = 0
    for i in range(len(G[0])):             #iterate through all vertices
                for j in range(len(G[0])):           #iterate through 
                    if(G[1][i][j] != float("inf")):     #Check that the edge exists
                        if(d[j] > d[i] + float(G[1][i][j])):     #Check if d[v] > d[u]+d(u,v)
                            flag = 1
                            break
    if flag == 1:
        return False
    d = []                                              #reset d list
    return pathPairs

def FloydWarshall(G):
    # Fill in your Floyd-Warshall algorithm here
    # The pathPairs list will contain the list of vertex pairs and their weights [((s,t),w),...]
    
    pathPairs=[]
    for i in range(len(G[0])):
        row = []
        for j in range(len(G[0])):
            row.append(float("inf"))
        pathPairs.append(row)

    for i in range(len(G[0])):                   #iterate by rows
        for j in range(len(G[0])):             #iterate by columns
            if i == j:
                pathPairs[i][j] = 0
            elif float(G[1][i][j]) != float("inf"):
                pathPairs[i][j] = float(G[1][i][j])
            else:
                pathPairs[i][j] = float("inf")
    for k in range(len(G[0])):                   #iterate by rows
        for i in range(len(G[0])):             #iterate by columns
            for j in range(len(G[0])):
                if pathPairs[i][j] > pathPairs[i][k] + pathPairs[k][j]:
                    pathPairs[i][j] = pathPairs[i][k] + pathPairs[k][j]
    return pathPairs

def writeFile(Trace,filename,algorithm):
    filename=os.path.splitext(os.path.split(filename)[1])[0]
    outFile=open(filename+"algorithm_"+algorithm+'_output.txt','w')
    for vertex in Trace:
        for length in vertex:
            outFile.write(str(length)+',')
        outFile.write('\n')
        


def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            edges[int(source)-1][int(sink)-1]=weight
    #Debugging
    #for i in G:
        #print(i)
    return (vertices,edges)

def main(filename,algorithm):
    algorithm=algorithm[1:]
    G=readFile(filename)
    Trace=[]
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    if algorithm == 'b' or algorithm == 'B':
        Trace=BellmanFord(G)
    if algorithm == 'f' or algorithm == 'F':
        Trace=FloydWarshall(G)
    if algorithm == "both":
        start=time.clock()
        BellmanFord(G)
        end=time.clock()
        BFTime=end-start
        start=time.clock()
        FloydWarshall(G)
        end=time.clock()
        FWTime=end-start
        print("Bellman-Ford timing: "+str(BFTime))
        print("Floyd-Warshall timing: "+str(FWTime))
    writeFile(Trace,filename,algorithm)
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python assignment2.py -<f|b> <input_file>")
        quit(1)
    if len(sys.argv[1]) < 2:
        print('python assignment2.py -<f|b> <input_file>')
        quit(1)
    main(sys.argv[2],sys.argv[1])
