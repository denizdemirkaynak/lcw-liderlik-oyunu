import streamlit as st
import google.generativeai as genai
import json
import random
from collections import Counter

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="LCW Liderlik Simülasyonu", page_icon="💙", layout="wide")

# --- MODERN CSS TASARIMI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .stApp { background-color: #f5f7fa; }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1250px; }
    
    .hero-banner {
        background: linear-gradient(135deg, #0054a6 0%, #003d7a 100%);
        padding: 40px 50px; border-radius: 20px; margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 84, 166, 0.25);
    }
    .hero-banner h1 { color: white; font-size: 2.4em; font-weight: 800; margin: 0; }
    .hero-banner p { color: #cfe0f5; font-size: 1.1em; margin-top: 8px; font-weight: 300; }
    
    .stat-card {
        background: white; border-radius: 16px; padding: 20px 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06); border-left: 5px solid #0054a6; margin-bottom: 10px;
    }
    .stat-label { font-size: 0.85em; color: #6b7280; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .stat-value { font-size: 2em; font-weight: 700; color: #1f2937; margin: 4px 0; }
    .progress-outer { background-color: #e5e7eb; border-radius: 20px; height: 10px; width: 100%; overflow: hidden; margin-top: 8px; }
    .progress-inner { height: 100%; border-radius: 20px; transition: width 0.5s ease; }
    
    .vaka-badge {
        display: inline-block; background: #eaf1fb; color: #0054a6; 
        padding: 6px 18px; border-radius: 30px; font-weight: 600; font-size: 0.9em; margin-bottom: 15px;
    }
    
    .olay-box {
        background: white; border-radius: 16px; padding: 28px 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07); font-size: 1.1em; line-height: 1.6;
        color: #1f2937; margin-bottom: 25px; border-top: 4px solid #0054a6;
    }
    
    .stButton>button { 
        width: 100%; border-radius: 14px; min-height: 6.5em; 
        background-color: #ffffff; color: #0054a6; border: 1.5px solid #e0e4e8;
        font-weight: 500; white-space: normal; padding: 14px; font-size: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: all 0.25s ease; text-align: left;
    }
    .stButton>button:hover { 
        border-color: #0054a6; background-color: #0054a6; color: white; 
        transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,84,166,0.25);
    }
    
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #0054a6, #003d7a);
        color: white; font-weight: 700; font-size: 17px; min-height: 3.2em; border: none;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #003d7a, #0054a6); color: white; transform: translateY(-2px);
    }
    
    section[data-testid="stSidebar"] { background-color: #ffffff; }
    h1, h2, h3 { font-weight: 700; color: #1f2937; }
    
    .rapor-kart {
        background: white; border-radius: 16px; padding: 22px 26px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06); margin-bottom: 16px;
    }
    
    /* SAĞ PANEL: KARAR YOLCULUĞU */
    .journey-header {
        background: white; border-radius: 12px; padding: 14px 18px; margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); font-weight: 700; color: #0054a6; font-size: 1.05em;
    }
    .history-card {
        background: white; border-radius: 12px; padding: 14px 16px; margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 4px solid #0054a6; font-size: 0.85em;
    }
    .history-tur { font-weight: 700; color: #0054a6; font-size: 0.85em; margin-bottom: 4px; }
    .history-tip {
        display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.72em;
        font-weight: 600; color: white; margin-bottom: 6px;
    }
    .history-metin { color: #4b5563; font-style: italic; font-size: 0.82em; margin-bottom: 8px; line-height: 1.4; }
    .history-stat-row { display: flex; justify-content: space-between; font-size: 0.82em; margin-bottom: 3px; }
    .stat-up { color: #16a34a; font-weight: 700; }
    .stat-down { color: #dc2626; font-weight: 700; }
    .stat-same { color: #9ca3af; font-weight: 600; }
    .empty-journey { color: #9ca3af; font-size: 0.9em; text-align: center; padding: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- API YAPILANDIRMASI ---
API_KEY = 'AQ.Ab8RN6LpvpinBuDLv3Qo6n0kLMOLt_fN6DWQX4rHkjAkYvKkCA'
genai.configure(api_key=API_KEY)

MODEL_ADI = 'gemini-1.5-flash'
generation_config = {"temperature": 1.4, "top_p": 0.95, "top_k": 40}
model = genai.GenerativeModel(MODEL_ADI, generation_config=generation_config)

# --- SİSTEM HAFIZASI ---
if 'started' not in st.session_state:
    st.session_state.started = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
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
if 'gecmis_konular' not in st.session_state:
    st.session_state.gecmis_konular = []
if 'secim_gecmisi' not in st.session_state:
    st.session_state.secim_gecmisi = []
if 'karar_gecmisi' not in st.session_state:
    st.session_state.karar_gecmisi = []   # Sağ paneldeki "Karar Yolculuğu" için detaylı kayıt

temalar = ["Performans Yönetimi", "Çalışan Bağlılığı", "Kriz Yönetimi", "Yenilikçilik",
           "Zor Kişiliklerle İletişim", "Etik İkilemler", "Mağaza Operasyonu", "Uzaktan Yönetim",
           "İşe Alım Kararları", "Terfi ve Adalet", "Müşteri Şikayeti Yönetimi", "Bütçe Kısıtlaması"]

karakterler = ["yeni işe başlayan bir kasiyer", "10 yıllık kıdemli bir reyon sorumlusu",
               "stajyer bir çalışan", "vardiya amiri", "depo sorumlusu", "kıdemli bir mağaza müdür yardımcısı"]

tip_renk = {"Demokratik": "#2563eb", "Otoriter": "#dc2626", "Koçvari": "#16a34a", "Kaçınmacı": "#6b7280", "Belirsiz": "#9ca3af"}

# --- YEDEK SENARYO HAVUZU ---
havuz = [
    {
        "olay": "Ekibinizdeki iki kıdemli çalışan, yeni bir iş süreci üzerinde fikir ayrılığı yaşıyor ve bu durum ofis huzurunu bozuyor.",
        "secenekler": [
            {"metin": "İkisini aynı anda odaya çağırıp ortak bir çözüm bulana kadar çıkmayacağınızı söyleyin.", "etki": {"Moral": -5, "Verimlilik": 5, "Güven": 10}, "tip": "Otoriter"},
            {"metin": "Fikirlerini ayrı ayrı dinleyip, size en uygun olanı siz seçin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": -5}, "tip": "Otoriter"},
            {"metin": "Tarafsız bir moderatör eşliğinde fikirlerini tüm ekibe sunmalarını isteyin.", "etki": {"Moral": 5, "Verimlilik": -5, "Güven": 10}, "tip": "Demokratik"},
            {"metin": "Zamanla düzeleceğini düşünüp müdahale etmeyin.", "etki": {"Moral": -10, "Verimlilik": -5, "Güven": -10}, "tip": "Kaçınmacı"}
        ]
    },
    {
        "olay": "Mağazada yoğun kampanya dönemi başladı ama 2 personel rapor aldı. Kalan ekip çok gergin ve yorgun.",
        "secenekler": [
            {"metin": "Merkezden geçici destek isteyin, süreç biraz yavaşlasa da ekibi yormayın.", "etki": {"Moral": 10, "Verimlilik": -5, "Güven": 5}, "tip": "Koçvari"},
            {"metin": "Vardiyaları uzatın ve ekstra mesai ücreti sözü verin.", "etki": {"Moral": -5, "Verimlilik": 15, "Güven": 0}, "tip": "Otoriter"},
            {"metin": "Siz de sahaya inip satış desteği verin, örnek liderlik yapın.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 5}, "tip": "Demokratik"},
            {"metin": "Hedefleri revize etmeden mevcut ekiple devam etmelerini isteyin.", "etki": {"Moral": -15, "Verimlilik": 5, "Güven": -10}, "tip": "Kaçınmacı"}
        ]
    },
    {
        "olay": "Yeni bir dijital İK platformuna geçiliyor. Kıdemli bir müdür 'eski usul devam edelim' diyerek direniyor.",
        "secenekler": [
            {"metin": "Gönüllü bir pilot grup kurup küçük bir başarı örneği gösterin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
            {"metin": "Kullanımı performans kriteri olarak zorunlu tutun.", "etki": {"Moral": -10, "Verimlilik": 15, "Güven": -5}, "tip": "Otoriter"},
            {"metin": "Müdürle birebir oturup endişelerini dinleyin, esnek bir geçiş planı sunun.", "etki": {"Moral": 10, "Verimlilik": -5, "Güven": 10}, "tip": "Demokratik"},
            {"metin": "Konuyu merkez İK'ya devredip kendiniz müdahale etmeyin.", "etki": {"Moral": 0, "Verimlilik": -10, "Güven": -10}, "tip": "Kaçınmacı"}
        ]
    },
    {
        "olay": "Yüksek potansiyelli bir çalışanınızın başka bir firmadan iş teklifi aldığını öğrendiniz.",
        "secenekler": [
            {"metin": "Kariyer planını öne çekin ve yetki alanını genişletin.", "etki": {"Moral": 10, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
            {"metin": "Hemen maaş zammı teklif edip bağlılık isteyin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": -5}, "tip": "Otoriter"},
            {"metin": "Onunla açık bir sohbet edip gerçek beklentilerini anlamaya çalışın.", "etki": {"Moral": 10, "Verimlilik": -5, "Güven": 10}, "tip": "Demokratik"},
            {"metin": "Gitmek istiyorsa engel olmayın, yenisini bulursunuz deyin.", "etki": {"Moral": -10, "Verimlilik": -10, "Güven": -15}, "tip": "Kaçınmacı"}
        ]
    },
    {
        "olay": "Ekip toplantısında sunduğunuz bir fikri, en güvendiğiniz çalışma arkadaşınız herkesin önünde eleştirdi.",
        "secenekler": [
            {"metin": "Toplantı sonrası özel olarak konuşup duygularınızı netçe paylaşın.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 10}, "tip": "Demokratik"},
            {"metin": "Eleştiriyi orada profesyonelce karşılayıp fikrinizi revize edin.", "etki": {"Moral": 10, "Verimlilik": 10, "Güven": 5}, "tip": "Koçvari"},
            {"metin": "Konuyu kapatıp bir daha o kişiyle toplantılarda göz teması kurmayın.", "etki": {"Moral": -10, "Verimlilik": -5, "Güven": -10}, "tip": "Kaçınmacı"},
            {"metin": "Herkesin önünde aynı sertlikte karşılık verin.", "etki": {"Moral": -15, "Verimlilik": 5, "Güven": -10}, "tip": "Otoriter"}
        ]
    },
    {
        "olay": "Merkezden gelen yeni bir kural, çalışanların çok sevdiği bir esnekliği (mola saati esnekliği) kaldırıyor. Ekip tepkili.",
        "secenekler": [
            {"metin": "Kararın nedenlerini şeffafça açıklayın ve başka bir alanda iyileştirme sözü verin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 15}, "tip": "Demokratik"},
            {"metin": "Kararı sert şekilde uygulayın, kurallara uymayanlarla yolları ayıracağınızı belirtin.", "etki": {"Moral": -15, "Verimlilik": 10, "Güven": -10}, "tip": "Otoriter"},
            {"metin": "Bu kararı siz almadınız, 'yukarıdan geldi' deyip sorumluluktan kaçının.", "etki": {"Moral": -5, "Verimlilik": 0, "Güven": -15}, "tip": "Kaçınmacı"},
            {"metin": "Görmezden gelip eski usulün sessizce devam etmesine izin verin.", "etki": {"Moral": 10, "Verimlilik": -15, "Güven": -5}, "tip": "Kaçınmacı"}
        ]
    }
]

def aciklama_yon(v):
    if v > 0: return "arttı"
    elif v < 0: return "azaldı"
    return "değişmedi"

# Sayısal değişimi, hikaye diline çeviren ipuçları (AI'ya "Moral" kelimesini doğrudan söylemeden anlatı context'i vermek için)
narratif_ipuclari = {
    ("Moral", "arttı"): "ekibin motivasyonu ve enerjisi gözle görülür şekilde yükseldi",
    ("Moral", "azaldı"): "ekipte hafif bir huzursuzluk ve gerginlik sezildi",
    ("Verimlilik", "arttı"): "operasyonel sonuçlar ve iş akışı belirgin şekilde iyileşti",
    ("Verimlilik", "azaldı"): "günlük işlerde küçük aksamalar ve yavaşlamalar ortaya çıktı",
    ("Güven", "arttı"): "çalışanlar sizinle daha açık ve rahat iletişim kurmaya başladı",
    ("Güven", "azaldı"): "bazı çalışanlarda size karşı hafif bir güven sarsıntısı oluştu",
}

def onceki_karar_ozeti_uret(karar):
    """Bir önceki kararın etkilerini, oyun terimi kullanmadan hikaye diline çevirir."""
    if not karar:
        return None
    ipuclari = []
    for k, v in karar['etki'].items():
        if abs(v) >= 5:  # küçük etkileri atla, sadece belirgin olanları anlat
            yon = aciklama_yon(v)
            ipucu = narratif_ipuclari.get((k, yon))
            if ipucu:
                ipuclari.append(ipucu)
    if not ipuclari:
        return f"Bir önceki turda '{karar['metin']}' yaklaşımını seçtiniz ve durum genel olarak stabil kaldı."
    return f"Bir önceki turda '{karar['metin']}' yaklaşımını seçtiniz. Bunun sonucunda {', '.join(ipuclari)}."


def kriz_uret():
    tema = random.choice(temalar)
    karakter = random.choice(karakterler)
    onceki_ozet = ", ".join(st.session_state.gecmis_konular[-3:]) if st.session_state.gecmis_konular else "yok"

    # Bir önceki kararın hikaye özetini al (devamlılık için)
    onceki_karar = st.session_state.karar_gecmisi[-1] if st.session_state.karar_gecmisi else None
    baglanti_ozeti = onceki_karar_ozeti_uret(onceki_karar)

    baglanti_talimati = ""
    if baglanti_ozeti:
        baglanti_talimati = f"""
        DEVAMLILIK BİLGİSİ: {baglanti_ozeti}
        Yeni senaryonun İLK CÜMLESİNDE, bu önceki kararın doğal bir yansımasını (ekip tepkisi, gelişen bir durum, bir sonuç) 
        hikayenin doğal bir parçası olarak anlat. ASLA "Moral", "Verimlilik", "Güven" gibi oyun terimlerini doğrudan kullanma; 
        bunun yerine gerçekçi, insani bir anlatım kullan. Sonrasında yeni krizi/durumu sun.
        """

    try:
        istek = f"""Sen üst düzey, tecrübeli ve YARATICI bir LCW (LC Waikiki) Liderlik Koçusun. 
        Konu teması: {tema}. 
        Senaryoda mutlaka şu karakter yer alsın: {karakter}. 
        
        Daha önce şu konular kullanıldı, bunları TEKRARLAMA: {onceki_ozet}.
        
        {baglanti_talimati}
        
        Gerçekçi, özgün, sürpriz detaylar içeren, sıradanlıktan uzak bir yönetim senaryosu yaz (2-4 cümle, somut detaylar içersin, isim kullanabilirsin).
        
        4 farklı liderlik tarzını temsil eden seçenekler sun ve her birine bir "tip" etiketi ver:
        1. "Demokratik" (Güven artırır, Verimlilik bazen yavaşlar)
        2. "Otoriter" (Verimlilik artırır, Moral bazen düşer)
        3. "Koçvari" (Gelişim odaklı, dengeli etki)
        4. "Kaçınmacı" (Risk almaz, genelde skorları düşürür)
        
        ÖNEMLİ: Hiçbir seçenek 'mükemmel' olmasın, her birinin bir bedeli olsun. Etkiler -15 ile +15 arasında olsun.
        Seçeneklerin metinleri de birbirine çok bariz zıt olmasın, gerçekçi ve yorumsal olsun (kararı okumadan tahmin edilemesin).
        
        SADECE şu JSON formatında döndür, başka hiçbir açıklama ekleme:
        {{"olay": "...", "secenekler": [
            {{"metin": "...", "etki": {{"Moral": 5, "Verimlilik": -5, "Güven": 0}}, "tip": "Demokratik"}},
            {{"metin": "...", "etki": {{"Moral": 0, "Verimlilik": 5, "Güven": -5}}, "tip": "Otoriter"}},
            {{"metin": "...", "etki": {{"Moral": 5, "Verimlilik": 0, "Güven": 5}}, "tip": "Koçvari"}},
            {{"metin": "...", "etki": {{"Moral": -10, "Verimlilik": -5, "Güven": -5}}, "tip": "Kaçınmacı"}}
        ]}}"""

        cevap = model.generate_content(istek)
        res_text = cevap.text.strip()
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0].strip()
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0].strip()

        data = json.loads(res_text)
        random.shuffle(data['secenekler'])

        st.session_state.gecmis_konular.append(f"{tema} - {data['olay'][:50]}")
        st.session_state.last_error = None
        st.session_state.ai_success_count += 1
        return data

    except Exception as e:
        st.session_state.last_error = str(e)
        secim = random.choice(havuz)
        secim_copy = {"olay": secim["olay"], "secenekler": [dict(s) for s in secim["secenekler"]]}
        random.shuffle(secim_copy['secenekler'])
        return secim_copy


def final_rapor_uret(stats, secim_gecmisi):
    ortalama = sum(stats.values()) / 3
    tip_sayaci = Counter(secim_gecmisi)
    baskin_tip = tip_sayaci.most_common(1)[0][0] if tip_sayaci else "Belirsiz"

    tip_aciklamalari = {
        "Demokratik": "Kararlarınızda ekibinizin fikrini almayı ve katılımcı bir yönetim tarzını önceliklendirdiniz. Bu, uzun vadede güçlü bir güven ortamı kurar ama bazı acil durumlarda karar hızınızı yavaşlatabilir.",
        "Otoriter": "Çoğunlukla hızlı ve net kararlar alarak operasyonel sonuçlara odaklandınız. Kısa vadede verimlilik sağlasa da, sürekli bu tarz ekipte tükenmişlik ve güven kaybına yol açabilir.",
        "Koçvari": "Çalışanlarınızın gelişimine ve uzun vadeli potansiyeline yatırım yapan bir yaklaşım sergilediniz. Bu tarz, sürdürülebilir başarı için en dengeli yöntemlerden biridir.",
        "Kaçınmacı": "Zor kararlar karşısında çoğunlukla geri çekilmeyi veya sorumluluğu ertelemeyi tercih ettiniz. Bu durum kısa vadede rahatlık sağlasa da ekipte belirsizlik ve güvensizlik yaratabilir.",
        "Belirsiz": "Henüz yeterli veri toplanmadı."
    }

    metrik_yorumlari = {}
    for metrik, deger in stats.items():
        if deger >= 75:
            seviye = "Güçlü"
        elif deger >= 50:
            seviye = "Orta"
        else:
            seviye = "Zayıf"

        aciklamalar = {
            "Moral": {
                "Güçlü": "Ekibiniz kendini değerli ve motive hissediyor. Bu, düşük personel devir hızı ve yüksek işbirliği anlamına gelir.",
                "Orta": "Ekip morali dengeli ama kırılgan. Küçük bir kriz bile motivasyonu hızla düşürebilir.",
                "Zayıf": "Ekibinizde tükenmişlik belirtileri riski var. Düşük moral genellikle performans düşüşü ve istifa oranlarında artışla sonuçlanır."
            },
            "Verimlilik": {
                "Güçlü": "Operasyonel hedeflere ulaşma konusunda güçlüsünüz, ekip süreçleri hızlı yönetiyor.",
                "Orta": "İşler yürüyor ama optimize edilebilecek gecikmeler ve verimsizlikler mevcut.",
                "Zayıf": "Operasyonel aksaklıklar riski yüksek; kararlarınız süreçleri yavaşlatmış olabilir."
            },
            "Güven": {
                "Güçlü": "Ekibiniz sizi şeffaf ve adil buluyor, kritik anlarda sizinle açık iletişim kuruyorlar.",
                "Orta": "Güven var ama sınırlı; ekip bazı konularda sizinle tam açık olmayabilir.",
                "Zayıf": "Ekip-lider güveni zedelenmiş durumda. Bu, geri bildirim akışını ve dürüst iletişimi ciddi şekilde azaltır."
            }
        }
        metrik_yorumlari[metrik] = f"**{metrik} (%{deger} - {seviye}):** {aciklamalar[metrik][seviye]}"

    return ortalama, baskin_tip, tip_aciklamalari[baskin_tip], metrik_yorumlari, tip_sayaci


def renk_belirle(deger):
    if deger >= 70: return "#16a34a"
    elif deger >= 40: return "#f59e0b"
    else: return "#dc2626"


def stat_karti_ciz(label, deger, icon):
    renk = renk_belirle(deger)
    st.markdown(f"""
        <div class="stat-card" style="border-left-color:{renk};">
            <div class="stat-label">{icon} {label}</div>
            <div class="stat-value">%{deger}</div>
            <div class="progress-outer">
                <div class="progress-inner" style="width:{deger}%; background:{renk};"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def karar_kartı_ciz(kayit):
    tip = kayit.get('tip', 'Belirsiz')
    renk = tip_renk.get(tip, "#9ca3af")
    metin_kisa = kayit['metin'][:65] + ("..." if len(kayit['metin']) > 65 else "")

    stat_satirlari = ""
    for k, v in kayit['etki'].items():
        if v > 0:
            cls, ok = "stat-up", f"▲ +{v}"
        elif v < 0:
            cls, ok = "stat-down", f"▼ {v}"
        else:
            cls, ok = "stat-same", "→ 0"
        stat_satirlari += f'<div class="history-stat-row"><span>{k}</span><span class="{cls}">{ok}</span></div>'

    st.markdown(f"""
        <div class="history-card" style="border-left-color:{renk};">
            <div class="history-tur">Vaka {kayit['tur']}</div>
            <div class="history-tip" style="background:{renk};">{tip}</div>
            <div class="history-metin">"{metin_kisa}"</div>
            {stat_satirlari}
        </div>
    """, unsafe_allow_html=True)


# --- SOL MENÜ: TEŞHİS PANELİ ---
with st.sidebar:
    st.header("🔧 Sistem Durumu")
    st.write(f"✅ AI Başarılı Çağrı: {st.session_state.ai_success_count}")
    st.write(f"🤖 Kullanılan Model: `{MODEL_ADI}`")
    if st.session_state.last_error:
        st.error("❌ AI Bağlantı Hatası:")
        st.code(st.session_state.last_error)
    else:
        st.success("Şu ana kadar hata yok.")

    st.write("---")
    if st.button("🔄 Oyunu Sıfırla"):
        st.session_state.clear()
        st.rerun()


# ==========================================================
# ============  1. AŞAMA: KARŞILAMA (ONBOARDING) EKRANI  ==
# ==========================================================
if not st.session_state.started:

    st.markdown("""
        <div class="hero-banner">
            <h1>💙 LC Waikiki Liderlik Simülasyonu</h1>
            <p>Gerçek yönetim senaryolarıyla liderlik becerilerinizi test edin.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("Nasıl Oynanır? 🎯")
        st.markdown("""
        - Karşınıza toplam **10 farklı liderlik vakası** çıkacak.  
        - Her vakada **4 farklı karar seçeneği** sunulacak.  
        - Verdiğiniz kararlar birbirine **bağlı bir hikaye** oluşturacak; bir önceki kararınızın yansımalarını bir sonraki vakada göreceksiniz.  
        - Sağ panelde, verdiğiniz her kararın etkilerini **anlık olarak** takip edebileceksiniz.  
        - Sonunda size özel bir **"Liderlik Karnesi"** hazırlanacak.

        ⚠️ *Unutmayın: Hiçbir seçenek mükemmel değildir. Gerçek liderlik, doğru dengeleri kurmaktır.*
        """)

    with col2:
        st.subheader("📝 Katılımcı Bilgileri")
        with st.form("giris_formu"):
            ad_soyad = st.text_input("Ad Soyad *", placeholder="Örn: Deniz Demirkaynak")
            gorev = st.text_input("Görev / Departman (opsiyonel)", placeholder="Örn: Mağaza Müdürü")
            gonder = st.form_submit_button("🚀 Simülasyonu Başlat")

            if gonder:
                if ad_soyad.strip() == "":
                    st.warning("Lütfen devam etmek için adınızı ve soyadınızı girin.")
                else:
                    st.session_state.user_name = ad_soyad.strip()
                    st.session_state.user_role = gorev.strip()
                    st.session_state.started = True
                    st.rerun()

    st.stop()


# ==========================================================
# ==================  2. AŞAMA: OYUN EKRANI  ===============
# ==========================================================

ust_bilgi = f"👤 {st.session_state.user_name}"
if st.session_state.user_role:
    ust_bilgi += f"  •  {st.session_state.user_role}"

st.markdown(f"""
    <div class="hero-banner">
        <h1>💙 LC Waikiki Liderlik Simülasyonu</h1>
        <p>{ust_bilgi}</p>
    </div>
""", unsafe_allow_html=True)

# Ana içerik (sol) + Karar Yolculuğu (sağ) sütunları
col_main, col_side = st.columns([2.6, 1])

with col_main:
    c1, c2, c3 = st.columns(3)
    with c1: stat_karti_ciz("Moral", st.session_state.stats['Moral'], "😊")
    with c2: stat_karti_ciz("Verimlilik", st.session_state.stats['Verimlilik'], "📈")
    with c3: stat_karti_ciz("Güven", st.session_state.stats['Güven'], "🤝")

    st.write("")

    if st.session_state.tur <= 10:
        if st.session_state.current_scenario is None:
            with st.spinner("Yeni liderlik vakası hazırlanıyor..."):
                st.session_state.current_scenario = kriz_uret()

        current = st.session_state.current_scenario

        st.markdown(f'<div class="vaka-badge">VAKA {st.session_state.tur} / 10</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="olay-box">{current["olay"]}</div>', unsafe_allow_html=True)

        st.markdown("##### Liderlik Yaklaşımınız:")

        cb1, cb2 = st.columns(2)
        for i, s in enumerate(current['secenekler']):
            with (cb1 if i % 2 == 0 else cb2):
                if st.button(s['metin'], key=f"v_{st.session_state.tur}_{i}"):
                    for k, v in s['etki'].items():
                        st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))

                    st.session_state.secim_gecmisi.append(s.get('tip', 'Belirsiz'))

                    # Sağ paneldeki karar yolculuğu için kayıt ekle
                    st.session_state.karar_gecmisi.append({
                        "tur": st.session_state.tur,
                        "metin": s['metin'],
                        "tip": s.get('tip', 'Belirsiz'),
                        "etki": s['etki']
                    })

                    st.session_state.tur += 1
                    st.session_state.current_scenario = None
                    st.rerun()

    else:
        st.balloons()
        st.success(f"🏁 Tebrikler {st.session_state.user_name}, 10 Günlük Liderlik Maratonunu Tamamladınız!")

        ortalama, baskin_tip, tip_metni, metrik_yorumlari, tip_sayaci = final_rapor_uret(
            st.session_state.stats, st.session_state.secim_gecmisi
        )

        st.markdown(f"""
            <div class="rapor-kart" style="text-align:center;">
                <div class="stat-label">FİNAL LİDERLİK ENDEKSİ</div>
                <div style="font-size:3em; font-weight:800; color:{renk_belirle(int(ortalama))};">%{int(ortalama)}</div>
                <div style="color:#6b7280;">Bu skor, Moral + Verimlilik + Güven ortalamasıdır.</div>
            </div>
        """, unsafe_allow_html=True)

        st.write("### 📊 Metrik Bazlı Detaylı Analiz")
        for metrik, yorum in metrik_yorumlari.items():
            st.markdown(f'<div class="rapor-kart">{yorum}</div>', unsafe_allow_html=True)

        st.write("### 🧭 Baskın Liderlik Tarzınız")
        st.markdown(f"""
            <div class="rapor-kart">
                <b>{baskin_tip}</b> ({tip_sayaci.get(baskin_tip, 0)}/10 kararınızda bu yaklaşımı sergilediniz)<br><br>
                {tip_metni}
            </div>
        """, unsafe_allow_html=True)

        st.write("### 📈 Tüm Kararlarınızın Dağılımı")
        for tip, sayi in tip_sayaci.items():
            st.write(f"**{tip}** — {sayi} kez")
            st.progress(sayi / 10)

        st.write("---")
        if ortalama > 75:
            st.markdown('<div class="rapor-kart">💎 <b>Genel Değerlendirme:</b> Dengeleri harika koruyan, stratejik bir lidersiniz.</div>', unsafe_allow_html=True)
        elif ortalama > 50:
            st.markdown('<div class="rapor-kart">📈 <b>Genel Değerlendirme:</b> Sonuç odaklısınız ama insan faktörüne biraz daha ağırlık vermelisiniz.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="rapor-kart">⚠️ <b>Genel Değerlendirme:</b> Kararlarınızın uzun vadeli etkilerini daha dikkatli tartmalısınız.</div>', unsafe_allow_html=True)

        if st.button("Simülasyonu Baştan Başlat"):
            st.session_state.clear()
            st.rerun()

# --- SAĞ PANEL: KARAR YOLCULUĞU ---
with col_side:
    st.markdown('<div class="journey-header">📜 Karar Yolculuğunuz</div>', unsafe_allow_html=True)

    if not st.session_state.karar_gecmisi:
        st.markdown('<div class="empty-journey">Henüz bir karar vermediniz.<br>İlk kararınızı verdiğinizde burada görünecek.</div>', unsafe_allow_html=True)
    else:
        for kayit in st.session_state.karar_gecmisi:
            karar_kartı_ciz(kayit)
