import pandas as pd


def data_processing():
    temp = pd.read_csv('./csv/original/temp.csv', encoding="UTF-8")

    # 필요 없는 데이터 삭제
    temp = temp.drop(['\t\t지점번호'], axis=1)
    temp = temp.drop(['지점명'], axis=1)
    temp = temp.drop(['최고기온(℃)'], axis=1)
    temp = temp.drop(['\t최고기온시각'], axis=1)
    temp = temp.drop(['최저기온(℃)'], axis=1)
    temp = temp.drop(['최저기온시각일교차'], axis=1)
    temp = temp.drop(['Unnamed: 8'], axis=1)

    # 일시 -> 날짜로 변경
    temp = temp.rename({'일시': 'date'}, axis='columns')
    temp = temp.rename({'평균기온(℃)': 'temp'}, axis='columns')

    temp.to_csv('./csv/temp.csv', index=False, encoding='UTF-8')

    temp_y = pd.read_csv('./csv/temp.csv', encoding='UTF-8')
    temp_y = temp_y.rename({'temp': 'temp_y'}, axis='columns')
    temp_y = temp_y.drop(['date'], axis=1)
    temp_y = temp_y.shift(periods=1, axis=0)

    temp_yy = pd.read_csv('./csv/temp.csv', encoding='UTF-8')
    temp_yy = temp_yy.rename({'temp': 'temp_yy'}, axis='columns')
    temp_yy = temp_yy.drop(['date'], axis=1)
    temp_yy = temp_yy.shift(periods=2, axis=0)

    temp_merge = pd.concat([temp, temp_y, temp_yy], axis=1)
    temp_merge.to_csv('./csv/temp.csv', index=False, encoding='UTF-8')
