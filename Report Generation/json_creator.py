import json
import random
import datetime

# Set the number of people and number of data points
num_people = 10
num_data_points = 1000

# Generate names for the people
names = ["Person {}".format(i + 1) for i in range(num_people)]

# Generate data for each person
people_data = []

for name in names:
    # Generate random data following a normal distribution
    data = [
        max(0, round(random.gauss(50, 15), 2)) for _ in range(num_data_points)
    ]

    # Generate timestamps for the data points
    start_date = datetime.datetime(2022, 1, 1)
    timestamps = [
        (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(num_data_points)
    ]

    # Generate session for the class
    sessions = [
        "Session {}".format(i + 1) if i % 100 == 0 else ""
        for i in range(num_data_points)
    ]

    # Combine the data and timestamps for the person
    person_data = [
        {"value": data[i], "timestamp": timestamps[i], "session": sessions[i]}
        for i in range(num_data_points)
    ]

    # Add the person's data to the list of people's data
    people_data.append({"name": name, "data": person_data})

# Combine the people's data into a JSON object
json_data = {"people": people_data}

# Write the JSON object to a file
with open("people_data.json", "w") as f:
    json.dump(json_data, f)
