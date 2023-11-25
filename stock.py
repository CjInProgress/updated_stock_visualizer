import pandas as pd
from pandas import to_datetime
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

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

def plot_and_save_stock_data(df, symbol, chart_type, start_date, end_date, save_path):
    # Convert start and end dates to datetime, handling empty or invalid inputs
    if start_date:
        start_date = to_datetime(start_date)
    else:
        start_date = df.index.min()  # use earliest date in the DataFrame

    if end_date:
        end_date = to_datetime(end_date)
    else:
        end_date = df.index.max()  # use latest date in the DataFrame

    # Filter the DataFrame by date range
    df = df.loc[start_date:end_date]

    # Create the plot
    ax = plt.subplots()
    
    # Plot the data according to chart type
    if chart_type == "line":
        ax.plot(df.index, df["Close"], label="Close", color='green')
    elif chart_type == "bar":
        ax.bar(df.index, df["Close"], label="Close", color='blue')
        
    plt.title(f"{symbol} Prices from {start_date} to {end_date}")
    plt.xlabel("Date")
    plt.ylabel("Price")

    # Set y-axis to start at 0 and dynamically set the upper limit based on the data
    ax.set_ylim(bottom=0, top=max(df["Close"])*1.1)  # 10% padding above the max value

    # Set the maximum number of y-axis ticks to 5
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))

    # Rotate x-axis labels
    plt.setp(ax.get_xticklabels(), rotation=45)

    plt.legend()  # Add a legend to distinguish the close line

    # Save the figure
    plt.savefig(save_path, dpi=300)
    plt.close()
