import pandas as pd
import geopy
from geopy.geocoders import Nominatim
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

#Turning the xls file into a pandas dataframe
city_temps = 'city_temperatures.xlsx'
df = pd.read_excel(city_temps)

#To check out the first few rows of the initial dataframe
df.head()

# #Geocoder toy example
locator = Nominatim(user_agent='saifahme@buffalo.edu')
location = locator.geocode('Albuquerque, NM')
# print('Latitude = {}, Longitude = {}'.format(location.latitude, location.longitude))

#Adding Latitude and Longitude columns to the dataframe
Latitude = []
Longitude = []

for i in range(df.shape[0]):
    Latitude.append((locator.geocode('%s, %s' % (df['City'][i], df['State'][i]))).latitude)
    Longitude.append((locator.geocode('%s, %s' % (df['City'][i], df['State'][i]))).longitude)

df['Latitude'] = Latitude
df['Longitude'] = Longitude 

#To check out the first few rows of the revised dataframe
df.head()

#Using plotly to show data on the map
#Created a Mapbox account at "https://studio.mapbox.com/" to get a public token 
token = 'pk.eyJ1IjoiY3NhaWYiLCJhIjoiY2wwYnJiYW9mMTA5ZDNqbWczYnRkZ242ciJ9.SyoWnR-M1id4C5pdwmOF6w'

card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]

px.set_mapbox_access_token(token)
fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color='Avg Temp [degrees F]', hover_name="City",
                            size='Avg Temp [degrees F]', color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig),

])

app.run_server(debug=True, use_reloader=False) 