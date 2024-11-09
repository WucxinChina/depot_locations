from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from plotting_utilities import plot_country, plot_path

if TYPE_CHECKING:
    from pathlib import Path

    from matplotlib.figure import Figure

import numpy as np
import warnings
import math

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
    def __init__(self, name, region, r, theta, depot):
        if not isinstance(name, str):
            raise TypeError("The 'name' must be a string.")
        if not isinstance(region, str):
            raise TypeError("The 'region' must be a string.")
        
        formatted_name = " ".join([word.capitalize() for word in name.split()])
        formatted_region = " ".join([word.capitalize() for word in region.split()])
        
        if name != formatted_name:
            warnings.warn(f"The 'name' value '{name}' was reformatted to '{formatted_name}'.")
        if region != formatted_region:
            warnings.warn(f"The 'region' value '{region}' was reformatted to '{formatted_region}'.")

        self.name = formatted_name
        self.region = formatted_region

        try:
            self.r = float(r)
            self.theta = float(theta)
        except ValueError:
            raise TypeError("The 'r' and 'theta' values must be convertible to float.")

        if self.r < 0:
            raise ValueError("The 'r' value (polar radius) must be non-negative.")

        if not (-np.pi <= self.theta <= math.pi):
            raise ValueError("The 'theta' value must be within the range -π ≤ θ ≤ π.")

        if not isinstance(depot, bool):
            raise TypeError("The 'depot' value must be a boolean.")
        
        self._depot = depot
    
    @property
    def depot(self):
        return self._depot

    @depot.setter
    def depot(self, value):
        if not isinstance(value, bool):
            raise TypeError("The 'depot' value must be a boolean.")
        self._depot = value

    @property
    def settlement(self):
        return not self._depot

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
        type_str = "depot" if self._depot else "settlement"
        r_str = f"{self.r:.2f}".rstrip("0").rstrip(".")
        theta_over_pi = self.theta / math.pi
        theta_str = f"{theta_over_pi:.2f}".rstrip("0").rstrip(".")

        return f"{self.name} [{type_str}] in {self.region} @ ({r_str} m, {theta_str} pi)"

    def distance_to(self, other):
        return math.sqrt(
            self.r**2 + other.r**2 - 2 * self.r * other.r * math.cos(self.theta - other.theta)
        )

    def __eq__(self, other):
        return (self.name == other.name) and (self.region == other.region)
    
    def __hash__(self) -> int:
        return hash(self.name + self.region)
    
    def __lt__(self, other):
        return (self.region, self.name) < (other.region, other.name)

    def __le__(self, other):
        return (self.region, self.name) <= (other.region, other.name)

    def __gt__(self, other):
        return (self.region, self.name) > (other.region, other.name)

    def __ge__(self, other):
        return (self.region, self.name) >= (other.region, other.name)


class Country:
    def __init__(self, list_of_locations: List[Location]):
        self._all_locations = tuple(list_of_locations)
    
    @property
    def settlements(self):
        return tuple(location for location in self._all_locations if location.settlement)

    @property
    def n_settlements(self):
        return len(self.settlements)

    @property
    def depots(self):
        return tuple(location for location in self._all_locations if location.depot)

    @property
    def n_depots(self):
        return len(self.depots)


    def travel_time(self, start_location, end_location):

        if start_location not in self._all_locations:
            raise ValueError(f"Location {start_location} is not in the Country")
        if end_location not in self._all_locations:
            raise ValueError(f"Location {end_location} is not in the Country")
        
        distance = start_location.distance_to(end_location)
        different_regions = start_location.region != end_location.region
        locations_in_dest_region = len([location for location in self._all_locations
         if location.region == end_location.region])
        
        return travel_time(distance, different_regions, locations_in_dest_region)

    def fastest_trip_from(self, current_location, potential_locations=None):
        if potential_locations is None:
            potential_locations = list(self.settlements)

        resolved_locations = []
        for loc in potential_locations:
            if isinstance(loc, int):
                if 0 <= loc < len(self.settlements):
                    resolved_locations.append(self.settlements[loc])
                else:
                    raise IndexError(f"Index {loc} is out of range for settlements.")
            elif isinstance(loc, Location):
                resolved_locations.append(loc)

        if not resolved_locations:
            return None, None

        travel_times = []
        for loc in resolved_locations:
            time = self.travel_time(current_location, loc)
            travel_times.append((loc, time))

        travel_times.sort(key=lambda x: (x[1], x[0].name, x[0].region))

        return travel_times[0]
    
    def nn_tour(self, starting_depot):
        if starting_depot not in self.depots:
            raise ValueError(f"Starting location {starting_depot} is not a depot in the Country")

        tour = [starting_depot]
        unvisited = list(self.settlements)
        current_location = starting_depot
        total_time = 0

        while unvisited:
            next_location, travel_time = self.fastest_trip_from(current_location, unvisited)
            tour.append(next_location)
            total_time += travel_time
            unvisited.remove(next_location)
            current_location = next_location

        return_time = self.travel_time(current_location, starting_depot)
        tour.append(starting_depot)
        total_time += return_time

        return tour, total_time
    
    def nearest_neighbour_path(self, start_depot):
        path = [start_depot]
        unvisited = list(self.settlements)
        current_location = start_depot

        while unvisited:
            nearest = min(unvisited, key=lambda loc: self.travel_time(current_location, loc))
            path.append(nearest)
            unvisited.remove(nearest)
            current_location = nearest

        path.append(start_depot)
        return path

    def best_depot_location(self):
        min_time = float('inf')
        best_depot = None

        for depot in self.depots:
            path = self.nearest_neighbour_path(depot)
            total_time = sum(self.travel_time(path[i], path[i + 1]) 
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
