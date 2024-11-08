from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from plotting_utilities import plot_country, plot_path

if TYPE_CHECKING:
    from pathlib import Path

    from matplotlib.figure import Figure

import csv

def travel_time(
    distance,
    different_regions,
    locations_in_dest_region,
    speed = 4.75,
):
    r_diff = 1 if different_regions else 0
    travel_time_using = (distance / speed) * (1 + (r_diff * locations_in_dest_region) / 10) / 3600
    return travel_time_using

class Location:
    def __init__(self, name, region, is_depot, x, y):
        self.name = name
        self.region = region
        self.is_depot = is_depot
        self.x = x
        self.y = y
    
    def __repr__(self):
        """
        Do not edit this function.
        You are NOT required to document or test this function.

        Not all methods of printing variable values delegate to the
        __str__ method. This implementation ensures that they do,
        so you don't have to worry about Locations not being formatted
        correctly due to these internal Python caveats.
        """
        return self.__str__()

    def __str__(self):
        return f"{self.name} ({'Depot' if self.is_depot else 'Settlement'}) in {self.region}"

    def distance_to(self, other):
        distance_squared = (self.x - other.x)**2 + (self.y - other.y)**2
        return distance_squared ** 0.5

    def __eq__(self, other):
        return (self.name == other.name) and (self.region == other.region)


class Country:

    @classmethod
    def from_csv(location_information, filepath):
        locations = []
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['location']
                region = row['region']
                is_depot = row['depot'] == 'TRUE'
                x = float(row['x'])
                y = float(row['y'])
                locations.append(Location(name, region, is_depot, x, y))
        return location_information(locations)

    def __init__(self, locations):
        self.locations = locations
        self.depots = [location for location in locations if location.is_depot]
        self.settlements = [location for location in locations if not location.is_depot]

    def travel_time(self, start_location, end_location):
        distance = start_location.distance_to(end_location)
        different_regions = start_location.region != end_location.region
        locations_in_dest_region = len([location for location in self.locations if location.region == end_location.region])
        return travel_time(distance, different_regions, locations_in_dest_region)

    def nearest_neighbour_path(self, start_depot, speed):
        path = [start_depot]
        unvisited = list(self.settlements)
        current_location = start_depot

        while unvisited:
            nearest = min(unvisited, key=lambda loc: self.travel_time(current_location, loc, speed))
            path.append(nearest)
            unvisited.remove(nearest)
            current_location = nearest

        path.append(start_depot)
        return path

    def fastest_trip_from(
        self,
        current_location,
        potential_locations,
    ):
        raise NotImplementedError

    def nn_tour(self, starting_depot):
        raise NotImplementedError

    def best_depot_location(self, speed):
        min_time = float('inf')
        best_depot = None

        for depot in self.depots:
            path = self.nearest_neighbour_path(depot, speed)
            total_time = sum(self.travel_time(path[i], path[i + 1], speed) 
                             for i in range(len(path) - 1))

            if total_time < min_time:
                min_time = total_time
                best_depot = depot

        return best_depot

    def plot_country(
        self,
        distinguish_regions: bool = True,
        distinguish_depots: bool = True,
        location_names: bool = True,
        polar_projection: bool = True,
        save_to: Optional[Path | str] = None,
    ) -> Figure:
        """

        Plots the locations that make up the Country instance on a
        scale diagram, either displaying or saving the figure that is
        generated.

        Use the optional arguments to change the way the plot displays
        the information.

        Attention
        ---------
        You are NOT required to write tests or documentation for this
        function; and you are free to remove it from your final
        submission if you wish.

        You should remove this function from your submission if you
        choose to delete the plotting_utilities.py file.

        Parameters
        ----------
        distinguish_regions : bool, default: True
            If True, locations in different regions will use different
            marker colours.
        distinguish_depots bool, default: True
            If True, depot locations will be marked with crosses
            rather than circles.  Their labels will also be in
            CAPITALS, and underneath their markers, if not toggled
            off.
        location_names : bool, default: True
            If True, all locations will be annotated with their names.
        polar_projection : bool, default: True
            If True, the plot will display as a polar
            projection. Disable this if you would prefer the plot to
            be displayed in Cartesian (x,y) space.
        save_to : Path, str
            Providing a file name or path will result in the diagram
            being saved to that location. NOTE: This will suppress the
            display of the figure via matplotlib.
        """
        return plot_country(
            self,
            distinguish_regions=distinguish_regions,
            distinguish_depots=distinguish_depots,
            location_names=location_names,
            polar_projection=polar_projection,
            save_to=save_to,
        )

    def plot_path(
        self,
        path: List[Location],
        distinguish_regions: bool = True,
        distinguish_depots: bool = True,
        location_names: bool = True,
        polar_projection: bool = True,
        save_to: Optional[Path | str] = None,
    ) -> Figure:
        """
        Plots the path provided on top of a diagram of the country,
        in order to visualise the path.

        Use the optional arguments to change the way the plot displays
        the information. Refer to the plot_country method for an
        explanation of the optional arguments.

        Attention
        ---------
        You are NOT required to write tests or documentation for this
        function; and you are free to remove it from your final
        submission if you wish.

        You should remove this function from your submission if you
        choose to delete the plotting_utilities.py file.

        Parameters
        ----------
        path : list
            A list of Locations in the country, where consecutive
            pairs are taken to mean journeys from the earlier location to
            the following one.
        distinguish_regions : bool, default: True,
        distinguish_depots : bool, default: True,
        location_names : bool, default: True,
        polar_projection : bool, default: True,
        save_to : Path, str

        See Also
        --------
        self.plot_path for a detailed description of the parameters
        """
        return plot_path(
            self,
            path,
            distinguish_regions=distinguish_regions,
            distinguish_depots=distinguish_depots,
            location_names=location_names,
            polar_projection=polar_projection,
            save_to=save_to,
        )
