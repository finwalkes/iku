import streamlit as st
import pandas as pd
import numpy as np
import requests
from glom import glom

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

tab1, tab2 = st.tabs(['Live History', "Date History"])

with tab1:
    # live history
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
    data = df_merge.values.tolist()

    # Tampilkan menggunakan Streamlit
    st.write("History Data Kualitas Udara Pada Kota ", df_merge['city_name'].iloc[0])
    st.write(pd.DataFrame(data, columns=["Nama Kota", "latitude", "longtitude", "AQI", "PM10", "PM25", "Ozone", "SO2", "NO2", "CO", "Timestamp"]))
    
with tab2:
    col1, col2 = st.columns(2)
    button = st.button("History")
    
    start_date = col1.date_input("Tanggal Awal")
    end_date = col2.date_input("Tanggal akhir")
    
    if button:
        history = f"https://api.weatherbit.io/v2.0/history/airquality?lat={lat}&lon={lon}&start_date={start_date}&end_date={end_date}&tz=local&key={api_key}"
        response2 = requests.get(history)
        dt = pd.read_json(response2.text)
        
        # Proses data
        target_aqi1 = df["data"]
        spec1 = {      
            "aqi" : (["aqi"]),
            "pm10" : (["pm10"]),
            "pm25" : (["pm25"]),
            "o3" : (["o3"]),
            "so2" : (["so2"]),
            "no2" : (["no2"]),
            "co" : (["co"]),
            "timestamp_local" : (['timestamp_local'])
        }

        data_json1 = glom(target_aqi1, spec1)
        df_aqi1 = pd.DataFrame.from_dict(data_json1)
        df_city1 = df[["city_name", "lat", "lon"]]
        df_merge1 = pd.concat([df_city1, df_aqi1], axis=1, sort=False)
        data1 = df_merge1.values.tolist()

        # Tampilkan menggunakan Streamlit
        st.write("Tren History Data Kualitas Udara pada tanggal", start_date, "sampai", end_date, 'pada kota',df_merge1['city_name'].iloc[0])
        st.write(pd.DataFrame(data1, columns=["Nama Kota", "latitude", "longtitude", "AQI", "PM10", "PM25", "Ozone", "SO2", "NO2", "CO", "Timestamp"]))

st.image('iku/image/iku.jpg', caption="Klasifikasi Kualitas Udara")

# Footer
st.markdown("""
    ---
    Skripsi © 2024 Bagus Wahyu Pratomo. 2015061003
    """)

st.sidebar.markdown("""
    © 2024 Bagus Wahyu Pratomo.
    """)
