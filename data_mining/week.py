import pandas
import pandas as pd


def data_processing():
    dt_index = pandas.date_range(start='20160101', end='20181231')
    dt_list = dt_index.strftime("%Y-%m-%d").tolist()
    dt_week = dt_index.weekday.tolist()
    df = pd.DataFrame(dt_list, columns=['날짜'])
    df1 = pd.DataFrame(dt_week, columns=['weeknum'])
    df2 = pd.concat([df, df1], axis=1)
    df2 = df2.rename({'날짜': 'date'}, axis='columns')
    df2.to_csv('./csv/week.csv', index=False, header=True, encoding='UTF-8')
