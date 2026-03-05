# 🛡️ Enterprise Vulnerability Context Engine (EVCE)

*(🇹🇷 Türkçe versiyonu aşağıdadır / Turkish version is below)*

What a cybersecurity analyst spends the most time on is not finding vulnerabilities, but **creating the business context for them.** This project is a "Micro-Automation" tool that automatically enriches raw vulnerability outputs (JSONL) from security scanners like Nuclei using Google Gemini AI. Instead of just listing vulnerabilities by their technical names, it generates elegant HTML reports ready to be presented to executives and CISOs by providing **Real Business Risk**, **Attacker Perspective**, and **Immediate Remediation Steps**.

## ✨ Features
* **Automated Enrichment:** Automatically parses scanner outputs (JSON/JSONL).
* **AI-Powered Risk Engine:** Analyzes the financial impact, reputation loss, and legal/compliance risks (GDPR, etc.) of the vulnerability.
* **Executive Summary (HTML):** Transforms raw logs from the terminal into readable, styled HTML cards categorized by severity levels.
* **Lightweight & Fast:** Does not require any heavy databases or complex setups.

## 🚀 Installation
You can get the tool up and running in seconds on your local environment or a cloud server (Ubuntu/Debian, etc.).

### 1. Clone the Repository
```bash
git clone [https://github.com/adstech/enterprise-vuln-ai.git](https://github.com/adstech/enterprise-vuln-ai.git)
cd enterprise-vuln-ai
```

### 2. Create a Virtual Environment (Recommended)
To avoid polluting your system packages, use an isolated Python environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install google-genai
```

## ⚙️ Configuration and Usage

### 1. Set the API Key
Export your Google Gemini API key (which you can get for free from Google AI Studio) to your environment variables:
```bash
export GEMINI_API_KEY="Your_API_Key_Here"
```

### 2. Prepare Scan Data
Place a JSONL file (one JSON object per line) named `nuclei_output.json` in the project directory. An example line should look like this:
```json
{"host": "login.company.com", "info": {"name": "Reflected Cross-Site Scripting (XSS)", "severity": "medium"}}
```

### 3. Run the Engine
```bash
python3 ai_risk_engine.py
```

### 4. View the Report
Once the process is complete, a `Kurumsal_Risk_Raporu.html` file will be generated in the directory. If you are working on a remote cloud server, you can start a simple web server to view it:
```bash
python3 -m http.server 8080
```
Then, navigate to `http://localhost:8080` (or your server's IP address) in your browser to review the executive report.

## 🤝 Contributing
This project is a community effort aimed at reducing the cognitive load and decision-making time of security analysts. Pull Requests (PRs) and new ideas (Issues) are always welcome!

## 📜 License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

# 🛡️ Enterprise Vulnerability Context Engine (EVCE) - Türkçe

Bir siber güvenlik analistinin en çok zaman harcadığı şey zafiyet bulmak değil, **bulunan zafiyetin bağlamını (context) oluşturmaktır.** Bu proje, Nuclei gibi güvenlik tarayıcılarından alınan ham (JSONL) zafiyet çıktılarını Google Gemini AI kullanarak otomatik olarak zenginleştiren bir "Mikro Otomasyon" aracıdır. Zafiyetleri sadece teknik isimleriyle listelemek yerine; **Gerçek İş Riski**, **Saldırgan Perspektifi** ve **Acil Çözüm Önerisi** sunarak yöneticilere ve CISO'lara sunulmaya hazır şık HTML raporlar üretir.

## ✨ Özellikler

* **Otomatik Zenginleştirme:** Tarayıcı çıktılarını (JSON/JSONL) otomatik okur.
* **Yapay Zeka Destekli Risk Motoru:** Zafiyetin kuruma maliyetini, itibar kaybını ve yasal risklerini (KVKK vb.) analiz eder.
* **Yönetici Özeti (HTML):** Siyah terminal ekranındaki logları, kurumsal renklere ve önem derecelerine göre kategorize edilmiş okunabilir HTML kartlarına dönüştürür.
* **Hafif ve Hızlı:** Herhangi bir ağır veritabanı veya karmaşık kurulum gerektirmez.

## 🚀 Kurulum

Aracı kendi lokal ortamınızda veya bir bulut sunucusunda (Ubuntu/Debian vb.) saniyeler içinde ayağa kaldırabilirsiniz.

### 1. Repoyu Klonlayın
```bash
git clone [https://github.com/adstech/enterprise-vuln-ai.git](https://github.com/adstech/enterprise-vuln-ai.git)
cd enterprise-vuln-ai
```

### 2. Sanal Ortam Oluşturun (Önerilen)
Sistem paketlerinizi kirletmemek için izole bir Python ortamı kullanın:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Gereksinimleri Yükleyin
```bash
pip install google-genai
```

## ⚙️ Yapılandırma ve Kullanım

### 1. API Anahtarını Tanımlama
Google AI Studio üzerinden ücretsiz alabileceğiniz API anahtarınızı sisteminize tanıtın:
```bash
export GEMINI_API_KEY="Sizin_API_Anahtariniz"
```

### 2. Tarama Verisini Hazırlama
Aracın bulunduğu dizine `nuclei_output.json` adında bir JSONL (her satırda bir JSON objesi) dosyası koyun. Örnek bir satır şu formatta olmalıdır:
```json
{"host": "login.sirketim.com", "info": {"name": "Reflected Cross-Site Scripting (XSS)", "severity": "medium"}}
```

### 3. Motoru Çalıştırma
```bash
python3 ai_risk_engine.py
```

### 4. Raporu Görüntüleme
İşlem tamamlandığında dizinde `Kurumsal_Risk_Raporu.html` dosyası oluşacaktır. Bulut sunucuda çalışıyorsanız raporu görüntülemek için basit bir web sunucusu başlatabilirsiniz:
```bash
python3 -m http.server 8080
```
Ardından tarayıcınızdan `http://localhost:8080` (veya sunucu IP'niz) adresine giderek raporu inceleyebilirsiniz.

## 🤝 Katkıda Bulunma
Bu proje, analistlerin karar verme süresini kısaltmayı amaçlayan bir topluluk eforudur. Pull Request'ler (PR) ve yeni fikirler (Issue) her zaman memnuniyetle karşılanır!

## 📜 Lisans
Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için repodaki `LICENSE` dosyasına göz atabilirsiniz.
