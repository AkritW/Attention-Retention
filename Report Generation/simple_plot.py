import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read JSON data from file
with open("people_data.json", "r") as f:
    json_data = json.load(f)

# Get people data from JSON object
people_data = json_data["people"]

# Create data frame with values as rows and columns as time
data = []
for person in people_data:
    values = [data_point["value"] for data_point in person["data"]]
    data.append(values)

df = pd.DataFrame(data).T
df.columns = [person["name"] for person in people_data]

# Calculate average for each person and get the average
means = df.mean(axis=1)
mean = np.mean(means)

# Calculate rolling mean with window size of 10
rolling_mean = means.rolling(window=20).mean()

# Create color tone plot using a line plot
plt.plot(range(len(means)), rolling_mean, color="red")

ppl_values = []
for person in people_data:
    p = []
    for data in person["data"]:
        p.append(data["value"])
    ppl_values.append(p)

# Calculate rolling mean for each person's data with window size of 10
rolling_ppl_values = []
for p in ppl_values:
    rolling_ppl_values.append(pd.Series(p).rolling(window=40).mean())

for rp in rolling_ppl_values:
    plt.plot(range(len(rp)), rp, color="orange", alpha=0.2)

# Set plot title and labels
plt.title("Attention Span Plot")
plt.xlabel("Time")
plt.ylabel("Standard Deviation")

# Save Image
plt.savefig("-1.png")

# Display the plot
# plt.show()

plt.cla()
plt.clf()
