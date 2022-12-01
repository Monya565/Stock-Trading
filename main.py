import tools
from config import WEBHOOK_PASSPHRASE, period, leverage
import json
from flask import Flask, request, jsonify
from datetime import datetime
import advanced_tools


app = Flask(__name__)



@app.route('/', methods=['GET'])
def welcome():
    return "Hello world, am Monya"

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = json.loads(request.data)
    
    if payload['passphrase'] != WEBHOOK_PASSPHRASE:
        info ={
            "code": "error",
            "message": "Nice try, invalid request"
        }
        return jsonify(info) 

    # Payload & data
    symbol = payload['symbol']
    signal_price = tools.get_price(symbol=symbol)
    side = payload['side'].lower()
    tf = payload['tf']
    at = datetime.now()

    # anti- duplication ..
    if tools.is_unique(symbol=symbol, side=side, time=at):
        data = tools.get_data(symbol=symbol, timeframe=tf, period= period)

        stoploss = tools.stoploss(data = data, side=side, signal_price=signal_price)
        
        targets = tools.find_targets(data = data, side=side, signal_price=signal_price)

        message = tools.create_message(side=side, symbol=symbol, signal_price=signal_price, targets=targets, leverage=leverage, stoploss=stoploss)

        tools.send_message(text= message)
        info = {
            "code": "success",
            "message": message
        }
        return jsonify(info) 

    else:
        info ={
            "code": "error",
            "message": "Post request is dublicated"
        }
        return jsonify(info) 


# Start the app
if __name__ == '__main__':
    app.run(host="0.0.0.0")