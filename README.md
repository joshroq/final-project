# Analyzing EV infrastructure data and Optimizing Routes for EV owners
The Repository to hold the resources for the final project for ENGR340. The project is focused on utilizing locational fuel station data to give valuable information about EV charging and create an optimization algorithm for EV owners for long trips.

# Required Dependencies
Required Python Libraries:
pandas
pyplot from matplotlib
Image from PIL
math
tabulate
geodesic from geopy.distance

Required dataset: (https://catalog.data.gov/dataset/alternative-fueling-station-locations-422f2/resource/341957d8-daf6-4a38-ab1d-8ec1bc21cfb9)

Required images present within the repository.

# The main programs
The main programs utilized within this project are split into four parts. 

The first part is a program  that focuses on utilizing the raw data from the dataset to analyze and visualize the EV infrastructure across the US. This program will utilize pandas to analyze and graph the image in bar graph format. A bar graph for every type of EV charger and the all of them at once will be created. The pandas for the EV charger data for every state and for the total of the US will also be printed to the console.

The second part of the program focuses on just the data from Virginia and creates a distribution map of the EV chargers in the state. It will utilize PIL to create the Virginia image, pandas to perform data analysis, and matplotlib to plot the results. The only results of this program are a dot map.

The third part of the program focuses on the distance data between all of the EV chargers in Virginia. The program performs calculations on the distance between chargers using pandas and geopy and calculates the average distance between chargers in every county of Virginia. The results of the information are tabulated and printed to the console.

The fourth part of the program is the optimization algorithm. This program defines multiple functions to allow the algorithm to work in the if "__name__" == "__main__" function as the program runs. The functions are "filter_chargers()", "calculate_cost()", and "find_best_route()". 

filter_chargers() takes in the current location of the user in a tuple with the longitude and latitude data and the current capacity for the user in miles and filters out any charger not in range of the user. It outputs a list of the chargers that can be reached in the form of a list of tuples with longitude and latitude data.

calculate_cost() takes a tuple for the longitude and latitude for a charger location, the destination of the whole route, and the types of chargers available at the fuel station. It performs a weighted cost analysis to determine what the worth of going to that charger is and outputs that value as a float.

find_best_route() takes the user's input for the latitude and longitude for the user's starting location as floats, the latitude and longitude for the user's end location as floats, and the initial capacity that the user is starting with for their battery. It runs both the filter_chargers() and calculate_cost() functions on repeat to determine the best stops for the route and outputs them as a list of tuples containing the longitude and latitude data.

In the if "__name__" == "__main__" function, the find_best_route() function is ran and the user is prompted to input the necessary parameters. Afterwards, the code is ran and the results from running the code are printed. A map of the US is then downloaded using PIL and the results are printed on that map.

# Walkthrough
After running the code, the analysis for the first 3 parts will be performed on its own and the results will all be printed to the command window. Each of the figures will pop up one after the other to display the data. The command window will then prompt the user to input the necessary parameters to run the optimization algorithm. Input the longitude and latitude as float values. Make sure that the values are signed appropriately with longitudes being negative (-) in the West and latitudes being negative (-) in the South. The initial capacity is asked for, but a default value of 250 miles will be used if not provided.

# Output samples
Program 1 Output Example:

 Level 1  Level 2  DC Fast  Every Type
State                                       
AK           0       65        5          70
AL          30      499       97         626
AR           2      359       66         427
AZ           5     1615      414        2034
CA         701    32551     5968       39220

Program 3 Output Example:
╒═════════════════════════╤════════════════════════════╕
│ City                    │   Average Distance (miles) │
╞═════════════════════════╪════════════════════════════╡
│ Portsmouth              │                      24.95 │
├─────────────────────────┼────────────────────────────┤
│ Woodford                │                       9.9  │
├─────────────────────────┼────────────────────────────┤
│ Bedford                 │                       9.38 │
├─────────────────────────┼────────────────────────────┤
│ King George             │                       8.79 │
├─────────────────────────┼────────────────────────────┤
│ Richmond                │                       6.67 │
├─────────────────────────┼────────────────────────────┤
│ South Boston            │                       6.51 │
├─────────────────────────┼────────────────────────────┤
│ Floyd                   │                       5.57 │
├─────────────────────────┼────────────────────────────┤
│ Chesapeake              │                       5.41 │
├─────────────────────────┼────────────────────────────┤
│ Virginia Beach          │                       5.15 │
├─────────────────────────┼────────────────────────────┤

Program 4 Output Example:

Welcome to the EV Route Optimizer!
Enter the starting latitude: 37.2388
Enter the starting longitude: -76.5097
Enter the destination latitude: 40.7128
Enter the destination longitude: -74.0060
Enter the initial battery capacity (default is 250 miles): 230

Optimal Route:
Stop 1: Latitude 40.1938, Longitude -74.5954
Stop 2: Latitude 40.7128, Longitude -74.006


# Limitations
The main limitations with the code come in the final map result having inaccuracy on plotted information. The code has built-in measures for improper data given for parameters as long as they follow the right types of data.

# Future Results
Improvements should be made to the final map generated to create more accurate results to the provided map. Additionally, new data may be utilized to analyze more charging options and allow for more factors to be considered in the optimization algorithm.
