import streamlit as st
import google.generativeai as genai
import json
import random

# --- KURUMSAL AYARLAR ---
st.set_page_config(page_title="LCW Liderlik Simülasyonu Pro", layout="wide")

st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 7em; 
        background-color: #ffffff; color: #0054a6; 
        border: 1px solid #d1d3d4; font-weight: 500;
        white-space: normal; padding: 10px; font-size: 15px;
    }
    .stButton>button:hover { border-color: #0054a6; background-color: #f8f9fa; color: #0054a6; }
    </style>
    """, unsafe_allow_html=True)

# API
genai.configure(api_key='AQ.Ab8RN6LpvpinBuDLv3Qo6n0kLMOLt_fN6DWQX4rHkjAkYvKkCA')
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SİSTEM HAFIZASI ---
if 'stats' not in st.session_state:
    st.session_state.stats = {'Moral': 60, 'Verimlilik': 60, 'Güven': 60}
if 'tur' not in st.session_state:
    st.session_state.tur = 1
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None
if 'history' not in st.session_state:
    st.session_state.history = []

# Senaryo temaları (Tekrarı önlemek için)
temalar = ["Performans Yönetimi", "Çalışan Bağlılığı", "Kriz Yönetimi", "Yenilikçilik", "Zor Kişiliklerle İletişim", "Etik İkilemler", "Mağaza Operasyonu", "Uzaktan Yönetim"]

def kriz_uret():
    tema = random.choice(temalar)
    try:
        istek = f"""Sen üst düzey bir LCW Liderlik Koçusun. 
        Konu: {tema}. 
        Gerçekçi ve yorumsal bir yönetim senaryosu yaz. 
        4 farklı liderlik tarzını temsil eden seçenekler sun: 
        1. Demokratik (Güven artırır, Verimlilik yavaşlatabilir)
        2. Otoriter (Verimlilik artırır, Moral düşürebilir)
        3. Koçvari (Gelişim odaklı, orta vadeli)
        4. Kaçınmacı (Risk almaz, skorları düşürür)
        
        ÖNEMLİ: Hiçbir seçenek 'mükemmel' olmasın. Her seçeneğin bir avantajı bir dezavantajı olsun.
        Sadece JSON döndür: 
        {{"olay": "...", "secenekler": [{{"metin": "...", "etki": {{"Moral": 5, "Verimlilik": -5, "Güven": 0}}}}, ...]}}"""
        
        cevap = model.generate_content(istek)
        res_text = cevap.text.strip()
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0].strip()
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0].strip()
            
        data = json.loads(res_text)
        random.shuffle(data['secenekler'])
        return data
    except Exception as e:
        st.error(f"HATA DETAYI: {str(e)}")  # <-- GEÇİCİ OLARAK BUNU EKLEDİK
        return {"olay": "Bağlantı hatası. Lütfen bir sonraki tura geçin.", "secenekler": []}

# --- ARAYÜZ ---
st.title("💙 LC WAIKIKI LİDERLİK SİMÜLASYONU")
st.caption("Yönetim kararlarınızın karmaşık etkilerini deneyimleyin.")

# Skor Paneli
col_stats = st.columns(3)
metrics = list(st.session_state.stats.items())
for i, (k, v) in enumerate(metrics):
    col_stats[i].metric(k, f"%{v}")

st.write("---")

if st.session_state.tur <= 10:
    if st.session_state.current_scenario is None:
        with st.spinner("Yeni liderlik vakası hazırlanıyor..."):
            st.session_state.current_scenario = kriz_uret()
            st.rerun()
    
    current = st.session_state.current_scenario
    
    st.subheader(f"VAKA {st.session_state.tur}")
    st.info(current['olay'])
    
    st.write("#### Liderlik Yaklaşımınız:")
    
    # Şıklar 2x2 Grid
    c1, c2 = st.columns(2)
    for i, s in enumerate(current['secenekler']):
        with (c1 if i % 2 == 0 else c2):
            if st.button(s['metin'], key=f"v_{st.session_state.tur}_{i}"):
                # Puan güncelle
                for k, v in s['etki'].items():
                    st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))
                
                # İlerle
                st.session_state.tur += 1
                st.session_state.current_scenario = None
                st.rerun()

else:
    st.success("🏁 10 Günlük Liderlik Maratonu Tamamlandı.")
    avg = sum(st.session_state.stats.values()) / 3
    st.metric("Final Liderlik Endeksiniz", f"%{int(avg)}")
    
    # Detaylı Analiz
    if avg > 75:
        st.write("💎 **Stratejik Lider:** Dengeleri harika korudunuz.")
    elif avg > 50:
        st.write("📈 **Operasyonel Lider:** Sonuç odaklısınız ama insan faktörüne dikkat.")
    else:
        st.write("⚠️ **Gelişim Alanı:** Kararlarınızın yan etkilerini daha iyi analiz etmelisiniz.")

    if st.button("Simülasyonu Baştan Başlat"):
        st.session_state.clear()
        st.rerun()
