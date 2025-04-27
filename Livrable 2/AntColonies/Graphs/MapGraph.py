from Graphs.AbstractGraph import AbstractGraph
import random
from geopy.geocoders import Nominatim
from utils.plot import Plot
from math import radians, sin, cos, sqrt, atan2

class MapGraph(AbstractGraph):
    def __init__(self, cities, start_city = None):
        super().__init__()
        random.shuffle(cities)
        if start_city:
            if start_city in cities: #else that use the first city of the cities list
                cities.remove(start_city)
            cities.insert(0, start_city)

        geolocator = Nominatim(user_agent="city_locator", timeout=10)

        self.city_coordinates = {}

        for city in cities:
            location = geolocator.geocode(city)
            if location:
                self.city_coordinates[city] = (location.latitude, location.longitude)
            else:
                print(f"Could not find coordinates for {city}")

        valid_cities = list(self.city_coordinates.keys())
        self.add_nodes_from(valid_cities)

        for city1 in valid_cities:
            for city2 in valid_cities:
                if city1 != city2:
                    distance = self.haversine(self.city_coordinates[city1], self.city_coordinates[city2])
                    self.add_edge(city1, city2, weight=distance)
    

    def haversine(self,coord1, coord2):
        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        radius = 6371
        return radius * c
    
    def plot_graph(self,best_path = None,show_graph = True):
        Plot.plot_map(self.city_coordinates,self, best_path, show_graph)
        