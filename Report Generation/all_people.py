import json
import seaborn as sns
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

# Interpolate data to 100 rows
df = df.interpolate(method="slinear", axis=0).iloc[
    :: int(df.shape[0] / (len(data)))
]

# Calculate standard deviation for each person
stds = df.std(axis=1)

# Create heatmap with highlighted values
ax = sns.heatmap(
    df,
    cmap="YlOrRd",
    mask=df >= (stds * 2).values.reshape(-1, 1),
)

ax.set_yticklabels(
    # data_point["session"] for data_point in people_data[0]["data"]
    [
        f"Session {(i // 5)+1}" if i % 5 == 0 else ""
        for i in range(len(people_data))
    ]
)

# Save Image
plt.savefig("0.png")

# Display the plot
# plt.show()

plt.cla()
plt.clf()
