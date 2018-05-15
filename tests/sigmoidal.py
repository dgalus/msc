from statistics import *
from sklearn.cluster import KMeans
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import math

TCP_SYN_FILE = 'tcp_syn_trunc.dat'

def read_file(filename):
    arr = []
    with open(filename, 'r') as f:
        for val in f.read().split():
            arr.append(int(val))
    return arr

traffic = read_file(TCP_SYN_FILE)

def initial_trend(series, season_length):
    s = 0.0
    for i in range(season_length):
        s += float(series[i+season_length] - series[i])/season_length
    return s/season_length

def initial_seasonal_components(series, season_length):
    seasonals = {}
    season_averages = []
    n_seasons = int(len(series)/season_length)
    for j in range(n_seasons):
        season_averages.append(sum(series[season_length*j:season_length*j+season_length])/float(season_length))
    for i in range(season_length):
        sum_of_vals_avg = 0.0
        for j in range(n_seasons):
            sum_of_vals_avg += series[season_length*j+i]-season_averages[j]
        seasonals[i] = sum_of_vals_avg/n_seasons
    return seasonals

def holt_winters_forecast(series, season_length, alpha, beta, gamma, n_preds):
    result = []
    seasonals = initial_seasonal_components(series, season_length)
    for i in range(len(series) + n_preds):
        if i == 0:
            smooth = series[0]
            trend = initial_trend(series, season_length)
            result.append(series[0])
            continue
        if i >= len(series):
            m = i-len(series)+1
            result.append((smooth+m*trend) + seasonals[i%season_length])
        else:
            val = series[i]
            last_smooth = smooth
            smooth = alpha*(val-seasonals[i%season_length]) + (1-alpha)*(smooth+trend)
            trend = beta*(smooth-last_smooth)+(1-beta)*trend
            seasonals[i%season_length] = gamma*(val-smooth)+(1-gamma)*seasonals[i%season_length]
            result.append(smooth+trend+seasonals[i%season_length])
    return result


def holt_long():
    aver = []
    st = traffic[4320:-1440]
    m = mean(st)
    res = holt_winters_forecast(st, 1440, 0.99, 0, 0.1, 1440)
    aver = res[-1440:]
    aver = res[-1440:]
    l_ci = []
    h_ci = []
    for i in aver:
        l_ci.append(i - m)
        h_ci.append(i + m)
    _, ax = plt.subplots()
    ax.plot(range(0, 1440), traffic[-1440:], linewidth=0.7, color='#df9292', alpha=1, label="Rzeczywisty ruch")
    ax.plot(range(0, 1440), aver, linewidth=0.7, color = '#539caf', alpha=1, label="Prognozowany ruch")
    ax.fill_between(range(0, 1440), l_ci, h_ci, color = '#539caf', alpha = 0.4, label="Przedział ufności")
    ax.set_title("Prognozowanie Holta-Wintersa dla TCP SYN")
    ax.set_xlabel("Czas")
    ax.set_ylabel("Ilość segmentów TCP SYN")
    ax.legend(loc='best')
    plt.savefig('hw.svg', format="svg")
    plt.clf()