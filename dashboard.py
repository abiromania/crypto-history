import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px


# Reading CSV file into a DataFrame
df = pd.read_csv('crypto_history.csv')

df_mean = df.groupby('ticker')['close'].mean().reset_index()

# Creating a Dash application
app = Dash(__name__)


# Creating dashboard layout
app.layout = html.Div(children=[
    html.H1(children='Crypto Historical Data Dashboard'),
    dcc.Checklist(
        id='crypto-selector',
        options=[{'label': crypto, 'value': crypto} for crypto in df['ticker'].unique()],
        value=[df['ticker'].unique()[2]],  # Default selection
        className='checklist'
    ),
    dcc.Graph(id='line-chart', figure={}),
    dcc.Graph(id='pie-chart', figure={}),
    
])

@app.callback(
    Output('line-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('crypto-selector', 'value'))

def update_chart(selected_cryptos):
    # Crypto Filter for charts
    filtered_df = df[df['ticker'].isin(selected_cryptos)]


    # Creating line chart
    fig_bar = px.line(filtered_df, 
                      x='date', 
                      y='close', 
                      color='ticker', 
                      title='Crypto Prices Over Time')
    
    fig_bar.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color='white',
        title_font_color='white',
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


    # Creating pie chart
    fig_pie = px.pie(df_mean[df_mean['ticker'].isin(selected_cryptos)], 
                     names='ticker', 
                     values='close', 
                     title='Average Closing Prices Distribution')
    
    fig_pie.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font_color='white',
        title_font_color='white',
        legend_font_color='white',
    )



    return fig_bar, fig_pie

if __name__ == '__main__':
    app.run(debug=True)
