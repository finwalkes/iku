import streamlit as st
import requests
import pandas as pd
import numpy as np
from glom import glom
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# Function to preprocess the input data
def preprocess_input_data(input_data):
    # Perform any necessary preprocessing here (scaling, encoding, etc.)
    scaler = StandardScaler()
    input_data_scaled = scaler.fit_transform(input_data)
    return input_data_scaled

# Function to make prediction
def predict_air_quality(features):
    # Load your pre-trained LSTM model
    model = load_model('model/psw.h5')  # Load your LSTM model

    # Make prediction
    prediction = model.predict(features)
    return prediction

# Load data from API and process
def load_and_process_data(lat, lon, api_key):
    live_history = f"https://api.weatherbit.io/v2.0/history/airquality?lat={lat}&lon={lon}&key={api_key}"
    response1 = requests.get(live_history)
    df = pd.read_json(response1.text)

    # Proses data
    target_aqi = df["data"]
    spec = {      
        "aqi" : (["aqi"]),
        "pm10" : (["pm10"]),
        "pm25" : (["pm25"]),
        "o3" : (["o3"]),
        "so2" : (["so2"]),
        "no2" : (["no2"]),
        "co" : (["co"]),
        "timestamp_local" : (['timestamp_local'])
    }

    data_json = glom(target_aqi, spec)
    df_aqi = pd.DataFrame.from_dict(data_json)
    df_city = df[["city_name", "lat", "lon"]]
    df_merge = pd.concat([df_city, df_aqi], axis=1, sort=False)
    df_merge['timestamp_local'] = pd.to_datetime(df_merge['timestamp_local'])
    # df_merge.set_index('timestamp_local', inplace=True)
    return df_merge

def calculate_r_squared(actual_values, predicted_values):
    r_squared = r2_score(actual_values, predicted_values)
    return r_squared

# Streamlit UI
st.header('Forcasting Kualitas Udara Menggunakan LSTM')

api_key = "11772efb3a01408c8c0407a8be9ee5d9"

point = st.selectbox(
    "Pilih Kota",
    ("Bandar Lampung","Metro","Pringsewu","Tanggamus","Pesawaran","Lampung Tengah", "Lampung Selatan", "Lampung Timur", "Tulang Bawang", "Mesuji", "Tulang Bawang Barat", "Lampung Utara", "Way Kanan", "Lampung Barat", "Pesisir Barat")
) 
if point == "Bandar Lampung":
    lat = "-5.397217328032725" # Kedaton
    lon = "105.26712874423644" # Kedaton
elif point == "Metro":
    lat = "-5.118338672913152" # Kota Metro
    lon = "105.30878306231706" # Kota Metro
elif point == "Pringsewu":
    lat = "-5.323054251492792" # pringsewu
    lon = "104.92825019949758" # 
elif point == "Tanggamus":
    lat = "-5.425875948289883" # kota agung
    lon = "104.67542683904134" # 
elif point == "Pesawaran":
    lat = "-5.379500773415511" # gedong tataan
    lon = "105.09725924505528" # 
elif point == "Lampung Tengah":
    lat = "-4.788326405280659" # Terbanggi besar
    lon = "105.13390811560652" # 
elif point == "Lampung Selatan":
    lat = "-5.735090704003585" # kalianda
    lon = "105.59342531664616" # 
elif point == "Lampung Timur":
    lat = "-5.066487613361172" # Sukadana
    lon = "105.54617418440846" # Sukadana
elif point == "Tulang Bawang":
    lat = "-4.481194627124103" # Menggala
    lon = "105.24859593037621" # Menggala
elif point == "Mesuji":
    lat = "-3.873036433806739" # Wiralaga Mulya
    lon = "105.42211402543693" # Wiralaga Mulya
elif point == "Tulang Bawang Barat":
    lat = "-4.520336186080023" # Panaragan Jaya
    lon = "105.09373974042978" # Panaragan Jaya
elif point == "Lampung Utara":
    lat = "-4.824536940653451" # Kotabumi
    lon = "104.89652404507099" # Kotabumi
elif point == "Way Kanan":
    lat = "-4.508519895853042" # Blambangan Umpu
    lon = "104.50897169186732" # Blambangan Umpu
elif point == "Lampung Barat":
    lat = "-5.034768300289403" # Liwa
    lon = "104.1325553249168" # Liwa
elif point == "Pesisir Barat":
    lat = "-5.190160597418451" # Krui
    lon = "103.9311192290223" # Krui


if st.button('Predict Air Quality'):
    df_merge = load_and_process_data(lat, lon, api_key)

    st.subheader("Forecasting Kualitas udara dalam 36 Jam")

    # Extract features for prediction
    features_for_prediction = df_merge[['aqi', 'pm10', 'pm25', 'o3', 'so2', 'no2', 'co']].values

    # Preprocess input data
    input_features_processed = preprocess_input_data(features_for_prediction)

    # Reshape features for LSTM input shape
    features_reshaped = np.reshape(input_features_processed, (int(input_features_processed.shape[0] / 6), 6, input_features_processed.shape[1]))

    # Make prediction
    prediction = predict_air_quality(features_reshaped)

    # Fit objek StandardScaler dengan data historis
    scaler = StandardScaler()
    scaler.fit(df_merge[['aqi', 'pm10', 'pm25', 'o3', 'so2', 'no2', 'co']])

    # Transformasi prediksi ke skala aslinya
    predictions = np.reshape(prediction, (int(input_features_processed.shape[0] / 6)*4, 7))
    predictions = scaler.inverse_transform(predictions)
    predictions = pd.DataFrame(predictions, columns=['aqi_pred', 'pm10_pred', 'pm25_pred', 'o3_pred', 'so2_pred', 'no2_pred', 'co_pred'])

    # Concatenate df_merge and predictions horizontally
    df_final = pd.concat([df_merge.reset_index(drop=True), predictions], axis=1)
    col1, col2 = st.columns(2)
    with col1:
        # Display historical data
        st.write("Historical Data")
        st.write(df_merge)

    with col2:
        # Display predicted data
        st.write("Predicted Data")
        st.write(predictions)

    # Plot real and predicted values for each feature separately
    for feature in ['aqi', 'pm10', 'pm25', 'o3', 'so2', 'no2', 'co']:
        st.subheader(f'Predicted vs Real {feature.capitalize()}')
        # Ensure that the column names exist in df_final
        if feature in df_final.columns and f'{feature}_pred' in df_final.columns:
            chart_data = df_final[['timestamp_local', feature, f'{feature}_pred']].set_index('timestamp_local')
            st.line_chart(chart_data)
        else:
            st.write(f"Column names for {feature} or {feature}_pred not found in df_final.")
    
    # Define actual_values and predicted_values
    actual_values = df_final[['aqi', 'pm10', 'pm25', 'o3', 'so2', 'no2', 'co']]
    predicted_values = df_final[['aqi_pred', 'pm10_pred', 'pm25_pred', 'o3_pred', 'so2_pred', 'no2_pred', 'co_pred']]

    # # Handle NaN values in actual_values and predicted_values
    # actual_values.fillna(actual_values.mean(), inplace=True)
    # predicted_values.fillna(predicted_values.mean(), inplace=True)

    # Calculate R-squared values
    r_squared_values = [calculate_r_squared(actual_values[feature], predicted_values[f'{feature}_pred']) for feature in actual_values.columns]

    st.subheader("R-squared Values")
    for i, feature in enumerate(actual_values.columns):
        st.write(f"{feature.capitalize()}: {r_squared_values[i]}")
        
# Footer
    st.markdown("""
        ---
        Skripsi © 2024 Bagus Wahyu Pratomo. 2015061003
        """)

st.sidebar.markdown("""
    © 2024 Bagus Wahyu Pratomo.
    """)
