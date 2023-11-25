import requests

def fetch_all_stock_data(symbol, time_series_function):
    #api_key = 'YTWWO25DJI2S9JJW'
    api_key = '1754LTIVH88SHG3R'
    base_url = 'https://www.alphavantage.co/query'

    params = {
        'symbol': symbol,
        'apikey': api_key,
        'outputsize': 'compact'
    }

    if time_series_function == "TIME_SERIES_INTRADAY":
        params['function'] = "TIME_SERIES_INTRADAY"
        params['interval'] = '60min'
    elif time_series_function == "TIME_SERIES_DAILY":
        params['function'] = "TIME_SERIES_DAILY"
    elif time_series_function == "TIME_SERIES_WEEKLY":
        params['function'] = "TIME_SERIES_WEEKLY"
    elif time_series_function == "TIME_SERIES_MONTHLY":
        params['function'] = "TIME_SERIES_MONTHLY"
        
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        print(response.json())  # Add this line for debugging
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
