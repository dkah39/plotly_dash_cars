# 2020 Vehicles Dashboard

## Overview

This Dash app provides an interactive dashboard for exploring various aspects of car data for the year 2020. Users can filter the data based on engine type, price range, make, and fuel type to gain insights into the horsepower-to-price ratio and the range of horsepower across different makes.

![Dashboard Screenshot](/artifacts/dashboard.png)

## Features

- **Interactive Filters**: Four dropdown menus allow users to filter the data based on:
  - Engine Type
  - Price Range
  - Make
  - Fuel Type

- **Box Plot with Markers**: This plot shows the horsepower-to-price ratio for different makes. An orange line indicates the median value for the current filter settings. Individual data points are also plotted as markers.

- **Scatter Plot**: This plot shows the range of horsepower for different makes. Hovering over a point reveals additional information like the model and trim.

## Installation

1. Clone this repository.
2. Navigate to the project directory.
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the app:
    ```bash
    python app.py
    ```

## Usage

1. Open your web browser and go to `http://127.0.0.1:8050/`.
2. Use the dropdown menus to filter the data.
3. Explore the plots to gain insights into the 2020 car market.

## Dependencies

- Python 3.x
- Dash
- Plotly
- Pandas
- Dash Bootstrap Components

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
