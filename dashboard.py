import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go


# Reading CSV file into a DataFrame
df = pd.read_csv('crypto_history.csv')

# Creating a Dash application
app = Dash(__name__)


# Creating dashboard layout
app.layout = html.Div(children=[
    html.H1(children='Crypto Historical Data Dashboard'),
   
    # Crypto filter, pie and line charts
    dcc.Checklist(
        id='crypto-selector',
        options=[{'label': crypto, 'value': crypto} for crypto in df['ticker'].unique()],
        value=[df['ticker'].unique()[2]],  # Default selection
        className='checklist'
    ),

    html.Div(children=[
        dcc.Graph(id='line-chart', figure={}, className='graph'),
        dcc.Graph(id='pie-chart', figure={}, className='graph'),
    ], className='dashboard-container'),
    

    # Candlestick filter and chart
    html.Div(children=[
        dcc.RadioItems(
            [{'label': crypto, 'value': crypto} for crypto in df['ticker'].unique()],
            df['ticker'].unique()[2],
            id='candlestick-selector',
            className='radio-items'
        ),
        dcc.Graph(id='candlestick-chart', figure={}, className='graph')
    ], className='dashboard-container')
])



# Updates candlestick chart
@app.callback(
    Output('candlestick-chart', 'figure'),
    Input('candlestick-selector', 'value')
)
def update_line_chart(candlestick_value):

    candle_df = df[df['ticker'] == candlestick_value].copy()

    fig_candlestick = go.Figure(data=[go.Candlestick(
        x=candle_df['date'],
        open=candle_df['open'],
        high=candle_df['high'],
        low=candle_df['low'],
        close=candle_df['close'],
    )])

    fig_candlestick.update_layout(
        title=f'{candlestick_value} Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color='white',
        title_font_color='white',
        title_x=0.5,
        legend_font_color='white',
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            zerolinecolor='white',
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.2)',
            zerolinecolor='white',
        )
    )

    return fig_candlestick
    


# Updates line and pie charts
@app.callback(
    Output('line-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('crypto-selector', 'value')
)

def update_charts(selected_cryptos):
    filtered_df = df[df['ticker'].isin(selected_cryptos)].copy()
    filtered_df['mean'] = (filtered_df['high'] + filtered_df['low']) / 2

    # Create line chart
    fig_line = px.line(filtered_df,
                       x='date',
                       y='mean',
                       color='ticker',
                       title='Average Crypto Prices Over Time')

    fig_line.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color='white',
        title_font_color='white',
        title_x=0.5,
        legend_font_color='white',
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            zerolinecolor='white',
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.2)',
            zerolinecolor='white',
        )
    )

    # Create pie chart
    fig_pie = px.pie(filtered_df, 
                     values='mean',
                     names='ticker',
                     title='Average Prices Distribution')

    fig_pie.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color='white',
        title_font_color='white',
        title_x=0.5,
        legend_font_color='white',
    )


    return fig_line, fig_pie



if __name__ == '__main__':
    app.run(debug=True)
