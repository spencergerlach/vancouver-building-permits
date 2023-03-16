from dash import dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd
import geopandas as gpd

alt.data_transformers.enable('data_server')

# Read data
df = pd.read_csv('../data/clean/permit_cleaned.csv')
gdf = gpd.read_file('../data/clean/geo_nbhd_summary_long.geojson')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# UI
app.layout = html.Div([
    html.H1("Vancouver Building Permits"),
    html.Br(),
    html.Div([
        html.Div([
            html.Label("X-axis Value:"),
            dcc.Dropdown(
                id='selected_x1',
                options=[{'label': col, 'value': col} for col in ['PermitElapsedDays', 'ProjectValue']],
                value='PermitElapsedDays',
                style={'width':'50%'}
            ),
            html.Iframe(
                id='bars',
                style={'border-width': '0', 'width': '50%', 'height': '500px'})
        ] ), #, className="six columns"
        html.Div([
            html.Label("Summary Statistic:"),
            dcc.Dropdown(
                id='selected_map',
                options=[{'label': col, 'value': col} for col in ['elapsed_days_avg', 'project_value_avg', 'count_permits']],
                value='count_permits',
                style={'width': '50%'}
            ),
            html.Br(),
            html.Iframe(
                id='map',
                style={'border-width': '0', 'width': '50%', 'height': '500px', 'padding-left':'50px'})
        ] ) #, className="six columns"
    ], className="row"),
    dcc.Dropdown(
        id='selected_use',
        options=[{'label': col, 'value': col} for col in ['1FD on Sites w/ More Than One Principal Building', 
                                                          '1FD w/ Family Suite', 
                                                          '2FD on Sites w/ Mult Principal Bldg', 
                                                          'Duplex', 
                                                          'Duplex w/Secondary Suite', 
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
                                                          'Not Applicable', 
                                                          'Principal Dwelling Unit w/Lock Off', 
                                                          'Residential Unit Associated w/ an Artist Studio', 
                                                          'Residential/Business Unit', 
                                                          'Rooming House', 
                                                          'Seniors Supportive/Assisted Housing', 
                                                          'Single Detached House', 
                                                          'Single Detached House w/Sec Suite', 
                                                          'Sleeping Unit', 
                                                          'Temporary Modular Housing', 
                                                          'Dwelling Unit', 
                                                          'Dwelling Unit w/ Other Use', 
                                                          'Multiple Dwelling', 
                                                          'Secondary Suite']],
        value=['Duplex', 'Infill', 'Multiple Dwelling'],
        multi=True
    ),
    html.Br(),
    html.Iframe(
        id='lines',
        style={'border-width': '0', 'width': '100%', 'height': '600px'}),
])



# Server
@app.callback(
    Output(component_id='bars', component_property='srcDoc'),
    Output(component_id='lines', component_property='srcDoc'),
    Output(component_id='map', component_property='srcDoc'),
    Input(component_id='selected_x1', component_property='value'),
    Input(component_id='selected_use', component_property='value'),
    Input(component_id='selected_map', component_property='value')
)
def plot_altair(x_axis, uses, map_stat):
    
    chart = alt.Chart(df).mark_bar().encode(
        x = alt.X("mean(%s)" % (x_axis), 
                  title = "Mean of %s" % (x_axis)),
        y = alt.Y("GeoLocalArea", 
                  sort = 'x', 
                  title = "Neighbourhood"),
        tooltip=alt.Tooltip("mean(%s)" % (x_axis),
                            format = '~f')
    ).interactive()
    
    df_filtered = df.loc[df['SpecificUseCategory'].isin(uses)]
    # df_filtered = df[df['SpecificUseCategory'].str.contains('|'.join(uses))]
    chart2 = alt.Chart(df_filtered).mark_line().encode(
        x = alt.X("YearMonth"),
        y = alt.Y("count()"),
        color = alt.Color("SpecificUseCategory"),
        tooltip=alt.Tooltip(["SpecificUseCategory", "count()"])
    ).interactive()

    gdf_filtered = gdf.loc[gdf['stat'] == map_stat]
    chart3 = alt.Chart(gdf_filtered, title = "Chloropleth Map of Vancouver Neighbourhoods").mark_geoshape().encode(
        color = alt.Color("value"),
        tooltip = ["name", "value"]
    ).project(type="identity", reflectY=True)

    return chart.to_html(), chart2.to_html(), chart3.to_html()

# Run the bish
if __name__ == '__main__':
    app.run_server(debug=True)