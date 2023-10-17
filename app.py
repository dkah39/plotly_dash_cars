import pandas as pd
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


# Read the JSON file into a DataFrame

allcars_raw = pd.read_json('./data/engines_data.json')

# Flatten the nested column
all_cars = pd.json_normalize(allcars_raw['make_model_trim'])
all_cars.columns = [f"make_model_trim_{col}" for col in all_cars.columns]
all_cars = pd.concat([allcars_raw.reset_index(drop=True), all_cars.reset_index(drop=True)], axis=1)

# Make pretty
all_cars = all_cars.rename(columns={
    "make_model_trim_make_model.make.name": "make",
    "make_model_trim_make_model.name": "model",
    "make_model_trim_invoice": "invoice",
    "make_model_trim_msrp": "msrp",
    "make_model_trim_description": "description",
    "make_model_trim_year": "year",
    "make_model_trim_name": "trim"
})

all_cars = all_cars.drop(columns=[
    'make_model_trim_id',
    'make_model_trim_make_model_id',
    'make_model_trim_make_model.make_id',
    'make_model_trim_make_model.id',
    'make_model_trim_make_model.make.id',
    'make_model_trim_created',
    'make_model_trim_modified',
    'make_model_trim'
])
all_cars['engine_type'] = all_cars['engine_type'].str.title()
all_cars['fuel_type'] = all_cars['fuel_type'].str.title()

# Create a new column for cost($100):power ratios for later analysis
all_cars['horsepower_per_100_dollars'] = (all_cars['horsepower_hp'] / all_cars['msrp']) * 100


##--- Start the  plotly dash app ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

#Datasets, lists and artifacts
engine_type_checklist = all_cars['engine_type'].unique()
make_name_checklist = all_cars['make'].unique()
fuel_type_checklist = all_cars['fuel_type'].unique()
# Existing code for qcut
all_cars['msrp_qcut'] = pd.qcut(all_cars['msrp'], q=5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])

# Existing code for creating the string labels
quantile_ranges = all_cars.groupby('msrp_qcut')['msrp'].agg(['min', 'max']).reset_index()
quantile_labels = [f"${row['min']:,.0f} to ${row['max']:,.0f}" for index, row in quantile_ranges.iterrows()]
# Create a dictionary to map 'msrp_qcut' labels to string labels
quantile_dict = {qcut: label for qcut, label in zip(['Q1', 'Q2', 'Q3', 'Q4', 'Q5'], quantile_labels)}
# Create a new column that maps the 'msrp_qcut' labels to string labels
all_cars['msrp_label'] = all_cars['msrp_qcut'].map(quantile_dict)


# Layout
app.layout = dbc.Container([
    # Banner Row 
    dbc.Row(
        [
            dbc.Col(
                html.Img(src='https://github.com/car-api-team/docs/blob/main/carapi.png?raw=true', style={'height': '40px', 'position': 'relative'}),
                width=1,
                style={'padding-top': '1rem', 'padding-bottom': '1rem', 'padding-left': '1rem', 'padding-right': '0rem'}
            ),
            dbc.Col(
                html.H5("2020 Vehicles"),
                width={"size": 2, "offset": 9},
                style={'text-align': 'right', 'size':20, 'padding-top': '1rem', 'padding-bottom': '1rem',
                       'padding-left': '0rem', 'padding-right': '1rem'}
            )
        ],
        justify='around'
    ),
    # First Data Row
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                id='engine_type_dropdown',
                                value=[],  # Default empty
                                options=engine_type_checklist,
                                multi=True
                            ),
                            width={'size': 3, 'offset': 0, 'order': 2}
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='price_range_dropdown',
                                value=[],  # Default empty
                                options=[{'label': label, 'value': label} for label in quantile_labels],
                                multi=True
                            ),
                            width={'size': 3, 'offset': 0, 'order': 1}
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='make_dropdown',
                                value=[],  # Default empty
                                options=make_name_checklist,
                                multi=True
                            ),
                            width={'size': 3, 'offset': 0, 'order': 3}
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id='fuel_type_dropdown',
                                value=[],  # Default empty
                                options=fuel_type_checklist,
                                multi=True
                            ),
                            width={'size': 3, 'offset': 0, 'order': 4}
                        )
                    ])
                ]),
                className='mb-3 pt-2 pb-2',  # Add some margin and padding
                style={'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)'}  # Add a slight box-shadow for depth
            )
        )
    ]),
    # Second Row
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(
                        id='box_plot_with_markers',
                        figure={}  # Initially empty
                    )
                ]),
                style={'padding-top': '0rem', 'padding-bottom': '0rem', 'padding-left': '0rem', 'padding-right': '0rem'},
                className='mb-3 pt-2 pb-2',  # Add some margin and padding
            ),
            width=8
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    dcc.Graph(
                        id='scatter_by_horsepower',
                        figure={}  # Initially empty
                    )
                ]),
                style={'padding-top': '0rem', 'padding-bottom': '0rem', 'padding-left': '0rem', 'padding-right': '0rem'},
                className='mb-3 pt-2 pb-2',  # Add some margin and padding
            ),
            width=4
        )
    ], justify='center')
], fluid=True)



@app.callback(
    [Output('box_plot_with_markers', 'figure'),
     Output('scatter_by_horsepower', 'figure')],
    [Input('engine_type_dropdown', 'value'),
    Input('price_range_dropdown', 'value'),
    Input('make_dropdown', 'value'),
    Input('fuel_type_dropdown', 'value')]
)
def update_box_graph_with_markers(engine_type_selected, price_range_selected, make_selected, fuel_type_selected):

    # Handle dropdowns & filters to build a plot'able df
    df_to_plot = all_cars

    if engine_type_selected:
        df_to_plot = df_to_plot[df_to_plot['engine_type'].isin(engine_type_selected)]

    if price_range_selected:
        df_to_plot = df_to_plot[df_to_plot['msrp_label'].isin(price_range_selected)]

    if make_selected:
        df_to_plot = df_to_plot[df_to_plot['make'].isin(make_selected)]

    if fuel_type_selected:
        df_to_plot = df_to_plot[df_to_plot['fuel_type'].isin(fuel_type_selected)]

    # First Figure:
    # Define the figure based on a df that has been filtered according to all the pick lists. 
    figBox = px.box(df_to_plot, 
                   x='make', 
                   y='horsepower_per_100_dollars')

    # Add a shape to our box plot. An overall median based on our current filter
    filtered_df_overall_median = df_to_plot['horsepower_per_100_dollars'].median()
    if not df_to_plot.empty:
        figBox.add_shape(
            type="line",
            x0=0,
            x1=1,
            y0=filtered_df_overall_median,
            y1=filtered_df_overall_median,
            xref='paper',
            yref='y',
            line=dict(color="orange", width=1)
        )

    # Add a scatter plot to show individual points
    figBox.add_scatter(
        y=df_to_plot['horsepower_per_100_dollars'],
        x=df_to_plot['make'],
        mode='markers',
        hovertext=df_to_plot['model'].astype(str) +
                ": " + df_to_plot['trim'].astype(str) +
                " " + df_to_plot['horsepower_hp'].astype(str) + "hp" +
                " $" + df_to_plot['msrp'].astype(str),
        marker=dict(
            color='orange',
            size=5
        ),
        showlegend=False
    ),
    #This is a box-graph x-axis sorter based on the median horsepower_per_100_dollars col so we see low to hi, not Acura to Volvo.
    filtered_df_agg_make_median = df_to_plot.groupby('make')['horsepower_per_100_dollars'].median().reset_index()
    filtered_df_agg_make_median_sort_list = filtered_df_agg_make_median.sort_values('horsepower_per_100_dollars')['make'].tolist()
    
    figBox.update_layout(
        title={
            'text': 'How much horsepower does $100 buy?',
            'font': {'size':18}
        },
        xaxis=dict(
            categoryorder='array',
            categoryarray=filtered_df_agg_make_median_sort_list
        ),
        xaxis_title="",
        yaxis_title="MSRP to Power Ratio",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=650
    )

    # Second Figure

    figScatter = px.scatter(
        df_to_plot,
        x='horsepower_hp',
        y='make',
        hover_data=["model", "trim"],
        color_discrete_sequence=['orange'],  # Set the marker color
        size_max=5  # Set the maximum marker size
    )

    figScatter.update_layout(
        title={
            'text': 'Range of Horsepower',
            'font': {'size': 18}
        },
        yaxis=dict(
            categoryorder='array',
            categoryarray=filtered_df_agg_make_median_sort_list[::-1], #Reverse the list as I swapped axes
            title_text=''
        ),
        xaxis=dict(
            title_text=''
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=650
    )

    return figBox, figScatter

if __name__ == '__main__':
    app.run(debug=True)
