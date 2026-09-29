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
    .dept-badge {
        display: inline-block; background: #fef3c7; color: #92400e; 
        padding: 6px 18px; border-radius: 30px; font-weight: 600; font-size: 0.85em; margin-bottom: 15px; margin-left: 8px;
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

# 🔧 Daha yaratıcı ama daha yavaş sonuçlar isterseniz 'gemini-1.5-pro' deneyebilirsiniz.
MODEL_ADI = 'gemini-1.5-flash'
generation_config = {"temperature": 1.6, "top_p": 0.97, "top_k": 60}
model = genai.GenerativeModel(MODEL_ADI, generation_config=generation_config)

# --- DEPARTMAN TANIMLARI ---
DEPARTMANLAR = {
    "Mağazacılık": {
        "icon": "🏬",
        "temalar": ["Mağaza Operasyonu", "Müşteri Şikayeti Yönetimi", "Vardiya Planlama", "Kampanya Yönetimi",
                    "Vitrin ve Görsel Merchandising", "Stok Sayımı", "Kasa Farkı Yönetimi", "Hırsızlık ve Kayıp Yönetimi"],
        "karakterler": ["yeni işe başlayan bir kasiyer", "10 yıllık kıdemli bir reyon sorumlusu", "stajyer bir çalışan",
                         "vardiya amiri", "depo sorumlusu", "mağaza müdür yardımcısı", "görsel merchandising uzmanı"],
        "baglamlar": ["yoğun bir hafta sonu indirim kampanyası sırasında", "yıl sonu stok sayımı gecesinde",
                      "AVM'deki büyük indirim haftasında", "okula dönüş sezonunun zirvesinde",
                      "ani bir bölge müdürü ziyareti sırasında", "yeni sezon vitrin değişiminin son gününde"]
    },
    "Tedarik Zinciri": {
        "icon": "🚚",
        "temalar": ["Depo Yönetimi", "Sevkiyat Gecikmeleri", "Lojistik Kriz Yönetimi", "Envanter Optimizasyonu",
                    "Tedarikçi ile Anlaşmazlık", "Mevsimsel Talep Dalgalanması", "Depo İş Güvenliği"],
        "karakterler": ["depo operasyon şefi", "sevkiyat planlama uzmanı", "yeni transfer olmuş lojistik koordinatörü",
                         "forklift operatörü ekip lideri", "envanter analisti", "gümrük süreçleri sorumlusu"],
        "baglamlar": ["kritik bir sevkiyatın gümrükte 3 gündür beklediği bir durumda", "depo kapasitesinin sınırına dayandığı bir dönemde",
                      "yılın en yoğun sevkiyat haftasında", "yeni bir depo yönetim sistemine geçiş sürecinde",
                      "bir tedarikçinin son anda teslimat tarihini değiştirdiği bir durumda"]
    },
    "Satın Alma": {
        "icon": "🛒",
        "temalar": ["Tedarikçi Müzakeresi", "Maliyet Optimizasyonu", "Kalite Kontrol Anlaşmazlığı",
                    "Yeni Tedarikçi Seçimi", "Bütçe Aşımı", "Numune Onay Süreci", "Sürdürülebilirlik Kriterleri"],
        "karakterler": ["kıdemli satın alma uzmanı", "yeni mezun satın alma asistanı", "kategori yöneticisi",
                         "kalite kontrol sorumlusu", "yurt dışı tedarikçi temsilcisi"],
        "baglamlar": ["sezon başlamasına 2 hafta kala", "ana tedarikçinin ani fiyat artışı bildirdiği bir günde",
                      "numune onaylandıktan sonra üretimde kalite sorunu çıktığında", "yıllık tedarikçi değerlendirme toplantısı öncesinde",
                      "döviz kurunun ani yükseldiği bir dönemde"]
    },
    "İnsan Kaynakları": {
        "icon": "👥",
        "temalar": ["İşe Alım Kararları", "Terfi ve Adalet", "Performans Değerlendirme", "Çalışan Bağlılığı",
                    "Etik İkilemler", "İşten Çıkarma Süreci", "Eğitim ve Gelişim", "Mobbing İddiası"],
        "karakterler": ["yeni İK uzmanı", "kıdemli İK iş ortağı", "işe alım uzmanı", "eğitim ve gelişim sorumlusu",
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
                         "yeni mezun pazarlama asistanı", "influencer ilişkileri sorumlusu"],
        "baglamlar": ["büyük bir kampanya lansmanına 24 saat kala", "işbirliği yapılan bir influencer'ın tartışmalı paylaşımından sonra",
                      "sosyal medyada markayla ilgili olumsuz bir trend başladığında", "reklam bütçesinin yarısı harcandıktan sonra beklenen sonuç gelmediğinde",
                      "rakip firmanın beklenmedik bir kampanya yaptığı günde"]
    },
    "Finans": {
        "icon": "💰",
        "temalar": ["Bütçe Kısıtlaması", "Maliyet Raporlama Hatası", "Yatırım Kararı", "Nakit Akışı Krizi",
                    "Denetim Süreci", "Departmanlar Arası Bütçe Çatışması"],
        "karakterler": ["finansal analist", "kıdemli muhasebe uzmanı", "bütçe planlama sorumlusu",
                         "iç denetim uzmanı", "yeni mezun finans asistanı"],
        "baglamlar": ["üst yönetime sunumdan bir gün önce ciddi bir rapor hatası fark edildiğinde",
                      "yıl sonu bütçe kapanışına günler kala", "bir departmanın bütçesini aştığı ve ek onay istediği durumda",
                      "beklenmedik bir denetimin duyurulduğu günde", "nakit akışında geçici bir sıkışma yaşandığında"]
    },
    "Bilgi Teknolojileri": {
        "icon": "💻",
        "temalar": ["Sistem Arızası Krizi", "Yeni Yazılım Geçişi", "Siber Güvenlik Riski", "Proje Gecikmesi",
                    "Ekip İçi Teknik Anlaşmazlık", "Otomasyon Projesi"],
        "karakterler": ["yazılım geliştirici", "sistem yöneticisi", "proje yöneticisi",
                         "yeni mezun IT stajyeri", "siber güvenlik uzmanı"],
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
                         "yeni mezun e-ticaret asistanı", "kargo süreçleri koordinatörü"],
        "baglamlar": ["büyük indirim gününde (11.11 tarzı) site trafiği beklenenin 5 katına çıktığında",
                      "stok-web senkronizasyon hatası yüzünden tükenen ürünler satılmaya devam ettiğinde",
                      "kargo firmasının ardı ardına gecikme yaptığı bir haftada", "sosyal medyada bir müşteri şikayeti viral olduğunda",
                      "yeni web sitesi tasarımına geçişin ilk gününde"]
    }
}

# --- SİSTEM HAFIZASI ---
defaults = {
    'started': False, 'user_name': "", 'user_department': "",
    'stats': {'Moral': 60, 'Verimlilik': 60, 'Güven': 60},
    'tur': 1, 'current_scenario': None, 'last_error': None, 'ai_success_count': 0,
    'gecmis_konular': [], 'secim_gecmisi': [], 'karar_gecmisi': [], 'havuz_kullanilan': []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

tip_renk = {"Demokratik": "#2563eb", "Otoriter": "#dc2626", "Koçvari": "#16a34a", "Kaçınmacı": "#6b7280", "Belirsiz": "#9ca3af"}

# --- GENİŞLETİLMİŞ YEDEK SENARYO HAVUZU (22 senaryo, departmanlara etiketli) ---
havuz = [
    # --- MAĞAZACILIK ---
    {"departman": "Mağazacılık", "olay": "Kampanya haftasında bir üründe etiket hatası çıktı; kasada indirim yansımıyor ve müşteri kuyruğu büyüyor.",
     "secenekler": [
        {"metin": "Kasiyerlere manuel indirim yetkisi verip kuyruğu hemen eritin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 5}, "tip": "Otoriter"},
        {"metin": "Sistemi düzeltene kadar özür dileyip müşterilere kupon verin.", "etki": {"Moral": 5, "Verimlilik": -5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Ekiple birlikte hatayı analiz edip anlık çözüm üretin, süreci öğretici hale getirin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 5}, "tip": "Koçvari"},
        {"metin": "IT'nin düzeltmesini bekleyin, müşterilere sabır isteyin.", "etki": {"Moral": -10, "Verimlilik": -10, "Güven": -10}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Mağazacılık", "olay": "Yeni sezon vitrin değişimi yetişmiyor; ekip yorgun ve bölge müdürünün habersiz ziyareti yaklaşıyor.",
     "secenekler": [
        {"metin": "Ekstra personel çağırıp geceye kalarak yetiştirin.", "etki": {"Moral": -10, "Verimlilik": 15, "Güven": 0}, "tip": "Otoriter"},
        {"metin": "Öncelik sırası belirleyip en görünür alanları önce tamamlayın, gerisini ekiple birlikte planlayın.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Ekibe durumu açıklayıp gönüllü fazla mesai isteyin, karşılığında esnek izin sözü verin.", "etki": {"Moral": 10, "Verimlilik": 5, "Güven": 5}, "tip": "Koçvari"},
        {"metin": "Mevcut vitrinle idare edip müdüre 'zaman yetmedi' deyin.", "etki": {"Moral": 0, "Verimlilik": -5, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Mağazacılık", "olay": "Kasa sayımında sürekli küçük farklar çıkıyor; ekip içinde kimin sorumlu olduğu belirsiz, güvensizlik başlıyor.",
     "secenekler": [
        {"metin": "Tüm ekibe kamera kayıtlarının izleneceğini duyurup net kurallar koyun.", "etki": {"Moral": -10, "Verimlilik": 5, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Kasa sürecini ekiple birlikte gözden geçirip yeni bir kontrol sistemi tasarlayın.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Herkesle teker teker konuşup güven ortamı oluşturarak gönüllü itiraf bekleyin.", "etki": {"Moral": 5, "Verimlilik": -5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Küçük farklar diye görmezden gelip sürecin kendiliğinden düzelmesini bekleyin.", "etki": {"Moral": -5, "Verimlilik": -10, "Güven": -10}, "tip": "Kaçınmacı"}
     ]},

    # --- TEDARİK ZİNCİRİ ---
    {"departman": "Tedarik Zinciri", "olay": "Kritik bir sevkiyat gümrükte 3 gündür bekliyor; 12 mağaza bu üründe stoksuz kalma riski taşıyor.",
     "secenekler": [
        {"metin": "Gümrük müşavirine ekstra ücret ödeyerek süreci hızlandırın.", "etki": {"Moral": 0, "Verimlilik": 15, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Mağazalara durumu şeffafça bildirip alternatif ürün önerileri sunun.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Ekiple birlikte benzer krizler için uzun vadeli bir acil durum planı oluşturun.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Sürecin kendiliğinden çözülmesini bekleyip mağazaları bilgilendirmeyin.", "etki": {"Moral": -5, "Verimlilik": -15, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Tedarik Zinciri", "olay": "Depo sayımında ciddi bir fark çıktı; forklift ekibi ile envanter ekibi birbirini suçluyor.",
     "secenekler": [
        {"metin": "İki ekibi ayrı ayrı sorgulayıp sorumluyu bulana kadar sıkı takip uygulayın.", "etki": {"Moral": -10, "Verimlilik": 10, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Ortak bir toplantı düzenleyip süreci birlikte haritalandırarak kök nedeni bulun.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Her iki ekibin de görüşünü ayrı dinleyip tarafsız bir karar verin.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 5}, "tip": "Demokratik"},
        {"metin": "Konuyu üst yönetime iletip kendiniz karışmayın.", "etki": {"Moral": -5, "Verimlilik": -10, "Güven": -10}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Tedarik Zinciri", "olay": "Yeni depo yönetim sistemine geçiş sürecinde eski çalışanlar sistemi kullanmakta zorlanıyor, hatalar artıyor.",
     "secenekler": [
        {"metin": "Sistemi kullanmayanlara performans uyarısı verin.", "etki": {"Moral": -10, "Verimlilik": 10, "Güven": -10}, "tip": "Otoriter"},
        {"metin": "Kıdemli çalışanlarla birebir eğitim seansları planlayıp sabırla destek olun.", "etki": {"Moral": 10, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Ekipten geri bildirim toplayıp sistemin zor kısımlarını tedarikçiyle birlikte iyileştirin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Geçiş sürecini yavaşça kendiliğinden oturmasına bırakın.", "etki": {"Moral": 0, "Verimlilik": -15, "Güven": -5}, "tip": "Kaçınmacı"}
     ]},

    # --- SATIN ALMA ---
    {"departman": "Satın Alma", "olay": "Ana tedarikçi, sezon başlamasına 2 hafta kala fiyatlarda %18 artış bildirdi ve ürünler zaten sipariş edilmiş durumda.",
     "secenekler": [
        {"metin": "Sert bir müzakereyle eski fiyatta ısrar edin, gerekirse anlaşmayı riske atın.", "etki": {"Moral": 0, "Verimlilik": 5, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Tedarikçiyle uzun vadeli bir anlaşma önererek orta yol bulun.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Ekiple birlikte alternatif tedarikçi araştırması başlatıp riski dağıtın.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Artışı kabul edip konuyu üst yönetime yansıtmadan kapatın.", "etki": {"Moral": -5, "Verimlilik": -5, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Satın Alma", "olay": "Onaylanan numunenin aksine, seri üretimde kumaş kalitesinde belirgin düşüş fark edildi; teslim tarihine 10 gün var.",
     "secenekler": [
        {"metin": "Üretimi tamamen durdurup tedarikçiden yeniden numune isteyin.", "etki": {"Moral": 0, "Verimlilik": -10, "Güven": 10}, "tip": "Otoriter"},
        {"metin": "Kalite ekibiyle birlikte kabul edilebilir bir tolerans aralığı belirleyip devam edin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 5}, "tip": "Koçvari"},
        {"metin": "Tedarikçiyle şeffaf konuşup sorunun kök nedenini birlikte çözün.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Teslim tarihini kaçırmamak için düşük kaliteyi görmezden gelin.", "etki": {"Moral": -5, "Verimlilik": 5, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Satın Alma", "olay": "Yeni bir tedarikçi çok uygun fiyat sunuyor ama sürdürülebilirlik sertifikaları eksik; sezon başına yetişmesi gereken kritik bir ürün var.",
     "secenekler": [
        {"metin": "Fiyat avantajı için riski göze alıp anlaşmayı hemen imzalayın.", "etki": {"Moral": 0, "Verimlilik": 15, "Güven": -10}, "tip": "Otoriter"},
        {"metin": "Tedarikçiye kısa süreli şartlı bir anlaşma sunup sertifikasyon sürecini takip edin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Ekiple birlikte artı ve eksileri tartışıp ortak bir karara varın.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Kararı geciktirip başka birinin karar vermesini bekleyin.", "etki": {"Moral": -5, "Verimlilik": -10, "Güven": -10}, "tip": "Kaçınmacı"}
     ]},

    # --- İNSAN KAYNAKLARI ---
    {"departman": "İnsan Kaynakları", "olay": "İki eşit performanslı çalışan aynı terfi pozisyonu için bekliyor; ikisi de haklı gerekçelere sahip.",
     "secenekler": [
        {"metin": "Objektif verilere dayanarak hızlıca kendiniz karar verip açıklayın.", "etki": {"Moral": -5, "Verimlilik": 10, "Güven": 0}, "tip": "Otoriter"},
        {"metin": "Her ikisiyle de ayrı ayrı görüşüp kariyer beklentilerine göre alternatif fırsatlar sunun.", "etki": {"Moral": 10, "Verimlilik": 0, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Şeffaf bir değerlendirme komitesi kurup kararı birlikte verin.", "etki": {"Moral": 5, "Verimlilik": -5, "Güven": 15}, "tip": "Demokratik"},
        {"metin": "Kararı belirsiz bir tarihe erteleyin.", "etki": {"Moral": -10, "Verimlilik": -5, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "İnsan Kaynakları", "olay": "Anonim bir şikayet mektubu geldi; bir departman yöneticisinin çalışanlarına karşı mobbing yaptığı iddia ediliyor.",
     "secenekler": [
        {"metin": "Yöneticiyi hemen görevden uzaklaştırıp soruşturma başlatın.", "etki": {"Moral": 5, "Verimlilik": -10, "Güven": 5}, "tip": "Otoriter"},
        {"metin": "Gizlilik içinde, tarafsız bir soruşturma ekibi kurup tüm tarafları dinleyin.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 15}, "tip": "Demokratik"},
        {"metin": "Yöneticiyle koçluk odaklı bir gelişim planı üzerinde çalışın, süreci yakından izleyin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 5}, "tip": "Koçvari"},
        {"metin": "Kanıt yetersiz diyerek konuyu kapatın.", "etki": {"Moral": -15, "Verimlilik": -5, "Güven": -20}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "İnsan Kaynakları", "olay": "Toplu işe alım sürecinde, işe alınan adayların üçte biri ilk ayda işi bırakıyor; sebep net değil.",
     "secenekler": [
        {"metin": "İşe alım kriterlerini sertleştirip mülakat sürecini zorlaştırın.", "etki": {"Moral": 0, "Verimlilik": 5, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Ayrılan çalışanlarla çıkış görüşmesi yapıp kök nedeni analiz edin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Yeni başlayanlar için bir oryantasyon/mentorluk programı tasarlayın.", "etki": {"Moral": 10, "Verimlilik": 5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Normal bir devir hızı olduğunu düşünüp müdahale etmeyin.", "etki": {"Moral": -5, "Verimlilik": -10, "Güven": -10}, "tip": "Kaçınmacı"}
     ]},

    # --- PAZARLAMA ---
    {"departman": "Pazarlama", "olay": "İş birliği yapılan bir influencer, kampanya lansmanından bir gün önce tartışmalı bir paylaşım yaptı; marka adı da etiketli.",
     "secenekler": [
        {"metin": "İş birliğini derhal sonlandırıp kamuoyuna açıklama yapın.", "etki": {"Moral": 0, "Verimlilik": 5, "Güven": 10}, "tip": "Otoriter"},
        {"metin": "Influencer ile özel görüşüp durumu netleştirmesini isteyin, karar sonrasında verin.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 5}, "tip": "Demokratik"},
        {"metin": "Kriz iletişim ekibiyle birlikte durumu yönetip süreci öğrenme fırsatına çevirin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Tepki vermeyip konunun kendiliğinden unutulmasını bekleyin.", "etki": {"Moral": -5, "Verimlilik": -10, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Pazarlama", "olay": "Büyük bir kampanyanın ana görseli, lansmana 24 saat kala tasarım ekibinden hâlâ teslim edilmedi.",
     "secenekler": [
        {"metin": "Tasarım ekibine sert bir uyarı yapıp gece boyunca çalışmalarını isteyin.", "etki": {"Moral": -15, "Verimlilik": 15, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Ekiple birlikte oturup önceliklendirme yapın, gerekirse basitleştirilmiş bir versiyonla ilerleyin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Sorunun kaynağını sakin bir şekilde sorup ekibe destek sunun.", "etki": {"Moral": 10, "Verimlilik": 5, "Güven": 5}, "tip": "Demokratik"},
        {"metin": "Lansmanı ertelemeden mevcut eksik materyalle devam edin.", "etki": {"Moral": -5, "Verimlilik": -5, "Güven": -10}, "tip": "Kaçınmacı"}
     ]},

    # --- FİNANS ---
    {"departman": "Finans", "olay": "Üst yönetime sunumdan bir gün önce, aylık raporda ciddi bir hesaplama hatası fark edildi.",
     "secenekler": [
        {"metin": "Geceyi kullanarak raporu tamamen yeniden hazırlayıp kimseyi bilgilendirmeyin.", "etki": {"Moral": -5, "Verimlilik": 10, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Hatayı ekiple birlikte şeffafça ele alıp üst yönetime durumu erkenden bildirin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 15}, "tip": "Demokratik"},
        {"metin": "Hatanın kök nedenini bulup ekiple birlikte kalıcı bir kontrol mekanizması kurun.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Küçük bir hata olduğunu düşünüp sunumu değiştirmeden sunun.", "etki": {"Moral": -5, "Verimlilik": -5, "Güven": -20}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Finans", "olay": "Pazarlama departmanı, planlanan bütçenin %40 fazlasını harcamış ve ek onay istiyor; genel bütçe zaten kısıtlı.",
     "secenekler": [
        {"metin": "Talebi doğrudan reddedip bütçe disiplinini vurgulayın.", "etki": {"Moral": -5, "Verimlilik": 5, "Güven": -10}, "tip": "Otoriter"},
        {"metin": "Pazarlama ekibiyle oturup harcamanın getirisini analiz ederek ortak bir çözüm bulun.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 15}, "tip": "Demokratik"},
        {"metin": "Diğer departmanlardan tasarruf bularak esnek bir çözüm sunun.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Kararı üst yönetime havale edip taraf olmayın.", "etki": {"Moral": -5, "Verimlilik": -10, "Güven": -10}, "tip": "Kaçınmacı"}
     ]},

    # --- BİLGİ TEKNOLOJİLERİ ---
    {"departman": "Bilgi Teknolojileri", "olay": "Kritik bir sistem güncellemesi sırasında tüm mağaza kasaları çöktü; müşteriler mağazalarda bekliyor.",
     "secenekler": [
        {"metin": "Güncellemeyi anında geri alıp eski sisteme dönün.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 5}, "tip": "Otoriter"},
        {"metin": "Ekiple birlikte hatayı canlı olarak analiz edip mağazalara sürekli bilgi akışı sağlayın.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Mağaza müdürleriyle direkt iletişime geçip alternatif ödeme yöntemleri sunun.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Sorunun kendiliğinden çözülmesini bekleyip mağazaları bilgilendirmeyin.", "etki": {"Moral": -10, "Verimlilik": -15, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Bilgi Teknolojileri", "olay": "Yeni bir otomasyon projesine, işini kaybetmekten korkan kıdemli bir çalışandan sessiz bir direniş geliyor.",
     "secenekler": [
        {"metin": "Projenin zorunlu olduğunu belirtip katılımı şart koşun.", "etki": {"Moral": -10, "Verimlilik": 10, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Çalışanla birebir görüşüp otomasyonun onun rolünü nasıl geliştireceğini birlikte planlayın.", "etki": {"Moral": 10, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Ekibi sürece dahil edip fikirlerini alarak projeyi birlikte şekillendirin.", "etki": {"Moral": 5, "Verimlilik": 5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Direnci görmezden gelip projeyi sessizce ilerletin.", "etki": {"Moral": -5, "Verimlilik": -5, "Güven": -10}, "tip": "Kaçınmacı"}
     ]},

    # --- E-TİCARET ---
    {"departman": "E-Ticaret", "olay": "Büyük indirim gününde web sitesi trafiği beklenenin 5 katına çıktı; site zaman zaman yavaşlıyor, siparişler aksıyor.",
     "secenekler": [
        {"metin": "Sunucu kapasitesini acil olarak artırıp ek maliyeti göze alın.", "etki": {"Moral": 0, "Verimlilik": 15, "Güven": 5}, "tip": "Otoriter"},
        {"metin": "Ekiple birlikte kritik olmayan özellikleri geçici kapatarak performansı önceliklendirin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 5}, "tip": "Koçvari"},
        {"metin": "Müşterilere şeffaf bir bildirimle durumu açıklayıp bekleyenlere ekstra indirim kodu verin.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 15}, "tip": "Demokratik"},
        {"metin": "Sorunun kendi kendine düzelmesini bekleyin.", "etki": {"Moral": -10, "Verimlilik": -15, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "E-Ticaret", "olay": "Stok-web senkronizasyon hatası yüzünden tükenmiş bir ürün satılmaya devam ediyor; iade talepleri hızla artıyor.",
     "secenekler": [
        {"metin": "Ürünü siteden anında kaldırıp mevcut siparişleri iptal edin.", "etki": {"Moral": 0, "Verimlilik": 10, "Güven": 0}, "tip": "Otoriter"},
        {"metin": "Müşterilere alternatif ürün veya bekleme süresi seçeneği sunarak iletişimde kalın.", "etki": {"Moral": 5, "Verimlilik": 0, "Güven": 15}, "tip": "Demokratik"},
        {"metin": "IT ekibiyle birlikte senkronizasyon sürecini kökten iyileştirin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": 5}, "tip": "Koçvari"},
        {"metin": "Talepleri sırayla işleyip acil bir aksiyon almayın.", "etki": {"Moral": -10, "Verimlilik": -10, "Güven": -15}, "tip": "Kaçınmacı"}
     ]},

    # --- GENEL (her departmanda kullanılabilir yedek) ---
    {"departman": "Genel", "olay": "Ekibinizdeki iki kıdemli çalışan, yeni bir iş süreci üzerinde fikir ayrılığı yaşıyor ve bu durum ekip huzurunu bozuyor.",
     "secenekler": [
        {"metin": "İkisini aynı anda odaya çağırıp ortak bir çözüm bulana kadar çıkmayacağınızı söyleyin.", "etki": {"Moral": -5, "Verimlilik": 5, "Güven": 10}, "tip": "Otoriter"},
        {"metin": "Fikirlerini ayrı ayrı dinleyip size en uygun olanı siz seçin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Tarafsız bir moderatör eşliğinde fikirlerini tüm ekibe sunmalarını isteyin.", "etki": {"Moral": 5, "Verimlilik": -5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Zamanla düzeleceğini düşünüp müdahale etmeyin.", "etki": {"Moral": -10, "Verimlilik": -5, "Güven": -10}, "tip": "Kaçınmacı"}
     ]},
    {"departman": "Genel", "olay": "Yüksek potansiyelli bir çalışanınızın başka bir firmadan iş teklifi aldığını öğrendiniz.",
     "secenekler": [
        {"metin": "Kariyer planını öne çekin ve yetki alanını genişletin.", "etki": {"Moral": 10, "Verimlilik": 5, "Güven": 10}, "tip": "Koçvari"},
        {"metin": "Hemen maaş zammı teklif edip bağlılık isteyin.", "etki": {"Moral": 5, "Verimlilik": 10, "Güven": -5}, "tip": "Otoriter"},
        {"metin": "Onunla açık bir sohbet edip gerçek beklentilerini anlamaya çalışın.", "etki": {"Moral": 10, "Verimlilik": -5, "Güven": 10}, "tip": "Demokratik"},
        {"metin": "Gitmek istiyorsa engel olmayın, yenisini bulursunuz deyin.", "etki": {"Moral": -10, "Verimlilik": -10, "Güven": -15}, "tip": "Kaçınmacı"}
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


def kriz_uret():
    departman = st.session_state.user_department
    dept_data = DEPARTMANLAR.get(departman, DEPARTMANLAR["Mağazacılık"])

    tema = random.choice(dept_data["temalar"])
    karakter = random.choice(dept_data["karakterler"])
    baglam = random.choice(dept_data["baglamlar"])

    onceki_ozet = " | ".join(st.session_state.gecmis_konular[-6:]) if st.session_state.gecmis_konular else "yok"

    onceki_karar = st.session_state.karar_gecmisi[-1] if st.session_state.karar_gecmisi else None
    baglanti_ozeti = onceki_karar_ozeti_uret(onceki_karar)

    baglanti_talimati = ""
    if baglanti_ozeti:
        baglanti_talimati = f"""
        DEVAMLILIK BİLGİSİ: {baglanti_ozeti}
        Yeni senaryonun İLK CÜMLESİNDE, bu önceki kararın doğal bir yansımasını (ekip tepkisi, gelişen bir durum, bir sonuç) 
        hikayenin doğal bir parçası olarak anlat. ASLA "Moral", "Verimlilik", "Güven" gibi oyun terimlerini doğrudan kullanma; 
        gerçekçi, insani bir anlatım kullan. Sonrasında yeni krizi/durumu sun.
        """

    try:
        istek = f"""Sen üst düzey, tecrübeli ve son derece YARATICI bir LCW (LC Waikiki) Liderlik Koçusun. 

        Bu senaryo özellikle "{departman}" departmanı bağlamında olmalı ve bu departmanın gerçek iş süreçlerini yansıtmalı.
        Konu teması: {tema}. 
        Bağlam/ortam: {baglam}. 
        Senaryoda mutlaka şu karakter yer alsın: {karakter}. 

        Daha önce şu konular kullanıldı, bunları ve benzer olay örgülerini KESİNLİKLE TEKRARLAMA: {onceki_ozet}.
        Her senaryo tamamen farklı bir çatışma türü, farklı bir yapı ve farklı bir sürpriz unsur içermeli.

        {baglanti_talimati}

        Gerçekçi, özgün, klişe olmayan, sürpriz detaylar içeren bir yönetim senaryosu yaz (2-4 cümle). 
        Somut detaylar kullan: sayılar, yüzdeler, tarihler, ürün/kampanya isimleri gibi. Sıradan "ofis çatışması" anlatma; 
        departmana özgü gerçek bir iş krizi/ikilemi anlat.

        4 farklı liderlik tarzını temsil eden seçenekler sun ve her birine bir "tip" etiketi ver:
        1. "Demokratik" (Güven artırır, Verimlilik bazen yavaşlar)
        2. "Otoriter" (Verimlilik artırır, Moral bazen düşer)
        3. "Koçvari" (Gelişim odaklı, dengeli etki)
        4. "Kaçınmacı" (Risk almaz, genelde skorları düşürür)

        ÖNEMLİ: Hiçbir seçenek 'mükemmel' olmasın, her birinin bir bedeli olsun. Etkiler -15 ile +15 arasında olsun.
        Seçeneklerin metinleri birbirine çok bariz zıt olmasın; gerçekçi ve yorumsal olsun (kararı okumadan hangisinin "doğru" olduğu tahmin edilemesin).

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

        st.session_state.gecmis_konular.append(f"{tema} - {data['olay'][:70]}")
        st.session_state.last_error = None
        st.session_state.ai_success_count += 1
        return data

    except Exception as e:
        st.session_state.last_error = str(e)

        departman = st.session_state.user_department
        eslesenler = [h for h in havuz if h.get("departman") == departman]
        if not eslesenler:
            eslesenler = [h for h in havuz if h.get("departman") == "Genel"]

        kullanilmayanlar = [h for h in eslesenler if h['olay'] not in st.session_state.havuz_kullanilan]
        if not kullanilmayanlar:
            st.session_state.havuz_kullanilan = []
            kullanilmayanlar = eslesenler

        secim = random.choice(kullanilmayanlar)
        st.session_state.havuz_kullanilan.append(secim['olay'])

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
        if deger >= 75: seviye = "Güçlü"
        elif deger >= 50: seviye = "Orta"
        else: seviye = "Zayıf"

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
        if v > 0: cls, ok = "stat-up", f"▲ +{v}"
        elif v < 0: cls, ok = "stat-down", f"▼ {v}"
        else: cls, ok = "stat-same", "→ 0"
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
    if st.session_state.user_department:
        st.write(f"🏢 Departman: {st.session_state.user_department}")
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
        - Departmanınızı seçin; senaryolar tamamen **o departmana özel** üretilecek.
        - Karşınıza toplam **10 farklı liderlik vakası** çıkacak.  
        - Her vakada **4 farklı karar seçeneği** sunulacak.  
        - Verdiğiniz kararlar birbirine **bağlı bir hikaye** oluşturacak.  
        - Sağ panelde, verdiğiniz her kararın etkilerini **anlık olarak** takip edebileceksiniz.  
        - Sonunda size özel bir **"Liderlik Karnesi"** hazırlanacak.

        ⚠️ *Unutmayın: Hiçbir seçenek mükemmel değildir. Gerçek liderlik, doğru dengeleri kurmaktır.*
        """)

    with col2:
        st.subheader("📝 Katılımcı Bilgileri")
        with st.form("giris_formu"):
            ad_soyad = st.text_input("Ad Soyad *", placeholder="Örn: Deniz Demirkaynak")

            departman_secenekleri = ["-- Seçiniz --"] + [f"{v['icon']} {k}" for k, v in DEPARTMANLAR.items()]
            secilen = st.selectbox("Departman *", departman_secenekleri)

            gonder = st.form_submit_button("🚀 Simülasyonu Başlat")

            if gonder:
                if ad_soyad.strip() == "":
                    st.warning("Lütfen devam etmek için adınızı ve soyadınızı girin.")
                elif secilen == "-- Seçiniz --":
                    st.warning("Lütfen devam etmek için bir departman seçin.")
                else:
                    temiz_departman = secilen.split(" ", 1)[1]  # ikonu at
                    st.session_state.user_name = ad_soyad.strip()
                    st.session_state.user_department = temiz_departman
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

        st.markdown(f'<div class="vaka-badge">VAKA {st.session_state.tur} / 10</div> <div class="dept-badge">{dept_icon} {st.session_state.user_department}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="olay-box">{current["olay"]}</div>', unsafe_allow_html=True)

        st.markdown("##### Liderlik Yaklaşımınız:")

        cb1, cb2 = st.columns(2)
        for i, s in enumerate(current['secenekler']):
            with (cb1 if i % 2 == 0 else cb2):
                if st.button(s['metin'], key=f"v_{st.session_state.tur}_{i}"):
                    for k, v in s['etki'].items():
                        st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))

                    st.session_state.secim_gecmisi.append(s.get('tip', 'Belirsiz'))

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

with col_side:
    st.markdown('<div class="journey-header">📜 Karar Yolculuğunuz</div>', unsafe_allow_html=True)

    if not st.session_state.karar_gecmisi:
        st.markdown('<div class="empty-journey">Henüz bir karar vermediniz.<br>İlk kararınızı verdiğinizde burada görünecek.</div>', unsafe_allow_html=True)
    else:
        for kayit in st.session_state.karar_gecmisi:
            karar_kartı_ciz(kayit)
