import yfinance as yf

with open('kospi.txt') as f:
    lines = [line.strip() for line in f]

lines.pop(0)

for code in lines:
    ticker = yf.Ticker(code + ".ks")
    if (ticker.info['fiftyTwoWeekLowChangePercent'] < 0.05):
        print('symbol : {}, shortName : {}, 52w_low_% : {}'.format(
            ticker.info['symbol'], ticker.info['shortName'], ticker.info['fiftyTwoWeekLowChangePercent']))
