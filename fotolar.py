import streamlit as st
import os

fis_dizini = 'fisler'

st.title("Fiş Okuma Uygulaması")

uploaded_file = st.file_uploader("Bir fiş resmi yükleyin", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Yüklenen Fiş Resmi", use_column_width=True)

if st.button("Fişler Galerisi"):
    st.write("Fişler Galerisi")
    for fis in os.listdir(fis_dizini):
        if fis.endswith(('.png', '.jpg', '.jpeg')):
            fis_yolu = os.path.join(fis_dizini, fis)
            st.image(fis_yolu, caption=fis, use_column_width=True)
