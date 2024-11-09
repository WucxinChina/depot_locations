#import pytest
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

RW_to_HM_time = skyrim.travel_time(riverwood, heartwood_mill)
HM_to_RW_time = skyrim.travel_time(heartwood_mill, riverwood)
print(f"Travel time from Riverwood to Heartwood Mill: {RW_to_HM_time}")
print(f"Travel time from Heartwood Mill to Riverwood: {HM_to_RW_time}")

kvatch = Location("Kvatch", "Cyrodiil", 175000, -3 * math.pi / 4, False)
try:
    skyrim.travel_time(riverwood, kvatch)
    print("If you see this message in the output, no error was raised!")
except ValueError as e:
    print("Attempting to determine travel time to a location not in the country threw an error:")
    print(f"\t{e}")

print(f"Using default args: {skyrim.fastest_trip_from(riverwood)}")
print(f"Selecting settlements: {skyrim.fastest_trip_from(riverwood, [0, 1, 3, 4])}")
print(f"Providing explicit locations: {skyrim.fastest_trip_from(riverwood, [heartwood_mill, whiterun])}")
print(f"Mix and match selection: {skyrim.fastest_trip_from(riverwood, [0, whiterun, 2, 3, heartwood_mill])}")

tour_from_heartwood_mill, tour_time = skyrim.nn_tour(heartwood_mill)

print(f"Time to complete tour starting in Heartwood Mill: {tour_time:2.2f} h")
print("The tour path was:")
for loc in tour_from_heartwood_mill:
    print(f"\t{loc}")

best_depot = skyrim.best_depot_site(display=False)
print(f"\nThe best depot found was: {best_depot}")
print("\nWith display=True however, we get information automatically...\n")
best_depot_again = skyrim.best_depot_site()
assert best_depot_again == best_depot