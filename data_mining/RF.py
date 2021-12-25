import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import r2_score


def random_forest(fruit_name):
    df = pd.read_csv('csv/test_' + fruit_name + '.csv', thousands=',', encoding='UTF-8')
    df = df.drop(['date'], axis=1)

    if fruit_name == 'apple':
        feature_columns = list(df.columns.difference(['apple_price']))
        X = df[feature_columns]
        y = df['apple_price']
    elif fruit_name == 'pear':
        feature_columns = list(df.columns.difference(['pear_price']))
        X = df[feature_columns]
        y = df['pear_price']

    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=0)

    clf = RandomForestClassifier(n_estimators=6, random_state=0)
    clf.fit(train_x, train_y)

    predict1 = clf.predict(test_x)

    r2 = r2_score(test_y, predict1)

    print("랜덤 포레스트 (" + fruit_name + ") R2 Score :", str(r2))

#######################################################
