import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Fraud Sentinel PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #1c1e21; }
    .stDataFrame { background-color: white !important; color: black !important; border: 1px solid #ddd; }
    [data-testid="stMetricValue"] { color: #d32f2f !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Fraud Sentinel AI — Güvenli Veri Merkezi")

tab1, tab2 = st.tabs(["⚡ Tekli Kontrol", "📊 Toplu Veri Dashboard"])

with tab1:
    st.write("Manuel test için tekli işlem kontrolü.")
    with st.form("manual"):
        amt = st.number_input("İşlem Tutarı ($)", value=150.0)
        cat = st.selectbox("Kategori", ["gas_station", "grocery", "entertainment", "other"])
        submit = st.form_submit_button("Analiz Et")
        if submit:
            try:
                res = requests.post("http://localhost:8000/predict", json={"amt": amt, "category": cat})
                if res.status_code == 200:
                    d = res.json()
                    st.metric("Risk", f"%{round(d['fraud_probability']*100, 2)}")
                    st.warning(f"KARAR: {d['decision']}")
            except Exception as e: st.error("Bağlantı koptu.")

with tab2:
    st.subheader("Büyük Veri Analizi")
    file = st.file_uploader("Dosyayı buraya bırakın (CSV)", type=["csv"])
    
    if file:
        df = pd.read_csv(file)
        st.write(f"📂 Okunan Satır: **{len(df):,}**")
        
        if st.button("🚀 DERİN ANALİZİ BAŞLAT"):
            CHUNK = 50000; results = []; bar = st.progress(0); start = time.time()
            
            for i in range(0, len(df), CHUNK):
                # ÇÖKME ÖNLEYİCİ 1: Boş hücreleri (NaN) None'a çevir (JSON bunu sever)
                chunk = df.iloc[i : i+CHUNK]
                chunk_clean = chunk.where(pd.notnull(chunk), None)
                batch = chunk_clean.to_dict(orient="records")
                
                try:
                    r = requests.post("http://localhost:8000/predict-batch", json=batch)
                    if r.status_code == 200:
                        results.extend(r.json())
                    else:
                        st.error(f"API Hatası (Chunk {i}): {r.text}")
                except Exception as e:
                    st.error(f"API'ye ulaşılamıyor: {e}")
                    break
                    
                bar.progress(min((i + CHUNK) / len(df), 1.0))
            
            # ÇÖKME ÖNLEYİCİ 2: Eğer API hiçbir şey döndürmediyse sistemi durdur
            if not results:
                st.error("🚨 İşlem başarısız! API'den hiçbir sonuç alınamadı. Lütfen hataları kontrol edin.")
            else:
                res_df = pd.DataFrame(results)
                
                st.markdown("---")
                st.header("📊 Yönetici Özeti")
                m1, m2, m3 = st.columns(3)
                m1.metric("İşlenen Toplam", f"{len(res_df):,}")
                m2.metric("Bloke Edilen (BLOCK)", len(res_df[res_df['decision'] == 'BLOCK']))
                m3.metric("Analiz Süresi", f"{round(time.time()-start, 1)} sn")

                st.markdown("---")
                st.subheader("📥 Veri Ayıklama (İndirme)")
                st.write("Sadece riskli işlemleri indirerek dosya boyutunu küçültün.")
                
                only_fraud = res_df[res_df['decision'] != 'ALLOW']
                
                col_a, col_b = st.columns(2)
                col_a.download_button("🚩 SADECE ŞÜPHELİLERİ İNDİR (Küçük Boyut)", only_fraud.to_csv(index=False), "suspicious.csv")
                col_b.download_button("💾 TÜM LİSTEYİ İNDİR (Büyük Boyut)", res_df.to_csv(index=False), "full.csv")