import telegram
import tools
from config import WEBHOOK_PASSPHRASE, tadawul_chat_id, tadawul_telegram_token
import json
from flask import Flask, request, jsonify
from datetime import datetime
from general_memory import tadawl_stocks


app = Flask(__name__)

tadawul_telegram_bot = telegram.Bot(tadawul_telegram_token)

@app.route('/', methods=['GET'])
def welcome():
    return "Hello world, am Monya"

@app.route('/tadawul', methods=['POST'])
def tadawul():
    payload = json.loads(request.data)
    
    if payload['passphrase'] != WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid request"
        }


    # Payload & data
    symbol = payload['symbol']
    name = tadawl_stocks[symbol]
    tf = payload['tf']
    df = tools.get_tadawul_data(symbol=f"{symbol}.SR", timeframe=tf, period="5d")
    signal_price = df['close'].iloc[-1]
    side = payload['side'].lower()
    at = datetime.now()
    print(f"tadawul - {name} - @ {at}")

    # anti- duplication ..
    if tools.is_unique(symbol=symbol, side=side, at = at) and side.lower() == "long":
        stoploss = tools.set_pivot_stoploss(data= df, side=side, signal_price=signal_price)
        targets = tools.find_pivot_targets(data=df, side=side, signal_price=signal_price)
        message = tools.create_AR_message(side=side, name=name, symbol=symbol, signal_price=signal_price, targets=targets, stoploss=stoploss, risklevel=True)
        tadawul_telegram_bot.send_message(text= message, chat_id=tadawul_chat_id, parse_mode=telegram.ParseMode.HTML)
        # info= general_tools.trade_info(bot="Tadauwl", status="success", symbol=symbol, side=side, at=at)
        info = "success"
        print(info)
        return jsonify(info)

    # info= general_tools.trade_info(bot="Tadauwl", status="failure", symbol=symbol, side=side, at=at)
    info="failure"
    return jsonify(info)



# Start the app
if __name__ == '__main__':
    app.run(host="0.0.0.0")