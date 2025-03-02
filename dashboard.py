import dash
from dash import dcc, html
import dash_table
import pandas as pd
import requests
from dash.dependencies import Input, Output, State

class VenmitoDashboard:
    def __init__(self):
        # Initialize the Dash app
        self.app = dash.Dash(__name__, suppress_callback_exceptions=True)
        self.setup_layout()

    def setup_layout(self):
        # Define the layout of the app
        self.app.layout = html.Div(children=[
            dcc.Location(id='url', refresh=False),  # Track the URL

            html.H1(children='Venmito Dashboard', style={'textAlign': 'center', 'marginBottom': '20px'}),

            # Navigation Links
            dcc.Link('Go to Client Promotions', href='/promotions', className='button', style={'display': 'block', 'margin': '10px 0'}),

            # Content will be rendered in this container
            html.Div(id='page-content'),

            # Search forms
            html.Div([
                self.create_search_form('clients', ['id', 'first_name', 'last_name', 'telephone', 'email', 'android', 'desktop', 'iphone', 'city', 'country']),
                self.create_search_form('promotions', ['id', 'client_email', 'telephone', 'promotion', 'responded']),
                self.create_search_form('transactions', ['id', 'phone', 'store']),
                self.create_search_form('transfers', ['id', 'sender_id', 'recipient_id', 'amount', 'date']),
                self.create_search_form('items', ['id', 'transaction_id', 'item_name', 'price', 'price_per_item', 'quantity']),
                self.create_search_form('promotions/person', ['id', 'first_name', 'last_name', 'telephone', 'email', 'city', 'country'])
            ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

            # Best and Worst Seller Section
            html.Div([
                dcc.Interval(id='interval-best-worst-seller', interval=1*1000, n_intervals=0),
                html.Div(id='best-worst-seller-results', style={'marginTop': '20px'})
            ]),

            # Store-related Section
            html.Div([
                dcc.Interval(id='interval-store-results', interval=1*1000, n_intervals=0),
                html.Div(id='store-results', style={'marginTop': '20px'})
            ])
        ])

        # Define the layout for the promotions page
        self.promotions_layout = html.Div(children=[
            html.H2(children='Client Promotions'),

            dash_table.DataTable(
                id='client-promotions-table',
                columns=[{"name": i, "id": i} for i in self.fetch_promotions_data().columns],
                data=self.fetch_promotions_data().to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
        ])

        # Set up the callback for page navigation
        self.setup_callbacks()

    def create_search_form(self, entity, fields):
        return html.Div([
            html.H3(f'Search {entity.capitalize()}', style={'marginBottom': '10px'}),
            *[dcc.Input(id=f'{entity}-{field}', type='text', placeholder=f'Enter {field}', style={'margin': '5px', 'width': '200px'}) for field in fields],
            html.Button(f'Search {entity.capitalize()}', id=f'search-{entity}-button', style={'margin': '10px', 'padding': '5px 10px'}),
            html.Div(id=f'{entity}-search-results', style={'marginTop': '10px'})
        ], style={'border': '1px solid #ccc', 'padding': '20px', 'margin': '10px', 'borderRadius': '5px', 'width': '80%', 'maxWidth': '600px'})

    def setup_callbacks(self):
        @self.app.callback(
            Output('page-content', 'children'),
            [Input('url', 'pathname')]
        )
        def display_page(pathname):
            print(f"Current pathname: {pathname}")  # Debugging statement
            if pathname == '/promotions':
                return self.promotions_layout
            else:
                return html.Div(children='Welcome to the Venmito Dashboard!')

        # Callback for each search form
        for entity in ['clients', 'promotions', 'transactions', 'transfers', 'items', 'promotions/person']:
            self.app.callback(
                Output(f'{entity}-search-results', 'children'),
                [Input(f'search-{entity}-button', 'n_clicks')],
                [State(f'{entity}-{field}', 'value') for field in self.get_fields(entity)]
            )(self.create_search_callback(entity))

        # Callback for Best and Worst Seller
        @self.app.callback(
            Output('best-worst-seller-results', 'children'),
            [Input('interval-best-worst-seller', 'n_intervals')]
        )
        def update_best_worst_seller(n_intervals):
            return self.fetch_and_display_data('items/best_worst_seller')

        # Callbacks for Store-related Results
        @self.app.callback(
            Output('store-results', 'children'),
            [Input('interval-store-results', 'n_intervals')]
        )
        def update_store_results(n_intervals):
            # Fetch and display data for all store-related endpoints
            profit_data = self.fetch_and_display_data('stores/profit')
            profit_list_data = self.fetch_and_display_data('stores/profit/list')
            quantity_data = self.fetch_and_display_data('stores/quantity')
            quantity_max_min_data = self.fetch_and_display_data('stores/quantity/max_min')

            # Combine all results into a single display
            return html.Div([
                html.H3("Store Profit"),
                profit_data,
                html.H3("Store Profit List"),
                profit_list_data,
                html.H3("Store Quantity"),
                quantity_data,
                html.H3("Store Quantity Max/Min"),
                quantity_max_min_data
            ])

    def fetch_and_display_data(self, endpoint):
        try:
            response = requests.get(f'http://localhost:5000/{endpoint}')
            response.raise_for_status()
            data = response.json()
            print(f"Data from {endpoint}: {data}")  # Debugging statement

            # Display the data
            display_content = []

            if endpoint == 'items/best_worst_seller':
                # Comparative bar graph for Best Seller vs Worst Seller
                display_content.append(html.H3("Best Seller vs Worst Seller"))
                display_content.append(dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': ['Best Seller', 'Worst Seller'],
                                'y': [data['best_seller']['total_quantity'], data['worst_seller']['total_quantity']],
                                'type': 'bar',
                                'name': 'Total Quantity'
                            }
                        ],
                        'layout': {
                            'title': 'Best Seller vs Worst Seller',
                            'xaxis': {'title': 'Item'},
                            'yaxis': {'title': 'Total Quantity'},
                            'annotations': [
                                {'x': 'Best Seller', 'y': data['best_seller']['total_quantity'], 'text': data['best_seller']['item_name'], 'showarrow': True},
                                {'x': 'Worst Seller', 'y': data['worst_seller']['total_quantity'], 'text': data['worst_seller']['item_name'], 'showarrow': True}
                            ]
                        }
                    }
                ))

            elif endpoint == 'stores/profit':
                # Comparative bar graph for Most Profit vs Least Profit
                display_content.append(html.H3("Most Profit vs Least Profit"))
                display_content.append(dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': ['Most Profit', 'Least Profit'],
                                'y': [data['most_profit']['total_profit'], data['least_profit']['total_profit']],
                                'type': 'bar',
                                'name': 'Total Profit'
                            }
                        ],
                        'layout': {
                            'title': 'Most Profit vs Least Profit',
                            'xaxis': {'title': 'Store'},
                            'yaxis': {'title': 'Total Profit'},
                            'annotations': [
                                {'x': 'Most Profit', 'y': data['most_profit']['total_profit'], 'text': data['most_profit']['store'], 'showarrow': True},
                                {'x': 'Least Profit', 'y': data['least_profit']['total_profit'], 'text': data['least_profit']['store'], 'showarrow': True}
                            ]
                        }
                    }
                ))

            elif endpoint == 'stores/profit/list':
                # Handle store profit list as a bar graph
                display_content.append(html.H3("Store Profit List"))
                display_content.append(dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': [item['store'] for item in data],
                                'y': [item['total_profit'] for item in data],
                                'type': 'bar',
                                'name': 'Total Profit'
                            }
                        ],
                        'layout': {
                            'title': 'Store Profit List',
                            'xaxis': {'title': 'Store'},
                            'yaxis': {'title': 'Total Profit'}
                        }
                    }
                ))

            elif endpoint == 'stores/quantity':
                # Handle store quantity as a bar graph
                display_content.append(html.H3("Store Quantity"))
                display_content.append(dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': [item['store'] for item in data],
                                'y': [item['total_quantity'] for item in data],
                                'type': 'bar',
                                'name': 'Total Quantity'
                            }
                        ],
                        'layout': {
                            'title': 'Store Quantity',
                            'xaxis': {'title': 'Store'},
                            'yaxis': {'title': 'Total Quantity'}
                        }
                    }
                ))

            elif endpoint == 'stores/quantity/max_min':
                # Comparative bar graph for Max Quantity vs Min Quantity
                display_content.append(html.H3("Max Quantity vs Min Quantity"))
                display_content.append(dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': ['Max Quantity', 'Min Quantity'],
                                'y': [data['max_quantity']['total_quantity'], data['min_quantity']['total_quantity']],
                                'type': 'bar',
                                'name': 'Total Quantity'
                            }
                        ],
                        'layout': {
                            'title': 'Max Quantity vs Min Quantity',
                            'xaxis': {'title': 'Store'},
                            'yaxis': {'title': 'Total Quantity'},
                            'annotations': [
                                {'x': 'Max Quantity', 'y': data['max_quantity']['total_quantity'], 'text': data['max_quantity']['store'], 'showarrow': True},
                                {'x': 'Min Quantity', 'y': data['min_quantity']['total_quantity'], 'text': data['min_quantity']['store'], 'showarrow': True}
                            ]
                        }
                    }
                ))

            return html.Div(display_content)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")  # Debugging statement
            return html.Div(children=f"Error fetching data: {e}")

    def create_search_callback(self, entity):
        def search_callback(n_clicks, *args):
            if n_clicks:
                query_params = {field: value for field, value in zip(self.get_fields(entity), args) if value}
                query_string = '&'.join([f'{key}={value}' for key, value in query_params.items()])
                print(f"Querying {entity} with: {query_string}")  # Debugging statement

                try:
                    # Adjust the URL path for the promotions/person endpoint
                    if entity == 'promotions/person':
                        endpoint = 'promotions/search/person'
                    else:
                        endpoint = f'{entity}/search'

                    response = requests.get(f'http://localhost:5000/{endpoint}?{query_string}')
                    response.raise_for_status()  # Raise an error for bad responses
                    data = response.json()
                    print(f"Response data: {data}")  # Debugging statement

                    # Process and display the response data
                    display_content = []
                    for key, value in data.items():
                        display_content.append(html.H4(f"{key.replace('_', ' ').title()}:"))
                        if isinstance(value, list):
                            for item in value:
                                display_content.append(html.Div([html.P(f"{k}: {v}") for k, v in item.items()]))
                        else:
                            display_content.append(html.P(str(value)))

                    return html.Div(display_content)
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching data: {e}")  # Debugging statement
                    return html.Div(children=f"Error fetching data: {e}")
            return html.Div()
        return search_callback

    def get_fields(self, entity):
        fields = {
            'clients': ['id', 'first_name', 'last_name', 'telephone', 'email', 'android', 'desktop', 'iphone', 'city', 'country'],
            'promotions': ['id', 'client_email', 'telephone', 'promotion', 'responded'],
            'transactions': ['id', 'phone', 'store'],
            'transfers': ['id', 'sender_id', 'recipient_id', 'amount', 'date'],
            'items': ['id', 'transaction_id', 'item_name', 'price', 'price_per_item', 'quantity'],
            'promotions/person': ['id', 'first_name', 'last_name', 'telephone', 'email', 'city', 'country']
        }
        return fields[entity]

    def fetch_promotions_data(self):
        # Fetch data from the API
        response = requests.get('http://localhost:5000/clients/promotions')
        data = response.json()

        # Convert the data into a DataFrame
        df = pd.DataFrame(data)
        return df

    def run(self):
        # Run the app without SSL
        self.app.run_server(debug=True)

if __name__ == '__main__':
    dashboard = VenmitoDashboard()
    dashboard.run()