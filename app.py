import streamlit as st
import google.generativeai as genai
import json
import random
from collections import Counter

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
    .baslat-buton>button {
        height: 3.5em; background-color: #0054a6; color: white; font-size: 18px;
    }
    .baslat-buton>button:hover { background-color: #003d7a; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- API YAPILANDIRMASI ---
API_KEY = 'AQ.Ab8RN6LpvpinBuDLv3Qo6n0kLMOLt_fN6DWQX4rHkjAkYvKkCA'
genai.configure(api_key=API_KEY)

MODEL_ADI = 'gemini-1.5-flash'

generation_config = {
    "temperature": 1.4,
    "top_p": 0.95,
    "top_k": 40,
}

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

temalar = ["Performans Yönetimi", "Çalışan Bağlılığı", "Kriz Yönetimi", "Yenilikçilik",
           "Zor Kişiliklerle İletişim", "Etik İkilemler", "Mağaza Operasyonu", "Uzaktan Yönetim",
           "İşe Alım Kararları", "Terfi ve Adalet", "Müşteri Şikayeti Yönetimi", "Bütçe Kısıtlaması"]

karakterler = ["yeni işe başlayan bir kasiyer", "10 yıllık kıdemli bir reyon sorumlusu",
               "stajyer bir çalışan", "vardiya amiri", "depo sorumlusu", "kıdemli bir mağaza müdür yardımcısı"]

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

def kriz_uret():
    tema = random.choice(temalar)
    karakter = random.choice(karakterler)
    onceki_ozet = ", ".join(st.session_state.gecmis_konular[-3:]) if st.session_state.gecmis_konular else "yok"

    try:
        istek = f"""Sen üst düzey, tecrübeli ve YARATICI bir LCW (LC Waikiki) Liderlik Koçusun. 
        Konu teması: {tema}. 
        Senaryoda mutlaka şu karakter yer alsın: {karakter}. 
        
        Daha önce şu konular kullanıldı, bunları TEKRARLAMA: {onceki_ozet}.
        
        Gerçekçi, özgün, sürpriz detaylar içeren, sıradanlıktan uzak bir yönetim senaryosu yaz (2-3 cümle, somut detaylar içersin, isim kullanabilirsin).
        
        4 farklı liderlik tarzını temsil eden seçenekler sun ve her birine bir "tip" etiketi ver:
        1. "Demokratik" (Güven artırır, Verimlilik bazen yavaşlar)
        2. "Otoriter" (Verimlilik artırır, Moral bazen düşer)
        3. "Koçvari" (Gelişim odaklı, dengeli etki)
        4. "Kaçınmacı" (Risk almaz, genelde skorları düşürür)
        
        ÖNEMLİ: Hiçbir seçenek 'mükemmel' olmasın, her birinin bir bedeli olsun. Etkiler -15 ile +15 arasında olsun.
        
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
    st.title("💙 LC WAIKIKI LİDERLİK SİMÜLASYONU")
    st.write("---")

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("Hoş Geldiniz! 👋")
        st.markdown("""
        Bu simülasyonda, bir **LC Waikiki mağaza/ekip yöneticisi** rolüne bürüneceksiniz.

        🎯 **Nasıl Oynanır?**
        - Karşınıza toplam **10 farklı liderlik vakası** çıkacak.
        - Her vakada **4 farklı karar seçeneği** sunulacak.
        - Verdiğiniz her karar; **Moral, Verimlilik ve Güven** skorlarınızı etkileyecek.
        - Sonunda size özel bir **"Liderlik Karnesi"** hazırlanacak: baskın liderlik tarzınızı ve gelişim alanlarınızı göreceksiniz.

        ⚠️ Unutmayın: Hiçbir seçenek mükemmel değildir. Gerçek liderlik, doğru dengeleri kurmaktır.
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

    st.stop()  # Karşılama ekranı bitmeden aşağıdaki oyun koduna geçilmesin


# ==========================================================
# ==================  2. AŞAMA: OYUN EKRANI  ===============
# ==========================================================
st.title("💙 LC WAIKIKI LİDERLİK SİMÜLASYONU")

ust_bilgi = f"👤 **{st.session_state.user_name}**"
if st.session_state.user_role:
    ust_bilgi += f" — {st.session_state.user_role}"
st.caption(ust_bilgi)

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

    st.subheader(f"VAKA {st.session_state.tur} / 10")
    st.info(current['olay'])

    st.write("#### Liderlik Yaklaşımınız:")

    c1, c2 = st.columns(2)
    for i, s in enumerate(current['secenekler']):
        with (c1 if i % 2 == 0 else c2):
            if st.button(s['metin'], key=f"v_{st.session_state.tur}_{i}"):
                for k, v in s['etki'].items():
                    st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))

                st.session_state.secim_gecmisi.append(s.get('tip', 'Belirsiz'))

                st.session_state.tur += 1
                st.session_state.current_scenario = None
                st.rerun()

else:
    st.balloons()
    st.success(f"🏁 Tebrikler {st.session_state.user_name}, 10 Günlük Liderlik Maratonunu Tamamladınız!")

    ortalama, baskin_tip, tip_metni, metrik_yorumlari, tip_sayaci = final_rapor_uret(
        st.session_state.stats, st.session_state.secim_gecmisi
    )

    st.metric("Final Liderlik Endeksiniz", f"%{int(ortalama)}")
    st.caption("Bu skor, 3 metriğinizin (Moral + Verimlilik + Güven) basit ortalamasıdır.")

    st.write("### 📊 Metrik Bazlı Detaylı Analiz")
    for metrik, yorum in metrik_yorumlari.items():
        st.markdown(yorum)

    st.write("### 🧭 Baskın Liderlik Tarzınız")
    st.markdown(f"**{baskin_tip}** ({tip_sayaci.get(baskin_tip, 0)}/10 kararınızda bu yaklaşımı sergilediniz)")
    st.markdown(tip_metni)

    st.write("### 📈 Tüm Kararlarınızın Dağılımı")
    for tip, sayi in tip_sayaci.items():
        st.write(f"- {tip}: {sayi} kez")
        st.progress(sayi / 10)

    st.write("---")
    if ortalama > 75:
        st.write("💎 **Genel Değerlendirme:** Dengeleri harika koruyan, stratejik bir lidersiniz.")
    elif ortalama > 50:
        st.write("📈 **Genel Değerlendirme:** Sonuç odaklısınız ama insan faktörüne biraz daha ağırlık vermelisiniz.")
    else:
        st.write("⚠️ **Genel Değerlendirme:** Kararlarınızın uzun vadeli etkilerini daha dikkatli tartmalısınız. Özellikle en düşük skorlu metriğinize odaklanın.")

    if st.button("Simülasyonu Baştan Başlat"):
        st.session_state.clear()
        st.rerun()
