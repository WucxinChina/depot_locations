import numpy as np
import matplotlib.pyplot as plt
from timeit import timeit
from utilities import regular_n_gon

location_counts = np.unique(np.logspace(0, 9, base=2, num=75, dtype=int))

execution_times = []

for count in location_counts:
    country = regular_n_gon(count)
    
    depot = country.depots[0]
    time = timeit(lambda: country.nn_tour(depot), number=1)
    
    execution_times.append(time)
    print(f"Processed {count} locations in {time:.4f} seconds.")

plt.figure(figsize=(10, 6))
plt.plot(location_counts, execution_times, marker='o', linestyle='-')
plt.xlabel("Number of Locations (n)")
plt.ylabel("Execution Time (seconds)")
plt.title("NNA Execution Time vs. Number of Locations")
plt.grid(True)
plt.savefig("report/nna_execution_times.png")
plt.show()