# Import required libraries
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

import pandas as pd
spacex_df = pd.read_csv('spacex_launch_dash.csv')


# Create a dash application
app = Dash(__name__)

site_dropdown = dcc.Dropdown( ... )
payload_slider = dcc.RangeSlider( ... )

app.layout = html.Div([
    site_dropdown,
    payload_slider,
    dcc.Graph(id='success-pie-chart'),
    dcc.Graph(id='success-payload-scatter-chart')
])

# TASK 1: Add a Launch Site Drop-down Input Component
site_dropdown = dcc.Dropdown(
    id='site-dropdown',
    options=[
        {'label': 'All Sites', 'value': 'ALL'},
        {'label': 'site1', 'value': 'site1'},
        # Add other sites dynamically if needed
    ],
    value='ALL',
    placeholder="Select a launch site",
    searchable=True
)

# TASK 2: Callback to render success-pie-chart based on selected site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Pie chart showing overall success counts by site
        fig = px.pie(
            spacex_df, 
            names='Launch Site', 
            values='class',  # Assuming 'class' is 1 for success count
            title='Total Successful Launches by Site'
        )
    else:
        # Filter for the selected site and show success vs failure counts
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        fig = px.pie(
            success_counts, 
            names='class', 
            values='count', 
            title=f'Success vs Failure for site {entered_site}'
        )
    return fig

# TASK 3: Add a Range Slider to Select Payload range
# Get min and max payload from the dataframe for slider limits
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

payload_slider = dcc.RangeSlider(
    id='payload-slider',
    min=min_payload,
    max=max_payload,
    step=1000,
    marks={int(min_payload): str(int(min_payload)), int(max_payload): str(int(max_payload))},
    value=[min_payload, max_payload]
)

# TASK 4: Callback to render success-payload-scatter-chart based on site and payload slider
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Outcome Scatter Plot'
    )
    return fig
if __name__ == '__main__':
    app.run(debug=True)
