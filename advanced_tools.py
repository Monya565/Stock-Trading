
def checkhl(data_back, data_forward, hl):

    if hl == 'high' or hl == 'High':
        ref = data_back[len(data_back)-1]
        for i in range(len(data_back)-1):
            if ref < data_back[i]:
                return 0
        for i in range(len(data_forward)):
            if ref <= data_forward[i]:
                return 0
        return 1
    if hl == 'low' or hl == 'Low':
        ref = data_back[len(data_back)-1]
        for i in range(len(data_back)-1):
            if ref > data_back[i]:
                return 0
        for i in range(len(data_forward)):
            if ref >= data_forward[i]:
                return 0
        return 1



def pivot(osc, LBL, LBR, highlow):

    pivots=[]
    left = []
    right = []
    for i in range(len(osc)):
        pivots.append(0.0)
        if i < LBL + 1:
            left.append(osc[i])
        if i > LBL:
            right.append(osc[i])
        if i > LBL + LBR:
            left.append(right[0])
            left.pop(0)
            right.pop(0)
            if checkhl(left, right, highlow):
                pivots[i - LBR] = osc[i - LBR]
    return pivots



def filter_targets(targets,side):
    filtered_targets=[targets[0]]
    if side.lower() == 'long':
        for price in targets:
            if price/filtered_targets[-1] > 1.005 :
                filtered_targets.append(price)

    elif side.lower() == 'short':
        for price in targets:
            if filtered_targets[-1]/price > 1.005 :
                filtered_targets.append(price)

    return filtered_targets



def calculate_targets(df, side, signal_price, k =0.005):
    targets=[]
    if side.lower() == 'short':
        try:
            piv=pivot(osc=df["low"], LBL=10,LBR=10,highlow="low")
            targets_sorted = sorted([p for p in piv if p != 0.0 and p < ((1-k) * signal_price)],reverse=True)
            targets = filter_targets(targets=targets_sorted, side= side)
        except Exception as e:
            targets = [signal_price*0.985]

    elif side.lower() == 'long':   
        try:
            piv=pivot(osc=df["high"], LBL=10,LBR=10,highlow="high")
            targets_sorted = sorted([p for p in piv if p != 0.0 and p > ((1+k) * signal_price) ])
            targets = filter_targets(targets=targets_sorted, side= side)
        except Exception as e:
            targets = [signal_price*1.015]

    return targets



def calculate_stoploss(df, side, signal_price):
    sl =0
    if side.lower() == 'long':
        try:
            piv=pivot(osc=df["low"], LBL=10,LBR=10,highlow="low")
            sl = [p for p in piv if p != 0.0 and p < 0.995 * signal_price][-1]
        except Exception as e:
            sl = signal_price*0.985


    elif side.lower() == 'short':   
        try:
            piv=pivot(osc=df["high"], LBL=10,LBR=10,highlow="high")
            sl = [p for p in piv if p != 0.0 and p > 1.005 * signal_price ][-1]
        except Exception as e:
            sl = signal_price*1.015

    return sl    