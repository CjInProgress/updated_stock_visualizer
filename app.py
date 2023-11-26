from flask import Flask, render_template, request, url_for
import os, pandas as pd
from datetime import datetime

# Importing the functions from the script.py and stock.py
from script import fetch_all_stock_data
from stock import process_stock_data, plot_and_save_stock_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get the stock symbol file
    stock_symbol_list_file_path = 'data/stocks.csv'
    stocks_df = pd.read_csv(stock_symbol_list_file_path)

    # Extracting just the stock symbols
    stock_symbols = stocks_df['Symbol'].tolist()
    
    if request.method == 'POST':
        print(request.form)  # Debugging line to print form data
    
        symbol = request.form.get('symbol')
        if symbol not in stock_symbols:
            return render_template('index.html', error="Invalid stock symbol.", symbols=stock_symbols)
        chart_type = request.form['chart_type']
        time_series = request.form['time_series']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Define the time series function name based on the input
        time_series_function = {
            "1": "TIME_SERIES_INTRADAY",
            "2": "TIME_SERIES_DAILY",
            "3": "TIME_SERIES_WEEKLY",
            "4": "TIME_SERIES_MONTHLY"
        }.get(time_series, "TIME_SERIES_DAILY")  # Default to DAILY if invalid

        # Fetch stock data
        raw_data = fetch_all_stock_data(symbol, time_series_function)
        
        if 'Error Message' in raw_data:
            # Provide a specific error message
            error_message = raw_data['Error Message']
            return render_template('index.html', error=error_message, symbols=stock_symbols)

        if raw_data:
            # Process the data
            processed_data = process_stock_data(raw_data)
            
            if processed_data is not None:
                # Generate a unique filename for the graph image
                filename = f"{symbol}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                save_path = os.path.join('static', 'images', filename)

                # Plot and save the stock data
                plot_and_save_stock_data(processed_data, symbol, chart_type, start_date, end_date, save_path)

                # Generate the URL for the image
                graph_image_url = url_for('static', filename=os.path.join('images', filename))
                print("Image file path successfully generated")
                return render_template('result.html', graph_url=graph_image_url, symbol=symbol)

        # Error handling for failed data fetch or processing
        error_message = "Failed to fetch or process data. Please check the stock symbol or try again later."
        return render_template('index.html', error=error_message, symbols=stock_symbols)

    # GET request - show the initial form
    # Pass the stock symbols to the template
    return render_template('index.html', symbols=stock_symbols)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

