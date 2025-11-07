import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px


# Reading CSV file into a DataFrame
df = pd.read_csv('crypto_history.csv')


# Creating a Dash application
app = Dash(__name__)


# Creating dashboard layout
app.layout = html.Div(children=[
    html.H1(children='Crypto Historical Data Dashboard'),
    dcc.Checklist(
        id='crypto-selector',
        options=[{'label': crypto, 'value': crypto} for crypto in df['ticker'].unique()],
        value=[df['ticker'].unique()[0]],  # Default selection
    ),
    dcc.Graph(id='price-chart'),
    
])

@app.callback(
    Output('price-chart', 'figure'),
    Input('crypto-selector', 'value'))

def update_chart(selected_cryptos):
    filtered_df = df[df['ticker'].isin(selected_cryptos)]
    fig_bar = px.line(filtered_df, x='date', y='close', color='ticker', title='Crypto Prices Over Time')
    return fig_bar

if __name__ == '__main__':
    app.run(debug=True)
