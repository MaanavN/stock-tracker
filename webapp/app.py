from flask import Flask, render_template, request
from main import run_main, get_stock, refresh_stock, set_price_checker, validate_phone_num



app = Flask(__name__)



@app.route("/")
def landing_page():
    return render_template('landing_page.html')



@app.route("/getstock", methods=['POST'])
def get_stock_info():
    ticker_symbol = request.form['ticker_symbol']
    ticker_symbol = str(ticker_symbol).upper()

    global stock_info
    stock_info = get_stock(ticker_symbol)

    if stock_info == 'invalid':
        return render_template('landing_page.html')
    else:
        return render_template('getprices.html', current_price = stock_info['current_price'])



@app.route("/getprices", methods=['POST'])
def get_stock_prices():
    try:
        high_price = float(request.form['high_price'])
        low_price = float(request.form['low_price'])
    except ValueError:
        return render_template('getprices.html', current_price = stock_info['current_price'])

    if high_price < stock_info['current_price']:
        return render_template('getprices.html', current_price = stock_info['current_price'])

    if low_price > stock_info['current_price']:
        return render_template('getprices.html', current_price = stock_info['current_price'])

    global prices
    prices = {"low": low_price, "high": high_price}
    return render_template('getphonenum.html')



@app.route("/getphonenum", methods=['POST'])
def get_phone_num():
    phone_num = request.form['phonenum']

    phone_num = validate_phone_num(phone_num)
    if phone_num == 'invalid':
        return render_template('getphonenum.html')

    run_main(stock_info, prices, phone_num)


if __name__ == '__main__':
    app.run(host = '0.0.0.0')