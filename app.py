import streamlit as st
import google.generativeai as genai
import json
import random

# --- KURUMSAL TEMA ---
st.set_page_config(page_title="LCW Liderlik Akademisi", layout="wide")

st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 5em; 
        background-color: #f8f9fa; color: #0054a6; 
        border: 2px solid #0054a6; font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #0054a6; color: white; }
    .stMetric { background: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# API Konfigürasyonu
genai.configure(api_key='AQ.Ab8RN6LpvpinBuDLv3Qo6n0kLMOLt_fN6DWQX4rHkjAkYvKkCA')
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SİSTEM HAFIZASI ---
if 'stats' not in st.session_state:
    st.session_state.stats = {'Moral': 50, 'Verimlilik': 50, 'Güven': 50}
if 'tur' not in st.session_state:
    st.session_state.tur = 1
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# --- GENİŞLETİLMİŞ LCW SENARYO ÖRNEKLERİ ---
# Buraya manuel olarak istediğiniz kadar (100+) soru ekleyebilirsiniz. 
# Ama AI kısmı zaten her seferinde benzersiz üretecektir.
havuz = [
    {
        "olay": "Mağaza müdürü olarak, ekibin en iyi satışçısının diğer arkadaşlarına karşı kibirli davrandığını fark ettin. Satışlar çok iyi ama ekip huzursuz.",
        "secenekler": [
            {"metin": "Birebir görüşüp satış başarısını öv ama ekip ruhunun LCW için daha kritik olduğunu anlat.", "etki": {"Moral": 10, "Verimlilik": 5, "Güven": 10}},
            {"metin": "Ekip toplantısında isim vermeden 'nezaket' vurgulu bir konuşma yap.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 5}},
            {"metin": "Satışları düşürmemek adına görmezden gel, sonuçta rakamlar önemli.", "etki": {"Moral": -15, "Verimlilik": 10, "Güven": -10}},
            {"metin": "Performansını diğerlerine örnek göster ve herkesin onun gibi olmasını iste.", "etki": {"Moral": -20, "Verimlilik": 5, "Güven": -15}}
        ]
    },
    {
        "olay": "Merkezden gelen yeni bir kural, çalışanların çok sevdiği bir esnekliği (örn: mola saati esnekliği) kaldırıyor. Ekip tepkili.",
        "secenekler": [
            {"metin": "Kararın nedenlerini şeffafça açıkla ve başka bir alanda iyileştirme sözü ver.", "etki": {"Güven": 15, "Moral": 5, "Verimlilik": 5}},
            {"metin": "Bu kararı senin almadığını, 'Yukarıdan' geldiğini söyleyip sorumluluktan kaç.", "etki": {"Güven": -15, "Moral": -5, "Verimlilik": 0}},
            {"metin": "Kararı sert bir şekilde uygula, kurallara uymayanlarla yolları ayıracağını belirt.", "etki": {"Verimlilik": 10, "Moral": -20, "Güven": -10}},
            {"metin": "Görmezden gel, eski usul devam etmelerine sessizce izin ver.", "etki": {"Moral": 15, "Verimlilik": -15, "Güven": -5}}
        ]
    }
]

def kriz_uret():
    try:
        istek = """Sen bir LCW Liderlik Eğitmenisin. 
        Gerçekçi, kurumsal ve 4 seçenekli bir İK/Liderlik senaryosu üret. 
        JSON formatında şu yapıda olsun: 
        {"olay": "...", "secenekler": [{"metin": "...", "etki": {"Moral": 10, "Verimlilik": -5, "Güven": 5}}, ...]} 
        Lütfen 4 seçenek de birbirinden farklı yaklaşımlar (Demokratik, Otoriter, İlgisiz, Çözüm Odaklı) olsun."""
        
        cevap = model.generate_content(istek)
        txt = cevap.text.strip().replace('```json', '').replace('```', '')
        return json.loads(txt)
    except:
        return random.choice(havuz)

# --- ARAYÜZ ---
st.image("https://corporate.lcwaikiki.com/Resource/Images/logo.png", width=200)
st.title("Liderlik Simülasyonu 2.0")

# Yan Panel: Skorlar
with st.sidebar:
    st.header("Liderlik Göstergeleri")
    for k, v in st.session_state.stats.items():
        st.write(f"**{k}**")
        st.progress(v / 100)
        st.metric("", f"%{v}")
    
    if st.button("Oyunu Sıfırla"):
        st.session_state.clear()
        st.rerun()

# Oyun Alanı
if not st.session_state.game_over:
    if st.session_state.current_scenario is None:
        with st.spinner("Yeni kriz analiz ediliyor..."):
            st.session_state.current_scenario = kriz_uret()
            st.rerun()

    sc = st.session_state.current_scenario
    
    st.info(f"**DURUM {st.session_state.tur}:** 

 {sc['olay']}")
    
    st.write("### Kararınız Nedir?")
    
    # 4 Seçeneği 2x2 grid yapısında gösterelim
    col1, col2 = st.columns(2)
    
    for i, s in enumerate(sc['secenekler']):
        target_col = col1 if i % 2 == 0 else col2
        if target_col.button(s['metin'], key=f"btn_{i}"):
            # Puan güncelle
            for k, v in s['etki'].items():
                st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))
            
            # Tur kontrolü
            if st.session_state.tur >= 10: # 10 Soru sürecek
                st.session_state.game_over = True
            else:
                st.session_state.tur += 1
                st.session_state.current_scenario = None
            st.rerun()

else:
    st.success("🏁 Simülasyon Tamamlandı!")
    final_score = sum(st.session_state.stats.values()) / 3
    st.header(f"Toplam Liderlik Puanınız: {int(final_score)}")
    
    if final_score > 70:
        st.balloons()
        st.write("🏆 Muazzam bir LCW Liderisiniz! Ekibiniz size güveniyor.")
    elif final_score > 40:
        st.write("📈 İyi bir yöneticisiniz ancak ekip bağlılığına daha çok odaklanmalısınız.")
    else:
        st.write("⚠️ Liderlik tarzınızı gözden geçirmelisiniz. Verimlilik kadar insan odağı da önemli.")

