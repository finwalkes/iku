import streamlit as st

def main():
    st.title("Tentang Aplikasi")
    st.write("Aplikasi ini merupakan Tugas Akhir Sarjana Teknik Informatika. ")

    st.header("Pengembang")
    st.write("Aplikasi ini dikembangkan oleh Bagus Wahyu Pratomo.")

    st.header("Kualitas Udara")
    st.write("")

    st.header("Perhitungan Indeks Kualitas Udara (IKU)")
    

    st.header("Sumber Data")
    st.write("Data kualitas udara yang saya gunakan berasal dari weatherbit API.")
    
    # Footer
    st.markdown("""
        ---
        Skripsi © 2024 Bagus Wahyu Pratomo. 2015061003
        """)

    st.sidebar.markdown("""
        © 2024 Bagus Wahyu Pratomo.
        """)



if __name__ == "__main__":
    main()
