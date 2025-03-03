import dash
from dash import dcc, html
import dash_table
import requests
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Venmito Dashboard"), className="text-center my-4")),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),  # Trigger once on page load
    dbc.Row([
        dbc.Col(dcc.Graph(id="promotions-output"), width=4),
        dbc.Col(dcc.Graph(id="items-summary-graph"), width=4),
        dbc.Col(dcc.Graph(id="promotions-max-min-graph"), width=4),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="city-max-min-graph"), width=4),
        dbc.Col(dcc.Graph(id="device-max-min-graph"), width=4),
        dbc.Col(dcc.Graph(id="store-profit-graph"), width=4),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="store-profit-list-graph"), width=4),
        dbc.Col(dcc.Graph(id="store-quantity-max-min-graph"), width=4),
        dbc.Col(dcc.Graph(id="total-transfers-graph"), width=4),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="transfers-max-min-graph"), width=4),
        dbc.Col(dcc.Graph(id="device-transfers-total-graph"), width=4),
    ], className="mb-4"),
], fluid=True)

# Define the callback to update the promotions data
@app.callback(
    Output("promotions-output", "figure"),
    [Input("interval-component", "n_intervals")]
)
def display_promotions(n_intervals):
    try:
        # Fetch data from the API
        response = requests.get('http://localhost:5000/clients/promotions')
        if response.status_code == 200:
            promotions = response.json()
            # Create a bar graph using Plotly Express
            fig = px.bar(promotions, x='email', y='promotion', title='Promotions')
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# Define the callback to update the items summary graph
@app.callback(
    Output("items-summary-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def display_items_summary(n_intervals):
    try:
        # Fetch data from the API
        response = requests.get('http://localhost:5000/items/summary')
        if response.status_code == 200:
            items_summary = response.json()
            # Create a DataFrame from the JSON data
            df = pd.DataFrame(items_summary)
            # Create a bar graph using Plotly Express
            fig = px.bar(df, x='item_name', y='total_quantity', title='Item Summary')
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# Define the callback to update the promotions max/min graph
@app.callback(
    Output("promotions-max-min-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def display_promotions_max_min(n_intervals):
    try:
        # Fetch data from the API
        response = requests.get('http://localhost:5000/promotions/responded/max_min')
        if response.status_code == 200:
            data = response.json()
            # Prepare data for the bar graph
            df = pd.DataFrame([
                {'Type': 'Max Responded', 'Promotion': data['max_responded']['promotion'], 'Count': data['max_responded']['response_count']},
                {'Type': 'Min Responded', 'Promotion': data['min_responded']['promotion'], 'Count': data['min_responded']['response_count']}
            ])
            # Create a bar graph using Plotly Express
            fig = px.bar(df, x='Promotion', y='Count', color='Type', title='Promotions Max/Min Responded')
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# Define the callback to update the city max/min graph
@app.callback(
    Output("city-max-min-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def display_city_max_min(n_intervals):
    try:
        # Fetch data from the API
        response = requests.get('http://localhost:5000/promotions/responded/city/max_min')
        if response.status_code == 200:
            data = response.json()
            # Prepare data for the bar graph
            df = pd.DataFrame([
                {'Type': 'Max Responded City', 'City': data['max_responded_city']['city'], 'Count': data['max_responded_city']['response_count']},
                {'Type': 'Min Responded City', 'City': data['min_responded_city']['city'], 'Count': data['min_responded_city']['response_count']}
            ])
            # Create a bar graph using Plotly Express
            fig = px.bar(df, x='City', y='Count', color='Type', title='City Max/Min Responded')
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# Define the callback to update the device max/min graph
@app.callback(
    Output("device-max-min-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def display_device_max_min(n_intervals):
    try:
        # Fetch data from the API
        response = requests.get('http://localhost:5000/promotions/responded/device/max_min')
        if response.status_code == 200:
            data = response.json()
            # Prepare data for the bar graph
            df = pd.DataFrame([
                {'Type': 'Max Responded Device', 'Device': data['max_responded_device']['device'], 'Count': data['max_responded_device']['response_count']},
                {'Type': 'Min Responded Device', 'Device': data['min_responded_device']['device'], 'Count': data['min_responded_device']['response_count']}
            ])
            # Create a bar graph using Plotly Express
            fig = px.bar(df, x='Device', y='Count', color='Type', title='Device Max/Min Responded')
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# Define the callback to update the store profit graph
@app.callback(
    Output("store-profit-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def display_store_profit(n_intervals):
    try:
        # Fetch data from the API
        response = requests.get('http://localhost:5000/stores/profit')
        if response.status_code == 200:
            data = response.json()
            # Prepare data for the bar graph
            df = pd.DataFrame([
                {'Type': 'Most Profit', 'Store': data['most_profit']['store'], 'Profit': data['most_profit']['total_profit']},
                {'Type': 'Least Profit', 'Store': data['least_profit']['store'], 'Profit': data['least_profit']['total_profit']}
            ])
            # Create a bar graph using Plotly Express
            fig = px.bar(df, x='Store', y='Profit', color='Type', title='Store Profit Max/Min')
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# Define the callback to update the store profit list graph
@app.callback(
    Output("store-profit-list-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def display_store_profit_list(n_intervals):
    try:
        # Fetch data from the API
        response = requests.get('http://localhost:5000/stores/profit/list')
        if response.status_code == 200:
            data = response.json()
            # Create a DataFrame from the JSON data
            df = pd.DataFrame(data)
            # Create a bar graph using Plotly Express
            fig = px.bar(df, x='store', y='total_profit', title='Store Profit List')
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# Define the callback to update the store quantity max/min graph
@app.callback(
    Output("store-quantity-max-min-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def display_store_quantity_max_min(n_intervals):
    try:
        # Fetch data from the API
        response = requests.get('http://localhost:5000/stores/quantity/max_min')
        if response.status_code == 200:
            data = response.json()
            # Prepare data for the bar graph
            df = pd.DataFrame([
                {'Type': 'Max Quantity', 'Store': data['max_quantity']['store'], 'Quantity': data['max_quantity']['total_quantity']},
                {'Type': 'Min Quantity', 'Store': data['min_quantity']['store'], 'Quantity': data['min_quantity']['total_quantity']}
            ])
            # Create a bar graph using Plotly Express
            fig = px.bar(df, x='Store', y='Quantity', color='Type', title='Store Quantity Max/Min')
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# Define the callback to update the total transfers graph
@app.callback(
    Output("total-transfers-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def display_total_transfers(n_intervals):
    try:
        # Fetch data from the API
        response = requests.get('http://localhost:5000/transfers/total')
        if response.status_code == 200:
            total_transfers = response.json()['total_transfers']
            # Prepare data for the bar graph
            df = pd.DataFrame([{'Type': 'Total Transfers', 'Amount': total_transfers}])
            # Create a bar graph using Plotly Express
            fig = px.bar(df, x='Type', y='Amount', title='Total Transfers')
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# Define the callback to update the transfers max/min graph
@app.callback(
    Output("transfers-max-min-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def display_transfers_max_min(n_intervals):
    try:
        # Fetch data from the API
        response = requests.get('http://localhost:5000/transfers/max_min')
        if response.status_code == 200:
            data = response.json()
            # Prepare data for the bar graph
            df = pd.DataFrame([
                {'Type': 'Max Transferred', 'Person': data['max_transferred']['person'], 'Amount': data['max_transferred']['total_transferred']},
                {'Type': 'Min Transferred', 'Person': data['min_transferred']['person'], 'Amount': data['min_transferred']['total_transferred']}
            ])
            # Create a bar graph using Plotly Express
            fig = px.bar(df, x='Person', y='Amount', color='Type', title='Transfers Max/Min')
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# Define the callback to update the device transfers total graph
@app.callback(
    Output("device-transfers-total-graph", "figure"),
    [Input("interval-component", "n_intervals")]
)
def display_device_transfers_total(n_intervals):
    try:
        # Fetch data from the API
        response = requests.get('http://localhost:5000/transfers/device/total')
        if response.status_code == 200:
            data = response.json()
            # Prepare data for the bar graph
            df = pd.DataFrame([
                {'Device': 'Android', 'Total Transferred': data['android']},
                {'Device': 'Desktop', 'Total Transferred': data['desktop']},
                {'Device': 'iPhone', 'Total Transferred': data['iphone']}
            ])
            # Create a bar graph using Plotly Express
            fig = px.bar(df, x='Device', y='Total Transferred', title='Device Transfers Total')
            return fig
        else:
            return {}
    except Exception as e:
        return {}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
