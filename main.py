import random

from City import City
from helpers import (getDistanceBetweenTwoCities)
import math
from random import randint, uniform, shuffle
from pprint import pprint
population = []
distanceDictionary = {}
graph = []


def main():
    global distanceDictionary
    global graph
    (numberOfCities, g) = generateGraphFromFile("bayg29.txt")
    graph = g
    distanceDictionary = calculateDistancesBetweenCities(graph)
    greedyVoyagePath = getGreedyVoyagePath(graph[0], graph, distanceDictionary)
    greedyVoyagePath.append(graph[0])
    greedyVoyagePathDistance = countVoyageLength(greedyVoyagePath)
    cuckooSearch(graph, distanceDictionary)
    print("Total greedy length:", greedyVoyagePathDistance)


def cuckooSearch(graph, distanceDictionary):
    global population
    numberOfNests = len(graph)

    abandonedNestsParameter = math.floor(numberOfNests - 1)

    generations = 100

    population = generatePopulation(graph, len(graph))

    # tuple -> tuple with voyage at index 0 and distance at 1
    population.sort(key=lambda tuple: tuple[1])
    min = float('inf')
    for i in range(generations):
        res = cuckoo(abandonedNestsParameter)
        if res < min:
            min = res
        print(i, min)
    print("Total cuckoo lenght:", population[0][1])
    # for i in population[0][0]:
    #     print(i.name)


def cuckoo(abandonedNestsParameter):
    global population
    pop = population.copy()
    nest = pop[randint(0, len(pop)-1)]

    if leviFlight() > 2:
        nest = doubleBridgeMove(nest)
    else:
        nest = twoOptMove(nest)

    randomNestIndex = randint(0, len(pop)-1)

    if(population[randomNestIndex][1] > nest[1]):
        population[randomNestIndex] = nest

    abandonNests(abandonedNestsParameter)
    population.sort(key=lambda tuple: tuple[1])
    return population[0][1]


def abandonNests(numberOfNests):
    global population
    global graph

    goodNests = population[0:len(population)-numberOfNests]

    newNests = generatePopulation2(population[0][0], numberOfNests)
    population = goodNests + newNests


def doubleBridgeMove(nest):
    nest = nest[0]

    l = len(nest)

    a = randint(1, l-2)
    b = randint(1, l-2)
    c = randint(1, l-2)
    d = randint(1, l-2)

    nest[a], nest[c] = nest[c], nest[a]
    nest[b], nest[d] = nest[d], nest[b]

    return (nest, countVoyageLength(nest))


def twoOptMove(nest):
    nest = nest[0]

    l = len(nest)

    a = randint(1, l-2)
    b = randint(1, l-2)
    nest[a], nest[b] = nest[b], nest[a]

    return (nest, countVoyageLength(nest))


def leviFlight():
    flight = math.pow(uniform(0, 1), -1/3)
    return flight


def generatePopulation(graph, numberOfCities):
    population = []
    cities = graph.copy()
    originCity = cities[0]
    cities.remove(cities[0])

    for _ in range(numberOfCities):
        nest = shuffleCities(cities)
        nest.insert(0, originCity)
        nest.append(originCity)
        population.append((nest, countVoyageLength(nest)))
    return population


def generatePopulation2(bestPath, numberOfCities):
    population = []
    cities = bestPath.copy()
    originCity = cities[0]
    cities.remove(cities[0])
    cities.pop()


    for _ in range(numberOfCities):
        nest = cities.copy()
        random.shuffle(nest)
        nest.insert(0, originCity)
        nest.append(originCity)
        population.append((nest, countVoyageLength(nest)))
    return population

def countVoyageLength(voyage):
    global distanceDictionary
    length = 0
    for i in range(len(voyage)):
        if i != len(voyage) - 1:
            length += distanceDictionary[voyage[i].name][voyage[i + 1].name]
    return length


def shuffleCities(cities):
    shuffled = cities.copy()
    citiesLength = len(shuffled)
    for i in range(citiesLength-1):
        j = randint(i, citiesLength-1)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    return shuffled

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
    distanceDictionary = {}
    for city in graph:
        localDictionary = {}
        for nearbyCity in graph:
            if city.name != nearbyCity.name:
                localDictionary[nearbyCity.name] = getDistanceBetweenTwoCities(
                    city, nearbyCity)
        distanceDictionary[city.name] = localDictionary

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
