import streamlit as st
import google.generativeai as genai
import json
import random

# --- KURUMSAL TEMA VE AYARLAR ---
st.set_page_config(page_title="LCW Liderlik Simülatörü", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 4em; background-color: #0054a6; color: white; font-weight: bold; }
    .stAlert { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# API Anahtarı Yapılandırması
genai.configure(api_key='AQ.Ab8RN6LpvpinBuDLv3Qo6n0kLMOLt_fN6DWQX4rHkjAkYvKkCA')
model = genai.GenerativeModel('gemini-1.5-flash')

# --- HAFIZA (SESSION STATE) ---
if 'stats' not in st.session_state:
    st.session_state.stats = {'Moral': 60, 'Verimlilik': 60, 'Güven': 60}
if 'tur' not in st.session_state:
    st.session_state.tur = 1
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None

# --- GENİŞLETİLMİŞ LCW SENARYO HAVUZU (AI ÇALIŞMAZSA DEVREYE GİRER) ---
havuz = [
    {"olay": "Mağazada yoğun kampanya dönemi başladı ama 2 personel rapor aldı. Kalan ekip çok gergin.", "secenekler": [{"id": "A", "metin": "Merkezden geçici destek iste ve ekibe yemek ısmarla.", "etki": {"Moral": 15, "Verimlilik": 10}}, {"id": "B", "metin": "Vardiyaları uzat ve ekstra mesai ücreti sözü ver.", "etki": {"Verimlilik": 20, "Moral": -10}}]},
    {"olay": "Yeni bir dijital İK platformuna geçiliyor. Kıdemli müdürler 'eski usul devam edelim' diyor.", "secenekler": [{"id": "A", "metin": "Gönüllü bir pilot grup kurup başarıyı onlara göster.", "etki": {"Güven": 15, "Verimlilik": 10}}, {"id": "B", "metin": "Kullanımı performans kriteri olarak zorunlu tut.", "etki": {"Verimlilik": 20, "Moral": -15}}]},
    {"olay": "Bir çalışanının yüksek potansiyeli var ama başka firmadan teklif aldığını öğrendin.", "secenekler": [{"id": "A", "metin": "Kariyer planını öne çek ve yetki alanını genişlet.", "etki": {"Güven": 20, "Moral": 10}}, {"id": "B", "metin": "Maaş artışı teklif et ve bağlılık sözü iste.", "etki": {"Verimlilik": 10, "Moral": 5}}]},
    {"olay": "Ekip toplantısında bir fikir sundun ama en güvendiğin arkadaşın seni herkesin önünde eleştirdi.", "secenekler": [{"id": "A", "metin": "Toplantı sonrası odana çağırıp duygularını netçe paylaş.", "etki": {"Güven": 15, "Moral": 5}}, {"id": "B", "metin": "Eleştiriyi profesyonelce karşıla ve fikrini revize et.", "etki": {"Moral": 10, "Verimlilik": 10}}]}
]

def kriz_uret():
    try:
        istek = "Sen bir LCW yöneticisisin. Kurumsal, etik ve gerçekçi bir İK liderlik senaryosu yaz. Sadece JSON formatında 'olay' ve 2 'secenek' (id, metin, etki{Moral, Verimlilik, Güven}) döndür."
        cevap = model.generate_content(istek)
        temiz_cevap = cevap.text.strip().replace('```json', '').replace('```', '')
        return json.loads(temiz_cevap)
    except:
        return random.choice(havuz)

# --- OYUN AKIŞI ---
st.title("💙 LC WAIKIKI LİDERLİK SİMÜLASYONU")
st.write("---")

# Skor Tablosu
cols = st.columns(3)
cols[0].metric("😊 Moral", f"{st.session_state.stats['Moral']}%")
cols[1].metric("📈 Verimlilik", f"{st.session_state.stats['Verimlilik']}%")
cols[2].metric("🤝 Güven", f"{st.session_state.stats['Güven']}%")

if st.session_state.tur <= 5:
    if st.session_state.current_scenario is None:
        st.session_state.current_scenario = kriz_uret()
    
    st.subheader(f"SENARYO {st.session_state.tur}")
    st.info(st.session_state.current_scenario['olay'])
    
    # Seçenek Butonları
    for s in st.session_state.current_scenario['secenekler']:
        if st.button(s['metin']):
            # Puanları Güncelle
            for k, v in s['etki'].items():
                st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))
            
            # Sonraki tura geç
            st.session_state.tur += 1
            st.session_state.current_scenario = None
            st.rerun()

else:
    st.balloons()
    st.success("Tebrikler! 5 günlük liderlik maratonunu tamamladınız.")
    st.write("### Final Liderlik Karneniz")
    st.dataframe([st.session_state.stats])
    
    if st.button("Simülasyonu Yeniden Başlat"):
        st.session_state.clear()
        st.rerun()
