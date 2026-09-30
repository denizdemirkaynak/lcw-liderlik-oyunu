import html
import random
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

    .devam-badge {
        display: inline-block;
        background: #f3e8ff;
        color: #7e22ce;
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
        line-height: 1.65;
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

    .history-sonuc {
        color: #374151;
        background: #f3f6fb;
        padding: 8px 10px;
        border-radius: 8px;
        font-size: 0.82em;
        line-height: 1.45;
        margin: 7px 0;
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
    "Mağazacılık": "🏬",
    "Tedarik Zinciri": "🚚",
    "Satın Alma": "🛒",
    "İnsan Kaynakları": "👥",
    "Pazarlama": "📣",
    "Finans": "💰",
    "Bilgi Teknolojileri": "💻",
    "E-Ticaret": "🌐",
}

TIP_RENK = {
    "Demokratik": "#2563eb",
    "Otoriter": "#dc2626",
    "Koçvari": "#16a34a",
    "Kaçınmacı": "#6b7280",
}


# ==========================================================
# VERİ YARDIMCILARI
# ==========================================================
#
# Her seçenek:
# (metin, liderlik_tipi, moral, verimlilik, güven, somut_sonuç)
#
# Her vaka:
# (id, olay, kişi_adı, kişi_rolü, dört_seçenek)
#
# "Kaçınmacı" etiketi yalnızca gerçekten erteleme/kaçınma
# içeren seçenekte kullanılır. Diğer etiketler karar verme
# yaklaşımını tanımlar; tek başlarına iyi/kötü puanı değildir.
# ==========================================================

def S(metin, tip, moral, verimlilik, guven, sonuc):
    return {
        "metin": metin,
        "tip": tip,
        "etki": {
            "Moral": moral,
            "Verimlilik": verimlilik,
            "Güven": guven,
        },
        "sonuc": sonuc,
    }


def V(kimlik, olay, kisi, rol, secenekler):
    return {
        "id": kimlik,
        "olay": olay,
        "kisi": kisi,
        "rol": rol,
        "secenekler": secenekler,
        "devam": False,
    }


# ==========================================================
# BAĞIMSIZ VAKA HAVUZU — HER DEPARTMANDA 20 VAKA
# ==========================================================

VAKALAR = {

    "Mağazacılık": [
        V("mag-01",
          "Cumartesi kampanyasında aynı ürünün raf etiketinde %30, kasada %20 indirim görünüyor. Kasiyer Ayşe Yıldız işlemleri durdurmayı öneriyor; kuyruk 19 kişiye ulaştı. Müşteri mağduriyetini giderirken onay sınırınızı ve kayıt düzenini nasıl korursunuz?",
          "Ayşe Yıldız", "kasiyer", [
              S("Etiket-kasa farkını belgeleyip yetkili geçici düzeltmeyi başlatın; sırayı ikinci kasaya aktarın.", "Otoriter", -3, 9, 7, "Kuyruk kısaldı; geçici düzeltmeler için gün sonunda ek kontrol gerekecek."),
              S("Ayşe ve reyon sorumlusuyla etkilenen ürünleri belirleyip müşterilere tek bir uygulama duyurun.", "Demokratik", 5, -3, 10, "Uygulama tutarlılaştı; ilk müşteriler çözüm beklerken kuyruk uzadı."),
              S("Ayşe'yi kasa akışını yönetmekle görevlendirip başka çalışana etiketleri doğrulatın.", "Koçvari", 6, 4, 5, "Ayşe sorumluluk aldı; hatalı etiketlerin tamamını bulmak zaman alacak."),
              S("Merkezden açıklama gelene kadar kasadaki itirazları tek tek ele alın.", "Kaçınmacı", -7, -8, -9, "İtirazlar tek tek çözüldü ama müşteriler arasında farklı uygulama algısı oluştu."),
          ]),
        V("mag-02",
          "Vardiya amiri Mehmet Kara, hasta olan iki çalışanın yerine ekibi fazla mesaiye çağırmak istiyor. Aynı gün deneme kabininde bekleme süresi 14 dakikaya çıktı; ekip geçen hafta da fazla mesai yaptı.",
          "Mehmet Kara", "vardiya amiri", [
              S("Kritik saatlere kısa vardiya takviyesi isteyin; görevleri geçici yeniden dağıtın.", "Otoriter", -3, 8, 5, "Bekleme azaldı; kısa süreli görev değişimi bazı reyonları zayıflattı."),
              S("Mehmet ve ekiple gönüllülük ve müsaitlik durumunu konuşup vardiyayı yeniden kurun.", "Demokratik", 7, -3, 8, "Ekip planı sahiplendi; çözümün netleşmesi zaman aldı."),
              S("Mehmet'e kabin ve kasa yoğunluğunu ölçtürüp sonraki hafta için yedek plan hazırlatın.", "Koçvari", 5, 3, 5, "Mehmet planlama sorumluluğu aldı; bugünkü sıkışıklık kısmen sürdü."),
              S("Günün kalanında mevcut vardiyayla devam edip yoğunluğun düşmesini bekleyin.", "Kaçınmacı", -8, -8, -6, "Ek mesai yapılmadı; bekleme ve müşteri şikâyetleri arttı."),
          ]),
        V("mag-03",
          "Görsel düzenleme uzmanı Elif Demir, kampanya masasını girişe yakın kurdu. Güvenlik ekibi geçiş genişliğinin azaldığını, satış ekibi ise bu yerleşimin ilgiyi artırdığını söylüyor.",
          "Elif Demir", "görsel düzenleme uzmanı", [
              S("Masayı hemen güvenli ölçüye göre taşıtıp satış etkisini gün sonunda inceleyin.", "Otoriter", -3, 4, 9, "Geçiş güvenli hâle geldi; kampanya görünürlüğü geçici azaldı."),
              S("Güvenlik ve Elif'le alternatif yerleşimleri ölçerek aynı gün kararlaştırın.", "Demokratik", 5, -3, 9, "Ekip ortak düzende uzlaştı; kurulum tekrar yapıldı."),
              S("Elif'e güvenli geçiş koşuluyla iki yerleşim denemesi hazırlatın.", "Koçvari", 6, 2, 5, "Elif çözüm üretti; test süresince ek takip gerekti."),
              S("Şikâyet gelene kadar masayı olduğu yerde bırakın.", "Kaçınmacı", -5, 5, -10, "Kampanya devam etti ama geçiş riski açık kaldı."),
          ]),
        V("mag-04",
          "Kasa kapanışlarında üç gündür küçük tutarlı farklar çıkıyor. Ayşe Yıldız devir teslim sırasında sayım yapılmadığını söylüyor; çalışanlar birbirinden şüphelenmeye başladı.",
          "Ayşe Yıldız", "kasiyer", [
              S("Çift imzalı devir sayımı başlatıp farkları kayıtlar üzerinden inceleyin.", "Otoriter", -5, 6, 7, "İzlenebilirlik arttı; ekip ilk günlerde denetim baskısı hissetti."),
              S("Kasiyerleri ayrı dinleyip devir sürecini birlikte yeniden tanımlayın.", "Demokratik", 5, -2, 9, "Şüphe dili azaldı; yeni süreç için ek görüşme gerekti."),
              S("Ayşe'ye örnek devir kontrolü hazırlatıp pilot vardiyada deneyin.", "Koçvari", 7, 3, 4, "Ayşe süreci sahiplendi; pilot dışındaki farklar henüz açıklanmadı."),
              S("Farklar küçük diye bir hafta daha kayıt tutmakla yetinin.", "Kaçınmacı", -6, -5, -9, "Maddi fark küçük kaldı ama ekipte güvensizlik büyüdü."),
          ]),
        V("mag-05",
          "Depo sorumlusu Can Öztürk, çocuk montlarında sistemle raf arasında 18 adet fark buldu. Ürün ertesi günün ana kampanya görselinde yer alıyor.",
          "Can Öztürk", "depo sorumlusu", [
              S("Satışı doğru stok doğrulanana kadar sınırlayıp acil yeniden sayım yaptırın.", "Otoriter", -4, -4, 10, "Yanlış satış riski azaldı; kampanya açılışında ürün görünürlüğü düştü."),
              S("Can ve satış ekibiyle hareket kayıtlarını inceleyip doğrulanan adedi duyurun.", "Demokratik", 4, 0, 8, "Ekip ortak sayıya ulaştı; inceleme açılışa kadar sürdü."),
              S("Can'a sayım farkının kaynağını buldurup kontrol adımını kurmasına destek olun.", "Koçvari", 5, 2, 5, "Can kalıcı kontrol önerdi; kısa vadeli stok kararı yine gerekti."),
              S("Kampanyayı planlandığı gibi açıp stok farkını sonra araştırın.", "Kaçınmacı", -4, 6, -10, "Kampanya hızlı açıldı; yanlış stok vaadi riski oluştu."),
          ]),
        V("mag-06",
          "Müşteri, fişteki ürünle aldığı ürünün bedeninin farklı olduğunu belirtiyor. Reyon sorumlusu Selin Kaya ürünün son adet olduğunu ve ikinci müşterinin ürünü ayırttığını söylüyor.",
          "Selin Kaya", "reyon sorumlusu", [
              S("Kayıtları doğrulayıp ayırma kuralına göre tek bir karar verin.", "Otoriter", -2, 6, 5, "Karar hızlı çıktı; müşterilerden biri önerilen alternatifi kabul etmedi."),
              S("İki müşterinin beklentisini ayrı dinleyip mevcut seçenekleri açıkça sunun.", "Demokratik", 4, -4, 9, "Süreç adil görüldü; işlem süresi uzadı."),
              S("Selin'e stok ve ayırma adımlarını inceletip seçenekleri hazırlamasını isteyin.", "Koçvari", 5, 2, 4, "Selin uygulama açığını fark etti; müşteri yanıtı için yine hızlı karar gerekti."),
              S("Ürünü depoya kaldırıp iki müşteriye de daha sonra dönüş yapın.", "Kaçınmacı", -4, -6, -8, "Anlık tartışma durdu; iki müşteri de belirsizlik yaşadı."),
          ]),
        V("mag-07",
          "Mağaza müdür yardımcısı Zeynep Aydın, yeni çalışanın yanlış etiket bastığını fark etti. Çalışan bunu kendisi bildirmiş, ancak Zeynep hatanın kampanya sabahı duyurulmasının mağazayı zor durumda bırakacağını düşünüyor.",
          "Zeynep Aydın", "mağaza müdür yardımcısı", [
              S("Etiketleri hemen toplatıp hatanın kapsamını kayda alın.", "Otoriter", -4, 5, 9, "Hatalı fiyat riski durdu; sabah hazırlığı aksadı."),
              S("Zeynep ve yeni çalışanla ürünleri önceliklendirip ortak düzeltme yapın.", "Demokratik", 5, -2, 8, "Çalışan hatayı saklamadığı için destek gördü; düzeltme biraz uzadı."),
              S("Yeni çalışana Zeynep'in desteğiyle etiket doğrulama görevi verin.", "Koçvari", 7, 2, 4, "Çalışan süreci öğrendi; kontrol tamamlanana kadar yakın takip gerekti."),
              S("İlk müşteri itirazına kadar yalnızca not alın.", "Kaçınmacı", -4, 5, -10, "Açılış hızlı yapıldı; ilk itirazda sorun büyüdü."),
          ]),
        V("mag-08",
          "Bölge müdürü ziyareti öncesi vitrin bitmedi. Elif Demir, ekibin iki gecedir geç çıktığını; yalnızca ana vitrinin bugün yetişebileceğini söylüyor.",
          "Elif Demir", "görsel düzenleme uzmanı", [
              S("Ana vitrini önceliklendirip diğer alanların teslim tarihini açıkça belirtin.", "Otoriter", -2, 7, 7, "Ana vitrin tamamlandı; diğer alanlar için takip sözü verildi."),
              S("Elif ve ekiple gerçekçi kapsamı belirleyip bölge müdürüne önceden bildirin.", "Demokratik", 6, -3, 9, "Beklenti yönetildi; ekip üretime daha az zaman ayırdı."),
              S("Elif'e sadeleştirilmiş vitrin önerisi geliştirme yetkisi verin.", "Koçvari", 8, 3, 4, "Elif pratik bir çözüm buldu; kapsam son anda değişti."),
              S("Ziyarette yetişmeyen alanları açıklamayı tercih edin.", "Kaçınmacı", 1, -6, -8, "Ekip ek mesai yapmadı; yönetim hazırlıksız yakalandı."),
          ]),
        V("mag-09",
          "Kasiyer Burak Şahin, müşterinin iade etmek istediği üründe fiş olmadığını ama sistemde satın alma kaydı gördüğünü söylüyor. Ürün kullanılmış görünüyor; müşteri bugün çözüm istiyor.",
          "Burak Şahin", "kasiyer", [
              S("İade koşullarını ve ürün durumunu doğrulayıp gerekçeli karar verin.", "Otoriter", -2, 5, 7, "Kural tutarlı uygulandı; müşteri farklı çözüm talep etti."),
              S("Müşteriye inceleme adımlarını anlatıp Burak'la uygun seçenekleri değerlendirin.", "Demokratik", 4, -3, 8, "Müşteri süreci anladı; karar daha geç verildi."),
              S("Burak'a benzer iadelerde kanıt toplama ve iletişim pratiği yaptırın.", "Koçvari", 5, 1, 4, "Burak güven kazandı; mevcut talep için ayrıca onay gerekti."),
              S("Uyuşmazlığı başka vardiyaya aktarın.", "Kaçınmacı", -5, -5, -9, "Bugünkü tartışma sonlandı; müşteri yeniden gelmek zorunda kaldı."),
          ]),
        V("mag-10",
          "Yeni sezon ürünleri mağazaya geldi; Can Öztürk depoda yer kalmadığını söylüyor. Satış ekibi ise eski sezon ürünlerinin raftan erken çekilmesinin satış kaybettireceğini düşünüyor.",
          "Can Öztürk", "depo sorumlusu", [
              S("Güvenli depo sınırına göre eski ürünlerin kontrollü sevkini başlatın.", "Otoriter", -3, 5, 6, "Depo rahatladı; bazı eski ürünlerin satış fırsatı azaldı."),
              S("Can ve satış ekibiyle günlük satışa göre kademeli alan planı yapın.", "Demokratik", 5, -2, 8, "İki ekip ortak takvim buldu; kurulum yavaş ilerledi."),
              S("Can'a lokasyon alternatiflerini inceletip pilot yerleşim yaptırın.", "Koçvari", 6, 2, 4, "Can kapasite kazandı; çözüm tüm ürünleri karşılamadı."),
              S("Yeni kolileri koridorlarda geçici tutun.", "Kaçınmacı", -7, 3, -10, "Ürünler kabul edildi; güvenli geçiş alanı daraldı."),
          ]),
        V("mag-11",
          "Kasada ödeme bekleyen müşteri sıra önceliği nedeniyle çalışanla tartıştı. Vardiya amiri Mehmet Kara, çalışanı müşterilerin önünde uyarmayı öneriyor.",
          "Mehmet Kara", "vardiya amiri", [
              S("Müşteri önündeki tartışmayı bitirip çalışanla ayrı alanda görüşün.", "Otoriter", -1, 6, 7, "Kasa akışı düzeldi; olayın nedeni ayrıca incelenecek."),
              S("Müşteri ve çalışanı ayrı dinleyerek somut sıra kuralını açıklayın.", "Demokratik", 4, -4, 9, "Taraflar dinlendi; kuyruk bir süre daha uzadı."),
              S("Mehmet'le zor konuşmalar için vardiya sonrası kısa uygulama çalışın.", "Koçvari", 6, 1, 5, "Mehmet yaklaşımını gözden geçirdi; anlık çözüm için destek gerekti."),
              S("Mehmet'in müşterinin önünde uyarı yapmasına müdahale etmeyin.", "Kaçınmacı", -9, 3, -10, "Müşteri sakinleşti; çalışan kendini herkesin önünde suçlanmış hissetti."),
          ]),
        V("mag-12",
          "Ayşe Yıldız, kapanıştan sonra kalan iadelerin ertesi günün kasiyerine devredildiğini ve sahiplik belirsizliği yarattığını bildiriyor.",
          "Ayşe Yıldız", "kasiyer", [
              S("Kapanışta açık iade listesi ve sorumlu onayı zorunlu tutun.", "Otoriter", -2, 5, 7, "İş takibi netleşti; kapanış süresi biraz uzadı."),
              S("Kasiyerlerle kabul edilebilir devir akışını birlikte kurun.", "Demokratik", 5, -2, 8, "Devir sahiplenildi; standartlaşma için birkaç vardiya gerekti."),
              S("Ayşe'ye devir kontrolünü pilot olarak yönetme fırsatı verin.", "Koçvari", 6, 3, 4, "Ayşe çözümü sahada test etti; tek kişiye bağımlılık izlenmeli."),
              S("Açık iadeleri mevcut alışkanlıkla devretmeye devam edin.", "Kaçınmacı", -4, -5, -8, "Kısa vadede işlem değişmedi; ertesi gün uyuşmazlık sürdü."),
          ]),
        V("mag-13",
          "Bir müşteri son üç ziyarette istediği bedeni bulamadığını söylüyor. Selin Kaya, depoda ürünün olduğunu fakat raf yenilemenin öğleden sonraya bırakıldığını fark etti.",
          "Selin Kaya", "reyon sorumlusu", [
              S("Çok satan bedenler için sabah raf yenileme kuralı koyun.", "Otoriter", -2, 6, 6, "Ürün erişimi düzeldi; sabah görev yoğunluğu arttı."),
              S("Selin ve depo ekibiyle raf yenileme saatini satış akışına göre ayarlayın.", "Demokratik", 4, -2, 8, "İş yükü dengelendi; yeni düzenin oturması zaman alacak."),
              S("Selin'e beden bazlı stok takibi pilotu verin.", "Koçvari", 6, 2, 5, "Selin veriye dayalı öneri hazırladı; pilot kapsamı sınırlı kaldı."),
              S("Müşteriye çevrim içi kanalı önerip raf sürecini değiştirmeyin.", "Kaçınmacı", -3, -5, -9, "Müşteriye alternatif sunuldu; mağaza stok sorunu devam etti."),
          ]),
        V("mag-14",
          "Kampanya ürünü için mağaza içi afişte bitiş tarihi pazar, dijital ekranda cumartesi görünüyor. Zeynep Aydın, müşteriler gelmeden bir karar verilmesi gerektiğini söylüyor.",
          "Zeynep Aydın", "mağaza müdür yardımcısı", [
              S("Onaylı kampanya takvimini doğrulayıp yanlış görseli derhal kaldırın.", "Otoriter", -2, 6, 8, "Yanlış bilgi kaldırıldı; bazı görsel alanlar boş kaldı."),
              S("Pazarlama ve Zeynep'le tek tarih üzerinde uzlaşıp ekibi bilgilendirin.", "Demokratik", 4, -3, 9, "Tutarlı iletişim sağlandı; açılış hazırlığı uzadı."),
              S("Zeynep'e tüm mağaza materyallerini taratıp kontrol listesi oluşturun.", "Koçvari", 5, 2, 5, "Zeynep ek uyumsuzlukları da buldu; ilk düzeltme için destek gerekti."),
              S("Müşteri sorarsa doğru tarihi sözlü söyleyin.", "Kaçınmacı", -3, 4, -10, "Görseller yerinde kaldı; müşteriler farklı tarih gördü."),
          ]),
        V("mag-15",
          "Kasiyer Ayşe Yıldız, işitme güçlüğü yaşayan bir müşterinin kampanya koşullarını anlamadığını ve kuyruğun sabırsızlandığını bildiriyor.",
          "Ayşe Yıldız", "kasiyer", [
              S("Ayşe'ye diğer kasayı açtırıp müşteriye yazılı koşulları siz gösterin.", "Otoriter", -1, 6, 8, "Müşteri bilgi aldı; kısa süreli personel kaydırma gerekti."),
              S("Müşterinin tercih ettiği iletişim yolunu sorup Ayşe'yle işlemi tamamlayın.", "Demokratik", 5, -3, 10, "Müşteri anlaşılmış hissetti; işlem süresi uzadı."),
              S("Ayşe ile erişilebilir iletişim için kısa bir uygulama hazırlayın.", "Koçvari", 6, 1, 5, "Ayşe sonraki işlemler için hazırlandı; mevcut işlemde destek sürdü."),
              S("Kuyruğu eritmek için müşteriyi daha sakin saate davet edin.", "Kaçınmacı", -5, 5, -10, "Kuyruk azaldı; müşteri işlem yapamadan ayrıldı."),
          ]),
        V("mag-16",
          "Yeni açılan mağazanın açılış saatinde depo kapısı arızalandı. Can Öztürk kolilerin güvenli girişini sağlayamadığını; satış ekibi rafların eksik olduğunu söylüyor.",
          "Can Öztürk", "depo sorumlusu", [
              S("Güvenli giriş sağlanana kadar yük hareketini durdurup bakım çağırın.", "Otoriter", -3, -5, 10, "Güvenlik korundu; rafların dolması gecikti."),
              S("Can, bakım ve satış ekibiyle güvenli geçici dağıtım planı kurun.", "Demokratik", 4, -2, 8, "Ekip planı uyguladı; koordinasyon zaman aldı."),
              S("Can'a güvenli alternatif akışın sınırlarını çizip uygulamayı yönetme fırsatı verin.", "Koçvari", 5, 2, 5, "Can sorumluluk aldı; çözüm bakım tamamlanana kadar geçici kaldı."),
              S("Kolileri müşteri geçişine yakın kapıdan hızla taşıtın.", "Kaçınmacı", -6, 7, -11, "Raflar doldu; müşteri geçişinde risk oluştu."),
          ]),
        V("mag-17",
          "Reyon sorumlusu Selin Kaya, sürekli yüksek satış yapan bir çalışanın ekip arkadaşlarına zor görevleri bıraktığını söylüyor. Satış sonuçları güçlü, ekip memnuniyeti düşüyor.",
          "Selin Kaya", "reyon sorumlusu", [
              S("Görev dağılımını netleştirip tüm ekip için ölçülebilir sınır koyun.", "Otoriter", -4, 5, 5, "Dağılım düzeldi; başarılı çalışan kararın kişiselleştiğini düşündü."),
              S("Selin ve çalışanlarla görev yükünü verilerle birlikte konuşun.", "Demokratik", 5, -3, 8, "Adalet algısı arttı; toplantı satış saatinden zaman aldı."),
              S("Güçlü satış yapan çalışanla ekip katkısı üzerine gelişim görüşmesi yapın.", "Koçvari", 6, 2, 5, "Çalışan davranışının etkisini gördü; değişim takip gerektiriyor."),
              S("Satış sonuçları iyi diye iş dağılımına karışmayın.", "Kaçınmacı", -8, 4, -9, "Satış sürdü; ekipte görev adaletsizliği büyüdü."),
          ]),
        V("mag-18",
          "Mehmet Kara, mağaza kapanışında güvenlik kontrolünü kısaltırsa ekibin zamanında çıkabileceğini söylüyor. Son haftalarda kapanış mesaisi uzadı.",
          "Mehmet Kara", "vardiya amiri", [
              S("Güvenlik adımlarını koruyup vardiya görevlerini daha erken başlatın.", "Otoriter", -3, 4, 8, "Kontrol tam yapıldı; kapanış görevleri gün içine taşındı."),
              S("Mehmet ve ekiple hangi hazırlıkların daha erken yapılabileceğini belirleyin.", "Demokratik", 4, -2, 8, "Ekip gerçekçi plan kurdu; ilk akşam yine gecikme yaşandı."),
              S("Mehmet'e kapanış süresi ölçümü yaptırıp darboğazı iyileştirin.", "Koçvari", 6, 2, 5, "Mehmet kalıcı fırsat buldu; ilk gün ölçüm zaman aldı."),
              S("Bugün güvenlik kontrolünü kısaltıp yarın düzeltmeye karar verin.", "Kaçınmacı", 2, 6, -11, "Ekip erken çıktı; kontrol açığı kayıt altına alındı."),
          ]),
        V("mag-19",
          "Sezon sonu indiriminde müşteri yoğunluğu artarken prova kabininde unutulan kişisel bir eşya bulundu. Zeynep Aydın teslim sürecini hızlandırmak istiyor.",
          "Zeynep Aydın", "mağaza müdür yardımcısı", [
              S("Eşyayı kayıt altına alıp teslim doğrulamasıyla işlem yapın.", "Otoriter", -2, 3, 9, "Eşya güvenli tutuldu; teslim alan müşterinin işlemi uzadı."),
              S("Zeynep ve güvenlikle standart teslim prosedürünü birlikte uygulayın.", "Demokratik", 4, -2, 8, "Sorumluluk netleşti; yoğun saatte iki çalışan ayrıldı."),
              S("Zeynep'e kayıp eşya adımlarını ekibe öğretme görevi verin.", "Koçvari", 5, 1, 5, "Ekip bilgi kazandı; yoğunluğa kısa süreli yük bindi."),
              S("Eşyayı danışmaya bırakıp kayıt tutmayın.", "Kaçınmacı", -3, 5, -10, "Tezgâh rahatladı; teslim zinciri belirsiz kaldı."),
          ]),
        V("mag-20",
          "Ayşe Yıldız, mağazanın en yoğun saatinde POS cihazının bağlantısının aralıklı koptuğunu söylüyor. Nakit işlem mümkün, ancak müşterilerin çoğu kartla ödeme yapıyor.",
          "Ayşe Yıldız", "kasiyer", [
              S("Arızalı kasayı durdurup diğer kasalara yönlendirin; teknik destek kaydı açın.", "Otoriter", -3, 5, 8, "Hatalı işlemler durdu; diğer kasalarda sıra uzadı."),
              S("Ayşe ve ekiple ödeme seçeneklerini müşterilere tutarlı biçimde anlatın.", "Demokratik", 4, -2, 8, "Müşteriler bilgilendi; iletişim için personel ayrıldı."),
              S("Ayşe'ye sorun saatlerini kaydettirip teknik ekiple çözümü izlemesini sağlayın.", "Koçvari", 5, 2, 5, "Arıza verisi toplandı; anlık sıkışıklık sürdü."),
              S("Cihaz tekrar bağlanır diye müşterileri aynı kasada bekletin.", "Kaçınmacı", -6, -7, -9, "Bazı işlemler tamamlandı; kuyruk öngörülemez hâle geldi."),
          ]),
    ],

    "Tedarik Zinciri": [
        V("ted-01",
          "Planlama uzmanı Derya Aksoy, 12 mağazaya gidecek ürünlerin gümrükte üçüncü gününe girdiğini bildiriyor. Mağazalar yarın kampanyaya çıkacak; alternatif stok yalnızca altı mağazaya yeterli.",
          "Derya Aksoy", "sevkiyat planlama uzmanı", [
              S("Doğrulanmış stokla altı mağazaya sevk yapıp diğerleri için kampanya uyarısı gönderin.", "Otoriter", -3, 7, 6, "Altı mağaza ürün aldı; diğer altısı kampanya planını değiştirdi."),
              S("Mağaza ekipleriyle satış potansiyeline göre sınırlı stoku dağıtın.", "Demokratik", 4, -3, 9, "Dağıtım gerekçesi paylaşıldı; sevkiyat kararı gecikti."),
              S("Derya'ya gümrük takibi ve erken uyarı planı hazırlama yetkisi verin.", "Koçvari", 5, 2, 5, "Derya kalıcı uyarı önerdi; stok açığı bugün devam etti."),
              S("Gümrükten haber gelene kadar mağazalara bir şey söylemeyin.", "Kaçınmacı", -4, 2, -10, "Mağazalar kampanyaya hazırlıksız yakalandı."),
          ]),
        V("ted-02",
          "Depo şefi Murat Demir, yoğun sevkiyat için forkliftlerin tek koridorda çift yönlü kullanılmasını öneriyor. İş güvenliği sorumlusu bu planın güvenli olmadığını belirtiyor.",
          "Murat Demir", "depo operasyon şefi", [
              S("Çift yönlü hareketi reddedip sevkiyat sırasını yeniden belirleyin.", "Otoriter", -3, -5, 10, "Risk azaltıldı; bazı çıkışlar geç kaldı."),
              S("Murat ve iş güvenliğiyle güvenli alternatif rotayı birlikte tasarlayın.", "Demokratik", 4, -3, 9, "Güvenli rota bulundu; saha düzenlemesi zaman aldı."),
              S("Murat'a güvenli kapasite ölçümü yaptırıp sonraki sevkiyatı buna göre planlayın.", "Koçvari", 5, 2, 5, "Murat planlama verisi çıkardı; ilk sevkiyat yavaşladı."),
              S("Sadece bu vardiyada çift yönlü kullanıma göz yumun.", "Kaçınmacı", -6, 7, -11, "Sevkiyat hızlandı; güvenlik riski açık kaldı."),
          ]),
        V("ted-03",
          "Envanter analisti Elif Demir, aynı SKU'nun sistemde iki lokasyonda göründüğünü fark etti. Sipariş toplama ekibi yanlış rafa gidiyor; sistem düzeltmesi gece yapılabiliyor.",
          "Elif Demir", "envanter analisti", [
              S("İlgili SKU'nun toplamasını geçici durdurup fiziksel yeri doğrulayın.", "Otoriter", -3, -4, 9, "Yanlış toplama önlendi; siparişler bekledi."),
              S("Elif ve saha ekibiyle doğrulanan lokasyonu vardiyaya duyurun.", "Demokratik", 4, 0, 8, "Operasyon sürdü; geçici duyuru titiz takip gerektirdi."),
              S("Elif'e lokasyon uyuşmazlıklarını tespit eden günlük kontrol tasarlatın.", "Koçvari", 5, 2, 5, "Yeni kontrol önerildi; sistem kaydı gece düzeltilecek."),
              S("Çalışanların ürünü buldukları yerden toplamasına izin verin.", "Kaçınmacı", -4, 5, -10, "Bazı siparişler çıktı; stok doğruluğu daha da bozuldu."),
          ]),
        V("ted-04",
          "Taşıyıcı son dakika daha küçük araç gönderdi. Lojistik koordinatörü Barış Şahin, tüm mağazalara az miktarda ürün ulaştırmayı öneriyor; bazı ürünler ise yalnızca belirli mağazalarda satıyor.",
          "Barış Şahin", "lojistik koordinatörü", [
              S("Öncelikli mağazaları satış verisine göre seçip ikinci araç isteyin.", "Otoriter", -3, 7, 5, "Kritik mağazalar ürün aldı; kalan sevkiyat ek maliyet yarattı."),
              S("Barış ve mağazalarla kısıtlı kapasiteyi birlikte paylaştırın.", "Demokratik", 4, -3, 9, "Karar kabul gördü; araç çıkışı gecikti."),
              S("Barış'a kapasite teyit kontrolü kurdurup bugünkü dağıtımı destekleyin.", "Koçvari", 5, 2, 5, "Gelecek hata riski azaldı; bugünkü dağıtım kısmi kaldı."),
              S("Kolileri araç sığdığı kadar yükleyip kalanı haber vermeden bırakın.", "Kaçınmacı", -4, 5, -10, "Araç zamanında çıktı; mağazalar eksik teslimata hazırlıksız yakalandı."),
          ]),
        V("ted-05",
          "İade ürünleri yeni ürün kabul alanına karıştı. Kalite sorumlusu Selin Kaya, bazı ürünlerin yeniden satışa uygunluğunun belirsiz olduğunu söylüyor.",
          "Selin Kaya", "kalite sorumlusu", [
              S("Karışan partiyi ayırıp kalite onayı gelene dek sevkiyatı sınırlayın.", "Otoriter", -3, -5, 10, "Uygunsuz satış riski durdu; teslimatlar yavaşladı."),
              S("Selin ve depo ekibiyle ürünleri risk düzeyine göre ayırın.", "Demokratik", 4, -2, 8, "Öncelikli ayrıştırma yapıldı; süreç ek iş gücü istedi."),
              S("Selin'e kabul etiketlerini yeniden tasarlatıp ekipte pilot uygulayın.", "Koçvari", 5, 2, 5, "Kalıcı çözüm denendi; mevcut karışıklık ayrıca ayıklandı."),
              S("Kolileri mevcut alanlarında tutup sevkiyat sırasında kontrol edin.", "Kaçınmacı", -5, 3, -10, "Alan boşaltılmadı; yanlış sevkiyat olasılığı arttı."),
          ]),
        V("ted-06",
          "Planlama uzmanı Derya Aksoy, okul sezonu talep tahmininin üç bölgede %25 düşük kaldığını söylüyor. Tek ek sevkiyat hakkı var ve tüm bölgelere yetmeyecek.",
          "Derya Aksoy", "sevkiyat planlama uzmanı", [
              S("Satış hızı en yüksek bölgelere sevkiyat yapın ve gerekçeyi paylaşın.", "Otoriter", -3, 7, 5, "Satış kaybı sınırlı kaldı; düşük öncelikli bölgeler memnun olmadı."),
              S("Bölgelerle mevcut stok ve alternatif ürünleri birlikte değerlendirin.", "Demokratik", 4, -3, 9, "Alternatifler bulundu; dağıtım kararı yavaşladı."),
              S("Derya'ya bölgesel talep sinyali için erken uyarı modeli hazırlatın.", "Koçvari", 5, 2, 5, "Yeni tahmin yöntemi başladı; bugünkü açık kısmen sürdü."),
              S("Ürünler eşit dağılsın diye tüm bölgelere sembolik miktar gönderin.", "Kaçınmacı", -3, 1, -8, "Herkese az ürün ulaştı; hiçbir bölgede talep karşılanmadı."),
          ]),
        V("ted-07",
          "Gece vardiyasında tarayıcıların yarısı çalışmıyor. Depo şefi Murat Demir manuel toplama öneriyor; sabah teslimat saati sabit.",
          "Murat Demir", "depo operasyon şefi", [
              S("Öncelikli siparişleri çalışan cihazlarla tamamlayıp diğerlerini işaretleyin.", "Otoriter", -3, 6, 6, "Kritik siparişler çıktı; kalanlar açıkça gecikti."),
              S("Murat ve ekiple manuel toplamada çift kontrol uygulanabilecek siparişleri seçin.", "Demokratik", 4, -2, 8, "Kapasite arttı; çift kontrol zaman aldı."),
              S("Murat'a cihaz hazırlık kontrolünü vardiya açılışına ekletin.", "Koçvari", 5, 1, 5, "Sorun tekrarı için adım atıldı; sabah riski sürdü."),
              S("Tüm siparişleri cihazlar düzelene kadar bekletin.", "Kaçınmacı", -4, -8, -7, "Yanlış toplama olmadı; teslimatların çoğu gecikti."),
          ]),
        V("ted-08",
          "Bir tedarikçinin koli etiketlerinde ürün kodları hatalı. Elif Demir manuel düzeltmenin hızlı olduğunu, ancak kaynak hatanın tedarikçide sürdüğünü belirtiyor.",
          "Elif Demir", "envanter analisti", [
              S("Sorunlu partiyi kabulde ayırıp tedarikçiden doğrulanmış liste isteyin.", "Otoriter", -3, -4, 9, "Stok doğruluğu korundu; kabul gecikti."),
              S("Elif ve tedarikçiyle etiket düzeltme sorumluluğunu yazılı netleştirin.", "Demokratik", 4, -2, 8, "Sorumluluk belirlendi; ilk sevkiyat için ek koordinasyon gerekti."),
              S("Elif'e örnekleme kontrolü kurdurup tedarikçi performansına ekleyin.", "Koçvari", 5, 2, 5, "Gelecek hatalar daha erken bulunacak; bugünkü parti hâlâ iş gerektiriyor."),
              S("Tüm etiketleri depoda sessizce düzeltip tedarikçiye bildirmeyin.", "Kaçınmacı", -4, 4, -9, "Sevkiyat hızlandı; maliyet ve hata kaynağı görünmez kaldı."),
          ]),
        V("ted-09",
          "Yağış nedeniyle araçlar gecikiyor. Barış Şahin gece vardiyasını uzatmayı öneriyor; ekip son iki haftadır sık ek mesai yaptı.",
          "Barış Şahin", "lojistik koordinatörü", [
              S("Yalnız kritik teslimatlar için sınırlı ve kayıtlı ek vardiya düzenleyin.", "Otoriter", -3, 6, 5, "Kritik sevkiyatlar çıktı; yorgunluk riski izlenmeli."),
              S("Barış ve ekiple gönüllülük ve teslim önceliğini birlikte belirleyin.", "Demokratik", 5, -2, 8, "Yük dengelendi; bazı teslimler ertelendi."),
              S("Barış'a gecikme senaryoları için dönüşümlü kapasite planı yaptırın.", "Koçvari", 6, 1, 5, "Kalıcı plan oluştu; ilk gece çözüm sınırlı kaldı."),
              S("Gecikmeyi sabah vardiyasına açıklamasız devredin.", "Kaçınmacı", -6, -5, -9, "Gece ekip çıktı; sabah vardiyası birikmiş işle karşılaştı."),
          ]),
        V("ted-10",
          "Depo kapasitesi %96'ya ulaştı. Murat Demir koridor kenarlarını geçici stok alanı olarak kullanmak istiyor; gelecek hafta yeni sezon girişi başlayacak.",
          "Murat Demir", "depo operasyon şefi", [
              S("Koridor kullanımını reddedip onaylı geçici alan ve erken sevkiyat başlatın.", "Otoriter", -3, 4, 8, "Güvenli alan korundu; ek taşıma maliyeti doğdu."),
              S("Murat ve mağazalarla kabul-sevkiyat akışını yeniden planlayın.", "Demokratik", 4, -2, 8, "Depo rahatladı; mağazalar daha erken teslimat aldı."),
              S("Murat'a raf doluluk analizi ve pilot yerleşim iyileştirmesi yaptırın.", "Koçvari", 5, 2, 5, "Alan kazanıldı; yeni sezon hacminin tamamı karşılanmadı."),
              S("Bir haftalığına koridorlarda stok tutun.", "Kaçınmacı", -5, 5, -10, "Ürün kabul edildi; hareket ve tahliye alanı daraldı."),
          ]),
        V("ted-11",
          "Yanlış aktarma merkezine giden koliler fark edildi. Derya Aksoy hemen geri sevk edilirse maliyet artacağını; beklenirse üç mağazanın ürünsüz kalacağını söylüyor.",
          "Derya Aksoy", "sevkiyat planlama uzmanı", [
              S("Üç mağazanın kritik ürünlerini hızlandırılmış yönlendirmeye alın.", "Otoriter", -2, 5, 6, "Stok açığı azaldı; ek taşıma maliyeti oluştu."),
              S("Derya ve mağazalarla hangi ürünlerin gerçekten acil olduğunu netleştirin.", "Demokratik", 4, -2, 8, "Gereksiz ekspres maliyet azaltıldı; karar biraz gecikti."),
              S("Derya'ya yönlendirme kontrolünü ve yeni uyarı eşiğini geliştirtin.", "Koçvari", 5, 2, 5, "Tekrar riski azaldı; mevcut koliler ayrıca yönetildi."),
              S("Planlı transfer gününü bekleyin.", "Kaçınmacı", -4, -5, -8, "Ek maliyet oluşmadı; mağaza rafları boş kaldı."),
          ]),
        V("ted-12",
          "Depodaki sıcaklık sensörü bir ürün grubunda limit dışı değer gösterdi. Selin Kaya sensörün hatalı olabileceğini, yine de sevkiyat öncesi kontrol istediğini belirtiyor.",
          "Selin Kaya", "kalite sorumlusu", [
              S("İlgili ürünleri ayırıp bağımsız ölçüm doğrulanana kadar çıkışı durdurun.", "Otoriter", -3, -6, 10, "Kalite riski kontrol edildi; sevkiyat gecikti."),
              S("Selin, bakım ve depo ekibiyle ölçüm ve ürün durumunu birlikte doğrulayın.", "Demokratik", 4, -3, 9, "Veriye dayalı karar verildi; inceleme ek kapasite istedi."),
              S("Selin'e sıcaklık sapması uyarı planı hazırlatın.", "Koçvari", 5, 1, 5, "İzleme iyileşti; bugünkü parti için ayrıca karar gerekti."),
              S("Sensör hatalıdır diye ürünleri planlandığı gibi gönderin.", "Kaçınmacı", -4, 6, -11, "Sevkiyat çıktı; ürün uygunluğu belirsiz kaldı."),
          ]),
        V("ted-13",
          "Barış Şahin, taşıyıcının teslim edildi olarak işaretlediği üç kolinin mağazaya ulaşmadığını bildiriyor. Teslim tutanağındaki imza okunmuyor.",
          "Barış Şahin", "lojistik koordinatörü", [
              S("Kayıp bildirimi açıp taşıyıcıdan teslim kanıtı ve rota kaydı isteyin.", "Otoriter", -2, 4, 8, "Sorumluluk takibi başladı; ürünler hemen bulunmadı."),
              S("Barış ve mağaza ekibiyle teslim alanı kayıtlarını birlikte inceleyin.", "Demokratik", 4, -2, 8, "İki tarafın kayıtları karşılaştırıldı; araştırma zaman aldı."),
              S("Barış'a teslim kanıtı kalite kontrolü için düzenli izleme görevi verin.", "Koçvari", 5, 1, 5, "Yeni kontrol tasarlandı; bugünkü kayıp ayrıca çözülecek."),
              S("Tutar küçük diye taşıyıcı beyanını kabul edin.", "Kaçınmacı", -3, 3, -9, "Dosya kapandı; mağazanın eksik ürünü açıklanamadı."),
          ]),
        V("ted-14",
          "Elif Demir, stok sayımında aynı ürünün farklı renklerinin birbirine karıştığını söylüyor. Siparişler doğru miktarda ama yanlış renkte çıkabilir.",
          "Elif Demir", "envanter analisti", [
              S("İlgili lokasyonları geçici kapatıp renk bazlı ayrıştırma yaptırın.", "Otoriter", -3, -5, 9, "Yanlış ürün riski düştü; siparişler bekledi."),
              S("Elif ve toplama ekibiyle önce acil siparişleri kontrollü ayırın.", "Demokratik", 4, -2, 8, "Kritik siparişler çıktı; ek çift kontrol gerekti."),
              S("Elif'e renk-lokasyon işaretleme düzenini pilot olarak kurdurun.", "Koçvari", 5, 2, 5, "Takip kolaylaştı; mevcut karışımın ayıklanması sürdü."),
              S("Miktarlar tuttuğu için renk ayrımını sayım sonuna bırakın.", "Kaçınmacı", -4, 4, -10, "İşlem hızlandı; yanlış renk iade riski arttı."),
          ]),
        V("ted-15",
          "Yeni depo yazılımında eski sistemden aktarılan bazı siparişler çift görünüyor. Murat Demir bütün sevkiyatı durdurmanın büyük gecikme yaratacağını söylüyor.",
          "Murat Demir", "depo operasyon şefi", [
              S("Çift görünen siparişleri bloke edip doğrulananları sevk edin.", "Otoriter", -2, 5, 8, "Kontrollü sevkiyat sürdü; ayrıştırma iş yükü doğdu."),
              S("Murat ve IT ile çift kayıt ölçütünü belirleyip ekibi bilgilendirin.", "Demokratik", 4, -2, 8, "Ekip aynı kurala göre çalıştı; ilk inceleme gecikme yarattı."),
              S("Murat'a geçiş hatalarını günlük kontrol etme sorumluluğu verin.", "Koçvari", 5, 2, 5, "Geçiş daha yakından izlendi; ilk partide destek gerekti."),
              S("Müşteri şikâyeti gelene kadar tüm kayıtları sevk edin.", "Kaçınmacı", -4, 6, -11, "Çıkış hızı korundu; mükerrer teslimat riski oluştu."),
          ]),
        V("ted-16",
          "Bir mağaza, planlanan teslim penceresi dışında gece sevkiyat kabul edebileceğini söylüyor. Derya Aksoy bu seçeneğin maliyeti azaltacağını fakat güvenlik planının hazır olmadığını belirtiyor.",
          "Derya Aksoy", "sevkiyat planlama uzmanı", [
              S("Güvenlik ve personel teyidi gelmeden gece teslimatı onaylamayın.", "Otoriter", -2, -3, 9, "Güvenli kabul korundu; gündüz taşıma maliyeti arttı."),
              S("Derya ve mağaza yöneticisiyle kabul koşullarını netleştirin.", "Demokratik", 4, -2, 8, "Koşullar açıklandı; ilk uygun pencere kaçırıldı."),
              S("Derya'ya gece teslimatları için standart risk kontrolü hazırlatın.", "Koçvari", 5, 1, 5, "Gelecekte süreç hızlanacak; bugünkü karar ayrıca verildi."),
              S("Mağazanın sözlü kabulüne güvenip aracı yönlendirin.", "Kaçınmacı", -4, 5, -10, "Maliyet azaldı; teslim anında güvenlik ve sayım belirsiz kaldı."),
          ]),
        V("ted-17",
          "Selin Kaya, tedarikçiden gelen partinin koli dışlarının hasarlı, ürünlerin çoğunun sağlam olduğunu bildiriyor. Sevkiyat için yalnızca dört saat var.",
          "Selin Kaya", "kalite sorumlusu", [
              S("Hasarlı kolileri ayırıp örnekleme ve kayıt tamamlanmadan sevk etmeyin.", "Otoriter", -3, -5, 9, "Kanıt korundu; çıkışın bir bölümü gecikti."),
              S("Selin ve sevkiyat ekibiyle sağlam ürünleri kontrollü ayırın.", "Demokratik", 4, -2, 8, "Sağlam ürünler çıktı; ayrıştırma ekip zamanı aldı."),
              S("Selin'e tedarikçi hasar kontrol eşiği tasarlatın.", "Koçvari", 5, 1, 5, "Yeni ölçüt hazırlandı; bugünkü kontrol ayrıca sürdü."),
              S("Ürünler sağlam görünüyor diye tüm partiyi sevk edin.", "Kaçınmacı", -4, 5, -10, "Teslim tarihi korundu; sonradan hasar sorumluluğu tartışmalı kaldı."),
          ]),
        V("ted-18",
          "Depoda vardiya geçişinde yükleme listeleri sözlü aktarılıyor. Barış Şahin iki mağazanın yükleme sırasının bu yüzden karıştığını söylüyor.",
          "Barış Şahin", "lojistik koordinatörü", [
              S("Yazılı ve çift onaylı yükleme devri başlatın.", "Otoriter", -2, 5, 7, "Sıralama hatası azaldı; vardiya geçişi uzadı."),
              S("Barış ve vardiya liderleriyle pratik devir şablonu kurun.", "Demokratik", 4, -2, 8, "Ekip yöntemi benimsedi; ilk gün uyarlama gerekti."),
              S("Barış'a bir haftalık devir pilotu yönettirin.", "Koçvari", 5, 2, 5, "Barış veri topladı; diğer vardiyalara yayılım bekliyor."),
              S("Hataları yükleme öncesi fark ederiz diyerek mevcut yöntemi koruyun.", "Kaçınmacı", -4, -4, -9, "Kısa vadede değişim olmadı; karışıklık sürdü."),
          ]),
        V("ted-19",
          "Nakliye firması yakıt artışı nedeniyle sözleşmede olmayan ek ücret istiyor. Derya Aksoy, sevkiyatın bir gün ertelenmesinin mağazaları etkileyeceğini belirtiyor.",
          "Derya Aksoy", "sevkiyat planlama uzmanı", [
              S("Sözleşme dışı ücreti onaysız reddedip alternatif taşıma arayın.", "Otoriter", -2, -4, 8, "Yetki sınırı korundu; bazı araçlar geç çıktı."),
              S("Satın alma ve Derya'yla maliyet-hizmet seçeneklerini değerlendirin.", "Demokratik", 4, -2, 8, "Karar gerekçelendi; koordinasyon süresi uzadı."),
              S("Derya'ya kritik hatlar için alternatif taşıyıcı planı hazırlatın.", "Koçvari", 5, 1, 5, "Yedek kapasite belirlendi; bugünkü fiyat görüşmesi sürdü."),
              S("Ek ücreti kayıt dışında kabul edip sevkiyatı çıkarın.", "Kaçınmacı", -4, 6, -11, "Araç çıktı; mali ve sözleşmesel risk oluştu."),
          ]),
        V("ted-20",
          "Murat Demir, sevkiyat hedefi nedeniyle mola dönüşlerinin geciktiğini söylüyor. Bir çalışan yorgunluk yüzünden barkodları yanlış okuduğunu bildirdi.",
          "Murat Demir", "depo operasyon şefi", [
              S("Mola ve güvenli çalışma düzenini koruyup hedefleri yeniden sıralayın.", "Otoriter", -2, -4, 9, "Hata riski düştü; bazı sevkiyatlar gecikti."),
              S("Murat ve ekiple yük yoğunluğunu ve mola planını birlikte düzenleyin.", "Demokratik", 4, -2, 8, "Ekip planı benimsedi; yeniden dağıtım zaman aldı."),
              S("Murat'a yorgunluk işaretleri ve vardiya kapasitesi için takip sorumluluğu verin.", "Koçvari", 5, 1, 5, "Erken uyarı başladı; bugünkü yük yine sınırlanmalı."),
              S("Hedef tutana kadar molaları esnek bırakın.", "Kaçınmacı", -7, 5, -11, "Hedefe yaklaşıldı; okuma hataları ve yorgunluk arttı."),
          ]),
    ],

    "Satın Alma": [
        V("sat-01",
          "Ana tedarikçi sezon açılışına 15 gün kala %18 fiyat artışı istedi. Kategori yöneticisi Ece Arslan alternatifin kalite onayının henüz tamamlanmadığını söylüyor.",
          "Ece Arslan", "kategori yöneticisi", [
              S("Sözleşme şartlarına dayanarak artışı reddedip mevcut teslimatı talep edin.", "Otoriter", -3, 4, 7, "Bütçe korundu; tedarikçi teslim takvimini yeniden görüşmek istedi."),
              S("Ece ve finansla hacim, takvim ve fiyat seçeneklerini müzakere edin.", "Demokratik", 4, -2, 8, "Orta yol bulundu; görüşmeler zaman aldı."),
              S("Ece'ye alternatif kalite onayını hızlandıracak yasal plan hazırlatın.", "Koçvari", 5, 2, 5, "Yedek seçenek güçlendi; bugünkü fiyat talebi devam etti."),
              S("Artışı onaysız kabul edip bütçeyi daha sonra düzeltin.", "Kaçınmacı", -3, 6, -10, "Teslimat rahatladı; bütçe açığı doğdu."),
          ]),
        V("sat-02",
          "Kalite sorumlusu Selin Kaya, onaylanan numuneyle seri üretim kumaşı arasında belirgin fark buldu. Teslime 10 gün kaldı; ürün kampanyada yer alıyor.",
          "Selin Kaya", "kalite sorumlusu", [
              S("Uygunsuz partiyi durdurup sözleşmedeki düzeltme sürecini başlatın.", "Otoriter", -3, -7, 10, "Kalite korundu; kampanya teslimi riske girdi."),
              S("Selin, tedarikçi ve planlamayla uygun partileri ayırma olanağını inceleyin.", "Demokratik", 4, -3, 8, "Kısmi teslim seçeneği oluştu; kontrol iş yükü arttı."),
              S("Selin'e hızlı yeniden test ve kök neden çalışmasını yönettirin.", "Koçvari", 5, 1, 5, "Hatanın kaynağı bulundu; teslim kararı yine gerekti."),
              S("Görünüş farkı az diye partiyi kabul edin.", "Kaçınmacı", -4, 6, -11, "Takvim korundu; iade ve itibar riski oluştu."),
          ]),
        V("sat-03",
          "Satın alma uzmanı Ayşe Yıldız, yeni tedarikçinin fiyatının güçlü olduğunu fakat zorunlu uygunluk belgelerinin eksik olduğunu bildiriyor.",
          "Ayşe Yıldız", "satın alma uzmanı", [
              S("Belgeler doğrulanmadan sipariş onayı vermeyin.", "Otoriter", -2, -3, 10, "Uyum korundu; fiyat avantajı için ayrılan süre azaldı."),
              S("Ayşe ve uyum ekibiyle belge tamamlama takvimi oluşturun.", "Demokratik", 4, -2, 8, "Tedarikçi şartları öğrendi; sipariş bekledi."),
              S("Ayşe'ye onaylı alternatif tedarikçileri karşılaştırma görevi verin.", "Koçvari", 5, 2, 5, "Alternatif netleşti; düşük fiyat henüz kullanılamadı."),
              S("Belgeleri teslimattan önce alırız diyerek siparişi açın.", "Kaçınmacı", -3, 6, -11, "Fiyat sabitlendi; uygunluk riski üstlenildi."),
          ]),
        V("sat-04",
          "Ece Arslan bir tedarikçiye yetkisi dışında sözlü fiyat taahhüdü verdiğini söyledi. Tedarikçi bunu yazılı siparişe dönüştürmek istiyor.",
          "Ece Arslan", "kategori yöneticisi", [
              S("Yeni taahhüdü durdurup yetki ve sözleşme koşullarını resmen inceleyin.", "Otoriter", -4, 3, 9, "Şirket riski sınırlandı; tedarikçi yanıt bekliyor."),
              S("Ece ve tedarikçiyle şartları açıkça yeniden görüşün.", "Demokratik", 4, -2, 8, "İlişki korundu; pazarlık yeniden açıldı."),
              S("Ece'yle özel görüşüp yetki sınırları ve müzakere planı hazırlayın.", "Koçvari", 6, 1, 5, "Ece hatayı sahiplendi; tedarikçi talebi ayrıca çözülmeli."),
              S("İlişki bozulmasın diye sözlü taahhüdü onaysız onaylayın.", "Kaçınmacı", -3, 5, -10, "Tedarikçi memnun oldu; iç kontrol zayıfladı."),
          ]),
        V("sat-05",
          "Tedarikçi ödeme vadesini kısaltarak birim fiyatı düşürüyor. Finansal analist Kaan Polat, toplam nakit maliyetinin artabileceğini söylüyor.",
          "Kaan Polat", "finansal analist", [
              S("Toplam maliyet hesabı olmadan fiyat indirimini kabul etmeyin.", "Otoriter", -2, -2, 8, "Nakit riski sınırlandı; teklif süresi kısaldı."),
              S("Kaan ve satın alma ekibiyle farklı vade seçeneklerini karşılaştırın.", "Demokratik", 4, -2, 8, "Gerçek maliyet görüldü; karar gecikti."),
              S("Kaan'a sonraki tekliflerde kullanılacak karşılaştırma şablonu hazırlatın.", "Koçvari", 5, 2, 5, "Kararlar için standart oluştu; mevcut pazarlık sürdü."),
              S("Birim fiyat düşük diye teklifi doğrudan imzalayın.", "Kaçınmacı", -3, 5, -10, "Birim fiyat düştü; nakit baskısı arttı."),
          ]),
        V("sat-06",
          "Bir tedarikçi üretimi onaylı tesis dışındaki atölyeye kaydırmak istiyor. Selin Kaya yeni tesisin kalite ve çalışma koşullarının doğrulanmadığını söylüyor.",
          "Selin Kaya", "kalite sorumlusu", [
              S("Yeni tesis onaylanana kadar üretim yeri değişikliğini reddedin.", "Otoriter", -2, -6, 10, "Uyum korundu; teslim tarihi riske girdi."),
              S("Selin ve uyum ekibiyle doğrulama için gerçekçi yol haritası çıkarın.", "Demokratik", 4, -3, 8, "Koşullar netleşti; kısa vadeli kapasite daraldı."),
              S("Selin'e onaylı kapasite alternatiflerini bulma görevi verin.", "Koçvari", 5, 1, 5, "Yedek üretim seçeneği oluştu; maliyet artabilir."),
              S("Atölyeyi kayıt değiştirmeden geçici kullanmalarına izin verin.", "Kaçınmacı", -4, 6, -11, "Takvim korundu; doğrulanmamış üretim riski oluştu."),
          ]),
        V("sat-07",
          "İki tedarikçinin fiyatı eşit. Ayşe Yıldız birinin son üç teslimatta geciktiğini, diğerinin ise ilk kez çalışılacağını belirtiyor.",
          "Ayşe Yıldız", "satın alma uzmanı", [
              S("Geciken tedarikçiden kapasite kanıtı ve ceza koşulu isteyin.", "Otoriter", -2, 3, 7, "Risk görünür oldu; tedarikçi ek koşula itiraz etti."),
              S("Ayşe ve planlamayla iki seçeneğin teslim riskini puanlayın.", "Demokratik", 4, -2, 8, "Karar belgeli verildi; değerlendirme zaman aldı."),
              S("Ayşe'ye küçük pilot sipariş ve alternatif plan hazırlatın.", "Koçvari", 5, 2, 5, "Risk bölündü; sipariş yönetimi karmaşıklaştı."),
              S("Fiyat eşit diye rastgele mevcut tedarikçiyle devam edin.", "Kaçınmacı", -3, 4, -9, "Sipariş hızlı açıldı; gecikme riski sürdü."),
          ]),
        V("sat-08",
          "Kumaş numunesinin yıkama testi toplantı gününe yetişmedi. Kategori yöneticisi Ece Arslan sipariş penceresini kaçırmaktan endişeleniyor.",
          "Ece Arslan", "kategori yöneticisi", [
              S("Test tamamlanmadan nihai siparişi açmayın.", "Otoriter", -2, -5, 9, "Kalite güvencesi korundu; üretim penceresi daraldı."),
              S("Ece ve kaliteyle testin kritik kısmını ve alternatif takvimi değerlendirin.", "Demokratik", 4, -2, 8, "Sınırlı seçenek ortaya çıktı; ekip ek çalışma yaptı."),
              S("Ece'ye erken test kontrol noktası kurma sorumluluğu verin.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; bugünkü karar bekledi."),
              S("Numune iyi göründüğü için test olmadan onay verin.", "Kaçınmacı", -3, 5, -10, "Pencere korundu; dayanıklılık belirsiz kaldı."),
          ]),
        V("sat-09",
          "Üretici, teslimatı korumak için ambalaj malzemesini değiştirmek istiyor. Mağazacılık ekibi raf görünümünün etkilenebileceğini söylüyor.",
          "Ece Arslan", "kategori yöneticisi", [
              S("Onaylı ambalaj dışında üretimi durdurup yazılı değişiklik isteyin.", "Otoriter", -2, -4, 8, "Marka standardı korundu; üretim gecikti."),
              S("Ece ve mağaza ekibiyle örnek ambalajı hızlı değerlendirin.", "Demokratik", 4, -2, 8, "İki etki birlikte görüldü; numune bekleme süresi oluştu."),
              S("Ece'ye küçük parti testi ve raf geri bildirimi hazırlatın.", "Koçvari", 5, 1, 5, "Veri toplandı; toplu teslim kararı ertelendi."),
              S("Maliyet değişmiyor diye ambalaj değişikliğini bildirimsiz kabul edin.", "Kaçınmacı", -3, 5, -10, "Üretim sürdü; mağaza deneyimi öngörülemedi."),
          ]),
        V("sat-10",
          "Döviz artışı imzalanmamış siparişleri bütçe dışına taşıdı. Kaan Polat, tüm ürünleri aynı oranda azaltmanın temel bedenlerde stok açığı yaratacağını belirtiyor.",
          "Kaan Polat", "finansal analist", [
              S("Yüksek öncelikli ürünleri koruyup düşük önceliklerin miktarını kesin.", "Otoriter", -2, 5, 6, "Bütçe dengelendi; bazı ürün çeşitleri azaldı."),
              S("Kaan ve kategori ekibiyle ürün bazlı satış ve marj etkisini değerlendirin.", "Demokratik", 4, -2, 8, "Kesinti gerekçelendi; sipariş süreci uzadı."),
              S("Kaan'a farklı kur ve hacim senaryoları hazırlatın.", "Koçvari", 5, 1, 5, "Ekip seçenekleri gördü; tedarikçiye yanıt bekledi."),
              S("Bütçe sonra bulunur diyerek tüm siparişleri açın.", "Kaçınmacı", -3, 5, -10, "Stok planı korundu; finansal açık büyüdü."),
          ]),
        V("sat-11",
          "Tedarikçi, onaylı ürün yerine küçük teknik farkı olan bir muadil önermekte. Selin Kaya farkın müşteri kullanımını etkileyebileceğini belirtiyor.",
          "Selin Kaya", "kalite sorumlusu", [
              S("Muadili teknik onay olmadan reddedin.", "Otoriter", -2, -4, 9, "Ürün standardı korundu; tedarik riski arttı."),
              S("Selin ve ürün ekibiyle kullanım etkisini test ederek karar verin.", "Demokratik", 4, -2, 8, "Karar veriye dayandı; test maliyeti doğdu."),
              S("Selin'e muadil değerlendirme kontrol listesini geliştirtin.", "Koçvari", 5, 1, 5, "Sonraki kararlar hızlanacak; mevcut teklif bekledi."),
              S("Fark küçük diye muadili siparişe ekleyin.", "Kaçınmacı", -3, 5, -10, "Tedarik sürdü; kullanım uyumu belirsiz kaldı."),
          ]),
        V("sat-12",
          "Ayşe Yıldız, aynı tedarikçinin art arda üç faturasında sipariş şartlarından farklı bir navlun kalemi buldu. Faturalar ödeme gününe girdi.",
          "Ayşe Yıldız", "satın alma uzmanı", [
              S("Tartışmalı kalemi durdurup sözleşmeye göre yazılı açıklama isteyin.", "Otoriter", -2, 3, 9, "Ödeme kontrol edildi; tedarikçi itiraz etti."),
              S("Ayşe ve finansla üç faturayı birlikte karşılaştırın.", "Demokratik", 4, -2, 8, "Hatanın kapsamı netleşti; ödeme biraz gecikti."),
              S("Ayşe'ye navlun farklarını erken yakalayan kontrol hazırlatın.", "Koçvari", 5, 1, 5, "Tekrar riski düştü; mevcut üç fatura ayrıca düzeltilecek."),
              S("İlişki bozulmasın diye kalemi sorgulamadan ödeyin.", "Kaçınmacı", -3, 5, -10, "Ödeme çıktı; gereksiz maliyet yerleşti."),
          ]),
        V("sat-13",
          "Bir üretici acil üretim kapasitesi sunuyor ancak önceki denetiminde düzeltici aksiyonları açık. Ece Arslan sezon teslimine yetişmek için sınırlı sipariş öneriyor.",
          "Ece Arslan", "kategori yöneticisi", [
              S("Açık kritik aksiyonlar kapanmadan üretim onayı vermeyin.", "Otoriter", -2, -5, 10, "Uyum korundu; kapasite fırsatı kaybedildi."),
              S("Ece ve denetim ekibiyle aksiyonların risk düzeyini inceleyin.", "Demokratik", 4, -2, 8, "Kısıtlı güvenli seçenekler görüldü; karar uzadı."),
              S("Ece'ye onaylı üreticilerde kapasite arama görevi verin.", "Koçvari", 5, 1, 5, "Yedek seçenek gelişti; teslim maliyeti artabilir."),
              S("Düzeltmeler sonra kapanır diyerek siparişi açın.", "Kaçınmacı", -3, 5, -11, "Kapasite sağlandı; denetim riski taşındı."),
          ]),
        V("sat-14",
          "Tedarikçi, geçen sezonun başarılı ürününü aynı fiyatla sunuyor. Ayşe Yıldız bu sezonun beden dağılımının değiştiğini ve eski siparişin yanıltıcı olacağını söylüyor.",
          "Ayşe Yıldız", "satın alma uzmanı", [
              S("Eski siparişi kopyalamayı durdurup yeni beden dağılımı isteyin.", "Otoriter", -2, -3, 8, "Stok riski azaldı; sipariş açılışı gecikti."),
              S("Ayşe ve mağazacılıkla geçen sezon satışlarını bölge bazında inceleyin.", "Demokratik", 4, -2, 8, "Daha doğru sipariş oluştu; analiz emek istedi."),
              S("Ayşe'ye beden tahmin modeli pilotu hazırlatın.", "Koçvari", 5, 1, 5, "Öğrenme arttı; ilk sipariş hâlâ onay bekliyor."),
              S("Ürün geçen sezon sattı diye miktarları aynen koruyun.", "Kaçınmacı", -3, 5, -9, "Sipariş hızlı açıldı; beden uyumsuzluğu riski arttı."),
          ]),
        V("sat-15",
          "Numune onay toplantısında Selin Kaya dikiş dayanıklılığına itiraz ediyor; tasarım ekibi görünümü korumakta ısrar ediyor.",
          "Selin Kaya", "kalite sorumlusu", [
              S("Dayanıklılık eşiği sağlanana kadar onayı durdurun.", "Otoriter", -2, -4, 9, "Kalite ölçütü korundu; lansman sıkıştı."),
              S("Selin ve tasarımla görünümü koruyan teknik alternatif arayın.", "Demokratik", 4, -2, 8, "Ortak çözüm olasılığı doğdu; yeni numune gerekti."),
              S("Selin'e karşılaştırmalı test hazırlatıp tasarıma veriyi gösterin.", "Koçvari", 5, 1, 5, "İtiraz somutlaştı; karar test sonucunu bekledi."),
              S("Görsel onay verildiği için teknik itirazı not edip geçin.", "Kaçınmacı", -3, 5, -10, "Takvim korundu; dayanıklılık riski kaldı."),
          ]),
        V("sat-16",
          "Yeni tedarikçi ödeme için kayıtlı şirket hesabından farklı bir hesap iletti. Kaan Polat e-postanın sahte olabileceğini söylüyor.",
          "Kaan Polat", "finansal analist", [
              S("Ödemeyi durdurup kayıtlı irtibat üzerinden hesap teyidi alın.", "Otoriter", -2, -3, 10, "Dolandırıcılık riski azaltıldı; ödeme gecikti."),
              S("Kaan ve tedarikçi ilişkileriyle değişiklik belgelerini birlikte doğrulayın.", "Demokratik", 4, -2, 8, "Değişiklik netleşti; ek kontrol süresi oluştu."),
              S("Kaan'a hesap değişikliklerinde çift teyit kontrolü kurdurun.", "Koçvari", 5, 1, 5, "Sonraki ödemeler korunacak; bu ödeme ayrıca bekletildi."),
              S("E-posta kurumsal görünüyor diye yeni hesaba ödeme yapın.", "Kaçınmacı", -3, 5, -12, "Ödeme hızlı çıktı; hesap doğruluğu bilinmedi."),
          ]),
        V("sat-17",
          "Tedarikçi teslimatı ikiye bölmek istiyor. Ece Arslan ilk partinin kampanyaya yeteceğini, ikinci partinin gecikmesi hâlinde bazı mağazaların stoksuz kalacağını söylüyor.",
          "Ece Arslan", "kategori yöneticisi", [
              S("İkinci parti için bağlayıcı takvim ve risk planı isteyin.", "Otoriter", -2, 3, 8, "İlk parti ilerledi; tedarikçi ek koşula pazarlık açtı."),
              S("Ece ve planlamayla ilk partiyi kritik mağazalara ayırın.", "Demokratik", 4, -2, 8, "Stok açığı azaltıldı; dağıtım karmaşıklaştı."),
              S("Ece'ye yedek tedarik ve erken uyarı senaryosu hazırlatın.", "Koçvari", 5, 1, 5, "Esneklik arttı; maliyet yükselme olasılığı var."),
              S("İkinci parti zamanında gelir diye mevcut dağıtımı değiştirmeyin.", "Kaçınmacı", -3, 4, -9, "İlk sevkiyat kolaylaştı; gecikme riski açık kaldı."),
          ]),
        V("sat-18",
          "Ayşe Yıldız, tedarikçi değerlendirmesinde yüksek puan alan firmanın müşteri iadelerinde artış gördüğünü fark etti. Puan kartında iade verisi yok.",
          "Ayşe Yıldız", "satın alma uzmanı", [
              S("Yeni siparişi gözden geçirip iade verisini değerlendirmeye ekleyin.", "Otoriter", -2, -3, 8, "Risk görünür oldu; sipariş onayı gecikti."),
              S("Ayşe, kalite ve müşteri ekipleriyle iade nedenlerini birlikte analiz edin.", "Demokratik", 4, -2, 8, "Karar daha dengeli verildi; analiz zaman aldı."),
              S("Ayşe'ye puan kartını güncelleme sorumluluğu verin.", "Koçvari", 5, 1, 5, "Ölçüm gelişti; mevcut tedarikçi kararı bekledi."),
              S("Puan kartı güçlü diye iadeleri değerlendirmeye almayın.", "Kaçınmacı", -3, 4, -9, "Sipariş hızlı ilerledi; müşteri sorunu sürebilir."),
          ]),
        V("sat-19",
          "Kaan Polat, hacim indiriminin ancak depo kapasitesini aşacak miktarda alımla sağlanacağını bildiriyor.",
          "Kaan Polat", "finansal analist", [
              S("Depo kapasitesini aşan hacmi reddedip birim fiyatı yeniden görüşün.", "Otoriter", -2, 2, 8, "Operasyon riski azaldı; birim maliyet arttı."),
              S("Kaan ve lojistikle kademeli teslim teklifini müzakere edin.", "Demokratik", 4, -2, 8, "İndirim olasılığı korundu; sözleşme ayrıntıları uzadı."),
              S("Kaan'a toplam stok taşıma maliyeti hesabı hazırlatın.", "Koçvari", 5, 1, 5, "Gerçek tasarruf görüldü; teklif süresi daraldı."),
              S("İndirimi kaçırmamak için tüm hacmi tek seferde alın.", "Kaçınmacı", -4, 4, -10, "Birim fiyat düştü; depolama yükü arttı."),
          ]),
        V("sat-20",
          "Selin Kaya, test raporunda sınırda sonuç alan bir ürünü yeniden test etmek istiyor. Tedarikçi raporun teknik olarak geçerli olduğunu savunuyor.",
          "Selin Kaya", "kalite sorumlusu", [
              S("Politikadaki eşik ve tekrar test koşullarını uygulayın.", "Otoriter", -2, -3, 8, "Karar tutarlı verildi; teslim süresi daraldı."),
              S("Selin ve tedarikçiyle test koşullarındaki farkları açıkça inceleyin.", "Demokratik", 4, -2, 8, "Veri anlaşmazlığı netleşti; görüşme zaman aldı."),
              S("Selin'e benzer sınır değerler için karar matrisi hazırlatın.", "Koçvari", 5, 1, 5, "Gelecek kararlar kolaylaşacak; ürün için ek değerlendirme gerekti."),
              S("Rapor geçiyor diye Selin'in itirazını kayda almadan onaylayın.", "Kaçınmacı", -3, 4, -9, "Takvim korundu; kalite kaygısı çözümsüz kaldı."),
          ]),
    ],

    "İnsan Kaynakları": [
        V("ik-01",
          "İK iş ortağı Elif Demir, iki eşit güçlü adayın aynı terfiyi beklediğini söylüyor. Bir yönetici performansı, diğeri kritik teknik beceriyi öne çıkarıyor; kriterler önceden tam netleştirilmemiş.",
          "Elif Demir", "İK iş ortağı", [
              S("Rolün önceden belgelenmiş zorunlu kriterlerini esas alıp kararı gerekçelendirin.", "Otoriter", -3, 5, 7, "Karar netleşti; dışarıda kalan aday gelişim yolu bekliyor."),
              S("Elif'le bağımsız değerlendirme ve kalibrasyon oturumu kurun.", "Demokratik", 4, -3, 9, "Adalet algısı güçlendi; terfi takvimi uzadı."),
              S("Her adayla ayrı gelişim ve gelecek rol görüşmesi yapın.", "Koçvari", 7, -2, 7, "Adaylar geri bildirim aldı; seçim kararı yine verilmek zorunda."),
              S("İtiraz olmasın diye pozisyonu belirsiz süre açık tutun.", "Kaçınmacı", -7, -5, -10, "Kimse hemen reddedilmedi; ekipte belirsizlik büyüdü."),
          ]),
        V("ik-02",
          "İK uzmanı Zeynep Aydın, bir yönetici hakkında anonim psikolojik taciz iddiası aldı. Şikâyette tarih ve olay örnekleri var; iddia henüz doğrulanmadı.",
          "Zeynep Aydın", "İK uzmanı", [
              S("Gizlilik ve tarafsızlıkla resmî inceleme başlatın; peşin hüküm kurmayın.", "Otoriter", -2, -3, 10, "İddia ciddiye alındı; ekipte süreç gizliliği dikkatle yönetilmeli."),
              S("Zeynep'le ilgili prosedür ve güvenli ifade alma planı hazırlayın.", "Demokratik", 4, -3, 9, "İnceleme sağlam temele oturdu; başlangıç biraz gecikti."),
              S("Zeynep'e inceleme desteği verip tarafların korunmasını izleyin.", "Koçvari", 5, -2, 7, "Zeynep süreci yürüttü; bağımsızlık düzenli kontrol edilmeli."),
              S("Anonim olduğu için yeni kanıt gelmesini bekleyin.", "Kaçınmacı", -8, 2, -12, "İddia kayda geçti ama çalışanlar güvenli başvuru görmedi."),
          ]),
        V("ik-03",
          "İşe alım uzmanı Ayşe Yıldız, yeni başlayanların %30'unun ilk ayda ayrıldığını bildiriyor. Yöneticiler aday kalitesini, adaylar ise ilk hafta desteğini eleştiriyor.",
          "Ayşe Yıldız", "işe alım uzmanı", [
              S("Çıkış görüşmesi ve ilk ay verilerini standart biçimde toplayın.", "Otoriter", -2, 4, 7, "Nedenler ölçüldü; hemen çözüm bekleyen yöneticiler sabırsızlandı."),
              S("Ayşe, yeni başlayanlar ve yöneticilerle deneyimi birlikte inceleyin.", "Demokratik", 4, -3, 9, "Farklı nedenler görüldü; görüşmeler zaman aldı."),
              S("Ayşe'ye mentorluk pilotu yürütme sorumluluğu verin.", "Koçvari", 7, 2, 5, "Başlangıç desteği arttı; işe alım ölçütleri ayrıca incelenmeli."),
              S("Sezon yoğunluğu biterse ayrılma düşer diyerek bekleyin.", "Kaçınmacı", -5, -5, -8, "Ek işlem yapılmadı; sonraki grupta ayrılma sürdü."),
          ]),
        V("ik-04",
          "Bordro uzmanı Kaan Polat, fazla mesai kayıtlarının üç ekipte iş planlarıyla uyuşmadığını belirtiyor. Ücretler birkaç gün içinde ödenecek.",
          "Kaan Polat", "bordro uzmanı", [
              S("Kayıtları ve yasal süreleri koruyarak şüpheli girişleri acil doğrulayın.", "Otoriter", -2, 4, 8, "Ödeme doğruluğu arttı; bordro ekibine ek iş çıktı."),
              S("Kaan ve ekip yöneticileriyle farkların kaynağını birlikte inceleyin.", "Demokratik", 4, -3, 8, "Eksik bilgiler tamamlandı; süreç yetişmekte zorlandı."),
              S("Kaan'a aylık erken fark uyarısı hazırlatın.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; bu ayın kayıtları ayrıca kontrol edildi."),
              S("Ödemeyi kapatıp farkları gelecek ay düzeltin.", "Kaçınmacı", -5, 5, -10, "Ödeme zamanında çıktı; yanlış ödeme riski taşındı."),
          ]),
        V("ik-05",
          "Elif Demir, performans görüşmelerinde bir yöneticinin tüm çalışanlara aynı puanı verdiğini görüyor. Yönetici ayrıntılı gerekçe hazırlamanın ekipte tartışma yaratacağını söylüyor.",
          "Elif Demir", "İK iş ortağı", [
              S("Gerekçesiz puanları iade edip kanıtlı değerlendirme isteyin.", "Otoriter", -3, 3, 9, "Süreç tutarlılaştı; yönetici ek iş yükü gördü."),
              S("Elif ve yöneticiyle örnekleri kalibre ederek gerekçeleri oluşturun.", "Demokratik", 4, -3, 8, "Değerlendirmeler netleşti; toplantılar uzadı."),
              S("Yöneticiye zor geri bildirim konuşması için koçluk verin.", "Koçvari", 6, 1, 6, "Yönetici daha hazırlandı; puanların yeniden çalışılması sürdü."),
              S("Takvim yetişsin diye aynı puanları onaylayın.", "Kaçınmacı", -5, 5, -10, "Süreç kapandı; gelişim geri bildirimi zayıf kaldı."),
          ]),
        V("ik-06",
          "Zeynep Aydın, bir çalışanın onaylı izninin vardiya planına yansımadığını bildiriyor. Yönetici açığı kapatacak çalışan bulamadığını söylüyor.",
          "Zeynep Aydın", "İK uzmanı", [
              S("Onaylı izni koruyup vardiya açığı için alternatif görev planı isteyin.", "Otoriter", -2, -3, 9, "Çalışanın hakkı korundu; vardiya kapasitesi daraldı."),
              S("Zeynep ve yöneticiyle görevleri yeniden önceliklendirin.", "Demokratik", 4, -3, 8, "Plan dengelendi; bazı işler ertelendi."),
              S("Yöneticiye izin-çizelge kontrolü kurması için destek verin.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; bugünkü açığın çözümü ayrıca gerekti."),
              S("Çalışandan iznini kendisinin ertelemesini isteyin.", "Kaçınmacı", -6, 4, -10, "Vardiya doldu; adalet ve güven sorunu oluştu."),
          ]),
        V("ik-07",
          "Ayşe Yıldız, adaya gönderilen teklifte maaşın yanlış yazıldığını fark etti. Aday kabul etmeye hazır; doğru tutar daha düşük.",
          "Ayşe Yıldız", "işe alım uzmanı", [
              S("Yanlış teklifi durdurup yazılı düzeltmeyi gerekçesiyle iletin.", "Otoriter", -3, -4, 10, "Şeffaflık sağlandı; aday teklifi yeniden değerlendirdi."),
              S("Ayşe ve ücret ekibiyle aday için onaylı seçenekleri araştırın.", "Demokratik", 4, -3, 8, "Alternatif değerlendirildi; yanıt süresi uzadı."),
              S("Ayşe'ye tekliflerin ikinci kontrolünü kurdurun ve görüşmeyi destekleyin.", "Koçvari", 5, 1, 5, "Süreç iyileşti; mevcut aday için zor konuşma hâlâ gerekli."),
              S("Aday başladıktan sonra hatayı düzeltmeyi planlayın.", "Kaçınmacı", -6, 5, -12, "İşe alım ilerledi; güveni zedeleyecek hata saklandı."),
          ]),
        V("ik-08",
          "Çıkış görüşmelerinde aynı ekipten dört kişi eğitim eksikliğini dile getirdi. Eğitim sorumlusu Merve Çelik bütçenin sınırlı olduğunu söylüyor.",
          "Merve Çelik", "eğitim sorumlusu", [
              S("Kritik beceriler için kısa zorunlu eğitim planı çıkarın.", "Otoriter", -2, 3, 7, "Açıklar hedeflendi; diğer eğitim talepleri ertelendi."),
              S("Merve ve ekip yöneticisiyle ihtiyaçları önceliklendirin.", "Demokratik", 4, -3, 8, "Bütçe odaklı kullanıldı; planlama zaman aldı."),
              S("Merve'ye iç mentorluk pilotu oluşturma alanı açın.", "Koçvari", 7, 2, 5, "Düşük maliyetli destek oluştu; mentorların yükü artabilir."),
              S("Yeni bütçeye kadar geri bildirimleri arşivleyin.", "Kaçınmacı", -5, -4, -8, "Maliyet çıkmadı; beceri açığı sürdü."),
          ]),
        V("ik-09",
          "Elif Demir, bir ekipte anonim güven puanının sert düştüğünü bildiriyor. Ekip yöneticisi sonucu birkaç memnuniyetsiz kişiye bağlıyor.",
          "Elif Demir", "İK iş ortağı", [
              S("Yöneticiden ölçülebilir eylem planı isteyip sonucu takip edin.", "Otoriter", -2, 3, 7, "Sorumluluk belirlendi; yönetici savunmaya geçti."),
              S("Elif'le gizliliği koruyan gönüllü görüşmeler düzenleyin.", "Demokratik", 4, -3, 9, "Nedenler görünür oldu; ekip zaman ayırdı."),
              S("Yöneticiye geri bildirim toplantıları için destek sunun.", "Koçvari", 7, 1, 5, "Konuşma zemini açıldı; güvenin geri gelmesi zaman alacak."),
              S("Sonraki anketi bekleyip müdahale etmeyin.", "Kaçınmacı", -5, -4, -9, "Gerilim açıkça ele alınmadı."),
          ]),
        V("ik-10",
          "Kaan Polat, bir çalışanın banka hesabı değişikliğinin yalnızca e-postayla bildirildiğini fark etti. Bordro kapanışı bugün.",
          "Kaan Polat", "bordro uzmanı", [
              S("Kimlik doğrulaması bitene kadar hesap değişikliğini işlemeyin.", "Otoriter", -2, -3, 10, "Yanlış ödeme riski azaldı; çalışanla hızla iletişim gerekti."),
              S("Kaan ve çalışanla onaylı doğrulama kanalını uygulayın.", "Demokratik", 4, -2, 8, "Kayıt doğrulandı; kapanış süresi daraldı."),
              S("Kaan'a güvenli hesap değişikliği kontrolü hazırlatın.", "Koçvari", 5, 1, 5, "Gelecek risk azaldı; bu değişiklik ayrıca teyit edildi."),
              S("E-postadaki bilgiyi doğrudan bordroya işleyin.", "Kaçınmacı", -3, 5, -11, "Bordro yetişti; hesap doğruluğu belirsiz kaldı."),
          ]),
        V("ik-11",
          "Merve Çelik, oryantasyon içeriğinin mağaza çalışanlarının fiilî görevlerinden geri kaldığını söylüyor. Yeni grup pazartesi başlayacak.",
          "Merve Çelik", "eğitim sorumlusu", [
              S("Kritik süreçleri güncelleyip diğer içeriği sonraki sürüme bırakın.", "Otoriter", -2, 5, 6, "Yeni grup kritik bilgiyi aldı; içerik bütünü tamamlanmadı."),
              S("Merve ve mağaza yöneticileriyle ilk hafta için doğru görev listesini belirleyin.", "Demokratik", 4, -2, 8, "İçerik sahaya uydu; hazırlık sıkıştı."),
              S("Merve'ye çalışan geri bildirimiyle canlı güncelleme pilotu verin.", "Koçvari", 6, 1, 5, "Öğrenme başladı; ilk grup bazı değişiklikleri sahada görecek."),
              S("Mevcut içeriği kullanıp güncellemeyi sonraki gruba bırakın.", "Kaçınmacı", -4, 3, -8, "Başlangıç aksamadı; görev uyumsuzluğu sürdü."),
          ]),
        V("ik-12",
          "Bir yönetici, düşük performans gösteren çalışanı hakkında yalnızca sözlü geri bildirim verdiğini söylüyor. Elif Demir, yakında resmî karar istenebileceğini belirtiyor.",
          "Elif Demir", "İK iş ortağı", [
              S("Belgelenmemiş değerlendirmeyle işlem yapmayıp adil geri bildirim planı isteyin.", "Otoriter", -2, -3, 9, "Usul korundu; karar süresi uzadı."),
              S("Elif ve yöneticiyle somut hedefler ve destek süresi oluşturun.", "Demokratik", 4, -3, 8, "Beklenti netleşti; ek takip gerekti."),
              S("Yöneticiyi kanıta dayalı gelişim görüşmesine hazırlayın.", "Koçvari", 6, 1, 5, "Çalışana gelişim fırsatı oluştu; sonuç için süre lazım."),
              S("Sözlü anlatımı yeterli sayıp hızlı resmî işlem başlatın.", "Kaçınmacı", -6, 5, -11, "Karar hızlandı; adalet ve süreç riski yükseldi."),
          ]),
        V("ik-13",
          "Ayşe Yıldız, adayların aynı pozisyonda farklı mülakat sorularıyla değerlendirildiğini fark etti. Yöneticiler kendi sorularını korumak istiyor.",
          "Ayşe Yıldız", "işe alım uzmanı", [
              S("Temel yetkinlik sorularını standartlaştırıp ek sorulara sınırlı alan bırakın.", "Otoriter", -2, 4, 8, "Karşılaştırma kolaylaştı; yöneticiler esneklik kaybı hissetti."),
              S("Ayşe ve yöneticilerle ortak değerlendirme kriterleri belirleyin.", "Demokratik", 4, -3, 8, "Süreç sahiplenildi; uyum toplantısı uzadı."),
              S("Ayşe'ye yapılandırılmış mülakat pilotu yönettirin.", "Koçvari", 6, 1, 5, "Ölçüm gelişti; tüm pozisyonlara yayılmadı."),
              S("Yöneticilerin yöntemi farklı olabilir diyerek müdahale etmeyin.", "Kaçınmacı", -4, 2, -9, "İşe alım hızlı kaldı; aday karşılaştırması zayıfladı."),
          ]),
        V("ik-14",
          "Zeynep Aydın, izin ve fazla mesai taleplerinin bazı ekiplerde yöneticinin kişisel mesajlarıyla yönetildiğini söylüyor. Kayıtlar eksik.",
          "Zeynep Aydın", "İK uzmanı", [
              S("Onaylı sistem dışındaki yeni işlemleri durdurup kayıtları doğrulatın.", "Otoriter", -3, -2, 9, "İzlenebilirlik arttı; eski kayıtların toplanması yük getirdi."),
              S("Zeynep ve yöneticilerle kullanım engellerini belirleyin.", "Demokratik", 4, -2, 8, "Geçiş için gerçek sorunlar görüldü; uygulama uzadı."),
              S("Zeynep'e kısa sistem eğitimi ve takip pilotu verin.", "Koçvari", 6, 1, 5, "Kullanım iyileşti; geçmiş kayıtların düzeltilmesi sürdü."),
              S("Mesaj kayıtları var diye sistemi kullanmalarını istemeyin.", "Kaçınmacı", -4, 3, -10, "Anlık kolaylık sürdü; resmî kayıt eksiği kaldı."),
          ]),
        V("ik-15",
          "Bir çalışanın sağlıkla ilgili hassas bilgisinin ekip sohbetinde paylaşıldığı iddia edildi. Elif Demir, bilginin kimden çıktığını henüz bilmiyor.",
          "Elif Demir", "İK iş ortağı", [
              S("Paylaşımı durdurup gizlilik prosedürüne göre sınırlı inceleme açın.", "Otoriter", -2, -3, 10, "Yayılım sınırlandı; iddia dikkatle araştırılacak."),
              S("Elif'le etkilenen çalışanın ihtiyaçlarını güvenli biçimde görüşün.", "Demokratik", 4, -3, 9, "Çalışana destek sağlandı; inceleme sürüyor."),
              S("Ekibe kişisel veri farkındalığını kimseyi ifşa etmeden yeniden anlatın.", "Koçvari", 5, 1, 6, "Farkındalık arttı; özgül olay ayrıca incelenmeli."),
              S("Somut şikâyet gelene kadar olayı açmayın.", "Kaçınmacı", -6, 3, -11, "Yayılım devam edebilir; çalışan güveni zedelendi."),
          ]),
        V("ik-16",
          "Eğitim sorumlusu Merve Çelik, zorunlu güvenlik eğitimine katılımın %72'de kaldığını bildiriyor. Yoğun mağazalar çalışanlarını eğitime ayıramadıklarını söylüyor.",
          "Merve Çelik", "eğitim sorumlusu", [
              S("Kalan katılım için vardiya bazlı zorunlu takvim belirleyin.", "Otoriter", -3, 3, 8, "Katılım yükseldi; bazı vardiyalar sıkıştı."),
              S("Merve ve mağaza yöneticileriyle kısa oturum saatleri oluşturun.", "Demokratik", 4, -2, 8, "Katılım planı kabul gördü; koordinasyon gerekti."),
              S("Merve'ye mikro eğitim pilotu ve tamamlama takibi hazırlatın.", "Koçvari", 6, 1, 5, "Erişim kolaylaştı; kalan çalışanlar takip edilmeli."),
              S("Sezon yoğunluğu geçene kadar eğitimi erteleyin.", "Kaçınmacı", -4, 4, -10, "Operasyon rahatladı; eğitim açığı sürdü."),
          ]),
        V("ik-17",
          "İşe alım ekibi bir pozisyonu hızlı doldurdu; Ayşe Yıldız, adayın görev beklentisinin ilan metninden farklı olduğunu görüşmede fark etti.",
          "Ayşe Yıldız", "işe alım uzmanı", [
              S("Teklifi vermeden görev tanımını yazılı netleştirin.", "Otoriter", -2, -3, 8, "Yanlış beklenti önlendi; teklif gecikti."),
              S("Ayşe ve yöneticiyle görevin gerçek kapsamını adaya birlikte anlatın.", "Demokratik", 4, -2, 8, "Aday bilinçli karar verebildi; görüşme uzadı."),
              S("Ayşe'ye ilan metinlerinin sahayla doğrulanması için kontrol kurdurun.", "Koçvari", 6, 1, 5, "Gelecek ilanlar iyileşti; bu adayla ayrıca konuşulmalı."),
              S("Aday işe başlayınca görevi öğrenir diyerek teklif verin.", "Kaçınmacı", -4, 5, -9, "Pozisyon doldu; erken ayrılma riski arttı."),
          ]),
        V("ik-18",
          "Zeynep Aydın, bir ekipte iki çalışanın aynı izin tarihini önceden sözlü olarak onaylattığını söylüyor. Sistemde ise yalnızca birinin kaydı var.",
          "Zeynep Aydın", "İK uzmanı", [
              S("Kayıt ve önceki onayları doğrulayıp gerekçeli karar verin.", "Otoriter", -2, 3, 8, "Karar belgeli verildi; bir çalışan hayal kırıklığı yaşadı."),
              S("Zeynep ve ekiple alternatif tarih veya geçici destek görüşün.", "Demokratik", 4, -2, 8, "Seçenekler görüldü; planlama uzadı."),
              S("Yöneticiye sözlü onayların sisteme işlenmesi için destek verin.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; bugünkü çakışma ayrıca çözüldü."),
              S("Kayıtlı olanı onaylayıp diğerine açıklama yapmayın.", "Kaçınmacı", -5, 5, -10, "Vardiya planlandı; adalet algısı bozuldu."),
          ]),
        V("ik-19",
          "Elif Demir, yüksek performanslı bir çalışanın başka firmadan teklif aldığını duydu. Çalışan henüz yöneticisine söylemedi; maaş tek neden olmayabilir.",
          "Elif Demir", "İK iş ortağı", [
              S("Çalışana doğrudan koşulsuz kalma teklifi vermeden önce resmî süreçleri izleyin.", "Otoriter", -2, 2, 6, "Tutarlılık korundu; çalışan kişisel ilgi bekledi."),
              S("Elif'le çalışanın beklentisini gönüllü görüşmede dinleyin.", "Demokratik", 5, -2, 8, "Gerçek nedenler ortaya çıktı; çözüm hemen oluşmadı."),
              S("Çalışanla gelişim ve sorumluluk seçeneklerini konuşun.", "Koçvari", 7, 1, 5, "Gelecek yolu görünür oldu; her beklenti karşılanamayabilir."),
              S("Kararını kendi verir diye hiç konuşmayın.", "Kaçınmacı", -5, -4, -8, "Baskı yapılmadı; elde tutma fırsatı kaçtı."),
          ]),
        V("ik-20",
          "Kaan Polat, yasal kesintileri etkileyen bir bordro kuralının sistem güncellemesinde değiştiğini fark etti. Ön inceleme yalnızca küçük bir çalışan grubunu gösteriyor.",
          "Kaan Polat", "bordro uzmanı", [
              S("Etkilenen ödemeleri kontrol edip doğrulanana kadar ilgili bordroyu bekletin.", "Otoriter", -2, -4, 10, "Yanlış ödeme önlendi; bazı bordrolar gecikti."),
              S("Kaan ve sistem ekibiyle kapsamı belirleyip çalışan iletişimi hazırlayın.", "Demokratik", 4, -2, 8, "Etkilenenler doğru bilgilendirildi; inceleme sürdü."),
              S("Kaan'a güncelleme sonrası test listesini kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski düştü; mevcut fark ayrıca düzeltilecek."),
              S("Küçük grubu gelecek ay düzeltmek üzere bu ay işlemi tamamlayın.", "Kaçınmacı", -5, 5, -11, "Bordro yetişti; çalışan hakları riske girdi."),
          ]),
    ],

    "Pazarlama": [
        V("paz-01",
          "Marka yöneticisi Selin Kaya, kampanya görselindeki fiyatın satış ekibinin onayladığı fiyattan farklı olduğunu lansmana iki saat kala fark etti.",
          "Selin Kaya", "marka yöneticisi", [
              S("Yanlış görseli durdurup doğru fiyatlı sürümü onaydan geçirin.", "Otoriter", -2, -3, 9, "Yanlış bilgilendirme önlendi; lansman kısmen gecikti."),
              S("Selin ve satış ekibiyle etkilenen kanalları birlikte önceliklendirin.", "Demokratik", 4, -2, 8, "Kanallar tutarlılaştı; koordinasyon zaman aldı."),
              S("Selin'e yayın öncesi fiyat kontrolü kurdurun.", "Koçvari", 5, 1, 5, "Yeni kontrol oluştu; ilk görsel yine değiştirilmek zorunda."),
              S("Müşteri fark ederse düzeltiriz diyerek yayına girin.", "Kaçınmacı", -3, 5, -11, "Lansman zamanında oldu; yanlış vaat yayıldı."),
          ]),
        V("paz-02",
          "Sosyal medya editörü Ece Arslan, iş birliği yapılan içerik üreticisinin tartışmalı paylaşımında marka etiketinin yer aldığını bildiriyor. Kampanya yarın başlayacak.",
          "Ece Arslan", "sosyal medya editörü", [
              S("Sözleşme riskini inceleyip planlı yayını geçici durdurun.", "Otoriter", -2, -4, 8, "Risk sınırlandı; alternatif içerik ihtiyacı doğdu."),
              S("Ece, hukuk ve iletişimle koşullara uygun ortak yanıt hazırlayın.", "Demokratik", 4, -2, 8, "Yanıt tutarlı oldu; karar biraz gecikti."),
              S("Ece'ye yedek içerik ve izleme planını yönettirin.", "Koçvari", 5, 1, 5, "Ekip hazırlandı; iş birliğinin geleceği ayrıca kararlaştırılacak."),
              S("Gündem geçer diye kampanyayı değiştirmeyin.", "Kaçınmacı", -4, 5, -10, "Takvim korundu; marka bağlantısı sorgulandı."),
          ]),
        V("paz-03",
          "Dijital uzman Can Öztürk, reklam bütçesinin yarısı harcanmasına rağmen dönüşümün hedefin altında kaldığını bildiriyor. Kampanya ekibi görünürlüğün güçlü olduğunu savunuyor.",
          "Can Öztürk", "dijital pazarlama uzmanı", [
              S("Düşük dönüşümlü grupları durdurup kalan bütçeyi koruyun.", "Otoriter", -2, 4, 6, "Bütçe kaybı azaldı; erişim düştü."),
              S("Can ve kampanya ekibiyle satış, erişim ve marka hedeflerini ayrıştırın.", "Demokratik", 4, -2, 8, "Başarı ölçütü netleşti; değişiklik gecikti."),
              S("Can'a küçük yaratıcı testlerle yeni hedefleme fırsatı verin.", "Koçvari", 5, 1, 5, "Öğrenme oluştu; test bütçesi gerekti."),
              S("Sonuç toparlar diye kampanyayı aynı şekilde sürdürün.", "Kaçınmacı", -3, -4, -9, "Görünürlük devam etti; dönüşüm sorunu sürdü."),
          ]),
        V("paz-04",
          "Tasarım uzmanı Elif Demir, kampanya ana görselini teslim edemediğini söylüyor. Nedeni son üç günde gelen birbiriyle çelişen iki yönetici revizyonu.",
          "Elif Demir", "tasarım uzmanı", [
              S("Tek nihai onay merciini belirleyip sade görselle lansmanı koruyun.", "Otoriter", -3, 5, 6, "Lansman ilerledi; bazı yaratıcı beklentiler karşılanmadı."),
              S("Elif ve yöneticilerle tek yaratıcı brif üzerinde uzlaşın.", "Demokratik", 4, -3, 8, "Çelişki kalktı; toplantı üretim zamanını azalttı."),
              S("Elif'e uygulanabilir iki versiyon geliştirme alanı verin.", "Koçvari", 6, 1, 5, "Elif çözüm üretti; son seçimi yine yönetim yapacak."),
              S("Yeni revizyon gelir diye karar vermeden bekleyin.", "Kaçınmacı", -5, -6, -9, "Kimseyle çatışılmadı; teslim daha da gecikti."),
          ]),
        V("paz-05",
          "Yerel kampanya afişindeki mesajın bir şehirde yanlış anlaşıldığı bildirildi. Selin Kaya, tüm ülke kampanyasını durdurmanın aşırı tepki olabileceğini düşünüyor.",
          "Selin Kaya", "marka yöneticisi", [
              S("Etkilenen bölgede görseli durdurup incelemeyi başlatın.", "Otoriter", -2, -2, 8, "Bölgesel risk sınırlandı; ulusal takvim korundu."),
              S("Selin ve yerel ekiplerle mesajın nasıl algılandığını doğrulayın.", "Demokratik", 4, -2, 8, "Geri bildirim anlaşıldı; düzeltme zamanı uzadı."),
              S("Selin'e sonraki kampanyalar için bölgesel ön test kurdurun.", "Koçvari", 5, 1, 5, "Önleyici adım oluştu; mevcut görsel ayrıca yönetildi."),
              S("Tepki az diye hiçbir değişiklik yapmayın.", "Kaçınmacı", -3, 4, -10, "Kampanya sürdü; yanlış anlaşılma büyüyebilir."),
          ]),
        V("paz-06",
          "Ece Arslan, sosyal medyada ürün stokta olmadığı hâlde reklamın gösterilmeye devam ettiğini fark etti. Reklam iyi performans gösteriyor.",
          "Ece Arslan", "sosyal medya editörü", [
              S("Stoksuz ürün reklamını durdurup benzer stoklu ürüne yönlendirin.", "Otoriter", -2, 2, 8, "Yanlış beklenti azaldı; performans verisi yeniden başlayacak."),
              S("Ece ve tedarikle bölgesel stok durumuna göre yayını sınırlandırın.", "Demokratik", 4, -2, 8, "Reklam kısmen sürdü; stok takibi yoğunlaştı."),
              S("Ece'ye stok sinyaliyle reklam uyarısı kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; mevcut yayın ayrıca ayarlandı."),
              S("Talep toplar diye reklamı stok gelene kadar sürdürün.", "Kaçınmacı", -3, 5, -10, "Tıklama arttı; müşteri hayal kırıklığı oluştu."),
          ]),
        V("paz-07",
          "Can Öztürk, e-posta kampanyasının yanlış müşteri segmentine gittiğini söylüyor. Mesaj kişisel bilgi içermiyor ama alıcılar teklifin kendilerine özel olduğunu düşünüyor.",
          "Can Öztürk", "dijital pazarlama uzmanı", [
              S("Yeni gönderimi durdurup teklif koşullarını açık düzeltmeyle belirtin.", "Otoriter", -2, -2, 8, "Yanlış beklenti azaltıldı; ek iletişim gerekti."),
              S("Can ve müşteri ekibiyle etkilenen alıcılara adil seçenek belirleyin.", "Demokratik", 4, -2, 8, "Müşteri tepkisi dengelendi; maliyet oluşabilir."),
              S("Can'a segment onayında çift kontrol süreci kurdurun.", "Koçvari", 5, 1, 5, "Yeni hata önlenecek; mevcut müşteriler ayrıca bilgilendirildi."),
              S("Şikâyet gelmezse düzeltme yapmayın.", "Kaçınmacı", -3, 4, -10, "Ek iletişim olmadı; teklif algısı belirsiz kaldı."),
          ]),
        V("paz-08",
          "Elif Demir, yeni koleksiyon sloganının rakibin eski sloganına benzediğini fark etti. Üretim dosyaları matbaaya gönderilmek üzere.",
          "Elif Demir", "tasarım uzmanı", [
              S("Matbaa onayını durdurup marka ve hukuk incelemesi isteyin.", "Otoriter", -2, -4, 9, "Risk değerlendirildi; baskı takvimi daraldı."),
              S("Elif ve yaratıcı ekiple özgün alternatifleri hemen karşılaştırın.", "Demokratik", 4, -2, 8, "Alternatif çıktı; ek tasarım zamanı gerekti."),
              S("Elif'e özgünlük kontrol adımı geliştirme sorumluluğu verin.", "Koçvari", 5, 1, 5, "Süreç gelişti; slogan için bugün ayrıca karar verildi."),
              S("Slogan eski olduğu için benzerliği görmezden gelin.", "Kaçınmacı", -3, 5, -10, "Baskı yetişti; itibar ve hak riski kaldı."),
          ]),
        V("paz-09",
          "Selin Kaya, mağazalardaki kampanya başlangıç tarihiyle dijital reklamdaki tarihin bir gün farklı olduğunu bildiriyor. Reklam yayına girmiş.",
          "Selin Kaya", "marka yöneticisi", [
              S("Doğru takvimi teyit edip yanlış tarihli yayını durdurun.", "Otoriter", -2, 3, 8, "Yanlış bilgilendirme durdu; reklam teslimleri aksadı."),
              S("Selin ve mağazacılıkla müşteri beklentisine uygun düzeltme belirleyin.", "Demokratik", 4, -2, 8, "Kanallar tutarlılaştı; koordinasyon zaman aldı."),
              S("Selin'e kampanya tarihleri için tek kaynak kontrolü kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski düştü; bugünkü reklam ayrıca düzeltildi."),
              S("Mağazalar sorulursa açıklar diye reklamı değiştirmeyin.", "Kaçınmacı", -3, 4, -10, "Reklam sürdü; mağazada itiraz arttı."),
          ]),
        V("paz-10",
          "Ece Arslan, müşteri yorumlarına farklı çalışanların birbiriyle çelişen yanıtlar verdiğini fark etti. Bazı yanıtlar iade süresi hakkında yanlış bilgi içeriyor.",
          "Ece Arslan", "sosyal medya editörü", [
              S("Yanlış yanıtları düzeltip geçici onaylı yanıt rehberi yayımlayın.", "Otoriter", -2, 3, 8, "Bilgi tutarlılaştı; editör özerkliği azaldı."),
              S("Ece ve müşteri ekibiyle doğru uygulama örneklerini hazırlayın.", "Demokratik", 4, -2, 8, "Yanıtlar sahaya uydu; süreç biraz yavaşladı."),
              S("Ece'ye örnek yorumlar üzerinde eğitim pilotu yürütün.", "Koçvari", 6, 1, 5, "Ekip gelişti; eski yanlış yanıtlar ayrıca düzeltildi."),
              S("Yanıtlar eski tarihte kaldı diye düzeltmeyin.", "Kaçınmacı", -3, 4, -10, "Ek iş çıkmadı; müşteriler yanlış bilgi görmeye devam etti."),
          ]),
        V("paz-11",
          "Can Öztürk, mobil reklamda yüksek tıklama fakat düşük satış görüyor. Ürün sayfasının yüklenme süresi 8 saniyeye çıkmış.",
          "Can Öztürk", "dijital pazarlama uzmanı", [
              S("Sorunlu sayfaya giden reklamı sınırlayıp teknik öncelik açın.", "Otoriter", -2, 2, 8, "Bütçe korundu; erişim azaldı."),
              S("Can ve e-ticaret ekibiyle teknik sorun ile hedefleme etkisini ayırın.", "Demokratik", 4, -2, 8, "Gerçek neden netleşti; analiz zaman aldı."),
              S("Can'a yüklenme hızı uyarısı içeren kampanya paneli hazırlatın.", "Koçvari", 5, 1, 5, "Gelecek kayıplar erken görülecek; mevcut sayfa ayrıca düzeltilecek."),
              S("Tıklama iyi diye reklamı aynı bütçeyle sürdürün.", "Kaçınmacı", -3, -4, -10, "Görünürlük sürdü; satış kaybı arttı."),
          ]),
        V("paz-12",
          "Elif Demir'in hazırladığı ürüne ait görsel, gerçek kumaş rengini olduğundan daha açık gösteriyor. Kampanya yerleşimleri onaylanmış.",
          "Elif Demir", "tasarım uzmanı", [
              S("Yanlış görseli durdurup ürünle doğrulanmış sürümü isteyin.", "Otoriter", -2, -3, 8, "Yanıltıcı sunum önlendi; yerleşimler değişti."),
              S("Elif ve ürün ekibiyle ışık ve renk farkını örnek üzerinden değerlendirin.", "Demokratik", 4, -2, 8, "Düzeltme kanıta dayandı; baskı zamanı kısaldı."),
              S("Elif'e ürün-fotoğraf doğrulama kontrolü kurdurun.", "Koçvari", 5, 1, 5, "Kalite arttı; bugünkü görsel ayrıca yenilendi."),
              S("Ekranlar değişken diye görseli olduğu gibi bırakın.", "Kaçınmacı", -3, 4, -10, "Yayın sürdü; ürün beklentisi bozulabilir."),
          ]),
        V("paz-13",
          "Selin Kaya, rakibin benzer kampanyayı bir hafta önce başlattığını bildiriyor. Sizin kampanyanızın gücü daha geniş beden seçeneği, ancak bu mesaj henüz görsellerde yok.",
          "Selin Kaya", "marka yöneticisi", [
              S("Ana mesajı beden çeşitliliğine çevirip mevcut takvimi koruyun.", "Otoriter", -2, 4, 6, "Farklılaşma arttı; son dakika revizyon gerekti."),
              S("Selin ve ekiple müşteri için gerçek farkları yeniden seçin.", "Demokratik", 4, -2, 8, "Mesaj güçlendi; yayın biraz gecikti."),
              S("Selin'e kısa müşteri testi yaptırıp en anlaşılır mesajı seçin.", "Koçvari", 5, 1, 5, "Öğrenme sağlandı; test bütçesi kullanıldı."),
              S("Rakip benzer diye hiçbir açıklama yapmadan kampanyayı erteleyin.", "Kaçınmacı", -4, -5, -8, "Benzerlik baskısı azaldı; fırsat penceresi daraldı."),
          ]),
        V("paz-14",
          "Ece Arslan, kampanya etiketinin kullanıcılar tarafından farklı bir anlamda kullanılmaya başladığını fark etti. Marka etiketi hâlâ reklamlarda yer alıyor.",
          "Ece Arslan", "sosyal medya editörü", [
              S("Ücretli reklamlardaki etiketi durdurup izlemeyi sürdürün.", "Otoriter", -2, -2, 8, "Marka ilişkilendirmesi azaldı; kampanya ölçümü değişti."),
              S("Ece ve iletişim ekibiyle bağlama uygun yanıt ihtiyacını tartışın.", "Demokratik", 4, -2, 8, "Gereksiz tepki önlendi; karar zaman aldı."),
              S("Ece'ye alternatif etiket ve topluluk izlemesi hazırlatın.", "Koçvari", 5, 1, 5, "Alternatif oluştu; mevcut içerikler ayrı değerlendirildi."),
              S("Etiket görünürlük getiriyor diye aynı şekilde kullanın.", "Kaçınmacı", -3, 4, -10, "Erişim sürdü; mesaj üzerindeki kontrol azaldı."),
          ]),
        V("paz-15",
          "Can Öztürk, iki reklam kanalının aynı satışı kendine yazdığını söylüyor. Üst yönetime performans raporu yarın sunulacak.",
          "Can Öztürk", "dijital pazarlama uzmanı", [
              S("Kesin olmayan dönüşüm toplamını rapordan çıkarıp not düşerek sunun.", "Otoriter", -2, 2, 9, "Rapor dürüst kaldı; sonuçlar daha düşük göründü."),
              S("Can ve analitik ekibiyle örtüşmeyi hesaplayıp aralık belirtin.", "Demokratik", 4, -2, 8, "Belirsizlik açıklandı; analiz geceye uzadı."),
              S("Can'a tekil satış ölçümü için kalıcı model hazırlatın.", "Koçvari", 5, 1, 5, "Gelecek raporlar iyileşecek; yarınki rakam yaklaşık kaldı."),
              S("İki kanalın toplamını doğru kabul edip yüksek performans sunun.", "Kaçınmacı", -3, 5, -11, "Rapor etkileyici oldu; sonuç şişirildi."),
          ]),
        V("paz-16",
          "Elif Demir, çocuk kampanyası görselinde kullanılan görselin kullanım izninin yalnızca dijital kanalı kapsadığını fark etti. Mağaza baskısı bugün başlıyor.",
          "Elif Demir", "tasarım uzmanı", [
              S("Baskıyı durdurup izin kapsamına uygun görsel seçin.", "Otoriter", -2, -4, 10, "Hak riski önlendi; baskı takvimi kaydı."),
              S("Elif ve hukukla genişletme izni veya alternatif görseli görüşün.", "Demokratik", 4, -2, 8, "Seçenekler netleşti; üretime geçiş uzadı."),
              S("Elif'e kanal bazlı kullanım hakkı kontrolü kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski düştü; bugün alternatif gerekli."),
              S("İzin sonra alınır diye mağaza baskısına devam edin.", "Kaçınmacı", -3, 5, -11, "Baskı yetişti; kullanım hakkı riski oluştu."),
          ]),
        V("paz-17",
          "Selin Kaya, mağazaların kullandığı kampanya metninin dijital metinden daha geniş indirim sözü verdiğini bildiriyor.",
          "Selin Kaya", "marka yöneticisi", [
              S("Onaylı koşullar dışındaki metni hemen değiştirin.", "Otoriter", -2, 3, 8, "Vaatler tutarlılaştı; materyal değişimi gerekti."),
              S("Selin ve mağazalarla müşteriye verilecek geçiş açıklamasını belirleyin.", "Demokratik", 4, -2, 8, "Müşteri iletişimi netleşti; koordinasyon uzadı."),
              S("Selin'e tek kampanya metni kaynağı oluşturma görevi verin.", "Koçvari", 5, 1, 5, "Tekrar riski düştü; eski materyal ayrıca toplandı."),
              S("Mağazalar satış yapıyor diye farkı görmezden gelin.", "Kaçınmacı", -3, 4, -10, "Satış sürdü; yanlış vaat riski büyüdü."),
          ]),
        V("paz-18",
          "Ece Arslan, müşterinin ürün şikâyetine verilen yanıtta müşterinin sipariş numarasının herkese açık yazıldığını gördü.",
          "Ece Arslan", "sosyal medya editörü", [
              S("Yanıtı kaldırıp olayı veri güvenliği sürecine bildirin.", "Otoriter", -2, -2, 10, "Görünürlük durdu; olay kayıt altına alındı."),
              S("Ece ve gizlilik ekibiyle müşteriye uygun kanaldan ulaşın.", "Demokratik", 4, -2, 8, "Müşteri bilgilendirildi; inceleme emek istedi."),
              S("Ece'ye güvenli yanıt örnekleriyle kısa eğitim hazırlatın.", "Koçvari", 5, 1, 5, "Ekip öğrenme sağladı; mevcut olay ayrıca takip edilmeli."),
              S("Numara tek başına zararsızdır diye yanıtı bırakın.", "Kaçınmacı", -3, 4, -11, "Ek işlem olmadı; veri paylaşımı sürdü."),
          ]),
        V("paz-19",
          "Can Öztürk, kampanya bağlantısının bazı telefonlarda boş sayfa açtığını söylüyor. Masaüstü performansı güçlü.",
          "Can Öztürk", "dijital pazarlama uzmanı", [
              S("Etkilenen mobil reklamları durdurup çalışan bağlantıya yönlendirin.", "Otoriter", -2, 2, 8, "Mobil kayıp azaldı; kanal erişimi düştü."),
              S("Can ve IT ile hangi cihazların etkilendiğini doğrulayın.", "Demokratik", 4, -2, 8, "Hedefli düzeltme yapıldı; analiz zaman aldı."),
              S("Can'a cihaz bazlı yayın kontrolü ekletin.", "Koçvari", 5, 1, 5, "Gelecek hata erken görülecek; bugünkü bağlantı ayrıca onarıldı."),
              S("Masaüstü çalışıyor diye reklamı değiştirmeyin.", "Kaçınmacı", -3, -4, -10, "Masaüstü satışları sürdü; mobil bütçe boşa aktı."),
          ]),
        V("paz-20",
          "Elif Demir, kampanya mesajındaki çevresel fayda ifadesinin ölçülebilir dayanağını bulamadığını bildiriyor. Lansman yarın.",
          "Elif Demir", "tasarım uzmanı", [
              S("Dayanağı olmayan ifadeyi çıkarıp doğrulanabilir bilgiyle değiştirin.", "Otoriter", -2, -3, 10, "Yanıltıcı iddia riski azaldı; görseller değişti."),
              S("Elif ve sürdürülebilirlik ekibiyle kanıtlanan kısmı belirleyin.", "Demokratik", 4, -2, 8, "Mesaj güçlendi; çalışma süresi uzadı."),
              S("Elif'e iddia doğrulama kontrolü hazırlatın.", "Koçvari", 5, 1, 5, "Gelecek kampanyalar iyileşti; yarınki metin ayrıca düzeltildi."),
              S("İfade genel diye kanıt aramadan yayımlayın.", "Kaçınmacı", -3, 5, -11, "Lansman yetişti; güven ve uyum riski doğdu."),
          ]),
    ],

    "Finans": [
        V("fin-01",
          "Finansal analist Ece Arslan, yönetim sunumundan bir gün önce aylık raporda önemli bir hesaplama hatası buldu. Düzeltme sonucu kârlılık önceki taslağa göre düşük görünecek.",
          "Ece Arslan", "finansal analist", [
              S("Raporu düzeltip değişikliğin etkisini sunum öncesi yönetime bildirin.", "Otoriter", -2, 3, 10, "Yönetim doğru veriyi gördü; son dakika değişiklik güven sorusu doğurdu."),
              S("Ece ve ilgili ekiplerle hatanın kapsamını teyit edip revizyon notu ekleyin.", "Demokratik", 4, -3, 9, "Düzeltme sağlam temele oturdu; hazırlık uzadı."),
              S("Ece'ye hata kaynağı ve sonraki kontrol adımı için çalışma yaptırın.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; bu sunum ayrıca revize edildi."),
              S("Fark sonraki ay dengelenir diye eski raporu sunun.", "Kaçınmacı", -3, 5, -12, "Sunum değişmedi; karar vericiler yanlış rakam gördü."),
          ]),
        V("fin-02",
          "Bütçe sorumlusu Kaan Polat, pazarlama harcamasının planı %40 aştığını söylüyor. Harcama devam ederse kampanya tamamlanabilir; durdurulursa yapılan yatırımın getirisi düşebilir.",
          "Kaan Polat", "bütçe planlama sorumlusu", [
              S("Yeni harcamaya onay vermeden ölçülebilir getiri ve yetki dosyası isteyin.", "Otoriter", -2, 3, 8, "Bütçe disiplini korundu; kampanya kısa süre yavaşladı."),
              S("Kaan ve pazarlamayla kalan yatırımın getirisine göre aşamalı karar verin.", "Demokratik", 4, -3, 8, "Kaynak kontrollü aktarıldı; analiz zaman aldı."),
              S("Kaan'a farklı bütçe kesintisi senaryoları hazırlatın.", "Koçvari", 5, 1, 5, "Seçenekler netleşti; karar toplantısı gerekti."),
              S("Kampanya bitince bakarız diyerek tüm harcamayı onaylayın.", "Kaçınmacı", -3, 5, -11, "Kampanya sürdü; bütçe açığı büyüdü."),
          ]),
        V("fin-03",
          "Muhasebe uzmanı Ayşe Yıldız, denetime üç gün kala bazı harcamaların destekleyici belgelerinin eksik olduğunu bildiriyor. Harcamaların gerçek olduğu görülüyor, belgeler tamamlanmamış.",
          "Ayşe Yıldız", "muhasebe uzmanı", [
              S("Eksikleri dürüstçe listeleyip denetim sürecine uygun biçimde tamamlayın.", "Otoriter", -2, -3, 10, "Denetim izi korundu; ekip yoğun çalıştı."),
              S("Ayşe ve gider sahipleriyle belgelerin kaynağını tek tek doğrulayın.", "Demokratik", 4, -3, 8, "Belgeler sağlam toplandı; süreç uzadı."),
              S("Ayşe'ye ödeme öncesi belge kontrolü pilotu hazırlatın.", "Koçvari", 5, 1, 5, "Tekrar riski düştü; mevcut eksikler ayrıca ele alındı."),
              S("Sorulmadıkça eksikleri açıklamayın.", "Kaçınmacı", -3, 4, -12, "Hazırlık yükü azaldı; denetim güveni riske girdi."),
          ]),
        V("fin-04",
          "Ayşe Yıldız, aynı tedarikçiden gelen iki faturanın numaraları farklı olsa da aynı teslimata ait olabileceğini fark etti. İkinci ödemenin son onayına saatler kaldı.",
          "Ayşe Yıldız", "muhasebe uzmanı", [
              S("İkinci ödemeyi durdurup teslim ve sipariş kayıtlarını doğrulayın.", "Otoriter", -2, -2, 10, "Mükerrer ödeme riski durdu; tedarikçi yanıt bekledi."),
              S("Ayşe ve satın almayla iki faturanın farkını birlikte inceleyin.", "Demokratik", 4, -2, 8, "Sorumluluk netleşti; ödeme gecikti."),
              S("Ayşe'ye mükerrer belge taraması kurdurun.", "Koçvari", 5, 1, 5, "Sonraki risk azaldı; bugünkü işlem ayrıca teyit edildi."),
              S("Fatura numarası farklı diye ödemeyi onaylayın.", "Kaçınmacı", -3, 5, -12, "Ödeme zamanında çıktı; çift ödeme riski doğdu."),
          ]),
        V("fin-05",
          "Kaan Polat, büyük tahsilatın bir hafta gecikeceğini öğrendi. Aynı hafta ücretler ve tedarikçi ödemeleri var; üst yönetim henüz güncel nakit öngörüsünü görmedi.",
          "Kaan Polat", "bütçe planlama sorumlusu", [
              S("Öncelikli yükümlülükleri koruyup nakit planını hemen güncelleyin.", "Otoriter", -2, 3, 8, "Kritik ödemeler korundu; bazı ödemeler görüşmeye açıldı."),
              S("Kaan ve ilgili ekiplerle takvim seçeneklerini şeffafça değerlendirin.", "Demokratik", 4, -3, 8, "Alternatif bulundu; çoklu görüşme zaman aldı."),
              S("Kaan'a gecikme senaryoları için erken uyarı modeli hazırlatın.", "Koçvari", 5, 1, 5, "Öngörü gelişti; bu haftanın nakit açığı ayrıca yönetildi."),
              S("Tahsilat yakında gelir diyerek mevcut ödeme planını koruyun.", "Kaçınmacı", -3, 4, -11, "Plan değişmedi; nakit tamponu daraldı."),
          ]),
        V("fin-06",
          "Ece Arslan, yatırım değerlendirmesinde iki satış tahmininin uyuşmadığını bildiriyor. Yatırım komitesi yarın; yüksek tahmin projeyi kârlı gösteriyor.",
          "Ece Arslan", "finansal analist", [
              S("Uyuşmazlığı komiteye açıkça sunup nihai kararı veri teyidine bağlayın.", "Otoriter", -2, -3, 10, "Yanlış karar riski düştü; yatırım takvimi uzadı."),
              S("Ece ve iş birimiyle iki tahminin varsayımlarını karşılaştırın.", "Demokratik", 4, -3, 8, "Belirsizlik kaynağı görüldü; hazırlık geceye uzadı."),
              S("Ece'ye ortak tahmin şablonu geliştirme sorumluluğu verin.", "Koçvari", 5, 1, 5, "Gelecek kararlar iyileşti; yarınki rakam hâlâ açıklama gerektiriyor."),
              S("Karar çıksın diye yüksek tahmini kullanın.", "Kaçınmacı", -3, 5, -12, "Yatırım ilerledi; getirisi olduğundan iyi gösterildi."),
          ]),
        V("fin-07",
          "Ayşe Yıldız, tedarikçinin yeni IBAN bilgisini yalnızca e-postadan aldığını belirtiyor. Eski hesaba ödeme için onay hazır.",
          "Ayşe Yıldız", "muhasebe uzmanı", [
              S("Ödemeyi durdurup kayıtlı kanaldan hesap doğrulaması alın.", "Otoriter", -2, -3, 10, "Yanlış hesaba ödeme riski azaldı; işlem gecikti."),
              S("Ayşe ve satın almayla değişiklik belgelerini birlikte doğrulayın.", "Demokratik", 4, -2, 8, "Hesap değişikliği açıklığa kavuştu; ek kontrol gerekti."),
              S("Ayşe'ye hesap değişikliği için çift teyit prosedürü hazırlatın.", "Koçvari", 5, 1, 5, "Gelecek ödeme güvenliği arttı; bu işlem ayrıca doğrulandı."),
              S("Kurumsal e-posta görünüyor diye yeni IBAN'a ödeme yapın.", "Kaçınmacı", -3, 5, -12, "İşlem hızlandı; alıcı doğruluğu belirsiz kaldı."),
          ]),
        V("fin-08",
          "Kaan Polat, iki departmanın aynı tasarrufu kendi bütçe planına eklediğini gördü. Toplam hedef bu tutar sayesinde tutuyor.",
          "Kaan Polat", "bütçe planlama sorumlusu", [
              S("Çifte sayımı çıkarıp hedef açığını yönetime gösterin.", "Otoriter", -2, -3, 10, "Hedef dürüst hesaplandı; yeni tasarruf ihtiyacı doğdu."),
              S("Kaan ve departmanlarla tasarruf sahipliğini netleştirin.", "Demokratik", 4, -2, 8, "Ortak veri oluştu; toplantı zamanı gerekti."),
              S("Kaan'a tasarruf kayıtları için tekil takip sistemi kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; hedef açığı yine çözülmeli."),
              S("Yıl içinde telafi edilir diye iki kaydı da bırakın.", "Kaçınmacı", -3, 5, -11, "Hedef tutar göründü; gerçekte açık kaldı."),
          ]),
        V("fin-09",
          "Ece Arslan, üç mağazanın elektrik giderinde beklenmeyen artış buldu. Tesis ekibi yeni aydınlatma kurulumunun tasarruf sağlaması gerektiğini söylüyor.",
          "Ece Arslan", "finansal analist", [
              S("Fatura ve sayaç verisini doğrulayıp gider varsayımını güncelleyin.", "Otoriter", -2, 3, 7, "Sapma görünür oldu; neden henüz kesinleşmedi."),
              S("Ece ve tesis ekibiyle kurulum-tüketim karşılaştırması yapın.", "Demokratik", 4, -2, 8, "Muhtemel neden bulundu; veri toplama uzadı."),
              S("Ece'ye mağaza bazlı enerji uyarı paneli hazırlatın.", "Koçvari", 5, 1, 5, "Sapmalar erken görülecek; üç mağaza ayrıca incelendi."),
              S("Mevsimsel dalgalanmadır diye bütçeyi değiştirmeyin.", "Kaçınmacı", -3, -4, -9, "Ek çalışma çıkmadı; gerçek neden saklı kaldı."),
          ]),
        V("fin-10",
          "İç denetim uzmanı Zeynep Aydın, bazı masraf onaylarının ödeme yapıldıktan sonra verildiğini bildiriyor. İşlemler hizmet alımı için yapılmış.",
          "Zeynep Aydın", "iç denetim uzmanı", [
              S("İşlemleri raporlayıp yeni ödemelerde ön onayı zorunlu tutun.", "Otoriter", -3, 2, 10, "Kontrol güçlendi; acil hizmet talepleri yavaşladı."),
              S("Zeynep ve hizmet sahipleriyle onay darboğazını inceleyin.", "Demokratik", 4, -2, 8, "Kök neden görüldü; süreç tasarımı gerekti."),
              S("Zeynep'e acil onay için kontrollü istisna akışı hazırlatın.", "Koçvari", 5, 1, 5, "Esneklik oluşturuldu; eski işlemler ayrıca raporlandı."),
              S("Hizmet alınmış diye gecikmiş onayları sorun etmeyin.", "Kaçınmacı", -3, 4, -11, "İşleyiş sürdürdü; kontrol açığı kalıcılaştı."),
          ]),
        V("fin-11",
          "Ayşe Yıldız, bir giderin yanlış döneme kaydedildiğini söylüyor. Aylık sonuç düzeltilirse hedef kaçacak; yıllık toplam değişmeyecek.",
          "Ayşe Yıldız", "muhasebe uzmanı", [
              S("Dönemsellik hatasını düzeltip aylık sapmayı açıkça raporlayın.", "Otoriter", -2, -2, 10, "Aylık veri doğru oldu; hedef kaçırıldı."),
              S("Ayşe ve ilgili departmanla işlem tarihini teyit edip not ekleyin.", "Demokratik", 4, -2, 8, "Düzeltme kanıtlandı; kapanış uzadı."),
              S("Ayşe'ye dönem doğrulama kontrolü hazırlatın.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; bu ayın hedef sapması sürdü."),
              S("Yıllık toplam aynı diye kaydı taşımayın.", "Kaçınmacı", -3, 5, -12, "Aylık hedef tuttu; rapor dönemi yanlış kaldı."),
          ]),
        V("fin-12",
          "Kaan Polat, yeni kiralama teklifinin düşük aylık ödeme sunduğunu, fakat uzun dönem toplam maliyetin satın almadan yüksek olduğunu söylüyor.",
          "Kaan Polat", "bütçe planlama sorumlusu", [
              S("Toplam maliyeti ve yükümlülükleri karşılaştırmadan onay vermeyin.", "Otoriter", -2, -3, 8, "Maliyet görünür oldu; karar gecikti."),
              S("Kaan ve kullanım ekibiyle nakit ve esneklik değerini birlikte ölçün.", "Demokratik", 4, -2, 8, "Tercih bilinçli verildi; analiz emek istedi."),
              S("Kaan'a standart kirala-satın al modeli hazırlatın.", "Koçvari", 5, 1, 5, "Gelecek kararlar kolaylaştı; bu teklif ayrıca değerlendirildi."),
              S("Aylık ödeme düşük diye uzun maliyete bakmadan imzalayın.", "Kaçınmacı", -3, 5, -10, "İlk bütçe rahatladı; toplam maliyet arttı."),
          ]),
        V("fin-13",
          "Ece Arslan, mağaza performans raporunda iadelerin yanlış mağazaya yazıldığını fark etti. Bazı mağaza primleri bu rapora bağlı.",
          "Ece Arslan", "finansal analist", [
              S("Prim hesabını durdurup mağaza bazlı iadeleri doğrulayın.", "Otoriter", -2, -3, 10, "Yanlış prim önlendi; ödeme süreci gecikti."),
              S("Ece ve mağazacılıkla işlem kaynağını birlikte düzeltin.", "Demokratik", 4, -2, 8, "Dağılım adil oldu; veri çalışması uzadı."),
              S("Ece'ye iade-mağaza eşleştirmesi için kontrol kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; mevcut primler yine hesaplandı."),
              S("Toplam iade aynı diye raporu değiştirmeyin.", "Kaçınmacı", -4, 5, -11, "Prim işlemi yetişti; mağazalar arasında adaletsizlik oluştu."),
          ]),
        V("fin-14",
          "Zeynep Aydın, kontrol örnekleminde aynı kişinin hem tedarikçi kartı açıp hem de ödemeyi onaylayabildiğini fark etti.",
          "Zeynep Aydın", "iç denetim uzmanı", [
              S("Yetki ayrımını hemen uygulayıp geçmiş işlemleri risk bazlı inceleyin.", "Otoriter", -3, -4, 10, "Kontrol açığı kapandı; ödeme işlemleri yavaşladı."),
              S("Zeynep ve süreç sahipleriyle uygulanabilir görev ayrımı kurun.", "Demokratik", 4, -2, 8, "Kontrol sürdürülebilir oldu; tasarım zamanı aldı."),
              S("Zeynep'e periyodik yetki gözden geçirmesi yönettirin.", "Koçvari", 5, 1, 5, "İzleme güçlendi; mevcut erişim ayrıca kapatıldı."),
              S("Kimse kötüye kullanmadı diye erişimi değiştirmeyin.", "Kaçınmacı", -3, 4, -12, "İş akışı hızlı kaldı; suistimal fırsatı sürdü."),
          ]),
        V("fin-15",
          "Kaan Polat, bir departmanın yıl sonu bütçesini kullanmak için ihtiyacı gelecek yıla ait hizmeti erkenden satın almak istediğini söylüyor.",
          "Kaan Polat", "bütçe planlama sorumlusu", [
              S("İhtiyaç ve muhasebe dönemi doğrulanmadan onay vermeyin.", "Otoriter", -2, -3, 9, "Kaynak doğru döneme yöneldi; departman bütçeyi kullanamadı."),
              S("Kaan ve departmanla hizmetin gerçek zamanlamasını değerlendirin.", "Demokratik", 4, -2, 8, "İhtiyaç netleşti; karar uzadı."),
              S("Kaan'a yıl sonu bütçe davranışını azaltacak planlama önerisi hazırlatın.", "Koçvari", 5, 1, 5, "Gelecek dönem iyileşebilir; mevcut talep ayrıca kararlaştırıldı."),
              S("Bütçe boşa gitmesin diye alımı hemen onaylayın.", "Kaçınmacı", -3, 5, -10, "Bütçe kullanıldı; gerçek ihtiyaç ve dönem uyumu sorgulandı."),
          ]),
        V("fin-16",
          "Ayşe Yıldız, tedarikçinin ödendi dediği fatura için bankadan başarısız işlem bildirimi geldiğini söylüyor. Tedarikçi teslimatı durdurmakla tehdit ediyor.",
          "Ayşe Yıldız", "muhasebe uzmanı", [
              S("Banka durumunu teyit edip doğrulanmış ödeme takvimini yazılı paylaşın.", "Otoriter", -2, 3, 8, "Belirsizlik azaldı; teslimat için ek görüşme gerekti."),
              S("Ayşe, banka ve tedarikçiyle işlem izini birlikte inceleyin.", "Demokratik", 4, -2, 8, "Hata kaynağı bulundu; çoklu koordinasyon zaman aldı."),
              S("Ayşe'ye başarısız ödeme uyarı süreci kur u.", "Koçvari", 5, 1, 5, "Yeni risk azaldı; bu fatura ayrıca ödendi."),
              S("Ödendi varsayımıyla bankanın düzeltmesini bekleyin.", "Kaçınmacı", -3, -4, -9, "Ek işlem olmadı; teslimat riski büyüdü."),
          ]),
        V("fin-17",
          "Ece Arslan, raporda maliyet düşüşünün bir kısmının henüz gelmemiş faturadan kaynaklandığını fark etti. Yönetim düşüşü kalıcı tasarruf sanıyor.",
          "Ece Arslan", "finansal analist", [
              S("Henüz gelmeyen maliyeti tahminle rapora ekleyip açıklama yapın.", "Otoriter", -2, -2, 10, "Tasarruf doğru yorumlandı; rapor revize edildi."),
              S("Ece ve satın almayla olası fatura tutarını doğrulayın.", "Demokratik", 4, -2, 8, "Tahmin güçlendi; kapanış uzadı."),
              S("Ece'ye tahakkuk kontrolü için düzenli liste hazırlatın.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; bu rapor ayrıca düzeltildi."),
              S("Fatura gelince kaydederiz diyerek tasarruf yorumunu bırakın.", "Kaçınmacı", -3, 5, -12, "Rapor hızlı çıktı; kalıcı olmayan düşüş başarı sayıldı."),
          ]),
        V("fin-18",
          "Zeynep Aydın, denetimde küçük tutarlı ama çok sayıda istisnai ödeme görüyor. Tek tek eşik altında; toplamda anlamlı tutara ulaşıyor.",
          "Zeynep Aydın", "iç denetim uzmanı", [
              S("Toplu tutarı inceleyip işlem örüntüsünü resmî kayda alın.", "Otoriter", -2, -3, 10, "Örüntü görüldü; inceleme ek iş yarattı."),
              S("Zeynep ve ödeme ekipleriyle istisnaların meşru nedenlerini araştırın.", "Demokratik", 4, -2, 8, "Yanlış suçlama önlendi; süreç uzadı."),
              S("Zeynep'e parçalı ödeme uyarı raporu hazırlatın.", "Koçvari", 5, 1, 5, "Erken tespit sağlandı; geçmiş işlemler ayrıca incelendi."),
              S("Her ödeme küçük diye konuyu kapatın.", "Kaçınmacı", -3, 4, -11, "İnceleme yapılmadı; toplu risk gözden kaçtı."),
          ]),
        V("fin-19",
          "Kaan Polat, iki yeni mağaza yatırımının birlikte bütçeye sığmadığını söylüyor. Birinin getirisi yüksek ama belirsiz; diğerinin getirisi düşük ama daha öngörülebilir.",
          "Kaan Polat", "bütçe planlama sorumlusu", [
              S("Önceden belirlenen risk ölçütüne göre birini seçip gerekçelendirin.", "Otoriter", -2, 4, 6, "Karar çıktı; seçilmeyen proje ek değerlendirme istedi."),
              S("Kaan ve iş ekipleriyle risk-getiri senaryolarını karşılaştırın.", "Demokratik", 4, -2, 8, "Tercih kanıta dayandı; yatırım kararı gecikti."),
              S("Kaan'a aşamalı yatırım seçeneği hazırlatın.", "Koçvari", 5, 1, 5, "Esneklik oluştu; ilk yatırım ölçeği küçüldü."),
              S("Çatışma çıkmasın diye iki projeyi de kısmi finanse edin.", "Kaçınmacı", -3, -4, -9, "İki ekip de başladı; hiçbiri yeterli kaynağı bulamadı."),
          ]),
        V("fin-20",
          "Ayşe Yıldız, otomatik ödeme dosyasında aynı tedarikçinin bir hesabının pasif, diğerinin aktif olduğunu fark etti. Dosya bankaya gönderilmek üzere.",
          "Ayşe Yıldız", "muhasebe uzmanı", [
              S("Dosyayı bekletip onaylı aktif hesabı teyit edin.", "Otoriter", -2, -3, 10, "Yanlış aktarım önlendi; ödeme saati gecikti."),
              S("Ayşe ve tedarikçi yöneticisiyle hesap geçmişini doğrulayın.", "Demokratik", 4, -2, 8, "Hesap netleşti; ek inceleme gerekti."),
              S("Ayşe'ye pasif hesapların dosyada görünmesini önleyen kontrol kurdurun.", "Koçvari", 5, 1, 5, "Yeni hata önlenecek; bugünkü dosya ayrıca düzeltildi."),
              S("Banka reddederse düzeltiriz diyerek dosyayı gönderin.", "Kaçınmacı", -3, 5, -11, "Dosya zamanında gitti; ödeme başarısız olabilir."),
          ]),
    ],

    "Bilgi Teknolojileri": [
        V("bt-01",
          "Sistem yöneticisi Emre Yılmaz, gece güncellemesinden sonra bazı mağaza kasalarının işlem yapamadığını bildiriyor. Geri alma mümkün; ancak güncelleme başka bir güvenlik açığını kapatıyor.",
          "Emre Yılmaz", "sistem yöneticisi", [
              S("Geri alma riskini değerlendirip kasa hizmetini önceleyen kontrollü dönüş yapın.", "Otoriter", -2, 5, 7, "Kasalar çalıştı; güvenlik açığına geçici önlem gerekti."),
              S("Emre ve güvenlik ekibiyle etkilenen mağazalar için kademeli çözüm belirleyin.", "Demokratik", 4, -3, 9, "İki risk birlikte yönetildi; ilk çözüm yavaşladı."),
              S("Emre'ye geri dönüş ve güvenlik önlemlerini ayrı ekiplerle koordine ettirin.", "Koçvari", 5, 1, 6, "Ekip sorumluluk aldı; yoğun iletişim gerekti."),
              S("Güncellemenin kendiliğinden düzelmesini bekleyin.", "Kaçınmacı", -5, -8, -11, "Açık kapalı kaldı; mağazalarda satış aksadı."),
          ]),
        V("bt-02",
          "Siber güvenlik uzmanı Deren Aksoy, müşteri verilerini etkileyebilecek bir açık buldu. Henüz ihlal kanıtı yok; sistemi kapatmak çevrim içi satışları durduracak.",
          "Deren Aksoy", "siber güvenlik uzmanı", [
              S("Olay müdahale planını başlatıp gerekli erişimleri geçici sınırlayın.", "Otoriter", -2, -5, 10, "Risk alanı daraldı; bazı hizmetler yavaşladı."),
              S("Deren ve sistem ekipleriyle açığın kapsamını doğrulayıp kontrollü önlem alın.", "Demokratik", 4, -3, 9, "Önlem hedefli oldu; inceleme boyunca risk izlendi."),
              S("Deren'e izleme ve kanıt koruma akışını yönetme yetkisi verin.", "Koçvari", 5, 1, 6, "Olay kaydı güçlendi; erişim kararı yine gerekli."),
              S("İhlal kanıtı yok diye sabaha kadar bekleyin.", "Kaçınmacı", -4, 5, -12, "Satış sürdü; olası maruziyet uzadı."),
          ]),
        V("bt-03",
          "Yazılım geliştirici Can Öztürk, teslimden üç gün önce kritik entegrasyon testinin yapılmadığını fark ediyor. İş birimi lansmanı duyurdu.",
          "Can Öztürk", "yazılım geliştirici", [
              S("Kritik testi tamamlamadan canlı geçişe onay vermeyin.", "Otoriter", -2, -5, 10, "Canlı hata riski düştü; lansman tarihine baskı oluştu."),
              S("Can ve iş birimiyle güvenli dar kapsamlı lansman seçeneğini değerlendirin.", "Demokratik", 4, -3, 9, "Kısmi lansman mümkün oldu; kapsam revize edildi."),
              S("Can'a risk odaklı test planını yönetme sorumluluğu verin.", "Koçvari", 5, 1, 5, "Eksik test görünür oldu; teslim kararı yeniden verildi."),
              S("Zaman kalmadı diye testi sonraki sürüme bırakın.", "Kaçınmacı", -4, 5, -12, "Lansman yetişti; kritik entegrasyon bilinmeden açıldı."),
          ]),
        V("bt-04",
          "Destek uzmanı Ayşe Yıldız, aynı stok ekranı hatası için 80 talep geldiğini söylüyor. Ekip talepleri tek tek kapatıyor; kök neden çalışması yapılmadı.",
          "Ayşe Yıldız", "destek uzmanı", [
              S("Ortak olay kaydı açıp tekrar eden talepleri tek çözüm altında toplayın.", "Otoriter", -2, 5, 7, "Destek kapasitesi açıldı; bazı talepler geç yanıt aldı."),
              S("Ayşe ve geliştirmeyle hangi mağazaların gerçekten etkilendiğini belirleyin.", "Demokratik", 4, -2, 8, "Öncelik doğru kondu; inceleme zaman aldı."),
              S("Ayşe'ye tekrar eden sorun analizi ve bilgi bankası görevi verin.", "Koçvari", 6, 1, 5, "Destek ekibi gelişti; teknik hata ayrıca giderilecek."),
              S("Talepleri sırayla çözmeye devam edin.", "Kaçınmacı", -4, -5, -9, "Kısa vadeli yanıt sürdü; kuyruk büyüdü."),
          ]),
        V("bt-05",
          "Proje yöneticisi Zeynep Aydın, iki kıdemli geliştiricinin mimari seçimde anlaşamadığını söylüyor. İki çözüm de çalışabilir; biri hızlı, diğeri bakım açısından daha uygun.",
          "Zeynep Aydın", "proje yöneticisi", [
              S("Ölçüt ve tarih koyup sınırlı veriye göre mimari kararı verin.", "Otoriter", -3, 5, 5, "Ekip ilerledi; seçilmeyen yaklaşımın sahibi ikna edilmeli."),
              S("Zeynep'le bakım ve teslim maliyetini aynı tabloda karşılaştırın.", "Demokratik", 4, -3, 8, "Karar ortak veriye dayandı; teslim zamanı azaldı."),
              S("İki geliştiriciye küçük prototip hazırlatıp sonuçları tartıştırın.", "Koçvari", 6, 1, 5, "Teknik öğrenme oluştu; prototip maliyeti doğdu."),
              S("Uzlaşmalarını bekleyip kararı açık bırakın.", "Kaçınmacı", -5, -5, -9, "Çatışma ertelendi; proje bekledi."),
          ]),
        V("bt-06",
          "Emre Yılmaz, yedekleme raporunun başarılı olduğunu fakat son geri yükleme testinin başarısız kaldığını bildiriyor. Yeni yedekleme penceresi bu gece.",
          "Emre Yılmaz", "sistem yöneticisi", [
              S("Geri yükleme güvence altına alınana kadar olayı kritik risk olarak açın.", "Otoriter", -2, -4, 10, "Risk görünür oldu; ekip gece çalıştı."),
              S("Emre ve iş sürekliliği ekibiyle geçici kurtarma seçenekleri belirleyin.", "Demokratik", 4, -3, 9, "Alternatif oluştu; doğrulama zaman aldı."),
              S("Emre'ye otomatik geri yükleme testi tasarlatın.", "Koçvari", 5, 1, 5, "Uzun vadeli güvence artacak; bu geceki test ayrıca yapılmalı."),
              S("Yedekleme başarılı göründüğü için test hatasını önemsemeyin.", "Kaçınmacı", -4, 5, -12, "Ek iş çıkmadı; veri kurtarma güvencesi yok."),
          ]),
        V("bt-07",
          "Deren Aksoy, görev değiştiren bir çalışanın eski yönetici yetkisinin hâlâ aktif olduğunu söylüyor. Çalışanın yetkiyi kötüye kullandığına dair işaret yok.",
          "Deren Aksoy", "siber güvenlik uzmanı", [
              S("Gereksiz erişimi kaldırıp benzer hesapları tarayın.", "Otoriter", -2, -2, 10, "Yetki açığı kapandı; erişim talepleri arttı."),
              S("Deren ve İK ile rol değişikliği akışını doğrulayın.", "Demokratik", 4, -2, 8, "Kök neden bulundu; koordinasyon zamanı gerekti."),
              S("Deren'e düzenli yetki gözden geçirme görevi verin.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; eski erişim ayrıca kaldırıldı."),
              S("Kötüye kullanım yok diye erişimi bırakın.", "Kaçınmacı", -3, 4, -12, "Kullanıcı etkilenmedi; gereksiz yetki kaldı."),
          ]),
        V("bt-08",
          "Can Öztürk, yeni sürümde stok ekranının 9 saniyede açıldığını gösterdi. Mağaza ekibi kâğıt notlara döndü; diğer özellikler sorunsuz.",
          "Can Öztürk", "yazılım geliştirici", [
              S("Stok özelliğini önceki sürüme alıp diğer özellikleri koruyun.", "Otoriter", -2, 4, 7, "Mağaza işi hızlandı; iki sürüm birlikte yönetildi."),
              S("Can ve mağazalarla kullanım etkisini ölçüp hedefli düzeltme seçin.", "Demokratik", 4, -2, 8, "En büyük darboğaz görüldü; anlık sorun sürdü."),
              S("Can'a performans ölçümünü ve sonraki sürüm testini yönettirin.", "Koçvari", 5, 1, 5, "Ölçüm gelişti; mağazalar geçici yöntem kullandı."),
              S("Sistem çalışıyor diye yavaşlığı sonraki döneme bırakın.", "Kaçınmacı", -4, -5, -10, "Sürüm değişmedi; mağazada manuel iş arttı."),
          ]),
        V("bt-09",
          "Ayşe Yıldız, mağaza çalışanlarına yazılım eğitimi verilmeden erişim açıldığını bildiriyor. Hatalı ürün güncellemeleri oluşmuş.",
          "Ayşe Yıldız", "destek uzmanı", [
              S("Riskli yetkileri sınırlayıp hatalı güncellemeleri geri alın.", "Otoriter", -2, -3, 9, "Yeni hata durdu; mağaza işlemleri kısıtlandı."),
              S("Ayşe ve eğitim ekibiyle erişim ve eğitim takvimini eşleştirin.", "Demokratik", 4, -2, 8, "Geçiş düzeldi; koordinasyon gerekti."),
              S("Ayşe'ye kısa uygulama rehberi ve destek oturumu hazırlatın.", "Koçvari", 6, 1, 5, "Çalışanlar destek aldı; yanlış kayıtlar ayrıca temizlendi."),
              S("Çalışanlar deneyerek öğrenir diye erişimi açık bırakın.", "Kaçınmacı", -4, 4, -10, "Kullanım sürdü; veri hataları arttı."),
          ]),
        V("bt-10",
          "Zeynep Aydın, yazılım tedarikçisinin bakım saatini kampanya gecesine aldığını söylüyor. Sözleşmede bakım penceresi değişimi için ön bildirim gerekiyor.",
          "Zeynep Aydın", "proje yöneticisi", [
              S("Sözleşme şartına dayanarak farklı bakım saati isteyin.", "Otoriter", -2, 3, 8, "Kampanya korundu; tedarikçi yeni takvim aradı."),
              S("Zeynep ve e-ticaretle kesinti etkisini ve uygun pencereyi seçin.", "Demokratik", 4, -2, 8, "Ortak takvim oluştu; bakım ertelendi."),
              S("Zeynep'e kesinti ve geri dönüş planı hazırlatın.", "Koçvari", 5, 1, 5, "Hazırlık güçlendi; saat değişikliği ayrıca görüşüldü."),
              S("Bakım kısa sürer diyerek kampanya gecesini kabul edin.", "Kaçınmacı", -3, 5, -11, "Bakım hızlı planlandı; satış kesintisi riski doğdu."),
          ]),
        V("bt-11",
          "Deren Aksoy, bir ekipte ortak hesapla sisteme giriş yapıldığını tespit etti. Bu yöntem hızlı ama hangi işlemi kimin yaptığı bilinmiyor.",
          "Deren Aksoy", "siber güvenlik uzmanı", [
              S("Ortak hesabı kontrollü kapatıp kişisel erişimleri açın.", "Otoriter", -3, -3, 10, "İşlem izi oluştu; geçişte destek talebi arttı."),
              S("Deren ve ekip lideriyle ortak hesap kullanım nedenini çözün.", "Demokratik", 4, -2, 8, "Gerçek erişim sorunu bulundu; geçiş uzadı."),
              S("Deren'e kolay kişisel giriş pilotu geliştirme görevi verin.", "Koçvari", 5, 1, 5, "Kullanım kolaylığı arttı; ortak erişim ayrıca kapatıldı."),
              S("İşler aksamasın diye ortak hesabı kullanmaya devam edin.", "Kaçınmacı", -3, 5, -11, "Akış hızlı kaldı; sorumluluk izi olmadı."),
          ]),
        V("bt-12",
          "Emre Yılmaz, üç şehirde ağ kesintisi olduğunu söylüyor. Taşıyıcı genel arıza bildiriyor ama bir mağazada yerel cihaz hatası da olabilir.",
          "Emre Yılmaz", "sistem yöneticisi", [
              S("Etkilenen mağazalarda yedek bağlantıyı açıp yerel cihazı ayrı inceleyin.", "Otoriter", -2, 4, 7, "Kritik bağlantı geri geldi; yedek maliyeti oluştu."),
              S("Emre ve saha ekibiyle genel ve yerel etkileri ayrıştırın.", "Demokratik", 4, -2, 8, "Hedefli müdahale yapıldı; ilk yanıt uzadı."),
              S("Emre'ye şehir bazlı kesinti izleme planı kurdurun.", "Koçvari", 5, 1, 5, "Uyarı iyileşti; mevcut kesinti ayrıca çözülüyor."),
              S("Taşıyıcı düzeltir diye mağazaları aramayın.", "Kaçınmacı", -4, -5, -10, "Ekip zaman harcamadı; yerel sorun gözden kaçtı."),
          ]),
        V("bt-13",
          "Can Öztürk, kod inceleme yapılmadan acil düzeltmenin canlıya alınmasını öneriyor. Düzeltme ödeme akışına dokunuyor.",
          "Can Öztürk", "yazılım geliştirici", [
              S("En azından ödeme akışına odaklı ikinci göz kontrolü isteyin.", "Otoriter", -2, -3, 9, "Hata riski azaldı; düzeltme gecikti."),
              S("Can ve ödeme ekibiyle kısa risk temelli test listesi belirleyin.", "Demokratik", 4, -2, 8, "Kritik yollar test edildi; ekip yoğunlaştı."),
              S("Can'a güvenli acil yayın kontrolünü tasarlatın.", "Koçvari", 5, 1, 5, "Sonraki yayınlar iyileşti; bugünkü inceleme ayrıca yapıldı."),
              S("Sorun acil diye inceleme olmadan canlıya alın.", "Kaçınmacı", -3, 5, -12, "Düzeltme hızlı çıktı; ödeme akışı yeni risk taşıdı."),
          ]),
        V("bt-14",
          "Ayşe Yıldız, destek kuyruğunda kritik mağaza talebinin çok sayıda düşük öncelikli talep arasında kaldığını söylüyor.",
          "Ayşe Yıldız", "destek uzmanı", [
              S("Etki ve aciliyete göre sıra kuralı koyup kritik talebi öne alın.", "Otoriter", -2, 4, 7, "Kritik mağaza destek aldı; diğer talepler bekledi."),
              S("Ayşe ve destek ekibiyle öncelik ölçütlerini birlikte belirleyin.", "Demokratik", 4, -2, 8, "Adil sıra oluştu; ilk düzenleme zaman aldı."),
              S("Ayşe'ye önceliklendirme örneklerini ekibe öğretme görevi verin.", "Koçvari", 6, 1, 5, "Ekip gelişti; biriken talepler ayrıca çözülmeli."),
              S("İlk giren ilk çözülür kuralını hiç değiştirmeyin.", "Kaçınmacı", -4, -5, -9, "Sıra basit kaldı; yüksek etki yaratan arıza uzadı."),
          ]),
        V("bt-15",
          "Deren Aksoy, güvenlik günlüğünde çok sayıda başarısız giriş görüyor. Hesap sahibi sık şifre unuttuğunu söylüyor; denemelerin bir bölümü farklı ülkelerden.",
          "Deren Aksoy", "siber güvenlik uzmanı", [
              S("Hesabı geçici korumaya alıp girişleri doğrulayın.", "Otoriter", -2, -3, 10, "Olası saldırı sınırlandı; kullanıcının işi aksadı."),
              S("Deren ve kullanıcıyla bilinen ve şüpheli girişleri ayırın.", "Demokratik", 4, -2, 8, "Durum netleşti; inceleme sürdü."),
              S("Deren'e şüpheli konum uyarısı eşiklerini iyileştirtin.", "Koçvari", 5, 1, 5, "Uyarı kalitesi artacak; mevcut hesap yine incelendi."),
              S("Kullanıcı şifre unutuyor diye kayıtları önemsemeyin.", "Kaçınmacı", -3, 5, -12, "İş kesilmedi; gerçek saldırı olasılığı göz ardı edildi."),
          ]),
        V("bt-16",
          "Zeynep Aydın, proje takviminde veri geçişine yalnızca bir gece ayrıldığını fark etti. Eski sistem aynı sabah kapatılacak.",
          "Zeynep Aydın", "proje yöneticisi", [
              S("Geri dönüş testi olmadan eski sistemi kapatma kararını erteleyin.", "Otoriter", -2, -4, 9, "İş sürekliliği korundu; geçiş tarihi değişti."),
              S("Zeynep ve iş ekipleriyle kademeli geçiş seçeneği oluşturun.", "Demokratik", 4, -2, 8, "Risk bölündü; iki sistemi birlikte yönetmek gerekti."),
              S("Zeynep'e küçük veri grubuyla prova yaptırın.", "Koçvari", 5, 1, 5, "Hatalar erken görüldü; tam geçiş yine plan gerektiriyor."),
              S("Takvim duyuruldu diye tek gecelik planı değiştirmeyin.", "Kaçınmacı", -3, 5, -11, "Takvim korundu; geri dönüş güvencesi zayıf kaldı."),
          ]),
        V("bt-17",
          "Emre Yılmaz, sun Yitesinin kampanya yüküne sınırda yettiğini söylüyor. Kapasite artırmak maliyetli; kampanya iki gün sürecek.",
          "Emre Yılmaz", "sistem yöneticisi", [
              S("Onaylı kısa süreli kapasite artışı yapıp kullanım sınırı koyun.", "Otoriter", -2, 5, 6, "Performans korundu; ek maliyet doğdu."),
              S("Emre ve e-ticaretle kritik işlemler için yük planı oluşturun.", "Demokratik", 4, -2, 8, "Kaynak verimli kullanıldı; bazı özellikler yavaşladı."),
              S("Emre'ye otomatik kapasite izleme eşiği hazırlatın.", "Koçvari", 5, 1, 5, "Uyarı gelişti; bugünkü kapasite kararı yine gerekli."),
              S("Trafik tahmini tutar diye mevcut kapasiteyle ilerleyin.", "Kaçınmacı", -3, 4, -10, "Maliyet artmadı; yoğun saatte kesinti riski yükseldi."),
          ]),
        V("bt-18",
          "Can Öztürk, bir ürünün stok güncellemesi iki sistem arasında geciktiğinde yanlış satış oluştuğunu gösterdi. Kalıcı çözüm üç hafta sürecek.",
          "Can Öztürk", "yazılım geliştirici", [
              S("Geçici satış sınırı koyup kalıcı düzeltmeyi önceliklendirin.", "Otoriter", -2, -3, 9, "Yanlış satış azaldı; bazı doğru satışlar da sınırlandı."),
              S("Can, stok ve e-ticaretle riskli ürünleri belirleyin.", "Demokratik", 4, -2, 8, "Sınırlama hedefli oldu; günlük takip gerekti."),
              S("Can'a gecikme ölçümü ve erken uyarı geliştirtin.", "Koçvari", 5, 1, 5, "Hata erken görülecek; kalıcı düzeltme hâlâ bekleniyor."),
              S("Üç hafta sonunda çözülecek diye geçici adım atmayın.", "Kaçınmacı", -3, 4, -11, "İş akışı değişmedi; yanlış satış sürdü."),
          ]),
        V("bt-19",
          "Ayşe Yıldız, farklı mağazalardan gelen hata ekran görüntülerinde müşteri bilgileri olduğunu fark etti. Talepler geniş bir destek grubunda paylaşılıyor.",
          "Ayşe Yıldız", "destek uzmanı", [
              S("Geniş paylaşımları durdurup görüntüleri güvenli kanala taşıyın.", "Otoriter", -2, -3, 10, "Veri yayılımı sınırlandı; destek alışkanlığı değişti."),
              S("Ayşe ve veri güvenliğiyle maskeleme yöntemi belirleyin.", "Demokratik", 4, -2, 8, "Destek akışı korundu; yeni yöntem öğretildi."),
              S("Ayşe'ye güvenli örnek paylaşımı eğitimi hazırlatın.", "Koçvari", 5, 1, 5, "Ekip öğrendi; eski paylaşımlar ayrıca incelendi."),
              S("Destek hızını korumak için paylaşımları değiştirmeyin.", "Kaçınmacı", -3, 5, -12, "Talepler hızlı görüldü; kişisel veri gereksiz yayıldı."),
          ]),
        V("bt-20",
          "Deren Aksoy, harici yazılım tedarikçisinin bakım için süresiz yönetici erişimi istediğini söylüyor. Bakımın bu gece yapılması planlanıyor.",
          "Deren Aksoy", "siber güvenlik uzmanı", [
              S("Yalnız sınırlı süreli ve kayıtlı erişim verin.", "Otoriter", -2, 3, 9, "Bakım yapılabildi; erişim hazırlığı zaman aldı."),
              S("Deren ve tedarikçiyle gerekli en düşük yetkiyi belirleyin.", "Demokratik", 4, -2, 8, "Yetki uygun ölçüde kaldı; görüşme uzadı."),
              S("Deren'e tedarikçi erişim şablonu geliştirtin.", "Koçvari", 5, 1, 5, "Gelecek bakım kolaylaşacak; bu erişim yine sınırlanmalı."),
              S("Bakım gecikmesin diye süresiz yetki açın.", "Kaçınmacı", -3, 5, -12, "Bakım hızlandı; dış erişim kalıcı kaldı."),
          ]),
    ],

    "E-Ticaret": [
        V("eti-01",
          "E-ticaret operasyon uzmanı Merve Çelik, indirim gününde sipariş ekranının yavaşladığını bildiriyor. Sepetler dolu; teknik ekip kapasite artışının maliyetli olacağını söylüyor.",
          "Merve Çelik", "e-ticaret operasyon uzmanı", [
              S("Onaylı kapasite artışını kısa süreli açıp maliyeti izleyin.", "Otoriter", -2, 6, 6, "Sipariş akışı düzeldi; ek altyapı maliyeti oluştu."),
              S("Merve ve teknik ekiple kritik adımlara kaynak ayırın.", "Demokratik", 4, -2, 8, "Ödeme akışı korundu; ikincil özellikler yavaşladı."),
              S("Merve'ye canlı darboğaz izleme ve iletişim sorumluluğu verin.", "Koçvari", 5, 1, 5, "Ekip görünürlük kazandı; teknik çözüm ayrıca gerekti."),
              S("Trafik düşer diye müşterilere bilgi vermeden bekleyin.", "Kaçınmacı", -4, -7, -11, "Maliyet artmadı; başarısız sepetler çoğaldı."),
          ]),
        V("eti-02",
          "Ürün içerik uzmanı Ece Arslan, tükenmiş bir ürünün stok eşitleme gecikmesi yüzünden satılmaya devam ettiğini gördü. 36 sipariş etkilenmiş olabilir.",
          "Ece Arslan", "ürün içerik uzmanı", [
              S("Ürünü satıştan çıkarıp etkilenen siparişleri doğrulayın.", "Otoriter", -2, -3, 9, "Yeni yanlış satış durdu; 36 sipariş için çözüm gerekti."),
              S("Ece ve müşteri ekibiyle alternatif ürün, bekleme ve iade seçeneklerini sunun.", "Demokratik", 4, -2, 9, "Müşteriler seçim yaptı; çözüm maliyeti oluştu."),
              S("Ece'ye stok uyuşmazlığı uyarısı kurma görevi verin.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; mevcut siparişler ayrıca ele alındı."),
              S("Stok gelebilir diye ürünü satışta tutun.", "Kaçınmacı", -3, 5, -11, "Satış sürdü; etkilenen müşteri sayısı arttı."),
          ]),
        V("eti-03",
          "Kargo koordinatörü Burak Şahin, taşıyıcının üçüncü haftadır teslim hedefini tutturamadığını söylüyor. Alternatif taşıyıcının kapasitesi yalnızca siparişlerin yarısına yeterli.",
          "Burak Şahin", "kargo süreçleri koordinatörü", [
              S("Gecikmenin yoğun olduğu bölgeleri alternatife aktarın.", "Otoriter", -2, 5, 6, "Gecikme azaldı; iki taşıyıcıyı yönetmek karmaşıklaştı."),
              S("Burak ve müşteri ekibiyle bölge bazlı hizmet planı açıklayın.", "Demokratik", 4, -2, 8, "Beklentiler yönetildi; ek iletişim gerekti."),
              S("Burak'a taşıyıcı performansı ve geçiş eşiği planı hazırlatın.", "Koçvari", 5, 1, 5, "Gelecek kararlar veriye dayanacak; bugünkü gecikmeler sürdü."),
              S("Firma düzelir diye tüm siparişleri aynı şekilde vermeye devam edin.", "Kaçınmacı", -3, -4, -10, "Geçiş maliyeti oluşmadı; şikâyetler arttı."),
          ]),
        V("eti-04",
          "Müşteri deneyimi sorumlusu Zeynep Aydın, iade kodu oluşturma ekranının çalışmadığını bildiriyor. Yasal iade süresi yaklaşan müşteriler var.",
          "Zeynep Aydın", "müşteri deneyimi sorumlusu", [
              S("Onaylı alternatif iade kanalını açıp talep tarihlerini kayıt altına alın.", "Otoriter", -2, 3, 9, "Hak kaybı önlendi; manuel iş yükü oluştu."),
              S("Zeynep ve teknik ekiple müşteriye açık geçici süreç belirleyin.", "Demokratik", 4, -2, 8, "Müşteriler bilgilendi; koordinasyon sürdü."),
              S("Zeynep'e etkilenen talepleri günlük izleme sorumluluğu verin.", "Koçvari", 5, 1, 5, "Riskli iadeler görüldü; teknik çözüm ayrıca gerekti."),
              S("Ekran düzelince müşteriler yeniden dener diye bekleyin.", "Kaçınmacı", -4, -4, -11, "Manuel iş çıkmadı; müşterilerin süre kaygısı arttı."),
          ]),
        V("eti-05",
          "Ece Arslan, mont beden tablosunun yanlış olduğunu ve benzer gerekçeli iadelerin yükseldiğini söylüyor. Ürün çok satıyor; sayfayı kapatmak satış kaybettirecek.",
          "Ece Arslan", "ürün içerik uzmanı", [
              S("Yanlış tabloyu kaldırıp doğrulanmış ölçüler gelene kadar açık uyarı ekleyin.", "Otoriter", -2, -2, 9, "Yanıltıcı bilgi kalktı; dönüşüm azaldı."),
              S("Ece ve ürün ekibiyle doğru ölçüleri hızlıca doğrulayın.", "Demokratik", 4, -2, 8, "Tablo düzeldi; ekip ek ölçüm yaptı."),
              S("Ece'ye beden bilgisi kontrolünü ürün yayınına ekletin.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; geçmiş iadeler ayrıca yönetildi."),
              S("Satış güçlü diye tabloyu kampanya sonuna kadar bırakın.", "Kaçınmacı", -3, 5, -11, "Satış sürdü; iade maliyeti büyüdü."),
          ]),
        V("eti-06",
          "Burak Şahin, takip numaralarının müşterilere iki gün geç iletildiğini bildiriyor. Paketler gerçekte yolda; müşteri hizmetlerine 'Siparişim nerede?' talepleri yağıyor.",
          "Burak Şahin", "kargo süreçleri koordinatörü", [
              S("Doğrulanmış takip numaralarını toplu gönderip gecikmeyi açıklayın.", "Otoriter", -2, 4, 8, "Talep sayısı azaldı; toplu kontrol iş yükü doğdu."),
              S("Burak ve müşteri ekibiyle güvenilir teslim bilgisini ortak paylaşın.", "Demokratik", 4, -2, 8, "Mesaj tutarlılaştı; hazırlık zaman aldı."),
              S("Burak'a bildirim gecikmesi için otomatik uyarı kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski düştü; mevcut mesajlar ayrıca gönderildi."),
              S("Paketler yolda diye bildirimleri düzeltmeyin.", "Kaçınmacı", -3, -4, -10, "Ek iş olmadı; müşteri belirsizliği sürdü."),
          ]),
        V("eti-07",
          "Zeynep Aydın, yanlış ürün gönderildiğini anlatan müşteri paylaşımının yayıldığını bildiriyor. Sipariş kaydı müşterinin haklı olabileceğini gösteriyor.",
          "Zeynep Aydın", "müşteri deneyimi sorumlusu", [
              S("Siparişi doğrulatıp müşteriye özel kanaldan hızlı çözüm sunun.", "Otoriter", -2, 3, 8, "Müşteriyle temas kuruldu; kamuya açık beklenti ayrıca yönetildi."),
              S("Zeynep ve depo ekibiyle hatayı doğrulayıp uygun açıklamayı hazırlayın.", "Demokratik", 4, -2, 8, "Açıklama doğru oldu; ilk yanıt gecikti."),
              S("Zeynep'e benzer gönderiler için çözüm ve kök neden takibi verin.", "Koçvari", 5, 1, 5, "Süreç gelişti; müşterinin siparişi ayrıca düzeltildi."),
              S("Paylaşım geçer diye müşteriye dönüş yapmayın.", "Kaçınmacı", -4, -3, -11, "Ek açıklama yapılmadı; güven kaybı arttı."),
          ]),
        V("eti-08",
          "Ece Arslan, indirim kodunun koşulları karşılamayan sepetlerde de çalıştığını fark ediyor. Siparişler artıyor, fakat marj hızla düşüyor.",
          "Ece Arslan", "ürün içerik uzmanı", [
              S("Kuralı düzeltip etkilenen siparişleri adil uygulama için inceleyin.", "Otoriter", -2, -2, 9, "Yeni kayıp durdu; mevcut siparişler için çözüm gerekti."),
              S("Ece, finans ve müşteri ekibiyle mevcut siparişlere yaklaşımı belirleyin.", "Demokratik", 4, -2, 8, "Karar dengeli oldu; görüşme zaman aldı."),
              S("Ece'ye kampanya koşulları için yayın öncesi test kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; bugünkü kod ayrıca düzeltildi."),
              S("Satış hedefi tutuyor diye kodu kampanya sonuna kadar bırakın.", "Kaçınmacı", -3, 5, -11, "Sipariş arttı; kârlılık bozuldu."),
          ]),
        V("eti-09",
          "Burak Şahin, teslim edildi görünen bazı paketler için müşterilerin ürün almadığını söylüyor. Taşıyıcının teslim fotoğrafları bulanık.",
          "Burak Şahin", "kargo süreçleri koordinatörü", [
              S("İlgili teslimleri itiraz kaydına alıp taşıyıcıdan kanıt isteyin.", "Otoriter", -2, 3, 8, "İnceleme başladı; müşteriler sonuç bekliyor."),
              S("Burak ve müşteri ekibiyle her siparişe uygun geçici çözüm sunun.", "Demokratik", 4, -2, 8, "Müşteriler destek gördü; ek maliyet doğabilir."),
              S("Burak'a teslim kanıtı kalite eşiği oluşturtun.", "Koçvari", 5, 1, 5, "Sonraki kayıtlar iyileşecek; mevcut paketler ayrıca araştırıldı."),
              S("Teslim kaydı var diye müşteri taleplerini reddedin.", "Kaçınmacı", -4, 4, -11, "Dosyalar hızlı kapandı; haklı müşteriler mağdur olabilir."),
          ]),
        V("eti-10",
          "Zeynep Aydın, ödeme ekranında bazı bankaların kartlarında başarısızlık oranının arttığını bildiriyor. Alternatif ödeme yöntemleri çalışıyor.",
          "Zeynep Aydın", "müşteri deneyimi sorumlusu", [
              S("Sorunlu yöntemi işaretleyip sağlayıcıya acil olay kaydı açın.", "Otoriter", -2, 3, 8, "Başarısız denemeler azaldı; bazı müşteriler seçenek değiştirdi."),
              S("Zeynep ve teknik ekiple bankalara göre etkiyi ölçüp bilgi verin.", "Demokratik", 4, -2, 8, "Açıklama doğru yapıldı; ilk yanıt gecikti."),
              S("Zeynep'e ödeme başarısızlık oranı uyarısı kurdurun.", "Koçvari", 5, 1, 5, "Yeni sorun erken görülecek; mevcut hata ayrıca çözüldü."),
              S("Müşteriler başka kart dener diye uyarı göstermeyin.", "Kaçınmacı", -4, -4, -10, "Sayfa değişmedi; terk edilen sepetler arttı."),
          ]),
        V("eti-11",
          "Ece Arslan, ürün yorumlarında aynı dikiş sorununun tekrarlandığını bildiriyor. Depoda üründen büyük stok var; kalite kontrol örneklemesi daha önce geçmiş.",
          "Ece Arslan", "ürün içerik uzmanı", [
              S("Şüpheli partiyi geçici incelemeye alıp satış etkisini ölçün.", "Otoriter", -2, -4, 9, "Müşteri riski sınırlandı; stok bekledi."),
              S("Ece ve kaliteyle yorumları parti numarasına göre eşleştirin.", "Demokratik", 4, -2, 8, "Sorunlu parti ayırt edildi; inceleme zaman aldı."),
              S("Ece'ye yorumlardan kalite sinyali üreten süreç kurdurun.", "Koçvari", 5, 1, 5, "Gelecek işaretler erken görülecek; mevcut ürün ayrıca incelendi."),
              S("İlk test geçtiği için yorumları dikkate almayın.", "Kaçınmacı", -3, 4, -11, "Satış sürdü; iadeler artabilir."),
          ]),
        V("eti-12",
          "Merve Çelik, mobil uygulama afişinin yanlış ürün listesine yönlendirdiğini söylüyor. Kampanya görünürlüğü yüksek, ancak tıklayanların çoğu aradığını bulamıyor.",
          "Merve Çelik", "e-ticaret operasyon uzmanı", [
              S("Afişi geçici durdurup doğru listeye bağlantıyı doğrulayın.", "Otoriter", -2, 3, 8, "Yanlış yönlendirme durdu; görünürlük kısa süre düştü."),
              S("Merve ve pazarlamayla doğru ürün kapsamını birlikte belirleyin.", "Demokratik", 4, -2, 8, "Kapsam netleşti; düzeltme zaman aldı."),
              S("Merve'ye yayın öncesi bağlantı kontrolü kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; mevcut afiş ayrıca düzeltildi."),
              S("Kullanıcılar aramayla bulur diye afişi bırakın.", "Kaçınmacı", -3, -4, -10, "Görünürlük sürdü; deneyim bozuldu."),
          ]),
        V("eti-13",
          "Burak Şahin, ücretsiz kargo eşiğinin bazı sepetlerde yanlış hesaplandığını bildiriyor. Müşteri ödeme ekranında beklemediği kargo ücreti görüyor.",
          "Burak Şahin", "kargo süreçleri koordinatörü", [
              S("Hatalı hesaplamayı durdurup doğru koşulu sepetten önce gösterin.", "Otoriter", -2, -3, 9, "Yanlış ücret azaltıldı; kısa bakım gerekti."),
              S("Burak ve finansla etkilenen siparişler için tutarlı çözüm belirleyin.", "Demokratik", 4, -2, 8, "Müşteri kaybı azaldı; telafi maliyeti oluşabilir."),
              S("Burak'a kargo eşiği için test senaryoları hazırlatın.", "Koçvari", 5, 1, 5, "Tekrar riski düştü; bugünkü sepetler ayrıca düzeltildi."),
              S("Ödeyen müşteriler itiraz ederse bakın.", "Kaçınmacı", -3, 4, -11, "İşlem sürdü; gizli ücret algısı doğdu."),
          ]),
        V("eti-14",
          "Zeynep Aydın, müşteri hizmetleri sohbetinde bekleme süresinin 22 dakikaya çıktığını söylüyor. Taleplerin çoğu tek kargo gecikmesinden kaynaklanıyor.",
          "Zeynep Aydın", "müşteri deneyimi sorumlusu", [
              S("Kargo gecikmesini toplu duyurup temsilcileri özel durumlara ayırın.", "Otoriter", -2, 5, 6, "Bekleme azaldı; genel duyuru kişisel çözüm yerine geçmedi."),
              S("Zeynep ve kargo ekibiyle gerçek teslim takvimini doğrulayın.", "Demokratik", 4, -2, 8, "Yanıtlar doğru oldu; ilk duyuru gecikti."),
              S("Zeynep'e sık sorulan talepler için güncel yanıt akışı hazırlatın.", "Koçvari", 5, 1, 5, "Ekip hızlandı; sorunlu kargo ayrıca çözülmeli."),
              S("Yoğunluk geçer diye temsilci sayısını ve iletişimi değiştirmeyin.", "Kaçınmacı", -4, -5, -10, "Ek kaynak kullanılmadı; bekleme arttı."),
          ]),
        V("eti-15",
          "Ece Arslan, ürün başlığında organik içerik iddiası gördü. Tedarikçi belgesi sistemde bulunamıyor; ürünün satışı yüksek.",
          "Ece Arslan", "ürün içerik uzmanı", [
              S("Belge doğrulanana kadar iddiayı ürün sayfasından çıkarın.", "Otoriter", -2, -2, 10, "Yanıltıcı iddia riski azaldı; sayfanın çekiciliği düştü."),
              S("Ece ve satın almayla belge kaynağınılaın.", "Demokratik", 4, -2, 8, "İddia netleşti; kontrol zaman aldı."),
              S("Ece'ye ürün iddiaları için belge kontrolü kurdurun.", "Koçvari", 5, 1, 5, "Yeni sayfalar güvenli olacak; mevcut iddia ayrıca değerlendirildi."),
              S("Satış güçlü diye belgeyi kampanya sonrası isteyin.", "Kaçınmacı", -3, 5, -11, "Satış sürdü; doğrulanmamış vaat devam etti."),
          ]),
        V("eti-16",
          "Merve Çelik, ürün stoklarının gece yalnızca bir kez güncellendiğini söylüyor. Kampanya gününde hızlı tükenen ürünler için bu aralık çok uzun.",
          "Merve Çelik", "e-ticaret operasyon uzmanı", [
              S("Riskli ürünler için geçici satış tamponu koyun.", "Otoriter", -2, -2, 8, "Fazla satış azaldı; bazı gerçek stoklar geç satıldı."),
              S("Merve ve stok ekibiyle yüksek hızlı ürünlerde sık kontrol planlayın.", "Demokratik", 4, -2, 8, "Kontrol hedefli oldu; operasyon iş yükü arttı."),
              S("Merve'ye stok gecikme ölçümü ve uyarı görevi verin.", "Koçvari", 5, 1, 5, "Gecikmeler görünür oldu; eşitleme altyapısı ayrıca iyileştirilmeli."),
              S("Gece güncellemesi yeterlidir diyerek düzeni koruyun.", "Kaçınmacı", -3, 4, -10, "İş yükü değişmedi; fazla satış riski sürdü."),
          ]),
        V("eti-17",
          "Burak Şahin, bir müşteriye iki kez teslimat bildirimi gittiğini ama yalnızca tek paket gönderildiğini fark etti. Benzer mesajlar başka müşterilere de ulaşmış olabilir.",
          "Burak Şahin", "kargo süreçleri koordinatörü", [
              S("Bildirim akışını durdurup etkilenen müşterilere doğru bilgi gönderin.", "Otoriter", -2, -2, 9, "Yanlış bilgi durdu; ek mesaj trafiği oluştu."),
              S("Burak ve teknik ekiple çift bildirimin kapsamını doğrulayın.", "Demokratik", 4, -2, 8, "Düzeltme doğru kişilere yapıldı; hazırlık uzadı."),
              S("Burak'a bildirim tekrarı kontrolü kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; mevcut mesajlar ayrıca düzeltildi."),
              S("Paket doğru gitti diye mesajları önemsemeyin.", "Kaçınmacı", -3, 4, -10, "Ek iş çıkmadı; müşteriler ikinci paket bekledi."),
          ]),
        V("eti-18",
          "Zeynep Aydın, müşterinin değişim istediği ürünün stokta olmadığını söylüyor. İade yapılabilir; müşteri özellikle aynı ürünün farklı bedenini bekliyor.",
          "Zeynep Aydın", "müşteri deneyimi sorumlusu", [
              S("Gerçek stok durumunu açıkça bildirip iade ve bekleme seçeneklerini sunun.", "Otoriter", -2, 2, 8, "Beklenti netleşti; müşteri beklemeyi kabul etmeyebilir."),
              S("Zeynep ve stok ekibiyle diğer kanallarda uygun beden araştırın.", "Demokratik", 4, -2, 8, "Alternatif bulundu; transfer zaman aldı."),
              S("Zeynep'e değişim stok takibi ve geri dönüş planı verin.", "Koçvari", 5, 1, 5, "Takip iyileşti; ürün bulunması garanti değil."),
              S("Ürün gelebilir diye müşteriye tarih vermeden bekletin.", "Kaçınmacı", -3, -4, -10, "İade ertelendi; müşteri belirsizlik yaşadı."),
          ]),
        V("eti-19",
          "Ece Arslan, farklı satıcı kanallarında aynı ürünün iade koşullarının farklı yazıldığını fark ediyor. Müşteriler markadan tek yanıt bekliyor.",
          "Ece Arslan", "ürün içerik uzmanı", [
              S("Onaylı koşulu esas alıp yanlış kanal bilgisini düzeltin.", "Otoriter", -2, 2, 8, "Bilgi tutarlılaştı; geçmiş siparişlerin beklentisi incelenmeli."),
              S("Ece ve müşteri ekibiyle etkilenen siparişler için adil çözüm belirleyin.", "Demokratik", 4, -2, 8, "Müşteri etkisi gözetildi; çözüm maliyeti artabilir."),
              S("Ece'ye kanallar arası koşul kontrolü kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; eski siparişler ayrıca ele alındı."),
              S("Her kanal farklıdır deyip tutarsız metinleri bırakın.", "Kaçınmacı", -3, 4, -10, "Değişiklik yapılmadı; şikâyetler sürdü."),
          ]),
        V("eti-20",
          "Merve Çelik, ödeme sonrası teşekkür sayfasının hata verdiğini fakat bankadan ödeme onayı geldiğini söylüyor. Müşteriler işlemi tekrar deneyerek çift sipariş verebilir.",
          "Merve Çelik", "e-ticaret operasyon uzmanı", [
              S("Tekrar denemeyi önleyen geçici uyarı gösterip ödeme kayıtlarını kontrol edin.", "Otoriter", -2, -3, 9, "Çift işlem riski azaldı; ödeme sonrası akış yavaşladı."),
              S("Merve ve ödeme ekibiyle sipariş-onay eşleşmesini doğrulayın.", "Demokratik", 4, -2, 8, "Doğru müşteriler bilgilendirildi; inceleme zaman aldı."),
              S("Merve'ye ödeme sonrası akış için otomatik test kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; mevcut işlemler ayrıca kontrol edildi."),
              S("Banka onayı var diye teşekkür sayfasını sonra düzeltin.", "Kaçınmacı", -3, 4, -11, "Ödeme sürdü; çift işlem ve destek talebi arttı."),
          ]),
    ],
}


# ==========================================================
# KARARA BAĞLI DEVAM ZİNCİRLERİ
# ==========================================================
#
# Her departmanda iki zincir bulunur.
# Her zincirin açılışında dört karar vardır.
# Aynı zincirin devam vakasında olay metni, alınan karara
# özel olarak yazılmıştır. Devam metninde gerçek sonuç ve
# aynı kişinin rolü bulunur.
#
# Devam vakası mevcut vakadan hemen sonra zorunlu olarak
# gelmez; 1-2 bağımsız vakanın ardından gelebilir.
# ==========================================================

ZINCIRLER = {
    "Mağazacılık": [
        {
            "id": "mag-z1",
            "baslangic": V(
                "mag-z1-bas",
                "Kasiyer Ayşe Yıldız, indirimli ürünün kasada farklı fiyat çıktığını ve aynı hatanın başka bedenlerde de olabileceğini söylüyor. Müşteri kuyruğu büyürken kampanya merkezden aktif görünüyor. Ayşe hatayı saklamak yerine size bildirdi; satış akışını ve fiyat doğruluğunu birlikte yönetmeniz gerekiyor.",
                "Ayşe Yıldız",
                "kasiyer",
                [
                    S("Şüpheli ürünlerin satışını kısa süre durdurup fiyat listesini doğrulatın.", "Otoriter", -4, -4, 10, "Yanlış fiyatla satış durdu; mağaza yoğunluğunda satış kaybı oluştu."),
                    S("Ayşe ve reyon ekibiyle hatalı bedenleri ayırıp müşterilere tek uygulama duyurun.", "Demokratik", 5, -3, 8, "Müşteriler tutarlı bilgi aldı; ayırma işlemi kuyruk yarattı."),
                    S("Ayşe'ye fiyat kontrolünü yönettirip diğer kasaya yoğunluğu aktarın.", "Koçvari", 6, 4, 5, "Ayşe kontrolü sahiplendi; bazı ürünler kontrol sırası bekledi."),
                    S("İlk itirazları tek tek çözerek sistem düzeltmesini bekleyin.", "Kaçınmacı", -5, 2, -9, "İşlemler sürdü; farklı müşterilere farklı çözüm uygulanmaya başladı."),
                ],
            ),
            "devam_metinleri": [
                "Ayşe Yıldız'ın durdurduğu ürünlerde sorun yalnız bir etikette değil, beş bedende çıktı. Satış kaybı şikâyeti gelirken fiyat doğruluğu korundu. Bölge müdürü, kampanyayı aynı gün yeniden açmak için hangi kontrolün yeterli olacağını soruyor.",
                "Ayşe Yıldız'ın ekiple hazırladığı ortak açıklama müşterilerin tepkisini azalttı. Ancak reyon görevlileri hangi bedenlerin doğrulandığı konusunda iki farklı liste tutmuş. Kampanya sürerken tek güvenilir stok-fiyat kaydı oluşturmanız gerekiyor.",
                "Ayşe Yıldız'ın yönettiği kontrolde kuyruk azaldı; genç bir kasiyer kontrol bekleyen bir ürünü yanlışlıkla sattı. Ayşe hatayı size hemen iletti. Kişiyi suçlamadan işlemi ve kontrol sınırlarını nasıl ele alırsınız?",
                "Fiyat itirazları tek tek çözülürken bir müşteri, aynı ürünü arkadaşının daha farklı indirimle aldığını kanıtladı. Ayşe Yıldız tutarsızlığı görüyor ve kasadaki kayıtların topluca incelenmesi gerektiğini söylüyor.",
            ],
        },
        {
            "id": "mag-z2",
            "baslangic": V(
                "mag-z2-bas",
                "Depo sorumlusu Can Öztürk, yarının kampanya ürünü çocuk montlarında sistemden 18 adet eksik buldu. Mağaza müdür yardımcısı Zeynep Aydın reklamın zaten çıktığını söylüyor. Eksik stokun nedeni henüz bilinmiyor.",
                "Can Öztürk",
                "depo sorumlusu",
                [
                    S("Doğrulanmayan adetleri satışa kapatıp acil sayım başlatın.", "Otoriter", -3, -5, 9, "Yanlış stok vaadi azaldı; reklamla gelen müşterilerin seçenekleri daraldı."),
                    S("Can ve Zeynep'le raf, depo ve transfer kayıtlarını birlikte doğrulayın.", "Demokratik", 5, -3, 8, "Ekip ortak sayıya yaklaştı; kampanya açılışı gecikti."),
                    S("Can'a hareket kayıtlarının kök nedenini araştırma görevi verip doğrulanan stokla açın.", "Koçvari", 6, 3, 5, "Kampanya kısmen açıldı; Can eksik adedin izini sürüyor."),
                    S("İlk satışları yapıp farkı kampanya sonunda netleştirin.", "Kaçınmacı", -4, 5, -10, "Satış başladı; karşılanamayabilecek siparişler oluştu."),
                ],
            ),
            "devam_metinleri": [
                "Can Öztürk'ün sayımı, 18 monttan 11'inin başka mağazaya transfer edildiğini gösterdi. Satışa kapatma doğruydu; ancak reklamla gelen müşteriler mağazalar arası transfer bekliyor. Zeynep Aydın maliyetin kimden karşılanacağını soruyor.",
                "Can Öztürk ve Zeynep Aydın kayıtları karşılaştırınca transfer fişinin sisteme geç işlendiği görüldü. Mağazadaki gerçek stok netleşti ama kampanya açılışı bir saat gecikti. Bölge ekibi, müşterilere nasıl telafi sunulacağını soruyor.",
                "Can Öztürk, eksik montların yedisinin depoda yanlış lokasyonda olduğunu buldu; kalanları başka mağazaya gitmiş. Doğrulanan stokla kampanya açıldı. Şimdi hangi ürünleri mağazada tutup hangilerini müşterilere transferle sunacağınızı seçmelisiniz.",
                "Mont satışları başladıktan sonra stok fazladan beş müşteriye vaat edilmiş görünüyor. Can Öztürk gerçek sayımı tamamladı. Zeynep Aydın müşterilerle bugün iletişim kurulmasını istiyor; satış ekibi önce transfer bulmayı öneriyor.",
            ],
        },
    ],

    "Tedarik Zinciri": [
        {
            "id": "ted-z1",
            "baslangic": V(
                "ted-z1-bas",
                "Planlama uzmanı Derya Aksoy, 12 mağazaya gidecek ürünlerin gümrükte kaldığını ve elde yalnız altı mağazaya yetecek stok olduğunu bildirdi. Kampanya yarın başlayacak; hangi mağazalara öncelik verileceği satış sonuçlarını ve ekipler arası güveni etkileyecek.",
                "Derya Aksoy",
                "sevkiyat planlama uzmanı",
                [
                    S("Stoku en yüksek satış potansiyelli altı mağazaya tahsis edin.", "Otoriter", -3, 6, 5, "Satış fırsatı korundu; diğer mağazalar kararı adaletsiz buldu."),
                    S("Bölge ekipleriyle açık ölçüt belirleyip stok dağıtımını birlikte yapın.", "Demokratik", 4, -3, 9, "Dağıtım kabul gördü; araç çıkışı gecikti."),
                    S("Derya'ya alternatif ürün ve kısmi sevk planı hazırlatın.", "Koçvari", 5, 2, 5, "Alternatifler oluştu; bazı mağazalar ana ürünü alamadı."),
                    S("Gümrükten çıkış bekleyip mevcut kampanya planını değiştirmeyin.", "Kaçınmacı", -4, 3, -10, "Kampanya takvimi korundu; stoksuz mağazalar ortaya çıktı."),
                ],
            ),
            "devam_metinleri": [
                "Derya Aksoy'un yönlendirdiği altı mağazada ürün satışa çıktı; stok alamayan bir bölge müdürü seçimin gerekçesini istiyor. Gümrükten çıkış tarihi hâlâ belirsiz. Aynı bölgedeki alternatif ürünleri nasıl devreye alacaksınız?",
                "Derya Aksoy bölge ekipleriyle dağıtımı uzlaşıyla yaptı. Araç bir saat geç çıktı ve iki mağaza açılışa yetişemedi. Mağazalar kararın adil olduğunu söylüyor ama teslim performansı düştü; sonraki sevkiyatı nasıl düzenlersiniz?",
                "Derya Aksoy'un alternatif ürün planı mağazaların yarısında kabul gördü; üç mağaza müşterinin yalnız kampanya görselindeki ürünü istediğini bildiriyor. Sınırlı ana ürün stoğunu yeniden dağıtma baskısı oluştu.",
                "Kampanya başladı ve dört mağaza açılışta ürünsüz kaldı. Derya Aksoy gümrükten en erken yarın çıkış olacağını öğrendi. Mağazalar müşterilere ne söyleyeceğini soruyor; iletişim ve sevkiyat kararı birlikte verilmeli.",
            ],
        },
        {
            "id": "ted-z2",
            "baslangic": V(
                "ted-z2-bas",
                "Depo şefi Murat Demir, acil sevkiyatı yetiştirmek için forkliftlere dar bir koridorda çift yönlü hareket izni istiyor. İş güvenliği sorumlusu Selin Kaya bunun kabul edilemez olduğunu söylüyor. İki araç çıkışı için 90 dakika kaldı.",
                "Murat Demir",
                "depo operasyon şefi",
                [
                    S("Çift yönü yasaklayıp sevkiyatları öncelik sırasına göre tek yönden çıkarın.", "Otoriter", -3, -5, 10, "Güvenlik korundu; bir araç geç çıktı."),
                    S("Murat ve Selin'le güvenli alternatif rota için saha düzeni kurun.", "Demokratik", 4, -3, 9, "Güvenli yol bulundu; düzenleme zaman aldı."),
                    S("Murat'a güvenli tek yön kapasitesini ölçtürüp görevleri buna göre ayarlayın.", "Koçvari", 5, 1, 7, "Ekip gerçek kapasiteyi gördü; bazı hedefler küçüldü."),
                    S("Yalnız bu vardiyada çift yönlü kullanıma göz yumun.", "Kaçınmacı", -5, 6, -11, "Araçlar çıktı; güvenliğe ilişkin yakın tehlike bildirimi yapıldı."),
                ],
            ),
            "devam_metinleri": [
                "Murat Demir tek yönlü sevkiyatı tamamladı; geciken aracın taşıyıcısı ek bekleme ücreti istiyor. Selin Kaya güvenlik kararının tartışmaya açılmaması gerektiğini belirtiyor. Ücreti ve sonraki kapasite planını nasıl ele alırsınız?",
                "Murat Demir ve Selin Kaya alternatif rotayı açtı; geçici yönlendirme başka bir ekibin iade alanını daralttı. Güvenlik sağlandı fakat vardiyalar arası görev çatışması çıktı.",
                "Murat Demir'in ölçümü, mevcut hedefin güvenli kapasitenin %20 üstünde olduğunu gösterdi. Selin Kaya yönetime gerçek hedefin bildirilmesini istiyor; satış ekibi teslim tarihini korumakta ısrar ediyor.",
                "Çift yönlü vardiyada bir operatör ani fren yaptı; yaralanma olmadı. Murat Demir olayı size bildirdi, Selin Kaya kaydın açılmasını istiyor. Sevkiyat tamamlanmış olsa da şimdi nasıl hareket edersiniz?",
            ],
        },
    ],

    "Satın Alma": [
        {
            "id": "sat-z1",
            "baslangic": V(
                "sat-z1-bas",
                "Kalite sorumlusu Selin Kaya, sezon ürünü kumaşının seri üretimde onaylı numuneden farklı olduğunu buldu. Tedarikçi teslim tarihini korumak için partinin kabulünü istiyor; mağazalar kampanya için ürün bekliyor.",
                "Selin Kaya",
                "kalite sorumlusu",
                [
                    S("Partiyi durdurup sözleşmedeki uygunsuzluk sürecini başlatın.", "Otoriter", -3, -6, 10, "Kalite korundu; kampanya ürünsüz kalabilir."),
                    S("Selin ve üreticiyle uygun partileri ayırma ve kısmi teslim seçeneğini inceleyin.", "Demokratik", 4, -3, 8, "Kısmi teslim olasılığı doğdu; yoğun test gerekti."),
                    S("Selin'e hızlı yeniden test ve alternatif planı yönetme yetkisi verin.", "Koçvari", 5, 1, 6, "Sorun kapsamı netleşti; nihai teslim kararı bekliyor."),
                    S("Üreticinin sözüne güvenip partiyi teslim alın.", "Kaçınmacı", -4, 6, -11, "Teslim tarihi korundu; kalite şikâyeti riski taşındı."),
                ],
            ),
            "devam_metinleri": [
                "Selin Kaya'nın incelemesi, durdurulan partinin %40'ının standart dışı olduğunu doğruladı. Mağazalar kampanya için ürün bekliyor; tedarikçi kalan %60'ı ayrı teslim etmeyi öneriyor. Teslim riskini nasıl bölersiniz?",
                "Selin Kaya ve üretici partiyi ayırdı; uygun görünen %60'ın testleri olumlu. Ancak yeni paketleme ayrımı gecikmeye yol açacak. Kısmi kampanya ve müşteri beklentisi arasında karar vermelisiniz.",
                "Selin Kaya hızlı testte hatanın tek üretim hattıyla sınırlı olduğunu buldu. Tedarikçi hattı durdurdu ama yeniden üretim için ek maliyet istiyor. Kaliteyi korurken maliyet pazarlığını nasıl yürütürsünüz?",
                "Ürünler mağazaya dağıtıldıktan sonra ilk yıkama şikâyetleri geldi. Selin Kaya numune farkının olası neden olduğunu söylüyor. Satışları durdurmak ve müşterilere ulaşmak maliyetli olacak.",
            ],
        },
        {
            "id": "sat-z2",
            "baslangic": V(
                "sat-z2-bas",
                "Kategori yöneticisi Ece Arslan, yeni tedarikçinin %12 düşük fiyat verdiğini; ancak zorunlu uygunluk belgelerinin eksik olduğunu söylüyor. Teklif 48 saat geçerli. Alternatif onaylı tedarikçi daha pahalı.",
                "Ece Arslan",
                "kategori yöneticisi",
                [
                    S("Belge doğrulanana kadar siparişi açmayıp onaylı alternatifi hazırlayın.", "Otoriter", -2, -4, 10, "Uyum korundu; düşük fiyat fırsatı daraldı."),
                    S("Ece ve uyum ekibiyle 48 saatlik doğrulama planı kurun.", "Demokratik", 4, -3, 8, "Belge durumu görünür oldu; pazarlık zamanı azaldı."),
                    S("Ece'ye alternatif tedarik ve maliyet etkisi analizi yaptırın.", "Koçvari", 5, 1, 5, "Yedek seçenek netleşti; düşük fiyat için karar hâlâ gerekli."),
                    S("Belgeler sonra gelir diyerek düşük fiyatı sözlü kabul edin.", "Kaçınmacı", -3, 5, -11, "Fiyat tutuldu; uygunluk taahhüdü belirsiz kaldı."),
                ],
            ),
            "devam_metinleri": [
                "Ece Arslan, onaylı alternatifi ayarladı; yeni tedarikçi eksik belgenin bir hafta sonra hazır olacağını bildirdi. Alternatifin maliyeti yükseliyor fakat sezon teslimi güvenli. Sipariş hacmini nasıl paylaştırırsınız?",
                "Ece Arslan'ın 48 saatlik takibinde belgelerin bir kısmı doğrulandı, kritik bir denetim kaydı açık kaldı. Tedarikçi indirim süresini uzatmıyor. Riskin hangi kısmının kabul edilemeyeceğini belirlemelisiniz.",
                "Ece Arslan iki onaylı alternatif buldu: biri pahalı ama hızlı, diğeri ucuz ama geç teslim ediyor. Yeni tedarikçinin belgesi hâlâ eksik. Ürün önceliğine göre nasıl karar verirsiniz?",
                "Sözlü fiyat kabulünün ardından tedarikçi kapora talep etti. Ece Arslan uygunluk kaydı hâlâ gelmeden ödeme yapılamayacağını söylüyor; tedarikçi teklifi çekebilir.",
            ],
        },
    ],

    "İnsan Kaynakları": [
        {
            "id": "ik-z1",
            "baslangic": V(
                "İK iş ortağı Elif Demir, aynı terfiye iki güçlü adayın başvurduğunu söylüyor. Biri son yılın performansında, diğeri rolün kritik teknik becerisinde önde. Değerlendirme ölçütleri önceden yeterince açıklanmamış.",
                "Elif Demir",
                "İK iş ortağı",
                [
                    S("Rolün belgeli asgari gereklerini kullanıp kararı gerekçeli açıklayın.", "Otoriter", -3, 5, 7, "Karar çıktı; seçilmeyen aday gerekçeye itiraz edebilir."),
                    S("Elif'le bağımsız değerlendiricileri bir araya getirip ölçütleri kalibre edin.", "Demokratik", 4, -3, 9, "Karar daha savunulabilir oldu; terfi takvimi uzadı."),
                    S("Her iki adayla ayrı gelişim görüşmesi yapıp sonraki fırsatları planlayın.", "Koçvari", 7, -2, 6, "Adaylar destek gördü; seçim için yine nesnel karar gerekti."),
                    S("İki adayın tepkisini görmemek için terfiyi erteleyin.", "Kaçınmacı", -6, -4, -10, "Anlık itiraz çıkmadı; ekipte beklenti belirsizleşti."),
                ],
            ),
            "devam_metinleri": [
                "Elif Demir'in belgeli ölçütlerle açıkladığı terfi kararından sonra seçilmeyen aday, teknik katkısının küçümsendiğini söylüyor. Performans verisi doğru ama rolün değişen ihtiyaçları yeterince anlatılmamış. Güveni nasıl onarırsınız?",
                "Elif Demir'in kurduğu değerlendirme toplantısı kararı netleştirdi; adaylar sürecin uzamasına rağmen ölçütlerin neden şimdi belirlendiğini soruyor. Gelecek terfilerde adaleti gösterecek somut adım gerekiyor.",
                "Elif Demir, iki adayla gelişim görüşmesini tamamladı. Ancak bir aday terfi kararı olmadan verilen gelecek fırsat sözünü belirsiz buluyor. Açık pozisyon için seçim hâlâ yapılmalı.",
                "Terfi ertelendikten sonra iki adaydan biri başka ekipte iş aramaya başladı. Elif Demir, ertelemenin çatışmayı önlemediğini söylüyor. Artık hem pozisyon hem çalışan bağlılığı için karar vermelisiniz.",
            ],
        },
        {
            "id": "ik-z2",
            "baslangic": V(
                "İK uzmanı Zeynep Aydın, bir yöneticiyle ilgili anonim psikolojik taciz iddiası aldı. İddiada somut tarihler var; kimse suçun kanıtlandığını söylemiyor. Şikâyetçinin korunması ve yöneticinin adil değerlendirilmesi gerekiyor.",
                "Zeynep Aydın",
                "İK uzmanı",
                [
                    S("Tarafsız ve gizli resmî inceleme başlatıp kayıtları güvenceye alın.", "Otoriter", -2, -3, 10, "İddia ciddiye alındı; bilgi sızıntısına karşı dikkat gerekiyor."),
                    S("Zeynep ve uygun yetkililerle güvenli ifade alma planı hazırlayın.", "Demokratik", 4, -3, 9, "Süreç dikkatle kuruldu; ilk görüşmeler biraz gecikti."),
                    S("Zeynep'e bağımsız inceleme desteği verip tarafların ihtiyaçlarını izleyin.", "Koçvari", 5, -2, 7, "Destek mekanizması kuruldu; tarafsızlık yakından korunmalı."),
                    S("Yeni kanıt gelene kadar anonim iddiayı işleme almayın.", "Kaçınmacı", -7, 2, -12, "İddia bekledi; güvenli başvuru algısı zedelendi."),
                ],
            ),
            "devam_metinleri": [
                "Zeynep Aydın'ın başlattığı gizli incelemede iki çalışan benzer olaylar anlattı; yönetici iddiaları reddediyor. Bilgilerin ekipte yayılmasını önleyerek tarafların adil dinlenmesini nasıl sürdürürsünüz?",
                "Zeynep Aydın güvenli görüşmeleri planladı; bir çalışan tanıklık etmek istiyor ama kimliğinin yöneticiye ulaşmasından kaygılı. İncelemeyi geciktirmeden gizliliğin sınırlarını nasıl açıklarsınız?",
                "Zeynep Aydın taraflara destek sağladı; yöneticinin bazı çalışanların vardiyalarını değiştirdiği görüldü. Değişikliğin iş gerekçesi olabilir, fakat misilleme algısı oluştu. Ne yaparsınız?",
                "Başvuru beklerken aynı ekipten ikinci bir şikâyet geldi. Zeynep Aydın, önceki anonim bildirimin işlenmemesinin çalışanları etkilediğini söylüyor. İncelemenin kapsamını ve güvenli başvuru yolunu şimdi belirlemelisiniz.",
            ],
        },
    ],

    "Pazarlama": [
        {
            "id": "paz-z1",
            "baslangic": V(
                "Marka yöneticisi Selin Kaya, lansmana iki saat kala kampanya görselinde yanlış fiyat olduğunu fark etti. Reklam dosyası kanallara dağıtıldı; mağazalar doğru fiyatı kullanıyor. Görsellerin tamamını değiştirmek lansmanı geciktirecek.",
                "Selin Kaya",
                "marka yöneticisi",
                [
                    S("Yanlış fiyatlı yayını durdurup yalnız doğrulanan kanallarla başlayın.", "Otoriter", -2, -4, 10, "Yanlış vaat sınırlandı; erişim hedefi düştü."),
                    S("Selin ve satışla etkilenen kanalları belirleyip ortak düzeltme yayınlayın.", "Demokratik", 4, -3, 9, "Mesaj tutarlılaştı; lansman geç başladı."),
                    S("Selin'e hızlı düzeltme ve kanal teyidini koordine ettirin.", "Koçvari", 5, 1, 6, "Ekip çevik davrandı; birkaç kanal teyit bekledi."),
                    S("İlk reklamlar yayına girsin, fiyat itirazında düzeltme yapın.", "Kaçınmacı", -3, 5, -11, "Lansman yetişti; yanlış fiyat yayıldı."),
                ],
            ),
            "devam_metinleri": [
                "Selin Kaya yanlış fiyatlı yayını durdurdu. İki büyük kanalda doğru görsel hazır; küçük kanallarda kampanya görünmüyor. Satış ekibi erişim kaybını sorguluyor. Kalan kanalları nasıl açarsınız?",
                "Selin Kaya'nın koordinasyonuyla düzeltme yayımlandı; erken reklamı gören müşteriler mağazada eski fiyatı bekliyor. Düzeltmenin dürüst ve uygulanabilir olması için satışla nasıl hareket edersiniz?",
                "Selin Kaya kanalları tek tek kontrol ederken bir yerel hesap eski görseli paylaştı. Hesap yöneticisi uyarılmadığını söylüyor. Tekil hatayı düzeltirken kontrol sistemini nasıl kurarsınız?",
                "Yanlış fiyatlı reklam yayıldı ve müşteriler ekran görüntüsü paylaşıyor. Selin Kaya yalnız görseli silmenin yeterli olmadığını söylüyor. Müşteri beklentisini ve marka güvenini nasıl yönetirsiniz?",
            ],
        },
        {
            "id": "paz-z2",
            "baslangic": V(
                "Sosyal medya editörü Ece Arslan, iş birliği yapılan içerik üreticisinin tartışmalı paylaşımında marka etiketini gördü. Paylaşım doğrudan kampanyayla ilgili değil; sözleşmedeki davranış maddesinin uygulanıp uygulanmayacağı belirsiz.",
                "Ece Arslan",
                "sosyal medya editörü",
                [
                    S("Planlı iş birliği yayınını geçici durdurup sözleşmeyi inceleyin.", "Otoriter", -2, -4, 8, "Marka mesafe koydu; lansman içeriğinde boşluk oluştu."),
                    S("Ece, hukuk ve iletişimle doğrulanmış bilgiye dayalı karar verin.", "Demokratik", 4, -3, 9, "Tepki ölçülü oldu; karar gecikti."),
                    S("Ece'ye yedek içerik ve topluluk izleme planı hazırlatın.", "Koçvari", 5, 1, 6, "Ekip hazırlandı; iş birliği kararı yine gerekli."),
                    S("Paylaşım kampanya dışı diye takvimi değiştirmeyin.", "Kaçınmacı", -3, 5, -10, "Yayın sürdü; marka etiketine yönelik sorular arttı."),
                ],
            ),
            "devam_metinleri": [
                "Ece Arslan iş birliği yayınını durdurdu; içerik üreticisi sözleşmeye uyduğunu savunuyor ve kamuya açıklama istiyor. Hukuk değerlendirmesi sürerken marka adına hangi ölçüde iletişim kurarsınız?",
                "Ece Arslan'ın hukukla incelemesi paylaşımın bağlamının ilk aktarılandan farklı olduğunu gösterdi. Tepki azalıyor ama kampanyanın yeni tarihi belirsiz. Kararı hangi ölçüte bağlarsınız?",
                "Ece Arslan yedek içerikle lansmanı başlattı; içerik üreticisi kendisinin sessizce dışlandığını düşünüyor. Marka takvimi korunurken sözleşme ilişkisinde açıklığı nasıl sağlarsınız?",
                "Kampanya yayına girdi ve yorumlarda marka etiketine ilişkin sorular birikti. Ece Arslan hazır cevapların olayı küçümsediğini söylüyor. Yanıt çerçevesini nasıl kurarsınız?",
            ],
        },
    ],

    "Finans": [
        {
            "id": "fin-z1",
            "baslangic": V(
                "Finansal analist Ece Arslan, yönetim raporunda kârlılığı olduğundan yüksek gösteren hesaplama hatası buldu. Sunum yarın; düzeltme hedefin kaçtığını gösterecek. Hata onun hazırladığı tabloda oluşmuş ve Ece bunu kendisi size bildirdi.",
                "Ece Arslan",
                "finansal analist",
                [
                    S("Raporu düzeltip değişikliğin yönetim kararlarına etkisini önceden bildirin.", "Otoriter", -2, 2, 10, "Yönetim doğru veriyi gördü; ek açıklama beklentisi oluştu."),
                    S("Ece ve iş birimiyle hatanın tüm kapsamını teyit edip açıklama hazırlayın.", "Demokratik", 4, -3, 9, "Düzeltme güvenilir oldu; ekip yoğun çalıştı."),
                    S("Ece'ye düzeltmeyi ve kontrol tasarımını yönetme sorumluluğu verin.", "Koçvari", 6, 1, 6, "Ece hatayı sahiplendi; rapor yine yönetimle paylaşılmalı."),
                    S("Farkı sonraki raporda düzeltip mevcut sunumu değiştirmeyin.", "Kaçınmacı", -3, 5, -12, "Sunum yetişti; yanlış veriye dayalı karar riski oluştu."),
                ],
            ),
            "devam_metinleri": [
                "Ece Arslan'ın düzelttiği rapor yönetimle paylaşıldı. Üst yönetim yalnız hatayı değil, bu rakama dayanılarak daha önce verilen bütçe kararlarını da soruyor. Ece kendisini tek sorumlu ilan etmeye hazır; kontrol zincirini nasıl ele alırsınız?",
                "Ece Arslan ve iş birimi hatanın iki ayrı tablodan yayıldığını buldu. Rapor doğru ancak üç departmanın hedefi değişti. Yönetim kararı öncesi etkilenen ekiplerle nasıl iletişim kurarsınız?",
                "Ece Arslan düzeltme ve ikinci kontrol şablonunu hazırladı. Yönetim, zaman baskısında bu kontrolün gerçekten uygulanıp uygulanamayacağını soruyor. Gerçekçi kontrol ve hesap verebilirlik dengesini kurmalısınız.",
                "Eski rapor sunulduktan sonra yatırım ekibi rakamlara dayanarak ön onay verdi. Ece Arslan hatayı hâlâ düzeltebileceğinizi söylüyor; kararın resmileşmesini beklemek riski artıracak.",
            ],
        },
        {
            "id": "fin-z2",
            "baslangic": V(
                "Muhasebe uzmanı Ayşe Yıldız, ödemesi bugün yapılacak faturanın daha önce ödenmiş teslimata ait olabileceğini söylüyor. Tedarikçi ödeme gecikirse yeni sevkiyatı durduracağını bildirmiş.",
                "Ayşe Yıldız",
                "muhasebe uzmanı",
                [
                    S("Ödemeyi durdurup teslim ve sipariş eşleşmesini hemen doğrulayın.", "Otoriter", -2, -3, 10, "Çift ödeme riski önlendi; tedarikçi sevkiyatı bekletti."),
                    S("Ayşe ve satın alma ile iki faturayı tedarikçiyle birlikte karşılaştırın.", "Demokratik", 4, -3, 8, "Fark netleşti; çoklu görüşme gecikme yarattı."),
                    S("Ayşe'ye mükerrer ödeme kontrolü ve hızlı inceleme yetkisi verin.", "Koçvari", 5, 1, 6, "Ayşe sorunu sahiplendi; ödeme kararı teyit bekledi."),
                    S("Sevkiyat durmasın diye faturayı ödeyip sonra mahsuplaşın.", "Kaçınmacı", -3, 5, -11, "Sevkiyat ilerledi; geri alma yükü doğabilir."),
                ],
            ),
            "devam_metinleri": [
                "Ayşe Yıldız, faturanın gerçekten mükerrer olduğunu doğruladı. Tedarikçi kendi sistemindeki hatayı kabul ediyor ama durmuş sevkiyatı yeniden başlatmak için başka açık faturayı gündeme getiriyor.",
                "Ayşe Yıldız ve satın alma, faturalardan birinin ek hizmet bedeline ait olduğunu buldu; ancak hizmetin yazılı onayı yok. Sevkiyat acil. Ödeme ve yetki sorununu nasıl ayırırsınız?",
                "Ayşe Yıldız'ın kontrolü, iki faturanın aynı teslimatı farklı kodlarla gösterdiğini yakaladı. Tedarikçi düzeltme belgesi hazırlıyor; ödeme takviminde başka gerçek borçlar da var.",
                "Ödeme yapıldıktan sonra Ayşe Yıldız, faturanın mükerrer olduğunu kesinleştirdi. Tedarikçi iade yerine sonraki siparişe mahsup öneriyor. Nakit, kontrol ve ilişki açısından hangi yolu izlersiniz?",
            ],
        },
    ],

    "Bilgi Teknolojileri": [
        {
            "id": "bt-z1",
            "baslangic": V(
                "Sistem yöneticisi Emre Yılmaz, güvenlik güncellemesinden sonra mağaza kasalarının bir bölümünün çalışmadığını bildirdi. Geri alma satışları açacak ancak kapatılan güvenlik açığını yeniden ortaya çıkarabilir.",
                "Emre Yılmaz",
                "sistem yöneticisi",
                [
                    S("Riskli erişimleri sınırlayıp sorunlu mağazalarda kontrollü geri alma yapın.", "Otoriter", -2, 4, 8, "Kasalar açıldı; geçici güvenlik önlemleri izlenmeli."),
                    S("Emre ve güvenlik ekibiyle mağaza bazlı etkiyi ölçüp kademeli çözüm uygulayın.", "Demokratik", 4, -3, 9, "Riskler dengelendi; ilk mağazalar bekledi."),
                    S("Emre'ye satış ve güvenlik ekiplerini ayrı iş akışlarında koordine ettirin.", "Koçvari", 5, 1, 6, "İş bölümü netleşti; karar noktaları sıklaştı."),
                    S("Güncelleme düzelir diye bir süre müdahale etmeyin.", "Kaçınmacı", -5, -7, -11, "Güvenlik açığı kapalı kaldı; satış kaybı büyüdü."),
                ],
            ),
            "devam_metinleri": [
                "Emre Yılmaz kontrollü geri almayla kasaları açtı. Güvenlik ekibi geri dönen mağazalarda ek izleme gerekiyor diyor; mağazacılık bu önlemin işlem hızını düşürdüğünü bildiriyor. Geçici tedbirin sınırını nasıl koyarsınız?",
                "Emre Yılmaz'ın kademeli çözümü mağazaların çoğunda çalıştı; üç mağazada sorun sürdü. Güvenlik ekibi toplu geri almayı istemiyor. Üç mağazaya özel çözüm ve iletişimi nasıl kurarsınız?",
                "Emre Yılmaz ekipleri ayırdı ve kasa kesintisi azaldı; güvenlik ekibi değişikliklerin tek kayıt altında toplanmadığını fark etti. Hızlı müdahalenin izlenebilirliğini nasıl geri kurarsınız?",
                "Müdahale beklerken yoğun saat başladı; mağazalar müşterilere işlem yapamadığını bildiriyor. Emre Yılmaz güncellemenin kendiliğinden düzelmeyeceğini doğruladı. Güvenlik ve hizmet sürekliliği için hemen karar vermelisiniz.",
            ],
        },
        {
            "id": "bt-z2",
            "baslangic": V(
                "Siber güvenlik uzmanı Deren Aksoy, müşteri verisini etkileyebilecek bir açık buldu. Şu an ihlal kanıtı yok; çevrim içi servisi tamamen kapatmak satışları durduracak. Deren kanıtın korunması gerektiğini vurguluyor.",
                "Deren Aksoy",
                "siber güvenlik uzmanı",
                [
                    S("Riskli bileşeni izole edip olay müdahalesini başlatın.", "Otoriter", -2, -5, 10, "Maruziyet sınırlandı; bazı kullanıcı işlemleri durdu."),
                    S("Deren ve hukuk-iş ekipleriyle erişim sınırı ve iletişim planı kurun.", "Demokratik", 4, -3, 9, "Önlem tutarlı oldu; karar süresi uzadı."),
                    S("Deren'e izleme ve delil koruma akışını yönetme yetkisi verin.", "Koçvari", 5, 1, 6, "Kanıt korundu; erişim kararı tekrar değerlendirilmeli."),
                    S("İhlal kanıtı çıkana kadar normal yayına devam edin.", "Kaçınmacı", -4, 5, -12, "Satış kesilmedi; olası maruziyet devam etti."),
                ],
            ),
            "devam_metinleri": [
                "Deren Aksoy riskli bileşeni izole etti; bazı müşteriler hesaplarına ulaşamıyor. İnceleme bir saldırı girişimi gösteriyor fakat veri çıkışı doğrulanmadı. Hizmeti kademeli açma ölçütlerini belirlemelisiniz.",
                "Deren Aksoy'un ekiplerle hazırladığı plan sayesinde riskli erişim sınırlandı. İnceleme, geçmiş haftaya ait şüpheli bir oturum buldu. Henüz veri çıkışı kanıtı yok; bilgi ve bildirim kararını nasıl yönetirsiniz?",
                "Deren Aksoy delilleri korudu ve izleme açık kullanım girişimleri buldu. Servis çalışıyor ama risk devam ediyor. İzleme yeterli mi, hangi bileşen ne süreyle kapatılmalı?",
                "Normal yayın sürerken Deren Aksoy şüpheli hesap erişimleri gördü. Bazılarının meşru olup olmadığı belirsiz; beklemek kanıt kaybına yol açabilir. İlk 30 dakikalık kararınız ne olur?",
            ],
        },
    ],

    "E-Ticaret": [
        {
            "id": "eti-z1",
            "baslangic": V(
                "Ürün içerik uzmanı Ece Arslan, tükenmiş bir montun stok eşitleme gecikmesiyle satılmaya devam ettiğini buldu. İlk incelemede 36 sipariş etkilenmiş olabilir; yeni stok tarihi kesin değil.",
                "Ece Arslan",
                "ürün içerik uzmanı",
                [
                    S("Ürünü durdurup etkilenen siparişleri doğrulama sırasına alın.", "Otoriter", -2, -3, 9, "Yeni fazla satış durdu; sipariş sahipleri açıklama bekliyor."),
                    S("Ece ve müşteri ekibiyle bekleme, alternatif ürün ve iade seçenekleri sunun.", "Demokratik", 4, -3, 9, "Müşteriler seçim yaptı; telafi yükü oluştu."),
                    S("Ece'ye siparişleri gruplandırıp stok uyarısı tasarlama görevi verin.", "Koçvari", 5, 1, 6, "Etkilenenler ayrıldı; acil müşteri yanıtı hâlâ gerekli."),
                    S("Yeni stok gelebilir diye satışa devam edin.", "Kaçınmacı", -4, 5, -11, "Satış arttı; teslim edilemeyecek sipariş sayısı büyüdü."),
                ],
            ),
            "devam_metinleri": [
                "Ece Arslan satışları durdurunca toplam 36 etkilenen sipariş doğrulandı. Tedarik ekibi aynı monttan 20 adet bulabildi; kalan müşterilere ne önerileceği belirsiz. Tahsis ve iletişimi nasıl yönetirsiniz?",
                "Ece Arslan'ın hazırladığı seçeneklerden bazı müşteriler beklemeyi seçti. Tedarikçi kesin teslim tarihi veremiyor; müşteriye verilen beklentiyi yeniden değerlendirmek gerekiyor.",
                "Ece Arslan siparişleri gruplandırdı; 12 müşteri ürünü hediye için belirli tarihe yetiştirmek istiyor. Alternatif ürün var ama renk farklı. Kimlerle önce, hangi açıklamayla iletişim kurarsınız?",
                "Satışa devam edildiği için etkilenen sipariş 58'e çıktı. Ece Arslan henüz kesin stok tarihi olmadığını söylüyor. Satışı durdurmak ve mevcut müşterilerin haklarını ele almak artık acil.",
            ],
        },
        {
            "id": "eti-z2",
            "baslangic": V(
                "Kargo koordinatörü Burak Şahin, taşıyıcının üç haftadır geciktiğini ve alternatif firmanın kapasitesinin siparişlerin yalnız yarısına yettiğini söylüyor. Müşteri hizmetleri talepleri artıyor.",
                "Burak Şahin",
                "kargo süreçleri koordinatörü",
                [
                    S("En çok geciken bölgeleri alternatif taşıyıcıya aktarın.", "Otoriter", -2, 5, 6, "Bazı teslimler hızlandı; diğer bölgeler değişim istedi."),
                    S("Burak ve müşteri ekibiyle bölgesel gerçekçi teslim sözleri verin.", "Demokratik", 4, -3, 9, "Beklentiler düzeldi; gecikme yine sürdü."),
                    S("Burak'a taşıyıcı performans eşiği ve geçiş planı hazırlatın.", "Koçvari", 5, 1, 6, "Geçiş planı oluştu; bugünkü şikâyetler çözüm bekliyor."),
                    S("Mevcut firmaya bir hafta daha müdahalesiz devam edin.", "Kaçınmacı", -4, -4, -10, "Geçiş maliyeti çıkmadı; gecikmeler tekrarlandı."),
                ],
            ),
            "devam_metinleri": [
                "Burak Şahin alternatif taşıyıcıyı geciken bölgelere yönlendirdi; toplam teslim süresi azaldı fakat bir taşıyıcının takip numaraları geç geliyor. Müşteri güvenini koruyacak operasyon düzeni gerekiyor.",
                "Burak Şahin gerçekçi teslim tarihlerini duyurdu. Müşteriler şeffaflığı olumlu karşıladı ama eski reklamlar hâlâ hızlı teslim vaat ediyor. Kanal mesajlarını nasıl eşlersiniz?",
                "Burak Şahin'in planına göre mevcut firma bir hafta içinde hizmet düzeyine dönmezse siparişler kademeli aktarılacak. Firma düzelme sözü veriyor fakat ölçüm yöntemine itiraz ediyor.",
                "Müdahalesiz haftada geciken siparişler arttı ve sosyal medyada şikâyetler birikti. Burak Şahin alternatif taşıyıcının hâlâ yarım kapasite sunduğunu söylüyor. Sınırlı kapasiteyi nasıl kullanırsınız?",
            ],
        },
    ],
}


def devam_secenekleri_uret(departman, zincir_no):
    """
    Devam sorularının seçenekleri de ilgili departmanın gerçek
    iş sürecine göre yazılmıştır. Her devamda dört seçenek vardır.
    """

    secenek_haritasi = {
        "Mağazacılık": [
            [
                S("Doğrulanmış ürün ve fiyat listesini esas alıp geçici satış kuralını yazılı duyurun.", "Otoriter", -2, 4, 8, "Tutarlı satış sağlandı; ekipten ek kontrol istendi."),
                S("Ayşe ve reyon ekibiyle müşteriye verilen sözleri karşılaştırıp ortak telafi belirleyin.", "Demokratik", 4, -3, 9, "Farklı vaatler dengelendi; işlem süresi uzadı."),
                S("Ayşe'ye kasa-reyon teyit akışını pilot olarak yönetme yetkisi verin.", "Koçvari", 6, 1, 5, "Ayşe kontrolü sahiplendi; pilot takip istedi."),
                S("Kampanya bitsin diye kalan farkları müşteri itirazlarına göre çözün.", "Kaçınmacı", -4, 4, -10, "Satış sürdü; uygulama farklılıkları devam etti."),
            ],
            [
                S("Doğrulanan stoğu sabitleyip eksik ürün için resmî transfer açın.", "Otoriter", -2, 4, 8, "Yanlış satış önlendi; transfer maliyeti arttı."),
                S("Can ve Zeynep'le müşterileri gerçek teslim seçeneklerine göre bilgilendirin.", "Demokratik", 4, -3, 9, "Beklenti doğru yönetildi; ekip zaman ayırdı."),
                S("Can'a stok-fiş eşleşmesini ve günlük kontrolü yönetme sorumluluğu verin.", "Koçvari", 5, 1, 5, "Tekrar riski azaldı; açık siparişler ayrıca çözüldü."),
                S("Kesin transfer tarihini bekleyip müşteri iletişimini erteleyin.", "Kaçınmacı", -4, 3, -10, "Eksik bilgi verilmedi; müşteriler belirsiz kaldı."),
            ],
        ],
        "Tedarik Zinciri": [
            [
                S("Doğrulanmış stok ve satış etkisine göre yeni sevkiyat sırası belirleyin.", "Otoriter", -2, 4, 7, "Sevkiyat netleşti; bazı mağazalar ikinci sırada kaldı."),
                S("Derya ve bölge ekipleriyle alternatif ürün ve teslim beklentisini eşleyin.", "Demokratik", 4, -3, 9, "Mağazalar planı anladı; koordinasyon uzadı."),
                S("Derya'ya yeni gümrük gecikmeleri için erken uyarı akışı kurdurun.", "Koçvari", 5, 1, 5, "Gelecek risk görünür olacak; mevcut gecikme ayrıca yönetildi."),
                S("Gümrük çıkışı kesinleşmeden yeni plan açıklamayın.", "Kaçınmacı", -4, 3, -10, "Yanlış tarih verilmedi; mağazalar plansız kaldı."),
            ],
            [
                S("Güvenli kapasiteyi esas alıp araç takvimini yeniden resmileştirin.", "Otoriter", -2, -3, 9, "Güvenlik korundu; bazı teslimler gecikti."),
                S("Murat ve Selin'le vardiyalar arası güvenli görev ve alan planı yapın.", "Demokratik", 4, -3, 9, "Çatışma azaldı; düzenleme zaman aldı."),
                S("Murat'a ölçülen kapasiteyi gelecek hedeflere yansıtma sorumluluğu verin.", "Koçvari", 5, 1, 6, "Hedefler gerçekçileşti; bugünkü gecikme ayrıca ele alındı."),
                S("Tekrarlanmaz diye olayı yalnız sözlü değerlendirin.", "Kaçınmacı", -5, 3, -11, "İş devam etti; riskin izi kayboldu."),
            ],
        ],
        "Satın Alma": [
            [
                S("Testten geçen miktarı yazılı kalite şartıyla ayrı teslim alın.", "Otoriter", -2, 2, 8, "Kısmi ürün sağlandı; kampanya hacmi azaldı."),
                S("Selin, planlama ve mağazalarla kısmi kampanya kapsamını belirleyin.", "Demokratik", 4, -3, 9, "Beklenti gerçekçi oldu; lansman planı değişti."),
                S("Selin'e partileri ve yeni üretimi ayrı izleyecek kontrol verin.", "Koçvari", 5, 1, 5, "Kalite izi güçlendi; takvim baskısı sürdü."),
                S("Kalan parti gelir diye kalite açıklamasını mağazalara yapmayın.", "Kaçınmacı", -4, 3, -10, "İletişim kolaylaştı; mağazalar gerçek kapasiteyi bilmedi."),
            ],
            [
                S("Eksik uygunluk tamamlanmadan riskli tedarikçiye sipariş açmayın.", "Otoriter", -2, -3, 9, "Uyum korundu; düşük fiyat fırsatı azaldı."),
                S("Ece ve uyum ekibiyle onaylı seçeneklerin toplam etkisini değerlendirin.", "Demokratik", 4, -3, 9, "Karar savunulabilir oldu; zaman daraldı."),
                S("Ece'ye onaylı kapasite ve bütçe için bölünmüş tedarik planı hazırlatın.", "Koçvari", 5, 1, 5, "Esneklik sağlandı; yönetim onayı gerekti."),
                S("Belge riski düşük olabilir diyerek kapora veya sipariş verin.", "Kaçınmacı", -4, 4, -11, "Fiyat korundu; uygunluk riski devam etti."),
            ],
        ],
        "İnsan Kaynakları": [
            [
                S("Terfi ölçütlerini ve gerekçeyi kişiye özel görüşmede açıkça paylaşın.", "Otoriter", -2, 2, 8, "Karar netleşti; hayal kırıklığı hemen bitmedi."),
                S("Elif'le adayların sorularını ayrı dinleyip gelecekteki ölçütleri yayımlayın.", "Demokratik", 4, -3, 9, "Adalet algısı güçlendi; süreç zaman aldı."),
                S("Adaylar için ölçülebilir gelişim fırsatları ve takip tarihleri oluşturun.", "Koçvari", 7, 1, 6, "Gelişim yolu netleşti; pozisyon kararı yine açıklanmalı."),
                S("Zamanla kabullenirler diye itirazları yanıtsız bırakın.", "Kaçınmacı", -5, 3, -10, "Tartışma azaldı; bağlılık sorunu sürdü."),
            ],
            [
                S("Gizli ve tarafsız incelemeyi resmî yetkili ekiple sürdürün.", "Otoriter", -2, -3, 10, "Süreç korundu; taraflarda belirsizlik devam etti."),
                S("Zeynep'le tanıklara gizliliğin sınırlarını ve destek kanallarını anlatın.", "Demokratik", 4, -3, 9, "Güvenli katılım arttı; görüşmeler uzadı."),
                S("Zeynep'e tarafları koruyan ara önlemleri düzenli kontrol ettirin.", "Koçvari", 5, 1, 7, "Misilleme riski izlendi; inceleme ayrıca devam etti."),
                S("İnceleme bitene kadar yeni gelişmeleri işlemeyin.", "Kaçınmacı", -6, 3, -11, "İş yükü azaldı; koruma açığı oluştu."),
            ],
        ],
        "Pazarlama": [
            [
                S("Onaylı fiyatı tek kaynak yapıp tüm kanal düzeltmelerini doğrulayın.", "Otoriter", -2, 3, 8, "Mesaj tutarlı oldu; yayın kapasitesi daraldı."),
                S("Selin ve satışla yanlış görseli gören müşteriler için ortak uygulama belirleyin.", "Demokratik", 4, -3, 9, "Müşteri beklentisi gözetildi; süreç uzadı."),
                S("Selin'e kanal bazlı ön onay ve doğrulama planı kurdurun.", "Koçvari", 5, 1, 5, "Tekrar riski düştü; mevcut görseller yine düzeltildi."),
                S("Düzeltme fark edilir diye yalnız hatalı görselleri sessizce silin.", "Kaçınmacı", -4, 3, -10, "Görsel kalktı; eski vaatle gelen müşteriler yanıtsız kaldı."),
            ],
            [
                S("Sözleşme ve doğrulanmış bilgiye göre geçici yayın sınırı koyun.", "Otoriter", -2, -2, 8, "Risk sınırlandı; içerik takvimi daraldı."),
                S("Ece, hukuk ve iletişimle tutarlı iç ve dış yanıt belirleyin.", "Demokratik", 4, -3, 9, "Mesaj dengeli oldu; karar gecikti."),
                S("Ece'ye yedek içerik ve yorum takibini yönetme alanı verin.", "Koçvari", 5, 1, 5, "Ekip hazırlandı; iş birliği kararı yine gerekiyor."),
                S("Yorumlar azalır diye konuyu yanıtsız bırakın.", "Kaçınmacı", -4, 3, -10, "Ek açıklama olmadı; belirsizlik sürdü."),
            ],
        ],
        "Finans": [
            [
                S("Düzeltmenin etkilediği önceki kararları tek tek tespit edip raporlayın.", "Otoriter", -2, -3, 10, "Kararlar doğru veriyle gözden geçirildi; iş yükü arttı."),
                S("Ece ve iş birimleriyle etkileri ortak ve yazılı olarak değerlendirin.", "Demokratik", 4, -3, 9, "Etki paylaşıldı; süreç uzadı."),
                S("Ece'ye uygulanabilir ikinci kontrolü pilot olarak yönettirin.", "Koçvari", 5, 1, 6, "Kontrol denendi; geçmiş kararlar ayrıca düzeltildi."),
                S("Hata düzeltildi diye önceki kararları incelemeyin.", "Kaçınmacı", -4, 3, -11, "İş azaldı; yanlış verinin etkisi kalabilir."),
            ],
            [
                S("Doğrulanmış borçla tartışmalı kalemi ayırıp yazılı ödeme planı sunun.", "Otoriter", -2, 2, 9, "Doğru ödeme korundu; tedarikçiyle pazarlık sürdü."),
                S("Ayşe ve satın almayla hizmet ve teslim belgelerini ortak doğrulayın.", "Demokratik", 4, -3, 9, "Uyuşmazlık netleşti; ödeme gecikti."),
                S("Ayşe'ye tedarikçi-fatura eşleştirme kontrolünü kurdurun.", "Koçvari", 5, 1, 6, "Tekrar riski azaldı; mevcut açık fatura ayrıca çözüldü."),
                S("Sevkiyat çıksın diye belirsiz kalemi koşulsuz ödeyin.", "Kaçınmacı", -4, 4, -11, "Sevkiyat ilerledi; ödeme kontrolü zayıfladı."),
            ],
        ],
        "Bilgi Teknolojileri": [
            [
                S("Mağaza bazlı güvenli açılış ölçütü koyup tüm değişiklikleri kaydedin.", "Otoriter", -2, 2, 9, "İzlenebilir hizmet döndü; açılış kademeli oldu."),
                S("Emre, güvenlik ve mağazacılıkla etkiyi birlikte gözden geçirin.", "Demokratik", 4, -3, 9, "Karar dengeli oldu; toplantı zamanı gerekti."),
                S("Emre'ye müdahale kayıtlarını ve geçici önlemleri koordine ettirin.", "Koçvari", 5, 1, 6, "Süreç toparlandı; kök neden hâlâ çözülmeli."),
                S("Kasalar çalışıyor diye geçici güvenlik tedbirlerini izlemeden bırakın.", "Kaçınmacı", -4, 3, -11, "İşlem hızı korundu; açık yeniden oluşabilir."),
            ],
            [
                S("Olay müdahalesinde erişim sınırını kanıta göre güncelleyin.", "Otoriter", -2, -3, 10, "Risk sınırlı kaldı; bazı kullanıcılar hizmet alamadı."),
                S("Deren ve ilgili ekiplerle kanıt, bildirim ve hizmet ölçütlerini netleştirin.", "Demokratik", 4, -3, 9, "Karar gerekçelendi; ekip yoğun çalıştı."),
                S("Deren'e kanıt zinciri ve periyodik risk güncellemesi yönettirin.", "Koçvari", 5, 1, 6, "İzleme güçlü oldu; hizmet sınırı ayrıca kararlaştırıldı."),
                S("İnceleme bitene kadar müşteriye veya ilgili ekiplere bilgi vermeyin.", "Kaçınmacı", -4, 3, -11, "Erken açıklama yapılmadı; güven ve hazırlık azaldı."),
            ],
        ],
        "E-Ticaret": [
            [
                S("Kesin stoğu doğrulayıp siparişleri şeffaf tahsis ölçütüne göre ayırın.", "Otoriter", -2, 2, 9, "Dağıtım netleşti; bazı müşteriler ürünü alamadı."),
                S("Ece ve müşteri ekibiyle kişiye uygun seçenekleri gerçek tarihlerle sunun.", "Demokratik", 4, -3, 9, "Müşteri seçimi korundu; iletişim iş yükü arttı."),
                S("Ece'ye fazla satış uyarısı ve etkilenen sipariş takibi verin.", "Koçvari", 5, 1, 6, "Tekrar riski azaldı; mevcut müşteriler ayrıca desteklendi."),
                S("Yeni stok gelebilir diye kesin çözümü bir süre daha erteleyin.", "Kaçınmacı", -4, 3, -11, "Anlık iptal yapılmadı; belirsizlik büyüdü."),
            ],
            [
                S("Hizmet düzeyine göre taşıyıcı geçiş eşiğini resmileştirin.", "Otoriter", -2, 2, 8, "Geçiş ölçülebilir oldu; ek maliyet çıkabilir."),
                S("Burak ve müşteri ekibiyle kanallardaki teslim vaatlerini eşleyin.", "Demokratik", 4, -3, 9, "Beklenti düzeldi; reklam revizyonu gerekti."),
                S("Burak'a takip numarası ve gecikme için canlı izleme görevi verin.", "Koçvari", 5, 1, 6, "Erken uyarı oluştu; geciken siparişler ayrıca çözüldü."),
                S("Taşıyıcının düzeleceği sözünü ölçüm olmadan kabul edin.", "Kaçınmacı", -4, 3, -10, "İlişki değişmedi; hizmet sorunu sürdü."),
            ],
        ],
    }

    return secenek_haritasi[departman][zincir_no]


# Devam seçeneklerini zincire ekle.
for departman_adi, zincir_listesi in ZINCIRLER.items():
    for zincir_indeksi, zincir in enumerate(zincir_listesi):
        zincir["devam_secenekleri"] = devam_secenekleri_uret(
            departman_adi,
            zincir_indeksi,
        )


# ==========================================================
# VERİ DOĞRULAMA
# ==========================================================

def veriyi_dogrula():
    for departman_adi in DEPARTMANLAR:
        if len(VAKALAR[departman_adi]) < 20:
            raise ValueError(
                f"{departman_adi} için en az 20 bağımsız vaka gerekli."
            )

        if len(ZINCIRLER[departman_adi]) < 2:
            raise ValueError(
                f"{departman_adi} için en az 2 devam zinciri gerekli."
            )

        tum_vakalar = list(VAKALAR[departman_adi])

        for zincir in ZINCIRLER[departman_adi]:
            tum_vakalar.append(zincir["baslangic"])

            if len(zincir["devam_metinleri"]) != 4:
                raise ValueError(
                    f"{zincir['id']}: dört karar için dört devam metni gerekli."
                )

            if len(zincir["devam_secenekleri"]) != 4:
                raise ValueError(
                    f"{zincir['id']}: devamda dört seçenek gerekli."
                )

        kimlikler = [vaka["id"] for vaka in tum_vakalar]

        if len(kimlikler) != len(set(kimlikler)):
            raise ValueError(
                f"{departman_adi}: tekrarlanan vaka kimliği var."
            )

        for vaka in tum_vakalar:
            if len(vaka["secenekler"]) != 4:
                raise ValueError(
                    f"{vaka['id']}: vaka tam dört seçenek içermeli."
                )

            for secenek in vaka["secenekler"]:
                if secenek["tip"] not in TIP_RENK:
                    raise ValueError(
                        f"{vaka['id']}: bilinmeyen liderlik tipi."
                    )

                if set(secenek["etki"]) != {
                    "Moral",
                    "Verimlilik",
                    "Güven",
                }:
                    raise ValueError(
                        f"{vaka['id']}: eksik veya fazla metrik."
                    )


veriyi_dogrula()


# ==========================================================
# OTURUM DURUMU
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
        "kullanilan_vakalar": [],
        "karakterler": {},
        "bekleyen_devamlar": [],
        "baslayan_zincirler": [],
        "son_vaka_devam_miydi": False,
    }


for anahtar, deger in yeni_oyun_durumu().items():
    if anahtar not in st.session_state:
        st.session_state[anahtar] = deger


def oyunu_sifirla():
    for anahtar, deger in yeni_oyun_durumu().items():
        st.session_state[anahtar] = deger

    st.rerun()


# ==========================================================
# KARAKTER YÖNETİMİ
# ==========================================================

def karakter_kaydet(kisi, rol, etki=None, karar_ozeti=None):
    """
    Sadece vakanın metninde gerçekten adı geçen karakteri
    yan panelde gösterir. Rastgele karakter üretmez.
    """
    if not kisi:
        return

    kayit = st.session_state.karakterler.setdefault(
        kisi,
        {
            "rol": rol or "ekip üyesi",
            "iliski": 50,
            "son_etkilesim": "",
        },
    )

    if rol:
        kayit["rol"] = rol

    if etki is not None:
        kayit["iliski"] = max(
            0,
            min(
                100,
                kayit["iliski"] + etki.get("Güven", 0),
            ),
        )

    if karar_ozeti:
        kayit["son_etkilesim"] = karar_ozeti


# ==========================================================
# SENARYO MOTORU
# ==========================================================

def vaka_kopyala(vaka):
    """
    Orijinal havuz verisini değiştirmeden ekrana verilen
    senaryoyu oluşturur.
    """
    kopya = {
        "id": vaka["id"],
        "olay": vaka["olay"],
        "kisi": vaka.get("kisi"),
        "rol": vaka.get("rol"),
        "devam": vaka.get("devam", False),
        "zincir_id": vaka.get("zincir_id"),
        "secenekler": [
            {
                "metin": secenek["metin"],
                "tip": secenek["tip"],
                "etki": dict(secenek["etki"]),
                "sonuc": secenek["sonuc"],
                "karar_indeksi": indeks,
            }
            for indeks, secenek in enumerate(vaka["secenekler"])
        ],
    }

    random.shuffle(kopya["secenekler"])
    return kopya


def zinciri_bul(departman, zincir_id):
    for zincir in ZINCIRLER[departman]:
        if zincir["id"] == zincir_id:
            return zincir

    raise ValueError(f"Zincir bulunamadı: {zincir_id}")


def devam_vakasi_olustur(bekleyen):
    departman = st.session_state.user_department
    zincir = zinciri_bul(departman, bekleyen["zincir_id"])
    karar_indeksi = bekleyen["karar_indeksi"]

    return {
        "id": f"{zincir['id']}-devam",
        "olay": zincir["devam_metinleri"][karar_indeksi],
        "kisi": zincir["baslangic"]["kisi"],
        "rol": zincir["baslangic"]["rol"],
        "devam": True,
        "zincir_id": zincir["id"],
        "secenekler": zincir["devam_secenekleri"],
    }


def yeni_vaka_sec():
    departman = st.session_state.user_department
    tur = st.session_state.tur
    kalan_tur = TOPLAM_VAKA - tur + 1

    # Karara özel bir devam açılmışsa, onu 1-2 bağımsız
    # vakadan sonra göster. Son tura kalırsa kaçırma.
    bekleyenler = st.session_state.bekleyen_devamlar

    if bekleyenler:
        ilk_bekleyen = bekleyenler[0]

        if (
            tur >= ilk_bekleyen["hazir_tur"]
            or kalan_tur <= len(bekleyenler)
        ):
            bekleyen = bekleyenler.pop(0)
            secilen = devam_vakasi_olustur(bekleyen)
            st.session_state.son_vaka_devam_miydi = True

            if secilen["id"] in st.session_state.kullanilan_vakalar:
                raise ValueError(
                    "Aynı devam vakası ikinci kez seçilmeye çalışıldı."
                )

            st.session_state.kullanilan_vakalar.append(secilen["id"])
            return vaka_kopyala(secilen)

    # İlk turlarda iki zincirin de açılabilmesine olanak ver.
    # Zincir başlangıcını son iki turda seçmeyiz; böylece
    # kararın devamı için oyunda yer kalır.
    acilmamis_zincirler = [
        zincir
        for zincir in ZINCIRLER[departman]
        if zincir["id"] not in st.session_state.baslayan_zincirler
    ]

    zincir_secelim = (
        bool(acilmamis_zincirler)
        and tur <= TOPLAM_VAKA - 2
        and not st.session_state.son_vaka_devam_miydi
        and (
            (tur == 2 and random.random() < 0.70)
            or (tur == 4 and random.random() < 0.65)
            or (tur == 6 and random.random() < 0.45)
            or (tur == 1 and random.random() < 0.25)
        )
    )

    if zincir_secelim:
        zincir = random.choice(acilmamis_zincirler)
        secilen = dict(zincir["baslangic"])
        secilen["zincir_id"] = zincir["id"]

        st.session_state.baslayan_zincirler.append(zincir["id"])
        st.session_state.son_vaka_devam_miydi = False
        st.session_state.kullanilan_vakalar.append(secilen["id"])

        return vaka_kopyala(secilen)

    # Bağımsız vaka: önceki kararın adı veya sonucu eklenmez.
    adaylar = [
        vaka
        for vaka in VAKALAR[departman]
        if vaka["id"] not in st.session_state.kullanilan_vakalar
    ]

    if not adaylar:
        raise ValueError(
            "Bu oyun için kullanılmamış bağımsız vaka kalmadı."
        )

    secilen = random.choice(adaylar)
    st.session_state.son_vaka_devam_miydi = False
    st.session_state.kullanilan_vakalar.append(secilen["id"])

    return vaka_kopyala(secilen)


def karar_uygula(vaka, secenek):
    """
    Karar verildiği anda:
    - istatistik güncellenir;
    - somut sonuç karar ağacına yazılır;
    - zincir başlangıcıysa karara özel devam sıraya alınır.
    """
    for metrik, etki in secenek["etki"].items():
        st.session_state.stats[metrik] = max(
            0,
            min(100, st.session_state.stats[metrik] + etki),
        )

    st.session_state.secim_gecmisi.append(secenek["tip"])

    karakter_kaydet(
        vaka.get("kisi"),
        vaka.get("rol"),
        secenek["etki"],
        secenek["sonuc"],
    )

    st.session_state.karar_gecmisi.append(
        {
            "tur": st.session_state.tur,
            "metin": secenek["metin"],
            "tip": secenek["tip"],
            "etki": dict(secenek["etki"]),
            "sonuc": secenek["sonuc"],
            "karakter": vaka.get("kisi"),
            "devam": vaka.get("devam", False),
        }
    )

    if vaka.get("zincir_id") and not vaka.get("devam"):
        # Devam vakası, verilen dört karardan hangisinin
        # seçildiğine göre farklı metinle açılır.
        gecikme = random.choice([2, 3])

        st.session_state.bekleyen_devamlar.append(
            {
                "zincir_id": vaka["zincir_id"],
                "karar_indeksi": secenek["karar_indeksi"],
                "hazir_tur": min(
                    TOPLAM_VAKA,
                    st.session_state.tur + gecikme,
                ),
            }
        )

    st.session_state.tur += 1
    st.session_state.current_scenario = None
    st.rerun()


# ==========================================================
# GÖRSEL VE RAPOR YARDIMCILARI
# ==========================================================

def temiz(metin):
    return html.escape(str(metin))


def renk_belirle(deger):
    if deger >= 70:
        return "#16a34a"

    if deger >= 40:
        return "#f59e0b"

    return "#dc2626"


def stat_karti_ciz(label, deger, ikon):
    renk = renk_belirle(deger)

    st.markdown(
        f'<div class="stat-card" style="border-left-color:{renk};">'
        f'<div class="stat-label">{ikon} {temiz(label)}</div>'
        f'<div class="stat-value">%{deger}</div>'
        '<div class="progress-outer">'
        f'<div class="progress-inner" style="width:{deger}%;'
        f'background:{renk};"></div>'
        '</div></div>',
        unsafe_allow_html=True,
    )


def karar_karti_ciz(kayit):
    renk = TIP_RENK.get(kayit["tip"], "#9ca3af")

    kisa_metin = kayit["metin"][:75]

    if len(kayit["metin"]) > 75:
        kisa_metin += "..."

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
            f'<span>{temiz(metrik)}</span>'
            f'<span class="{stil}">{gosterim}</span>'
            '</div>'
        )

    kisi_html = ""

    if kayit.get("karakter"):
        kisi_html = (
            '<div style="font-size:0.76em;color:#047857;'
            'margin-bottom:4px;">'
            f'👤 {temiz(kayit["karakter"])}'
            '</div>'
        )

    devam_html = ""

    if kayit.get("devam"):
        devam_html = (
            '<div style="color:#7e22ce;font-size:0.78em;'
            'font-weight:700;margin-bottom:4px;">'
            '↳ Önceki kararın devamı'
            '</div>'
        )

    st.markdown(
        f'<div class="history-card" style="border-left-color:{renk};">'
        f'<div class="history-tur">Vaka {kayit["tur"]}</div>'
        f'{devam_html}'
        f'<div class="history-tip" style="background:{renk};">'
        f'{temiz(kayit["tip"])}</div>'
        f'{kisi_html}'
        f'<div class="history-metin">"{temiz(kisa_metin)}"</div>'
        '<div class="history-sonuc">'
        f'<b>Sonuç:</b> {temiz(kayit["sonuc"])}'
        '</div>'
        f'{stat_satirlari}'
        '</div>',
        unsafe_allow_html=True,
    )


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
            "Farklı paydaşları dinleyerek karar vermeye ağırlık verdiniz. "
            "Bu yaklaşım güven sağlayabilir; zaman baskısı yüksek "
            "durumlarda karar hızını da korumak gerekir."
        ),
        "Otoriter": (
            "Belirsizlikte net sınırlar ve hızlı kararlar koydunuz. "
            "Kriz anında değerli olabilir; ekibin bilgisini ve "
            "katılımını dışlamamaya dikkat edin."
        ),
        "Koçvari": (
            "Çalışanlara sorumluluk ve gelişim alanı açtınız. "
            "Kalıcı yetkinlik kazandırabilir; acil durumlarda "
            "son kararın sahibini de net tutmak önemlidir."
        ),
        "Kaçınmacı": (
            "Bazı zor kararları ertelemeyi tercih ettiniz. "
            "Bu bazen aceleci kararı önleyebilir; ancak gerekçesiz "
            "belirsizlik güven ve sonuçlara zarar verir."
        ),
        "Belirsiz": "Henüz yeterli karar verilmedi.",
    }

    metrik_yorumlari = {}

    for metrik, deger in stats.items():
        if deger >= 75:
            seviye = "Güçlü"
        elif deger >= 50:
            seviye = "Dengede"
        else:
            seviye = "Geliştirilebilir"

        aciklamalar = {
            "Moral": {
                "Güçlü": "Ekip motivasyonunu büyük ölçüde korudunuz.",
                "Dengede": "Ekip motivasyonu korunuyor; yoğun kararların etkisi izlenmeli.",
                "Geliştirilebilir": "İş yükü, adalet algısı ve çalışan desteği daha fazla dikkat istiyor.",
            },
            "Verimlilik": {
                "Güçlü": "İş akışını ve operasyonel sonuçları güçlü yönettiniz.",
                "Dengede": "Operasyon sürüyor; gecikme ve darboğazlar azaltılabilir.",
                "Geliştirilebilir": "Kısa ve uzun vadeli operasyon etkilerini daha açık tartabilirsiniz.",
            },
            "Güven": {
                "Güçlü": "Şeffaflık ve tutarlılık algısını güçlü tuttunuz.",
                "Dengede": "Güven korunuyor; karar gerekçelerini paylaşmak yararlı olabilir.",
                "Geliştirilebilir": "Tutarlı süreç ve açık iletişim güveni güçlendirebilir.",
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


def secenekleri_ciz(vaka):
    # Her zaman 4 seçenek: 2 satır x 2 sütun.
    for baslangic in (0, 2):
        sutunlar = st.columns(2, gap="medium")

        for sutun_no, secenek in enumerate(
            vaka["secenekler"][baslangic:baslangic + 2]
        ):
            indeks = baslangic + sutun_no

            with sutunlar[sutun_no]:
                if st.button(
                    secenek["metin"],
                    key=f"v_{st.session_state.tur}_{indeks}",
                    use_container_width=True,
                ):
                    karar_uygula(vaka, secenek)


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
            f"📚 Bağımsız vaka: **{len(VAKALAR[departman])}**"
        )
        st.write(
            f"🔗 Karara bağlı zincir: "
            f"**{len(ZINCIRLER[departman])}**"
        )
        st.write(
            f"✅ Tamamlanan vaka: "
            f"**{len(st.session_state.karar_gecmisi)} / {TOPLAM_VAKA}**"
        )

    if st.session_state.karakterler:
        st.write("---")
        st.write("**👥 Hikâyedeki Kişiler**")

        for isim, bilgi in st.session_state.karakterler.items():
            son = bilgi["son_etkilesim"]

            if len(son) > 95:
                son = son[:92] + "..."

            st.markdown(
                '<div class="karakter-kart">'
                f'<b>{temiz(isim)}</b> — {temiz(bilgi["rol"])}'
                '<br>'
                f'İlişki göstergesi: %{bilgi["iliski"]}'
                + (
                    f'<br><span style="color:#6b7280;">'
                    f'Son etkileşim: {temiz(son)}</span>'
                    if son
                    else ""
                )
                + '</div>',
                unsafe_allow_html=True,
            )

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
            <p>Kararlarınızın operasyonel ve insani sonuçlarını deneyin.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sol, sag = st.columns([1.2, 1])

    with sol:
        st.subheader("Nasıl Oynanır? 🎯")
        st.markdown(
            """
            - Departmanınızı seçin; vakalar departmanınıza özel gelsin.
            - Her oyunda **10 vaka** çözün.
            - **Her vakada 4 karar seçeneği** bulunur.
            - Kararlarınız **Moral, Verimlilik ve Güven** değerlerini etkiler.
            - Bazı kararların **gerçek devam vakaları** vardır.
              Böyle bir devam, seçtiğiniz karara göre farklı gelişir.
            - Bağımsız vakalar zorla birbirine bağlanmaz.
            - Kişiler yalnızca vakada gerçekten rol aldıklarında görünür.
            - Sağdaki **Karar Yolculuğu**, kararınızın somut sonucunu gösterir.

            **Bu sürüm hazır senaryolarla çalışır.**
            Vertex AI, servis hesabı veya faturalandırma gerekmez.

            ⚠️ *Seçenekler tek bir ideal cevabı buldurmak için değil,
            liderlik tercihlerini ve bedellerini düşündürmek için tasarlanmıştır.*
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
                f"{ikon} {ad}"
                for ad, ikon in DEPARTMANLAR.items()
            ]

            secilen = st.selectbox(
                "Departman *",
                departman_secenekleri,
            )

            baslat = st.form_submit_button(
                "🚀 Simülasyonu Başlat"
            )

            if baslat:
                if not ad_soyad.strip():
                    st.warning("Lütfen adınızı ve soyadınızı girin.")
                elif secilen == "-- Seçiniz --":
                    st.warning("Lütfen departman seçin.")
                else:
                    departman = secilen.split(" ", 1)[1]

                    st.session_state.user_name = ad_soyad.strip()
                    st.session_state.user_department = departman
                    st.session_state.started = True

                    st.rerun()

    st.stop()


# ==========================================================
# OYUN EKRANI
# ==========================================================

departman = st.session_state.user_department
departman_ikonu = DEPARTMANLAR[departman]

ust_bilgi = (
    f"👤 {temiz(st.session_state.user_name)}"
    f"  •  "
    f"{departman_ikonu} {temiz(departman)}"
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
    moral_sutun, verim_sutun, guven_sutun = st.columns(3)

    with moral_sutun:
        stat_karti_ciz(
            "Moral",
            st.session_state.stats["Moral"],
            "😊",
        )

    with verim_sutun:
        stat_karti_ciz(
            "Verimlilik",
            st.session_state.stats["Verimlilik"],
            "📈",
        )

    with guven_sutun:
        stat_karti_ciz(
            "Güven",
            st.session_state.stats["Güven"],
            "🤝",
        )

    st.write("")

    if st.session_state.tur <= TOPLAM_VAKA:
        if st.session_state.current_scenario is None:
            st.session_state.current_scenario = yeni_vaka_sec()

        vaka = st.session_state.current_scenario

        # Sadece hikâyede adı geçen kişi kaydedilir.
        karakter_kaydet(
            vaka.get("kisi"),
            vaka.get("rol"),
        )

        rozetler = (
            f'<div class="vaka-badge">'
            f'VAKA {st.session_state.tur} / {TOPLAM_VAKA}'
            '</div> '
            f'<div class="dept-badge">'
            f'{departman_ikonu} {temiz(departman)}'
            '</div>'
        )

        if vaka.get("devam"):
            rozetler += (
                ' <div class="devam-badge">'
                '🔗 Kararınızın devamı'
                '</div>'
            )

        if vaka.get("kisi"):
            rozetler += (
                ' <div class="karakter-badge">'
                f'👤 {temiz(vaka["kisi"])}'
                ' — '
                f'{temiz(vaka["rol"])}'
                '</div>'
            )

        st.markdown(
            rozetler,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="olay-box">'
            f'{temiz(vaka["olay"])}'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown("##### Nasıl bir karar alırsınız?")
        secenekleri_ciz(vaka)

    else:
        st.success(
            f"🏁 Tebrikler {st.session_state.user_name}, "
            f"{TOPLAM_VAKA} vakalık simülasyonu tamamladınız!"
        )

        (
            ortalama,
            baskin_tip,
            tip_aciklamasi,
            metrik_yorumlari,
            tip_sayaci,
        ) = final_rapor_uret(
            st.session_state.stats,
            st.session_state.secim_gecmisi,
        )

        st.markdown(
            '<div class="rapor-kart" style="text-align:center;">'
            '<div class="stat-label">'
            'FİNAL LİDERLİK ENDEKSİ'
            '</div>'
            '<div style="font-size:3em;font-weight:800;'
            f'color:{renk_belirle(int(ortalama))};">'
            f'%{int(ortalama)}'
            '</div>'
            '<div style="color:#6b7280;">'
            'Moral, Verimlilik ve Güven ortalaması.'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.write("### 📊 Metrik Bazlı Analiz")

        for yorum in metrik_yorumlari.values():
            st.markdown(
                '<div class="rapor-kart">'
                f'{temiz(yorum)}'
                '</div>',
                unsafe_allow_html=True,
            )

        st.write("### 🧭 Baskın Liderlik Tarzınız")

        st.markdown(
            '<div class="rapor-kart">'
            f'<b>{temiz(baskin_tip)}</b> '
            f'({tip_sayaci.get(baskin_tip, 0)}/{TOPLAM_VAKA} karar)'
            '<br><br>'
            f'{temiz(tip_aciklamasi)}'
            '</div>',
            unsafe_allow_html=True,
        )

        st.write("### 📈 Karar Dağılımınız")

        for tip in TIP_RENK:
            sayi = tip_sayaci.get(tip, 0)
            st.write(f"**{tip}** — {sayi} kez")
            st.progress(sayi / TOPLAM_VAKA)

        st.write("### 🔗 Devam Vakaları")

        devam_sayisi = sum(
            1
            for karar in st.session_state.karar_gecmisi
            if karar["devam"]
        )

        st.write(
            f"Bu oyunda kararlarınızdan doğan **{devam_sayisi} "
            f"devam vakası** çözdünüz."
        )

        st.write("---")

        if ortalama > 75:
            genel = (
                "💎 Farklı karar bedellerini güçlü biçimde "
                "dengelediniz."
            )
        elif ortalama > 50:
            genel = (
                "📈 Güçlü tercihleriniz var; karar hızını, "
                "insan etkisini ve sürdürülebilirliği birlikte "
                "tartmaya devam edin."
            )
        else:
            genel = (
                "⚠️ Kararlarınızın ikinci aşamadaki etkilerine "
                "daha fazla odaklanabilirsiniz."
            )

        st.markdown(
            '<div class="rapor-kart">'
            f'<b>Genel Değerlendirme:</b> {temiz(genel)}'
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
            'İlk kararınız ve sonucu burada görünecek.'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        for kayit in st.session_state.karar_gecmisi:
            karar_karti_ciz(kayit)
