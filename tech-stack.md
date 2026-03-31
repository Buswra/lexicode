# LexiCode — Teknoloji Seçimi (Tech Stack)

> "Başlangıç seviyesindeyim. LexiCode için en basit teknoloji yığınını öner."
> Aşağıda her katman, neden seçildiği ve kurulum adımları açıklanmıştır.

---

## Kullanılan Teknolojiler

### 1. Python 3.14 + Flask — Backend
**Ne yapar:** Kelime kartları, kullanıcı ilerlemesi, AI Tutor ve TTS gibi tüm API endpoint'lerini çalıştırır.
**Neden seçildi:**
- Python öğrenmesi en kolay dillerden biri, AI kütüphaneleriyle doğal uyumlu.
- Flask, minimal bir micro-framework — sadece ihtiyacın kadar büyür, karmaşık ayar gerektirmez.
- Dosya: `features/app.py`

### 2. PySide6 + QtWebEngine — Desktop Shell
**Ne yapar:** Web arayüzünü bir Windows masaüstü penceresi içinde açar, tarayıcı yerine gerçek bir uygulama deneyimi sunar.
**Neden seçildi:**
- Electron'a göre daha hafif, Python ekosistemiyle doğal entegre.
- Tek kod tabanıyla hem web hem masaüstü çıktısı alınır.
- Dosya: `features/desktop_launcher.py`

### 3. HTML + CSS + JavaScript — Frontend
**Ne yapar:** Kullanıcının gördüğü arayüz: kartlar, butonlar, animasyonlar, quiz ekranı.
**Neden seçildi:**
- React/Vue gibi framework'lere gerek yok — tek sayfalık uygulama (SPA) olduğu için vanilla JS yeterli.
- Disleksi dostu CSS kuralları (büyük font, yüksek kontrast, geniş satır aralığı) doğrudan uygulanır.
- Dosya: `features/templates/index.html`

### 4. SQLite — Veritabanı
**Ne yapar:** Kullanıcı ilerlemesini, streak'leri, rozetleri ve ayarları yerel olarak saklar.
**Neden seçildi:**
- Sunucu gerektirmez, tek dosya (`.db`) olarak çalışır.
- Masaüstü dağıtımı için ideal — kullanıcı hiçbir veritabanı kurulumu yapmaz.
- Konum: `%LOCALAPPDATA%/LexiCode/progress.db`

### 5. Claude API — Yapay Zeka
**Ne yapar:** AI Tutor'un arkasındaki beyin. Cümle düzeltir, bağlam üretir, diyalog simülasyonu yapar.
**Neden seçildi:**
- Claude, doğal dil anlama ve eğitim bağlamında güçlü performans gösterir.
- Prompt engineering ile disleksi dostu, cesaretlendirici ton ayarlanır.
- Güvenli fallback: API anahtarı olmasa bile uygulama çalışmaya devam eder.

### 6. edge-tts — Sesli Okuma (Text-to-Speech)
**Ne yapar:** Kelimeleri İngilizce ve Türkçe olarak doğal Neural sesle okur.
**Neden seçildi:**
- Ücretsiz, API anahtarı gerektirmez.
- Yüksek kaliteli Microsoft Neural ses motoru kullanır.
- Yedek: Tarayıcı `speechSynthesis` fallback'i.
- Dosya: `features/services/tts_service.py`

### 7. PyInstaller + Inno Setup — Paketleme
**Ne yapar:** Python projesini `.exe` dosyasına dönüştürür, tek tık Windows installer'ı üretir.
**Neden seçildi:**
- Son kullanıcı Python yüklemez, pip çalıştırmaz — doğrudan `LexiCode-Setup.exe` ile kurar.
- Inno Setup: masaüstü kısayolu, Başlat menüsü girişi, kaldırma desteği sağlar.
- Dosyalar: `LexiCode.spec`, `installer/LexiCode.iss`

### 8. pytest — Test
**Ne yapar:** API endpoint'lerinin doğru çalıştığını otomatik olarak kontrol eder.
**Neden seçildi:**
- Python'un en popüler test framework'ü, basit ve okunabilir.
- Dosya: `features/tests/test_api.py`

---

## Kurulum Adımları (Geliştirici)

```bash
# 1. Python 3.14 kur (python.org)
# 2. Proje klasörüne gel
cd lexicode

# 3. Sanal ortam oluştur ve aktif et
python -m venv .venv
.venv\Scripts\activate

# 4. Bağımlılıkları kur
pip install -r requirements.txt

# 5. Ortam değişkenlerini ayarla (opsiyonel — AI Tutor için)
copy .env.example .env
# .env dosyasında ANTHROPIC_API_KEY değerini gir

# 6. Uygulamayı kaynak koddan çalıştır
python features/desktop_launcher.py

# 7. Testleri çalıştır
pytest features/tests/

# 8. EXE üret (opsiyonel — dağıtım için)
python -m PyInstaller --noconfirm --clean LexiCode.spec
# Inno Setup ile installer oluştur
ISCC.exe installer/LexiCode.iss
```

---

## Neden Bu Yığın?

| Kriter | Sonuç |
|---|---|
| **Öğrenme kolaylığı** | Python + HTML/CSS/JS — başlangıç seviyesi için ideal |
| **Kurulum maliyeti** | Sıfır — son kullanıcı sadece EXE çalıştırır |
| **AI entegrasyonu** | Claude API + fallback — her durumda çalışır |
| **Erişilebilirlik** | CSS ile disleksi dostu UX doğrudan uygulanır |
| **Dağıtım** | Tek dosya installer — GitHub'dan indir, kur, kullan |
