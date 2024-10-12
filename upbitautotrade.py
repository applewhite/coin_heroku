import time
import pyupbit
import datetime

access = "ja9Jls674pUSAI6FQHeffJIRT4m4LI3Guxo7U04S"
secret = "G9bVUPraYhwqEZypgaSouIv6HCTJj0GxAm73Xl29"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    if df is not None and not df.empty:
        target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
        return target_price
    else:
        print("Failed to get OHLCV data")
        return None

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    if df is not None and not df.empty:
        start_time = df.index[0]
        return start_time
    else:
        print("Failed to get start time")
        return None

def get_balance(ticker):
    """잔고 조회"""
    try:
        balances = upbit.get_balances()
        for b in balances:
            if b['currency'] == ticker:
                if b['balance'] is not None:
                    return float(b['balance'])
                else:
                    return 0
    except Exception as e:
        print(f"Error in get_balance: {e}")
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    try:
        orderbook = pyupbit.get_orderbook(ticker=ticker)
        if orderbook and "orderbook_units" in orderbook:
            return orderbook["orderbook_units"][0]["ask_price"]
        else:
            print(f"Failed to get orderbook for {ticker}")
            return None
    except Exception as e:
        print(f"Error in get_current_price: {e}")
        return None

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        if start_time is None:
            continue  # 데이터를 가져오지 못했으면 다음 루프 시도

        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5)
            current_price = get_current_price("KRW-BTC")
            
            if target_price is None or current_price is None:
                continue  # 데이터를 가져오지 못했으면 다음 루프 시도

            if 83125000 < current_price < 83500000:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
            elif 84787500 < current_price:
                btc = get_balance("BTC")
                if btc > 0.00008:
                    upbit.sell_market_order("KRW-BTC", btc*0.9995)
        
        time.sleep(1)
    
    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(1)
