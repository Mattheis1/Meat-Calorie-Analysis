import http.client
import json
import matplotlib.pyplot as plt
import pandas as pd

# Make the HTTP request to fetch the JSON data
conn = http.client.HTTPSConnection("www.calories.info")
conn.request("GET", "/page-data/food/meat/page-data.json", "")
res = conn.getresponse()
data = res.read().decode("utf-8")

# Parse the JSON data
food_data = json.loads(data)
meats = food_data["result"]["data"]["allFoodCategory"]["nodes"][0]["childrenFood"]

# Create a list of meats with calories per gram
meat_calories_per_gram = []

for meat in meats:
    name = meat["name"]
    if "displayPortionCalories" in meat and "displayServingSize" in meat:
        calories = float(meat["displayPortionCalories"])
        serving_size = float(meat["displayServingSize"])
        if serving_size > 0 and calories != 0:
            calories_per_gram = calories / serving_size
            meat_calories_per_gram.append((name, calories_per_gram))

# Sort the meats by calories per gram
meat_calories_per_gram.sort(key=lambda x: x[1])

# Print the top 5 meats with the least calories per gram
top_5_meats = meat_calories_per_gram[:5]

print("Top 5 Meats with the Least Calories per Gram:")
for i, (name, calories_per_gram) in enumerate(top_5_meats, start=1):
    print(f"{i}. {name}: {calories_per_gram:.2f} calories per gram")

df = pd.DataFrame(top_5_meats)
#print(df)
plt.bar(df[0], df[1])

plt.xlabel('Top 5 lowest CPG Meats', fontsize=14)
plt.ylabel('Calories per Gram (CPG)', fontsize=14)
plt.show()