# Stock Visualizer Web Application

This web application enables users to visualize stock price data for various companies. Built with Flask and Python, it integrates with the Alpha Vantage API for fetching stock data. The application includes a Docker setup for easy deployment and management.

## Prerequisites

Before running the application, ensure you have the following installed:

- Docker: [Install Docker](https://www.docker.com/get-started)
- Python 3.8 or higher: [Install Python](https://www.python.org/downloads/)

## Setup

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd stock-visualizer
   ```

3. **Build the Docker Image**:
   ```bash
   docker build -t my-python-app .
   ```

## Usage

1. **Run the Docker Container**:

   ```bash
   docker run -p 5000:5000 my-python-app
   ```

2. **Access the Application**:
   Open a web browser and navigate to `http://localhost:5000`.

3. **Using the Application**:
   - Select a stock symbol from the dropdown list.
   - Choose a chart type (line or bar).
   - Select a time series (intraday, daily, weekly, or monthly).
   - Optionally, specify a start and end date for the data.
   - Click the "Visualize" button to generate a stock price chart.

## Application Structure

1. **Dockerfile**: Sets up the Python environment, installs dependencies, and defines the entry point for the application.

2. **app.py**: The main Flask application file. It initializes the app and defines routes for web requests.

3. **script.py**: Contains scripts for additional functionalities used in the application.

4. **stock.py**: A module for handling stock data operations, including API interactions.

5. **requirements.txt**: Lists all Python dependencies required for the application.

6. **Static and Template Files**:

   - **app.css**: The stylesheet for the application's frontend.
   - **index.html**: The main landing page of the web application.
   - **result.html**: Displays the visualization results based on user input.

7. **Data Files**:
   - **stocks.csv**: Contains predefined stock data used in the application.

## Customizing the Application

- To customize the application, modify the Flask app (`app.py`) or the frontend templates (`index.html`, `result.html`).
- Update `app.css` for any stylistic changes to the application's appearance.
- Add or modify scripts in `script.py` for extended functionalities.

## Notes

- Ensure the Flask application is set to listen on `0.0.0.0` for Docker compatibility.
- For production deployment, use a WSGI server instead of the Flask development server.
- Always keep your dependencies updated for security and performance.

## Support

For any queries or issues, refer to the documentation or open an issue in the repository.
