import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd 
from geopy.geocoders import Nominatim
import haversine as hs
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


########### Load data 
df = pd.read_csv('SmallTownMurderData.csv')

########### Set up the map 
mapbox_access_token = open("mapboxtoken.txt").read()
title = df['title']
Location = df['Location']
fig = go.Figure(go.Scattermapbox(
        lat=df['lat'],
        lon=df['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=5, color='firebrick' 
        ),
        text=df['title'],
        hoverinfo = 'text'
        
    ))

fig.update_layout(
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=38,
            lon=-102
        ),
        pitch=0,
        zoom=1,
        style='dark'
    ),
    height = 800, 
    width = 800
)

fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
)

fig.update_layout(
    title="Small Town Murder Episodes",
    font=dict(
    family="Rockwell",
    size=36,
    color="firebrick"
    )
)



########### Set up the layout 
external_stylesheets = ['https://codepen.io/chriddp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server 
app.title ="Murder Map!"
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Graph(figure=fig),
    html.H3('Find the Episode Closest to Your Address', className = "header_text"),
    dcc.Input(id='input-1-state', type = 'text', value = 'Address'),
    html.Button(id='submit-button-state', children = 'Submit'),
    html.Div(id='output-state'),
    html.Label(['\n\nCheck out the Small Town Murder podcast at ', 
                html.A('shutupandgivememurder.com', href='https://shutupandgivememurder.com', target="_blank")])
   

])

@app.callback(Output(component_id = 'output-state', component_property = 'children'),
              [Input('submit-button-state', 'n_clicks')],
              state = [State(component_id = 'input-1-state', component_property = 'value')]
              )

def update_output(n_clicks, input1):
    if n_clicks is None:
        raise PreventUpdate
#    elif input1 == '':
 #       nearestEpisode = ''
    else:
        geolocator = Nominatim(user_agent="app")
        location = geolocator.geocode(input1)

        coords = (location.latitude, location.longitude)
        distance = []

        for i in range(len(df['lat'])): 
            episode_coords = (df['lat'].iloc[i], df['lon'].iloc[i])
            distance.append(hs.haversine(coords, episode_coords))

        df['Distance'] = distance
        nearestEpisode = df['title'].iloc[df['Distance'].idxmin()]

    return u'The nearest episode to your address is {}'.format(nearestEpisode)


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader = False)
