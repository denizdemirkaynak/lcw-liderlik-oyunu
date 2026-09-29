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

# --- API YAPILANDIRMASI ---
API_KEY = 'AQ.Ab8RN6LpvpinBuDLv3Qo6n0kLMOLt_fN6DWQX4rHkjAkYvKkCA'
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SİSTEM HAFIZASI ---
if 'stats' not in st.session_state:
    st.session_state.stats = {'Moral': 60, 'Verimlilik': 60, 'Güven': 60}
if 'tur' not in st.session_state:
    st.session_state.tur = 1
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None
if 'last_error' not in st.session_state:
    st.session_state.last_error = None
if 'ai_success_count' not in st.session_state:
    st.session_state.ai_success_count = 0

# Senaryo temaları (Tekrarı önlemek için)
temalar = ["Performans Yönetimi", "Çalışan Bağlılığı", "Kriz Yönetimi", "Yenilikçilik",
           "Zor Kişiliklerle İletişim", "Etik İkilemler", "Mağaza Operasyonu", "Uzaktan Yönetim"]

# --- YEDEK SENARYO HAVUZU (AI çalışmazsa devreye girer, çeşitlilik için 6 farklı vaka) ---
havuz = [
    {
        "olay": "Ekibinizdeki iki kıdemli çalışan, yeni bir iş süreci üzerinde fikir ayrılığı yaşıyor ve bu durum ofis huzurunu bozuyor.",
        "secenekler": [
            {"metin": "İkisini aynı anda odaya çağırıp ortak bir çözüm bulana kadar çıkmayacağınızı söyleyin.", "etki": {"Moral": -5, "Verimlilik": 5, "Güven": 10}},
            {"metin": "Fikirlerini ayrı ayrı dinleyip, size en uygun olanı siz seçin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": -5}},
            {"metin": "Tarafsız bir moderatör eşliğinde fikirlerini tüm ekibe sunmalarını isteyin.", "etki": {"Moral": 5, "Verimlilik": -5, "Güven": 10}},
            {"metin": "Zamanla düzeleceğini düşünüp müdahale etmeyin.", "etki": {"Moral": -10, "Verimlilik": -5, "Güven": -10}}
        ]
    },
    {
        "olay": "Mağazada yoğun kampanya dönemi başladı ama 2 personel rapor aldı. Kalan ekip çok gergin ve yorgun.",
        "secenekler": [
            {"metin": "Merkezden geçici destek isteyin, süreç biraz yavaşlasa da ekibi yormayın.", "etki": {"Moral": 10, "Verimlilik": -5, "Güven": 5}},
            {"metin": "Vardiyaları uzatın ve ekstra mesai ücreti sözü verin.", "etki": {"Moral": -5, "Verimlilik": 15, "Güven": 0}},
            {"metin": "Siz de sahaya inip satış desteği verin, örnek liderlik yapın.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 5}},
            {"metin": "Hedefleri revize etmeden mevcut ekiple devam etmelerini isteyin.", "etki": {"Moral": -15, "Verimlilik": 5, "Güven": -10}}
        ]
    },
    {
        "olay": "Yeni bir dijital İK platformuna geçiliyor. Kıdemli bir müdür 'eski usul devam edelim' diyerek direniyor.",
        "secenekler": [
            {"metin": "Gönüllü bir pilot grup kurup küçük bir başarı örneği gösterin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}},
            {"metin": "Kullanımı performans kriteri olarak zorunlu tutun.", "etki": {"Moral": -10, "Verimlilik": 15, "Güven": -5}},
            {"metin": "Müdürle birebir oturup endişelerini dinleyin, esnek bir geçiş planı sunun.", "etki": {"Moral": 10, "Verimlilik": -5, "Güven": 10}},
            {"metin": "Konuyu merkez İK'ya devredip kendiniz müdahale etmeyin.", "etki": {"Moral": 0, "Verimlilik": -10, "Güven": -10}}
        ]
    },
    {
        "olay": "Yüksek potansiyelli bir çalışanınızın başka bir firmadan iş teklifi aldığını öğrendiniz.",
        "secenekler": [
            {"metin": "Kariyer planını öne çekin ve yetki alanını genişletin.", "etki": {"Moral": 10, "Verimlilik": 5, "Güven": 10}},
            {"metin": "Hemen maaş zammı teklif edip bağlılık isteyin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": -5}},
            {"metin": "Onunla açık bir sohbet edip gerçek beklentilerini anlamaya çalışın.", "etki": {"Moral": 10, "Verimlilik": -5, "Güven": 10}},
            {"metin": "Gitmek istiyorsa engel olmayın, yenisini bulursunuz deyin.", "etki": {"Moral": -10, "Verimlilik": -10, "Güven": -15}}
        ]
    },
    {
        "olay": "Ekip toplantısında sunduğunuz bir fikri, en güvendiğiniz çalışma arkadaşınız herkesin önünde eleştirdi.",
        "secenekler": [
            {"metin": "Toplantı sonrası özel olarak konuşup duygularınızı netçe paylaşın.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 10}},
            {"metin": "Eleştiriyi orada profesyonelce karşılayıp fikrinizi revize edin.", "etki": {"Moral": 10, "Verimlilik": 10, "Güven": 5}},
            {"metin": "Konuyu kapatıp bir daha o kişiyle toplantılarda göz teması kurmayın.", "etki": {"Moral": -10, "Verimlilik": -5, "Güven": -10}},
            {"metin": "Herkesin önünde aynı sertlikte karşılık verin.", "etki": {"Moral": -15, "Verimlilik": 5, "Güven": -10}}
        ]
    },
    {
        "olay": "Merkezden gelen yeni bir kural, çalışanların çok sevdiği bir esnekliği (mola saati esnekliği) kaldırıyor. Ekip tepkili.",
        "secenekler": [
            {"metin": "Kararın nedenlerini şeffafça açıklayın ve başka bir alanda iyileştirme sözü verin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 15}},
            {"metin": "Kararı sert şekilde uygulayın, kurallara uymayanlarla yolları ayıracağınızı belirtin.", "etki": {"Moral": -15, "Verimlilik": 10, "Güven": -10}},
            {"metin": "Bu kararı siz almadınız, 'yukarıdan geldi' deyip sorumluluktan kaçının.", "etki": {"Moral": -5, "Verimlilik": 0, "Güven": -15}},
            {"metin": "Görmezden gelip eski usulün sessizce devam etmesine izin verin.", "etki": {"Moral": 10, "Verimlilik": -15, "Güven": -5}}
        ]
    }
]

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
        Sadece JSON döndür, başka hiçbir açıklama yazma: 
        {{"olay": "...", "secenekler": [{{"metin": "...", "etki": {{"Moral": 5, "Verimlilik": -5, "Güven": 0}}}}, {{"metin": "...", "etki": {{"Moral": 0, "Verimlilik": 5, "Güven": -5}}}}, {{"metin": "...", "etki": {{"Moral": 5, "Verimlilik": 0, "Güven": 5}}}}, {{"metin": "...", "etki": {{"Moral": -10, "Verimlilik": -5, "Güven": -5}}}}]}}"""
        
        cevap = model.generate_content(istek)
        res_text = cevap.text.strip()
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0].strip()
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0].strip()
            
        data = json.loads(res_text)
        random.shuffle(data['secenekler'])
        st.session_state.last_error = None
        st.session_state.ai_success_count += 1
        return data
    except Exception as e:
        st.session_state.last_error = str(e)
        secim = random.choice(havuz)
        # Havuzdan gelen senaryonun da şıklarını karıştıralım
        secim_copy = {"olay": secim["olay"], "secenekler": secim["secenekler"].copy()}
        random.shuffle(secim_copy['secenekler'])
        return secim_copy

# --- SOL MENÜ: TEŞHİS PANELİ ---
with st.sidebar:
    st.header("🔧 Sistem Durumu")
    st.write(f"✅ AI Başarılı Çağrı: {st.session_state.ai_success_count}")
    if st.session_state.last_error:
        st.error("❌ AI Bağlantı Hatası:")
        st.code(st.session_state.last_error)
    else:
        st.success("Şu ana kadar hata yok.")
    
    st.write("---")
    if st.button("🔄 Oyunu Sıfırla"):
        st.session_state.clear()
        st.rerun()

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
