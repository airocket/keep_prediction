import psycopg2
import pandas as pd
import pandas.io.sql as psql
from sklearn import preprocessing
import numpy as np
from tensorflow.keras.models import load_model
from utils_load_data.dbinit import update_predict

def get_data():
    conn = psycopg2.connect(database="keep_data", user="postgres", password="postgres", host="localhost", port="5432")
    df = psql.read_sql("Select * from markets_data", conn)
    conn.close()
    return df

def get_predict(df):
    history_points = 10
    data = df.copy()
    del data['time']
    data = data.reset_index()
    data = data.drop('index', axis=1)
    data_normaliser = preprocessing.MinMaxScaler()
    data_normalised = data_normaliser.fit_transform(data)
    ohlcv_histories_normalised = np.array([data_normalised[i: i + history_points].copy() for i in range(len(data_normalised) - history_points)])
    next_day_open_values_normalised = np.array([data_normalised[:,1][i + history_points].copy() for i in range(len(data_normalised) - history_points)])
    next_day_open_values_normalised = np.expand_dims(next_day_open_values_normalised, -1)
    next_day_open_values = np.array([data.loc[:, "close_b"][i + history_points].copy() for i in range(len(data) - history_points)])
    next_day_open_values = np.expand_dims(next_day_open_values, -1)
    y_normaliser = preprocessing.MinMaxScaler()
    y_normaliser.fit(next_day_open_values)

    model = load_model("models\keep_predit_lstm.h5")
    predicted = model.predict(ohlcv_histories_normalised[-1:])
    predicted = y_normaliser.inverse_transform(predicted)
    predicted_lstm_value = predicted[0][0].copy()
    predicted_time = df['time'][-1:].values[0].copy() + pd.Timedelta('1 days')

    del df['time']
    data_unsc = df.values
    data = df.values
    #data_norm = data
    data_normaliser = preprocessing.MinMaxScaler()
    data_norm = data_normaliser.fit_transform(data)
    history_points = 30
    pred_candel = 1
    ohlcv_histories = np.array([data_norm[i:i + history_points].copy() for i in range(len(data_norm) - history_points-pred_candel)])
    next_day_open_values = np.array([data_norm[:, 2][i + history_points+pred_candel].copy() for i in range(len(data_norm) - history_points-pred_candel)])
    next_day_open_values = np.expand_dims(next_day_open_values, -1)

    next_day_open_values_unsc = np.array([data_unsc[:, 2][i + history_points+pred_candel].copy() for i in range(len(data_unsc) - history_points-pred_candel)])
    next_day_open_values_unsc = np.expand_dims(next_day_open_values_unsc, -1)

    y_normaliser = preprocessing.MinMaxScaler()
    y_normaliser.fit(next_day_open_values_unsc)
    ohlcv_histories = np.reshape(ohlcv_histories,(ohlcv_histories.shape[0],ohlcv_histories.shape[1]*ohlcv_histories.shape[2],1))
    ohlcv_histories = np.reshape(ohlcv_histories,(ohlcv_histories.shape[0],ohlcv_histories.shape[1]*ohlcv_histories.shape[2]))

    model = load_model("models\keep_predit_simple.h5")
    predicted = model.predict(ohlcv_histories[-1:])
    predicted = y_normaliser.inverse_transform(predicted)
    predicted_simple_value = predicted[0][0].copy()
    return predicted_time, predicted_lstm_value, predicted_simple_value


def run_predict():
    data = get_data()
    predicted_time, predicted_lstm_value, predicted_simple_value = get_predict(data)
    update_predict(predicted_time, predicted_lstm_value, predicted_simple_value)


