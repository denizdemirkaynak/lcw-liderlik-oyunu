import random
import html
from collections import Counter

import streamlit as st


# ==========================================================
# SAYFA AYARLARI
# ==========================================================

st.set_page_config(
    page_title="LCW Liderlik Simülasyonu",
    page_icon="💙",
    layout="wide",
)

TOPLAM_VAKA = 10


# ==========================================================
# TASARIM
# ==========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background-color: #f5f7fa;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    .hero-banner {
        background: linear-gradient(135deg, #0054a6 0%, #003d7a 100%);
        padding: 40px 50px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 84, 166, 0.25);
    }

    .hero-banner h1 {
        color: white;
        font-size: 2.4em;
        font-weight: 800;
        margin: 0;
    }

    .hero-banner p {
        color: #cfe0f5;
        font-size: 1.1em;
        margin-top: 8px;
        font-weight: 300;
    }

    .stat-card {
        background: white;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
        border-left: 5px solid #0054a6;
        margin-bottom: 10px;
    }

    .stat-label {
        font-size: 0.85em;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stat-value {
        font-size: 2em;
        font-weight: 700;
        color: #1f2937;
        margin: 4px 0;
    }

    .progress-outer {
        background-color: #e5e7eb;
        border-radius: 20px;
        height: 10px;
        width: 100%;
        overflow: hidden;
        margin-top: 8px;
    }

    .progress-inner {
        height: 100%;
        border-radius: 20px;
    }

    .vaka-badge {
        display: inline-block;
        background: #eaf1fb;
        color: #0054a6;
        padding: 6px 18px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.9em;
        margin-bottom: 15px;
    }

    .dept-badge {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        padding: 6px 18px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.85em;
        margin-bottom: 15px;
        margin-left: 8px;
    }

    .karakter-badge {
        display: inline-block;
        background: #ecfdf5;
        color: #047857;
        padding: 6px 18px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.85em;
        margin-bottom: 15px;
        margin-left: 8px;
    }

    .olay-box {
        background: white;
        border-radius: 16px;
        padding: 28px 30px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.07);
        font-size: 1.1em;
        line-height: 1.6;
        color: #1f2937;
        margin-bottom: 25px;
        border-top: 4px solid #0054a6;
    }

    .stButton > button {
        width: 100%;
        border-radius: 14px;
        height: auto !important;
        min-height: 6.5em;
        background-color: #ffffff;
        color: #0054a6;
        border: 1.5px solid #e0e4e8;
        font-weight: 500;
        white-space: normal !important;
        padding: 16px;
        font-size: 14.5px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.25s ease;
        text-align: left;
        line-height: 1.45;
        overflow: visible !important;
        word-wrap: break-word;
    }

    .stButton > button * {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }

    .stButton > button:hover {
        border-color: #0054a6;
        background-color: #0054a6;
        color: white;
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 84, 166, 0.25);
    }

    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #0054a6, #003d7a);
        color: white;
        font-weight: 700;
        font-size: 17px;
        min-height: 3.2em;
        border: none;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #003d7a, #0054a6);
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    h1, h2, h3 {
        font-weight: 700;
        color: #1f2937;
    }

    .rapor-kart {
        background: white;
        border-radius: 16px;
        padding: 22px 26px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
        margin-bottom: 16px;
    }

    .journey-header {
        background: white;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        font-weight: 700;
        color: #0054a6;
        font-size: 1.05em;
    }

    .history-card {
        background: white;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #0054a6;
        font-size: 0.85em;
    }

    .history-tur {
        font-weight: 700;
        color: #0054a6;
        font-size: 0.85em;
        margin-bottom: 4px;
    }

    .history-tip {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.72em;
        font-weight: 600;
        color: white;
        margin-bottom: 6px;
    }

    .history-metin {
        color: #4b5563;
        font-style: italic;
        font-size: 0.82em;
        margin-bottom: 8px;
        line-height: 1.4;
    }

    .history-stat-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.82em;
        margin-bottom: 3px;
    }

    .stat-up {
        color: #16a34a;
        font-weight: 700;
    }

    .stat-down {
        color: #dc2626;
        font-weight: 700;
    }

    .stat-same {
        color: #9ca3af;
        font-weight: 600;
    }

    .empty-journey {
        color: #9ca3af;
        font-size: 0.9em;
        text-align: center;
        padding: 20px 0;
    }

    .karakter-kart {
        background: white;
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #047857;
        font-size: 0.82em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# DEPARTMANLAR
# ==========================================================

DEPARTMANLAR = {
    "Mağazacılık": {
        "icon": "🏬",
        "karakterler": [
            "kasiyer",
            "reyon sorumlusu",
            "vardiya amiri",
            "depo sorumlusu",
            "mağaza müdür yardımcısı",
        ],
    },
    "Tedarik Zinciri": {
        "icon": "🚚",
        "karakterler": [
            "depo operasyon şefi",
            "sevkiyat planlama uzmanı",
            "lojistik koordinatörü",
            "envanter analisti",
            "iş güvenliği sorumlusu",
        ],
    },
    "Satın Alma": {
        "icon": "🛒",
        "karakterler": [
            "satın alma uzmanı",
            "kategori yöneticisi",
            "kalite kontrol sorumlusu",
            "tedarikçi ilişkileri uzmanı",
            "satın alma asistanı",
        ],
    },
    "İnsan Kaynakları": {
        "icon": "👥",
        "karakterler": [
            "İK uzmanı",
            "İK iş ortağı",
            "işe alım uzmanı",
            "eğitim sorumlusu",
            "bordro uzmanı",
        ],
    },
    "Pazarlama": {
        "icon": "📣",
        "karakterler": [
            "dijital pazarlama uzmanı",
            "marka yöneticisi",
            "sosyal medya editörü",
            "pazarlama asistanı",
            "kampanya yöneticisi",
        ],
    },
    "Finans": {
        "icon": "💰",
        "karakterler": [
            "finansal analist",
            "muhasebe uzmanı",
            "bütçe planlama sorumlusu",
            "iç denetim uzmanı",
            "finans asistanı",
        ],
    },
    "Bilgi Teknolojileri": {
        "icon": "💻",
        "karakterler": [
            "yazılım geliştirici",
            "sistem yöneticisi",
            "proje yöneticisi",
            "siber güvenlik uzmanı",
            "destek uzmanı",
        ],
    },
    "E-Ticaret": {
        "icon": "🌐",
        "karakterler": [
            "e-ticaret operasyon uzmanı",
            "müşteri deneyimi sorumlusu",
            "dijital kanal yöneticisi",
            "kargo süreçleri koordinatörü",
            "ürün içerik uzmanı",
        ],
    },
}

ISIM_HAVUZU = [
    "Ayşe Yıldız",
    "Mehmet Kara",
    "Elif Demir",
    "Can Öztürk",
    "Zeynep Aydın",
    "Burak Şahin",
    "Selin Kaya",
    "Emre Yılmaz",
    "Deren Aksoy",
    "Merve Çelik",
    "Kaan Polat",
    "Ece Arslan",
]

KISILIK_OZELLIKLERI = [
    "disiplinli ama esnek olmayan",
    "yaratıcı fakat dağınık",
    "çok çalışkan ama özgüvensiz",
    "hızlı karar veren ama sabırsız",
    "sadık ama değişime kapalı",
    "hırslı ve hızlı öğrenen",
    "duygusal zekâsı yüksek",
    "detaycı ve mükemmeliyetçi",
    "esprili ama zaman yönetimi zayıf",
    "sessiz ama gözlemci",
]

TIP_RENK = {
    "Demokratik": "#2563eb",
    "Otoriter": "#dc2626",
    "Koçvari": "#16a34a",
    "Kaçınmacı": "#6b7280",
}


# ==========================================================
# HAZIR VAKA HAVUZU
#
# Her departman için 12 vaka vardır.
# Her vaka tam 4 şıklıdır.
#
# Şık yazım biçimi:
# (metin, liderlik_tipi, moral, verimlilik, güven)
# ==========================================================

HAM_VAKALAR = {
    "Mağazacılık": [
        (
            "Kampanya haftasında bir üründe etiket hatası çıktı; kasada indirim yansımıyor ve müşteri kuyruğu büyüyor.",
            [
                ("Yetki sınırları içinde geçici kasa düzeltmesi uygulayıp kuyruğu yönetin.", "Otoriter", -5, 10, 5),
                ("Kasiyerleri ve reyon ekibini dinleyip müşterilere ortak bir çözüm açıklayın.", "Demokratik", 5, -5, 10),
                ("Bir çalışana hatayı izleme görevi verip ekipçe geçici süreç oluşturun.", "Koçvari", 5, 5, 5),
                ("Merkezden yanıt gelene kadar kasadaki tartışmalara müdahale etmeyin.", "Kaçınmacı", -10, -10, -15),
            ],
        ),
        (
            "Yeni sezon vitrin değişimi yetişmiyor; ekip yorgun ve bölge müdürünün ziyareti yaklaşıyor.",
            [
                ("Öncelikli alanları siz belirleyip görevleri yeniden dağıtın.", "Otoriter", -5, 10, 0),
                ("Ekiple kapsamı daraltıp hangi vitrinlerin önce biteceğine karar verin.", "Demokratik", 5, 0, 10),
                ("Yeni çalışanları deneyimli kişilerle eşleştirerek işi bölün.", "Koçvari", 10, 5, 5),
                ("Mevcut vitrinle devam edip gecikmeyi ziyarette açıklayın.", "Kaçınmacı", 0, -10, -10),
            ],
        ),
        (
            "Yoğun saatte bir kasiyer ile müşteri arasında tartışma çıktı; müşteri şikâyet oluşturacağını söylüyor.",
            [
                ("Kasiyeri kasadan alıp müşterinin sorununu hemen siz çözün.", "Otoriter", -5, 10, 0),
                ("İki tarafı ayrı ayrı dinleyip uygulanabilir çözümü açıklayın.", "Demokratik", 5, -5, 10),
                ("Olayı çözdükten sonra kasiyere sakin iletişim için geri bildirim verin.", "Koçvari", 5, 0, 10),
                ("Tartışmanın kendiliğinden bitmesini bekleyin.", "Kaçınmacı", -10, -5, -15),
            ],
        ),
        (
            "Kasa sayımlarında üç akşam üst üste küçük farklar oluştu; ekip birbirinden şüphelenmeye başladı.",
            [
                ("Kasa devir prosedürünü hemen değiştirip çift imza zorunluluğu koyun.", "Otoriter", -5, 10, 5),
                ("Ekiple süreçteki hata noktalarını konuşup ortak kontrol listesi hazırlayın.", "Demokratik", 5, 0, 10),
                ("Kasiyerlere tek tek destek verip devir uygulamasını birlikte çalışın.", "Koçvari", 10, 0, 5),
                ("Tutarlar küçük olduğu için farkları bir süre daha izlemekle yetinin.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Hafta sonu vardiyasında iki çalışan hastalandı; deneme kabinlerinde uzun kuyruk oluştu.",
            [
                ("Reyon görevlerini geçici olarak değiştirip kabinlere personel kaydırın.", "Otoriter", -5, 10, 0),
                ("Ekibe seçenekleri sorup yoğun saatler için ortak vardiya planı kurun.", "Demokratik", 5, 0, 10),
                ("Az yoğun reyondaki çalışanlara kabin sürecini hızlıca öğretin.", "Koçvari", 5, 5, 5),
                ("Eksik kadroyla devam edip müşterilerden anlayış bekleyin.", "Kaçınmacı", -5, -10, -10),
            ],
        ),
        (
            "Yeni gelen okul ürünlerinin bedenleri depoda karışmış; açılıştan önce reyonun hazırlanması gerekiyor.",
            [
                ("Ürünleri hızlı sayım için gruplara ayırıp görevleri doğrudan dağıtın.", "Otoriter", -5, 10, 0),
                ("Depo ve reyon ekipleriyle öncelikli bedenleri birlikte belirleyin.", "Demokratik", 5, 0, 10),
                ("Deneyimli bir çalışanı yeni personele eşleştirip sayımı birlikte yaptırın.", "Koçvari", 10, 5, 5),
                ("Karışık kolileri kapalı tutup reyonu eksik ürünle açın.", "Kaçınmacı", 0, -10, -10),
            ],
        ),
        (
            "Bir müşteri etiketi kopmuş ürünü iade etmek istiyor; çalışanlar iade kuralını farklı yorumluyor.",
            [
                ("Mevcut iade kuralını kontrol edip o vaka için net karar verin.", "Otoriter", 0, 10, 5),
                ("Müşteriyi dinleyip çalışanlarla birlikte kuralın uygun uygulamasını değerlendirin.", "Demokratik", 5, -5, 10),
                ("İade sonrasında ekibe benzer durumlar için kısa bir uygulama eğitimi verin.", "Koçvari", 5, 5, 5),
                ("Kararı başka vardiyaya bırakıp müşteriden sonra gelmesini isteyin.", "Kaçınmacı", -5, -10, -10),
            ],
        ),
        (
            "Stok sayımında çocuk montlarında sistem ile raf arasında 18 adet fark çıktı; kampanya yarın başlıyor.",
            [
                ("İlgili satış ve depo hareketlerini bugün yeniden saydırın.", "Otoriter", -5, 10, 5),
                ("Depo ve satış ekipleriyle farkın olası kaynaklarını ortak inceleyin.", "Demokratik", 5, 0, 10),
                ("Sayım ekibine hata kontrol adımlarını gösterip yeniden sayımı yönetin.", "Koçvari", 5, 5, 5),
                ("Kampanya bitene kadar farkı kayıtlara işlemeyin.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Görsel düzenleme ekibi kampanya masasını kapı önüne taşıdı; güvenlik görevlisi geçişin daraldığını bildirdi.",
            [
                ("Masayı güvenli alana hemen taşıtıp açılış düzenini değiştirin.", "Otoriter", -5, 10, 5),
                ("Güvenlik ve satış ekipleriyle güvenli bir yerleşim belirleyin.", "Demokratik", 5, 0, 10),
                ("Görsel ekiple yerleşim ölçülerini gözden geçirip yeni düzeni birlikte kurun.", "Koçvari", 5, 5, 5),
                ("Yoğunluk azalır diye mevcut yerleşimi koruyun.", "Kaçınmacı", -10, -10, -15),
            ],
        ),
        (
            "Aynı müşteri farklı günlerde iki çalışan hakkında benzer hizmet şikâyeti bıraktı.",
            [
                ("Hizmet adımlarını yeniden duyurup ilgili vardiyada yakın takip başlatın.", "Otoriter", -5, 10, 0),
                ("Müşteri geri bildirimini ekiple paylaşmadan önce çalışanları ayrı ayrı dinleyin.", "Demokratik", 5, 0, 10),
                ("Çalışanlarla kısa canlandırmalar yapıp zor müşteri konuşmalarını çalışın.", "Koçvari", 10, 0, 5),
                ("Şikâyetleri öznel bularak ekiple konuşmayın.", "Kaçınmacı", -5, -5, -15),
            ],
        ),
        (
            "Hafta sonu kampanyasında popüler bir ürün sabah tükendi; çevre mağazada sınırlı stok var.",
            [
                ("Onaylı mağazalar arası transfer sürecini hemen başlatın.", "Otoriter", 0, 10, 5),
                ("Çevre mağaza ve satış ekibiyle ürünleri hangi müşterilere ayıracağınızı planlayın.", "Demokratik", 5, 0, 10),
                ("Ekibe alternatif ürün önerileri hazırlatıp müşteri iletişimini destekleyin.", "Koçvari", 5, 5, 5),
                ("Ürün gelene kadar müşterileri bilgilendirmeden bekletin.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Yeni bir çalışan, yoğun saatte yanlış raf etiketleri bastığını fark etti ve bunu size çekinerek söyledi.",
            [
                ("Hatalı etiketleri hemen toplatıp doğrulama kontrolü başlatın.", "Otoriter", -5, 10, 5),
                ("Çalışana teşekkür edip ekiple etiket kontrolünü birlikte organize edin.", "Demokratik", 5, 0, 10),
                ("Çalışanla etiket basım adımlarını yeniden uygulayıp destek verin.", "Koçvari", 10, 5, 5),
                ("Müşteri şikâyeti gelene kadar etiketleri değiştirmeyin.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
    ],

    "Tedarik Zinciri": [
        (
            "Kritik bir sevkiyat gümrükte üç gündür bekliyor; 12 mağaza üründe stoksuz kalma riski taşıyor.",
            [
                ("Resmî süreci hızlandırmak için müşavirden bugün net aksiyon planı isteyin.", "Otoriter", -5, 10, 5),
                ("Mağazaları bilgilendirip alternatif stok dağıtımını birlikte planlayın.", "Demokratik", 5, 0, 10),
                ("Ekiple gecikme nedenini inceleyip geleceğe dönük yedek plan kurun.", "Koçvari", 5, 5, 5),
                ("Sevkiyat gelene kadar mağazalara bilgi vermeyin.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Depo kapasitesi sınırına dayandı; yeni sezon ürünleri için boş yer kalmadı.",
            [
                ("Onaylı geçici alanı açıp ürün yerleşimini hemen yeniden düzenleyin.", "Otoriter", -5, 10, 0),
                ("Mağazalarla görüşüp uygun ürünler için erken sevkiyat planlayın.", "Demokratik", 5, 0, 10),
                ("Depo ekibine yerleşim iyileştirmesi için küçük gruplar kurdurun.", "Koçvari", 10, 5, 5),
                ("Yeni ürünleri boş koridorlarda geçici olarak biriktirin.", "Kaçınmacı", -10, -10, -15),
            ],
        ),
        (
            "Yeni depo yönetim sisteminde kıdemli çalışanlar barkod adımlarında zorlanıyor; işlem hataları artıyor.",
            [
                ("Hatalı işlemleri durdurup kontrol adımlarını zorunlu hâle getirin.", "Otoriter", -5, 10, 0),
                ("Çalışanlardan zorlandıkları ekranları öğrenip destek planını birlikte belirleyin.", "Demokratik", 5, 0, 10),
                ("Deneyimli kullanıcılarla kısa bire bir uygulama seansları düzenleyin.", "Koçvari", 10, 5, 5),
                ("Hataları dönem sonu değerlendirmesinde ele almayı bekleyin.", "Kaçınmacı", -5, -10, -10),
            ],
        ),
        (
            "Bir forklift operatörü, acil sevkiyat baskısı nedeniyle dar koridorda güvenlik mesafesinin ihlal edildiğini bildirdi.",
            [
                ("O koridordaki operasyonu durdurup güvenli rota belirleyin.", "Otoriter", -5, -5, 15),
                ("Operatör ve iş güvenliği ekibiyle sevkiyat sırasını yeniden planlayın.", "Demokratik", 5, 0, 10),
                ("Vardiyaya güvenli geçiş uygulaması yaptırıp yük akışını düzenleyin.", "Koçvari", 5, 5, 10),
                ("Sevkiyat bitince koridoru incelemek üzere not alın.", "Kaçınmacı", -10, 5, -15),
            ],
        ),
        (
            "Nakliye firması son dakika araç değişikliği yaptı; yeni araç planlanan paletlerin tamamını alamıyor.",
            [
                ("En kritik mağaza paletlerini belirleyip ikinci araç talep edin.", "Otoriter", -5, 10, 5),
                ("Mağaza ve nakliyeciyle teslim önceliklerini birlikte kararlaştırın.", "Demokratik", 5, 0, 10),
                ("Planlama ekibiyle araç kapasitesi kontrol adımını yeniden tasarlayın.", "Koçvari", 5, 5, 5),
                ("Eksik paletleri bildirmeden bir sonraki güne bırakın.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "İade ürünleri gelen sevkiyatla aynı alana bırakıldı; ürünlerin yeniden satışa uygunluğu karışıyor.",
            [
                ("İade alanını hemen ayırıp karışan ürünleri karantinaya alın.", "Otoriter", -5, 5, 10),
                ("Kalite ve depo ekipleriyle ayrıştırma önceliğini birlikte belirleyin.", "Demokratik", 5, 0, 10),
                ("Ekip liderlerine iade kabul kontrolünü yeniden uygulatın.", "Koçvari", 5, 5, 5),
                ("Yoğunluk bitene kadar ürünleri aynı alanda tutun.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Talep tahmini düşük kaldığı için okul dönemi ürünleri üç bölgede erken tükendi.",
            [
                ("Mevcut stokları bölgelere göre yeniden dağıtma kararı alın.", "Otoriter", -5, 10, 0),
                ("Bölge ekipleriyle satış hızlarını karşılaştırıp ortak dağıtım yapın.", "Demokratik", 5, 0, 10),
                ("Analistlerle tahmin hatasını inceleyip yeni uyarı eşiği oluşturun.", "Koçvari", 5, 5, 5),
                ("Yeni sipariş gelene kadar mağazaların çözüm bulmasını bekleyin.", "Kaçınmacı", -5, -10, -10),
            ],
        ),
        (
            "Yağış nedeniyle sevkiyat merkezine gelen kamyonlar gecikiyor; gece vardiyasının mesaisi uzuyor.",
            [
                ("Araç kabul sırasını değiştirip kritik yükleri öne alın.", "Otoriter", -5, 10, 0),
                ("Vardiya ve taşıyıcılarla gerçekçi yeni teslim saatleri belirleyin.", "Demokratik", 5, 0, 10),
                ("Ekibe görev dönüşümü uygulayıp aşırı yüklenen çalışanları destekleyin.", "Koçvari", 10, 0, 5),
                ("Kamyonların geliş sırasına göre bekleyip planı değiştirmeyin.", "Kaçınmacı", -5, -10, -10),
            ],
        ),
        (
            "Bir tedarikçinin kolilerinde ürün kodu etiketleri yanlış; otomatik ayırma hattı kolileri reddediyor.",
            [
                ("Hattı koruyup sorunlu kolileri manuel kontrol alanına alın.", "Otoriter", -5, 5, 10),
                ("Tedarikçi ve kabul ekibiyle düzeltme sırasını birlikte belirleyin.", "Demokratik", 5, 0, 10),
                ("Kabul ekibiyle etiket doğrulama örneklemesini geliştirip uygulayın.", "Koçvari", 5, 5, 5),
                ("Etiketleri kontrol etmeden manuel olarak sevkiyata ekleyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Depoda aynı SKU iki farklı lokasyonda görünüyor; sipariş toplama ekibi yanlış rafa gidiyor.",
            [
                ("İlgili SKU için toplama işlemini durdurup lokasyonları doğrulayın.", "Otoriter", -5, -5, 10),
                ("Toplama ve envanter ekipleriyle gerçek lokasyonu birlikte teyit edin.", "Demokratik", 5, 0, 10),
                ("Ekip lideriyle lokasyon güncelleme kontrolünü yeniden çalışın.", "Koçvari", 5, 5, 5),
                ("Ekipten ürünü buldukları raftan toplamalarını isteyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Bir bölgeye ayrılan yeni sezon ürünleri yanlış aktarma merkezine yönlendirildi.",
            [
                ("Gönderileri durdurup doğru aktarma merkezine yönlendirme başlatın.", "Otoriter", -5, 5, 10),
                ("Taşıyıcı ve bölge ekibiyle yeni teslim takvimini açıkça paylaşın.", "Demokratik", 5, 0, 10),
                ("Planlama ekibiyle yönlendirme kontrol noktasını yeniden tasarlayın.", "Koçvari", 5, 5, 5),
                ("Aktarma merkezinin hatayı kendiliğinden fark etmesini bekleyin.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Gece vardiyasında tarayıcı cihazların yarısı şarj olmuyor; sabah sevkiyatı yaklaşırken toplama yavaşladı.",
            [
                ("Çalışanları çalışan cihazlara göre yeniden dağıtıp teknik destek çağırın.", "Otoriter", -5, 10, 5),
                ("Ekipten darboğazları öğrenip kritik siparişleri birlikte sıralayın.", "Demokratik", 5, 0, 10),
                ("Yedek cihaz ve şarj kontrol rutini için çalışanlara sorumluluk verin.", "Koçvari", 5, 5, 5),
                ("Cihazlar düzelene kadar tüm siparişleri bekletin.", "Kaçınmacı", -5, -15, -10),
            ],
        ),
    ],

    "Satın Alma": [
        (
            "Ana tedarikçi sezon başlamasına iki hafta kala fiyatlarda %18 artış bildirdi.",
            [
                ("Sözleşme maddelerini kontrol edip fiyat değişikliğine resmî itiraz edin.", "Otoriter", -5, 5, 5),
                ("Tedarikçiyle miktar ve takvim seçeneklerini masaya yatırın.", "Demokratik", 5, 0, 10),
                ("Ekiple alternatif tedarikçi ve maliyet senaryoları hazırlayın.", "Koçvari", 5, 5, 5),
                ("Artışı değerlendirmeden kabul edip bütçe farkını sonra ele alın.", "Kaçınmacı", -5, -5, -15),
            ],
        ),
        (
            "Onaylı numuneye kıyasla seri üretimde kumaş kalitesi düştü; teslim tarihine on gün kaldı.",
            [
                ("Uygunsuz partiyi durdurup sözleşmedeki kalite şartlarını uygulayın.", "Otoriter", -5, -10, 15),
                ("Kalite ve üretim ekipleriyle uygun partilerin teslim seçeneğini görüşün.", "Demokratik", 5, -5, 10),
                ("Ekiple hızlı yeniden numune ve düzeltme planı oluşturun.", "Koçvari", 5, 0, 5),
                ("Tarih kaçmasın diye kalite farkını bildirmeden kabul edin.", "Kaçınmacı", -5, 10, -15),
            ],
        ),
        (
            "Yeni bir tedarikçi düşük fiyat öneriyor ancak gerekli sürdürülebilirlik belgelerini henüz paylaşmadı.",
            [
                ("Belgeler tamamlanmadan sipariş onayını vermeyin.", "Otoriter", 0, -5, 15),
                ("Uyum ekibi ve tedarikçiyle doğrulama takvimi belirleyin.", "Demokratik", 5, 0, 10),
                ("Ekibe alternatif uygun tedarikçileri karşılaştırma görevi verin.", "Koçvari", 5, 5, 5),
                ("Belgeleri sonra isteriz diyerek siparişi hemen açın.", "Kaçınmacı", -5, 10, -15),
            ],
        ),
        (
            "Kategori yöneticisi onay almadan tedarikçiye sözlü fiyat taahhüdünde bulundu.",
            [
                ("Taahhüdün bağlayıcılığını inceleyip onay sürecini durdurun.", "Otoriter", -5, 5, 10),
                ("Yönetici ve tedarikçiyle şartları şeffaf biçimde yeniden görüşün.", "Demokratik", 5, 0, 10),
                ("Yöneticiyle özel görüşüp yetki sınırları için gelişim planı yapın.", "Koçvari", 10, 0, 5),
                ("Konu büyümesin diye taahhüdü sorgulamadan kabul edin.", "Kaçınmacı", 0, -5, -15),
            ],
        ),
        (
            "Yeni sezon çocuk ürünlerinde iki tedarikçi aynı teslim tarihini verdi; birinin kapasite geçmişi zayıf.",
            [
                ("Geç teslim geçmişi olan tedarikçiye kapasite kanıtı şartı koyun.", "Otoriter", -5, 5, 10),
                ("Ekipçe fiyat, kalite ve teslim risklerini puanlayarak karar verin.", "Demokratik", 5, 0, 10),
                ("Genç satın almacıya risk karşılaştırması hazırlatıp birlikte gözden geçirin.", "Koçvari", 10, 0, 5),
                ("Sadece düşük fiyatı seçip geçmiş performansı dikkate almayın.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Onay bekleyen ambalaj değişikliği ürün başına maliyeti düşürüyor ama raf görünümünü etkileyebilir.",
            [
                ("Tasarım onayı alınana kadar ambalaj değişikliğini bekletin.", "Otoriter", 0, -5, 10),
                ("Mağaza ve tasarım ekipleriyle küçük bir karşılaştırma testi planlayın.", "Demokratik", 5, 0, 10),
                ("Ekibe maliyet ve müşteri deneyimi etkisini ölçme görevi verin.", "Koçvari", 5, 5, 5),
                ("Tasarruf için deneme yapmadan tüm siparişleri değiştirin.", "Kaçınmacı", -5, 10, -10),
            ],
        ),
        (
            "Döviz kurundaki ani artış, imzalanmamış sezon siparişlerinin bütçesini aştı.",
            [
                ("Yeni siparişleri kısa süre durdurup bütçe sınırını yeniden belirleyin.", "Otoriter", -5, -5, 10),
                ("Finans ve kategori ekipleriyle ürün önceliklerini birlikte düzenleyin.", "Demokratik", 5, 0, 10),
                ("Satın alma ekibiyle farklı kur senaryoları hazırlayıp eğitim yapın.", "Koçvari", 5, 5, 5),
                ("Bütçe aşımını dönem sonunda bildirmek üzere siparişleri açın.", "Kaçınmacı", -5, 10, -15),
            ],
        ),
        (
            "Tedarikçi, test raporu geciktiği için bebek ürünlerinin sevkini bekletiyor.",
            [
                ("Rapor gelmeden sevkiyata onay vermeyip takvimi güncelleyin.", "Otoriter", -5, -5, 15),
                ("Kalite ve planlama ekipleriyle mağazalara alternatif ürün bulun.", "Demokratik", 5, 0, 10),
                ("Ekibe test takibini erken uyarı listesine ekleme görevi verin.", "Koçvari", 5, 5, 5),
                ("Raporu teslimden sonra almak üzere sevkiyatı başlatın.", "Kaçınmacı", -5, 10, -15),
            ],
        ),
        (
            "İki tedarikçi aynı kumaşı sunuyor; uygun fiyatlı olanın teslim süreleri son üç siparişte değişti.",
            [
                ("Teslim güvencesi olmadan uygun fiyatlı teklifi onaylamayın.", "Otoriter", -5, 0, 10),
                ("Planlama ekibiyle gecikmenin mağaza etkisini değerlendirip karar verin.", "Demokratik", 5, 0, 10),
                ("Ekibe kademeli sipariş ve yedek tedarik planı hazırlatın.", "Koçvari", 5, 5, 5),
                ("Geçmiş gecikmeleri önemsemeyip tüm hacmi düşük fiyatlı firmaya verin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Numune toplantısında kalite sorumlusu, seçilen ürünün yıkama testinin tekrar edilmesini istedi.",
            [
                ("Test sonucu gelene kadar nihai sipariş onayını bekletin.", "Otoriter", -5, -5, 15),
                ("Kalite ve kategori ekiplerinin gerekçelerini açıkça karşılaştırın.", "Demokratik", 5, 0, 10),
                ("Ekibe daha erken numune test takvimi tasarlatın.", "Koçvari", 5, 5, 5),
                ("Toplantı uzamasın diye test talebini kayda almadan geçin.", "Kaçınmacı", -5, 10, -15),
            ],
        ),
        (
            "Bir tedarikçinin teklifindeki ödeme süresi değişikliği toplam maliyeti artırıyor; ekip sadece birim fiyata baktı.",
            [
                ("Kararı durdurup toplam maliyet hesabı isteyin.", "Otoriter", -5, 5, 10),
                ("Finans ve satın alma ekibiyle ödeme şartlarını birlikte karşılaştırın.", "Demokratik", 5, 0, 10),
                ("Ekibe toplam maliyet hesabı için standart şablon hazırlatın.", "Koçvari", 5, 5, 5),
                ("Birim fiyat düşük diye diğer şartları incelemeden imzalayın.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Üretici, teslimatı yetiştirmek için onaylı üretim tesisinin dışındaki bir atölyeyi kullanmak istiyor.",
            [
                ("Tesis uygunluğu doğrulanana kadar üretim değişikliğini reddedin.", "Otoriter", -5, -5, 15),
                ("Uyum ve kalite ekipleriyle onaylanabilir seçenekleri görüşün.", "Demokratik", 5, 0, 10),
                ("Ekibe alternatif kapasite ve yeni teslim planı hazırlatın.", "Koçvari", 5, 5, 5),
                ("Atölye bilgisini kayda geçirmeden üretimi kabul edin.", "Kaçınmacı", -5, 10, -15),
            ],
        ),
    ],

    "İnsan Kaynakları": [
        (
            "İki çalışan aynı terfi için güçlü aday; ikisi de kararın adil olmasını bekliyor.",
            [
                ("Önceden belirlenmiş kriterlere göre kararı verip gerekçesini açıklayın.", "Otoriter", -5, 10, 5),
                ("Değerlendirme kurulundan aynı kriterlerle bağımsız görüş alın.", "Demokratik", 5, -5, 15),
                ("Her adayla gelişim alanı ve sonraki fırsatları ayrı ayrı konuşun.", "Koçvari", 10, 0, 10),
                ("Tepki gelmesin diye terfi kararını belirsiz süre erteleyin.", "Kaçınmacı", -10, -5, -15),
            ],
        ),
        (
            "Bir yönetici hakkında anonim mobbing şikâyeti geldi; iddialar henüz doğrulanmadı.",
            [
                ("Gizlilik ve tarafsızlık ilkeleriyle resmî inceleme başlatın.", "Otoriter", 0, -5, 15),
                ("İlgili prosedür uyarınca tarafların ayrı ayrı dinlenmesini sağlayın.", "Demokratik", 5, -5, 10),
                ("İnceleme ekibine güvenli bildirim sürecinde destek verin.", "Koçvari", 5, 0, 10),
                ("İsimsiz diye şikâyeti kayda almadan kapatın.", "Kaçınmacı", -15, 0, -15),
            ],
        ),
        (
            "Yeni işe alınanların üçte biri ilk ayda ayrılıyor; nedenler kayıt altına alınmamış.",
            [
                ("Çıkış görüşmelerini standart hâle getirip ilk ay verilerini isteyin.", "Otoriter", -5, 10, 5),
                ("Yeni çalışanlar ve yöneticilerle başlangıç deneyimini birlikte inceleyin.", "Demokratik", 5, 0, 10),
                ("Mentorluk ve ilk hafta görüşmelerini pilot olarak başlatın.", "Koçvari", 10, 5, 5),
                ("Ayrılmaların sezonluk olduğunu varsayıp süreçleri değiştirmeyin.", "Kaçınmacı", -5, -10, -10),
            ],
        ),
        (
            "Bir çalışan, vardiya planlarının aile sorumlulukları açısından sürekli değiştiğini söylüyor.",
            [
                ("Planı ve mevzuat gerekliliklerini kontrol edip düzenli yayımlama kuralı koyun.", "Otoriter", 0, 5, 10),
                ("Çalışan ve yöneticisiyle uygulanabilir vardiya seçeneklerini görüşün.", "Demokratik", 5, 0, 10),
                ("Yöneticiye öngörülebilir planlama için destek ve araç sağlayın.", "Koçvari", 10, 5, 5),
                ("Konuyu kişisel sorun sayıp kayıt altına almayın.", "Kaçınmacı", -10, 0, -15),
            ],
        ),
        (
            "Performans döneminde bir yönetici tüm ekibine aynı puanı verdi; gerekçe yazmamış.",
            [
                ("Değerlendirmeleri gerekçeleriyle yeniden hazırlamasını isteyin.", "Otoriter", -5, 5, 10),
                ("Yöneticiyle kriterleri gözden geçirip kalibrasyon toplantısı yapın.", "Demokratik", 5, 0, 10),
                ("Yöneticiye kanıta dayalı geri bildirim konusunda koçluk verin.", "Koçvari", 10, 0, 5),
                ("Takvim sıkışık diye aynı puanları değiştirmeden onaylayın.", "Kaçınmacı", -5, 10, -15),
            ],
        ),
        (
            "Bir çalışanın izin talebi sistemde onaylı görünüyor; yöneticisi vardiyada olmasını bekliyor.",
            [
                ("Sistem kayıtlarını kontrol edip onaylı izni esas alarak vardiyayı düzeltin.", "Otoriter", 0, 5, 10),
                ("Çalışan ve yöneticiyle hatanın nasıl oluştuğunu ayrı ayrı netleştirin.", "Demokratik", 5, 0, 10),
                ("Yöneticiye izin planlama ve yedekleme adımlarında destek verin.", "Koçvari", 10, 5, 5),
                ("Çalışandan iznini iptal etmesini isteyip kaydı sonra düzeltin.", "Kaçınmacı", -10, 5, -15),
            ],
        ),
        (
            "Çıkış görüşmelerinde farklı ekiplerden çalışanlar eğitim eksikliğini tekrar tekrar dile getiriyor.",
            [
                ("Yüksek riskli roller için zorunlu eğitim listesini hemen güncelleyin.", "Otoriter", -5, 5, 10),
                ("Ekiplerle ihtiyaçları belirleyip öncelikli eğitimleri birlikte seçin.", "Demokratik", 5, 0, 10),
                ("Deneyimli çalışanlarla iç mentorluk pilotu oluşturun.", "Koçvari", 10, 5, 5),
                ("Bütçe dönemi gelene kadar geri bildirimleri arşivleyin.", "Kaçınmacı", -5, -5, -10),
            ],
        ),
        (
            "Adaya gönderilen teklif mektubunda maaş aralığı yanlış yazılmış; aday teklifi kabul etmek üzere.",
            [
                ("Hatalı teklifi hemen durdurup doğru koşulları yazılı olarak bildirin.", "Otoriter", -5, -5, 15),
                ("Adaya hatayı açıkça anlatıp seçeneklerini değerlendirmesi için süre tanıyın.", "Demokratik", 5, -5, 10),
                ("İşe alım ekibiyle teklif kontrolünü çift onaylı hâle getirin.", "Koçvari", 5, 5, 5),
                ("Aday kabul ettikten sonra hatayı açıklamayı planlayın.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Bir ekipte fazla mesai kayıtları artıyor ancak iş yükü raporları bunu açıklamıyor.",
            [
                ("Kayıtları ve yasal sınırları inceleyip yöneticiden plan isteyin.", "Otoriter", -5, 5, 10),
                ("Çalışanlar ve yöneticiyle gerçek iş yükünü güvenli biçimde konuşun.", "Demokratik", 5, 0, 10),
                ("Yöneticiye kapasite planı ve görev dağılımı konusunda destek verin.", "Koçvari", 10, 5, 5),
                ("Ay sonuna kadar artışı sorgulamadan onaylayın.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Yeni başlayan bir çalışan, oryantasyonda anlatılan görevlerle fiilî işinin farklı olduğunu bildiriyor.",
            [
                ("Görev tanımını ve uygulamayı kontrol edip uyuşmazlığı düzeltin.", "Otoriter", 0, 5, 10),
                ("Çalışan ve yöneticiyle beklentileri ortak görüşmede netleştirin.", "Demokratik", 5, 0, 10),
                ("Yöneticiyle oryantasyon kontrol listesi geliştirip çalışana rehber sağlayın.", "Koçvari", 10, 5, 5),
                ("Alışması için çalışandan birkaç ay beklemesini isteyin.", "Kaçınmacı", -5, -5, -10),
            ],
        ),
        (
            "Bir yönetici, çalışanına yapacağı zor geri bildirim görüşmesine İK'nın katılmasını istiyor.",
            [
                ("Görüşmenin amacını ve belgeleri netleştirip uygun süreci belirleyin.", "Otoriter", -5, 5, 10),
                ("İki tarafın da kendini ifade edebileceği görüşme çerçevesi kurun.", "Demokratik", 5, 0, 10),
                ("Yöneticiyle geri bildirim dilini önceden çalışıp görüşmeyi destekleyin.", "Koçvari", 10, 5, 5),
                ("Görüşmeyi yöneticinin tek başına çözmesi gerektiğini söyleyip çekilin.", "Kaçınmacı", -5, 0, -10),
            ],
        ),
        (
            "Anonim çalışan anketinde bir departmanda güven puanı ciddi biçimde düştü; neden bilinmiyor.",
            [
                ("Sonuçları yöneticiyle paylaşıp ölçülebilir iyileştirme planı isteyin.", "Otoriter", -5, 5, 5),
                ("Gizliliği koruyan gönüllü görüşmelerle nedenleri araştırın.", "Demokratik", 5, 0, 10),
                ("Yönetici ve ekibe düzenli geri bildirim oturumları için rehberlik edin.", "Koçvari", 10, 5, 5),
                ("Bir sonraki anketi bekleyip konuyu açmayın.", "Kaçınmacı", -5, -5, -15),
            ],
        ),
    ],

    "Pazarlama": [
        (
            "İş birliği yapılan bir içerik üreticisi, kampanyadan bir gün önce tartışmalı bir paylaşım yaptı.",
            [
                ("Sözleşme ve marka riskini değerlendirip yayını geçici durdurun.", "Otoriter", -5, -5, 10),
                ("İletişim ve hukuk ekipleriyle ortak yanıt belirleyin.", "Demokratik", 5, 0, 10),
                ("Ekibe yedek içerik ve iletişim akışı hazırlatın.", "Koçvari", 5, 5, 5),
                ("Paylaşımın unutulmasını bekleyip kampanyayı değiştirmeyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Kampanyanın ana görseli lansmana 24 saat kala teslim edilmedi.",
            [
                ("Kritik kanalları seçip sade görselle yayına çıkma kararı alın.", "Otoriter", -5, 10, 0),
                ("Tasarım ekibiyle kapsamı ve gerçekçi teslim saatini birlikte netleştirin.", "Demokratik", 5, 0, 10),
                ("Tasarımcıları görevlerine göre eşleştirip engelleri kaldırın.", "Koçvari", 10, 5, 5),
                ("Son ana kadar bekleyip diğer ekipleri bilgilendirmeyin.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Rakip marka planladığınız kampanyaya benzer bir fikri bir hafta önce yayımladı.",
            [
                ("Fark yaratan ürün mesajını öne çıkarıp takvimi koruyun.", "Otoriter", -5, 10, 0),
                ("Ekipçe benzer noktaları inceleyip yaratıcı içeriği revize edin.", "Demokratik", 5, 0, 10),
                ("Genç ekibe hızlı müşteri testi yaptırıp öğrendiklerini uygulayın.", "Koçvari", 10, 5, 5),
                ("Karar vermeyip kampanyayı sessizce erteleyin.", "Kaçınmacı", -5, -10, -10),
            ],
        ),
        (
            "Sosyal medyada yanlış fiyat bilgisini içeren kampanya paylaşımı kısa sürede yayıldı.",
            [
                ("Yanlış içeriği durdurup doğru fiyatla açık düzeltme yayımlayın.", "Otoriter", -5, 5, 10),
                ("Satış ve müşteri hizmetleriyle müşterilere ortak açıklama hazırlayın.", "Demokratik", 5, 0, 10),
                ("Ekiple yayın öncesi fiyat doğrulama kontrolü oluşturun.", "Koçvari", 5, 5, 5),
                ("Kimse fark etmez diye paylaşımı sessizce silin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Bir reklam grubunda bütçenin yarısı harcandı ancak satış dönüşümü hedefin çok altında.",
            [
                ("Düşük performanslı reklamları durdurup bütçeyi koruyun.", "Otoriter", -5, 5, 5),
                ("Analiz ekibiyle kanalları karşılaştırıp yeni dağılıma karar verin.", "Demokratik", 5, 0, 10),
                ("Ekibe küçük yaratıcı testler yaptırıp öğrenme planı çıkarın.", "Koçvari", 5, 5, 5),
                ("Kampanya bitene kadar performans düşüşünü raporlamayın.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Yeni sezon tanıtımında kullanılan ürün görseli, mağazalardaki gerçek renk tonuyla uyuşmuyor.",
            [
                ("Görseli kontrol için yayından çekip doğru ürün görseli isteyin.", "Otoriter", -5, -5, 10),
                ("Ürün ve müşteri deneyimi ekipleriyle farkı değerlendirip açıklayın.", "Demokratik", 5, 0, 10),
                ("Tasarım ekibiyle ürün doğrulama adımı oluşturun.", "Koçvari", 5, 5, 5),
                ("Renk farkını küçük görüp reklamı değiştirmeyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "E-posta kampanyasında yanlış müşteri grubuna çocuk ürünleri mesajı gönderildi.",
            [
                ("Gönderimi durdurup kapsamı ve veri güvenliği etkisini inceleyin.", "Otoriter", -5, 0, 10),
                ("CRM ve iletişim ekipleriyle uygun düzeltme mesajını planlayın.", "Demokratik", 5, 0, 10),
                ("Ekiple hedef kitle seçimi için çift kontrol uygulaması başlatın.", "Koçvari", 5, 5, 5),
                ("Şikâyet gelmedikçe hatayı kayda geçirmeyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Bir mağaza kampanya afişlerini taktı ancak dijital reklamda farklı başlangıç tarihi görünüyor.",
            [
                ("Yanlış tarihli reklamı durdurup tek resmî takvim yayımlayın.", "Otoriter", -5, 5, 10),
                ("Mağaza ve dijital ekiplerle hangi kanalların etkilendiğini belirleyin.", "Demokratik", 5, 0, 10),
                ("Kampanya ekibiyle tarih kontrol çizelgesini birlikte geliştirin.", "Koçvari", 5, 5, 5),
                ("Müşteriler sorarsa mağazaların açıklamasını bekleyin.", "Kaçınmacı", -5, -5, -15),
            ],
        ),
        (
            "Yeni koleksiyon için hazırlanan sloganın başka bir markanın sloganına çok benzediği fark edildi.",
            [
                ("Sloganın kullanımını durdurup hukuk ve marka incelemesi isteyin.", "Otoriter", -5, -5, 15),
                ("Yaratıcı ekip ve hukukla alternatif mesajları birlikte değerlendirin.", "Demokratik", 5, 0, 10),
                ("Ekibe özgünlük kontrolü içeren yeni yaratıcı süreç tasarlatın.", "Koçvari", 5, 5, 5),
                ("Lansman yaklaşınca benzerliği görmezden gelin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Sosyal medya ekibi müşteri yorumlarına çok farklı tonlarda yanıt veriyor.",
            [
                ("Riskli yanıtları durdurup geçici yanıt ilkeleri yayımlayın.", "Otoriter", -5, 5, 5),
                ("Ekipten örnekleri toplayıp ortak marka dili belirleyin.", "Demokratik", 5, 0, 10),
                ("Editörlerle gerçek yorumlar üzerinden kısa uygulama çalışın.", "Koçvari", 10, 5, 5),
                ("Yorumları bireysel üslup meselesi sayıp müdahale etmeyin.", "Kaçınmacı", -5, -5, -10),
            ],
        ),
        (
            "Mağazalardan gelen geri bildirim, tanıtılan ürüne olan talebin eldeki stoktan fazla olduğunu gösteriyor.",
            [
                ("Stok netleşene kadar ürün odaklı reklamın hızını düşürün.", "Otoriter", -5, 0, 10),
                ("Tedarik ve mağazalarla bölgesel reklam planını yeniden kurun.", "Demokratik", 5, 0, 10),
                ("Ekibe benzer stoktaki ürünler için alternatif içerik hazırlatın.", "Koçvari", 5, 5, 5),
                ("Stok bilgisine bakmadan reklamı aynı hızda sürdürün.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Yerel bir kampanyada kullanılan görsel, farklı bir şehirdeki hedef kitle tarafından yanlış anlaşıldı.",
            [
                ("İlgili bölgedeki yayını durdurup görseli incelemeye alın.", "Otoriter", -5, -5, 10),
                ("Yerel ekiplerden geri bildirim alıp uygun anlatımı birlikte seçin.", "Demokratik", 5, 0, 10),
                ("Ekiple bölgesel ön test süreci oluşturup yeni görsel geliştirin.", "Koçvari", 5, 5, 5),
                ("Geri bildirimi küçük bir grup ile sınırlı görüp değişiklik yapmayın.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
    ],

    "Finans": [
        (
            "Üst yönetime sunumdan bir gün önce aylık raporda ciddi bir hesaplama hatası bulundu.",
            [
                ("Sunumu durdurmadan raporu düzeltip değişikliği yönetime bildirin.", "Otoriter", -5, 5, 10),
                ("İlgili ekiplerle hatanın kapsamını teyit edip revize rapor hazırlayın.", "Demokratik", 5, 0, 10),
                ("Ekiple tekrarını önleyecek kontrol noktası tasarlayın.", "Koçvari", 5, 5, 5),
                ("Hata fark edilmez diye eski raporu sunun.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Pazarlama departmanı bütçesini %40 aştı ve ek onay istiyor.",
            [
                ("Yeni harcamayı durdurup gerekçeli onay dosyası isteyin.", "Otoriter", -5, 5, 5),
                ("Pazarlamayla harcama getirisini inceleyip öncelikleri birlikte seçin.", "Demokratik", 5, 0, 10),
                ("Ekiplerle tasarruf ve aşamalı finansman seçenekleri geliştirin.", "Koçvari", 5, 5, 5),
                ("Talebi incelemeden bütçe farkını gelecek aya taşıyın.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "İç denetim öncesinde bazı harcama kayıtlarında belge eksikliği görüldü.",
            [
                ("Eksikleri kayıt altına alıp denetçiye şeffafça bildirin.", "Otoriter", -5, 0, 15),
                ("İlgili ekiplerle belgeleri mevzuata uygun biçimde tamamlayın.", "Demokratik", 5, 0, 10),
                ("Muhasebe ekibiyle belge kontrol listesini kalıcı olarak iyileştirin.", "Koçvari", 5, 5, 5),
                ("Denetçi sormazsa eksiklerden bahsetmeyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Tedarikçinin aynı faturayı iki kez gönderdiği fark edildi; ikinci ödeme henüz yapılmadı.",
            [
                ("İkinci ödemeyi bloke edip fatura kayıtlarını karşılaştırın.", "Otoriter", -5, 10, 10),
                ("Satın alma ve tedarikçiyle durumu birlikte doğrulayın.", "Demokratik", 5, 0, 10),
                ("Ekiple mükerrer fatura uyarı kontrolü oluşturun.", "Koçvari", 5, 5, 5),
                ("Yoğunluk azalınca bakmak üzere faturayı sırada bırakın.", "Kaçınmacı", -5, -5, -15),
            ],
        ),
        (
            "Yıl sonu kapanışında iki departmanın giderleri yanlış maliyet merkezine yazılmış.",
            [
                ("Kapanıştan önce kayıtları doğrulatıp düzeltme yapın.", "Otoriter", -5, 5, 10),
                ("Departmanlarla gider sahipliğini tek tek teyit edin.", "Demokratik", 5, 0, 10),
                ("Ekiple maliyet merkezi seçimi için yeni kontrol şablonu kurun.", "Koçvari", 5, 5, 5),
                ("Toplam şirket gideri aynı diye sınıflandırmayı değiştirmeyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Nakit akışı tahmininde büyük bir tahsilatın bir hafta gecikeceği öğrenildi.",
            [
                ("Ödeme önceliklerini ve yükümlülükleri hemen yeniden planlayın.", "Otoriter", -5, 5, 10),
                ("İlgili ekiplerle tahsilat takvimi ve alternatifleri görüşün.", "Demokratik", 5, 0, 10),
                ("Analiste farklı gecikme senaryoları hazırlatıp değerlendirin.", "Koçvari", 5, 5, 5),
                ("Nakit planını değiştirmeden tahsilatın geleceğini varsayın.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Bir çalışan, ödeme talimatındaki IBAN'ın tedarikçinin önceki kaydından farklı olduğunu fark etti.",
            [
                ("Ödemeyi durdurup doğrulanmış kanaldan hesap teyidi alın.", "Otoriter", -5, -5, 15),
                ("Satın alma ve finansla değişiklik kaynağını birlikte inceleyin.", "Demokratik", 5, 0, 10),
                ("Ekiple hesap değişikliği onayı için çift kontrol süreci kurun.", "Koçvari", 5, 5, 5),
                ("Tedarikçi e-postasına güvenip ödemeyi gönderin.", "Kaçınmacı", -5, 10, -15),
            ],
        ),
        (
            "Yeni mağaza yatırımı için beklenen satış tahmini iki farklı raporda uyuşmuyor.",
            [
                ("Yatırım onayını veri kaynağı netleşene kadar bekletin.", "Otoriter", -5, -5, 10),
                ("Finans ve mağazacılık ekipleriyle varsayımları karşılaştırın.", "Demokratik", 5, 0, 10),
                ("Analistlere ortak tahmin şablonu hazırlatıp test edin.", "Koçvari", 5, 5, 5),
                ("Daha yüksek satış gösteren raporu seçip ilerleyin.", "Kaçınmacı", -5, 10, -15),
            ],
        ),
        (
            "Bir departman gideri yanlış döneme kaydedildiği için aylık sonuç olduğundan iyi görünüyor.",
            [
                ("Dönemsellik hatasını düzelttirip raporu yeniden yayımlayın.", "Otoriter", -5, 0, 15),
                ("Muhasebe ve ilgili departmanla işlem tarihini teyit edin.", "Demokratik", 5, 0, 10),
                ("Ekiple kapanış kontrolüne dönem doğrulaması ekleyin.", "Koçvari", 5, 5, 5),
                ("Yıllık toplam değişmez diye aylık sonucu değiştirmeyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Üç mağazanın elektrik gideri öngörülenin üstünde; sebep henüz bilinmiyor.",
            [
                ("Mağaza bazında tüketim ve fatura kontrolü başlatın.", "Otoriter", -5, 5, 5),
                ("Mağazacılık ve tesis ekipleriyle olası nedenleri inceleyin.", "Demokratik", 5, 0, 10),
                ("Analistle tüketim uyarı eşiği ve takip raporu oluşturun.", "Koçvari", 5, 5, 5),
                ("Artışı mevsimsel sayıp hiçbir kontrol yapmayın.", "Kaçınmacı", -5, -5, -10),
            ],
        ),
        (
            "Bütçe toplantısında iki ekip aynı tasarruf tutarını kendi planına yazmış.",
            [
                ("Çifte sayılan tutarı çıkarıp bütçe tablolarını düzeltin.", "Otoriter", -5, 5, 10),
                ("İki ekiple tasarrufun sahipliğini ve hesabını netleştirin.", "Demokratik", 5, 0, 10),
                ("Ekipçe ortak tasarruf takip çizelgesi oluşturun.", "Koçvari", 5, 5, 5),
                ("Toplam hedef tutuyor diye çifte kaydı bırakın.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Denetim ekibi, masraf onaylarının bazılarının ödeme sonrasında verildiğini fark etti.",
            [
                ("İlgili işlemleri inceleyip yetki ihlallerini raporlayın.", "Otoriter", -5, 0, 15),
                ("Departman yöneticileriyle onay darboğazını birlikte analiz edin.", "Demokratik", 5, 0, 10),
                ("Ekiple ödeme öncesi otomatik onay kontrolü tasarlayın.", "Koçvari", 5, 5, 5),
                ("Geçmiş ödemeler kapanmış diye konuyu kayda almayın.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
    ],

    "Bilgi Teknolojileri": [
        (
            "Sistem güncellemesinden sonra bazı mağaza kasaları işlem yapamaz hâle geldi.",
            [
                ("Güncellemeyi geri alıp önce kasa hizmetini ayağa kaldırın.", "Otoriter", -5, 10, 5),
                ("Mağazalar ve teknik ekiple etki alanını netleştirip plan paylaşın.", "Demokratik", 5, 0, 10),
                ("Ekibi hata çözümü ve iletişim işlerine ayırıp süreci yönetin.", "Koçvari", 5, 5, 5),
                ("Sorunun kendiliğinden düzelmesini bekleyin.", "Kaçınmacı", -10, -15, -15),
            ],
        ),
        (
            "Kıdemli bir çalışan otomasyon projesinin görevini ortadan kaldıracağından endişe ediyor.",
            [
                ("Proje kararını netleştirip görev geçiş takvimi açıklayın.", "Otoriter", -5, 10, 0),
                ("Çalışanın kaygılarını dinleyip yeni rol seçeneklerini konuşun.", "Demokratik", 5, 0, 10),
                ("Çalışan için beceri geliştirme ve pilot görev planı oluşturun.", "Koçvari", 10, 5, 5),
                ("Endişeyi konuşmadan projeyi yürütmeye devam edin.", "Kaçınmacı", -10, -5, -10),
            ],
        ),
        (
            "Gece yarısı müşteri verilerini etkileyebilecek bir güvenlik açığı bildirildi.",
            [
                ("Olay müdahale planını başlatıp gerekli erişimleri sınırlayın.", "Otoriter", -5, -5, 15),
                ("Güvenlik ve ilgili ekiplerle etki alanını teyit edip iletişim kurun.", "Demokratik", 5, 0, 10),
                ("Ekibi inceleme ve kayıt görevlerine ayırıp koordineli çalıştırın.", "Koçvari", 5, 5, 10),
                ("Sabah mesai başlayana kadar olayı bildirmeyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Yeni uygulama sürümünde stok ekranı geç açılıyor; mağazalar işlerini kâğıtla takip etmeye başladı.",
            [
                ("Sürümü geri alma ölçütünü uygulayıp sorunu önceliklendirin.", "Otoriter", -5, 5, 10),
                ("Mağazalardan etki örnekleri toplayıp teknik ekiple öncelik belirleyin.", "Demokratik", 5, 0, 10),
                ("Geliştiricilerle performans ölçümü ve test adımı oluşturun.", "Koçvari", 5, 5, 5),
                ("Yavaşlığı normal sayıp sonraki sürümü bekleyin.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Teslime üç gün kala yazılım ekibi kritik bir entegrasyon testinin hiç yapılmadığını fark etti.",
            [
                ("Teslim kararını durdurup kritik testi hemen planlayın.", "Otoriter", -5, -5, 15),
                ("İş birimiyle riskleri paylaşarak gerçekçi teslim kapsamını seçin.", "Demokratik", 5, 0, 10),
                ("Ekibe risk temelli test listesi hazırlatıp süreci iyileştirin.", "Koçvari", 5, 5, 5),
                ("Test yapılmadığını belirtmeden sürümü yayımlayın.", "Kaçınmacı", -5, 10, -15),
            ],
        ),
        (
            "Destek talepleri aynı hata için artıyor ama ekip her talebi ayrı ayrı çözüyor.",
            [
                ("Ortak hata kaydı açıp tek çözüm ve sorumlu belirleyin.", "Otoriter", -5, 10, 5),
                ("Destek ve geliştirme ekipleriyle kalıcı çözüm önceliği belirleyin.", "Demokratik", 5, 0, 10),
                ("Destek ekibine tekrar eden sorun analizi yaptırın.", "Koçvari", 5, 5, 5),
                ("Talepleri kapatmaya devam edip ortak nedeni araştırmayın.", "Kaçınmacı", -5, -10, -10),
            ],
        ),
        (
            "Bir çalışanın yönetici yetkisi görev değişikliğinden sonra hâlâ aktif görünüyor.",
            [
                ("Yetkiyi doğrulayıp gereksiz erişimi hemen kaldırın.", "Otoriter", -5, 0, 15),
                ("İK ve sistem sahipleriyle rol değişikliği kayıtlarını kontrol edin.", "Demokratik", 5, 0, 10),
                ("Ekiple otomatik erişim gözden geçirme süreci oluşturun.", "Koçvari", 5, 5, 5),
                ("Çalışan kullanmıyor diye yetkiyi olduğu gibi bırakın.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "İki kıdemli geliştirici mimari seçiminde anlaşamıyor; ekip karar beklerken işler gecikiyor.",
            [
                ("Ölçütleri belirleyip belirli tarihte teknik kararı verin.", "Otoriter", -5, 10, 0),
                ("İki yaklaşımı aynı performans ölçütleriyle karşılaştırın.", "Demokratik", 5, 0, 10),
                ("Kısa prototip için ekibi görevlendirip öğrenimleri değerlendirin.", "Koçvari", 10, 5, 5),
                ("Anlaşmalarını bekleyip karar tarihini belirlemeyin.", "Kaçınmacı", -5, -10, -10),
            ],
        ),
        (
            "Yedekleme raporu başarılı görünüyor ancak son geri yükleme testi başarısız oldu.",
            [
                ("Yedeklerin kullanılabilirliğini doğrulayana dek acil inceleme başlatın.", "Otoriter", -5, -5, 15),
                ("Sistem ve iş sürekliliği ekipleriyle risk ve geçici planı paylaşın.", "Demokratik", 5, 0, 10),
                ("Ekibe düzenli geri yükleme testi takvimi oluşturtun.", "Koçvari", 5, 5, 5),
                ("Rapor başarılı diye başarısız testi görmezden gelin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Mağaza ağındaki kesinti yalnızca belirli şehirlerde görülüyor; sebep henüz net değil.",
            [
                ("Etkilenen mağazalar için acil destek ve yedek bağlantı planı uygulayın.", "Otoriter", -5, 10, 5),
                ("Operatör ve saha ekipleriyle kesinti kapsamını birlikte haritalayın.", "Demokratik", 5, 0, 10),
                ("Ekibe bölgesel izleme ve uyarı düzeni kurma görevi verin.", "Koçvari", 5, 5, 5),
                ("Tüm şehirler etkilenmediği için müdahaleyi erteleyin.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Yeni yazılımı kullanacak mağaza ekibi eğitim tarihinden önce sisteme erişim aldı ve yanlış işlem yaptı.",
            [
                ("Gerekli erişimleri sınırlayıp hatalı kayıtları doğrulayın.", "Otoriter", -5, -5, 10),
                ("Mağaza ve eğitim ekipleriyle geçiş takvimini yeniden planlayın.", "Demokratik", 5, 0, 10),
                ("Ekiple eğitim tamamlanmadan erişim verilmesini önleyen kontrol kurun.", "Koçvari", 5, 5, 5),
                ("İşlemler az diye hatalı kayıtları incelemeyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Yazılım tedarikçisi bakım penceresini kampanya gecesine almak istiyor.",
            [
                ("Çakışan bakımı reddedip farklı zaman talep edin.", "Otoriter", -5, 5, 10),
                ("E-ticaret ve mağaza ekipleriyle etkiyi değerlendirip tarih seçin.", "Demokratik", 5, 0, 10),
                ("Ekibe kesintisiz geçiş ve geri dönüş planı hazırlatın.", "Koçvari", 5, 5, 5),
                ("Bakımın etkisini öğrenmeden önerilen saati kabul edin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
    ],

    "E-Ticaret": [
        (
            "İndirim gününde site trafiği beklenenin beş katına çıktı; siparişler yavaşlıyor.",
            [
                ("Onaylı kapasite artırma planını hemen devreye alın.", "Otoriter", -5, 10, 5),
                ("Teknik ve müşteri ekipleriyle kritik sayfalara öncelik verin.", "Demokratik", 5, 0, 10),
                ("Ekibi izleme, düzeltme ve bilgilendirme işlerine ayırın.", "Koçvari", 5, 5, 5),
                ("Trafik azalır diye müşterilere bilgi vermeden bekleyin.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Stok eşitleme hatası nedeniyle tükenmiş ürünler sitede satılmaya devam ediyor.",
            [
                ("Ürün satışını durdurup etkilenen siparişleri belirleyin.", "Otoriter", -5, 0, 10),
                ("Müşterilere alternatif ürün veya iade seçeneklerini açıkça sunun.", "Demokratik", 5, -5, 15),
                ("IT ve stok ekipleriyle eşitleme kontrolünü yeniden tasarlayın.", "Koçvari", 5, 5, 5),
                ("Şikâyetler gelene kadar ürünü satışta tutun.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Kargo firması art arda üçüncü kez gecikti; müşteri talepleri hızla artıyor.",
            [
                ("Sözleşmedeki hizmet düzeyini uygulayıp alternatif taşıyıcı açın.", "Otoriter", -5, 10, 5),
                ("Kargo firmasıyla iyileştirme takvimi ve müşteri bilgilendirmesi hazırlayın.", "Demokratik", 5, 0, 10),
                ("Ekibe taşıyıcı performansı için haftalık izleme sistemi kurdurun.", "Koçvari", 5, 5, 5),
                ("Gecikmeleri müşteriler sorana kadar duyurmayın.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "İade sayfasındaki teknik hata, müşterilerin iade kodu oluşturmasını engelliyor.",
            [
                ("Hata çözülene kadar onaylı alternatif iade kanalını açın.", "Otoriter", -5, 10, 5),
                ("Müşteri hizmetleri ve teknik ekiple açık bilgilendirme yapın.", "Demokratik", 5, 0, 10),
                ("Ekibe iade akışı için düzenli uçtan uca test planlatın.", "Koçvari", 5, 5, 5),
                ("Sorun çözülene kadar iade taleplerini yanıtsız bırakın.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Ürün sayfasında montun beden tablosu yanlış; aynı nedenle çok sayıda iade oluştu.",
            [
                ("Beden tablosunu kaldırıp doğru ölçü gelene kadar uyarı koyun.", "Otoriter", -5, 0, 10),
                ("Ürün ve müşteri ekipleriyle doğru ölçüleri teyit edip yayımlayın.", "Demokratik", 5, 0, 10),
                ("İçerik ekibiyle beden bilgisi için çift kontrol adımı kurun.", "Koçvari", 5, 5, 5),
                ("İadeleri normal sayıp beden tablosunu değiştirmeyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Ödeme ekranında bazı bankaların kartlarıyla işlem başarısız oluyor; kampanya devam ediyor.",
            [
                ("Etkilenen ödeme yöntemini izole edip sağlayıcıya acil bildirin.", "Otoriter", -5, 5, 10),
                ("Müşteri ve teknik ekiplerle kullanılabilir ödeme seçeneklerini duyurun.", "Demokratik", 5, 0, 10),
                ("Ekiple banka bazlı işlem izleme paneli oluşturun.", "Koçvari", 5, 5, 5),
                ("Müşterilerin farklı kart denemesini bekleyip açıklama yapmayın.", "Kaçınmacı", -5, -10, -15),
            ],
        ),
        (
            "Yeni sitede filtreleme kadın ve çocuk ürünlerini karıştırıyor; dönüşüm oranı düşüyor.",
            [
                ("Hatalı filtreyi geçici kapatıp kategori gezinmesini açık tutun.", "Otoriter", -5, 5, 5),
                ("Ürün ve teknik ekiple örnek hataları inceleyip öncelik belirleyin.", "Demokratik", 5, 0, 10),
                ("Ekibe kategori testi ve kontrol listesi hazırlatın.", "Koçvari", 5, 5, 5),
                ("Raporlar netleşene kadar filtreyi aynı şekilde bırakın.", "Kaçınmacı", -5, -10, -10),
            ],
        ),
        (
            "Sosyal medyada bir müşteri, yanlış ürün teslim edildiğini anlatan gönderisiyle yoğun etkileşim aldı.",
            [
                ("Siparişi doğrulatıp müşteriye resmî çözüm kanalı üzerinden ulaşın.", "Otoriter", -5, 5, 10),
                ("Müşterinin izniyle çözüm sürecini şeffaf biçimde takip edin.", "Demokratik", 5, 0, 10),
                ("Depo ve müşteri ekipleriyle yanlış ürünün kök nedenini araştırın.", "Koçvari", 5, 5, 5),
                ("Paylaşım unutulur diye müşteriye dönüş yapmayın.", "Kaçınmacı", -5, -5, -15),
            ],
        ),
        (
            "İndirim kodu, koşulları karşılamayan sepetlerde de çalışıyor; sipariş sayısı artıyor.",
            [
                ("Kodun hatalı kullanımını durdurup etkilenen siparişleri inceleyin.", "Otoriter", -5, 0, 10),
                ("Finans ve müşteri ekipleriyle adil çözüm seçeneklerini belirleyin.", "Demokratik", 5, 0, 10),
                ("Ekibe kampanya kuralı için yayın öncesi test süreci kurdurun.", "Koçvari", 5, 5, 5),
                ("Satışlar artıyor diye hatayı kampanya bitene kadar bırakın.", "Kaçınmacı", -5, 10, -15),
            ],
        ),
        (
            "Depodan çıkan siparişlerin takip numarası müşterilere iki gün gecikmeyle iletiliyor.",
            [
                ("Bildirim akışını kontrol edip geciken numaraları topluca gönderin.", "Otoriter", -5, 5, 5),
                ("Kargo ve müşteri ekipleriyle doğru teslim bilgisini paylaşın.", "Demokratik", 5, 0, 10),
                ("Ekibe bildirim gecikmesi için otomatik uyarı kurdurun.", "Koçvari", 5, 5, 5),
                ("Kargolar yolda diye bildirim gecikmesini önemsemeyin.", "Kaçınmacı", -5, -5, -10),
            ],
        ),
        (
            "Ürün yorumlarında aynı ürün için tekrarlayan dikiş sorunu bildiriliyor.",
            [
                ("Yeni sevkiyatın satışını kontrol için geçici durdurun.", "Otoriter", -5, -5, 10),
                ("Kalite ve müşteri ekipleriyle şikâyetleri örnekleyip çözüm belirleyin.", "Demokratik", 5, 0, 10),
                ("Ekibe yorumlardan kalite uyarısı çıkaran süreç hazırlatın.", "Koçvari", 5, 5, 5),
                ("Yorumları kişisel görüş sayıp inceleme açmayın.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
        (
            "Mobil uygulamadaki kampanya afişi, tıklanınca kampanyaya dâhil olmayan ürünleri gösteriyor.",
            [
                ("Yanlış yönlendirmeyi durdurup doğru kampanya sayfasını bağlayın.", "Otoriter", -5, 5, 10),
                ("Pazarlama ve ürün ekipleriyle kapsamı müşterilere açıkça anlatın.", "Demokratik", 5, 0, 10),
                ("Ekibe kampanya bağlantıları için yayın öncesi kontrol yaptırın.", "Koçvari", 5, 5, 5),
                ("Afiş yayında kalsın diye yanlış bağlantıyı değiştirmeyin.", "Kaçınmacı", -5, 5, -15),
            ],
        ),
    ],
}


def vakalari_hazirla(ham_vakalar):
    hazir = {}

    for departman, kayitlar in ham_vakalar.items():
        hazir[departman] = []

        for sira, (olay, ham_secenekler) in enumerate(kayitlar, start=1):
            secenekler = []

            for metin, tip, moral, verimlilik, guven in ham_secenekler:
                secenekler.append(
                    {
                        "metin": metin,
                        "tip": tip,
                        "etki": {
                            "Moral": moral,
                            "Verimlilik": verimlilik,
                            "Güven": guven,
                        },
                    }
                )

            hazir[departman].append(
                {
                    "id": f"{departman}-{sira}",
                    "olay": olay,
                    "secenekler": secenekler,
                }
            )

    return hazir


VAKALAR = vakalari_hazirla(HAM_VAKALAR)


# ==========================================================
# OTURUM HAFIZASI
# ==========================================================

def yeni_oyun_durumu():
    return {
        "started": False,
        "user_name": "",
        "user_department": "",
        "stats": {
            "Moral": 60,
            "Verimlilik": 60,
            "Güven": 60,
        },
        "tur": 1,
        "current_scenario": None,
        "secim_gecmisi": [],
        "karar_gecmisi": [],
        "havuz_kullanilan": [],
        "karakter_havuzu": [],
        "vaka_sirasi": [],
    }


for anahtar, varsayilan_deger in yeni_oyun_durumu().items():
    if anahtar not in st.session_state:
        st.session_state[anahtar] = varsayilan_deger


def oyunu_sifirla():
    for anahtar, deger in yeni_oyun_durumu().items():
        st.session_state[anahtar] = deger
    st.rerun()


# ==========================================================
# KARAKTERLER VE HAZIR VAKA SEÇİMİ
# ==========================================================

def karakter_sec_veya_uret(departman):
    karakterler = st.session_state.karakter_havuzu

    if karakterler and (len(karakterler) >= 4 or random.random() < 0.65):
        return random.choice(karakterler)

    kullanilan_isimler = {karakter["isim"] for karakter in karakterler}
    musait_isimler = [
        isim for isim in ISIM_HAVUZU if isim not in kullanilan_isimler
    ]

    if not musait_isimler:
        return random.choice(karakterler)

    yeni_karakter = {
        "isim": random.choice(musait_isimler),
        "rol": random.choice(DEPARTMANLAR[departman]["karakterler"]),
        "kisilik": random.choice(KISILIK_OZELLIKLERI),
        "iliski": 50,
        "gecmis": [],
    }

    karakterler.append(yeni_karakter)
    return yeni_karakter


def karakter_guncelle(isim, secilen_metin, etki):
    if not isim:
        return

    for karakter in st.session_state.karakter_havuzu:
        if karakter["isim"] == isim:
            karakter["iliski"] = max(
                0,
                min(100, karakter["iliski"] + etki.get("Güven", 0)),
            )

            karakter["gecmis"].append(
                f"'{secilen_metin[:60]}' yaklaşımıyla karşılaştı"
            )
            karakter["gecmis"] = karakter["gecmis"][-3:]
            break


def vaka_sirasini_hazirla(departman):
    """
    Oyun başında o departmanın vakaları bir kez karıştırılır.
    İlk 10 farklı vaka oynatılır; aynı oyun içinde tekrar olmaz.
    """
    vaka_idleri = [vaka["id"] for vaka in VAKALAR[departman]]
    random.shuffle(vaka_idleri)
    st.session_state.vaka_sirasi = vaka_idleri[:TOPLAM_VAKA]


def yeni_vaka_getir():
    departman = st.session_state.user_department
    sira = st.session_state.tur - 1

    vaka_id = st.session_state.vaka_sirasi[sira]
    orijinal = next(
        vaka for vaka in VAKALAR[departman]
        if vaka["id"] == vaka_id
    )

    secenekler = [
        {
            "metin": secenek["metin"],
            "tip": secenek["tip"],
            "etki": dict(secenek["etki"]),
        }
        for secenek in orijinal["secenekler"]
    ]
    random.shuffle(secenekler)

    karakter = karakter_sec_veya_uret(departman)

    onceki_karar = (
        st.session_state.karar_gecmisi[-1]
        if st.session_state.karar_gecmisi
        else None
    )

    if onceki_karar:
        onceki_metin = onceki_karar["metin"].rstrip(".")
        baglanti = (
            f"Bir önceki vakada '{onceki_metin}' kararını verdiniz. "
            "Şimdi departmanınızda farklı bir durumla karşılaşıyorsunuz: "
        )
    else:
        baglanti = ""

    st.session_state.havuz_kullanilan.append(vaka_id)

    return {
        "id": vaka_id,
        "olay": baglanti + orijinal["olay"],
        "secenekler": secenekler,
        "aktif_karakter": karakter["isim"],
        "karakter_rol": karakter["rol"],
    }


# ==========================================================
# RAPOR VE ARAYÜZ YARDIMCILARI
# ==========================================================

def renk_belirle(deger):
    if deger >= 70:
        return "#16a34a"
    if deger >= 40:
        return "#f59e0b"
    return "#dc2626"


def stat_karti_ciz(label, deger, icon):
    renk = renk_belirle(deger)

    kart = (
        f'<div class="stat-card" style="border-left-color:{renk};">'
        f'<div class="stat-label">{icon} {html.escape(label)}</div>'
        f'<div class="stat-value">%{deger}</div>'
        '<div class="progress-outer">'
        f'<div class="progress-inner" style="width:{deger}%;'
        f' background:{renk};"></div>'
        '</div></div>'
    )

    st.markdown(kart, unsafe_allow_html=True)


def karar_karti_ciz(kayit):
    tip = kayit["tip"]
    renk = TIP_RENK.get(tip, "#9ca3af")

    metin_kisa = kayit["metin"][:65]
    if len(kayit["metin"]) > 65:
        metin_kisa += "..."

    stat_satirlari = ""

    for metrik, etki in kayit["etki"].items():
        if etki > 0:
            stil = "stat-up"
            gosterim = f"▲ +{etki}"
        elif etki < 0:
            stil = "stat-down"
            gosterim = f"▼ {etki}"
        else:
            stil = "stat-same"
            gosterim = "→ 0"

        stat_satirlari += (
            '<div class="history-stat-row">'
            f'<span>{html.escape(metrik)}</span>'
            f'<span class="{stil}">{gosterim}</span>'
            '</div>'
        )

    karakter_html = ""

    if kayit.get("karakter"):
        karakter_html = (
            '<div style="font-size:0.75em;color:#047857;'
            'margin-bottom:4px;">'
            f'👤 {html.escape(kayit["karakter"])}'
            '</div>'
        )

    kart = (
        f'<div class="history-card" style="border-left-color:{renk};">'
        f'<div class="history-tur">Vaka {kayit["tur"]}</div>'
        f'<div class="history-tip" style="background:{renk};">'
        f'{html.escape(tip)}</div>'
        f'{karakter_html}'
        f'<div class="history-metin">"{html.escape(metin_kisa)}"</div>'
        f'{stat_satirlari}'
        '</div>'
    )

    st.markdown(kart, unsafe_allow_html=True)


def final_rapor_uret(stats, secim_gecmisi):
    ortalama = sum(stats.values()) / 3
    tip_sayaci = Counter(secim_gecmisi)

    baskin_tip = (
        tip_sayaci.most_common(1)[0][0]
        if tip_sayaci
        else "Belirsiz"
    )

    tip_aciklamalari = {
        "Demokratik": (
            "Kararlarınızda farklı görüşleri dinlemeyi ve katılımcı bir "
            "yaklaşımı öne çıkardınız. Bu, güven oluşturabilir; ancak acil "
            "durumlarda karar hızını da gözetmeniz gerekir."
        ),
        "Otoriter": (
            "Hızlı ve net kararlar almaya yöneldiniz. Bu yaklaşım kriz anında "
            "yararlı olabilir; sürekli kullanıldığında ekip katılımını azaltabilir."
        ),
        "Koçvari": (
            "Çalışanların gelişimine ve birlikte çözüm üretmeye ağırlık verdiniz. "
            "Bu yaklaşımın yanında gerektiğinde net öncelikler koymak da önemlidir."
        ),
        "Kaçınmacı": (
            "Bazı zor kararları ertelemeye yöneldiniz. Belirsizlik uzadığında "
            "ekibin güveni ve iş akışı bundan olumsuz etkilenebilir."
        ),
        "Belirsiz": "Henüz yeterli karar verilmedi.",
    }

    metrik_yorumlari = {}

    for metrik, deger in stats.items():
        if deger >= 75:
            seviye = "Güçlü"
        elif deger >= 50:
            seviye = "Orta"
        else:
            seviye = "Geliştirilebilir"

        aciklamalar = {
            "Moral": {
                "Güçlü": "Ekibin motivasyonunu koruyan kararlar aldınız.",
                "Orta": "Ekip morali dengede; yoğun dönemlerde yakından takip edilmeli.",
                "Geliştirilebilir": "Ekibin iş yükü ve motivasyonuna daha fazla odaklanabilirsiniz.",
            },
            "Verimlilik": {
                "Güçlü": "Operasyonel akışı destekleyen kararlar aldınız.",
                "Orta": "İş akışı sürüyor; bazı süreçler iyileştirilebilir.",
                "Geliştirilebilir": "Gecikme ve darboğazlara daha erken müdahale edebilirsiniz.",
            },
            "Güven": {
                "Güçlü": "Şeffaflık ve tutarlılık yönünden güçlü bir sonuç elde ettiniz.",
                "Orta": "Güven dengede; kararların gerekçesini paylaşmak yararlı olabilir.",
                "Geliştirilebilir": "Daha açık iletişim ve tutarlı uygulamalar güveni artırabilir.",
            },
        }

        metrik_yorumlari[metrik] = (
            f"{metrik} (%{deger} — {seviye}): "
            f"{aciklamalar[metrik][seviye]}"
        )

    return (
        ortalama,
        baskin_tip,
        tip_aciklamalari[baskin_tip],
        metrik_yorumlari,
        tip_sayaci,
    )


def secenekleri_ciz(current):
    secenekler = current["secenekler"]

    # Her vaka dört seçenek içerir: iki satır, iki sütun.
    for baslangic in (0, 2):
        sutunlar = st.columns(2, gap="medium")

        for sutun_numarasi, secenek in enumerate(
            secenekler[baslangic:baslangic + 2]
        ):
            secenek_numarasi = baslangic + sutun_numarasi

            with sutunlar[sutun_numarasi]:
                tiklandi = st.button(
                    secenek["metin"],
                    key=f"v_{st.session_state.tur}_{secenek_numarasi}",
                    use_container_width=True,
                )

                if tiklandi:
                    for metrik, etki in secenek["etki"].items():
                        st.session_state.stats[metrik] = max(
                            0,
                            min(
                                100,
                                st.session_state.stats[metrik] + etki,
                            ),
                        )

                    st.session_state.secim_gecmisi.append(
                        secenek["tip"]
                    )

                    aktif_karakter = current.get("aktif_karakter")

                    karakter_guncelle(
                        aktif_karakter,
                        secenek["metin"],
                        secenek["etki"],
                    )

                    st.session_state.karar_gecmisi.append(
                        {
                            "tur": st.session_state.tur,
                            "metin": secenek["metin"],
                            "tip": secenek["tip"],
                            "etki": dict(secenek["etki"]),
                            "karakter": aktif_karakter,
                        }
                    )

                    st.session_state.tur += 1
                    st.session_state.current_scenario = None
                    st.rerun()


# ==========================================================
# SOL MENÜ
# ==========================================================

with st.sidebar:
    st.header("🎮 Oyun Durumu")
    st.success("Hazır senaryo modu — API ve faturalandırma gerekmez.")

    if st.session_state.user_department:
        departman = st.session_state.user_department

        st.write(f"🏢 Departman: **{departman}**")
        st.write(
            f"📚 Bu departmandaki hazır vaka: "
            f"**{len(VAKALAR[departman])}**"
        )
        st.write(
            f"✅ Bu oyunda tamamlanan vaka: "
            f"**{len(st.session_state.karar_gecmisi)} / {TOPLAM_VAKA}**"
        )

    if st.session_state.karakter_havuzu:
        st.write("---")
        st.write("**👥 Tanıştığınız Karakterler**")

        for karakter in st.session_state.karakter_havuzu:
            kart = (
                '<div class="karakter-kart">'
                f'<b>{html.escape(karakter["isim"])}</b> — '
                f'{html.escape(karakter["rol"])}<br>'
                '<span style="color:#6b7280;">'
                f'{html.escape(karakter["kisilik"])}'
                '</span><br>'
                f'İlişki: %{karakter["iliski"]}'
                '</div>'
            )

            st.markdown(kart, unsafe_allow_html=True)

    st.write("---")

    if st.button("🔄 Oyunu Sıfırla"):
        oyunu_sifirla()


# ==========================================================
# KARŞILAMA EKRANI
# ==========================================================

if not st.session_state.started:
    st.markdown(
        """
        <div class="hero-banner">
            <h1>💙 LC Waikiki Liderlik Simülasyonu</h1>
            <p>Gerçekçi yönetim vakalarıyla liderlik kararlarınızı deneyin.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sol, sag = st.columns([1.2, 1])

    with sol:
        st.subheader("Nasıl Oynanır? 🎯")

        st.markdown(
            """
            - Departmanınızı seçin; vakalar seçtiğiniz departmana özel gelsin.
            - Her oyunda **10 farklı vaka** çözün.
            - **Her vakada 4 karar seçeneği** bulunur.
            - Aynı oyun içinde bir vaka **tekrar etmez**.
            - Seçimleriniz Moral, Verimlilik ve Güven değerlerini değiştirir.
            - Oyun sonunda kişisel **Liderlik Karnesi** oluşturulur.

            **Bu sürüm hazır senaryo kullanır:** API anahtarı,
            Vertex AI veya faturalandırma gerekmez.

            ⚠️ *Her yaklaşımın farklı avantajları ve bedelleri olabilir.*
            """
        )

    with sag:
        st.subheader("📝 Katılımcı Bilgileri")

        with st.form("giris_formu"):
            ad_soyad = st.text_input(
                "Ad Soyad *",
                placeholder="Örn: Deniz Demirkaynak",
            )

            departman_secenekleri = ["-- Seçiniz --"] + [
                f"{bilgi['icon']} {ad}"
                for ad, bilgi in DEPARTMANLAR.items()
            ]

            secilen = st.selectbox(
                "Departman *",
                departman_secenekleri,
            )

            gonder = st.form_submit_button(
                "🚀 Simülasyonu Başlat"
            )

            if gonder:
                if not ad_soyad.strip():
                    st.warning(
                        "Lütfen adınızı ve soyadınızı girin."
                    )
                elif secilen == "-- Seçiniz --":
                    st.warning(
                        "Lütfen bir departman seçin."
                    )
                else:
                    departman = secilen.split(" ", 1)[1]

                    st.session_state.user_name = ad_soyad.strip()
                    st.session_state.user_department = departman
                    st.session_state.started = True

                    vaka_sirasini_hazirla(departman)
                    st.rerun()

    st.stop()


# ==========================================================
# OYUN EKRANI
# ==========================================================

departman = st.session_state.user_department
departman_ikonu = DEPARTMANLAR[departman]["icon"]

ust_bilgi = (
    f"👤 {html.escape(st.session_state.user_name)}"
    f" &nbsp;•&nbsp; "
    f"{departman_ikonu} {html.escape(departman)}"
)

st.markdown(
    '<div class="hero-banner">'
    '<h1>💙 LC Waikiki Liderlik Simülasyonu</h1>'
    f'<p>{ust_bilgi}</p>'
    '</div>',
    unsafe_allow_html=True,
)

ana_alan, yan_alan = st.columns([2.6, 1], gap="large")

with ana_alan:
    moral_sutunu, verim_sutunu, guven_sutunu = st.columns(3)

    with moral_sutunu:
        stat_karti_ciz(
            "Moral",
            st.session_state.stats["Moral"],
            "😊",
        )

    with verim_sutunu:
        stat_karti_ciz(
            "Verimlilik",
            st.session_state.stats["Verimlilik"],
            "📈",
        )

    with guven_sutunu:
        stat_karti_ciz(
            "Güven",
            st.session_state.stats["Güven"],
            "🤝",
        )

    st.write("")

    if st.session_state.tur <= TOPLAM_VAKA:
        if st.session_state.current_scenario is None:
            st.session_state.current_scenario = yeni_vaka_getir()

        current = st.session_state.current_scenario

        rozetler = (
            f'<div class="vaka-badge">'
            f'VAKA {st.session_state.tur} / {TOPLAM_VAKA}'
            '</div> '
            f'<div class="dept-badge">'
            f'{departman_ikonu} {html.escape(departman)}'
            '</div>'
        )

        if current.get("aktif_karakter"):
            rozetler += (
                ' <div class="karakter-badge">'
                f'👤 {html.escape(current["aktif_karakter"])}'
                ' — '
                f'{html.escape(current["karakter_rol"])}'
                '</div>'
            )

        st.markdown(rozetler, unsafe_allow_html=True)

        st.markdown(
            '<div class="olay-box">'
            f'{html.escape(current["olay"])}'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown("##### Liderlik Yaklaşımınız:")
        secenekleri_ciz(current)

    else:
        st.success(
            f"🏁 Tebrikler {st.session_state.user_name}, "
            f"{TOPLAM_VAKA} vakalık simülasyonu tamamladınız!"
        )

        (
            ortalama,
            baskin_tip,
            tip_metni,
            metrik_yorumlari,
            tip_sayaci,
        ) = final_rapor_uret(
            st.session_state.stats,
            st.session_state.secim_gecmisi,
        )

        final_kart = (
            '<div class="rapor-kart" style="text-align:center;">'
            '<div class="stat-label">FİNAL LİDERLİK ENDEKSİ</div>'
            '<div style="font-size:3em;font-weight:800;'
            f'color:{renk_belirle(int(ortalama))};">'
            f'%{int(ortalama)}'
            '</div>'
            '<div style="color:#6b7280;">'
            'Bu skor Moral, Verimlilik ve Güven ortalamasıdır.'
            '</div>'
            '</div>'
        )

        st.markdown(final_kart, unsafe_allow_html=True)

        st.write("### 📊 Metrik Bazlı Analiz")

        for yorum in metrik_yorumlari.values():
            st.markdown(
                '<div class="rapor-kart">'
                f'{html.escape(yorum)}'
                '</div>',
                unsafe_allow_html=True,
            )

        st.write("### 🧭 Baskın Liderlik Tarzınız")

        baskin_kart = (
            '<div class="rapor-kart">'
            f'<b>{html.escape(baskin_tip)}</b> '
            f'({tip_sayaci.get(baskin_tip, 0)}/{TOPLAM_VAKA} karar)'
            '<br><br>'
            f'{html.escape(tip_metni)}'
            '</div>'
        )

        st.markdown(baskin_kart, unsafe_allow_html=True)

        st.write("### 📈 Kararlarınızın Dağılımı")

        for tip in TIP_RENK:
            sayi = tip_sayaci.get(tip, 0)
            st.write(f"**{tip}** — {sayi} kez")
            st.progress(sayi / TOPLAM_VAKA)

        st.write("---")

        if ortalama > 75:
            genel_yorum = (
                "💎 Dengeleri güçlü biçimde koruyan kararlar aldınız."
            )
        elif ortalama > 50:
            genel_yorum = (
                "📈 Güçlü yönleriniz var; bazı kararların ekip ve süreç "
                "üzerindeki etkilerini daha fazla dengeleyebilirsiniz."
            )
        else:
            genel_yorum = (
                "⚠️ Kararlarınızın uzun vadeli etkilerini daha dikkatli "
                "değerlendirebilirsiniz."
            )

        st.markdown(
            '<div class="rapor-kart">'
            f'<b>Genel Değerlendirme:</b> {html.escape(genel_yorum)}'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button("Simülasyonu Baştan Başlat"):
            oyunu_sifirla()


with yan_alan:
    st.markdown(
        '<div class="journey-header">'
        '📜 Karar Yolculuğunuz'
        '</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.karar_gecmisi:
        st.markdown(
            '<div class="empty-journey">'
            'Henüz bir karar vermediniz.<br>'
            'İlk kararınız burada görünecek.'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        for kayit in st.session_state.karar_gecmisi:
            karar_karti_ciz(kayit)
