import pytest
import math
from country import Location, Country, travel_time
from pathlib import Path
from utilities import read_country_data

# Test: 4.1 A Function for Travel Time
default_speed = 4.75
one_hour_distance = 3_600 * default_speed
print(f"Travelling at the default speed: {travel_time(one_hour_distance, 0.,
3.):2.1f} h")
print(f"Travelling at half default speed: {travel_time(one_hour_distance, 0.,
0., speed = default_speed / 2.):2.1f} h")
print(f"Travel at default speed but with a region penalty that equates to 3: {travel_time(one_hour_distance, 
1., 20.):2.1f} h")

# Test 4.2 The Location Class
riverwood = Location("Riverwood", "Whiterun Hold", 49_877.15654485528,
-1.1153081421843865, False)
heartwood_mill = Location("Heartwood Mill", "The Rift", 164_031.25924652288,
-0.6236682227787959, True)
bad_name = Location("noT CAPitalised", "Region", 0., 0., False)

print(f"Before changing depot: {heartwood_mill.settlement}")
heartwood_mill.depot = False
print(f"After changing depot: {heartwood_mill.settlement}")
try:
    heartwood_mill.settlement = False
    print("If you are seeing this in the output, no error was raised!")
except Exception as e:
    print("Attempting to assign to the settlement property raised the following error:")
    print(f"\t{e}")
print(f"Riverwood's information: {riverwood}")
print(f"Heartwood Mill's information: {heartwood_mill}")
RW_to_HM = riverwood.distance_to(heartwood_mill)
print(f"Distance from Riverwood to Heartwood Mill: {RW_to_HM} m")

def test_distance_same_location():
    loc1 = Location("A", "Region1", 10.0, 0.0, False)
    assert loc1.distance_to(loc1) == 0, "Distance between the same location should be 0."

def test_distance_right_triangle():
    loc1 = Location("A", "Region1", 10.0, 0.0, False)
    loc2 = Location("B", "Region1", 10.0, math.pi / 2, False)
    expected_distance = 10 * math.sqrt(2)
    assert math.isclose(loc1.distance_to(loc2), expected_distance, rel_tol=1e-9), "Distance between points forming a right triangle should be 10 * sqrt(2)."

def test_distance_same_angle():
    loc1 = Location("A", "Region1", 10.0, 0.0, False)
    loc2 = Location("B", "Region1", 15.0, 0.0, False)
    assert loc1.distance_to(loc2) == abs(10.0 - 15.0), "Distance between points with same angle should be the absolute difference in radius."

def test_distance_opposite_angles():
    loc1 = Location("A", "Region1", 10.0, 0.0, False)
    loc2 = Location("B", "Region1", 10.0, math.pi, False)
    assert loc1.distance_to(loc2) == math.sqrt(10.0**2 + 10.0**2 + 2 * 10.0 * 10.0), "Distance with angle difference of π should match the calculated formula."

# Test 4.3 The Country Class
riverwood = Location("Riverwood", "Whiterun Hold", 
49_877.15654485528, -1.1153081421843865, False)
heartwood_mill = Location("Heartwood Mill", "The Rift", 
164_031.25924652288, -0.6236682227787959, True)
karthwasten = Location("Karthwasten", "The Reach",
138_231.89539682947,2.858973382047493, True)
whiterun = Location("Whiterun", "Whiterun Hold", 
21_197.215713390284, -0.3577712724508101, False)
list_of_locations = [riverwood, heartwood_mill, karthwasten, whiterun]
country = Country(list_of_locations)

print("List of locations passed in:")
for loc in list_of_locations: 
    print(f"\t{loc}")
assert isinstance(country._all_locations, tuple), "Locations are not stored asa tuple in the Country class"
assert set(country._all_locations) == set(list_of_locations), "Provide dentries and those stored aren't the same"


locations_csv_file = Path("data/locations.csv")
skyrim = read_country_data(locations_csv_file)

print("List of locations in the country:")
for loc in skyrim._all_locations:
    print(f"\t{loc}")

print(f"Number of settlements in Skyrim: {skyrim.n_settlements}")
print("List of those settlements:")
for settlement in skyrim.settlements:
    print(f"\t{settlement}")

print(f"Number of depots in Skyrim: {skyrim.n_depots}")
print("List of those depots:")
for depot in skyrim.depots:
    print(f"\t{depot}")

skyrim_map = skyrim.plot_country()
skyrim_map.show()