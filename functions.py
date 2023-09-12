import numpy
from binance.spot import Spot


def get_client(binance_api):
    # print(binance_api)
    spot_client = Spot(api_key=binance_api.keys(), api_secret=binance_api.keys())
    return spot_client


def get_user_prices(spot_client, tickers):
    ticker_prices = {}  # Инициализируем пустой словарь для хранения цен

    for ticker in tickers:
        ticker_info = spot_client.ticker_price(symbol=ticker)
        symbol = ticker_info['symbol']
        price = ticker_info['price']
        ticker_prices[symbol] = price  # Сохраняем символ и цену в словарь

    # Выводим словарь с символом тикера в качестве ключа и ценой в качестве значения
    for symbol, price in ticker_prices.items():
        pass
        # print(f"{symbol}:{float(price)}")
    return ticker_prices


def get_bidask_info(spot_client, ticker):
    bidask_info = spot_client.depth(symbol=ticker)
    # print(bidask_info)
    return bidask_info


def depth_and_weights(client, tickers):
    bidask_info = get_bidask_info(client, tickers[0])
    # print(bidask_info)
    last_update_id = bidask_info['lastUpdateId']
    # print(price_avg)
    # print(last_update_id)
    bids_prices = numpy.array(bidask_info['bids'])
    asks_prices = numpy.array(bidask_info['asks'])
    # TODO попробовать опредедить текущую цену через array
    bids_sum = 0
    bids_volumes_summ = 0

    for bid in bids_prices:
        price = float(bid[0])
    volume = float(bid[1])

    # Вычисляем взвешенную сумму и сумму объемов
    summ = price * volume
    bids_sum += summ
    bids_volumes_summ += volume

    # Вычисляем взвешенный средний объем
    bids_result = bids_sum / bids_volumes_summ

    # print('Total Volume Bids:', bids_volumes_summ, '\n',
    #       'Weighted Average Volume Bids:', bids_result, '\n', )

    asks_sum = 0
    asks_volumes_summ = 0

    for ask in asks_prices:
        price = float(ask[0])
    volume = float(ask[1])

    # Вычисляем взвешенную сумму и сумму объемов
    summ = price * volume
    asks_sum += summ
    asks_volumes_summ += volume

    # Вычисляем взвешенный средний объем
    asks_result = asks_sum / asks_volumes_summ

    # print('Total Volume Asks:', asks_volumes_summ, '\n',
    #       'Weighted Average Volume Asks:', asks_result)

    return (bids_volumes_summ,
            bids_result,
            asks_volumes_summ,
            asks_result,
            last_update_id)


def create_dynamic_plot(*args, y_data):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots()
    x_values = [*args]
    y_values = []

    line, = ax.plot(x_values, y_values, label=None, marker='o')
    ax.legend()

    def update(frame):
        x_values.append(x_data[frame])
        y_values.append(y_data[frame])
        line.set_data(x_values, y_values)
        ax.relim()
        ax.autoscale_view()
        return line,
    num_frames = len(str(x_data))
    ani = FuncAnimation(fig, update, frames=num_frames, blit=True)

    plt.show()
