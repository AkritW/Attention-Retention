import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Interpolate data to 100 rows
df = df.interpolate(method="linear", axis=0).iloc[:: int(df.shape[0] / 100)]

# Calculate standard deviation for each person and get the average
stds = df.std(axis=1)
avg_std = np.mean(stds)

# Create color tone plot using a bar plot
colors = plt.cm.YlOrRd(stds / avg_std)
plt.bar(range(len(stds)), stds, color=colors)

# Set plot title and labels
plt.title("Attention Span Plot")
plt.xlabel("Time")
plt.ylabel("Standard Deviation")


plt.xticks(
    # data_point["session"] for data_point in people_data[0]["data"]
    range(len(people_data[0]["data"][:100])),
    [
        f"Session {(i // 50)+1}" if i % 50 == 0 else ""
        for i in range(len(people_data[0]["data"][:100]))
    ],
)

# Save Image
plt.savefig("1.png")

# Show the plot
# plt.show()

plt.cla()
plt.clf()
