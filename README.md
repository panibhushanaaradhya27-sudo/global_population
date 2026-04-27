# Population Dataset Visualization (Run in VS Code)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV files
df = pd.read_csv("API_SP.POP.TOTL_DS2_en_csv_v2_121650.csv", skiprows=4)
meta_df = pd.read_csv("Metadata_Country_API_SP.POP.TOTL_DS2_en_csv_v2_121650.csv")

# -------------------------------
# HISTOGRAM: Population Distribution
# -------------------------------

# Find latest available year column
year_cols = [col for col in df.columns if col.isdigit()]
latest_year = max(year_cols, key=int)

# Convert population values to numbers
population = pd.to_numeric(df[latest_year], errors='coerce')
population = population.dropna()
population = population[population > 0]

# Create histogram
plt.figure(figsize=(10,6))
plt.hist(population / 1_000_000, bins=30, edgecolor='black')

plt.title(f"Distribution of Country Populations ({latest_year})")
plt.xlabel("Population (Millions)")
plt.ylabel("Number of Countries")
plt.grid(axis='y', alpha=0.3)
plt.show()


# -------------------------------
# BAR CHART: Countries by Region
# -------------------------------

region_counts = meta_df["Region"].dropna()
region_counts = region_counts[region_counts != ""]
region_counts = region_counts.value_counts()

plt.figure(figsize=(10,6))
region_counts.plot(kind='bar', color='skyblue', edgecolor='black')

plt.title("Number of Countries by Region")
plt.xlabel("Region")
plt.ylabel("Count")
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
