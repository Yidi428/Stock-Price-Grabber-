# Stock Data Grabber

The Stock Data Grabber is a Python application built using the PyQt5 framework that allows users to fetch and display historical stock data from Yahoo Finance. The application provides a user-friendly interface with various features, including date selection using calendars, interval selection, and the ability to save the fetched data to a text file.

## Features

- **Ticker Symbol Input**: Users can enter the ticker symbol of the desired stock (e.g., AMZN for Amazon).
- **Date Selection**: Users can either manually enter the start and end dates or use the provided calendar widgets to select the desired date range.
- **Interval Selection**: Users can choose the interval for the stock data (1 day, 1 week, or 1 month).
- **Data Display**: The fetched stock data, including the dates and corresponding close prices, is displayed in a scrollable text area.
- **Data Saving**: Users can save the fetched stock data to a text file for future reference.
- **Error Handling**: The application handles various error scenarios, such as invalid date formats or unavailable data, and displays appropriate error messages.
- **Responsive Design**: The application window size adjusts automatically based on the screen resolution, ensuring a consistent user experience across different devices.

## Requirements

- Python 3.x
- PyQt5
- yfinance (Yahoo Finance API)

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies using pip:

```
pip install PyQt5 yfinance
```

## Usage

1. Run the `expense.py` file.
2. Enter the desired ticker symbol in the input field.
3. Select the start and end dates using either the calendar widgets or manual input.
4. Choose the desired interval (1 day, 1 week, or 1 month) from the dropdown menu.
5. Click the "Scrape" button to fetch the stock data.
6. The fetched data will be displayed in the text area, showing the dates and corresponding close prices.
7. (Optional) Click the "Save Data" button to save the fetched data to a text file.

## Contributing

Contributions to the Stock Data Grabber project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

_This project was created by a noob._
