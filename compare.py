import sys
import pathlib
import numpy as np
import matplotlib.pyplot as plt

import alpha_vantage
import plot_style


def compare(stock_symbol, benchmark_symbol, interval='MONTHLY', adjusted=True):
    stock_data = alpha_vantage.get_stock_price_history(
        stock_symbol, interval, adjusted)

    benchmark_data = alpha_vantage.get_stock_price_history(
        benchmark_symbol, interval, adjusted)

    stock_data = {k: v for (k, v) in stock_data.items()
                  if k in benchmark_data.keys()}

    benchmark_data = {
        k: v for (k, v) in benchmark_data.items() if k in stock_data.keys()}

    stock_data = adjust_values(stock_data)
    benchmark_data = adjust_values(benchmark_data)

    plot_style.line()

    plt.plot(list(benchmark_data.keys()), list(benchmark_data.values()), label=benchmark_symbol)
    plt.plot(list(stock_data.keys()), list(stock_data.values()), label=stock_symbol)

    plt.title(f'{stock_symbol} vs {benchmark_symbol} (adjusted)')
    plt.legend()

    pathlib.Path('img/compare').mkdir(parents=True, exist_ok=True)
    plt.savefig(f'img/compare/{stock_symbol}-{benchmark_symbol}.png')
    plt.close()


def adjust_values(data, start=100.0):
    scale_factor = None

    for k, v in sorted(data.items()):
        if scale_factor == None:
            scale_factor = v / start

        data[k] = v / scale_factor

    return data


compare(sys.argv[1], sys.argv[2])
