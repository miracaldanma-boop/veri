import os
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# CrewAI'ın yeni sistemine uygun Gemini kurulumu
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.environ["GEMINI_API_KEY"]
)

arama_araci = SerperDevTool(serper_api_key=os.environ["SERPER_API_KEY"])

# 1. Çalışan: Araştırmacı
arastirmaci = Agent(
    role='Finansal Araştırmacı',
    goal='Borsa ve yatırım fonlarındaki güncel haberleri, ekonomik verileri ve fırsatları bulmak.',
    backstory='Sen Wall Street düzeyinde titiz bir analistsin.',
    tools=[arama_araci],
    llm=gemini_llm
)

# 2. Çalışan: Raportör
raportor = Agent(
    role='Raportör',
    goal='Araştırmacının bulduğu karmaşık verileri sade, anlaşılır bir yatırım raporuna çevirmek.',
    backstory='Karmaşık finansal verileri patronun için en net hale getiren bir uzmansın.',
    llm=gemini_llm
)

# Yapılacak İşler
gorev_1 = Task(description='Bugünün en önemli 3 küresel ekonomik gelişmesini araştır.', expected_output='Haber özetleri listesi', agent=arastirmaci)
gorev_2 = Task(description='Bu gelişmeleri değerlendir ve öngörü içeren kısa bir rapor yaz.', expected_output='Final Yatırım Raporu', agent=raportor)

# Ekibi Topla ve İşe Başlat
ekip = Crew(agents=[arastirmaci, raportor], tasks=[gorev_1, gorev_2])
sonuc = ekip.kickoff()

# Sonucu Dosyaya Kaydet
with open("haftalik_rapor.md", "w", encoding="utf-8") as dosya:
    dosya.write(sonuc.raw)
