import pandas as pd


def data_processing():
    pptn = pd.read_csv('./csv/original/pptn.csv', encoding="UTF-8")
    all_data = []

    # 필요 없는 데이터 삭제
    pptn = pptn.drop(['\t지점번호'], axis=1)
    pptn = pptn.drop(['지점명'], axis=1)
    pptn = pptn.drop(['1시간최다강수량(mm)'], axis=1)
    pptn = pptn.drop(['1시간최다강수량시각'], axis=1)

    # 일시 -> 날짜로 변경
    pptn = pptn.rename({'일시': 'date'}, axis='columns')
    pptn = pptn.rename({'강수량(mm)': 'pptn'}, axis='columns')
    pptn = pptn.fillna(0)
    pptn.to_csv('./csv/pptn.csv', index=False, encoding='UTF-8')

    pptn_y = pd.read_csv('./csv/pptn.csv', encoding='UTF-8')
    pptn_y = pptn_y.rename({'pptn': 'pptn_y'},axis='columns')
    pptn_y = pptn_y.drop(['date'],axis=1)
    pptn_y = pptn_y.shift(periods=1,axis=0)

    pptn_yy = pd.read_csv('./csv/pptn.csv', encoding='UTF-8')
    pptn_yy = pptn_yy.rename({'pptn': 'pptn_yy'}, axis='columns')
    pptn_yy = pptn_yy.drop(['date'], axis=1)
    pptn_yy = pptn_yy.shift(periods=2, axis=0)

    pptn_merge = pd.concat([pptn, pptn_y, pptn_yy], axis=1)
    pptn_merge.to_csv('./csv/pptn.csv', index=False, encoding='UTF-8')