import yfinance as yf
from twilio.rest import Client
import sys



def get_stock(ticker):
    while True:
        valid_ticker = True
        try:
            stock = yf.Ticker(f"{ticker.upper()}")
        except:
            valid_ticker = False
            break
        try:
            current_price = stock.info['regularMarketPrice']
            break
        except:
            try:
                current_price = stock.info['currentPrice']
                break
            except:
                valid_ticker = False
                break

    if valid_ticker == False:
        return "invalid"
    else:
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
    


def validate_phone_num(phone_num):
    first_digit = str(phone_num)[0]

    try:
        int(phone_num)
        if len(str(phone_num)) == 10:
            phone_num = f"+1{phone_num}"
            return phone_num
        elif first_digit == "+" and len(str(phone_num)) == 12:
            return phone_num
        else:
            return "invalid"
    except ValueError:
        return "invalid"



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



def run_main(stock_info, prices, phonenum):
    ticker = stock_info['ticker']

    

    account_sid = "CHANGE ME"
    auth_token = "CHANGE ME"

    client = Client(account_sid, auth_token)



    while True:
        stock_info = refresh_stock(ticker)
        if float(stock_info['current_price']) >= float(prices['high']):
            text_message = f"{stock_info['stock']} is currently at {prices['high']}"
            message = client.messages.create(
                to="CHANGE ME",
                from_="CHANGE ME",
                body=text_message
            )
            break
        elif float(stock_info['current_price']) <= float(prices['low']):
            text_message = f"{stock_info['stock']} is currently at {prices['low']}"
            message = client.messages.create(
                to=str(phonenum),
                from_="CHANGE ME",
                body=text_message
            )
            break
        else:
            pass

    print(message.sid)
