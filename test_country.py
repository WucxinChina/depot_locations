import pytest
from country import Location, Country

def test_distance_to():
    loc1 = Location("Point 1", "Region A", False, 0, 0)
    loc2 = Location("Point 2", "Region A", False, 3, 4)
    assert loc1.distance_to(loc2) == 5, "Expected distance should be equal to 5."

def test_travel_time(speed):
    loc1 = Location("Location1", "Region1", False, 0, 0)
    loc2 = Location("Location2", "Region2", False, 3, 4)
    country = Country([loc1, loc2])
    time = country.travel_time(loc1, loc2, speed)
    assert time > 0, "Expected travel time should be greater than 0."

def test_nearest_neighbour_path(speed):
    depot = Location("Depot", "Region", True, 0, 0)
    settlement1 = Location("Settlement1", "Region", False, 1, 1)
    settlement2 = Location("Settlement2", "Region", False, 2, 2)
    country = Country([depot, settlement1, settlement2])
    path = country.nearest_neighbour_path(depot, speed)
    assert path[0] == depot and path[-1] == depot, "Path should start and end at the depot."
    assert len(path) == 4, "Path should include all locations and return to the start."

def test_best_depot_location(speed):
    depot1 = Location("Depot1", "Region1", True, 0, 0)
    depot2 = Location("Depot2", "Region2", True, 1, 1)
    settlement = Location("Settlement", "Region1", False, 2, 2)
    country = Country([depot1, depot2, settlement])
    best_depot = country.best_depot_location(speed)
    assert best_depot in [depot1, depot2], "Expected best depot should be one of the depots."

test_distance_to()
test_travel_time(40)
test_nearest_neighbour_path(40)
test_best_depot_location(40)