from City import City
from helpers import (getDistanceBetweenTwoCities)


def main():
    (numberOfCities, graph) = generateGraphFromFile("bayg29.txt")
    distanceDictionary = calculateDistancesBetweenCities(graph)
    greedyVoyagePath = getVoyagePath(graph[0], graph, distanceDictionary)
    # dystans, jaki trzeba pokonać na podstawie trasy wyliczonej za pomocą algorytmu zachłannego
    greedyVoyagePathDistance = 0
    print("Path: ")
    for i in range(numberOfCities):
        print(greedyVoyagePath[i].name)
        if i != numberOfCities - 1:
            greedyVoyagePathDistance += distanceDictionary[greedyVoyagePath[i].name
                                                           ][greedyVoyagePath[i + 1].name]
    print("Total length:", greedyVoyagePathDistance)


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
def getVoyagePath(begginingCity, graph, distanceDictionary):
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
