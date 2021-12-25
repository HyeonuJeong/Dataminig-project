import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split


def support_vector_machine(fruit_name):
    df = pd.read_csv('./csv/test_' + fruit_name + '.csv', encoding='UTF-8')
    # apple_price 및 price_y를 각각 리스트로 만듦
    if fruit_name == 'apple':
        fruit_prices = [int(each_price.replace(',', '')) for each_price in list(df['apple_price'])]
    elif fruit_name == 'pear':
        fruit_prices = [int(each_price.replace(',', '')) for each_price in list(df['pear_price'])]

    fruit_yesterday_prices = [int(each_price.replace(',', '')) for each_price in list(df['price_y'])]

    # apple_prices 변동성을 리스트로 만듦
    fruit_prices_volatility = [today - yesterday
                               for today, yesterday
                               in zip(fruit_prices, fruit_yesterday_prices)]

    # for today, yesterday in zip(list(apple_csv['apple_price']), list(apple_csv['price_y'])):
    # apple_prices_volatility.append(int(str(today).replace(',', '')) - int(str(yesterday).replace(',', '')))

    # 가격이 하락하는지 확인하는 리스트
    fruit_prices_lower = [1 if each_price < 0 else 0
                          for each_price in fruit_prices_volatility]
    # 가격이 상승하는지 확인하는 리스트
    fruit_prices_higher = [1 if each_price > 0 else 0
                           for each_price in fruit_prices_volatility]

    # 가격 상승과 하락에 대한 정보가 전부 저장된 리스트
    fruit_prices_total = list()
    for lower, higher in zip(fruit_prices_lower, fruit_prices_higher):
        if lower == higher == 0:
            fruit_prices_total.append(0)
        elif lower == 1:
            fruit_prices_total.append(-1)
        elif higher == 1:
            fruit_prices_total.append(1)

    # for each_price in apple_prices_volatility:
    #     if each_price < 0:
    #         apple_prices_lower.append(1)
    #     else:
    #         apple_prices_lower.append(0)

    # X축 데이터에 온도, 어제 온도, 그제 온도, 강수량, 어제 강수량, 그제 강수량, 최저임금, 요일 정보를 넣음
    X_temp = [
        [float(temp), float(temp_y), float(temp_yy), float(pptn), float(pptn_y), float(pptn_yy), float(minwage),
         float(weeknum)]
        for temp, temp_y, temp_yy, pptn, pptn_y, pptn_yy, minwage, weeknum
        in zip(df['temp'], df['temp_y'], df['temp_yy'],
               df['pptn'], df['pptn_y'], df['pptn_yy'],
               df['minwage'], df['weeknum'])]

    y_lower = fruit_prices_lower
    y_higher = fruit_prices_higher
    y_total = fruit_prices_total

    # train 및 test 데이터를 나눔
    X_lower_train, X_lower_test, y_lower_train, y_lower_test = train_test_split(X_temp, y_lower, test_size=0.3,
                                                                                random_state=0)
    X_higher_train, X_higher_test, y_higher_train, y_higher_test = train_test_split(X_temp, y_higher, test_size=0.3,
                                                                                    random_state=0)

    X_train, X_test, y_train, y_test = train_test_split(X_temp, y_total, test_size=0.3, random_state=0)

    # SVM을 이용해 classifier를 만듬
    clf_lower = SVC(kernel="linear", C=0.5)
    clf_lower.fit(X_lower_train, y_lower_train)
    clf_higher = SVC(kernel="linear", C=0.5)
    clf_higher.fit(X_higher_train, y_higher_train)

    clf_total = SVC(kernel="linear", C=0.5)
    clf_total.fit(X_train, y_train)

    # 데이터 예측
    y_pred_lower = clf_lower.predict(X_lower_test)
    y_pred_higher = clf_higher.predict(X_higher_test)

    y_pred = clf_total.predict(X_test)

    # 데이터 예측 정확도 결과
    f1_lower = f1_score(y_lower_test, y_pred_lower, average='micro')
    f1_higher = f1_score(y_higher_test, y_pred_higher, average='micro')

    f1_total = f1_score(y_test, y_pred, average='micro')

    # print(y_lower_test)
    # print(y_pred_lower)

    print("SVM (" + fruit_name + ") F1 Score :", str(f1_total))

    # 미래 사과, 배 가격 데이터 예측해보기 예시
    # pred_y_temp = clf_total.predict([["36", "38", "39", "300", "150", "100", 1.1, 3]])
    # print(pred_y_temp)

