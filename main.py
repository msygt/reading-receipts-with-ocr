import cv2
import pytesseract
import re
import pandas as pd
import os
import streamlit as st

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def fis_metnini_cikar(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return ""
    metin = pytesseract.image_to_string(img, lang='eng')
    return metin

def bilgi_ayikla(metin):
    toplam_tutar = re.search(r'TOTAL\s+(\d+\.\d{2})', metin)
    toplam_tutar = toplam_tutar.group(1) if toplam_tutar else "Tutar bulunamadı"
    tarih = re.search(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', metin)
    tarih = tarih.group(1) if tarih else "Tarih bulunamadı"
    saat = re.search(r'(\d{1,2}:\d{2})', metin)
    saat = saat.group(1) if saat else "Saat bulunamadı"
    return toplam_tutar, tarih, saat

st.title('Fiş Okuma Uygulaması')

fis_dizini = 'fisler'
veriler = []

if st.button('Fişleri Oku'):
    for fis in os.listdir(fis_dizini):
        if fis.endswith('.png'):
            fis_yolu = os.path.join(fis_dizini, fis)
            metin = fis_metnini_cikar(fis_yolu)
            if not metin:
                continue

            toplam_tutar, tarih, saat = bilgi_ayikla(metin)
            veriler.append({'Tarih': tarih, 'Saat': saat, 'Toplam Tutar': toplam_tutar})

    df = pd.DataFrame(veriler)

    excel_dosyasi = 'fis_verileri.xlsx'
    df.to_excel(excel_dosyasi, index=False)

    st.success("Veriler başarıyla okundu. Excel dosyasını indirmek için butona tıklayın.")
    with open(excel_dosyasi, 'rb') as f:
        st.download_button(
            label='Excel Dosyasını İndir',
            data=f,
            file_name=excel_dosyasi,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
