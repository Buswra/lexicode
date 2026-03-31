# 🧠 LexiCode

> **Disleksi dostu, AI destekli İngilizce öğrenme ve telaffuz pratiği uygulaması**

LexiCode; özellikle **CS İngilizcesi**, günlük kelime pratiği, doğru telaffuz ve motive edici öğrenme deneyimi için geliştirilmiş bir `Python + Flask + PySide6` projesidir.

---

## 📌 Problem

Birçok İngilizce öğrenme aracı disleksi dostu değildir ve teknik İngilizceye yeterince odaklanmaz. LexiCode bu boşluğu; büyük, sade ve destekleyici bir arayüzle, **AI destekli düzeltme** ve **Türkçe/İngilizce neural seslendirme** ile kapatmayı hedefler.

## 🎯 Ne yapar?

- kelime kartlarıyla öğretir
- İngilizce ve Türkçe telaffuz sunar
- AI Tutor ile cümle düzeltir ve mini diyalog kurar
- ilerleme, rozet ve tekrar mantığı ile öğrenmeyi takip eder

---

## 🎥 Demo Video

- Loom / YouTube: `https://www.loom.com/share/REPLACE-WITH-YOUR-DEMO-LINK`

## 🌍 Yayın Linki

- **GitHub Releases:** [LexiCode-Setup.exe İndir](https://github.com/Buswra/lexicode/releases/latest)
- **GitHub Repo:** https://github.com/Buswra/lexicode
- Yerel çalışma adresi: `http://127.0.0.1:5000`

---

## 🚀 Kurulum (Son Kullanıcı İçin)

Bu proje **hazır masaüstü uygulaması** olarak dağıtılır. Python, pip veya herhangi bir teknik bilgi gerekmez.

### 📥 Nasıl Kurulur?

1. [**LexiCode-Setup.exe**](https://github.com/Buswra/lexicode/releases/latest) dosyasını indirin
2. İndirilen dosyaya çift tıklayın
3. Kurulum sihirbazını takip edin: **İleri → İleri → Kur**
4. Masaüstünde oluşan **LexiCode** kısayoluna tıklayın
5. Uygulama açılır — öğrenmeye başlayın! 🎉

### ✅ Özellikler

- 📚 **Kelime Kartları (Flashcards)** — CS ve günlük İngilizce kelimeleri
- 🔊 **Neural Seslendirme** — İngilizce ve Türkçe telaffuz (edge-tts)
- 🤖 **AI Tutor** — Claude API ile cümle düzeltme, bağlam üretimi, mini diyalog
- 📝 **Quiz Sistemi** — 15 saniyelik zamanlayıcı, konfeti animasyonu
- 🧠 **Zihin Haritası** — Kelime ilişkilerini görselleştirir
- 📊 **İlerleme Takibi** — XP, streak, 11 rozet, öğrenme geçmişi
- ♿ **Erişilebilirlik Paneli** — Yazı boyutu, satır aralığı, yüksek kontrast modu
- 🔍 **Arama ve Sıralama** — Kelimeyi anında bul
- 📤 **CSV Dışa Aktarma** — İlerleme verisini indir

### ⚠️ Notlar

- Uygulama şu anda sadece **Windows** üzerinde desteklenmektedir
- Windows Defender uyarı verirse: **"Daha fazla bilgi" → "Yine de çalıştır"** tıklayın
- AI Tutor için Claude API anahtarı opsiyoneldir — olmasa da uygulama çalışır

---

## 🛠️ Geliştirici Kurulumu (Kaynak Koddan Çalıştırma)

Projeyi kaynak koddan çalıştırmak isteyen geliştiriciler için:

```bash
# 1. Repoyu klonla
git clone https://github.com/Buswra/lexicode.git
cd lexicode

# 2. Sanal ortam oluştur
python -m venv .venv
.venv\Scripts\activate

# 3. Bağımlılıkları kur
pip install -r requirements.txt

# 4. (Opsiyonel) AI Tutor için .env dosyası oluştur
copy .env.example .env
# .env dosyasında ANTHROPIC_API_KEY değerini gir

# 5. Uygulamayı çalıştır
python features/desktop_launcher.py

# 6. Testleri çalıştır
pytest features/tests/
```

---

## 📁 GitHub Repo Yapısı

```text
lexicode/
├─ README.md
├─ prd.md
├─ tasks.md
├─ idea.md
├─ user-flow.md
├─ tech-stack.md
├─ .cursorrules
├─ features/
│  ├─ app.py
│  ├─ config.py
│  ├─ desktop_launcher.py
│  ├─ services/
│  ├─ utils/
│  ├─ templates/
│  ├─ static/
│  ├─ tests/
│  ├─ words.py
│  └─ words_cs.py
├─ agents/
│  └─ README.md
├─ assets/
│  └─ README.md
├─ requirements.txt
├─ pyproject.toml
├─ LexiCode.spec
├─ dist/
│  └─ LexiCode-Setup.exe
└─ installer/
	└─ LexiCode.iss
```

---

## 🧰 Kullanılan Teknolojiler

| Katman | Teknoloji |
|---|---|
| Backend | `Python`, `Flask` |
| Arayüz | `HTML`, `CSS`, `JavaScript` |
| Desktop shell | `PySide6` + `QtWebEngine` |
| Veri | `SQLite` |
| AI | `Claude API` / güvenli fallback |
| TTS | `edge-tts` + browser fallback |
| Paketleme | `PyInstaller` |
| Test | `pytest` |

---

## 📂 Dokümanlar

- `idea.md` → problem, hedef kullanıcı ve AI rolü
- `user-flow.md` → kullanıcı akışı
- `tech-stack.md` → teknoloji seçimi ve gerekçeleri
- `features/` → tüm kaynak kodları
- `agents/` → opsiyonel agent / otomasyon içeriği
- `assets/` → ekran görüntüsü, logo, demo görselleri

---

Hazırlayan: Büşranur Açıkgöz

