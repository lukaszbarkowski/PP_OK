import random
import os
from City import City
from collections import defaultdict
from helpers import (getDistanceBetweenTwoCities)
import math
from random import randint, uniform, shuffle
from pprint import pprint
import multiprocessing as mp

population = []
distanceDictionary = defaultdict()
graph = []
pheromones = defaultdict()
standardGraph = []

def main():
    global distanceDictionary
    global graph
    global standardGraph
    global pheromones
    (numberOfCities, g) = generateGraphFromFile("bayg29.txt")
    manager = mp.Manager()
    standardGraph = g
    graph = manager.list(g)
    distanceDictionary = manager.dict(calculateDistancesBetweenCities(graph))
    antColony(32, 250)
    greedyVoyagePath = getGreedyVoyagePath(g[0], g, distanceDictionary)
    greedyVoyagePath.append(g[0])
    greedyVoyagePathDistance = countVoyageLength(greedyVoyagePath)
    print("Total greedy length:", greedyVoyagePathDistance)


def antColony(ants, iterations):
    minimalPathLength = float('inf')
    pool = mp.Pool(processes=ants)
    for g in range(iterations):
        print("Generation:", g)
        manager = mp.Manager()
        antPaths = manager.list()
        lock = manager.Lock()
        antsAlive = manager.Value("antsAlive", ants, lock=lock)

        for i in range(ants):
            pool.apply_async(ant, (graph, antPaths, antsAlive,
                                   distanceDictionary, pheromones, lock, standardGraph.copy()))

        while antsAlive.value > 0:
            pass
        addPheromones(antPaths)
        for i in range(len(antPaths)):
            antPaths[i].append(graph[0])
            length = countVoyageLength(antPaths[i])
            if(length < minimalPathLength):
                minimalPathLength = length

        evaporatePheromones()
    print(minimalPathLength)


def ant(graph, antPaths, antsAlive, distanceDictionary, pheromones, lock, standardGraph):
    antPath = [graph[0]]
    listOfCities = standardGraph.copy()
    listOfCities.pop(0)
    for i in range(len(graph)-1):
        actualCity = antPath[-1].name
        distance = distanceDictionary[actualCity]
        phero = pheromones[actualCity]
        probabilities = getProbabilities2(antPath, distance, phero, listOfCities, actualCity)
        city = getCityBasedOnProbability(probabilities, graph)
        antPath.append(city)
        index = [x.name for x in listOfCities].index(city.name)
        listOfCities.pop(index)
    antPaths.append(antPath)
    lock.acquire()
    antsAlive.value -= 1
    lock.release()


def addPheromones(paths):
    for path in paths:
        pathLength = countVoyageLength(path)
        for i in range(len(path)-1):
            pheromones[path[i].name][path[i + 1].name] = pheromones[path[i].name][path[i+1].name] + 1 / pathLength
        pheromones[path[-1].name][path[0].name] = pheromones[path[-1].name][path[0].name] + 1 / pathLength


def getProbabilities(currentPath, distance, phero):
    denominator = 0
    for (key2, value2) in distance.items():
        denominator = denominator + phero[key2] * (1 / value2)
    probabilities = defaultdict()
    for (key, value) in distance.items():
        if not any(x.name == key for x in currentPath):
            counter = phero[key] * (1 / value)
            probabilities[key] = counter / denominator

    return probabilities


def getProbabilities2(currentPath, distance, phero, cities, actualCity):
    denominator = 0
    for city in cities:
        denominator = denominator + \
            phero[city.name] * (1 / distance[city.name])
    probabilities = defaultdict()
    for city in cities:
        counter = phero[city.name] * (1 / distance[city.name])
        probabilities[city.name] = counter / denominator

    return probabilities

def getCityBasedOnProbability(probabilities, graph):
    ranges = defaultdict()
    probabilitySum = 0
    for (key, value) in probabilities.items():
        ranges[key] = (probabilitySum, probabilitySum+value)
        probabilitySum = probabilitySum + value

    randomValue = uniform(0, probabilitySum)

    for (key, value) in ranges.items():
        (minimal, maximal) = value
        if minimal == 0:
            chosenCity = key
        elif maximal == probabilitySum:
            chosenCity = key
        else:
            if minimal <= randomValue <= maximal:
                chosenCity = key
                break
    return graph[int(chosenCity)-1]


def evaporatePheromones():
    global pheromones
    for origin in pheromones:
        for destination in pheromones:
            if origin is not destination:
                pheromones[origin][destination] = pheromones[origin][destination] / 2


def countVoyageLength(voyage):
    global distanceDictionary
    length = 0
    for i in range(len(voyage)):
        if i != len(voyage) - 1:
            length += distanceDictionary[voyage[i].name][voyage[i + 1].name]
    return length


# wygenerowanie grafu zawierającego miasta o współrzędnych podanych w pliku
def generateGraphFromFile(filepath):
    cities = []
    f = open(filepath, "r", encoding="utf-8")
    # pobranie z 1. linii pliku liczby miast
    numberOfCities = int(f.readline())
    for line in f:
        dataOfCity = line.split()
        # pierwszy element to numer miasta, następnie współrzędne x i y
        cities.append(City(dataOfCity[0], float(
            dataOfCity[1]), float(dataOfCity[2])))
    return (numberOfCities, cities)


# funkcja zwracająca słownik, który na każdej pozycji odpowiadającej miastu przetrzymuje słownik
# zawierający odległości od danego miasta do innych miast
def calculateDistancesBetweenCities(graph):
    global pheromones
    distanceDictionary = {}
    for city in graph:
        localDictionary = {}
        localPheromones = {}
        for nearbyCity in graph:
            if city.name != nearbyCity.name:
                localDictionary[nearbyCity.name] = getDistanceBetweenTwoCities(
                    city, nearbyCity)
                localPheromones[nearbyCity.name] = 1
        distanceDictionary[city.name] = localDictionary
        pheromones[city.name] = localPheromones

    return distanceDictionary


# algorytm zachłanny obliczający trasę
def getGreedyVoyagePath(begginingCity, graph, distanceDictionary):
    voyagePath = [begginingCity]
    citiesArray = graph.copy()
    citiesArray.remove(begginingCity)
    while len(voyagePath) != len(graph):
        if len(citiesArray) == 0:
            break
        currentlyOptimalDistance = float('inf')  # infinity
        currentlyOptimalCity = None
        # wyszukujemy najbliższe miasto, którego nie odwiedziliśmy
        for city in citiesArray:
            distance = distanceDictionary[voyagePath[-1].name][city.name]
            if distance < currentlyOptimalDistance:
                currentlyOptimalDistance = distance
                currentlyOptimalCity = city

        voyagePath.append(currentlyOptimalCity)
        citiesArray.remove(currentlyOptimalCity)
    return voyagePath


if __name__ == "__main__":
    main()
