from City import City
from helpers import (
    getDistanceBetweenTwoCities
)

numberOfCities = 1000


def main():
    graph = generateGraph(numberOfCities)
    distanceDictionary = calculateDistancesBetweenCities(graph)
    greedyVoyagePath = getVoyagePath(graph[0], graph, distanceDictionary)
    greedyVoyagePathDistance = 0
    for i in range(numberOfCities):
        if i != numberOfCities - 1:
            greedyVoyagePathDistance += distanceDictionary[greedyVoyagePath[i].name
                                                           ][greedyVoyagePath[i+1].name]
    print(greedyVoyagePathDistance)


def generateGraph(n):
    cities = []
    for _ in range(n):
        cities.append(City())
    return cities


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


def getVoyagePath(begginingCity, graph, distanceDictionary):
    voyagePath = [begginingCity]
    citiesArray = graph.copy()
    citiesArray.remove(begginingCity)
    while len(voyagePath) != len(graph):
        if len(citiesArray) == 0:
            break
        currentlyOptimalDistance = float('inf')
        currentlyOptimalCity = None
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
