from random import random
import json

def graph(numNodes, connectivity):
    adjMat = []
    for i in range(numNodes):
        temp = [0]*numNodes
        adjMat.append(temp)
    for i in range(numNodes):
        for j in range(numNodes-i):
            j = numNodes-j-1
            if random() < connectivity:
                adjMat[i][j] = 1
                adjMat[j][i] = 1

    return adjMat

def round(adjMat, choices, benefits, costs, dist):
    payoffs = [0] * len(adjMat)
    for player in range(len(choices)):
        playerChoice = choices[player]
        lowest = findLowest(adjMat, choices, dist, player)
        payoffs[player] = benefits[lowest-1] - costs[playerChoice-1]

    return payoffs

def findLowest(adjMat, choices, dist, startInd):
    lowest = 7
    search = [startInd]
    allInRange = [startInd]
    for i in range(dist):
        nextSearch = []
        for ind in search:
            for j in range(len(adjMat)):
                if adjMat[ind][j] == 1 and j not in nextSearch and j not in allInRange:
                    nextSearch.append(j)
                    allInRange.append(j)
        search = nextSearch
    for ind in allInRange:
        if choices[ind] < lowest:
            lowest = choices[ind]
    return lowest

def generateChoices(descMat):
    choices = [0]* len(descMat)
    for ind in range(len(descMat)):
        randF = random()
        total = 0
        for i in range(len(descMat[ind])):
            total = descMat[ind][i]
            if randF <= total:
                choices[ind] = i
                break
    return choices

def game(rounds, numNodes, connectivity, benefits, costs, dist, learnRate):
    adjMat = graph(numNodes, connectivity)
    descMat = []
    for i in range(numNodes):
        temp = [0.05,0.05,0.05,0.05,0.05,0.05,0.7]
        descMat.append(temp)
    totalPayoffs = [0]*numNodes
    totalChoices = [0]*numNodes
    for i in range(rounds):
        choices = generateChoices(descMat)
        payoffs = round(adjMat, choices, benefits, costs, dist)
        for j in range(len(payoffs)):
            totalPayoffs[j] += payoffs[j]
            totalChoices[j] += choices[j]
        avgPayoff = sum(payoffs)/len(payoffs)
        for j in range(numNodes):
            change = ((payoffs[j]/avgPayoff) - 1) * learnRate
            miniChange = (change/6)*-1
            playerChoice = choices[j]
            for k in range(len(descMat[j])):
                descMat[j][k] += miniChange
            descMat[j][playerChoice - 1] += (change - miniChange)
    avgFinalPayoff = (sum(totalPayoffs)/50)/numNodes
    avgFinalChoice = (sum(totalChoices)/50)/numNodes
    return avgFinalPayoff, avgFinalChoice
            
        

connectivities = [0.2,0.4,0.6,0.8]
localities = [1,2,4,8]
benefits = [100,200,300,400,500,600,700]
costs = [[0,10,20,30,40,50,60],[0,50,100,150,200,250,300],[0,100,200,300,400,500,600]]
learnRates = [0.001,0.01,0.1]
graphSizes = [20,50,100]
rounds = 50

data = []
for connectivity in connectivities:
    for locality in localities:
        for cost in costs:
            for learnRate in learnRates:
                for graphSize in graphSizes:
                    tempPay, tempChoice = game(rounds, graphSize, connectivity, benefits, cost, locality, learnRate)
                    print((graphSize, connectivity, cost, locality, learnRate, tempPay, tempChoice))
                    data.append((graphSize, connectivity, cost, locality, learnRate, tempPay, tempChoice))

print(data)
with open("data.json", "w") as outfile:
    json.dumps(data)

