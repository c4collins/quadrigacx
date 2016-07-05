import requests
from datetime import datetime
from flask import Flask, render_template, request
from flask_qrcode import QRcode
from quadriga import  QCX
from lobgect import log

app = Flask(__name__)
logger = log.Log(__name__)
# auth = qcx_auth.Auth('config/auth.cfg')
qcx = QCX('config/auth.cfg')
qr = QRcode(app)




## INTERNAL HELPER FUNCTIONS ##
def _get_page_data(page_title, nav_root):
    page_info = {
        'nav_root'      : nav_root,
        'page_title'    : page_title
    }
    return { 'page_info': page_info }

## HOME ##
@app.route('/')
def index():
    return render_template('main.html')






## PUBLIC METHODS ##
@app.route('/currentTradingInformation')
@app.route('/currentTradingInformation/<book>')
def current_trading_information(book=None):
    data = qcx.api('ticker', book)
    return render_template('public/currentTradingInformation.html', data=data)

@app.route('/orderBook')
@app.route('/orderBook/<book>')
@app.route('/orderBook/<book>/<group>')
def order_book(book=None, group=None):
    data = qcx.api('order_book', book, False if group else True)
    return render_template('public/orderBook.html', data=data)

@app.route('/transactions')
@app.route('/transactions/<book>')
@app.route('/transactions/<book>/<time_frame>')
def transactions(book=None, time_frame=None):
    data = qcx.api('transactions', book, time_frame)
    return render_template('public/transactions.html', data=data)






## AUTHENTICATED METHODS ##
# Information #
@app.route('/accountBalance')
def account_balance():
    data = qcx.api('balance')
    return render_template('private/accountBalance.html', data=data)

@app.route('/userTransactions')
@app.route('/userTransactions/<book>')
def user_transactions(book=None):
    data = qcx.api('user_transactions', book)
    return render_template('private/userTransactions.html', data=data)

@app.route('/openOrders')
@app.route('/openOrders/<book>')
def open_orders(book=None):
    data = qcx.api('open_orders', book)
    return render_template('private/openOrders.html', data=data)

@app.route('/lookupOrder/<order_id>')
def lookup_order(order_id):
    data = qcx.api('lookup_order', order_id)
    return render_template('private/lookupOrder.html', data=data)
# Form Actions
@app.route('/lookupOrder', methods=['GET'])
def lookup_order_form():
    return render_template('private/forms/lookupOrder.html')
@app.route('/lookupOrder', methods=['POST'])
def lookup_order_form_post():
    return lookup_order(order_id=request.values['order_id'])

# Orders #
@app.route('/cancelOrder/<order_id>')
def cancel_order(order_id):
    data = qcx.api('cancel_order', order_id)
    return render_template('private/cancelOrder.html', data=data)
# Form Actions
@app.route('/cancelOrder', methods=['GET'])
def cancel_order_form():
    return render_template('private/forms/cancelOrder.html')
@app.route('/cancelOrder', methods=['POST'])
def cancel_order_form_post():
    return cancel_order(order_id=request.values['order_id'])

@app.route('/buy/<book>/<amount>/<price>')
def buy(book='btc_cad', amount='0', price='1000000'):
    data = qcx.api('buy', book, amount, price)
    return render_template('private/buy.html', data=data)
# Form Actions
@app.route('/buy', methods=['GET'])
def buy_form():
    return render_template('private/forms/buy.html')
@app.route('/buy', methods=['POST'])
def buy_form_post():
    return buy(book=request.values['book'], amount=request.values['amount'], price=request.values['price'])

@app.route('/sell/<book>/<amount>/<price>')
def sell(book='btc_cad', amount='0', price='1000000'):
    data = qcx.api('sell', book, amount, price)
    return render_template('private/sell.html', data=data)
# Form Actions
@app.route('/sell', methods=['GET'])
def sell_form():
    data = _get_page_data('Sell Cryptocurrencies', '/sell')
    return render_template('private/forms/sell.html', data=data)
@app.route('/sell', methods=['POST'])
def sell_form_post():
    return sell(book=request.values['book'], amount=request.values['amount'], price=request.values['price'])

# Currency #
@app.route('/deposit')
def deposit():
    data = _get_page_data('Deposit Cryptocurrencies', '/deposit')
    data['currencies'] = [
        {
            'name': 'Bitcoin',
            'deposit_address': qcx.api('bitcoin_deposit_address')
        },
        {
            'name': 'Ethereum',
            'deposit_address': qcx.api('ether_deposit_address')
        },
    ]
    return render_template('private/deposit.html', data=data)


@app.route('/withdraw/<currency>/<address>/<amount>')
def withdraw(currency, address, amount='0'):
    data = _get_page_data('Withdraw Cryptocurrencies', '/withdraw')

    if currency.lower() in ['btc', 'bitcoin']:
        data['response'] = qcx.api('bitcoin_withdraw', amount, address)
    elif currency.lower() in ['eth', 'ether', 'ethereum']:
        data['response'] = qcx.api('ether_withdraw', amount, address)

    return render_template('private/withdrawal.html', data=data)
# Form Actions
@logger.print_post_data
@app.route('/withdraw', methods=['GET', 'POST'])
def withdrawal_form():
    logger.debug( dir(request) )
    logger.debug( request.method )
    logger.debug( request.values )

    if request.method == 'GET':
        data = _get_page_data('Withdraw Cryptocurrencies', '/withdraw')
        return render_template('private/forms/withdrawal.html', data=data)

    elif request.method == 'POST':
        return withdraw(currency=request.values['currency'], address=request.values['address'], amount=request.values['amount'])


## TEMPLATE FORMATTERS ##
@app.template_filter('datetime')
def format_datetime(datetime_input, output_format="%d-%B-%Y %H:%M:%S"):
    if type(datetime_input) is not datetime:
        try:
            checked_datetime = datetime.strptime(datetime_input, '%Y-%m-%d %H:%M:%S')
        except TypeError:
            logger.warning('Invalid item passed for conversion to datetime: {}'.format(datetime_input))
            return datetime(2009, 1, 3, 18, 15, 05)
    else:
        checked_datetime = datetime_input
    return checked_datetime.strftime(output_format)

@app.template_filter('transaction_type')
def format_transaction_type(transaction_type_input):
    str_input = str(transaction_type_input)
    if   str_input == '0': transaction_type = 'deposit'
    elif str_input == '1': transaction_type = 'withdrawal'
    elif str_input == '2': transaction_type = 'trade'
    else:
        logger.warning('Invalid transaction_type returned by QuadrigaCX: <\'{}\' type=[{}]>'.format(transaction_type_input, type(transaction_type_input)))
        transaction_type = None
    return transaction_type

@app.template_filter('order_type')
def format_order_type(order_type_input):
    str_input = str(order_type_input)
    if   str_input == '0': order_type = 'buy'
    elif str_input == '1': order_type = 'sell'
    else:
        logger.warning('Invalid order_type returned by QuadrigaCX: <\'{}\' type=[{}]>'.format(order_type_input, type(order_type_input)))
        order_type = None
    return order_type

@app.template_filter('order_status')
def format_order_status(order_status_input):
    str_input = str(order_status_input)
    if   str_input == '-1': order_status = 'cancelled'
    elif str_input ==  '0': order_status = 'active'
    elif str_input ==  '1': order_status = 'partially filled'
    elif str_input ==  '2': order_status = 'complete'
    else:
        logger.warning('Invalid order_status returned by QuadrigaCX: <\'{}\' type=[{}]>'.format(order_status_input, type(order_status_input)))
        order_status = None
    return order_status





if __name__ == "__main__":
    app.run()
