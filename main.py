import os
from datetime import datetime, timedelta
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# 1. ADIM: Tarih aralığını hesapla
bugun = datetime.now()
gecen_hafta = bugun - timedelta(days=7)
tarih_metni = f"{gecen_hafta.strftime('%d-%m-%Y')}_ile_{bugun.strftime('%d-%m-%Y')}"

# 2. ADIM: "Raporlar" adında bir klasör oluştur
klasor_adi = "Raporlar"
os.makedirs(klasor_adi, exist_ok=True)
dosya_yolu = os.path.join(klasor_adi, f"Yatirim_Strateji_Raporu_{tarih_metni}.md")

# AI Motoru ve Araçlar
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.environ["GEMINI_API_KEY"]
)
arama_araci = SerperDevTool(serper_api_key=os.environ["SERPER_API_KEY"])

# Ajanlar
arastirmaci = Agent(
    role='Kıdemli Makroekonomi ve Portföy Araştırmacısı',
    goal='Tüm yatırım araçlarındaki (yerli/yabancı hisse, fon, maden, emtia) kritik gelişmeleri ve fırsatları tespit etmek.',
    backstory='Sen küresel piyasalardaki kelebek etkilerini gören, verilerin içindeki fırsatları avlayan tecrübeli bir fon yöneticisisin.',
    tools=[arama_araci],
    llm=gemini_llm
)

raportor = Agent(
    role='Baş Stratejist',
    goal='Araştırmacının verilerini vizyoner, anlaşılır ve aksiyon alınabilir bir yatırım tavsiye bültenine dönüştürmek.',
    backstory='Sen karmaşık piyasa verilerini süzerek patronuna "Şu an ne yapmalıyız?" sorusunun cevabını veren elit bir stratejistsin.',
    llm=gemini_llm
)

# Kapsamlı Görevler
gorev_1 = Task(
    description='Borsa İstanbul (BİST) hisseleri, Midas üzerinden işlem gören yabancı teknoloji hisseleri, altın/gümüş gibi kıymetli madenler ve genel emtialar hakkında son 1 haftanın kritik verilerini topla. Özellikle KTJ, KCV, KUT, KNJ, KDE, KPC gibi katılım esaslı yatırım fonlarındaki hareketlilikleri, temettü gelişmelerini ve makroekonomik olayların bu yatırım araçları üzerindeki etkilerini derinlemesine araştır.',
    expected_output='Tüm yatırım araçlarının (hisse, fon, emtia, maden) güncel durumunu gösteren detaylı ham veri listesi.',
    agent=arastirmaci
)

gorev_2 = Task(
    description='Araştırmacının verilerini alarak şu 4 başlıkta kapsamlı bir strateji raporu yaz: 1) Mevcut Durum (Piyasalarda, madenlerde ve fonlarda ne oldu?), 2) Gelişmelerin Etkileri (Yaşanan olaylar piyasaları nasıl etkileyecek?), 3) Gelecek Öngörüleri (Kısa ve orta vadede beklentiler neler?), 4) Fırsatlar ve Aksiyonlar (Neler yapılabilir, rotayı nereye çevirmeli?).',
    expected_output='Profesyonel, net alt başlıklara ayrılmış, vizyoner yatırım stratejisi raporu.',
    agent=raportor
)

# Ekibi Çalıştır
ekip = Crew(agents=[arastirmaci, raportor], tasks=[gorev_1, gorev_2])
sonuc = ekip.kickoff()

# 3. ADIM: Sonucu kaydet
with open(dosya_yolu, "w", encoding="utf-8") as dosya:
    dosya.write(sonuc.raw)
