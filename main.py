import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter
import numpy as np

def get_stock_data(symbol):
    url = "https://www.alphavantage.co/query"
    function = "TIME_SERIES_DAILY_ADJUSTED"
    apikey = "Z4VX380VZ3MXOFCO"
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": apikey,
        "outputsize": "compact"
    }

    response = requests.get(url, params=params)
    data = json.loads(response.text)["Time Series (Daily)"]

    stock_data = []
    for date, values in data.items():
        close = float(values["4. close"])
        stock_data.append((datetime.strptime(date, "%Y-%m-%d"), close))

    return stock_data


def save_stock_data_to_file(symbol):
    stock_data = get_stock_data(symbol)
    with open(f"{symbol}.json", "w") as f:
        json.dump(stock_data, f, default=str)


def plot_stock_data_from_file(symbol, start_date=None, end_date=None):
    with open(f"{symbol}.json", "r") as f:
        stock_data = json.load(f)

    dates = [data[0] for data in stock_data]
    prices = [data[1] for data in stock_data]

    # konwersja dat na wartości numeryczne
    dates_num = date2num(dates)

    # zastosowanie wypełnienia pod wykresem
    plt.fill_between(dates_num, prices, color='lightgray')

    # inicjowanie zmiennych start_date_num i end_date_num przed blokiem if
    start_date_num = None
    end_date_num = None

    # konwersja ceny na tablicę numpy
    prices_np = np.array(prices)

    # pomnożenie ceny przez 1.5
    prices_np *= 1.5

    # jeśli podano daty początkowe i końcowe, to ograniczamy wyświetlany zakres danych
    if start_date is not None and end_date is not None:
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        start_date_num = date2num(start_date)
        end_date_num = date2num(end_date)
        plt.xlim(start_date_num, end_date_num)

    # sprawdzanie, czy zmienne start_date_num i end_date_num mają przypisane wartości
    if start_date_num is not None and end_date_num is not None:
        # Rysowanie wykresu z ograniczonym zakresem dat
        plt.plot(dates_num, prices * 1.5)
        plt.fill_between(dates_num, prices * 1.5, color='lightgray')
        plt.xlim(start_date_num, end_date_num)
    else:
        # Rysowanie wykresu z pełnym zakresem dat
        plt.plot(dates_num, prices_np)
        plt.fill_between(dates_num, prices_np, color='lightgray')

    # ustawienie formatu osi x na "rok-miesiąc-dzień"
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

    # ustawienie stylu wykresu
    plt.style.use('dark_background')

    # ustawienie koloru tła
    plt.gcf().set_facecolor('#121212')

    # ustawienie koloru tekstu na biały
    plt.rcParams['text.color'] = 'white'

    # ustawienie tytułu wykresu
    title = plt.title(f"{symbol} Stock Prices")
    title.set_color('white')

    # ustawienie koloru linii i etykiet dla osi x i y na biały
    plt.plot(dates_num, prices_np, color='white')
    plt.gca().xaxis.label.set_color('white')
    plt.gca().yaxis.label.set_color('white')

    # ustawienie etykiet osi x i y oraz tytułu wykresu
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"{symbol} Stock Prices")

    # wyświetlenie wykresu
    plt.show()


def main():
    symbol = "AAPL"
    save_stock_data_to_file(symbol)

    # przykładowe daty początkowe i końcowe
    start_date = "2020-01-01 00:00:00"
    end_date = "2022-12-31"

    plot_stock_data_from_file(symbol, start_date="2020-01-01")


if __name__ == '__main__':
    main()
