from binance_api import Binance
import secret
import time



app_time = time.time()

btc_start = 1


bot = Binance(
    API_KEY=secret.key,
    API_SECRET=secret.secret
)
BTCUSDT = bot.tickerPrice(symbol='BTCUSDT')['price']


pt = bot.tickerPrice()

USDT_pair = list(filter(lambda x: 'USDT' in x['symbol'] and x['symbol'].index('USDT') > 0, pt))
BTC_pair = list(filter(lambda x: 'BTC' in x['symbol'] and x['symbol'].index('BTC') > 0, pt))


positivDivArr = []
for p in BTC_pair:
    coin = p['symbol'].replace('BTC', '')
    price = p['price']
    try:
        usd_price = list(filter(lambda x: x['symbol'].replace("USDT", "") == coin, USDT_pair))[0]
        btc_coin_items = btc_start / float(p['price'])
        usd_cost = float(usd_price['price'])*btc_coin_items
        btc_cost = usd_cost/float(BTCUSDT)

        div = btc_cost - btc_start
        if(div>0.01):
            print(div)
            row = {'coin':coin, 'price':price, 'btc_coin_items':btc_coin_items, 'usd_cost':usd_cost, 'btc_cost':btc_cost, 'div':div}
            positivDivArr.append(row)
            print (coin, price, 'btc /', btc_coin_items, 'шт / ', usd_cost, '$ /', btc_cost)
    except:
        continue
