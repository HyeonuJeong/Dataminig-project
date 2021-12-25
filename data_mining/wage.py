import pandas
import pandas as pd


def data_processing():
    wage = pd.read_csv('./csv/original/wage.csv', encoding="UTF-8")
    wage = wage.iloc[3:6, [1, 2]]
    wage = wage.reset_index()
    wage = wage.drop('index', axis=1)
    dt_index = pandas.date_range(start='20160101', end='20181231')
    dt_list = dt_index.strftime("%Y-%m-%d").tolist()
    df = pd.DataFrame(dt_list, columns=['날짜'])

    def minwage(row):
        if row.split('-')[0] == '2016':
            return wage.loc[2][1]
        elif row.split('-')[0] == '2017':
            return wage.loc[1][1]
        else:
            return wage.loc[0][1]

    df['minwage'] = df.날짜.apply(minwage)
    df = df.rename({'날짜': 'date'}, axis='columns')

    df.to_csv('./csv/wage.csv', index=False, header=True, encoding='UTF-8')

