import subprocess
import sys

#list of required packages
required_packages = [
    "dash",
    "pandas",
    "plotly",
]

#method to install missing packages
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in required_packages:
    install_and_import(pkg)

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

#read the dataset
file_path = 'world-data-2023.csv'
df = pd.read_csv(file_path)

#drop unnecessary columns
df = df.drop(columns=['Abbreviation', 'Capital/Major City', 'Currency-Code', 'Largest city', 'Official language', 'Calling Code', 'Latitude', 'Longitude'])

#drop rows with NaN values
df = df.dropna()

#correct the format of the numeric columns by stripping and removing string characters
df['Country_ID'] = df['Country'].astype('category').cat.codes
df['Population'] = df['Population'].replace({',': ''}, regex=True).astype(float)
df['Urban_population'] = df['Urban_population'].replace({',': ''}, regex=True).astype(float)
df['Density\n(P/Km2)'] = df['Density\n(P/Km2)'].replace({',': ''}, regex=True).astype(float)
df['Land Area(Km2)'] = df['Land Area(Km2)'].replace({',': ''}, regex=True).astype(float)
df['Agricultural Land( %)'] = df['Agricultural Land( %)'].replace({'%': ''}, regex=True).astype(float)
df['Armed Forces size'] = df['Armed Forces size'].replace({',': ''}, regex=True).astype(float)
df['Co2-Emissions'] = df['Co2-Emissions'].replace({',': ''}, regex=True).astype(float)
df['CPI'] = df['CPI'].replace({',': ''}, regex=True).astype(float)
df['CPI Change (%)'] = df['CPI Change (%)'].replace({'%': ''}, regex=True).astype(float)
df['Forested Area (%)'] = df['Forested Area (%)'].replace({'%': ''}, regex=True).astype(float)
df['Gasoline Price'] = df['Gasoline Price'].replace({r'[^\d.]': '', ' ': ''}, regex=True).astype(float)
df['Unemployment rate'] = df['Unemployment rate'].replace({r'[^\d.]': '', ' ': ''}, regex=True).astype(float)
df['Out of pocket health expenditure'] = df['Out of pocket health expenditure'].replace({r'[^\d.]': '', ' ': ''}, regex=True).astype(float)
df['GDP'] = df['GDP'].replace({r'[^\d.]': '', ',':''}, regex=True).astype(float)
df['Primary education'] = df['Gross primary education enrollment (%)'].replace({r'[^\d.]': '', ',':''}, regex=True).astype(float)
df['Tertiary education'] = df['Gross tertiary education enrollment (%)'].replace({r'[^\d.]': '', ',':''}, regex=True).astype(float)
df['Minimum wage'] = df['Minimum wage'].replace({r'[^\d.]': '', ',':''}, regex=True).astype(float)

#drop columns that are corrected above
df = df.drop(columns=['Gross primary education enrollment (%)', 'Gross tertiary education enrollment (%)'])

#map countries to regions
country_to_region = {
    "Afghanistan": "Asia", "Albania": "Europe", "Algeria": "Africa", "Andorra": "Europe",
    "Angola": "Africa", "Antigua and Barbuda": "North America", "Argentina": "South America",
    "Armenia": "Asia", "Australia": "Oceania", "Austria": "Europe", "Azerbaijan": "Asia",
    "The Bahamas": "North America", "Bahrain": "Asia", "Bangladesh": "Asia", "Barbados": "North America",
    "Belarus": "Europe", "Belgium": "Europe", "Belize": "North America", "Benin": "Africa",
    "Bhutan": "Asia", "Bolivia": "South America", "Bosnia and Herzegovina": "Europe", "Botswana": "Africa",
    "Brazil": "South America", "Brunei": "Asia", "Bulgaria": "Europe", "Burkina Faso": "Africa",
    "Burundi": "Africa", "Ivory Coast": "Africa", "Cape Verde": "Africa", "Cambodia": "Asia",
    "Cameroon": "Africa", "Canada": "North America", "Central African Republic": "Africa", "Chad": "Africa",
    "Chile": "South America", "China": "Asia", "Colombia": "South America", "Comoros": "Africa",
    "Republic of the Congo": "Africa", "Costa Rica": "North America", "Croatia": "Europe", "Cuba": "North America",
    "Cyprus": "Europe", "Czech Republic": "Europe", "Democratic Republic of the Congo": "Africa", "Denmark": "Europe",
    "Djibouti": "Africa", "Dominica": "North America", "Dominican Republic": "North America", "Ecuador": "South America",
    "Egypt": "Africa", "El Salvador": "North America", "Equatorial Guinea": "Africa", "Eritrea": "Africa",
    "Estonia": "Europe", "Eswatini": "Africa", "Ethiopia": "Africa", "Fiji": "Oceania", "Finland": "Europe",
    "France": "Europe", "Gabon": "Africa", "The Gambia": "Africa", "Georgia": "Asia", "Germany": "Europe",
    "Ghana": "Africa", "Greece": "Europe", "Grenada": "North America", "Guatemala": "North America", "Guinea": "Africa",
    "Guinea-Bissau": "Africa", "Guyana": "South America", "Haiti": "North America", "Vatican City": "Europe",
    "Honduras": "North America", "Hungary": "Europe", "Iceland": "Europe", "India": "Asia", "Indonesia": "Asia",
    "Iran": "Asia", "Iraq": "Asia", "Republic of Ireland": "Europe", "Israel": "Asia", "Italy": "Europe",
    "Jamaica": "North America", "Japan": "Asia", "Jordan": "Asia", "Kazakhstan": "Asia", "Kenya": "Africa",
    "Kiribati": "Oceania", "Kuwait": "Asia", "Kyrgyzstan": "Asia", "Laos": "Asia", "Latvia": "Europe", "Lebanon": "Asia",
    "Lesotho": "Africa", "Liberia": "Africa", "Libya": "Africa", "Liechtenstein": "Europe", "Lithuania": "Europe",
    "Luxembourg": "Europe", "Madagascar": "Africa", "Malawi": "Africa", "Malaysia": "Asia", "Maldives": "Asia",
    "Mali": "Africa", "Malta": "Europe", "Marshall Islands": "Oceania", "Mauritania": "Africa", "Mauritius": "Africa",
    "Mexico": "North America", "Federated States of Micronesia": "Oceania", "Moldova": "Europe", "Monaco": "Europe",
    "Mongolia": "Asia", "Montenegro": "Europe", "Morocco": "Africa", "Mozambique": "Africa", "Myanmar": "Asia",
    "Namibia": "Africa", "Nauru": "Oceania", "Nepal": "Asia", "Netherlands": "Europe", "New Zealand": "Oceania",
    "Nicaragua": "North America", "Niger": "Africa", "Nigeria": "Africa", "North Korea": "Asia", "North Macedonia": "Europe",
    "Norway": "Europe", "Oman": "Asia", "Pakistan": "Asia", "Palau": "Oceania", "Palestinian National Authority": "Asia",
    "Panama": "North America", "Papua New Guinea": "Oceania", "Paraguay": "South America", "Peru": "South America",
    "Philippines": "Asia", "Poland": "Europe", "Portugal": "Europe", "Qatar": "Asia", "Romania": "Europe", "Russia": "Europe",
    "Rwanda": "Africa", "Saint Kitts and Nevis": "North America", "Saint Lucia": "North America",
    "Saint Vincent and the Grenadines": "North America", "Samoa": "Oceania", "San Marino": "Europe", "Saudi Arabia": "Asia",
    "Senegal": "Africa", "Serbia": "Europe", "Seychelles": "Africa", "Sierra Leone": "Africa", "Singapore": "Asia",
    "Slovakia": "Europe", "Slovenia": "Europe", "Solomon Islands": "Oceania", "Somalia": "Africa", "South Africa": "Africa",
    "South Korea": "Asia", "South Sudan": "Africa", "Spain": "Europe", "Sri Lanka": "Asia", "Sudan": "Africa", "Suriname": "South America",
    "Sweden": "Europe", "Switzerland": "Europe", "Syria": "Asia", "Tajikistan": "Asia", "Tanzania": "Africa", "Thailand": "Asia",
    "East Timor": "Asia", "Togo": "Africa", "Tonga": "Oceania", "Trinidad and Tobago": "North America", "Tunisia": "Africa",
    "Turkey": "Asia", "Turkmenistan": "Asia", "Tuvalu": "Oceania", "Uganda": "Africa", "Ukraine": "Europe",
    "United Arab Emirates": "Asia", "United Kingdom": "Europe", "United States": "North America", "Uruguay": "South America",
    "Uzbekistan": "Asia", "Vanuatu": "Oceania", "Venezuela": "South America", "Vietnam": "Asia", "Yemen": "Asia",
    "Zambia": "Africa", "Zimbabwe": "Africa"
}

#add the region column based on the dictionary above
df['Region'] = df['Country'].map(country_to_region)

#create a column for GDP per Billion
df['GDP per Billion $'] = df['GDP'] / 1000000000
df = df.drop('GDP', axis=1)

#create a population per Billion
df['PopulationperBillion'] = df['Population'] / 1000000000
df = df.drop('Population', axis=1)

#filter dataframe for the top 10 countries by GDP per Billion $
df_top10 = df.sort_values('GDP per Billion $', ascending=False).head(10)

#list of numeric columns for scatter plot dropdown
numeric_columns = ['Birth Rate', 'CPI', 'Fertility Rate', 'Tertiary education',
                   'Gross tertiary education enrollment (%)', 'Infant mortality',
                   'Life expectancy', 'Maternal mortality ratio', 'Minimum wage',
                   'Out of pocket health expenditure', 'Physicians per thousand',
                   'Primary education']
numeric_columns.sort()
#list of numeric columns for choropleth dropdown
numeric_columns_map = ['Density\n(P/Km2)', 'Agricultural Land( %)', 'Land Area(Km2)',
                       'Armed Forces size', 'Birth Rate', 'Co2-Emissions', 'Fertility Rate', 'Forested Area (%)',
                       'Gross primary education enrollment (%)',
                       'Gross tertiary education enrollment (%)', 'Infant mortality',
                       'Life expectancy', 'Maternal mortality ratio', 'Minimum wage',
                       'Out of pocket health expenditure', 'Physicians per thousand',
                       'Population: Labor force participation (%)',
                       'Total tax rate', 'Unemployment rate',
                       'Urban_population', 'Primary education', 'Tertiary education', 'GDP per Billion $']
numeric_columns_map.sort()

#normalize numeric columns for GDP, infant mortality, and out of pocket expenditure
categories = ['GDP per Billion $', 'Infant mortality', 'Out of pocket health expenditure', 
              'Unemployment rate', 'Life expectancy', 'Primary education']
df_normalized = df[categories]
df_normalized = df_normalized.apply(lambda x: (x - x.min()) / (x.max() - x.min()))

#create a spider chart
fig_spider = go.Figure()
for i, country in enumerate(df['Country']):
    fig_spider.add_trace(go.Scatterpolar(
        r=df_normalized.iloc[i].values,
        theta=categories,
        fill='toself',
        name=country
    ))
fig_spider.update_layout(showlegend=False,
                         polar=dict(
                             radialaxis=dict(
                                 visible=True,
                                 range=[0, 1],
                             )
                         ),
                         title="Comparing Countries Across Multiple Metrics",
                         )

#create a sunburst chart
fig_sunburst = px.sunburst(
    df,
    path=['Region', 'Country'],  # Adjust hierarchy as needed
    values='PopulationperBillion',
    color='PopulationperBillion',
    color_continuous_scale='Purples',
    title='Population by Region and Country',
    labels={'PopulationperBillion': 'PopulationperBillion'}
)

#create a bar chart
purple_hues = ['#6A0DAD', '#9B30FF', '#8A2BE2', '#BA55D3', '#9932CC']
fig_bar = px.bar(
    df_top10,
    x='Country',
    y='GDP per Billion $',
    color='Country',
    color_discrete_sequence=purple_hues,
    text='GDP per Billion $',
    title="Top 10 Countries by GDP per Billion $",
    labels={'GDP per Billion $': 'GDP ($)'}
)
fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')

fig_bar.update_layout(yaxis_title="GDP ($)", xaxis_title="Country", showlegend=False)

#create a scatter plot
fig_infant = px.scatter(
    df,
    x='Out of pocket health expenditure',
    y='GDP per Billion $',
    color='Region',
    color_continuous_scale='Purples',
    size='Infant mortality',
    hover_name='Country',
)

#create a choropleth map
fig_choropleth = px.choropleth(df, locations="Country", 
                               locationmode="country names", color='GDP per Billion $', 
                               hover_name="Country", color_continuous_scale='Purples', 
                               title='GDP per Billion $ by Country')

#initialize the app
app = dash.Dash(__name__)

#create the layout with a dropdown for region
app.layout = html.Div(
    style={
            'maxWidth': '100%',
            'maxHeight': '100vh',
            'overflow': 'auto',
            'margin': '0 auto',
            'display': 'grid',
            'gridTemplateColumns': 'repeat(3, 1fr)',
            'gridTemplateRows': 'repeat(3, 1fr)',
            'gap': '5px',
        },
    children=[
        html.Div(
            children=[
                html.H1(
                    "Proteeti Kushari - 24333831 - Data Visualization, 2024, World Development Data (2023)",
                    style={'textAlign': 'center', 'fontSize': '24px', 'gridColumn': 'span 2'}
                ),
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[{'label': 'All Regions', 'value': 'All'}] + [{'label': region, 'value': region} for region in df['Region'].unique()],
                    value='All',
                    style={'width': '80%', 'margin': '0 auto'}
                ),
            ],
            style={'gridColumn': 'span 3', 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}
        ),
        #display sunburst chart
        html.Div([
            dcc.Graph(id='sunburst-plot', figure=fig_sunburst)
        ], style={'padding': '5px', 'height': '100%'}),
        #display spider chart
        html.Div([
            dcc.Graph(id='fig_spider-plot', figure=fig_spider)
        ], style={'padding': '5px', 'height': '100px'}),
        #display bar chart
        html.Div([
            dcc.Graph(id='bar-plot', figure=fig_bar)
        ], style={'padding': '5px', 'height': '100%'}),
        #display scatter chart
        html.Div([
            dcc.Dropdown(
                id='y-axis-dropdown',
                options=[{'label': col, 'value': col} for col in numeric_columns],
                value=numeric_columns[0],
                style={'width': '100%'}
            ),
            dcc.Graph(id='scatter-plot')
        ], style={'padding': '5px', 'height': '100%'}),
        #display choropleth chart
        html.Div([
            dcc.Dropdown(
                id='y-axis-dropdown2',
                options=[{'label': col, 'value': col} for col in numeric_columns_map],
                value=numeric_columns_map[0],
                style={'width': '100%'}
            ),
            dcc.Graph(id='choropleth-plot')
        ], style={'padding': '5px', 'height': '100%'}),
        #displa
        html.Div([
            dcc.Graph(id='infant-plot', figure=fig_infant)
        ], style={'padding': '5px', 'height': '100%'}),    
])

#define callback to update all plots based on region
@app.callback(
    [Output('sunburst-plot', 'figure'),
     Output('fig_spider-plot', 'figure'),
     Output('bar-plot', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('infant-plot', 'figure'),
     Output('choropleth-plot', 'figure')],
    [Input('region-dropdown', 'value'),
    Input('y-axis-dropdown', 'value'),
    Input('y-axis-dropdown2', 'value')
    ]
)
def update_charts_by_region(selected_region, y_column,y_column2):
    df_chart = pd.DataFrame()
    #filter the dataframe based on the selected region
    if (selected_region != 'All'):
       df_chart = df[df['Region'] == selected_region]
    else:
        df_chart = df
    
    #update the sunburst chart
    fig_sunburst = px.sunburst(
        df_chart,
        path=['Region', 'Country'],
        values='PopulationperBillion',
        color='PopulationperBillion',
        color_continuous_scale='Purples',
        title=f'Population by Region and Country ({selected_region})',
        labels={'PopulationperBillion': 'Population per Billion'}
    )
    
    #update spider chart
    df_normalized_filtered = df_chart[categories]
    df_normalized_filtered = df_normalized_filtered.apply(lambda x: (x - x.min()) / (x.max() - x.min()))  # Normalize data
    fig_spider = go.Figure()
    for i, country in enumerate(df_chart['Country']):
        fig_spider.add_trace(go.Scatterpolar(
            r=df_normalized_filtered.iloc[i].values,
            theta=categories,
            fill='toself',
            name=country
        ))
    fig_spider.update_layout(showlegend=False,
                             polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                             title=f"Comparing Countries Across Multiple Metrics ({selected_region})")

    #update the bar chart
    df_top10_filtered = df_chart.sort_values('GDP per Billion $', ascending=False).head(10)
    fig_bar = px.bar(df_top10_filtered,
                     x='Country',
                     y='GDP per Billion $',
                     color='Country',
                     color_discrete_sequence=purple_hues,
                     text='GDP per Billion $',
                     title=f"Top 10 Countries by GDP ({selected_region})",
                     labels={'GDP per Billion $': 'GDP ($)'})
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_bar.update_layout(yaxis_title="GDP ($)", xaxis_title="Country", showlegend=False)

    df_scatter = df_chart.sort_values('GDP per Billion $', ascending=False)
    #update the scatter chart
    fig_scatter = px.scatter(df_scatter,
                            x='GDP per Billion $',
                            y=y_column,
                            color='Country',
                            color_continuous_scale='Purples',
                            size='PopulationperBillion',
                            hover_name='Country',
                            title=f"({y_column}) vs GDP ($) / billion ({selected_region})",
                            )
    fig_scatter.update_layout(xaxis=dict(type='category', categoryorder='array'),
                             title=f"({y_column}) vs GDP per Billion $ ({selected_region})")

    #update the choropleth map
    fig_choropleth = px.choropleth(
                    df_chart, 
                    locations="Country",
                    locationmode="country names",
                    color=y_column2,
                    hover_name="Country",
                    color_continuous_scale='Purples', 
                    title=f'({y_column2}) in ({selected_region})')
    
    fig_choropleth.update_geos(showframe=False)
    
    #update the infant mortality chart
    fig_infant = px.scatter(
    df_chart,
    x='Out of pocket health expenditure',
    y='GDP per Billion $',
    color='Region',
    color_continuous_scale='Purples',
    size='Infant mortality',
    hover_name='Country',
    title="Child Mortality Rate vs Out-of-Pocket Healthcare Spending"
    )

    # Return the updated charts
    return fig_sunburst, fig_spider, fig_bar, fig_scatter, fig_infant, fig_choropleth

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
