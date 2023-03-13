from dash import dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import altair as alt
from vega_datasets import data

cars = data.cars()

def plot_altair(xmax):
    chart = alt.Chart(cars[cars["Horsepower"] < xmax]).mark_point().encode(
        x = "Horsepower",
        y = "Weight_in_lbs"
    )
    return chart.to_html()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
        html.H1("Test Dash App"),
        html.Iframe(
            id='scatter',
            srcDoc=plot_altair(xmax=0),
            style={'border-width': '0', 'width': '100%', 'height': '400px'}),
        dcc.Slider(id='xslider', min=0, max=240)])

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xslider', 'value')
)
def update_output(xmax):
    return plot_altair(xmax)

if __name__ == '__main__':
    app.run_server(debug=True)