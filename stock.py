import os
import pandas as pd
from pandas import to_datetime
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter

def process_stock_data(data):
    if "Error Message" in data:
        print("Invalid symbol or function. Please try again.")
        return None
    ts_key = next((key for key in data if "Time Series" in key), None)
    if not ts_key:
        print("Time series data not found.")
        return None
    df = pd.DataFrame.from_dict(data[ts_key], orient="index")
    df.columns = ["Open", "High", "Low", "Close", "Volume"]
    df.index = pd.to_datetime(df.index)
    return df.sort_index()

def delete_old_photos(save_path):
    # Ensure the image directory exists
        image_dir = os.path.dirname(save_path)
        os.makedirs(image_dir, exist_ok=True)

        # Delete all files in the image directory
        for filename in os.listdir(image_dir):
            file_path = os.path.join(image_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file: {e}")

def plot_and_save_stock_data(df, symbol, chart_type, start_date, end_date, save_path, column='Close'):
    #First, delete old photos in the images folder.
    delete_old_photos(save_path)
    
    # Check if DataFrame is empty
    if df.empty:
        raise ValueError("The provided DataFrame is empty.")

    # Convert the column to numeric, setting errors='coerce' to handle non-numeric values
    df[column] = pd.to_numeric(df[column], errors='coerce')

    # Check if the column contains any numeric data after conversion
    if df[column].isnull().all():
        raise ValueError(f"The column '{column}' does not contain numeric data.")

    # Convert start and end dates to datetime, handling empty or invalid inputs
    if start_date:
        start_date = to_datetime(start_date)
    else:
        start_date = df.index.min()  # use earliest date in the DataFrame

    if end_date:
        end_date = to_datetime(end_date)
    else:
        end_date = df.index.max()  # use latest date in the DataFrame

    # Ensure that start_date is before end_date
    if start_date > end_date:
        raise ValueError("Start date must be before end date.")

    # Filter the DataFrame by date range
    df = df.loc[start_date:end_date]

    # Check if the filtered DataFrame is empty
    if df.empty:
        raise ValueError("No data available for the given date range.")

    # Create the plot
    fig, ax = plt.subplots()

    # Plot the data according to chart type
    if chart_type == "line":
        ax.plot(df.index, df[column], label=column, color='green')
    elif chart_type == "bar":
        ax.bar(df.index, df[column], label=column, color='blue')
    else:
        raise ValueError("Unsupported chart type. Please use 'line' or 'bar'.")

    plt.title(f"{symbol} {column} Prices from {start_date.date()} to {end_date.date()}")
    plt.xlabel("Date")
    plt.ylabel("Price")

    # Set y-axis limits
    max_value = df[column].max()
    if pd.notna(max_value):  # Check if max_value is not NaN
        ax.set_ylim(top=max_value * 1.1)  # 10% padding above the max value
    else:
        raise ValueError("Unable to determine the y-axis limits due to non-numeric data.")

    # Set the maximum number of y-axis ticks to 5
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    
    # Custom formatter for the y-axis
    def currency_formatter(x, pos):
        return f'${x}'
    ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))

    # Improve x-axis label spacing and rotation
    plt.xticks(rotation=45, ha="right")  # Rotate labels and align to the right

    
    plt.grid(True)
    
    plt.legend()  # Add a legend to distinguish the plotted column

    # Save the figure
    plt.savefig(save_path, dpi=300)
    plt.close()
    
    print(f"Plot saved successfully at {save_path}")
    return f"Plot saved successfully at {save_path}"