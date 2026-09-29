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
        padding: 40px 50px; border-radius: 20px; margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 84, 166, 0.25);
    }
    .hero-banner h1 { color: white; font-size: 2.4em; font-weight: 800; margin: 0; }
    .hero-banner p { color: #cfe0f5; font-size: 1.1em; margin-top: 8px; font-weight: 300; }
    
    .hedef-banner {
        background: #fffbeb; border: 1.5px solid #fbbf24; border-radius: 14px;
        padding: 14px 22px; margin-bottom: 25px; color: #92400e; font-weight: 600; font-size: 0.95em;
    }
    
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
    .dept-badge {
        display: inline-block; background: #fef3c7; color: #92400e; 
        padding: 6px 18px; border-radius: 30px; font-weight: 600; font-size: 0.85em; margin-bottom: 15px; margin-left: 8px;
    }
    .karakter-badge {
        display: inline-block; background: #ecfdf5; color: #047857; 
        padding: 6px 18px; border-radius: 30px; font-weight: 600; font-size: 0.85em; margin-bottom: 15px; margin-left: 8px;
    }
    
    .olay-box {
        background: white; border-radius: 16px; padding: 28px 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07); font-size: 1.1em; line-height: 1.6;
        color: #1f2937; margin-bottom: 25px; border-top: 4px solid #0054a6;
    }
    
    /* BUTON TASARIMI + TAŞMA/KESİLME SORUNU KESİN ÇÖZÜMÜ */
    .stButton>button { 
        width: 100%; border-radius: 14px; height: auto !important; min-height: 6.5em; 
        background-color: #ffffff; color: #0054a6; border: 1.5px solid #e0e4e8;
        font-weight: 500; white-space: normal !important; padding: 16px; font-size: 14.5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: all 0.25s ease; text-align: left;
        line-height: 1.45; overflow: visible !important; word-wrap: break-word;
    }
    .stButton > button * {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
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
    
    .karakter-kart {
        background: white; border-radius: 12px; padding: 12px 14px; margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 4px solid #047857; font-size: 0.82em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API YAPILANDIRMASI ---
API_KEY = 'AQ.Ab8RN6LpvpinBuDLv3Qo6n0kLMOLt_fN6DWQX4rHkjAkYvKkCA'
genai.configure(api_key=API_KEY)

MODEL_ADI = 'gemini-1.5-flash'
generation_config = {"temperature": 1.6, "top_p": 0.97, "top_k": 60}
model = genai.GenerativeModel(MODEL_ADI, generation_config=generation_config)

# --- DEPARTMAN TANIMLARI ---
DEPARTMANLAR = {
    "Mağazacılık": {
        "icon": "🏬",
        "temalar": ["Mağaza Operasyonu", "Müşteri Şikayeti Yönetimi", "Vardiya Planlama", "Kampanya Yönetimi",
                    "Vitrin ve Görsel Merchandising", "Stok Sayımı", "Kasa Farkı Yönetimi", "Hırsızlık ve Kayıp Yönetimi"],
        "karakterler": ["kasiyer", "reyon sorumlusu", "stajyer çalışan", "vardiya amiri", "depo sorumlusu",
                         "mağaza müdür yardımcısı", "görsel merchandising uzmanı"],
        "baglamlar": ["yoğun bir hafta sonu indirim kampanyası sırasında", "yıl sonu stok sayımı gecesinde",
                      "AVM'deki büyük indirim haftasında", "okula dönüş sezonunun zirvesinde",
                      "ani bir bölge müdürü ziyareti sırasında", "yeni sezon vitrin değişiminin son gününde"]
    },
    "Tedarik Zinciri": {
        "icon": "🚚",
        "temalar": ["Depo Yönetimi", "Sevkiyat Gecikmeleri", "Lojistik Kriz Yönetimi", "Envanter Optimizasyonu",
                    "Tedarikçi ile Anlaşmazlık", "Mevsimsel Talep Dalgalanması", "Depo İş Güvenliği"],
        "karakterler": ["depo operasyon şefi", "sevkiyat planlama uzmanı", "lojistik koordinatörü",
                         "forklift operatörü ekip lideri", "envanter analisti", "gümrük süreçleri sorumlusu"],
        "baglamlar": ["kritik bir sevkiyatın gümrükte 3 gündür beklediği bir durumda", "depo kapasitesinin sınırına dayandığı bir dönemde",
                      "yılın en yoğun sevkiyat haftasında", "yeni bir depo yönetim sistemine geçiş sürecinde",
                      "bir tedarikçinin son anda teslimat tarihini değiştirdiği bir durumda"]
    },
    "Satın Alma": {
        "icon": "🛒",
        "temalar": ["Tedarikçi Müzakeresi", "Maliyet Optimizasyonu", "Kalite Kontrol Anlaşmazlığı",
                    "Yeni Tedarikçi Seçimi", "Bütçe Aşımı", "Numune Onay Süreci", "Sürdürülebilirlik Kriterleri"],
        "karakterler": ["satın alma uzmanı", "satın alma asistanı", "kategori yöneticisi",
                         "kalite kontrol sorumlusu", "yurt dışı tedarikçi temsilcisi"],
        "baglamlar": ["sezon başlamasına 2 hafta kala", "ana tedarikçinin ani fiyat artışı bildirdiği bir günde",
                      "numune onaylandıktan sonra üretimde kalite sorunu çıktığında", "yıllık tedarikçi değerlendirme toplantısı öncesinde",
                      "döviz kurunun ani yükseldiği bir dönemde"]
    },
    "İnsan Kaynakları": {
        "icon": "👥",
        "temalar": ["İşe Alım Kararları", "Terfi ve Adalet", "Performans Değerlendirme", "Çalışan Bağlılığı",
                    "Etik İkilemler", "İşten Çıkarma Süreci", "Eğitim ve Gelişim", "Mobbing İddiası"],
        "karakterler": ["İK uzmanı", "İK iş ortağı", "işe alım uzmanı", "eğitim ve gelişim sorumlusu",
                         "bordro uzmanı", "organizasyonel gelişim danışmanı"],
        "baglamlar": ["yıllık performans değerlendirme dönemi ortasında", "anonim bir şikayet mektubu geldiğinde",
                      "iki eşit performanslı çalışan aynı terfiyi beklerken", "toplu işe alım süreci yürütülürken",
                      "bir çalışanın istifasının ardındaki gerçek sebep ortaya çıktığında"]
    },
    "Pazarlama": {
        "icon": "📣",
        "temalar": ["Kampanya Krizi", "Sosyal Medya Yönetimi", "Marka İtibarı", "Influencer İş Birliği",
                    "Reklam Bütçesi Anlaşmazlığı", "Ürün Lansmanı", "Kriz İletişimi"],
        "karakterler": ["dijital pazarlama uzmanı", "marka yöneticisi", "sosyal medya editörü",
                         "pazarlama asistanı", "influencer ilişkileri sorumlusu"],
        "baglamlar": ["büyük bir kampanya lansmanına 24 saat kala", "işbirliği yapılan bir influencer'ın tartışmalı paylaşımından sonra",
                      "sosyal medyada markayla ilgili olumsuz bir trend başladığında", "reklam bütçesinin yarısı harcandıktan sonra beklenen sonuç gelmediğinde",
                      "rakip firmanın beklenmedik bir kampanya yaptığı günde"]
    },
    "Finans": {
        "icon": "💰",
        "temalar": ["Bütçe Kısıtlaması", "Maliyet Raporlama Hatası", "Yatırım Kararı", "Nakit Akışı Krizi",
                    "Denetim Süreci", "Departmanlar Arası Bütçe Çatışması"],
        "karakterler": ["finansal analist", "muhasebe uzmanı", "bütçe planlama sorumlusu",
                         "iç denetim uzmanı", "finans asistanı"],
        "baglamlar": ["üst yönetime sunumdan bir gün önce ciddi bir rapor hatası fark edildiğinde",
                      "yıl sonu bütçe kapanışına günler kala", "bir departmanın bütçesini aştığı ve ek onay istediği durumda",
                      "beklenmedik bir denetimin duyurulduğu günde", "nakit akışında geçici bir sıkışma yaşandığında"]
    },
    "Bilgi Teknolojileri": {
        "icon": "💻",
        "temalar": ["Sistem Arızası Krizi", "Yeni Yazılım Geçişi", "Siber Güvenlik Riski", "Proje Gecikmesi",
                    "Ekip İçi Teknik Anlaşmazlık", "Otomasyon Projesi"],
        "karakterler": ["yazılım geliştirici", "sistem yöneticisi", "proje yöneticisi",
                         "IT stajyeri", "siber güvenlik uzmanı"],
        "baglamlar": ["kritik bir güncelleme sırasında tüm mağaza kasalarının çöktüğü anda",
                      "yeni bir otomasyon projesine ekipten sessiz bir direniş geldiğinde",
                      "bir güvenlik açığının fark edildiği gece yarısı", "proje teslim tarihine 3 gün kala kritik bir hata bulunduğunda",
                      "iki kıdemli geliştiricinin mimari tercih konusunda anlaşamadığı bir durumda"]
    },
    "E-Ticaret": {
        "icon": "🌐",
        "temalar": ["Web Sitesi Krizi", "İade ve Müşteri Memnuniyeti", "Kargo Gecikmesi", "Online Kampanya Yönetimi",
                    "Stok-Web Senkronizasyon Hatası", "Müşteri Deneyimi İyileştirme"],
        "karakterler": ["e-ticaret operasyon uzmanı", "müşteri deneyimi sorumlusu", "dijital kanal yöneticisi",
                         "e-ticaret asistanı", "kargo süreçleri koordinatörü"],
        "baglamlar": ["büyük indirim gününde (11.11 tarzı) site trafiği beklenenin 5 katına çıktığında",
                      "stok-web senkronizasyon hatası yüzünden tükenen ürünler satılmaya devam ettiğinde",
                      "kargo firmasının ardı ardına gecikme yaptığı bir haftada", "sosyal medyada bir müşteri şikayeti viral olduğunda",
                      "yeni web sitesi tasarımına geçişin ilk gününde"]
    }
}

# --- KARAKTER SİSTEMİ İÇİN VERİ HAVUZLARI ---
ISIM_HAVUZU = ["Ayşe Yıldız", "Mehmet Kara", "Elif Demir", "Can Öztürk", "Zeynep Aydın",
               "Burak Şahin", "Selin Kaya", "Emre Yılmaz", "Deren Aksoy", "Merve Çelik",
               "Kaan Polat", "Ece Arslan"]

KISILIK_OZELLIKLERI = [
    "disiplinli ama esnek olmayan", "yaratıcı fakat dağınık", "çok çalışkan ama özgüvensiz",
    "karizmatik ama bazen otoriteye karşı gelen", "sadık ama değişime kapalı",
    "hırslı ve hızlı öğrenen", "duygusal zekası yüksek, çatışmadan kaçınan",
    "detaycı ve mükemmeliyetçi", "esprili ama zaman yönetimi zayıf", "sessiz ama gözlemci ve stratejik"
]

# --- SİSTEM HAFIZASI ---
defaults = {
    'started': False, 'user_name': "", 'user_department': "", 'oyun_uzunlugu': 10, 'hedef': None,
    'stats': {'Moral': 60, 'Verimlilik': 60, 'Güven': 60},
    'tur': 1, 'current_scenario': None, 'last_error': None, 'ai_success_count': 0,
    'gecmis_konular': [], 'secim_gecmisi': [], 'karar_gecmisi': [], 'havuz_kullanilan': [],
    'karakter_havuzu': []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

tip_renk = {"Demokratik": "#2563eb", "Otoriter": "#dc2626", "Koçvari": "#16a34a", "Kaçınmacı": "#6b7280", "Belirsiz": "#9ca3af"}
TUM_TIPLER = ["Demokratik", "Otoriter", "Koçvari", "Kaçınmacı"]

# --- YEDEK SENARYO HAVUZU (AI çalışmazsa devreye girer) ---
havuz = [
    {"departman": "Mağazacılık", "olay": "Kampanya haftasında bir üründe etiket hatası çıktı; kasada indirim yansımıyor ve müşteri kuyruğu büyüyor.",
     "secenekler": [
        {"metin": "Kasiyerlere manuel indirim yetkisi verip kuyruğu hemen eritin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 5}, "tip": "Otoriter"},
        {"metin": "Sistemi düzeltene kadar özür dileyip müşterilere kupon verin.", "etki": {"Moral": 5, "Verimlilik": -5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Ekiple birlikte hatayı analiz edip anlık çözüm üretin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 5}, "tip": "Koçvari"},
        {"metin": "IT'nin düzeltmesini bekleyin, müşterilere sabır isteyin.", "etki": {"Moral": -10, "Verimlilik": -10, "Güven": -10}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Mağazacılık", "olay": "Yeni sezon vitrin değişimi yetişmiyor; ekip yorgun ve bölge müdürünün habersiz ziyareti yaklaşıyor.",
     "secenekler": [
        {"metin": "Ekstra personel çağırıp geceye kalarak yetiştirin.", "etki": {"Moral": -10, "Verimlilik": 15, "Güven": 0}, "tip": "Otoriter"},
        {"metin": "Öncelik sırası belirleyip en görünür alanları önce tamamlayın.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Ekibe durumu açıklayıp gönüllü fazla mesai isteyin.", "etki": {"Moral": 10, "Verimlilik": 5, "Güven": 5}, "tip": "Koçvari"},
        {"metin": "Mevcut vitrinle idare edip müdüre 'zaman yetmedi' deyin.", "etki": {"Moral": 0, "Verimlilik": -5, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Tedarik Zinciri", "olay": "Kritik bir sevkiyat gümrükte 3 gündür bekliyor; 12 mağaza bu üründe stoksuz kalma riski taşıyor.",
     "secenekler": [
        {"metin": "Gümrük müşavirine ekstra ücret ödeyerek süreci hızlandırın.", "etki": {"Moral": 0, "Verimlilik": 15, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Mağazalara durumu şeffafça bildirip alternatif ürün önerileri sunun.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Ekiple birlikte uzun vadeli bir acil durum planı oluşturun.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Sürecin kendiliğinden çözülmesini bekleyip bildirim yapmayın.", "etki": {"Moral": -5, "Verimlilik": -15, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Satın Alma", "olay": "Ana tedarikçi, sezon başlamasına 2 hafta kala fiyatlarda %18 artış bildirdi.",
     "secenekler": [
        {"metin": "Sert bir müzakereyle eski fiyatta ısrar edin.", "etki": {"Moral": 0, "Verimlilik": 5, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Tedarikçiyle uzun vadeli bir anlaşma önererek orta yol bulun.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Ekiple birlikte alternatif tedarikçi araştırması başlatın.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Artışı kabul edip konuyu üst yönetime yansıtmadan kapatın.", "etki": {"Moral": -5, "Verimlilik": -5, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "İnsan Kaynakları", "olay": "İki eşit performanslı çalışan aynı terfi pozisyonu için bekliyor.",
     "secenekler": [
        {"metin": "Objektif verilere dayanarak hızlıca kendiniz karar verip açıklayın.", "etki": {"Moral": -5, "Verimlilik": 10, "Güven": 0}, "tip": "Otoriter"},
        {"metin": "Her ikisiyle de ayrı görüşüp alternatif fırsatlar sunun.", "etki": {"Moral": 10, "Verimlilik": 0, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Şeffaf bir değerlendirme komitesi kurup kararı birlikte verin.", "etki": {"Moral": 5, "Verimlilik": -5, "Güven": 15}, "tip": "Demokratik"},
        {"metin": "Kararı belirsiz bir tarihe erteleyin.", "etki": {"Moral": -10, "Verimlilik": -5, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Pazarlama", "olay": "İş birliği yapılan bir influencer, kampanya lansmanından bir gün önce tartışmalı bir paylaşım yaptı.",
     "secenekler": [
        {"metin": "İş birliğini derhal sonlandırıp kamuoyuna açıklama yapın.", "etki": {"Moral": 0, "Verimlilik": 5, "Güven": 10}, "tip": "Otoriter"},
        {"metin": "Influencer ile özel görüşüp netleştirmesini isteyin.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 5}, "tip": "Demokratik"},
        {"metin": "Kriz iletişim ekibiyle durumu yönetip öğrenme fırsatına çevirin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Tepki vermeyip konunun unutulmasını bekleyin.", "etki": {"Moral": -5, "Verimlilik": -10, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Finans", "olay": "Üst yönetime sunumdan bir gün önce, aylık raporda ciddi bir hesaplama hatası fark edildi.",
     "secenekler": [
        {"metin": "Geceyi kullanarak raporu yeniden hazırlayıp kimseyi bilgilendirmeyin.", "etki": {"Moral": -5, "Verimlilik": 10, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Hatayı şeffafça ele alıp üst yönetime erkenden bildirin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 15}, "tip": "Demokratik"},
        {"metin": "Kök nedeni bulup kalıcı bir kontrol mekanizması kurun.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Küçük bir hata diye düşünüp sunumu değiştirmeden sunun.", "etki": {"Moral": -5, "Verimlilik": -5, "Güven": -20}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Bilgi Teknolojileri", "olay": "Kritik bir sistem güncellemesi sırasında tüm mağaza kasaları çöktü.",
     "secenekler": [
        {"metin": "Güncellemeyi anında geri alıp eski sisteme dönün.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 5}, "tip": "Otoriter"},
        {"metin": "Ekiple hatayı canlı analiz edip mağazalara bilgi akışı sağlayın.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Mağaza müdürleriyle iletişime geçip alternatif ödeme yöntemleri sunun.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Sorunun kendiliğinden çözülmesini bekleyin.", "etki": {"Moral": -10, "Verimlilik": -15, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "E-Ticaret", "olay": "Büyük indirim gününde web sitesi trafiği beklenenin 5 katına çıktı; siparişler aksıyor.",
     "secenekler": [
        {"metin": "Sunucu kapasitesini acil artırıp ek maliyeti göze alın.", "etki": {"Moral": 0, "Verimlilik": 15, "Güven": 5}, "tip": "Otoriter"},
        {"metin": "Kritik olmayan özellikleri geçici kapatarak performansı önceliklendirin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 5}, "tip": "Koçvari"},
        {"metin": "Müşterilere şeffaf bildirimle durumu açıklayıp ekstra indirim kodu verin.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 15}, "tip": "Demokratik"},
        {"metin": "Sorunun kendi kendine düzelmesini bekleyin.", "etki": {"Moral": -10, "Verimlilik": -15, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Genel", "olay": "Ekibinizdeki iki kıdemli çalışan, yeni bir iş süreci üzerinde fikir ayrılığı yaşıyor.",
     "secenekler": [
        {"metin": "İkisini aynı anda odaya çağırıp çözüm bulana kadar çıkmayın.", "etki": {"Moral": -5, "Verimlilik": 5, "Güven": 10}, "tip": "Otoriter"},
        {"metin": "Fikirlerini ayrı dinleyip size en uygun olanı siz seçin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Tarafsız bir moderatör eşliğinde fikirlerini ekibe sunmalarını isteyin.", "etki": {"Moral": 5, "Verimlilik": -5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Zamanla düzeleceğini düşünüp müdahale etmeyin.", "etki": {"Moral": -10, "Verimlilik": -5, "Güven": -10}, "tip": "Kaçınmacı"}
     ]},
]

def aciklama_yon(v):
    if v > 0: return "arttı"
    elif v < 0: return "azaldı"
    return "değişmedi"

narratif_ipuclari = {
    ("Moral", "arttı"): "ekibin motivasyonu ve enerjisi gözle görülür şekilde yükseldi",
    ("Moral", "azaldı"): "ekipte hafif bir huzursuzluk ve gerginlik sezildi",
    ("Verimlilik", "arttı"): "operasyonel sonuçlar ve iş akışı belirgin şekilde iyileşti",
    ("Verimlilik", "azaldı"): "günlük işlerde küçük aksamalar ve yavaşlamalar ortaya çıktı",
    ("Güven", "arttı"): "çalışanlar sizinle daha açık ve rahat iletişim kurmaya başladı",
    ("Güven", "azaldı"): "bazı çalışanlarda size karşı hafif bir güven sarsıntısı oluştu",
}

def onceki_karar_ozeti_uret(karar):
    if not karar:
        return None
    ipuclari = []
    for k, v in karar['etki'].items():
        if abs(v) >= 5:
            yon = aciklama_yon(v)
            ipucu = narratif_ipuclari.get((k, yon))
            if ipucu:
                ipuclari.append(ipucu)
    if not ipuclari:
        return f"Bir önceki turda '{karar['metin']}' yaklaşımını seçtiniz ve durum genel olarak stabil kaldı."
    return f"Bir önceki turda '{karar['metin']}' yaklaşımını seçtiniz. Bunun sonucunda {', '.join(ipuclari)}."


def karakter_sec_veya_uret(departman):
    """Mevcut karakter havuzundan birini geri getirir ya da yeni bir karakter oluşturur."""
    havuz_pool = st.session_state.karakter_havuzu
    if havuz_pool and random.random() < 0.55:
        return random.choice(havuz_pool), False

    dept_data = DEPARTMANLAR.get(departman, DEPARTMANLAR["Mağazacılık"])
    kullanilan_isimler = [k['isim'] for k in havuz_pool]
    musait_isimler = [i for i in ISIM_HAVUZU if i not in kullanilan_isimler] or ISIM_HAVUZU

    yeni_karakter = {
        "isim": random.choice(musait_isimler),
        "rol": random.choice(dept_data["karakterler"]),
        "kisilik": random.choice(KISILIK_OZELLIKLERI),
        "iliski": 50,
        "gecmis": []
    }
    if len(havuz_pool) < 4:
        havuz_pool.append(yeni_karakter)
    return yeni_karakter, True


def karakter_guncelle(isim, secilen_metin, etki):
    for k in st.session_state.karakter_havuzu:
        if k['isim'] == isim:
            k['iliski'] = max(0, min(100, k['iliski'] + etki.get('Güven', 0)))
            kisa_not = f"'{secilen_metin[:60]}' yaklaşımıyla karşılaştı"
            k['gecmis'].append(kisa_not)
            k['gecmis'] = k['gecmis'][-3:]
            break


def kriz_uret():
    departman = st.session_state.user_department
    dept_data = DEPARTMANLAR.get(departman, DEPARTMANLAR["Mağazacılık"])

    tema = random.choice(dept_data["temalar"])
    baglam = random.choice(dept_data["baglamlar"])
    onceki_ozet = " | ".join(st.session_state.gecmis_konular[-6:]) if st.session_state.gecmis_konular else "yok"

    onceki_karar = st.session_state.karar_gecmisi[-1] if st.session_state.karar_gecmisi else None
    baglanti_ozeti = onceki_karar_ozeti_uret(onceki_karar)

    # --- Karakter seç (yeni ya da tekrarlayan) ---
    karakter, yeni_mi = karakter_sec_veya_uret(departman)
    if yeni_mi:
        karakter_bilgisi = f"""Senaryoda YENİ bir karakter tanıt: {karakter['isim']} ({karakter['rol']}). 
        Kişilik özelliği: {karakter['kisilik']}. Bu karakteri ismiyle anarak hikayeye dahil et."""
    else:
        gecmis_notu = "; ".join(karakter['gecmis']) if karakter['gecmis'] else "henüz belirgin bir geçmişiniz yok"
        iliski_durumu = "gayet iyi ve güvene dayalı" if karakter['iliski'] >= 65 else ("gergin ve mesafeli" if karakter['iliski'] <= 35 else "orta seviyede, ne çok iyi ne çok kötü")
        karakter_bilgisi = f"""Senaryoda DAHA ÖNCE TANIŞTIĞINIZ şu karakteri tekrar kullan: {karakter['isim']} ({karakter['rol']}, kişilik: {karakter['kisilik']}). 
        Bu karakterle aranızdaki ilişki şu an {iliski_durumu} durumda. Geçmişte yaşananlar: {gecmis_notu}. 
        Yeni senaryoyu bu karakterle olan ilişkinizin doğal bir devamı gibi kurgula."""

    baglanti_talimati = ""
    if baglanti_ozeti:
        baglanti_talimati = f"""
        DEVAMLILIK BİLGİSİ: {baglanti_ozeti}
        Yeni senaryonun İLK CÜMLESİNDE, bu önceki kararın doğal bir yansımasını hikayenin doğal bir parçası olarak anlat. 
        ASLA "Moral", "Verimlilik", "Güven" gibi oyun terimlerini doğrudan kullanma; gerçekçi, insani bir anlatım kullan.
        """

    # --- Rastgele seçenek sayısı (2, 3 veya 4) ---
    secenek_sayisi = random.choices([2, 3, 4], weights=[0.25, 0.35, 0.4])[0]
    secilecek_tipler = random.sample(TUM_TIPLER, secenek_sayisi)

    senaryo_turu_talimati = ""
    if secenek_sayisi == 2:
        senaryo_turu_talimati = """Bu sefer KESKİN BİR İKİLEM senaryosu yaz (örn: "yap ya da yapma", "onayla ya da reddet" tarzı net bir karar anı). 
        Sadece 2 seçenek olsun, bunlar birbirine net bir şekilde zıt olsun."""
    elif secenek_sayisi == 3:
        senaryo_turu_talimati = "3 farklı, nüanslı seçenek sun."
    else:
        senaryo_turu_talimati = "4 farklı, nüanslı seçenek sun."

    ornek_secenekler = ",
".join([
        f'{{"metin": "...", "etki": {{"Moral": 0, "Verimlilik": 0, "Güven": 0}}, "tip": "{t}"}}' for t in secilecek_tipler
    ])

    try:
        istek = f"""Sen üst düzey, tecrübeli ve son derece YARATICI bir LCW (LC Waikiki) Liderlik Koçusun. 

        Bu senaryo özellikle "{departman}" departmanı bağlamında olmalı ve bu departmanın gerçek iş süreçlerini yansıtmalı.
        Konu teması: {tema}. 
        Bağlam/ortam: {baglam}. 
        
        {karakter_bilgisi}

        Daha önce şu konular kullanıldı, bunları ve benzer olay örgülerini KESİNLİKLE TEKRARLAMA: {onceki_ozet}.

        {baglanti_talimati}

        Gerçekçi, özgün, klişe olmayan, günlük hayattan sürpriz detaylar içeren bir yönetim senaryosu yaz (2-4 cümle). 
        Somut detaylar kullan: sayılar, yüzdeler, tarihler, ürün/kampanya isimleri gibi.

        {senaryo_turu_talimati}
        Her seçeneğin "tip" etiketi şu listeden birebir kullanılsın (sırayla): {secilecek_tipler}.

        ÖNEMLİ KURALLAR:
        - Hiçbir seçenek 'mükemmel' olmasın, her birinin bir bedeli olsun. Etkiler -15 ile +15 arasında olsun.
        - Seçenek metinleri KISA VE ÖZ olsun, EN FAZLA 130 karakter, tek cümle.
        - Seçenekler birbirine çok bariz zıt olmasın; gerçekçi ve yorumsal olsun.

        SADECE şu JSON formatında döndür, başka hiçbir açıklama ekleme:
        {{"olay": "...", "secenekler": [
{ornek_secenekler}
        ]}}"""

        cevap = model.generate_content(istek)
        res_text = cevap.text.strip()
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0].strip()
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0].strip()

        data = json.loads(res_text)
        random.shuffle(data['secenekler'])
        data['aktif_karakter'] = karakter['isim']

        st.session_state.gecmis_konular.append(f"{tema} - {data['olay'][:70]}")
        st.session_state.last_error = None
        st.session_state.ai_success_count += 1
        return data

    except Exception as e:
        st.session_state.last_error = str(e)

        eslesenler = [h for h in havuz if h.get("departman") == departman]
        if not eslesenler:
            eslesenler = [h for h in havuz if h.get("departman") == "Genel"]

        kullanilmayanlar = [h for h in eslesenler if h['olay'] not in st.session_state.havuz_kullanilan]
        if not kullanilmayanlar:
            st.session_state.havuz_kullanilan = []
            kullanilmayanlar = eslesenler

        secim = random.choice(kullanilmayanlar)
        st.session_state.havuz_kullanilan.append(secim['olay'])

        secim_copy = {"olay": secim["olay"], "secenekler": [dict(s) for s in secim["secenekler"]], "aktif_karakter": None}
        random.shuffle(secim_copy['secenekler'])
        return secim_copy


def hedef_uret():
    metrik = random.choice(["Moral", "Verimlilik", "Güven"])
    deger = random.choice([70, 75, 80])
    return {"metrik": metrik, "deger": deger}


def final_rapor_uret(stats, secim_gecmisi):
    ortalama = sum(stats.values()) / 3
    tip_sayaci = Counter(secim_gecmisi)
    baskin_tip = tip_sayaci.most_common(1)[0][0] if tip_sayaci else "Belirsiz"

    tip_aciklamalari = {
        "Demokratik": "Kararlarınızda ekibinizin fikrini almayı ve katılımcı bir yönetim tarzını önceliklendirdiniz.",
        "Otoriter": "Çoğunlukla hızlı ve net kararlar alarak operasyonel sonuçlara odaklandınız.",
        "Koçvari": "Çalışanlarınızın gelişimine ve uzun vadeli potansiyeline yatırım yapan bir yaklaşım sergilediniz.",
        "Kaçınmacı": "Zor kararlar karşısında çoğunlukla geri çekilmeyi veya sorumluluğu ertelemeyi tercih ettiniz.",
        "Belirsiz": "Henüz yeterli veri toplanmadı."
    }

    metrik_yorumlari = {}
    for metrik, deger in stats.items():
        if deger >= 75: seviye = "Güçlü"
        elif deger >= 50: seviye = "Orta"
        else: seviye = "Zayıf"
        aciklamalar = {
            "Moral": {"Güçlü": "Ekibiniz kendini değerli ve motive hissediyor.", "Orta": "Ekip morali dengeli ama kırılgan.", "Zayıf": "Ekibinizde tükenmişlik belirtileri riski var."},
            "Verimlilik": {"Güçlü": "Operasyonel hedeflere ulaşma konusunda güçlüsünüz.", "Orta": "İşler yürüyor ama optimize edilebilecek gecikmeler var.", "Zayıf": "Operasyonel aksaklıklar riski yüksek."},
            "Güven": {"Güçlü": "Ekibiniz sizi şeffaf ve adil buluyor.", "Orta": "Güven var ama sınırlı.", "Zayıf": "Ekip-lider güveni zedelenmiş durumda."}
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
            <div class="progress-outer"><div class="progress-inner" style="width:{deger}%; background:{renk};"></div></div>
        </div>
    """, unsafe_allow_html=True)


def karar_kartı_ciz(kayit):
    tip = kayit.get('tip', 'Belirsiz')
    renk = tip_renk.get(tip, "#9ca3af")
    metin_kisa = kayit['metin'][:65] + ("..." if len(kayit['metin']) > 65 else "")
    stat_satirlari = ""
    for k, v in kayit['etki'].items():
        if v > 0: cls, ok = "stat-up", f"▲ +{v}"
        elif v < 0: cls, ok = "stat-down", f"▼ {v}"
        else: cls, ok = "stat-same", "→ 0"
        stat_satirlari += f'<div class="history-stat-row"><span>{k}</span><span class="{cls}">{ok}</span></div>'
    karakter_html = f'<div style="font-size:0.75em; color:#047857; margin-bottom:4px;">👤 {kayit["karakter"]}</div>' if kayit.get("karakter") else ""
    st.markdown(f"""
        <div class="history-card" style="border-left-color:{renk};">
            <div class="history-tur">Vaka {kayit['tur']}</div>
            <div class="history-tip" style="background:{renk};">{tip}</div>
            {karakter_html}
            <div class="history-metin">"{metin_kisa}"</div>
            {stat_satirlari}
        </div>
    """, unsafe_allow_html=True)


def secenekleri_ciz(current):
    secenekler = current['secenekler']
    n = len(secenekler)
    i = 0
    while i < n:
        satir = secenekler[i:i+2]
        cols = st.columns(len(satir))
        for j, s in enumerate(satir):
            idx = i + j
            with cols[j]:
                if st.button(s['metin'], key=f"v_{st.session_state.tur}_{idx}"):
                    for k, v in s['etki'].items():
                        st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))

                    st.session_state.secim_gecmisi.append(s.get('tip', 'Belirsiz'))

                    aktif_karakter = current.get('aktif_karakter')
                    if aktif_karakter:
                        karakter_guncelle(aktif_karakter, s['metin'], s['etki'])

                    st.session_state.karar_gecmisi.append({
                        "tur": st.session_state.tur, "metin": s['metin'],
                        "tip": s.get('tip', 'Belirsiz'), "etki": s['etki'], "karakter": aktif_karakter
                    })

                    st.session_state.tur += 1
                    st.session_state.current_scenario = None
                    st.rerun()
        i += 2


# --- SOL MENÜ: TEŞHİS PANELİ ---
with st.sidebar:
    st.header("🔧 Sistem Durumu")
    st.write(f"✅ AI Başarılı Çağrı: {st.session_state.ai_success_count}")
    st.write(f"🤖 Kullanılan Model: `{MODEL_ADI}`")
    if st.session_state.user_department:
        st.write(f"🏢 Departman: {st.session_state.user_department}")
    if st.session_state.last_error:
        st.error("❌ AI Bağlantı Hatası:")
        st.code(st.session_state.last_error)
    else:
        st.success("Şu ana kadar hata yok.")

    if st.session_state.karakter_havuzu:
        st.write("---")
        st.write("**👥 Tanıştığınız Karakterler**")
        for k in st.session_state.karakter_havuzu:
            st.markdown(f"""
                <div class="karakter-kart">
                    <b>{k['isim']}</b> — {k['rol']}<br>
                    <span style="color:#6b7280;">{k['kisilik']}</span><br>
                    İlişki: %{k['iliski']}
                </div>
            """, unsafe_allow_html=True)

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
        - Departmanınızı seçin; senaryolar tamamen **o departmana özel** üretilecek.
        - Kararlarınız birbirine **bağlı bir hikaye** oluşturacak.
        - Oyun boyunca **tekrar karşınıza çıkabilecek karakterlerle** tanışacaksınız.
        - Bazı vakalar 2 seçenekli keskin ikilemler, bazıları 3-4 seçenekli nüanslı kararlar olacak.
        - Size özel bir **hedef** atanacak ve sonunda bu hedefe ulaşıp ulaşmadığınız değerlendirilecek.
        - Sonunda kişisel bir **"Liderlik Karnesi"** hazırlanacak.

        ⚠️ *Unutmayın: Hiçbir seçenek mükemmel değildir.*
        """)

    with col2:
        st.subheader("📝 Katılımcı Bilgileri")
        with st.form("giris_formu"):
            ad_soyad = st.text_input("Ad Soyad *", placeholder="Örn: Deniz Demirkaynak")

            departman_secenekleri = ["-- Seçiniz --"] + [f"{v['icon']} {k}" for k, v in DEPARTMANLAR.items()]
            secilen = st.selectbox("Departman *", departman_secenekleri)

            uzunluk_secenekleri = {"Kısa (5 Vaka)": 5, "Standart (10 Vaka)": 10, "Uzun (15 Vaka)": 15}
            secilen_uzunluk = st.selectbox("Simülasyon Uzunluğu *", list(uzunluk_secenekleri.keys()), index=1)

            gonder = st.form_submit_button("🚀 Simülasyonu Başlat")

            if gonder:
                if ad_soyad.strip() == "":
                    st.warning("Lütfen devam etmek için adınızı ve soyadınızı girin.")
                elif secilen == "-- Seçiniz --":
                    st.warning("Lütfen devam etmek için bir departman seçin.")
                else:
                    temiz_departman = secilen.split(" ", 1)[1]
                    st.session_state.user_name = ad_soyad.strip()
                    st.session_state.user_department = temiz_departman
                    st.session_state.oyun_uzunlugu = uzunluk_secenekleri[secilen_uzunluk]
                    st.session_state.hedef = hedef_uret()
                    st.session_state.started = True
                    st.rerun()

    st.stop()


# ==========================================================
# ==================  2. AŞAMA: OYUN EKRANI  ===============
# ==========================================================

dept_icon = DEPARTMANLAR.get(st.session_state.user_department, {}).get("icon", "🏢")
ust_bilgi = f"👤 {st.session_state.user_name}  •  {dept_icon} {st.session_state.user_department}"

st.markdown(f"""
    <div class="hero-banner">
        <h1>💙 LC Waikiki Liderlik Simülasyonu</h1>
        <p>{ust_bilgi}</p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.hedef:
    h = st.session_state.hedef
    st.markdown(f'<div class="hedef-banner">🎯 Hedefiniz: Simülasyon sonunda <b>{h["metrik"]}</b> skorunuzu en az <b>%{h["deger"]}</b>\'e çıkarmak.</div>', unsafe_allow_html=True)

col_main, col_side = st.columns([2.6, 1])

with col_main:
    c1, c2, c3 = st.columns(3)
    with c1: stat_karti_ciz("Moral", st.session_state.stats['Moral'], "😊")
    with c2: stat_karti_ciz("Verimlilik", st.session_state.stats['Verimlilik'], "📈")
    with c3: stat_karti_ciz("Güven", st.session_state.stats['Güven'], "🤝")

    st.write("")

    if st.session_state.tur <= st.session_state.oyun_uzunlugu:
        if st.session_state.current_scenario is None:
            with st.spinner("Yeni liderlik vakası hazırlanıyor..."):
                st.session_state.current_scenario = kriz_uret()

        current = st.session_state.current_scenario

        badge_html = f'<div class="vaka-badge">VAKA {st.session_state.tur} / {st.session_state.oyun_uzunlugu}</div> <div class="dept-badge">{dept_icon} {st.session_state.user_department}</div>'
        if current.get('aktif_karakter'):
            badge_html += f' <div class="karakter-badge">👤 {current["aktif_karakter"]}</div>'
        st.markdown(badge_html, unsafe_allow_html=True)
        st.markdown(f'<div class="olay-box">{current["olay"]}</div>', unsafe_allow_html=True)

        st.markdown("##### Liderlik Yaklaşımınız:")
        secenekleri_ciz(current)

    else:
        st.balloons()
        st.success(f"🏁 Tebrikler {st.session_state.user_name}, {st.session_state.oyun_uzunlugu} Vakalık Liderlik Maratonunu Tamamladınız!")

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

        if st.session_state.hedef:
            h = st.session_state.hedef
            gerceklesen = st.session_state.stats[h['metrik']]
            basarili = gerceklesen >= h['deger']
            renk = "#16a34a" if basarili else "#dc2626"
            durum = "✅ Hedefinize ULAŞTINIZ!" if basarili else "❌ Hedefinize ulaşamadınız."
            st.markdown(f"""
                <div class="rapor-kart" style="border-left: 5px solid {renk};">
                    <b>🎯 Hedef Değerlendirmesi:</b><br>
                    Hedef: {h['metrik']} skorunuzu %{h['deger']}'e çıkarmak.<br>
                    Gerçekleşen: %{gerceklesen}<br>
                    <span style="color:{renk}; font-weight:700;">{durum}</span>
                </div>
            """, unsafe_allow_html=True)

        st.write("### 📊 Metrik Bazlı Detaylı Analiz")
        for metrik, yorum in metrik_yorumlari.items():
            st.markdown(f'<div class="rapor-kart">{yorum}</div>', unsafe_allow_html=True)

        st.write("### 🧭 Baskın Liderlik Tarzınız")
        st.markdown(f"""
            <div class="rapor-kart">
                <b>{baskin_tip}</b> ({tip_sayaci.get(baskin_tip, 0)}/{st.session_state.oyun_uzunlugu} kararınızda bu yaklaşımı sergilediniz)<br><br>
                {tip_metni}
            </div>
        """, unsafe_allow_html=True)

        st.write("### 📈 Tüm Kararlarınızın Dağılımı")
        for tip, sayi in tip_sayaci.items():
            st.write(f"**{tip}** — {sayi} kez")
            st.progress(sayi / st.session_state.oyun_uzunlugu)

        if st.button("Simülasyonu Baştan Başlat"):
            st.session_state.clear()
            st.rerun()

with col_side:
    st.markdown('<div class="journey-header">📜 Karar Yolculuğunuz</div>', unsafe_allow_html=True)
    if not st.session_state.karar_gecmisi:
        st.markdown('<div class="empty-journey">Henüz bir karar vermediniz.<br>İlk kararınızı verdiğinizde burada görünecek.</div>', unsafe_allow_html=True)
    else:
        for kayit in st.session_state.karar_gecmisi:
            karar_kartı_ciz(kayit)
