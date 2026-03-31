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

- Yayın / landing page: `https://replace-with-your-publish-link.example`
- Yerel çalışma adresi: `http://127.0.0.1:5000`

> Gönderimden önce üstteki iki placeholder linki kendi gerçek bağlantılarınla değiştirmen yeterli.

---

## 🚀 Installation & Usage

This project is distributed as a **ready-to-use desktop application**.
No technical setup or dependency installation is required.

### 📥 How to Use

1. Download `LexiCode-Setup.exe` from this repository (`dist/LexiCode-Setup.exe`).
2. Double-click the setup file to run the installer.
3. The application will automatically install itself on your system.
4. A shortcut will be created on your desktop.
5. Launch the application using the desktop shortcut.

### ✅ Features

* No need to install Python, Node.js, or any dependencies
* Fully packaged application
* One-click installation experience
* User-friendly and beginner-friendly setup

### ⚠️ Notes

* This application is currently supported on **Windows only**
* If Windows Defender shows a warning, click **"More info" -> "Run anyway"**

---

💡 The goal of this setup is to provide a **zero-setup experience**, allowing users to start using the application instantly without any technical knowledge.

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

