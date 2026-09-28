import streamlit as st
import google.generativeai as genai
import json
import random

# --- KURUMSAL AYARLAR ---
st.set_page_config(page_title="LCW Liderlik Simülatörü", layout="centered")

# API Anahtarı
genai.configure(api_key='AQ.Ab8RN6LpvpinBuDLv3Qo6n0kLMOLt_fN6DWQX4rHkjAkYvKkCA')
model = genai.GenerativeModel('gemini-1.5-flash')

# --- HAFIZA SİSTEMİ ---
if 'stats' not in st.session_state:
    st.session_state.stats = {'Moral': 50, 'KPI': 50, 'Güven': 50}
if 'tur' not in st.session_state:
    st.session_state.tur = 1
if 'history' not in st.session_state:
    st.session_state.history = []

# --- YEDEK SORULAR ---
yedek_sorular = [
    {"olay": "Ekipte iki kıdemli çalışan çatışıyor.", "secenekler": [{"id": "A", "metin": "Yüzleştir", "etki": {"Moral": 5, "Güven": 10}, "analiz": "Cesur hamle."}, {"id": "B", "metin": "Ayrı dinle", "etki": {"Moral": 10, "Güven": 15}, "analiz": "Sakin çözüm."}]}
]

# --- KRİZ ÜRETME ---
def kriz_getir():
    try:
        komut = "LCW liderlik senaryosu üret. IK Departmanı. SADECE JSON formatında bir olay ve 2 seçenek üret."
        res = model.generate_content(komut)
        txt = res.text.strip()
        if '```' in txt: txt = txt.split('```')[1].replace('json', '').strip()
        return json.loads(txt)
    except:
        return random.choice(yedek_sorular)

# --- ARAYÜZ ---
st.title("💙 LC WAIKIKI LİDERLİK SİMÜLASYONU")

# Skorlar
col1, col2, col3 = st.columns(3)
col1.metric("😊 Moral", f"{st.session_state.stats['Moral']}%")
col2.metric("📈 KPI", f"{st.session_state.stats['KPI']}%")
col3.metric("🤝 Güven", f"{st.session_state.stats['Güven']}%")

if st.session_state.tur <= 3:
    st.subheader(f"SORU {st.session_state.tur}")
    data = kriz_getir()
    st.warning(data['olay'])
    
    for s in data['secenekler']:
        if st.button(s['metin']):
            # Puanları güncelle
            for k in st.session_state.stats:
                st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + s['etki'].get(k, 0)))
            st.session_state.tur += 1
            st.rerun()
else:
    st.success("Tebrikler! Simülasyonu Tamamladınız.")
    st.write("Final Skorlarınız:", st.session_state.stats)
    if st.button("Yeniden Başlat"):
        st.session_state.clear()
        st.rerun()
