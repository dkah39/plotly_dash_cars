
# Car Data Dashboard - CarAPI Data + Plotly Dash

## Overview

This is a Dash app that visualizes various aspects of car data for the year 2020. The app allows you to filter data based on engine type, price range, make, and fuel type. It provides insights into the horsepower-to-price ratio and the range of horsepower across different makes.

![Dashboard Screenshot](/artifacts/dashboard.png)

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1. Clone this repository.
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```
2. Navigate to the project directory.
   ```bash
   cd your-repo-name
   ```
3. Install the required packages.
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Register for a free API key from [CarAPI](https://carapi.app/register).
2. Create a `.env` file in the root directory of the project.
3. Add your CarAPI API token and secret to the `.env` file.
   ```env
   CARAPI_API_TOKEN=your_api_token_here
   CARAPI_API_SECRET=your_api_secret_here
   ```

### Fetching Data

Run `get_carapi_data.py` to fetch the car data and save it as `engines_data.json` in the `./data` directory.

```bash
python get_carapi_data.py
```

### Running the App

Run `app.py` to start the Dash app.

```bash
python app.py
```

Open your web browser and go to `http://127.0.0.1:8050/` to view the app.

## Features

- Filter cars based on engine type, price range, make, and fuel type.
- Visualize the horsepower-to-price ratio across different makes.
- View the range of horsepower for different makes.

## Acknowledgments

Thanks to the team at [CarAPI](https://carapi.app/api) for allowing free usage of 2020 model data.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
