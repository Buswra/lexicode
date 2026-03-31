# LexiCode — Ürün Gereksinim Belgesi (PRD)

> Bu belge, kıdemli bir full stack developer bakış açısıyla, projeyi hiç bilmeyen birine anlatır gibi hazırlanmıştır.

---

## 📋 Uygulama Tarifi

LexiCode, **disleksili bireyler** ve **bilgisayar bilimleri (CS) öğrencileri** için tasarlanmış bir masaüstü İngilizce öğrenme uygulamasıdır. Kullanıcı sıkıcı metin yığınları yerine görsel zihin haritaları, akıllı kartlar ve yapay zeka destekli bir asistanla etkileşime girer. Uygulama tek bir EXE dosyasıyla Windows'a kurulur; Python, pip veya herhangi bir teknik bilgi gerektirmez.

## 👤 Kullanıcı Ne Yapar?

1. Uygulamayı `LexiCode-Setup.exe` ile kurar, masaüstü kısayoluna tıklar.
2. **CS İngilizcesi** veya **Günlük İngilizce** modunu seçer.
3. Kelime kartlarını inceler — her kartta kelime, fonetik, emoji, örnek cümle bulunur.
4. Kartı çevirerek Türkçe anlamı görür.
5. Seslendir butonuyla kelimeyi İngilizce/Türkçe dinler.
6. "Öğrendim" veya "Sonra" butonuna basarak ilerler.
7. Quiz ekranında çoktan seçmeli sorularla kendini test eder.
8. AI Tutor'a kendi cümlesini yazarak düzeltme ve geri bildirim alır.
9. İlerleme panelinden XP, streak, rozet ve analitik verilerini takip eder.

## 🤖 AI Ne Yapar?

Yapay zeka (Claude API) klasik bir chatbot gibi değil, **cesaretlendirici ve disleksi dostu bir İngilizce öğretmeni** olarak çalışır:

| Görev | Açıklama |
|---|---|
| **Cümle Düzeltme** | Kullanıcının kurduğu cümleyi yargılamadan inceler, hatayı formülle (S+V+O) açıklar |
| **Bağlam Üretimi** | Öğrenilen kelimeyi CS bağlamında (yazılım geliştirme süreçleri gibi) cümle içinde örnekler |
| **Mini Diyalog** | Kelime üzerinden kısa ve motive edici konuşma simülasyonu yapar |
| **Güvenli Fallback** | API anahtarı yoksa uygulama çökmez, temel düzeltme mesajıyla devam eder |

## 🖥️ Hangi Ekranlar Olacak?

| # | Ekran | Ne Gösterir |
|---|---|---|
| 1 | **Öğrenme (Flashcards)** | Kelime kartı, fonetik, emoji, örnek cümle, çevirme animasyonu |
| 2 | **Zihin Haritası (Mindmap)** | Kelimelerin anlamsal ilişkilerini görsel ağ yapısında gösterir |
| 3 | **AI Tutor** | Kullanıcının cümle kurduğu, hatalarının düzeltildiği sohbet ekranı |
| 4 | **Sınav (Quiz)** | Çoktan seçmeli sorular, 15 saniyelik zamanlayıcı, konfeti animasyonu |
| 5 | **İlerleme (Analytics)** | XP, streak, rozetler, öğrenme geçmişi, CSV dışa aktarma |
| 6 | **Erişilebilirlik Paneli** | Yazı boyutu, satır aralığı, yüksek kontrast modu ayarları |

## ⚙️ Teknoloji Yığını

| Katman | Teknoloji | Dosya |
|---|---|---|
| Backend | Python 3.14 + Flask | `features/app.py` |
| Desktop Shell | PySide6 + QtWebEngine | `features/desktop_launcher.py` |
| Frontend | HTML + CSS + JS (tek SPA) | `features/templates/index.html` |
| Veritabanı | SQLite | `%LOCALAPPDATA%/LexiCode/progress.db` |
| AI | Claude API + fallback | `features/app.py` (AI routes) |
| TTS | edge-tts + browser fallback | `features/services/tts_service.py` |
| Paketleme | PyInstaller + Inno Setup | `LexiCode.spec` + `installer/LexiCode.iss` |
| Test | pytest | `features/tests/test_api.py` |

## 📦 Dağıtım Modeli

- Son kullanıcı `LexiCode-Setup.exe` dosyasını indirir ve çift tıklar.
- Kurulum sihirbazı otomatik olarak `%LOCALAPPDATA%\Programs\LexiCode\` altına kurar.
- Masaüstü kısayolu ve Başlat menüsü girişi oluşturulur.
- Python, pip veya herhangi bir teknik bilgiye gerek yoktur.

## 📌 İlgili Belgeler

- **Görev listesi:** `tasks.md`
- **Kullanıcı akışı:** `user-flow.md`
- **Teknoloji seçimi:** `tech-stack.md`
- **Proje fikri:** `idea.md`