import yfinance as yf
from datetime import timedelta
from advanced_tools import calculate_targets, calculate_stoploss

# am using this liberary "telegram" at the rest of the app,
# so am using it here to ...
# you can install it by : pip install python-telegram-bot
# then:                   import telegram


messages = {}

# def is_unique(symbol, at , side):
#     #messages = [{"symbol:":symbol, "time:":datetime , "side:": side}]
#     try:
#         print(symbol, at , side)
#         if(at - messages [symbol][side]) > timedelta(minutes= 180):
#             messages[symbol][side] = at
#             return True
#         else:
#             return False
#     except Exception as e:
#         messages[symbol] = {"short":at , "long":at}
#         return True

def is_unique(symbol, side, at):
    try:
        print(symbol,side)
        if (at - messages[symbol][side]) > timedelta(hours=2):
            messages[symbol][side] = at
            return True
        else:
            return False
    except Exception as e:
        messages[symbol] = {"short":at, "long":at}
        return True


# def get_tadawul_price(symbol):   
#     ticker = yf.Ticker(symbol)
#     price = ticker.history(period= '1d' , interval= '15m')
#     last_price = price['Close'].iloc[-1]
#     print(last_price)
#     return last_price
#



def get_tadawul_data(symbol, timeframe, period):
    """
    decided that we can just get the data one time, 
    then call data.iloc[-1] on it to get the price
    find the data.iloc[-1] call in app.py
    so..., I canceled the get_price() function...
    """
    data= yf.download(tickers=symbol ,
                  interval= timeframe, 
                  period= period, 
                  auto_adjust= True)
    # here also I changed columns names from capital to small , 
    # just to make it compatable with the Advanced_tools functions....
    # as the set_stoploss & find_targets functions are expecting small letters
    # at the field names Open -> open, High -> high ...
    data.columns = ['open', 'high', 'low', 'close', 'volume']
    return data


def set_pivot_stoploss(data, side, signal_price):
    sl= calculate_stoploss(df=data, side=side, signal_price=signal_price)
    return sl

def find_pivot_targets(data, side, signal_price):
    targets =calculate_targets(df=data, side=side, signal_price=signal_price)
    return targets
    
# def create_message(side, symbol, signal_price, targets, leverage, stoploss):
#     targets= ('\n'.join(map(str, targets)))
#     if side.lower() == 'long':
#         side = side +' / SPOT'
#     else:
#         side = side
    
#     text = f'''
#     (ISOLATE)
#      {side} 
#      LEVERAGE: {leverage}
#      {symbol}
#      Entry Price: {signal_price}
#      STOPLOSS : {stoploss}
#      TARGET 
#      {targets}
#      '''
#     print(text)   


def create_AR_message( name, side, symbol, signal_price, targets, stoploss, risklevel=False):

    """
    made arabic massege, 
    rounded all numbers to 2 decimal places
    canceled short side messages for now,..
    added functionality to calculate risk based on how far is the stoploss from the entry price!!

    """


    if side.lower() == "long":
        stop = round(stoploss,2) 
        entery = round(signal_price,2)
        targets_statement=""
        risk_statement=""
        if risklevel:
            risk = abs(stop-entery)/entery
            if risk < 0.016:
                risk_statement="🟢 خطورة منخفضة"
            elif risk < 0.025:
                risk_statement="🟡 خطورة متوسطة"
            else:
                risk_statement="🔴 خطورة عالية"

        for i, target in enumerate(targets):
            t = f"\n {i+1})  {round(target,2)} "
            targets_statement += t
        entery_title= "سعر الدخول"
        stoploss_title= "وقف الخسارة"
        target_title= "الأهداف"
        message= f"""
     [تداول - الأسهم السعودية]

     [ {name} ] • [{symbol}] 

      {entery_title} : {entery}
      {stoploss_title} : {stop} 
      {target_title} :
      {targets_statement}
      {risk_statement}
    """
        return message        
    
