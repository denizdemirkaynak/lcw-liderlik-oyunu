import streamlit as st
import google.generativeai as genai
import json
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LCW Liderlik Akademisi", layout="wide")

# Görsel iyileştirme için CSS
st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 6em; 
        background-color: #ffffff; color: #0054a6; 
        border: 2px solid #0054a6; font-weight: bold;
        white-space: normal;
    }
    .stButton>button:hover { background-color: #0054a6; color: white; }
    .stMetric { background: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# API Yapılandırması (Sizin Anahtarınız)
genai.configure(api_key='AQ.Ab8RN6LpvpinBuDLv3Qo6n0kLMOLt_fN6DWQX4rHkjAkYvKkCA')
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SİSTEM HAFIZASI ---
if 'stats' not in st.session_state:
    st.session_state.stats = {'Moral': 50, 'Verimlilik': 50, 'Güven': 50}
if 'tur' not in st.session_state:
    st.session_state.tur = 1
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None
if 'finished' not in st.session_state:
    st.session_state.finished = False

# --- YEDEK SENARYO HAVUZU (AI BAĞLANTISI KESİLİRSE) ---
havuz = [
    {
        "olay": "Ekibinizdeki iki kıdemli çalışan, yeni bir iş süreci üzerinde fikir ayrılığı yaşıyor ve bu durum ofis huzurunu bozuyor.",
        "secenekler": [
            {"metin": "İkisini aynı anda odaya çağırıp ortak bir çözüm bulana kadar çıkmayacağınızı söyleyin.", "etki": {"Moral": -10, "Verimlilik": 5, "Güven": 10}},
            {"metin": "Fikirlerini ayrı ayrı dinleyip, LCW değerlerine en uygun olanı siz seçin.", "etki": {"Moral": 5, "Verimlilik": 15, "Güven": 5}},
            {"metin": "Tarafsız bir moderatör eşliğinde fikirlerini tüm ekibe sunmalarını isteyin.", "etki": {"Moral": 10, "Verimlilik": 10, "Güven": 15}},
            {"metin": "Zamanla düzeleceğini düşünüp müdahale etmeyin.", "etki": {"Moral": -15, "Verimlilik": -10, "Güven": -20}}
        ]
    }
]

def kriz_uret():
    try:
        istek = """Sen bir LCW Liderlik Eğitmenisin. 
        4 seçenekli, gerçekçi bir yönetim senaryosu üret. 
        SADECE JSON döndür: 
        {"olay": "...", "secenekler": [{"metin": "...", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": -5}}, ...]} 
        Lütfen 4 seçenek olsun."""
        
        cevap = model.generate_content(istek)
        # JSON temizleme
        res_text = cevap.text.strip()
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0].strip()
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(res_text)
    except:
        return random.choice(havuz)

# --- ARAYÜZ ---
st.title("💙 LC WAIKIKI LİDERLİK AKADEMİSİ")
st.write("---")

# Skorlar
col_a, col_b, col_c = st.columns(3)
col_a.metric("😊 Ekip Morali", f"%{st.session_state.stats['Moral']}")
col_b.metric("📈 Operasyonel Verimlilik", f"%{st.session_state.stats['Verimlilik']}")
col_c.metric("🤝 Kurumsal Güven", f"%{st.session_state.stats['Güven']}")

st.write("---")

if not st.session_state.finished:
    # Senaryo Getir
    if st.session_state.current_scenario is None:
        st.session_state.current_scenario = kriz_uret()
    
    current = st.session_state.current_scenario
    
    # Olay Metni
    st.subheader(f"DURUM {st.session_state.tur}")
    st.info(current['olay'])
    
    st.write("#### Kararınız Nedir?")
    
    # 4 Seçeneği göster (Grid yapı)
    c1, c2 = st.columns(2)
    for i, s in enumerate(current['secenekler']):
        with (c1 if i < 2 else c2):
            if st.button(s['metin'], key=f"btn_{i}_{st.session_state.tur}"):
                # Puanları uygula
                for k, v in s['etki'].items():
                    st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))
                
                # Tura devam veya bitiş
                if st.session_state.tur >= 10:
                    st.session_state.finished = True
                else:
                    st.session_state.tur += 1
                    st.session_state.current_scenario = None
                st.rerun()

else:
    st.balloons()
    st.header("🏁 Simülasyon Tamamlandı!")
    avg_score = sum(st.session_state.stats.values()) / 3
    
    st.subheader(f"Ortalama Liderlik Puanınız: {int(avg_score)} / 100")
    
    if avg_score > 70:
        st.success("Mükemmel Liderlik! LCW kültürünü harika temsil ediyorsunuz.")
    elif avg_score > 40:
        st.warning("İyi bir yönetici adayı. Bazı alanlarda gelişime ihtiyaç var.")
    else:
        st.error("Liderlik tarzınızı revize etmelisiniz. Ekip desteğine odaklanın.")
        
    if st.button("Tekrar Başlat"):
        st.session_state.clear()
        st.rerun()
