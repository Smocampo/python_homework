import plotly.express as px
import plotly.data as pldata
import pandas as pd

# 1. Load the Plotly wind dataset
df = pldata.wind(return_type='pandas')

# Print the first and last 10 lines of the DataFrame
print("--- FIRST 10 LINES ---")
print(df.head(10))
print("\n--- LAST 10 LINES ---")
print(df.tail(10))

# 2. Clean the data
df['strength'] = df['strength'].str.replace(r'[^0-9.]', '', regex=True).astype(float)

# 3. Create an interactive scatter plot 
fig = px.scatter(
    df, 
    x='strength', 
    y='frequency', 
    color='direction',
    title='Wind Analysis: Frequency vs. Strength by Direction',
    labels={
        'strength': 'Wind Strength',
        'frequency': 'Frequency of Occurrence',
        'direction': 'Compass Direction'
    }
)

fig.update_traces(marker=dict(size=12, opacity=0.8, line=dict(width=1, color='DarkSlateGrey')))

# 4. Save the plot as an HTML 
fig.write_html('wind.html')

import webbrowser
import os
webbrowser.open('file://' + os.path.realpath('wind.html'))