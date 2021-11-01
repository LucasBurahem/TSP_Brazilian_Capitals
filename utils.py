import numpy as np
import pandas as pd
import folium
from catalog import CoordinateDatasetKeys, RouteKeys, Output


def read_distances_dataset(distances):
    distance_matrix = np.loadtxt(open(distances, "rb"), delimiter=",", skiprows=1)

    return distance_matrix


def read_coordinates_dataset(coordinates):
    cities_coordinates = pd.read_csv(coordinates, delimiter=",")

    return cities_coordinates


def return_route(model):
    route_tuples = list()
    for i in list(model.x.keys()):
        if model.x[i]() == 1:
            route_tuples.append(i)

    route = [1]

    while len(route_tuples) > 0:
        former_destination = route[-1]
        for i, (origin, destination) in enumerate(route_tuples):
            if origin != former_destination:
                continue

            route_tuples.pop(i)
            route.append(destination)
            break

    return route


def mapping_route(route, coordinates):
    map_route = dict()
    for index in route:
        city = coordinates.iloc[index - 1]
        map_route[index] = {
            RouteKeys.City: city[CoordinateDatasetKeys.City],
            RouteKeys.Latitude: city[CoordinateDatasetKeys.Latitude],
            RouteKeys.Longitude: city[CoordinateDatasetKeys.Longitude]
        }

    return map_route


def plot_route(map_route, route):

    for index in range(len(route)-1):
        if index == 0:
            m = folium.Map([map_route[route[index]][RouteKeys.Latitude], map_route[route[index]][RouteKeys.Longitude]],
                           fill_color="red",
                           zoom_start=11)

        origin = [map_route[route[index]][RouteKeys.Latitude],
                  map_route[route[index]][RouteKeys.Longitude]]
        target = [map_route[route[index+1]][RouteKeys.Latitude],
                  map_route[route[index+1]][RouteKeys.Longitude]]

        folium.CircleMarker(origin,
                            radius=10,
                            fill_color="#3db7e4",  # divvy color
                            ).add_to(m)

        folium.CircleMarker(target,
                            radius=10,
                            fill_color="red",  # divvy color
                            ).add_to(m)

        folium.PolyLine([origin, target]).add_to(m)


    m.save(outfile=Output.MapOutputFile)

