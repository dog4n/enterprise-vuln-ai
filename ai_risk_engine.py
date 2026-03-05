import json
import google.generativeai as genai
import os

# 1. API Ayarları (Bunu Mac terminalinde 'export GEMINI_API_KEY="senin_anahtarin"' şeklinde tanımlayabilirsin)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Örnek bir Tarayıcı (Nuclei) Çıktısı Simülasyonu
# Gerçek senaryoda bunu 'nuclei_output.json' dosyasından okuyacağız.
tarama_sonuclari = [
    {
        "hedef": "192.168.1.55",
        "zafiyet_adi": "CVE-2021-44228 (Log4Shell)",
        "kategori": "Remote Code Execution",
        "arac_skoru": "Kritik"
    }
]

# 3. Zenginleştirme ve Raporlama Döngüsü
def yapay_zekadan_yorum_al(hedef, zafiyet, kategori):
    # İŞİN SIRRI BURADA: Sisteme nasıl bir rol biçtiğin.
    prompt = f"""
    Sen kurumsal bir firmada görev yapan Kıdemli Siber Güvenlik Analistisin. 
    Tarama aracımız {hedef} IP adresli sunucuda '{zafiyet}' ({kategori}) zafiyeti tespit etti.
    
    Lütfen bu bulgu için aşağıdaki formatta kısa, net ve yönetici seviyesine uygun bir rapor özeti hazırla:
    1. Gerçek İş Riski (Bu açık sömürülürse kuruma maliyeti/zararı ne olur?)
    2. Saldırgan Perspektifi (Bir Red Teamer bunu nasıl kullanır?)
    3. Acil Çözüm Önerisi (Sistem yöneticisinin yapması gereken ilk 2 adım)
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Yanıt veremedi: {e}"

# 4. Sistemi Çalıştır
print("--- Enterprise Vulnerability AI Motoru Başlıyor ---\n")

for bulgu in tarama_sonuclari:
    print(f"Hedef: {bulgu['hedef']} | Zafiyet: {bulgu['zafiyet_adi']} inceleniyor...")
    
    ai_yorumu = yapay_zekadan_yorum_al(
        bulgu["hedef"], 
        bulgu["zafiyet_adi"], 
        bulgu["kategori"]
    )
    
    print("\n--- AI Rapor Çıktısı ---")
    print(ai_yorumu)
    print("-" * 30)
