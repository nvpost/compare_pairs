from binance_api import Binance
import secret
import requests
import time

# from sql import sql


app_time = time.time()

btc = 0.1
usdt = 1000

bot = Binance(
    API_KEY=secret.key,
    API_SECRET=secret.secret
)
BTCUSDT = bot.tickerPrice(symbol='BTCUSDT')['price']

originBTCUSDT_Sum = usdt/float(BTCUSDT)


print("на", usdt, 'usdt можно купить', originBTCUSDT_Sum, 'BTC')


pt = bot.tickerPrice()

# & x['symbol'].index('USDT') > 0
USDT_pair = list(filter(lambda x: 'USDT' in x['symbol'] and x['symbol'].index('USDT') > 0, pt))
BTC_pair = list(filter(lambda x: 'BTC' in x['symbol'] and x['symbol'].index('BTC') > 0, pt))

usd_suppose = [];
for pair in USDT_pair:
    cp = usdt/float(pair['price'])
    coin = pair['symbol'].replace('USDT', '')
    usd_suppose.append({'coin': coin, 'sum':cp})
    # print("на", usdt, 'usdt можно купить', cp, coin)

btc_suppose = [];
for pair in BTC_pair:
    cp = originBTCUSDT_Sum/float(pair['price'])
    coin = pair['symbol'].replace('BTC', '')
    btc_suppose.append({'coin': coin, 'sum':cp})
    # print("на", originBTCUSDT_Sum, 'BTC можно купить', cp, coin)




# print(btc_suppose)

compareBTC_USDT = []
for bs in btc_suppose:
    btc_coin = bs['coin']
    # print(btc_coin)
    usd_row = list(filter(lambda x: x['coin'] == btc_coin, usd_suppose))
    if len(usd_row)>0:
        compareBTC_USDT.append({'btc':bs, 'usdt':usd_row[0]})



def diffInUSDTfoo(coin):
    pair_price = list(filter(lambda x: x['symbol'] == coin+"USDT", pt))
    usdt_diff = float(pair_price[0]['price'])
    return usdt_diff


difference_BTC_pairs = []
for pair in compareBTC_USDT:

    btc_sum = float(pair['btc']['sum'])
    usdt_sum = float(pair['usdt']['sum'])

    if btc_sum>usdt_sum:
        diff = btc_sum-usdt_sum
        diffInUSDT = diffInUSDTfoo(pair['btc']['coin'])

        margin = diffInUSDT*btc_sum - usdt


        row = {'coin': pair['btc']['coin'],
               'btc_sum':btc_sum,
               'ustd_sum':usdt_sum,
               'diff': diff,
               'diffInUSDT': diffInUSDT*diff,
               'sellForUSDT': diffInUSDT*btc_sum,
               'margin': margin
               }
        # print(row)
        difference_BTC_pairs.append(row)

# Разница в USDT* начальный капитал


for p in difference_BTC_pairs:
    print(p)


app_time = time.time() - app_time
print("Время выполнения:",round(app_time, 2),'s')