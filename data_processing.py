import concurrent.futures
from glob import glob
from math import sqrt
import re
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from bioinfokit.analys import stat

def read_file(filename):
    key = re.findall(r'hex(.*)\.txt', filename)[0]
    with open(filename) as file:
        txt = file.read().splitlines()[2:]
    arr = []
    for t in txt:
        t = t.split('|')[1]
        t = re.sub(r'\s+', ' ', t).strip()
        row = t.split(' ')
        row = list(map(int, row))
        arr.append(row)
    arr = np.array(arr)
    arr = arr.reshape(-1)[1:]
    mean = np.mean(arr)
    std = np.std(arr)
    _max = np.max(arr)
    # _min = np.min(arr)
    # zscore = (arr - mean) / std
    return _max
    # return {'std': std, 'mean': mean, 'max': _max, 'z': zscore}

def calculate(arr_max):
    mean_max = np.mean(arr_max)
    std_max = np.std(arr_max)
    return mean_max, std_max
def prob(counter):
    s = counter.total()
    for c in counter:
        print(f'{c}: {counter[c]}, prob: {counter[c]/s}')
    print('----------------')
def ci(arr):
    n = arr.shape[0]
    ta = stats.t.ppf(1-0.025, n-1)
    sqrt_n = sqrt(n)
    mean = np.mean(arr)
    sd_unbias = np.sum(arr - mean) / (n-1)
    lower = mean - (ta*(sd_unbias / sqrt_n))
    upper = mean - (ta*(sd_unbias / sqrt_n))
    print(f'[{lower}, {upper}]')
if __name__ == '__main__':
    # 1 hex
    addP = glob('ddt_addP2_32/addP_hex_*.txt')
    twokey = glob('ddt_twokey2_32/twokey_hex_*.txt')
    ori = glob('ddt_ori2_32/ori_hex_*.txt')

    # 2 hex
    # addP = glob('ddt_addP2/ddt_addP_2_hex(*).txt')
    # twokey = glob('ddt_twokey2/ddt_twokey_2_hex(*).txt')
    # ori = glob('ddt_ori2/ddt_ori_2_hex(*).txt')
    # twokey_arr = []
    # addP_arr = []
    # ori_arr = []
    arr = np.zeros((3, len(twokey)), dtype=np.uint16)
    for i, (val_twokey, val_addP, val_ori) in enumerate(zip(twokey, addP, ori)):
        print(f'current index: {i}')
        arr[0, i] = read_file(val_twokey)
        arr[1, i] = read_file(val_addP)
        arr[2, i] = read_file(val_ori)
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     for result in executor.map(read_file, twokey):
    #         twokey_arr.append(result)
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     for result in executor.map(read_file, addP):
    #         addP_arr.append(result)
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     for result in executor.map(read_file, ori):
    #         ori_arr.append(result)
    # # calculate addP and twokey
    from collections import Counter
    import pandas as pd
    res = stat()
    print(f'addP:', calculate(arr[1]))
    df = pd.DataFrame(pd.Series(arr[1], name='data'))
    res.ttest(df, test_type=1, res='data', mu=np.mean(df.to_numpy()))
    print(res.summary)
    print('+'*30)

    print(f'twokey:', calculate(arr[0]))
    df = pd.DataFrame(pd.Series(arr[0], name='data'))
    res.ttest(df, test_type=1, res='data', mu=np.mean(df.to_numpy()))
    print(res.summary)
    print('+'*30)
    print(f'ori:', calculate(arr[2]))
    df = pd.DataFrame(pd.Series(arr[2], name='data'))
    res.ttest(df, test_type=1, res='data', mu=np.mean(df.to_numpy()))
    print(res.summary)

    print (Counter(arr[1]))
    print (Counter(arr[0]))
    print (Counter(arr[2]))


    # print(f'addP:', )
    # print('--------'*10)
    # print(f'twokey:', np.mean(twokey_arr))
    