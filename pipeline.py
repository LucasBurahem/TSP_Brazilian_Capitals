import json

from catalog import Dataset
from model import mtz_model
from utils import read_distances_dataset, read_coordinates_dataset, return_route, mapping_route, plot_route


def pipeline():
    distance_matrix = read_distances_dataset(Dataset.DistancesDataset)
    coordinates = read_coordinates_dataset(Dataset.CoordinatesDataset)
    result, model = mtz_model(distance_matrix)
    route = return_route(model)
    map_route = mapping_route(route, coordinates)
    plot_route(map_route, route)
    data = {'objective_value': round(model.objective(), 2), 'Route': map_route}
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)