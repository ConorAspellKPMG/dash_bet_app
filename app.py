import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import dash_daq as daq
import dash_table
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# make a sample data frame with 6 columns
df = pd.read_csv('data/bets2.csv')
df2 =pd.read_csv('data/rec_bets2.csv')


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ])
            
            for i in range(min(len(dataframe), len(dataframe)))
        ])
    ])

def generate_checkboxes(df):
    pass


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
                            daq.ToggleSwitch(
                          id='pop-switch',
                          size=40,
                          label='Show all data',
                          labelPosition='top'
                          ),
    html.H4(children='Arbitrage Bets'),
    html.H3(children='Edit the "Stake" Column to see exact bets and returns'),
    html.Div([
        html.P("Football Odds",
                              style={'margin-top':'1rem',
                                     'margin-right':'0rem',
                                     'margin-bottom':'1rem'}
                              ),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
                      ], style={'display': 'none'},
                              id='data-table-container'
                              ),
    # html.Div(children=[
    # html.H4(children='Recommended Bets'),
    # dcc.Dropdown(id='dropdown', options=[
    #     {'label': i, 'value': i} for i in df2.home_team.unique()
    # ], multi=True, placeholder='Filter by game...'),
    # html.Div(id='table-container')
    # ]),

    html.Div([
        dash_table.DataTable(
        id='bet-table',
        columns=[{"name": i, "id": i} for i in df2.columns if i not in ['league','away_amount','home_amount','draw_amount','home_profit',
       'away_profit', 'draw_profit']],
        data=df2.to_dict('records'),
        editable=True,
    )])

    
])

@app.callback(
    Output('bet-table', 'data'),
    Input('bet-table', 'data'),
    Input('bet-table', 'columns'))
def display_output(rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    common_cols = ['away_team_odds', 'draw_odds', 'home_team_odds',
       'away_site', 'away_team', 'draw_site',
       'home_site', 'home_team'
       ]
    if not df[common_cols].equals(df2[common_cols]):
        df[common_cols] = df2[common_cols]
        return df.to_dict(orient="records")
    df.stake= df.stake.astype('float64')
    df.home_bet= df.home_bet.astype('float64')
    df.away_bet= df.away_bet.astype('float64')
    df.draw_bet= df.draw_bet.astype('float64')
    df['home_bet'] = round(df['stake'] * df2['home_amount'],2)
    df['away_bet'] = round(df['stake'] * df2['away_amount'],2)
    df['draw_bet'] = round(df['stake'] * df2['draw_amount'],2)
    df['home_return'] = round(df['stake'] * df2['home_profit'],2)
    df['away_return'] = round(df['stake'] * df2['away_profit'],2)
    df['draw_return'] = round(df['stake'] * df2['draw_profit'],2)
    return df.to_dict(orient="records")

@app.callback(Output(component_id='data-table-container', component_property='style'),
              [
               Input(component_id='pop-switch',component_property='value')
                ])
def generate_table_data_container(showRegions):

    if showRegions:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# @app.callback(
#     dash.dependencies.Output('table-container', 'children'),
#     [dash.dependencies.Input('dropdown', 'value')])
# def display_table(dropdown_value):
#     if dropdown_value is None:
#         return generate_table(df2)

#     dff = df2[df2.home_team.str.contains('|'.join(dropdown_value))]
#     return generate_table(dff)

if __name__ == '__main__':
    app.run_server(debug=True)