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
dosya_yolu = os.path.join(klasor_adi, f"Haftalik_Strateji_Raporu_{tarih_metni}.md")

# AI Motoru ve Araçlar
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.environ["GEMINI_API_KEY"]
)
arama_araci = SerperDevTool(serper_api_key=os.environ["SERPER_API_KEY"])

# Ajanlar
arastirmaci = Agent(
    role='Kıdemli Makroekonomi ve Portföy Araştırmacısı',
    goal='Tüm yatırım araçlarındaki kritik gelişmeleri ve fırsatları geniş bir yelpazede tespit etmek.',
    backstory='Sen piyasalardaki kelebek etkilerini gören, verilerin içindeki fırsatları avlayan tecrübeli bir fon yöneticisisin.',
    tools=[arama_araci],
    llm=gemini_llm
)

raportor = Agent(
    role='Baş Stratejist',
    goal='Araştırmacının verilerini, belirlenen katı şablona sadık kalarak vizyoner bir yatırım bültenine dönüştürmek.',
    backstory='Sen karmaşık piyasa verilerini süzerek yatırımcılara net yön veren, tarafsız ve veri odaklı elit bir stratejistsin.',
    llm=gemini_llm
)

# Kapsamlı Görevler
gorev_1 = Task(
    description='''Aşağıdaki 5 ana yatırım enstrümanı için son 1 haftanın verilerini, haberlerini ve makroekonomik gelişmeleri (enflasyon, faiz kararları vb.) araştır:
    1. Küresel ve Yerel Hisse Senedi Piyasaları (BIST, S&P 500, Nasdaq ve Midas üzerinden takip edilen yabancı teknoloji hisseleri, KTJ, KCV, KUT, KNJ, KDE, KPC gibi katılım fonları)
    2. Döviz Piyasaları (Dolar/TL, Euro/TL, EUR/USD paritesi)
    3. Emtialar (Ons/Gram Altın, Gümüş, Brent Petrol)
    4. Kripto Paralar (Bitcoin, Ethereum ve öne çıkan altcoin trendleri)
    5. Tahvil, Bono ve Faiz Piyasaları''',
    expected_output='Belirtilen 5 yatırım aracı için güncel durumu ve haberleri içeren kapsamlı ham veri listesi.',
    agent=arastirmaci
)

gorev_2 = Task(
    description='''Araştırmacının verilerini kullanarak son derece profesyonel, tarafsız ve veri odaklı bir yatırım raporu hazırla. Rapor kalın yazılar, alt başlıklar ve maddeler içermelidir.
    
    Raporun GÖVDESİNDE şu 5 başlık MUTLAKA olmalıdır (Her biri için: Geçen Haftanın Özeti, Gelecek Hafta İçin Öngörüler, Strateji (Ne Yapılmalı?), Riskler alt başlıklarını kullan):
    - Küresel ve Yerel Hisse Senedi Piyasaları
    - Döviz Piyasaları
    - Emtialar
    - Kripto Paralar
    - Tahvil, Bono ve Faiz Piyasaları
    
    Raporun SONUNDA şu iki bölüm MUTLAKA olmalıdır:
    - Haftanın Özeti ve Ana Tema (Tüm piyasaların genel bir özeti)
    - Örnek Portföy Dağılımı (Düşük, Orta ve Yüksek risk iştahına sahip 3 farklı yatırımcı profili için haftalık yüzdelik (%) varlık dağılımı tavsiyesi)''',
    expected_output='Belirtilen şablona harfi harfine uyan, Markdown formatında profesyonel haftalık strateji raporu.',
    agent=raportor
)

# Ekibi Çalıştır
ekip = Crew(agents=[arastirmaci, raportor], tasks=[gorev_1, gorev_2])
sonuc = ekip.kickoff()

# 3. ADIM: Sonucu kaydet
with open(dosya_yolu, "w", encoding="utf-8") as dosya:
    dosya.write(sonuc.raw)
