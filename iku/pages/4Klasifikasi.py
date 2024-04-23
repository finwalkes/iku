import streamlit as st

st.header("Klasifikasi Kualitas Udara")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['AQI', 'PM2.5', 'PM10', 'Karbon Monoksida (CO)', 'Sulfur Dioksida (SO2)', 'Nitrogen Dioksida (NO2)', 'Ozone (O3)'])

with tab1:
    # Fungsi untuk menghitung AQI untuk PM2.5
    def calculate_pm25_aqi(C):
        if 0 <= C <= 12.0:
            return linear_conversion(C, 0, 50)
        elif 12.1 <= C <= 35.4:
            return linear_conversion(C, 51, 100)
        elif 35.5 <= C <= 55.4:
            return linear_conversion(C, 101, 150)
        elif 55.5 <= C <= 150.4:
            return linear_conversion(C, 151, 200)
        elif 150.5 <= C <= 250.4:
            return linear_conversion(C, 201, 300)
        elif 250.5 <= C <= 350.4:
            return linear_conversion(C, 301, 400)
        elif 350.5 <= C <= 500.4:
            return linear_conversion(C, 401, 500)

    # Fungsi konversi linier
    def linear_conversion(C, I_low, I_high):
        return ((I_high - I_low) / (500.4 - 0.0)) * (C - 0.0) + I_low

    # Tampilan UI menggunakan Streamlit
    st.subheader("Kalkulator Air Quality Index (AQI) untuk PM2.5 (berdasarkan standar EPA)")
    st.write("Air Quality Index (AQI) untuk PM2.5 dihitung berdasarkan kisaran konsentrasi polutan dan indeks kualitas udara.")

    C = st.number_input("Konsentrasi PM2.5 (µg/m³):", min_value=0.0, max_value=500.4, value=12.0)

    # Hitung AQI untuk PM2.5
    AQI = calculate_pm25_aqi(C)

    # Tampilkan hasil
    st.write(f"Air Quality Index (AQI) untuk PM2.5: {AQI}")

    if 0 <= AQI <= 50:
        st.write("Deskripsi: Baik")
    elif 51 <= AQI <= 100:
        st.write("Deskripsi: Sedang")
    elif 101 <= AQI <= 150:
        st.write("Deskripsi: Tidak Sehat untuk Orang Sensitif")
    elif 151 <= AQI <= 200:
        st.write("Deskripsi: Tidak Sehat")
    elif 201 <= AQI <= 300:
        st.write("Deskripsi: Sangat Tidak Sehat")
    else:
        st.write("Deskripsi: Berbahaya")

    # Tampilkan rumus dan penjelasannya
    st.write("---")
    st.write("Rumus AQI untuk PM2.5:")
    st.latex(r'''AQI = \frac{{(I_{\text{high}} - I_{\text{low}})}}{{(C_{\text{high}} - C_{\text{low}})}} \times (C - C_{\text{low}}) + I_{\text{low}}''')
    st.write("di mana:")
    st.write("- $AQI$ adalah Air Quality Index.")
    st.write("- $I_{\text{high}}$ adalah indeks kualitas udara tertinggi dalam rentang tertentu.")
    st.write("- $I_{\text{low}}$ adalah indeks kualitas udara terendah dalam rentang tertentu.")
    st.write("- $C_{\text{high}}$ adalah batas atas konsentrasi PM2.5 dalam rentang tertentu.")
    st.write("- $C_{\text{low}}$ adalah batas bawah konsentrasi PM2.5 dalam rentang tertentu.")
    st.write("- $C$ adalah konsentrasi PM2.5 yang diamati.")

with tab2:
    def calculate_pm25(aqi):
        """
        Fungsi ini menghitung konsentrasi PM2.5 berdasarkan indeks AQI.
        Rumus yang digunakan berasal dari EPA (Environmental Protection Agency).
        """
        pm25 = None
        if aqi <= 50:
            pm25 = 0
        elif aqi <= 100:
            pm25 = ((aqi - 50) * (12.0 - 0) / (100 - 51)) + 0
        elif aqi <= 150:
            pm25 = ((aqi - 100) * (35.4 - 12.1) / (150 - 101)) + 12.1
        elif aqi <= 200:
            pm25 = ((aqi - 150) * (55.4 - 35.5) / (200 - 151)) + 35.5
        elif aqi <= 300:
            pm25 = ((aqi - 200) * (150.4 - 55.5) / (300 - 201)) + 55.5
        elif aqi <= 400:
            pm25 = ((aqi - 300) * (250.4 - 150.5) / (400 - 301)) + 150.5
        elif aqi <= 500:
            pm25 = ((aqi - 400) * (350.4 - 250.5) / (500 - 401)) + 250.5
        return pm25

    st.title("Kalkulator PM2.5 dari AQI")
    st.write("Aplikasi ini menghitung perkiraan konsentrasi PM2.5 berdasarkan indeks AQI.")

    # Memasukkan nilai AQI dari pengguna
    aqi = st.number_input("Masukkan nilai AQI:", min_value=0)

    # Hitung PM2.5 menggunakan fungsi yang telah ditentukan
    if st.button("Hitung PM2.5"):
        pm25 = calculate_pm25(aqi)
        st.write(f"Konsentrasi PM2.5 perkiraan adalah: {pm25} µg/m³")

    # Menampilkan rumus
    st.write("---")
    st.write("Rumus konversi AQI ke PM2.5 (berdasarkan EPA):")
    st.latex(r"PM2.5 = \begin{cases} 0, & \text{jika AQI} \leq 50 \\ ((\text{AQI} - 50) \times (12.0 - 0) / (100 - 51)) + 0, & \text{jika } 50 < \text{AQI} \leq 100 \\ ((\text{AQI} - 100) \times (35.4 - 12.1) / (150 - 101)) + 12.1, & \text{jika } 100 < \text{AQI} \leq 150 \\ ((\text{AQI} - 150) \times (55.4 - 35.5) / (200 - 151)) + 35.5, & \text{jika } 150 < \text{AQI} \leq 200 \\ ((\text{AQI} - 200) \times (150.4 - 55.5) / (300 - 201)) + 55.5, & \text{jika } 200 < \text{AQI} \leq 300 \\ ((\text{AQI} - 300) \times (250.4 - 150.5) / (400 - 301)) + 150.5, & \text{jika } 300 < \text{AQI} \leq 400 \\ ((\text{AQI} - 400) \times (350.4 - 250.5) / (500 - 401)) + 250.5, & \text{jika } 400 < \text{AQI} \leq 500 \\ \end{cases}")

    
with tab3:
    st.title('Kalkulator PM10')
    st.write('Gunakan kalkulator ini untuk mengkonversi konsentrasi partikulat dalam mikrogram per meter kubik (µg/m³) menjadi PM10.')

    st.write('### Rumus:')
    st.latex(r'PM_{10} = Konsentrasi_{partikulat} \times 1.0')

    def calculate_pm10(concentration):
        pm10 = concentration * 1.0
        return pm10

    concentration = st.number_input('Masukkan konsentrasi partikulat (µg/m³):', min_value=0.0, step=0.1, format="%.1f")
        
    if st.button('Hitung PM10'):
        pm10 = calculate_pm10(concentration)
        st.write(f'Konsentrasi PM10 yang dihasilkan adalah {pm10} µg/m³.')
    
with tab4:
    def carbon_monoxide_concentration(voltage):
        # Rumus konversi tegangan menjadi konsentrasi CO (contoh)
        # Ini hanyalah contoh, sesuaikan dengan rumus yang sesuai dengan sensor atau perangkat yang digunakan.
        concentration = voltage * 100  # Misalnya, ada rumus yang menyatakan bahwa setiap 0.01 V merepresentasikan 1 ppm CO
        
        return concentration

    st.title('Kalkulator Konsentrasi Karbon Monoksida (CO)')

    st.write('Kalkulator ini digunakan untuk menghitung konsentrasi karbon monoksida (CO) berdasarkan tegangan yang diukur.')
    st.write('Rumus yang digunakan untuk konversi tegangan menjadi konsentrasi CO adalah contoh dan mungkin perlu disesuaikan sesuai dengan sensor atau perangkat yang digunakan.')

    st.subheader('Rumus:')
    st.latex(r'''
        \text{Konsentrasi CO (ppm)} = \text{Tegangan (volt)} \times \text{Faktor Konversi}
    ''')

    # Input tegangan
    voltage_input = st.number_input('Masukkan tegangan (dalam volt):', min_value=0.0)

    # Tombol untuk menghitung konsentrasi
    if st.button('Hitung Konsentrasi CO'):
        # Hitung konsentrasi CO
        co_concentration = carbon_monoxide_concentration(voltage_input)
        st.write(f'Konsentrasi Karbon Monoksida (CO): {co_concentration:.2f} ppm')  # Sesuaikan dengan satuan yang sesuai

with tab5:
    def hitung_kadar_so2(konsentrasi_so2, volume_udara):
        kadar_so2 = konsentrasi_so2 * volume_udara
        return kadar_so2

    st.title("Kalkulator Kadar SO2")

    st.write("Kadar SO2 dalam udara dapat dihitung menggunakan rumus berikut:")
    st.latex(r'Kadar\ SO2\ (partikulat\ SO2) = Konsentrasi\ SO2\ (ppm) \times Volume\ Udara\ (m^3)')

    konsentrasi_so2_ppm = st.number_input("Masukkan konsentrasi SO2 (ppm):")
    volume_udara_m3 = st.number_input("Masukkan volume udara (m^3):")

    if st.button("Hitung"):
        kadar_so2 = hitung_kadar_so2(konsentrasi_so2_ppm, volume_udara_m3)
        st.write("Kadar SO2 dalam udara adalah:", kadar_so2, "partikulat SO2")

with tab6:
    def calculate_no2_molar_weight():
        st.title("Kalkulator Berat Molar NO2")
        st.write("Di sini Anda dapat menghitung berat molar NO2 (Dioksida Nitrogen) berdasarkan rumus kimianya.")
        st.write("Rumus kimia NO2 adalah NO2 = N + 2O, di mana N adalah atom Nitrogen dan O adalah atom Oksigen.")
        st.write("Untuk menghitung berat molar NO2, Anda perlu memasukkan berat atom Nitrogen (N) dan berat atom Oksigen (O).")
        st.write("Berikut rumus untuk menghitung berat molar NO2:")
        st.latex(r'Berat Molar (NO_2) = Berat Atom N + 2 \times Berat Atom O')
        
        berat_atom_n = st.number_input("Masukkan berat atom nitrogen (N) dalam gram/mol:", min_value=0.0, step=0.01)
        berat_atom_o = st.number_input("Masukkan berat atom oksigen (O) dalam gram/mol:", min_value=0.0, step=0.01)
        
        # Menghitung berat molar NO2
        berat_molar_no2 = berat_atom_n + 2 * berat_atom_o
        
        st.write("Hasil:")
        st.write("Berat Molar NO2 = {:.2f} g/mol".format(berat_molar_no2))

    calculate_no2_molar_weight()
    
with tab7:
    def hitung_konsentrasi_ozon(tekanan, volume, suhu):
        # Konstanta gas ideal (dalam J/(mol·K))
        R = 8.314
        
        # Konversi suhu dari Celcius ke Kelvin
        suhu_kelvin = suhu + 273.15
        
        # Menggunakan hukum gas ideal untuk menghitung jumlah mol ozon
        jumlah_mol_ozon = (tekanan * volume) / (R * suhu_kelvin)
        
        return jumlah_mol_ozon

    def main():
        st.subheader("Kalkulator Konsentrasi Ozon")
        
        st.markdown("""
        ### Penjelasan Rumus:
        
        Rumus yang digunakan untuk menghitung konsentrasi ozon dalam udara adalah turunan dari Hukum Gas Ideal:
        
        $$
        n = \\frac{{PV}}{{RT}}
        $$
        
        Di mana:
        - $ n $ adalah jumlah mol ozon.
        - $ P $ adalah tekanan udara (dalam pascal, Pa).
        - $ V $ adalah volume udara (dalam meter kubik, m³).
        - $ R $ adalah konstanta gas ideal (biasanya $ 8.314 $ J/(mol·K)).
        - $ T $ adalah suhu udara (dalam kelvin, K).
        
        Dengan menggunakan rumus ini, kita dapat menghitung jumlah mol ozon dalam volume udara tertentu pada suhu dan tekanan tertentu. Setelah itu, jika kita memiliki data lainnya, seperti berat molekul ozon, kita bisa mengonversi jumlah mol menjadi satuan lain, seperti gram atau ppm (bagian per juta).
        """)
        
        tekanan = st.number_input("Masukkan tekanan udara (Pa)", min_value=0.0)
        volume = st.number_input("Masukkan volume udara (m³)", min_value=0.0)
        suhu = st.number_input("Masukkan suhu udara (°C)", min_value=-273.15)
        
        if st.button("Hitung Konsentrasi Ozon"):
            konsentrasi_ozon = hitung_konsentrasi_ozon(tekanan, volume, suhu)
            st.success(f"Konsentrasi ozon dalam udara: {konsentrasi_ozon:.4f} mol/m³")

    if __name__ == "__main__":
        main()


# Footer
st.markdown("""
    ---
    Skripsi © 2024 Bagus Wahyu Pratomo (2015061003).
    """)

st.sidebar.markdown("""
    © 2024 Bagus Wahyu Pratomo.
    """)
