import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image
from math import radians, sin, cos, sqrt, atan2
from tabulate import tabulate
from geopy.distance import geodesic

# Load the data from the file into a dataframe
df = pd.read_csv('alt_fuel_stations (Jul 29 2021).csv', low_memory=False)
df = df.rename(columns={'EV Level1 EVSE Num': 'Level 1', 'EV Level2 EVSE Num': 'Level 2', 'EV DC Fast Count': 'DC Fast'})

# Clean the charger count columns and convert the values to integers
df['Level 1'] = pd.to_numeric(df['Level 1'], errors='coerce').fillna(0).astype(int)
df['Level 2'] = pd.to_numeric(df['Level 2'], errors='coerce').fillna(0).astype(int)
df['DC Fast'] = pd.to_numeric(df['DC Fast'], errors='coerce').fillna(0).astype(int)

# Part 1: State-Level Analysis
state_charger_total = df.groupby('State')[['Level 1', 'Level 2', 'DC Fast']].sum()
state_charger_total['Every Type'] = state_charger_total.sum(axis=1)

# Print total chargers by state
print('\nTotal Chargers for Each State:\n', state_charger_total)

# Plot total chargers by type
state_charger_total['Every Type'].plot(kind='bar', color='red', xlabel='States', ylabel='Number of Chargers', title='Total Chargers for Every State')
plt.show()
state_charger_total['Level 1'].plot(kind='bar', color='blue', xlabel='States', ylabel='Number of Chargers', title='Level 1 Chargers by State')
plt.show()
state_charger_total['Level 2'].plot(kind='bar', color='orange', xlabel='States', ylabel='Number of Chargers', title='Level 2 Chargers by State')
plt.show()
state_charger_total['DC Fast'].plot(kind='bar', color='green', xlabel='States', ylabel='Number of Chargers', title='DC Fast Chargers by State')
plt.show()

# Part 2: Virginia City-Level Analysis
va_df = df[df['State'] == 'VA']
va_charger_locations = va_df[(va_df['Level 1'] > 0) | (va_df['Level 2'] > 0) | (va_df['DC Fast'] > 0)]
va_charger_locations = va_charger_locations[['City', 'Latitude', 'Longitude', 'Level 1', 'Level 2', 'DC Fast']]

# Load and prepare the Virginia map
va_map = Image.open('virginia_map.jpg')
img_width, img_height = va_map.size
va_box = [-83.6753, 36.5408, -75.2423, 39.4660]

# Convert latitude and longitude to pixel coordinates (correcting inversion)
va_charger_locations['Pixel_X'] = (va_charger_locations['Longitude'] - va_box[0]) / (va_box[2] - va_box[0]) * img_width
va_charger_locations['Pixel_Y'] = (va_charger_locations['Latitude'] - va_box[1]) / (va_box[3] - va_box[1]) * img_height

# Flip the y-axis while plotting
plt.imshow(va_map.convert('L'), extent=(0, img_width, 0, img_height), cmap='gray', origin='upper')
plt.scatter(va_charger_locations['Pixel_X'], va_charger_locations['Pixel_Y'], color='blue', label='EV Chargers')
plt.title('Distribution of EV Chargers in Virginia')
plt.legend()
plt.axis('off')
plt.show()

# Part 3: Average Distance Calculation
# Define the Haversine formula for distance calculation
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

average_distances = {}
grouped_cities = va_charger_locations.groupby('City')

for city, group in grouped_cities:
    locations = list(zip(group['Latitude'], group['Longitude']))
    if len(locations) < 2:
        average_distances[city] = 0  # No meaningful average distance
        continue

    distances = [haversine(locations[i][0], locations[i][1], locations[j][0], locations[j][1])
                 for i in range(len(locations)) for j in range(i + 1, len(locations))]
    average_distances[city] = sum(distances) / len(distances) * 0.621371  # Convert to miles

# Sort cities by average distance
average_distances_list = sorted(average_distances.items(), key=lambda x: x[1], reverse=True)

# Prepare the data for tabulation
table_data = [("City", "Average Distance (miles)")] + [(city, f"{distance:.2f}") for city, distance in average_distances_list]

# Print the formatted table
print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))



# Part 3

# Set a battery capacity in terms of distance in miles
max_capacity = 250  # Value from US Department of Transportation

# Set the dataframe to extract the latitude and longitude locations for every type of EV charger
charger_locations = df[['Latitude', 'Longitude', 'Level 1', 'Level 2', 'DC Fast']]
charger_locations = charger_locations[
    (charger_locations['Level 1'] > 0) | (charger_locations['Level 2'] > 0) | (charger_locations['DC Fast'] > 0)
]


def filter_chargers(current_location, max_distance):
    """
    Filter chargers within the range of the current battery capacity.

    :param current_location:
    :param max_distance:
    :return:
    """
    chargers_in_range = []
    for _, row in charger_locations.iterrows():
        charger_coords = (row['Latitude'], row['Longitude'])
        distance = geodesic(current_location, charger_coords).miles
        if distance <= max_distance:
            chargers_in_range.append((row['Latitude'], row['Longitude'], distance))
    return sorted(chargers_in_range, key=lambda x: x[2])  # Sort by proximity


def calculate_cost(charger, destination, charger_types):
    """
    Calculate a simple cost based on distance to the destination and charger speed.

    :param charger:
    :param destination:
    :param charger_types:
    :return:
    """
    charger_location = (charger[0], charger[1])
    distance_to_dest = geodesic(charger_location, destination).miles
    type_cost = {'Level 1': 50, 'Level 2': 6, 'DC Fast': 1}  # Approximate charging times from
    charger_speed = min(type_cost.get(charger_type, float('inf')) for charger_type in charger_types)

    return distance_to_dest + charger_speed  # Combine distance and charging speed


def find_best_route(start_coords, dest_coords, max_capacity):
    """
    Plan the best route with chargers between two locations.

    :param start_coords:
    :param dest_coords:
    :param max_capacity:
    :return:
    """
    current_location = start_coords
    remaining_distance = geodesic(current_location, dest_coords).miles
    route = []

    while remaining_distance > max_capacity:
        chargers_in_range = filter_chargers(current_location, max_capacity)

        if not chargers_in_range:
            print(f"No chargers available within range from {current_location}.")
            break  # Exit if no chargers are in range

        # Evaluate chargers and pick the best one
        charger_candidates = []
        for charger in chargers_in_range:
            charger_lat, charger_lon, _ = charger
            matching_row = charger_locations[
                (charger_locations['Latitude'] == charger_lat) &
                (charger_locations['Longitude'] == charger_lon)
                ]
            if not matching_row.empty:
                charger_types = []
                if matching_row.iloc[0]['Level 1'] > 0:
                    charger_types.append('Level 1')
                if matching_row.iloc[0]['Level 2'] > 0:
                    charger_types.append('Level 2')
                if matching_row.iloc[0]['DC Fast'] > 0:
                    charger_types.append('DC Fast')

                cost = calculate_cost(charger, dest_coords, charger_types)
                charger_candidates.append((charger, cost))

        if not charger_candidates:
            print("No suitable chargers found.")
            break  # Exit if no suitable chargers are available

        # Select the best charger
        best_charger = min(charger_candidates, key=lambda x: x[1])[0]
        route.append(best_charger)

        # Update the current location
        current_location = (best_charger[0], best_charger[1])
        remaining_distance = geodesic(current_location, dest_coords).miles

    if remaining_distance <= max_capacity:
        route.append(dest_coords)

    return route


if __name__ == "__main__":
    print("\nWelcome to the EV Route Optimizer!")

    start_lat = float(input("Enter the starting latitude: "))
    start_lon = float(input("Enter the starting longitude: "))
    dest_lat = float(input("Enter the destination latitude: "))
    dest_lon = float(input("Enter the destination longitude: "))

    start_coords = (start_lat, start_lon)
    dest_coords = (dest_lat, dest_lon)

    max_capacity = float(input("Enter the initial battery capacity (default is 250 miles): ") or 250)

    optimal_route = find_best_route(start_coords, dest_coords, max_capacity)

    print("\nOptimal Route:")
    for idx, stop in enumerate(optimal_route, 1):
        print(f"Stop {idx}: Latitude {stop[0]}, Longitude {stop[1]}")

    # Load and prepare the US map
    us_map = Image.open('us_map.jpg')
    img_width, img_height = us_map.size
    us_box = [-125.0, 25.0, -67.0, 50.0]


    # Convert latitude and longitude to pixel coordinates for plotting
    def lat_lon_to_pixels(lat, lon, box, width, height):
        x = (lon - box[0]) / (box[2] - box[0]) * width
        y = (lat - box[1]) / (box[3] - box[1]) * height
        return x, height - y  # Invert y-axis


    # Filter out stops that are outside the map's bounding box
    def filter_stops_within_bounds(stops, box):
        return [stop for stop in stops if box[1] <= stop[0] <= box[3] and box[0] <= stop[1] <= box[2]]


    # Filter the optimal route stops
    filtered_route = filter_stops_within_bounds(optimal_route, us_box)

    # Convert the filtered route stops to pixel coordinates
    route_pixels = [lat_lon_to_pixels(stop[0], stop[1], us_box, img_width, img_height) for stop in filtered_route]

    # Plot the route on the map
    plt.imshow(us_map.convert('RGB'), extent=(0, img_width, 0, img_height), origin='upper')

    # Plot the stops
    if route_pixels:
        x_coords, y_coords = zip(*route_pixels)
        plt.plot(x_coords, y_coords, marker='o', color='blue', label='Route Stops')

        # Annotate the stops
        for idx, (x, y) in enumerate(route_pixels, 1):
            plt.text(x, y, str(idx), color='red', fontsize=12, ha='center', va='center')
    else:
        print("No stops within the bounding box of the map.")

    plt.title('Optimal EV Route')
    plt.legend()
    plt.axis('off')
    plt.show()
