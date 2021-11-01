class Dataset:
    DistancesDataset = "datasets/states_merged.csv"
    CoordinatesDataset = "datasets/states_coords.csv"


class CoordinateDatasetKeys:
    City = 'estado'
    Latitude = 'lat'
    Longitude = 'lng'


class RouteKeys:
    City = 'city'
    Latitude = 'lat'
    Longitude = 'lng'


class Solver:
    SolverName = 'cbc'


class Output:
    MapOutputFile = 'Route.html'
