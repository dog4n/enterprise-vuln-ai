# 🛡️ Enterprise Vulnerability Context Engine (EVCE)

*(🇹🇷 Türkçe versiyonu aşağıdadır / Turkish version is below)*

Security analysts spend more time explaining findings than finding them. EVCE takes raw
**Nuclei** output and uses **Google Gemini** to add business context to every finding:
**real business risk**, **attacker perspective** and **immediate remediation**. The result is a
single HTML report you can hand to a manager or CISO.

## ✨ Features
* **Reads Nuclei output directly:** JSONL (`nuclei -jsonl -o out.json`) or a JSON array.
* **De-duplicated and sorted:** same host + finding appears once, critical first.
* **AI risk context:** three short, executive-level sections per finding.
* **Self-contained HTML report:** severity summary + one card per finding, no external assets.
* **Turkish or English** reports (`--lang tr|en`).
* **Dry run:** preview the report without an API key (`--dry-run`).

## 🚀 Installation
```bash
git clone https://github.com/dog4n/enterprise-vuln-ai.git
cd enterprise-vuln-ai
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## ⚙️ Usage

### 1. Set the API key
Get a free key from Google AI Studio:
```bash
export GEMINI_API_KEY="Your_API_Key_Here"
```

### 2. Run a scan (or use the sample file)
```bash
nuclei -u https://target.example -jsonl -o nuclei_output.json
```
A sample `nuclei_output.json` is included so you can try the tool right away.

### 3. Build the report
```bash
python3 ai_risk_engine.py                                # nuclei_output.json -> risk_report.html (Turkish)
python3 ai_risk_engine.py scan.json -o report.html --lang en
python3 ai_risk_engine.py --dry-run                      # no API call, layout preview only
```

| Option | Default | Description |
|---|---|---|
| `input` | `nuclei_output.json` | Nuclei JSONL / JSON file |
| `-o, --output` | `risk_report.html` | Report path |
| `--lang` | `tr` | Report language: `tr` or `en` |
| `--model` | `gemini-flash-latest` | Gemini model (or set `GEMINI_MODEL`) |
| `--limit` | `0` (all) | Analyse only the first N findings |
| `--dry-run` | off | Skip the AI call |

### 4. View the report
Open `risk_report.html` in a browser. On a remote server:
```bash
python3 -m http.server 8080
```

> ⚠️ Finding details (host, URL, description) are sent to the Gemini API. Do not use it with
> data you are not allowed to share with a third-party service.

## 📜 License
MIT. See `LICENSE`.

---

# 🛡️ Enterprise Vulnerability Context Engine (EVCE) - Türkçe

Bir güvenlik analisti zamanının çoğunu zafiyet bulmaya değil, **bulunan zafiyetin bağlamını
anlatmaya** harcar. EVCE, **Nuclei** çıktısını okur ve **Google Gemini** ile her bulguya
**Gerçek İş Riski**, **Saldırgan Perspektifi** ve **Acil Çözüm Önerisi** ekler. Sonuç,
yöneticiye ya da CISO'ya doğrudan iletilebilecek tek bir HTML rapordur.

## ✨ Özellikler
* **Nuclei çıktısını doğrudan okur:** JSONL (`nuclei -jsonl -o out.json`) veya JSON dizi.
* **Tekrarlar ayıklanır, sıralanır:** aynı hedef + bulgu bir kez, kritik olanlar en üstte.
* **Yapay zeka ile risk bağlamı:** her bulgu için yönetici seviyesinde üç kısa başlık.
* **Tek dosya HTML rapor:** önem derecesi özeti + bulgu başına bir kart.
* **Türkçe veya İngilizce** rapor (`--lang tr|en`).
* **Deneme modu:** API anahtarı olmadan rapor görünümünü dene (`--dry-run`).

## 🚀 Kurulum
```bash
git clone https://github.com/dog4n/enterprise-vuln-ai.git
cd enterprise-vuln-ai
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## ⚙️ Kullanım
```bash
export GEMINI_API_KEY="Sizin_API_Anahtariniz"
nuclei -u https://hedef.example -jsonl -o nuclei_output.json   # veya örnek dosyayı kullanın
python3 ai_risk_engine.py                                       # -> risk_report.html
python3 ai_risk_engine.py --dry-run                             # API çağrısı yapmadan önizleme
```
Tüm seçenekler için yukarıdaki tabloya bakın veya `python3 ai_risk_engine.py -h` çalıştırın.

> ⚠️ Bulgu detayları (hedef, URL, açıklama) Gemini API'ye gönderilir. Üçüncü taraf bir
> servisle paylaşma yetkiniz olmayan verilerle kullanmayın.

## 📜 Lisans
MIT. Detaylar için `LICENSE` dosyasına bakın.
