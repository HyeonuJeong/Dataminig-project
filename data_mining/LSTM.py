import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import LSTM
import os


def make_dataset(data, label, window_size=20):
    feature_list = []
    label_list = []
    for i in range(len(data) - window_size):
        feature_list.append(np.array(data.iloc[i:i+window_size]))
        label_list.append(np.array(label.iloc[i+window_size]))
    return np.array(feature_list), np.array(label_list)


def long_short_term_memory(fruit_name):
    global df
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    df = pd.read_csv('./csv/test_' + fruit_name + '.csv', thousands=',')

    df.sort_index(ascending=False).reset_index(drop=True)
    scaler = MinMaxScaler()

    if fruit_name == 'apple':
        scale_cols = ['temp', 'temp_y', 'temp_yy', 'pptn', 'pptn_y', 'pptn_yy',
                      'apple_price', 'price_y', 'price_yy', 'minwage', 'weeknum']
    elif fruit_name == 'pear':
        scale_cols = ['temp', 'temp_y', 'temp_yy', 'pptn', 'pptn_y', 'pptn_yy',
                      'pear_price', 'price_y', 'price_yy', 'minwage', 'weeknum']

    df_scaled = scaler.fit_transform(df[scale_cols])
    df_scaled = pd.DataFrame(df_scaled)
    df_scaled.columns = scale_cols

    # print(df_scaled.describe())

    TEST_SIZE = 200
    WINDOW_SIZE = 20

    train = df_scaled[:-TEST_SIZE]
    test = df_scaled[-TEST_SIZE:]

    # dataset 생성

    feature_cols = ['temp', 'temp_y', 'temp_yy', 'pptn', 'pptn_y', 'pptn_yy', 'price_y', 'price_yy', 'minwage',
                    'weeknum']

    if fruit_name == 'apple':
        label_cols = ['apple_price']
    elif fruit_name == 'pear':
        label_cols = ['pear_price']

    train_feature = train[feature_cols]
    train_label = train[label_cols]

    # train dataset
    train_feature, train_label = make_dataset(train_feature, train_label, 20)

    # train, validation set 생성
    from sklearn.model_selection import train_test_split
    x_train, x_valid, y_train, y_valid = train_test_split(train_feature, train_label, test_size=0.2)

    test_feature = test[feature_cols]
    test_label = test[label_cols]

    # test dataset (실제 예측 해볼 데이터)
    test_feature, test_label = make_dataset(test_feature, test_label, 20)

    # LSTM 모델생성
    model = Sequential()
    model.add(LSTM(16,
                   input_shape=(train_feature.shape[1], train_feature.shape[2]),
                   activation='relu',
                   return_sequences=False)
              )
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    early_stop = EarlyStopping(monitor='val_loss', patience=5)

    model_path = 'ML/model'
    filename = os.path.join(model_path, 'tmp_checkpoint.h5')
    checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=0, save_best_only=True, mode='auto')

    # 모델의 실행
    history = model.fit(x_train, y_train, epochs=200, batch_size=16, validation_data=(x_valid, y_valid),
                        callbacks=[early_stop, checkpoint], verbose=0)
    # verbose 0:진행표시x, 1:표시o

    print("\n" + fruit_name + " Test Accuracy: %.4f" % (model.evaluate(x_valid, y_valid)))
