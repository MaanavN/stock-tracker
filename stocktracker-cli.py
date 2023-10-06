import yfinance as yf
from twilio.rest import Client
import sys



try:
    def get_stock():
        while True:
            ticker = input("Enter stock ticker symbol: ")
            stock = yf.Ticker(f"{ticker.upper()}")
            try:
                current_price = stock.info['regularMarketPrice']
                break
            except KeyError:
                try:
                    current_price = stock.info['currentPrice']
                    break
                except:
                    pass

        stock_info = {"stock": stock, "current_price": current_price, "ticker": ticker}
        
        return stock_info



    def set_price_checker(stock_info):
        while True:
            try:
                high_price = input(f"Set the high price to when you want to be notified (must be higher than current price of {stock_info['current_price']}): ")
                if float(high_price) > float(stock_info['current_price']):
                    break
                else:
                    pass
            except:
                pass

        while True:
            try:
                low_price = input(f"Set the low price to when you want to be notified (must be lower than current price of {stock_info['current_price']}): ")
                if float(low_price) < float(stock_info['current_price']):
                    break
                else:
                    pass
            except:
                pass

        prices = {"low": low_price, "high": high_price}

        return prices
        


    def refresh_stock(ticker):
        while True:
            stock = yf.Ticker(f"{str(ticker).upper()}")
            try:
                current_price = stock.info['regularMarketPrice']
                break
            except KeyError:
                try:
                    current_price = stock.info['currentPrice']
                    break
                except:
                    print("\nA problem occured with the API.")
                    print("Exiting Program.")
                    sys.exit()

        stock_info = {"stock": stock, "current_price": current_price}
        
        return stock_info



    def run_main():
        stock_info = get_stock()
        prices = set_price_checker(stock_info)
        ticker = stock_info['ticker']

        

        account_sid = "CHANGE ME"
        auth_token = "CHANGE ME"

        client = Client(account_sid, auth_token)



        while True:
            stock_info = refresh_stock(ticker)
            if float(stock_info['current_price']) == float(prices['high']):
                text_message = f"{stock_info['stock']} is currently at {prices['high']}"
                message = client.messages.create(
                    to="CHANGE ME",
                    from_="CHANGE ME",
                    body=text_message
                )
                break
            elif float(stock_info['current_price']) == float(prices['low']):
                text_message = f"{stock_info['stock']} is currently at {prices['low']}"
                message = client.messages.create(
                    to="CHANGE ME",
                    from_="CHANGE ME",
                    body=text_message
                )
                break
            else:
                pass

        print(message.sid)

    run_main()

except KeyboardInterrupt:
    print("\nExiting Program.")
    sys.exit()
