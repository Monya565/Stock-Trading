import telegram
import requests
from config import telegram_token, chat_id
import yfinance as yf
from datetime import timedelta
from advanced_tools import calculate_targets, calculate_stoploss
# telegram_bot = telegram.Bot(telegram_token)
messages = []

def is_unique(symbol, at , side):
    #messages = [{"symbol:":symbol, "time:":datetime , "side:": side}]
    try:
        print(symbol, at , side)
        if(at - messages [symbol][side]) > timedelta(minutes= 180):
            messages[symbol][side] = at
            return True
        else:
            return False
    except Exception as e:
        messages[symbol] = {"short":at , "long":at}
        return True
    unique_messages= []
    for(symbol, side) in messages:
        if symbol & side not in unique_messages:
            unique_messages.append(symbol, side)
            return True
        else:
            return False
    messages = unique_messages
    return messages


def get_price(symbol):
   
    price = 0
    ticker = yf.Ticker(symbol)
    price = ticker.history(period= '1d' , interval= 'tf')
    last_price = price['Close'].iloc[-1]
    return last_price


def get_data(symbol, timeframe, period):
    data = 0
    data= yf.download(tickers=symbol ,
                  interval= timeframe, 
                  period= period, 
                  auto_adjust= True)
    print (data)
    return data


def Stoploss(data, side, signal_price):
    sl= calculate_stoploss(df=data, side=side, signal_price=signal_price)
    return sl

def find_targets(data, side, signal_price):
    targets =calculate_targets(df=data, side=side, signal_price=signal_price)
    return targets
    
def create_message(side, symbol, signal_price, targets, leverage, stoploss):
    targets= ('\n'.join(map(str, targets)))
    if side.lower() == 'long':
        side = side +' / SPOT'
    else:
        side = side
    
    text = f'''
    (ISOLATE)
     {side} 
     LEVERAGE: {leverage}
     {symbol}
     Entry Price: {signal_price}
     STOPLOSS : {stoploss}
     TARGET 
     {targets}
     '''
    print(text)   
        

def send_message(text):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chat_id}&text={text}"
    print(requests.get(url).json())
    