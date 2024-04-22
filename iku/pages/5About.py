import streamlit as st

def main():
    st.title("Tentang Aplikasi")
    st.write("Aplikasi ini merupakan Tugas Akhir Sarjana Teknik Informatika.")

    st.header("Pengembang")
    st.write("Aplikasi ini dikembangkan oleh Bagus Wahyu Pratomo.")

    st.header("Kualitas Udara")
    st.write("Kualitas udara merujuk pada tingkat kemurnian udara yang kita hirup dalam lingkungan sekitar. Ini mencakup berbagai parameter seperti konsentrasi partikel, gas, dan zat-zat berbahaya lainnya yang dapat mempengaruhi kesehatan manusia dan lingkungan. Memahami kualitas udara sangat penting karena udara yang bersih mendukung kesehatan yang baik, sementara udara yang tercemar dapat menyebabkan berbagai masalah kesehatan serius. Pemantauan dan pengelolaan kualitas udara adalah upaya penting untuk memastikan lingkungan yang aman dan sehat bagi semua makhluk hidup.")

    st.image('iku/image/iku2.jpg', caption="Klasifikasi Kualitas Udara")

    st.header("Perhitungan Indeks Kualitas Udara (IKU)")
    st.write("Indeks Kualitas Udara (IKU) adalah nilai yang menunjukkan tingkat pencemaran udara di suatu daerah pada waktu tertentu.")
    st.write("IKU dihitung berdasarkan konsentrasi beberapa parameter pencemar udara seperti PM10, SO2, NO2, CO, O3, dan lainnya.")
    
    st.header("Sumber Data")
    st.write("Data kualitas udara yang digunakan berasal dari Weatherbit API.")
    
    # Footer
    st.markdown("""
        ---
        Skripsi © 2024 Bagus Wahyu Pratomo (2015061003).
        """)

    st.sidebar.markdown("""
        © 2024 Bagus Wahyu Pratomo.
        """)

if __name__ == "__main__":
    main()
