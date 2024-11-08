import pytest
from country import Location, Country, travel_time

# Test: 4.1 A Function for Travel Time
default_speed = 4.75
one_hour_distance = 3_600 * default_speed
print(f"Travelling at the default speed: {travel_time(one_hour_distance, 0.,
3.):2.1f} h")
print(f"Travelling at half default speed: {travel_time(one_hour_distance, 0.,
0., speed = default_speed / 2.):2.1f} h")
print(f"Travel at default speed but with a region penalty that equates to 3: {travel_time(one_hour_distance, 
1., 20.):2.1f} h")

riverwood = Location("Riverwood", "Whiterun Hold", 49_877.15654485528,
-1.1153081421843865, False)
heartwood_mill = Location("Heartwood Mill", "The Rift", 164_031.25924652288,
-0.6236682227787959, True)
# bad_name = Location("noT CAPitalised", "Region", 0., 0., False)

print(f"Before changing depot: {heartwood_mill.settlement}")
heartwood_mill.depot = False
print(f"After changing depot: {heartwood_mill.settlement}")
try:
    heartwood_mill.settlement = False
    print("If you are seeing this in the output, no error was raised!")
except Exception as e:
    print("Attempting to assign to the settlement property raised the following error:")
    print(f"\t{e}")