# Author: Spencer Gerlach
# Date: March 16, 2023

# ==== Imports ====
from dash import dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd
import geopandas as gpd
# from altair_data_server import data_server

# alt.data_transformers.enable('data_server')
# alt.renderers.enable('mimetype')

# ==== Housekeeping ====
# Read csv data (for most visuals)
df = pd.read_csv('../data/clean/permit_cleaned.csv', parse_dates=True)
df = df.sample(frac=0.2)
df['YearMonth'] = pd.to_datetime(df['YearMonth'])

# Read geojson data (neighbourhood polygons for chloropleth)
gdf = gpd.read_file('../data/clean/geo_nbhd_summary_long.geojson')

# ==== HTML stuff for the Information section ====
# Define the hyperlink and bullet list contents
hyperlink1 = html.A('Vancouver Open Data Portal', href='https://opendata.vancouver.ca/explore/dataset/issued-building-permits/information/')
hyperlink2 = html.A('Vancouver Building Permit Website', href='https://vancouver.ca/home-property-development/building-permit.aspx')
bullet_list = html.Ul([
    html.Li(hyperlink1),
    html.Li(hyperlink2)])
# Define the paragraph with the hyperlink and bullet list contents
paragraph = html.P([
    'For more information about Vancouver building permits, or the data behind this dashboard, visit:',
    html.Br(),
    bullet_list,
    html.Br(),
    'This dashboard focuses primarily on ', 
    html.B('residential'), 
    ' building types.'
])

# ==== Start the thing ====
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# ==== UI ====
app.layout = dbc.Container([
    
    dbc.Row([
        dbc.Col(html.H1("Vancouver Building Permit Summary")),
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H5("Comparison of Neighbourhood Summary Statistics"),
            html.Label("X-axis Value:"),
            dcc.Dropdown(
                id='selected_x1',
                options=[{'label': col, 'value': col} for col in ['PermitElapsedDays', 'ProjectValue']],
                value='PermitElapsedDays',
                style={'width':'100%'}
            ),
            html.Iframe(
                id='bars',
                style={'border-width': '0', 'width': '100%', 'height': '550px'})
        ], width=6),
        
        dbc.Col([
            html.H5("Neighbourhood Map of Summary Statistics"),
            html.Label("Summary Statistic:"),
            dcc.Dropdown(
                id='selected_map',
                options=[{'label': col, 'value': col} for col in ['count_permits',
                                                                  'elapsed_days_avg', 
                                                                  'elapsed_days_25q',
                                                                  'elapsed_days_50q',
                                                                  'elapsed_days_75q',
                                                                  'project_value_avg', 
                                                                  'project_value_25q',
                                                                  'project_value_50q',
                                                                  'project_value_75q'
                                                                  ]],
                value='count_permits',
                style={'width': '100%'}
            ),
            html.Iframe(
                id='map',
                style={'border-width': '0', 'width': '100%', 'height': '550px', 'padding-left':'50px'})
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H5('Count of Permits by Building Type'),
            html.Label("Specific Building Type:"),
            dcc.Dropdown(
                id='selected_use',
                options=[{'label': col, 'value': col} for col in ['1FD on Sites w/ More Than One Principal Building', 
                                                                  '1FD w/ Family Suite', 
                                                                  '2FD on Sites w/ Mult Principal Bldg', 
                                                                  'Duplex', 
                                                                  'Duplex w/Secondary Suite', 
                                                                  'Dwelling Unit', 
                                                                  'Dwelling Unit w/ Other Use', 
                                                                  'Freehold Rowhouse', 
                                                                  'Housekeeping Unit', 
                                                                  'Infill', 
                                                                  'Infill Multiple Dwelling', 
                                                                  'Infill Single Detached House', 
                                                                  'Infill Two-Family Dwelling', 
                                                                  'Laneway House', 
                                                                  'Micro Dwelling', 
                                                                  'Mixed', 
                                                                  'Multiple Conv Dwelling w/ Family Suite', 
                                                                  'Multiple Conv Dwelling w/ Sec Suite', 
                                                                  'Multiple Conversion Dwelling', 
                                                                  'Multiple Dwelling',
                                                                  'Not Applicable', 
                                                                  'Principal Dwelling Unit w/Lock Off', 
                                                                  'Residential Unit Associated w/ an Artist Studio', 
                                                                  'Residential/Business Unit', 
                                                                  'Rooming House', 
                                                                  'Secondary Suite'
                                                                  'Seniors Supportive/Assisted Housing', 
                                                                  'Single Detached House', 
                                                                  'Single Detached House w/Sec Suite', 
                                                                  'Sleeping Unit', 
                                                                  'Temporary Modular Housing'
                                                                  ]],
                value=['Duplex', 'Infill', 'Multiple Dwelling'],
                multi=True
            ),
            html.Iframe(
                id='lines',
                style={'border-width': '0', 'width': '100%', 'height': '550px'}
            )
        ]),
        dbc.Col([
            html.H5("More information"),
            paragraph

        ])
    ]),
], fluid=True)

# ==== Server ====
@app.callback(
    Output(component_id='bars', component_property='srcDoc'),
    Output(component_id='lines', component_property='srcDoc'),
    Output(component_id='map', component_property='srcDoc'),
    Input(component_id='selected_x1', component_property='value'),
    Input(component_id='selected_use', component_property='value'),
    Input(component_id='selected_map', component_property='value')
)
def plot_altair(x_axis, uses, map_stat):
    
    # ==== Bar Chart ====
    chart = alt.Chart(df, title="Comparison of Neighbourhood Summary Statistics").mark_bar().encode(
        x = alt.X("mean(%s)" % (x_axis), 
                  title = "Mean of %s" % (x_axis)),
        y = alt.Y("GeoLocalArea", 
                  sort = 'x', 
                  title = "Neighbourhood"),
        tooltip=alt.Tooltip("mean(%s)" % (x_axis),
                            format = '~f')
    ).interactive()
    
    # ==== Line Chart ====
    df_filtered = df.loc[df['SpecificUseCategory'].isin(uses)]
    chart2 = alt.Chart(df_filtered, title="Count of Building Permits by Building Type").mark_line().encode(
        x = alt.X("YearMonth"),
        y = alt.Y("count()"),
        color = alt.Color("SpecificUseCategory"),
        tooltip=alt.Tooltip(["SpecificUseCategory", "count()"])
    ).interactive()

    # ==== Chloropleth Map ====
    gdf_filtered = gdf.loc[gdf['stat'] == map_stat]
    chart3 = alt.Chart(gdf_filtered, title = "Chloropleth Map of Vancouver Neighbourhoods").mark_geoshape(stroke="grey").encode(
        color = alt.Color("value"),
        tooltip = ["name", "value"]
    ).project(type="identity", reflectY=True)

    # ==== Forth Chart ====

    return chart.to_html(), chart2.to_html(), chart3.to_html()

# ==== Run the bish ====
if __name__ == '__main__':
    app.run_server(debug=True)