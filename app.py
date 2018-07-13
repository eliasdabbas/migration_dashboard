import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from dash.dependencies import Input, Output
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s==%(funcName)s==%(message)s')

migration_df = pd.read_csv('data/country_data_master.csv',
                           usecols=lambda cols: cols in
                           ['country', 'lat', 'lon', 'migration'])
migration_df = migration_df[migration_df['migration'].notna()]

app = dash.Dash()
server = app.server

app.layout = html.Div([
    dcc.Graph(id='migration_scatter',
              config={'displayModeBar': False}),
    html.Div([
        dcc.Dropdown(id='country_dropdown',
                     value=tuple(),
                     multi=True,
                     options=[{'label': country, 'value': country}
                              for country in
                              migration_df[migration_df['migration'].notna()]['country']])
    ], style={'width': '50%', 'margin-left': '25%'}),
    dcc.Graph(id='migration_fig',
              config={'displayModeBar': False},
              figure={'data': [go.Scattergeo(lon=migration_df['lon'],
                                             lat=migration_df['lat'],
                                             mode='markers',
                                             hoverinfo='text',
                                             text=migration_df['country'].astype(str)
                                                  + '<br>' + 'Net migration: '
                                                  + migration_df['migration'].astype(str),
                                             marker={'size': 22,
                                                     'color': migration_df['migration'],
                                                     'line': {'color': '#000000', 'width': 0.2},
                                                     'colorscale': [[0, 'rgba(214, 39, 40, 0.85)'],
                                                                    [0.618, 'rgba(255, 255, 255, 0.85)'],
                                                                    [1, 'rgba(6,54,21, 0.85)']],
                                                     'colorbar': {'outlinewidth': 0},
                                                     'showscale': True,
                                                     },
                                             )],

                      'layout': go.Layout(title='Net Migration Rate per 1,000 Inhabitants - 2017 (CIA World Factbook)',
                                          font={'family': 'Palatino'},
                                          paper_bgcolor='#eeeeee',
                                          width=1420,
                                          height=750,
                                          geo={'showland': True, 'landcolor': '#eeeeee',
                                               'countrycolor': '#cccccc',
                                               'showcountries': True,
                                               'oceancolor': '#eeeeee',
                                               'showocean': True,
                                               'showcoastlines': True,
                                               'showframe': False,
                                               'coastlinecolor': '#cccccc',
                                               })
                      }),
    html.A('@eliasdabbas', href='https://www.twitter.com/eliasdabbas'),
    html.P(),
    html.Content('Data: CIA World Factobook  '),
    html.A('Net Migration Rate', href='https://www.cia.gov/library/publications/the-world-factbook/fields/2112.html'),
    html.Br(),
    html.Content('  Code: '),
    html.A('github.com/eliasdabbas/migration_dashboard', href='https://github.com/eliasdabbas/migration_dashboard'), html.Br(), html.Br(),
    html.Content('This entry includes the figure for the difference between the number of persons entering and leaving a '
                 'country during the year per 1,000 persons (based on midyear population). An excess of persons entering '
                 'the country is referred to as net immigration (e.g., 3.56 migrants/1,000 population); an excess of persons '
                 'leaving the country as net emigration (e.g., -9.26 migrants/1,000 population). The net migration rate '
                 'indicates the contribution of migration to the overall level of population change. The net migration rate '
                 'does not distinguish between economic migrants, refugees, and other types of migrants nor does it distinguish '
                 'between lawful migrants and undocumented migrants.')
], style={'background-color': '#eeeeee'})


@app.callback(Output('migration_scatter', 'figure'),
              [Input('country_dropdown', 'value')])
def update_migration_scatter(countries):
    logging.info(msg=locals())
    df = migration_df[migration_df['country'].isin(countries)]

    return {
        'data': [go.Scatter(x=migration_df.sort_values(['migration'])['country'],
                            y=migration_df.sort_values(['migration'])['migration'],
                            mode='markers',
                            name='',
                            showlegend=False,
                            hoverlabel={'font': {'size': 20}},
                            marker={'color': '#bbbbbb'})] +
                [go.Scatter(x=df[df['country'] == c]['country'],
                            y=df[df['country'] == c]['migration'],
                            mode='markers',
                            marker={'size': 15},
                            hoverinfo='text',
                            text=df[df['country'] == c]['country'].astype(str)
                                 + ': ' + df[df['country'] == c]['migration'].astype(str),
                            hoverlabel={'font': {'size': 20}},
                            name=c)
                 for c in sorted(countries)],
        'layout': go.Layout(title='Net Migration Rate per 1,000 Inhabitants - 2017 (CIA World Factbook)',
                            xaxis={'showticklabels': False, 'zeroline': False, 'title': 'Country'},
                            yaxis={'title': 'Net Migrants per 1,000'},
                            font={'family': 'Palatino'},
                            titlefont={'size': 30},
                            hovermode='x',
                            paper_bgcolor='#eeeeee',
                            plot_bgcolor='#eeeeee')
    }


if __name__ == '__main__':
    app.run_server()
