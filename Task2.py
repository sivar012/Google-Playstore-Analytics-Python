import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import pytz
import random
# Load dataset
df = pd.read_csv('C:/Users/Hemanth/OneDrive/Shiva/Play Store Data.csv') #Modify the path as your wish
# Clean 'Installs' column
df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
# Drop rows with missing values
df_cleaned = df.dropna(subset=['Category', 'Installs'])
# Filter out categories starting with A, C, G, S
df_filtered = df_cleaned[~df_cleaned['Category'].str.startswith(('A', 'C', 'G', 'S'))]
# Aggregate installs by category
category_installs = df_filtered.groupby('Category')['Installs'].sum().sort_values(ascending=False)
top_categories = category_installs.head(5).reset_index()
# Simulate country-wise installs
country_codes = ['USA', 'IND', 'BRA', 'CHN', 'RUS', 'ZAF', 'AUS', 'GBR', 'CAN', 'FRA']
data = []
for _, row in top_categories.iterrows():
    category = row['Category']
    total_installs = row['Installs']
    selected_countries = random.sample(country_codes, 5)
    weights = np.random.dirichlet(np.ones(5), size=1)[0]
    for i in range(5):
        installs = int(total_installs * weights[i])
        data.append({
            'Country': selected_countries[i],
            'Category': category,
            'Installs': installs
        })

choropleth_data = pd.DataFrame(data)
choropleth_data['Highlight'] = choropleth_data['Installs'] > 1_000_000
choropleth_data = choropleth_data[choropleth_data['Installs'] > 1_000_000]
# Get current time in IST
ist = pytz.timezone('Asia/Kolkata')
current_time_ist = datetime.now(ist)
hour = current_time_ist.hour
# Generate and save Choropleth map only between 6 PM and 8 PM IST
if 18 <= hour < 20:
    fig = px.choropleth(
        choropleth_data,
        locations='Country',
        locationmode='ISO-3',
        color='Installs',
        hover_name='Category',
        title='Top 5 App Categories by Country-wise Installs',
        color_continuous_scale='Plasma'
    )
    fig.update_layout(geo=dict(showframe=False, showcoastlines=True))

    # Save to HTML
    fig.write_html('C:/Users/Hemanth/OneDrive/Shiva/choropleth_map.html') #Modify the path as your wish
    print("Map saved as choropleth_map.html in respective path")
else:
    print(f"Choropleth map is hidden. Current IST time: {current_time_ist.strftime('%H:%M:%S')} (Allowed: 18:00–20:00)")
