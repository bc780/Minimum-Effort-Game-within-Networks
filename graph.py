import random

#generate random graph

numNodes = 20
chanceOfConnection = 0.4

graph = {}

for i in range(1, numNodes+1):
    tempList = []
    for j in range(i, numNodes+1):
        if i != j:
            if random.random() > chanceOfConnection:
                tempList.append(j)
    graph[i] = tempList



print(graph)