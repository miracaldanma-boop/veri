import os
from datetime import datetime, timedelta
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# 1. ADIM: Tarih aralığını hesapla (Son 7 gün)
bugun = datetime.now()
gecen_hafta = bugun - timedelta(days=7)
# Rapor isminde kullanılacak format: 19-06-2026_ile_26-06-2026
tarih_metni = f"{gecen_hafta.strftime('%d-%m-%Y')}_ile_{bugun.strftime('%d-%m-%Y')}"

# 2. ADIM: "Raporlar" adında bir klasör oluştur (yoksa yaratır)
klasor_adi = "Raporlar"
os.makedirs(klasor_adi, exist_ok=True)
dosya_yolu = os.path.join(klasor_adi, f"Yatirim_Raporu_{tarih_metni}.md")

# AI Motoru ve Araçlar
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.environ["GEMINI_API_KEY"]
)
arama_araci = SerperDevTool(serper_api_key=os.environ["SERPER_API_KEY"])

# Ajanlar
arastirmaci = Agent(
    role='Finansal Araştırmacı',
    goal='Borsa ve yatırım fonlarındaki güncel haberleri, ekonomik verileri ve fırsatları bulmak.',
    backstory='Sen Wall Street düzeyinde titiz bir analistsin.',
    tools=[arama_araci],
    llm=gemini_llm
)

raportor = Agent(
    role='Raportör',
    goal='Araştırmacının bulduğu karmaşık verileri sade, anlaşılır bir yatırım raporuna çevirmek.',
    backstory='Karmaşık finansal verileri patronun için en net hale getiren bir uzmansın.',
    llm=gemini_llm
)

# Görevler
gorev_1 = Task(description='Bugünün en önemli 3 küresel ekonomik gelişmesini araştır.', expected_output='Haber özetleri listesi', agent=arastirmaci)
gorev_2 = Task(description='Bu gelişmeleri değerlendir ve öngörü içeren kısa bir rapor yaz.', expected_output='Final Yatırım Raporu', agent=raportor)

# Ekibi Çalıştır
ekip = Crew(agents=[arastirmaci, raportor], tasks=[gorev_1, gorev_2])
sonuc = ekip.kickoff()

# 3. ADIM: Sonucu oluşturulan tarihli dosyaya ve klasöre kaydet
with open(dosya_yolu, "w", encoding="utf-8") as dosya:
    dosya.write(sonuc.raw)
