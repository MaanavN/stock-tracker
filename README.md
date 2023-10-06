# stock-tracker
Python script that will track a stock using the yfinance library and automatically notify the user when price hits a user-defined high or low.


The code is constantly checking the stock price by using the yfinance library so it needs to be run nonstop on a machine.

Make sure to change all "CHANGE ME"s within the code before running. The API key and and phone-number can be obtained from Twilio's website after signing up for free.

To run the cli version of the code: python3 stocktracker-cli.py
To run the webapp: python3 webapp/app.py
