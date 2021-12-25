import pandas as pd
import numpy as np


def data_processing():
    apple = pd.read_csv('./csv/apple.csv', encoding='UTF-8')
    pear = pd.read_csv('./csv/pear.csv', encoding='UTF-8')
    temp = pd.read_csv('./csv/temp.csv', encoding='UTF-8')
    pptn = pd.read_csv('./csv/pptn.csv', encoding='UTF-8')
    wage = pd.read_csv('./csv/wage.csv', encoding='UTF-8')
    holiday = pd.read_csv('./csv/holiday.csv', encoding='UTF-8')
    week = pd.read_csv('./csv/week.csv', encoding='UTF-8')

    # ------ 사과 ------
    data1 = pd.merge(temp, pptn, how='outer', on='date')
    data2 = pd.merge(data1, apple, how='outer', on='date')

    data2 = data2.fillna(method='ffill', limit=14)

    data2["price_y"] = data2["apple_price"].shift(1)
    data2["price_yy"] = data2["price_y"].shift(1)

    data2 = data2.dropna(how='any')

    data3 = pd.merge(data2, wage, how='outer', on='date')
    data4 = pd.merge(data3, holiday, how='outer', on='date')
    data5 = pd.merge(data4, week, how='outer', on='date')

    data5.loc[~((data5.dateName == '설날') | (data5.dateName == '추석')), 'dateName'] = np.NaN
    data5 = data5.fillna(method='bfill', limit=13)
    data5.loc[(data5.dateName == '설날') | (data5.dateName == '추석'), 'weeknum'] = 7
    data5 = data5.drop(['dateName'], axis=1)

    data5 = data5.dropna(how='any')

    # 사과 minwage 정규화 (0~1)
    mmn_a = data5.iloc[:, [10]]
    mmn_a = (mmn_a - mmn_a.min()) / (mmn_a.max() - mmn_a.min())
    data5['minwage'] = mmn_a['minwage']

    data5.to_csv('./csv/test_apple.csv', index=False, encoding='UTF-8')

    # ------ 배 ------
    data6 = pd.merge(temp, pptn, how='outer', on='date')
    data7 = pd.merge(data6, pear, how='outer', on='date')

    data7 = data7.fillna(method='ffill', limit=14)

    data7["price_y"] = data7["pear_price"].shift(1)
    data7["price_yy"] = data7["price_y"].shift(1)

    data7 = data7.dropna(how='any')

    data8 = pd.merge(data7, wage, how='outer', on='date')
    data9 = pd.merge(data8, holiday, how='outer', on='date')
    data10 = pd.merge(data9, week, how='outer', on='date')

    data10.loc[~((data10.dateName == '설날') | (data10.dateName == '추석')), 'dateName'] = np.NaN
    data10 = data10.fillna(method='bfill', limit=13)
    data10.loc[(data10.dateName == '설날') | (data10.dateName == '추석'), 'weeknum'] = 7
    data10 = data10.drop(['dateName'], axis=1)
    data10 = data10.dropna(how='any')

    # ------ 배 minwage 정규화 ------
    mmn_p = data10.iloc[:, [10]]
    mmn_p = (mmn_p - mmn_p.min()) / (mmn_p.max() - mmn_p.min())
    data10['minwage'] = mmn_p['minwage']

    data10.to_csv('./csv/test_pear.csv', index=False, encoding='UTF-8')