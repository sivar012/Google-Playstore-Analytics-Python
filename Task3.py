import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pytz
import os
# Load dataset
df = pd.read_csv('C:/Users/Hemanth/OneDrive/Shiva/Play Store Data.csv') # Modify the path as we want
# Define IST timezone
ist = pytz.timezone('Asia/Kolkata')
now_ist = datetime.now(ist)
current_hour = now_ist.hour
# Remove invalid 'Installs' values (e.g., 'Free', missing, etc.)
df = df[df['Installs'].str.contains(r'^\d+[+,]?', regex=True, na=False)]
# Ensure output directory exists
output_path = "C:/Users/Hemanth/OneDrive/Shiva/Install_trends.png" # Modify the path as we want
os.makedirs(os.path.dirname(output_path), exist_ok=True)
# Convert installs and reviews to numeric
df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True).astype(float)
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
# Apply filters
filtered_df = df[
    (df['Category'].str.startswith(('E', 'C', 'B'), na=False)) &
    (~df['App'].str.lower().str.startswith(('x', 'y', 'z'))) &
    (~df['App'].str.contains('s', case=False, na=False)) &
    (df['Reviews'] > 500)
]
# Assign fake "Last Updated" dates for simulation
filtered_df['Last Updated'] = pd.to_datetime(filtered_df['Last Updated'], errors='coerce')
filtered_df.dropna(subset=['Last Updated'], inplace=True)
# Group by month and category
filtered_df['Month'] = filtered_df['Last Updated'].dt.to_period('M').dt.to_timestamp()
category_translation = {
    "Beauty": "सौंदर्य",       # Hindi
    "Business": "வணிகம்",     # Tamil
    "Dating": "Partnersuche"  # German
}
filtered_df['Translated Category'] = filtered_df['Category'].replace(category_translation)
# Group data
grouped = filtered_df.groupby(['Month', 'Translated Category'])['Installs'].sum().reset_index()
grouped.sort_values(by=['Translated Category', 'Month'], inplace=True)
# Allow graph only between 6 PM and 9 PM IST
if 18 <= current_hour < 21:
    # Plotting
    plt.figure(figsize=(14, 7))
    for cat in grouped['Translated Category'].unique():
        cat_df = grouped[grouped['Translated Category'] == cat].copy()
        plt.plot(cat_df['Month'], cat_df['Installs'], label=cat)
    
        # Shade growth >20%
        cat_df['pct_change'] = cat_df['Installs'].pct_change()
        growth_periods = cat_df[cat_df['pct_change'] > 0.2]
        for _, row in growth_periods.iterrows():
            plt.axvspan(row['Month'] - pd.DateOffset(days=15),
                        row['Month'] + pd.DateOffset(days=15),
                        color='orange', alpha=0.2)
    
    plt.title("Monthly Install Trends by Category (Filtered Apps)")
    plt.xlabel("Month")
    plt.ylabel("Total Installs")
    plt.legend(title="App Category")
    plt.grid(True)
    plt.tight_layout()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Chart saved to: {output_path}")
else:
    print(f"Graph generation is disabled. Current IST time: {now_ist.strftime('%H:%M:%S')} (Allowed: 18:00–21:00)")
