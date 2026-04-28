import pandas as pd
import os
import glob
import matplotlib.pyplot as plt

# --------------------------------------------------
# Load CSV File Automatically
# --------------------------------------------------
base = os.path.dirname(__file__)
files = glob.glob(os.path.join(base, "API_SP.POP.TOTL*.csv"))

if not files:
    print("CSV file not found.")
    exit()

csv_file = files[0]

# Read Dataset
df = pd.read_csv(csv_file, skiprows=4)

# --------------------------------------------------
# Clean Data
# --------------------------------------------------
df_clean = df[['Country Name', 'Country Code', '2024']].dropna()

df_clean = df_clean.rename(columns={
    'Country Name': 'Country',
    'Country Code': 'Code',
    '2024': 'Population'
})

# Only Real Countries
real_countries = [
    'IND','CHN','USA','IDN','PAK','NGA','BRA','BGD','RUS','MEX',
    'JPN','ETH','PHL','EGY','VNM','COD','TUR','IRN','DEU','THA'
]

df_clean = df_clean[df_clean['Code'].isin(real_countries)]

# --------------------------------------------------
# Calculate Percentages
# --------------------------------------------------
total_population = df_clean['Population'].sum()

df_clean['World Population %'] = (
    df_clean['Population'] / total_population
) * 100

# Top 10 Countries
top10 = df_clean.sort_values(
    by='Population',
    ascending=False
).head(10).reset_index(drop=True)

# --------------------------------------------------
# Print Table
# --------------------------------------------------
print("\nTop 10 Most Populated Countries (2024)\n")

print(top10.to_string(
    index=False,
    formatters={
        'Population': '{:,.0f}'.format,
        'World Population %': '{:.2f}%'.format
    }
))

# --------------------------------------------------
# Create Professional Charts
# --------------------------------------------------
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# ---------------- Bar Chart ----------------
bars = axes[0].bar(
    top10['Country'],
    top10['Population']
)

axes[0].set_title(
    'Top 10 Most Populated Countries (2024)',
    fontsize=16,
    fontweight='bold'
)

axes[0].set_xlabel('Country')
axes[0].set_ylabel('Population')
axes[0].tick_params(axis='x', rotation=45)

# Labels on bars
for bar in bars:
    yval = bar.get_height()
    axes[0].text(
        bar.get_x() + bar.get_width()/2,
        yval,
        f'{int(yval):,}',
        ha='center',
        va='bottom',
        fontsize=8
    )

# ---------------- Histogram ----------------
axes[1].hist(
    df_clean['Population'],
    bins=10,
    edgecolor='black'
)

axes[1].set_title(
    'Population Distribution (Selected Countries)',
    fontsize=16,
    fontweight='bold'
)

axes[1].set_xlabel('Population')
axes[1].set_ylabel('Frequency')

# --------------------------------------------------
# Final Layout
# --------------------------------------------------
plt.tight_layout()
plt.show()
