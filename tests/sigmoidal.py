from statistics import *
import numpy as np
import matplotlib.pyplot as plt
import math

TCP_SYN_FILE = 'tcp_syn.dat'

def read_file(filename):
    arr = []
    with open(filename, 'r') as f:
        for val in f.read().split():
            arr.append(int(val))
    return arr

def simple_exp_smoothing(series, alpha):
    result = [series[0]]
    for n in range(1, len(series)):
        result.append(alpha*series[n] + (1-alpha)*result[n-1])
    return result[-1]

def get_biggest_increase_in_window(series):
    inc = 0
    for i in range(len(series)):
        if i < len(series)-1:
            if series[i+1] - series[i] > inc:
                inc = series[i+1] - series[i]
    return inc  

def sigmoid(a, b, x):
    try:
        return 1./(1+math.exp(-1.*a*(x-b)))
    except:
        return 0

def sigmoidal():
    res = []
    st = traffic[4320:-1440]
    window_size = 21
    season_length = 1440
    alpha = 0.9
    sigmoidal_threshold = 0.9
    elements = []
    sigm_res = []
    for i in range(season_length):
        st = traffic[4320:-2880+i]
        differences_increase = []
        if len(st) > season_length:
            start_item = len(st) % season_length
            end_item = len(st) - 1
            while True:
                if start_item-int(window_size/2) < 0:
                    differences_increase.append(get_biggest_increase_in_window(st[0:start_item+int(window_size/2)]))
                else:
                    differences_increase.append(get_biggest_increase_in_window(st[start_item-int(window_size/2):start_item+int(window_size/2)]))
                start_item += season_length
                if start_item > end_item:
                    sigm = stdev(st[-1440:])
                    elements.append(st[-1] + simple_exp_smoothing(differences_increase, alpha))
                    sigm_res.append(sigmoid(1/sigm, st[-1] + simple_exp_smoothing(differences_increase, 0.9), traffic[-2880+i+1]))
                    if sigm_res[-1] > sigmoidal_threshold:
                        print("ALERT")
                    print("zmierzone = " + str(traffic[-2880+i+1]) + "    |    prognoza = " + str(elements[-1]) + "    |     sigmoidal = " + str(sigm_res[-1]))
                    break
                    
traffic = read_file(TCP_SYN_FILE)
sigmoidal()
